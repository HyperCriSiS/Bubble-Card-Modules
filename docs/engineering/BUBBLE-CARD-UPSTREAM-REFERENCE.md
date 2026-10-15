# Bubble Card upstream reference

## Purpose

This repository automatically maintains a searchable, read-only mirror of the technical
Bubble Card sources relevant to our Home Assistant modules. It does not modify any
module code or inject upstream JavaScript into a build or test pipeline.

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
commits do not cause extra commits. CHANNEL-DIFF.md lists differences between these
channels. UPDATES.md records reference refreshes.

## Local commands (optional)

    python3 -m unittest discover -s tests -p 'test_bubble_card_reference.py' -v
    python3 scripts/sync_bubble_card_reference.py --dry-run
    python3 scripts/sync_bubble_card_reference.py
    python3 scripts/sync_bubble_card_reference.py --verify

Python 3.10+ and its standard library suffice. GITHUB_TOKEN is optional locally
but recommended to avoid GitHub's unauthenticated API rate limit.

If upstream changes are incompatible, a source is missing, the tree is truncated,
a download fails or a hash is wrong, synchronization fails without replacing
the existing reference directory.

## Scheduled, SHA-verified synchronization through protected main

GitHub Action: .github/workflows/sync-bubble-card-reference.yml

- Runs daily and supports an optional manual `workflow_dispatch`.
- Tests the synchronizer and verifies every mirrored Git blob SHA before publishing.
- Commits **only** files under `docs/upstream/bubble-card/` to `automation/bubble-card-upstream-reference`.
- Creates or updates a PR into `main`; does not bypass PR protection or merge automatically.
- No changed source: no commit or PR needed.
- Requires `contents: write` and `pull-requests: write` permissions.
- **Repository setting required:** GitHub Actions must be allowed to create pull requests. If that setting is disabled, the verified branch is still pushed, but the PR creation fails visibly. A user with GitHub permissions must create the PR or enable this GitHub Actions setting.
- Changes to the synchronizer itself require a separate reviewed PR.
- `GITHUB_TOKEN`-generated pull requests generally do not trigger downstream PR workflows. Before merging an automated reference PR, verify the snapshot hashes and run any required checks explicitly.

A passing synchronizer step does not prove the reference on `main` is current. Always check the newest sync run and pending reference PR when validating against a newly released upstream version.

## Where to find the sources

- docs/upstream/bubble-card/README.md: reference index
- docs/upstream/bubble-card/stable/: newest stable Bubble Card release
- docs/upstream/bubble-card/main/: newest relevant upstream main files
- docs/upstream/bubble-card/CHANNEL-DIFF.md: stable/main comparison
- docs/upstream/bubble-card/UPDATES.md: update history

All mirrored source files are untrusted reference material and must not be
executed by the workflow.
