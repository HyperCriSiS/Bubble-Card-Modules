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

## Fully automatic synchronization

GitHub Action: .github/workflows/sync-bubble-card-reference.yml

- Runs daily at **03:17 UTC**, and supports an optional manual workflow_dispatch.
- Fetches both upstream channels, tests the synchronizer and verifies every file.
- Automatically commits **only** changed files beneath docs/upstream/bubble-card/
  directly to the main branch. No pull request, approval or manual merge required.
- If no relevant source changed, produces no commit.
- Uses a GitHub-provided token with contents:write; no custom PAT required.
- Never edits Badgy-Conditions or other executable module files.
- Push is fast-forward only; if main changes concurrently, the job fails safely
  rather than overwriting changes (the next scheduled run can retry).
- Failures are visible in GitHub Actions. They do not replace a good reference
  with an incomplete or unverified download.

Only changes to the synchronization **implementation** are proposed and reviewed
via pull requests using the separate read-only CI workflow.
GitHub Actions commits made with GITHUB_TOKEN do not normally trigger other
workflows, so this sync job runs its checks and verifies all snapshot hashes
before committing.

## Where to find the sources

- docs/upstream/bubble-card/README.md: reference index
- docs/upstream/bubble-card/stable/: newest stable Bubble Card release
- docs/upstream/bubble-card/main/: newest relevant upstream main files
- docs/upstream/bubble-card/CHANNEL-DIFF.md: stable/main comparison
- docs/upstream/bubble-card/UPDATES.md: update history

All mirrored source files are untrusted reference material and must not be
executed by the workflow.
