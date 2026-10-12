# Visual Styling Center — audit (2026-10-12)

Reference: Bubble Card stable v3.4.1, mirrored under `docs/upstream/bubble-card/stable/`. Stable and main currently have no tracked source differences.

## Applied cleanup
- Removed the dormant `_hasInitialSliderUpdate` guard and `updateInitialSliderState` callback. The callback previously only read `hass.states` and did not change the slider, schedule updates, or subscribe to events. Native slider synchronization belongs to Bubble Card.
- Preserved the module ID `visual_styling_center` and all user-facing editor configuration keys.

## Follow-up review findings (not changed in this focused cleanup)
1. **State-derived colors can remain stale:** Directly applied `style.color` values in the icon and sub-button paths do not reliably clear when the previous entity-derived color is no longer applicable, or when the optional function-color feature is switched off. Audit ownership of inline style properties and remove only module-owned overrides.
2. **Zero values are lost:** `config.helper_opacity || 0.7`, `config.slider_helper_opacity || 0.7`, `config.helper_size_ratio || 0.7`, and related patterns override legitimate numeric zero values. Prefer `??` where zero is allowed.
3. **Configuration mutation:** `config.gradient_target = "slider"` and `config.gradient_entity = ...` mutate the object from `this.config`. Derive local effective values instead to avoid side effects.
4. **Gradient child entities:** A gradient built from group child light states must be retested when only one child light changes externally. Native slider value syncing does not by itself guarantee this custom visual dependency is invalidated.
5. **Styling specificity and compatibility:** The module uses a number of broad `!important` CSS rules and directly writes sub-button inline styles. Verify interaction with Bubble Card v3.4.1 defaults, other modules and section/grid layouts; avoid removing intended visuals solely based on class-name matches.
6. **Documentation drift:** The overview still calls the module 'Slider Control Center' though its name is 'Visual Styling Center'. Check supported-card claims and sample screenshots against v3.4.1.
7. **Verification gap:** Add automated checks covering parsing of the Markdown module, stable editor keys, zero-value behavior, stale-state cleanup and a browser-based slider/external-change regression scenario.

No Home Assistant runtime test was performed by this audit. These findings are code-review observations, not verified user-visible regressions.
