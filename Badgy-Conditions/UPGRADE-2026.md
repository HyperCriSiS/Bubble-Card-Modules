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

## Bug fixes

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

Source of original bug reports and community fixes:
https://github.com/Clooos/Bubble-Card/discussions/1333
