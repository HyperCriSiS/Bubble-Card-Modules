# Badgy beta — Home Assistant acceptance checklist

Target: Bubble Card **v3.4.2**, a separate dashboard, and the isolated
`badgy-condition-helper-beta` module. The original module and existing cards
must not be modified during the tests.

This is a **manual** release gate. Unit tests do not substitute for these checks.

## Installation and editor

- [ ] Import the beta YAML from the branch in **Modules → My Modules → Import from YAML**.
- [ ] Add a duplicate card using only the beta module and confirm it can be saved/reloaded.
- [ ] Open every editor group (Icon Colors, Backgrounds, Icons, Entity Badges,
      Icon Badges, Effects, Global Defaults); confirm nested fields appear.
- [ ] Save a list of 2+ condition rules, reorder them, reopen the card and
      confirm rule order, values and valid condition editors survive.
- [ ] Test the new Card Picker suggestion on a `sensor` and `binary_sensor`.
      It should use the beta module and not appear for an unrelated `light`.

## Rendering and state changes

- [ ] Show an entity badge and an icon badge simultaneously on the main icon.
- [ ] Check main badges at 0 default offsets, at -8 offsets and near both
      outer card edges in compact and large layouts (no inappropriate clipping).
- [ ] Check badge scale 0.6, 1.0, and 2.0 with each animation (no transform conflict).
- [ ] Switch animation condition on/off repeatedly: no animation remains after
      false and unrelated sensor updates do not restart it.
- [ ] Update a rapidly changing sensor every second; badge nodes should not
      flicker or accumulate in the DOM.
- [ ] Check a window binary sensor showing Open/Closed in the selected HA locale.
- [ ] Test dynamic colors from an entity attribute and from a Jinja template,
      including `unavailable` or invalid color values.
- [ ] Apply sub-button background opacity 0, 0.5 and 1.0; icon, label and badge
      must remain fully opaque.
- [ ] Enable/disable card glow, change themes and use both dark/light color values.
- [ ] Test a grouped sub-button as well as normal sub-buttons; ensure the
      icon/animation/badge stays on the correct numbered button.
- [ ] Check a Bubble Card dropdown and slider alongside Badgy styling:
      overlays, clicks, hover and pointer behavior must remain usable.

## Lifecycle, compatibility and multi-module safety

- [ ] Put the beta card in a pop-up and repeatedly open/close the pop-up.
      No badges or effect classes should leak, and each reopen should render.
- [ ] Change card entity state/native icon while Badgy overrides it; after
      disabling the rule the *new* native icon/color should reappear.
- [ ] Use another styling module that changes the same background/color.
      Removing a Badgy condition must not erase the other module's current style.
- [ ] Reload the dashboard and reconnect HA; no increased memory use, error
      spam, or lingering animation effects.
- [ ] Open browser devtools and check for JavaScript errors and unsupported
      CSS features (`color-mix`, `overflow-clip-margin`).
- [ ] Confirm an existing **stable** Badgy card remains unchanged and that
      removing the **beta** does not remove stable settings.

## Release decision

Do not merge the beta into `main` or post it to the public Bubble Card
discussion until the above tests have been performed. Record failures with
Bubble Card version, Home Assistant version, card YAML, browser/device,
expected/actual behavior, and a screenshot if visual.

Known review area: Bubble Card 3.4.2's native background-contrast calculation
uses sub-button color variables and scheduled tone updates. Verify that manual
Badgy background overrides do not leave icons with insufficient contrast.
