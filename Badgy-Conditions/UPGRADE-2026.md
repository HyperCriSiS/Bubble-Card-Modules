# Badgy Condition Helper — 2026 upgrade (beta)

## Test the beta alongside the stable version

The working branch contains a [separate importable beta](./Badgy-Conditions-beta.yaml).

- Open the raw YAML: https://raw.githubusercontent.com/HyperCriSiS/Bubble-Card-Modules/feature/badgy-v2026-upgrade/Badgy-Conditions/Badgy-Conditions-beta.yaml
- In a Bubble Card editor, open Modules -> My Modules -> Import from YAML.
- Paste the entire YAML, then select Import Module. The module ID is `badgy-condition-helper-beta`.
- Duplicate an existing card and activate the beta *only on the duplicate*. If necessary, change the card's `modules` entry and per-card configuration namespace from `badgy-condition-helper` to `badgy-condition-helper-beta`.
- Disable the old Badgy module on the duplicate. All other cards continue using the stable installation.

This special beta ID is for testing only. The eventual release retains the
original ID `badgy-condition-helper`, so stored configuration paths remain unchanged.


This document describes the update proposed in the 2026 Badgy PR.
The existing YAML module ID and **all 240 pre-existing editor configuration
paths are preserved**. Existing cards should not require migration.

## Bubble Card v3.4.2 hardening (2026-10-15)

The isolated import artifact is currently `v2026.10.19-beta.6`.

- All Badgy animation CSS class names, keyframes, and effect color variables
  are namespaced. The effect cleanup no longer removes unowned classes.
- Native background, color, and icon properties are preserved. If Bubble Card
  changes one while Badgy is active, Badgy records the newer native value and
  restores it when the rule stops matching. Styles touched by other modules
  after the last Badgy write are left alone when disabling the rule.
- Background transparency now uses CSS `color-mix()`, rather than setting
  `opacity` on the complete sub-button or main icon (which dimmed text and
  badges too). Modern Chromium-based Home Assistant frontends support this.
- Main-icon badges default to in-card offsets. Supported browsers receive
  `overflow-clip-margin` on just the card with these opt-in badges; unlike
  `overflow: visible`, this preserves Bubble Card's no-scroll clipping behavior.
- The native `hasChanged()` hook gates unchanged badge/background updates,
  using live DOM element identity as part of each fingerprint.
- `onTeardown()` restores owned CSS/icons and removes owned badges/effects when
  Bubble Card disconnects a card, without patching its lifecycle callbacks.
- `suggestions_code` offers one opt-in main-icon badge configuration for a
  selected sensor or binary sensor in Bubble Card 3.4.2's Card Picker.

The native Card Picker and visual editor still require testing in a real HA
frontend; neither the Node mock nor the standalone Chromium smoke test reproduces
Home Assistant's real editor, entity subscriptions or shadow DOM.

## Beta.4 quality fixes (2026-10-17)

- An explicit `display_text` always overrides rounding and unit suffixes, for
  main-icon and sub-button entity badges.
- Units are appended only to numeric readings, not `unavailable` or text.
- The README card example now has a module-ID string in `modules:` and a
  separate `badgy-condition-helper:` configuration block.
- Automated tests verify custom text and correct example YAML.

## Beta.6 editor and rule changes (2026-10-19)

All existing configuration paths are unchanged; new keys are optional.

- **Rules everywhere:** entity badges, icon badges and every effect entry
  (main icon, sub-button icons, sub-buttons, entity and icon badge effects)
  accept a `rules` list, like colors, icons and backgrounds already did.
  The first matching rule wins and its fields override the entry's own.
  A badge rule can change color, text color, display text / icon and effect.
- **Fallback (`fallback_to_static`):** off by default. When it is on and no
  rule matches, the entry's static settings apply, still gated by the entry's
  own `condition`. When it is off, nothing is shown, as before.
- **Effect on the badge:** badges have `effect` and `effect_color`. They win
  over the separate `entity_badge_effects` / `icon_badge_effects` entry, which
  keeps working when the badge has no effect of its own.
