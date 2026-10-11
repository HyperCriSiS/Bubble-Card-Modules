#!/usr/bin/env python3
"""Synchronize selected Bubble Card sources as verified, read-only references."""
import argparse
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import Request, urlopen

UPSTREAM = "Clooos/Bubble-Card"
ROOT = Path("docs/upstream/bubble-card")
CHANNELS = ("stable", "main")
FOLDERS = ("src/modules/", "src/components/sub-button/", "src/cards/sub-buttons/")
EXTRAS = {
    "README.md", "DEVELOPERS.md", "LICENSE", "package.json", "hacs.json",
    "src/cards/button/editor.js", "src/cards/button/create.js",
    "src/cards/button/changes.js", "src/cards/button/styles.css",
    "src/components/base-card/styles.css", "src/editor/bubble-card-editor.js",
    "src/editor/styles.css", "src/tools/ha-conditions.js",
    "src/tools/validate-condition.js", "src/tools/style-processor.js",
    "src/tools/style.js", "src/tools/module-gate.js",
    "src/tools/module-teardown.js", "src/tools/preview-badge.js",
    "src/tools/render-template.js",
}
REQUIRED = {
    "README.md", "LICENSE", "src/modules/module-documentation.md",
    "src/modules/parser.js", "src/modules/module-editor.js",
    "src/modules/yaml-schema.js", "src/components/sub-button/create.js",
    "src/components/sub-button/styles.css", "src/cards/sub-buttons/editor.js",
    "src/tools/ha-conditions.js",
}


def wanted(path):
    name = PurePosixPath(path).name
    return path in EXTRAS or (
        path.startswith(FOLDERS)
        and path.endswith((".js", ".css", ".md", ".json"))
        and not name.endswith((".test.js", ".test.css", ".spec.js"))
    )


def blob_sha(content):
    return hashlib.sha1(("blob %d\0" % len(content)).encode() + content).hexdigest()


