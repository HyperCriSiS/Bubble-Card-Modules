# Bubble Card upstream reference

## Purpose

This repository keeps a verified, read-only mirror of technical Bubble Card sources used to review our custom Home Assistant modules.

Original: https://github.com/Clooos/Bubble-Card

## Sources

- Stable: latest non-prerelease GitHub release
- Main: upstream development branch
- docs/upstream/bubble-card/README.md: source index and manifests
- docs/upstream/bubble-card/CHANNEL-DIFF.md: comparison
- docs/upstream/bubble-card/UPDATES.md: refresh history

The synchronizer uses upstream Git blob hashes and fails without publishing if any selected source cannot be verified. Only selected JS, CSS, JSON, and documentation files are mirrored. These files are reference material, not executable build inputs.

## Synchronization

Workflow: `.github/workflows/sync-bubble-card-reference.yml`. Daily schedule and manual dispatch.

1. Check out protected `main`, run synchronizer tests.
2. Fetch both snapshots and verify every mirrored file.
3. If changes exist, commit **only** `docs/upstream/bubble-card/` to `automation/bubble-card-upstream-reference`.
4. Create or update a synchronization pull request into `main`.
5. Merge using the repository's ordinary branch rules. No direct push to `main` or policy bypass.

The workflow requires `contents: write` and `pull-requests: write` permission for `GITHUB_TOKEN`. If GitHub Actions is not allowed to create PRs in repository settings, the branch push can succeed but the PR-create step will fail explicitly until this permission is enabled. A failed sync must not be treated as an up-to-date reference.

**Important:** This process automatically maintains an update PR; it does **not** automatically merge into protected `main`. Consequently, check the latest workflow runs and open sync PR before relying on the mirrored version. Automation-based merging can only be introduced separately if the existing protection rules permit it.

## Local verification

```bash
python3 -m unittest discover -s tests -p 'test_bubble_card_reference.py' -v
python3 scripts/sync_bubble_card_reference.py --dry-run
python3 scripts/sync_bubble_card_reference.py --verify
```

Python 3.10+ standard library is sufficient. The optional `GITHUB_TOKEN` avoids unauthenticated GitHub API rate limits.