- **Main icon badge offsets:** new `global_defaults.main_badge_h_pos` and
  `main_badge_v_pos` (default 0). The sub-button `badge_h_pos`/`badge_v_pos`
  no longer move main icon badges, which sit inside the card.
- **Editor:** labels state the priority (rules > color template > color
  entity > static color) and every default value, because Bubble Card does not
  display defaults inside named sections. Rules and the fallback switch sit
  after the static settings. Sub-button background color fields are shown
  only for the chosen type (needs Home Assistant 2026.9; older versions show
  all fields). Rule items hide gradient colors the same way.
- The main icon background only supports a solid color, so its rules no
  longer offer gradient fields.
- Badge position labels say which edge they measure from (entity badges:
  right edge, icon badges: left edge).

## Beta.5 fixes (2026-10-19)

- Badge gate: Bubble Card's `hasChanged()` compares values as text, so a DOM
  element passed to it always reads `[object HTMLDivElement]`. A badge that
  Bubble Card rebuilt (or that was removed) was therefore recreated empty and
  unpositioned. Each managed node now carries its own token for the gate.
- Rule colors: a matching rule's `color`/`color1-3` now wins over a
  `color_template`, `color_entity` or `color_attribute` set on the parent entry.
  A rule without its own color still inherits the parent's dynamic color.
- Three-color gradients without `color2` use green again (as in v2025), not blue.
- The module declares `unsupported:` (cover, horizontal buttons stack, media
  player, pop-up, separator), so Bubble Card disables it there by default.
- The test mocks now use Bubble Card 3.4.2's string-based `hasChanged()`
  semantics; regression tests cover all three fixes.

## Visible changes for existing configurations

No configuration is lost or needs migration, but two things look different:

- `opacity` on `sub_buttons_background` and `main_icon_background` now fades
  only the background color. In v2025 it set CSS `opacity` on the whole
  element, which also faded the icon, the name and the badges.
- Conditions use Bubble Card's native evaluator. Condition types the old
  built-in evaluator did not know (`time`, `screen`, `user`, `template`,
  `state_not`, ...) were always false before and now apply.


- Stop sub-button icon/container animations as soon as their conditions turn false.
- Update animation classes only when they change (no unrelated-state restarts).
- Update badges in place rather than removing/recreating them on every update.
- Keep scale independent of the CSS animation transform by scaling badge
  dimensions, padding, font size and its icon dimensions.
- Prefer native Bubble Card checkConditionsMet for the complete HA condition
  vocabulary; retain a fallback for older versions.
- Remove obsolete state_changed event subscription and disconnectedCallback patch.
- Treat background-color none as an unset color.
- Use hass.formatEntityState for binary_sensor badge values (Open/Closed, etc.);
  manually supplied display_text overrides the automatic value.

## New functions and editor layout

- Icon Colors: main icon, individual sub-button icons, condition/rule lists.
- Backgrounds: main icon, individual sub-buttons, first-match rules and
  dynamic Jinja/attribute color sources, plus Card Glow.
- Icons: main icon and sub-button icon overrides, including rule lists.
- Entity Badges: existing six sub-buttons plus Main Icon.
- Icon Badges: existing six sub-buttons plus Main Icon.
- Effects: main icon, sub-button icon, sub-button container, entity badge,
  icon badge, with dedicated main icon badge effects.
- Global Defaults: badge colors, position/scale, sub-button icon colors,
  sub-button background and effects.

### Main icon badge examples

    badgy-condition-helper:
      entity_badges:
        main:
          entity: binary_sensor.kitchen_window
          translated_state: true
          color: blue
          scale: 1.2
          h_pos: -8
          v_pos: -8
      icon_badges:
        main:
          icon: mdi:alert
          condition:
            - condition: state
              entity_id: binary_sensor.kitchen_window
              state: "on"
      entity_badge_effects:
        main:
          effect: heartbeat

