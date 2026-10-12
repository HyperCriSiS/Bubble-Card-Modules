# Visual Styling Center — compatibility audit (2026-10-12)

Upstream reference: Bubble Card **v3.4.1** (mirrored as read-only under docs/upstream/bubble-card/stable/). At review time main and stable tracked sources were identical.

## Implemented in PR #7
- Removed the obsolete _hasInitialSliderUpdate / updateInitialSliderState stub. Native Bubble Card updates button and sub-button sliders.
- Repaired corrupted Markdown code fences and module YAML metadata, removed stray JS-template closure, and restored invalid multiplication-unit characters. The entire module now parses as YAML.
- Preserved module ID visual_styling_center and **all 46 existing editor field names**. Version metadata is synchronized and advanced to v2026.10.12.
- Color changes for main icons and sub-button icons now restore only module-owned inline overrides when settings or entity states change. Supports legacy sub-button arrays and sectioned main/bottom + nested groups.
- Resolved nullish defaults, removed saved-config mutations, repaired function/scene detection, and removed redundant inline sub-button background writes.
- Explicitly reset module-owned color custom properties when settings are cleared. Re-enabled icon background picks up configured custom color.
- Corrected outdated introductory module name and repaired module download presentation.
- Added YAML/JavaScript regression tests and a GitHub Actions PR check for this module.

## Reactivity and reference
Current Bubble Card style-processor uses trackedHass during module execution. State reads inside this module, including group-member light states for gradients, are tracked as dependencies. No explicit state_changed subscription is needed. A regression test verifies gradient recalculation when a child light RGB value changes **on a style pass**, but does not simulate the entire Home Assistant frontend lifecycle.

## Still requiring Home Assistant UI verification
1. Manual slider interactions plus updates from outside HA, including sub-button sliders and long interactions.
2. All layout variants (normal, large, sections, grid, group/bottom sub-buttons) and interaction with other styling modules.
3. Theme changes and CSS specificity where broad !important rules override Bubble Card defaults.
4. Icon state colors for entities with unusual state values and missing attributes.
5. Screenshots and supported-card declarations against rendered Bubble Card v3.4.1.

Test coverage is intentionally focused on module serialization, naming compatibility and JavaScript side effects. A real HA/browser E2E test has not been performed.
