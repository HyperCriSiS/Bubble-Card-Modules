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