def fetch(url):
    headers = {"User-Agent": "Bubble-Card-Modules-reference", "Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(url, headers=headers), timeout=45) as response:
        data = response.read(8_000_001)
    if len(data) > 8_000_000:
        raise RuntimeError("Response exceeded safe download limit")
    return data


def api(path):
    return json.loads(fetch("https://api.github.com/repos/" + UPSTREAM + "/" + path))


def get_upstream(channel):
    if channel == "stable":
        ref = api("releases/latest")["tag_name"]
    else:
        ref = "main"
    commit = api("commits/" + quote(ref, safe=""))
    sha, tree_sha = commit["sha"], commit["commit"]["tree"]["sha"]
    tree = api("git/trees/" + tree_sha + "?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("Refusing truncated upstream file tree")
    files = []
    for entry in tree["tree"]:
        path = entry["path"]
        if entry["type"] != "blob" or not wanted(path):
            continue
        if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
            raise RuntimeError("Unsafe upstream path: " + path)
        if entry["size"] > 1_000_000:
            raise RuntimeError("Source exceeds file size limit: " + path)
        files.append({"path": path, "sha": entry["sha"], "bytes": entry["size"]})
    files.sort(key=lambda e: e["path"])
    missing = REQUIRED - {e["path"] for e in files}
    if missing or not files or len(files) > 130:
        raise RuntimeError("Unexpected upstream source selection: " + str(sorted(missing)))
    return ref, sha, tree_sha, files


def get_manifest(channel, root=ROOT):
    path = root / channel / "manifest.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def check_channel(channel, root=ROOT):
    manifest = get_manifest(channel, root)
    if not isinstance(manifest, dict) or not manifest.get("tracked_files"):
        raise RuntimeError("Missing manifest for " + channel)
    expected = {"manifest.json"}
    for entry in manifest["tracked_files"]:
        name = entry["path"]
        if not wanted(name) or name in expected or ".." in PurePosixPath(name).parts:
            raise RuntimeError("Invalid manifest source: " + name)
        expected.add(name)
        path = root / channel / name
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("Missing or symlinked source: " + name)
        data = path.read_bytes()
        if len(data) != entry["bytes"] or blob_sha(data) != entry["sha"]:
            raise RuntimeError("Hash mismatch: " + name)
    actual = {
        p.relative_to(root / channel).as_posix()
        for p in (root / channel).rglob("*") if p.is_file()
    }
    if actual != expected:
        raise RuntimeError("Unexpected snapshot files for " + channel)


def change_list(previous, current):
    old = {e["path"]: e["sha"] for e in (previous or {}).get("tracked_files", [])}
    new = {e["path"]: e["sha"] for e in current["tracked_files"]}
    return [
        ("added " if path not in old else "removed " if path not in new else "modified ") + path
        for path in sorted(old.keys() | new.keys()) if old.get(path) != new.get(path)
    ]


def write_channel(channel, stage, cache):
    ref, sha, tree_sha, files = get_upstream(channel)
    old = get_manifest(channel)
    previous = ROOT / channel
    dest = stage / channel
    same = (
        isinstance(old, dict) and old.get("tracked_files") == files
        and (channel == "main" or old.get("release_tag") == ref)
    )
    if same:
        try:
            check_channel(channel)
            shutil.copytree(previous, dest)
            print(channel + ": relevant upstream sources unchanged")
            return old, False
        except RuntimeError:
            print(channel + ": repairing invalid snapshot")
    dest.mkdir()
    for entry in files:
        name = entry["path"]
        data = cache.get(entry["sha"])
        if data is None:
            local = previous / name
            if local.is_file() and not local.is_symlink():
                candidate = local.read_bytes()
                if blob_sha(candidate) == entry["sha"]:
                    data = candidate
            if data is None:
                url = "https://raw.githubusercontent.com/" + UPSTREAM + "/" + sha + "/" + quote(name, safe="/")
                data = fetch(url)
            if blob_sha(data) != entry["sha"] or len(data) != entry["bytes"]:
                raise RuntimeError("Upstream SHA/size verification failed: " + name)
            data.decode("utf-8")
            cache[entry["sha"]] = data
        out = dest / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
    manifest = {
        "upstream_repository": UPSTREAM, "channel": channel,
        "release_tag": ref if channel == "stable" else None,
        "source_commit_sha": sha, "source_tree_sha": tree_sha,
        "tracked_files": files,
    }
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest, True


def index(manifests):
    lines = [
        "# Bubble Card upstream reference", "",
        "Read-only, SHA-verified sources from https://github.com/Clooos/Bubble-Card.",
        "These copies are not dependencies or executable build inputs.", "",
        "| Channel | Reference commit | Files | Module documentation |",
        "| --- | --- | ---: | --- |",
    ]
    for channel in CHANNELS:
        m = manifests[channel]
        label = m["release_tag"] or m["source_commit_sha"][:12]
        lines.append(
            "| [" + channel + "](./" + channel + "/manifest.json) | [" + label +
            "](https://github.com/" + UPSTREAM + "/tree/" + m["source_commit_sha"] + ") | " +
            str(len(m["tracked_files"])) + " | [Specification](./" + channel +
            "/src/modules/module-documentation.md) |"
        )
    lines += [
        "", "## Reference layout", "",
        "- CHANNEL/src/modules/ : parser, editor schema, lifecycle",
        "- CHANNEL/src/components/sub-button/ : sub-button DOM and CSS",
        "- CHANNEL/src/cards/sub-buttons/ : card integration",
        "- CHANNEL/src/tools/ : conditions and style helpers",
        "- CHANNEL/README.md : official public documentation", "",
        "CHANNEL means stable or main. The manifest records the last commit that changed",
        "a tracked source. Unrelated upstream commits do not cause noisy pull requests.",
        "See CHANNEL-DIFF.md for stable/main differences and UPDATES.md for update history.", "",
        "Update: python3 scripts/sync_bubble_card_reference.py",
        "Verify offline: python3 scripts/sync_bubble_card_reference.py --verify", "",
    ]
    return "\n".join(lines)


def compare(manifests):
    a, b = manifests["stable"], manifests["main"]
    changes = change_list(a, b)
    return "\n".join([
        "# Stable vs. main source comparison", "",
        "Stable: " + a["release_tag"] + " (" + a["source_commit_sha"] + ")",
        "Main: " + b["source_commit_sha"], "",
        str(len(changes)) + " tracked source differences", "",
        *("- " + item for item in changes),
        "" if changes else "No differences in the tracked source files.",
        "",
    ])


def file_map(path):
    if not path.exists():
        return {}
    return {p.relative_to(path).as_posix(): p.read_bytes() for p in path.rglob("*") if p.is_file()}


def synchronize(dry_run=False):
    with tempfile.TemporaryDirectory(prefix="bubble-card-upstream-") as tmp:
        stage = Path(tmp) / "snapshot"
        stage.mkdir()
        cache, manifests, events = {}, {}, []
        for channel in CHANNELS:
            before = get_manifest(channel)
            manifest, updated = write_channel(channel, stage, cache)
            manifests[channel] = manifest
            if updated:
                events.append(
                    "- " + datetime.now(timezone.utc).date().isoformat() + " | " + channel +
                    " | " + manifest["source_commit_sha"][:12] +
                    " | " + str(len(change_list(before, manifest))) + " selected source changes"
                )
        (stage / "README.md").write_text(index(manifests), encoding="utf-8")
        (stage / "CHANNEL-DIFF.md").write_text(compare(manifests), encoding="utf-8")
        history = ROOT / "UPDATES.md"
        content = history.read_text(encoding="utf-8") if history.is_file() else "# Reference updates\n\n"
        if events:
            content += "\n".join(events) + "\n"
        (stage / "UPDATES.md").write_text(content, encoding="utf-8")
        for channel in CHANNELS:
            check_channel(channel, stage)
        old, new = file_map(ROOT), file_map(stage)
        changed = sorted(p for p in old.keys() | new.keys() if old.get(p) != new.get(p))
        print("Changed reference files: " + str(len(changed)))
        for path in changed[:20]:
            print("  " + path)
        if not changed or dry_run:
            return
        if ROOT.exists():
            shutil.rmtree(ROOT)
        ROOT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(stage, ROOT)
        print("Snapshots updated and verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        for channel in CHANNELS:
            check_channel(channel)
        print("Both upstream snapshots verified.")
    else:
        synchronize(dry_run=args.dry_run)