### Multiple conditions in priority order

    badgy-condition-helper:
      sub_buttons_background:
        "0":
          rules:
            - label: Heating
              condition:
                - condition: state
                  entity_id: climate.living_room
                  state: heat
              color: red
              type: solid
            - label: Cooling
              condition:
                - condition: state
                  entity_id: climate.living_room
                  state: cool
              color: blue
              type: solid
            - label: Off
              condition:
                - condition: state
                  entity_id: climate.living_room
                  state: "off"
              color: black
              type: solid

The **first matching rule wins**. If a nonempty rules list is present but
none of its conditions matches, the override is removed so Bubble Card styling
can apply.

### Dynamic filament color

    badgy-condition-helper:
      sub_buttons_background:
        "0":
          type: solid
          color_entity: sensor.bambu_p1s_ams_1_tray_1
          color_attribute: color

Alternatively, use the template input:

    badgy-condition-helper:
      sub_buttons_background:
        "0":
          type: solid
          color_template: "{{ state_attr('sensor.bambu_p1s_ams_1_tray_1', 'color') }}"

The Jinja variant uses Bubble Card's renderTemplate helper when available.
A color which is not a valid CSS color is ignored in favor of the static
color configuration. Colors from dynamic sources are not JavaScript-evaluated.

### Main icon colors, icon replacement and global defaults

    badgy-condition-helper:
      icon_colors:
        main_icon:
          color: yellow
          condition:
            - condition: state
              entity_id: light.living_room
              state: "on"
      icons:
        main_icon:
          icon: mdi:lightbulb-on
          condition:
            - condition: state
              entity_id: light.living_room
              state: "on"
      global_defaults:
        badge_color: blue
        badge_scale: 1.15
        sub_button_effect: glow
        sub_button_effect_color: yellow

### Card glow

    badgy-condition-helper:
      card_effects:
        effect: glow
        color: red
        intensity: 12
        animate: true
        condition:
          - condition: state
            entity_id: switch.plug
            state: "on"

## Additional beta.3 safety fixes

- Badge CSS and runtime selectors are scoped to `badgy-owned-badge`; other modules' entity/icon badges are never reused, animated or deleted.
- Legacy class cleanup no longer strips third-party `opacity` values.
- Changes to a static sub-button container's CSS position are registered and undone via onTeardown.
- Temporary badge anchor positioning is now restored as soon as the last owned badge becomes inactive, even if the card remains mounted.
- Fallback `not` conditions now negate all nested conditions (equivalent to Home Assistant's NOT), not only the first.
- Automated tests include foreign badge coexistence, legacy-opacity ownership, position restoration and the fallback NOT truth table.

## Constraints

- Main icon badges are intentionally opt-in, so previous configurations stay
  visually unchanged. Their position is relative to the icon container.
- The editor exposes six explicit sub-button slots; the code also supports
  numbered DOM selectors through 10, including grouped sub-buttons numbered
  by Bubble Card. Layout-specific DOM differences still require HA UI testing.
- The native template/condition helpers depend on the installed Bubble Card
  version; no unsupported helpers are referenced without typeof checks.
- No direct production HA UI test has been performed yet. This is a beta and
  should be tested on a representative dashboard before release.

## Verification

The Badgy CI workflow:

- Parses the complete embedded module YAML.
- Compiles its Bubble Card JavaScript template.
- Compares saved editor paths against the original main-branch module.
- Runs mocked DOM regression tests for repeated sensor updates, main badges,
  animation start/stop, localized values, dynamic color rules, Jinja colors,
  icon restoration and global scale.
- Runs three headless Chromium Playwright smoke tests against a synthetic Bubble
  Card DOM: real computed CSS, color-mix alpha, scaled badges, animation
  start/stop, foreign badge isolation, repeated sensor updates, replacement of
  a lost badge node and onTeardown cleanup.
- A second browser suite uses the mirrored **actual Bubble Card v3.4.2 base-card CSS**
  and its DOM nesting for real clip-margin, badge overlap, normal/large layout,
  native click handling and immediate position restoration checks.
- These browser tests run in CI but **do not replace** a live Home Assistant
  acceptance test or visual review of actual Bubble Card layouts.

Source of original bug reports and community fixes:
https://github.com/Clooos/Bubble-Card/discussions/1333