# Agent instructions

- Start with [README.md](README.md), [documentation navigation](docs/DOCUMENTATION.md), and [current work](docs/engineering/CURRENT-WORK.md).
- **Bubble Card compatibility:** Before modifying module JavaScript, CSS, selectors, or editor schemas, read [the upstream reference guide](docs/engineering/BUBBLE-CARD-UPSTREAM-REFERENCE.md) and the [mirrored source index](docs/upstream/bubble-card/README.md). Compare `docs/upstream/bubble-card/stable/` (released version) with `docs/upstream/bubble-card/main/` (development) and check `CHANNEL-DIFF.md`. Use the mirrored `src/modules/`, `src/components/sub-button/`, and `src/cards/` sources as the primary API and lifecycle reference.
- The upstream mirror is read-only and automatically updated. Do not modify the snapshots by hand or execute mirrored code.
- No dedicated repository-wide `ROADMAP.md` is currently present. Do not invent project completion claims or create one automatically.
- Preserve existing configuration IDs, editor keys, defaults, module behavior, release paths, and branch conventions. Any incompatible change needs an explicit migration plan.
- Make implementation changes in a reviewable pull request and verify applicable checks.
- Each module lives in its own root directory. Keep module-specific contracts and documentation intact.

## README style

- Title, bold tagline, one badge row (at most six).
- Every `##` heading starts with an emoji. Fixed ones: ✨ Features,
  📦 Installation, 🚀 Usage, ⚙️ Configuration, 🖼️ Screenshots,
  🩺 Troubleshooting, 💬 Support, 🙏 Credits, 📄 License. Other sections get
  a fitting emoji of their own, never one twice per file.
- The root README is an overview: install path first, then one 🧩 table row
  per module. Module details stay in each module's own documentation.
- GitHub alerts for warnings.

## Branches and releases

- Default branch: `main`. Pull requests are squash merged.
- A change to the README alone is pushed straight to `main`, without a pull request.
