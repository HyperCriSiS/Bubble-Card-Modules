# Visual Styling Center — audit and automated test evidence (2026-10-12)

## Basis
- Read-only reference: Bubble Card stable v3.4.2 at docs/upstream/bubble-card/stable/.
- Module ID: visual_styling_center. All 46 legacy editor keys remain unchanged.
- Proposed changes live in pull request #7; no module release or merge is implied.

## Implemented
- Removed obsolete slider initialization stub: Bubble Card manages native slider updates.
- Repaired embedded YAML and Markdown structure, version metadata and invalid UTF-8-like multiplication units.
- Restored module-owned icon inline colors on state/option changes; supported legacy and sectioned/group sub-button config.
- Replaced problematic numeric || defaults with ??; stopped mutating this.config.
- Fixed scene/script/automation detection and optional function colors.
- Removed redundant inline sub-button background writes.
- Module defaults and color resets now restore previously selected backgrounds.
- Linked AGENTS.md to the verified local upstream mirror.

## Verification
- Python/PyYAML checks: module parses, 46 editor keys stable and JS syntax valid.
- Node.js mock runtime: colors, state changes, groups, gradient members, zero values, no config mutation.
- Chromium DOM integration: actual computed style and JS execution, against exact mirrored upstream base-card/button/sub-button CSS. Checks normal/large card geometry, colors, external simulated states, group gradients, contrast pseudo-elements, background cleanup, mobile spacing and native slider appearance when gradient is off.
- Screenshots from browser scenarios are attached to the GitHub Actions run.

## Known boundary
Browser integration tests simulate the DOM and hass.states. They are **not** a full Home Assistant frontend and do **not** test native slider pointer events, HA WebSocket subscriptions or the real Bubble Card lifecycle. Those require an isolated HA instance with installed Bubble Card and actual frontend/browser automation. The tests cannot certify that every Bubble Card layout, theme or third-party module is compatible.

## Remaining genuine HA verification
- Native main/sub-button slider pointer interactions, drag and outside-HA state changes.
- Actual card editor selectors and live update behavior in HA.
- Complex sections/grid and mixed-group layouts, module interactions, overlays and mobile touch.
- Visual screenshot diff snapshots across supported browsers and themes.

## Compatibility improvements added 2026-10-15
- Read-only upstream mirror updated to v3.4.2 in PR #10, and sync workflow changed to protected-main PRs in PR #9.
- Removed broad slider-fill styling, restricting VSC gradients to the main card slider. Native sub-slider contrast and state colors remain Bubble Card responsibilities.
- Native sub-button backgrounds remain active unless a VSC-specific background color is configured.
- CSS variables and gradients are written only when their values change; removed layout configuration fields no longer leave stale variables.
- Chromium tests cover native nested sub-slider preservation and custom sub-button background override.
- Real Home Assistant WebSocket/pointer lifecycle tests are still open. Repository setting must allow GitHub Actions to create PRs for unattended upstream-reference PR creation.

- Native Bubble Card `hasChanged('vsc-gradient', ...)` is now used to skip expensive gradient hue sorting when observed input RGBs remain unchanged. The entity reads still happen on each module style pass to preserve `trackedHass` dependencies. Python/Node/Chromium mocks now exercise the change gate.

## Follow-up fixes verified 2026-10-15 (PR #7)
- Parent entity fallback for sub-buttons: Bubble Card resolves `subButton.entity ?? context.config.entity`. VSC now uses the same rule; regression tests verify inherited icon colors and subsequent HA state changes.
- Explicit and implicit main groups and bottom groups now follow the same `.bubble-sub-button-N` class index order as Bubble Card v3.4.2. This fixes incorrect colors when YAML interleaves group items with individual buttons. Node and Chromium cover the mixed layout.
- Inline CSS custom properties are now ownership-tracked per card. Clearing a VSC option restores an earlier inline value (including `!important` priority), instead of unconditionally deleting a value owned by another module or custom theme.
- VSC registers Bubble Card's native `onTeardown` callback. When a card disconnects, it restores VSC-owned CSS variables, icon colors and card classes without adding WebSocket listeners or polling.
- Tests now enforce upstream source contracts for sub-button index ordering, inherited entities, the `trackedHass` dependency proxy and `hasChanged` / `onTeardown` support.
- The VSC GitHub Actions workflow also triggers when files under `docs/upstream/bubble-card/` change. This brings potential future API/DOM drift into the PR test cycle.
- Module metadata version was advanced to `v2026.10.15`; module ID and all 46 editor settings are unchanged.

**Verified:** Python module parsing, Node.js behavioral regressions, Chromium computed-CSS and state-change scenarios on simulated DOM using mirrored Bubble Card v3.4.2 CSS.

**Not verified:** Complete Home Assistant frontend mounting, actual WebSocket `state_changed` → Bubble Card style-pass chain, native slider drag/touch, live editor and module-disable events without card disconnection. Bubble Card currently calls module teardown on card disconnection; it is not evidence of cleanup on module disable while the same card stays mounted. The browser DOM and HA state used in CI are intentionally simulated.

## Original-Bubble-Card-Bundle-Smoke-Test (2026-10-15)
- GitHub Actions downloads the unchanged Bubble Card **v3.4.2** release asset `bubble-card.js` and checks SHA-256 `d526dfd815af6a022b8f7355874fc96f2df859aa213cff7b374f7d913a6436ae`.
- Chromium verifies that the real production bundle registers `customElements.get('bubble-card')`, exposes `setConfig` and the `hass` setter, and appears in the native card-picker registry.
- **Important limitation demonstrated in runs [38763892291](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38763892291), [38764404463](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38764404463), and [38765504975](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38765504975):** Rendering the actual element hangs during `card.hass = ...` in the standalone fixture, even with `styles: ""` and VSC absent. This does **not** establish a VSC bug. The artificially incomplete HA environment is not sufficient for full render/slider testing.
- Those unsupported render scenarios are explicitly marked `unittest.skip`; CI passes only the objectively verified production-bundle registration smoke test. They must be replaced with authentic HA/Lovelace integration cases per Issue #11, not treated as passed.
