# Agent instructions

- Start with [README.md](README.md), [documentation navigation](docs/DOCUMENTATION.md), and [current work](docs/engineering/CURRENT-WORK.md).
- **Bubble Card compatibility:** Before modifying module JavaScript, CSS, selectors, or editor schemas, read [the upstream reference guide](docs/engineering/BUBBLE-CARD-UPSTREAM-REFERENCE.md) and the [mirrored source index](docs/upstream/bubble-card/README.md). Compare `docs/upstream/bubble-card/stable/` (released version) with `docs/upstream/bubble-card/main/` (development) and check `CHANNEL-DIFF.md`. Use the mirrored `src/modules/`, `src/components/sub-button/`, and `src/cards/` sources as the primary API and lifecycle reference.
- The upstream mirror is read-only and automatically updated. Do not modify the snapshots by hand or execute mirrored code.
- No dedicated repository-wide `ROADMAP.md` is currently present. Do not invent project completion claims or create one automatically.
- Preserve existing configuration IDs, editor keys, defaults, module behavior, release paths, and branch conventions. Any incompatible change needs an explicit migration plan.
- Make implementation changes in a reviewable pull request and verify applicable checks.
- Each module lives in its own root directory. Keep module-specific contracts and documentation intact.
