#!/usr/bin/env python3
"""Validate Badgy YAML, JS syntax, and saved configuration compatibility."""
import re
import subprocess
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = "Badgy-Conditions/Badgy-Conditions.md"
MODULE = "badgy-condition-helper"


def read_module(markdown):
    fence = chr(96) * 3
    expression = (
        r"<summary>.*?Get this Module.*?</summary>[\s\S]*?" +
        re.escape(fence) + r"yaml\s*\n([\s\S]*?)\n" + re.escape(fence)
    )
    match = re.search(expression, markdown)
    assert match, "Module download YAML code block not found"
    value = yaml.safe_load(match.group(1))
    assert isinstance(value, dict) and MODULE in value
    assert isinstance(value[MODULE].get("editor"), list)
    return value[MODULE]


def paths(fields, prefix=()):
    result = set()
    for field in fields:
        if field.get("type") in ("expandable", "grid"):
            name = field.get("name")
            result.update(paths(
                field["schema"],
                prefix + ((str(name),) if name is not None else ())
            ))
        elif "name" in field:
            result.add(prefix + (str(field["name"]),))
    return result


def main():
    md = (ROOT / PATH).read_text(encoding="utf-8")
    new = read_module(md)
    # Parallel install must have a distinct ID but exactly the same runtime/editor.
    beta_id = "badgy-condition-helper-beta"
    beta = yaml.safe_load(
        (ROOT / "Badgy-Conditions/Badgy-Conditions-beta.yaml").read_text(encoding="utf-8")
    )
    assert list(beta) == [beta_id]
    isolated = beta[beta_id]
    assert isolated["name"] == "Badgy Condition Helper (Beta)"
    assert isolated["version"] == new["version"]
    assert isolated["editor"] == new["editor"]
    assert isolated["code"] == new["code"].replace(MODULE, beta_id)
    print("Verified isolated test module matches source without sharing its module ID")
    old_md = subprocess.check_output(
        ["git", "show", "origin/main:" + PATH], cwd=ROOT, text=True, errors="replace"
    )
    old = read_module(old_md)
    existing = paths(old["editor"])
    updated = paths(new["editor"])
    lost = sorted(existing - updated)
    assert not lost, "Legacy configuration fields lost: " + repr(lost[:50])
    assert len(existing) >= 100
    required = {
        ("entity_badges", "main", "entity"),
        ("icon_badges", "main", "icon"),
        ("entity_badge_effects", "main", "effect"),
        ("icon_badge_effects", "main", "effect"),
        ("icon_colors", "main_icon", "color"),
        ("icons", "main_icon", "icon"),
        ("card_effects", "effect"),
        ("global_defaults", "badge_scale"),
        ("sub_buttons_background", "0", "rules"),
        ("icon_colors", "sub_button_icon", "0", "color"),
    }
    assert required <= updated, "New fields missing: " + repr(sorted(required - updated))
    code = new["code"]
    node_check = (
        "const fs=require('fs');const code=fs.readFileSync(0,'utf8');"
        "new Function('hass','entity','state','card','checkConditionsMet',"
        "'hasChanged','onTeardown','return '+String.fromCharCode(96)+"
        "code+String.fromCharCode(96)+';');"
        "console.log('Bubble Card template parses as JavaScript');"
    )
    subprocess.run(["node", "-e", node_check], input=code, text=True, check=True)
    subprocess.run(["node", "tests/badgy_runtime.cjs"], input=code, text=True, check=True)
    for feature in ("formatBadgeState", "processMainBadges", "processIconsAndColors", "processCardGlow"):
        assert feature in code, "Missing feature: " + feature
    assert "transform: scale(var(--badge-scale" not in code
    print("Validated YAML, JS template and %d unchanged existing config paths; %d total fields" %
          (len(existing), len(updated)))


if __name__ == "__main__":
    main()
