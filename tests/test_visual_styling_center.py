"""Visual Styling Center YAML, configuration, and JS runtime contract."""
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "Visual-Styling-Center" / "Visual-Styling-Center.md"
REQUIRED = """height_multiplier inner_padding icon_vertical_margin subbutton_horizontal_margin subbutton_row_spacing subbutton_column_spacing icon_size_multiplier icon_background_ratio subicon_size_multiplier subbutton_background_ratio enable_icon_helper apply_to_main_icon apply_to_sub_icons helper_color manual_helper_color helper_opacity helper_size_ratio enable_helper_fade fade_strength enable_slider_helper slider_helper_color manual_slider_helper_color slider_helper_opacity slider_helper_size_ratio enable_slider_helper_fade slider_fade_strength hide_icon_background hide_subbutton_background custom_icon_color manual_icon_color custom_subicon_color manual_subicon_color custom_icon_background_color manual_icon_background_color custom_subbutton_background_color manual_subbutton_background_color enable_entity_colored_main_icon enable_entity_colored_subicons enable_function_button_color function_button_color manual_function_button_color enable_gradient gradient_target gradient_entity disable_default_gradient slider_bg_opacity enable_interaction_effects custom_card_background_color manual_card_background_color card_background_opacity card_border_radius icon_border_radius subbutton_border_radius custom_name_color manual_name_color name_font_size custom_state_color manual_state_color state_font_size use_theme_state_colors gradient_angle""".split()

def fields(schema):
    result = []
    for item in schema:
        if "selector" in item:
            result.append(item["name"])
        result.extend(fields(item.get("schema", [])))
    return result

class VisualStylingCenterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = MODULE.read_text(encoding="utf-8")
        marker = chr(96) * 3
        blocks = re.findall(re.escape(marker) + r"yaml\s*\n(.*?)\n" + re.escape(marker), cls.text, re.S)
        cls.blocks = [yaml.safe_load(x) for x in blocks]
        cls.module = next(x["visual_styling_center"] for x in cls.blocks
                          if "visual_styling_center" in x and "code" in x["visual_styling_center"])

    def test_valid_markdown_and_yaml(self):
        self.assertEqual(self.text.count(chr(96) * 3) % 2, 0)
        self.assertEqual(len(self.blocks), 4)
        self.assertEqual(self.module["name"], "Visual Styling Center")
        self.assertGreater(len(self.module["code"]), 15000)
        self.assertNotIn("\x97", self.text)
        self.assertEqual(self.module["version"], "v2026.10.29")
        self.assertNotIn("Ã", self.text)

    def test_config_id_and_all_editor_keys_unchanged(self):
        names = fields(self.module["editor"])
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(REQUIRED))
        self.assertIn("cover", self.module["unsupported"])
        diff = (ROOT / "docs/upstream/bubble-card/CHANNEL-DIFF.md").read_text(encoding="utf-8")
        self.assertIn("v3.4.2", diff)

    def test_no_obsolete_polling_or_config_mutation(self):
        code = self.module["code"]
        for forbidden in ("subscribeEvents(", "_hasInitialSliderUpdate",
                          "config.gradient_target =", "config.gradient_entity ="):
            self.assertNotIn(forbidden, code)

    def test_upstream_group_index_and_lifecycle_contract(self):
        # This test deliberately detects incompatible upstream changes.
        upstream = ROOT / "docs/upstream/bubble-card/stable/src"
        changes = (upstream / "components/sub-button/changes.js").read_text(encoding="utf-8")
        utils = (upstream / "components/sub-button/utils.js").read_text(encoding="utf-8")
        style = (upstream / "tools/style-processor.js").read_text(encoding="utf-8")
        self.assertRegex(changes, r"mainExplicitGroups,\s*\.\.\.mainNonGroupGroups")
        self.assertRegex(changes, r"bottomGroups,\s*\.\.\.bottomNonGroupGroups")
        self.assertIn("const entity = subButton.entity ?? context.config.entity", utils)
        self.assertIn("trackedHass(context)", style)
        self.assertIn("registerModuleTeardown(context", style)
        self.assertIn("hasChanged(context", style)

    def test_js_regression_scenarios(self):
        code = self.module["code"]
        marker = chr(36) + chr(123) + "(() => {"
        start = code.index(marker)
        end = code.index("})()}", start) + len("})()}")
        expression = code[start + 2:end - 1]
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "expression.js"
            script.write_text("function runner(card,hass,hasChanged,onTeardown){ return " + expression + "; }\n",
                              encoding="utf-8")
            check = subprocess.run(["node", "--check", str(script)],
                                   capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stderr)
            run = subprocess.run(["node", str(ROOT / "tests" / "vsc_runtime_test.cjs"), str(script)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
