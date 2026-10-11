# Bubble Card upstream reference

## Purpose

This repository maintains a searchable, read-only mirror of the technical Bubble Card
sources relevant to our Home Assistant modules. It does not modify any module code
or inject upstream JavaScript into a build or test pipeline.

Original source: https://github.com/Clooos/Bubble-Card

## Source selection

- Original LICENSE, official README, DEVELOPERS guide, package/hacs metadata
- src/modules: module schema, parser, registration, editor, lifecycle
- src/components/sub-button: component implementation, sub-button selectors and styles
- src/cards/sub-buttons: sub-button card integration
- Selected src/tools files: HA conditions, styling, cleanup and runtime helpers
- Selected src/editor, src/cards/button, src/components/base-card entry points

Only JS, CSS, Markdown and JSON source text is collected. Tests, dist bundles,
translations, media assets and other unrelated files are excluded.
Each mirrored byte is compared with the Git blob SHA from the upstream tree.

## Two separate channels

- stable: latest published non-prerelease GitHub release
- main: upstream main development branch

Each channel has its own manifest.json with source_commit_sha and SHA for every file.
The main snapshot changes only when relevant selected sources change. Unrelated upstream
commits do not cause PR churn. CHANNEL-DIFF.md lists differences between these channels.
UPDATES.md records reference refreshes.

## Local commands

    python3 -m unittest discover -s tests -p 'test_bubble_card_reference.py' -v
    python3 scripts/sync_bubble_card_reference.py --dry-run
    python3 scripts/sync_bubble_card_reference.py
    python3 scripts/sync_bubble_card_reference.py --verify

Python 3.10+ and its standard library suffice. GITHUB_TOKEN is optional locally
but recommended to avoid GitHub's unauthenticated API rate limit.

If upstream changes are incompatible, a source is missing, the tree is truncated,
a download fails or a hash is wrong, synchronization fails without replacing
the existing reference directory.

## Automation

GitHub Action: .github/workflows/sync-bubble-card-reference.yml

- Every day at 03:17 UTC, plus manual workflow_dispatch
- Test synchronizer, fetch stable and main, verify all files
- Create/update a reviewable pull request on automation/bubble-card-upstream
- Only docs/upstream/bubble-card changes get committed
- No automatic merge and no automatic changes to Badgy-Conditions
- A read-only pull request CI workflow validates the tooling

Required GitHub repository setting: Settings / Actions / General /
Workflow permissions / Allow GitHub Actions to create and approve pull requests.
The sync job has explicit contents:write and pull-requests:write permissions.

## Review procedure

1. Read the new channel manifests, official module specification and channel diff.
2. Check changes in module parser/editor and sub-button DOM/CSS.
3. Assess compatibility risks to existing module configuration values.
4. Merge the upstream-reference PR only after review.

The mirrored upstream code is untrusted reference material and must not be run
by the workflow.
