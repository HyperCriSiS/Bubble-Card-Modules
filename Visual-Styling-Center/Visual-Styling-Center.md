# Visual Styling Center

**Version:** v2026.11.05
**Creator:** [HyperCriSiS](https://github.com/HyperCriSiS)

> [!IMPORTANT] 
> **Unsupported cards:**
>  - Cover
>  - Climate
>  - Horizontal buttons stack
>  - Media player
>  - Pop-up
>  - Select
>  - Separator


--> The sections layout sizes cards itself, so the Card Height Multiplier only works in the other layouts. With two sub-button rows in a sections view, use Bubble Card's grid layout. If something does not look as expected, try another Bubble Card layout.

Visual Styling Center gives you precise control over the look of your Bubble Card buttons: sizes and spacing of the card, the main icon and the sub-buttons, colors for every element, entity state colors, contrast helpers behind icons and sliders, and dynamic gradients that follow your lights.

On **Sub-buttons** and **Calendar** cards there is no main icon, name or slider, so only the
sub-button options (sizes, spacing, colors, state colors, corner radius) have an effect there.
**Pop-up** cards are not supported: the module script skips them, so the pop-up and its cards keep
their colors and sizes. Only the module's default sizes can still reach the pop-up header through
its stylesheet, so do not add the module there by YAML or as a global module.

## Feature Overview

The editor sections follow this order. All option keys are unchanged from earlier
versions, so existing configurations keep working without migration.

### Card
- **Card Height Multiplier**: Scale the overall height of your Bubble Card (not in the sections layout)
- **Inner Card Padding**: Add padding inside the card for more spacing
- **Card Background Color** and **Opacity**: Solid color for button cards, opacity also fades the theme background
- **Card Corner Radius**: Empty keeps the theme value

### Main Icon
- **Main Icon Size Multiplier** and **Icon Background Ratio**
- **Main Icon Margin**: Spacing around the main icon (applies to all sides). Until you set it, the large layout keeps its own 8px instead of the shown 6.
- **Icon Background Corner Radius**: Empty keeps the theme value (a circle)
- **Icon Color** and **Icon Background Color** (RGB picker or manual CSS value, the manual value wins)
- **Hide Icon Background**: Remove the background from the main icon

### Sub-buttons
- **Sub-icon Size Multiplier** and **Sub-button Background Ratio**
- **Sub-button Container Outer Margin** (added to the default spacing, on the left in right-to-left languages; until you set it, the large layout keeps its own 14px instead of the shown 8), **Row Spacing** and **Column Spacing** (also inside sub-button groups)
- Always visible sub-button sliders follow the sub-button height (32px times the factors, like the sub-buttons; Bubble Card's own default is 36px)
- **Sub-button Icon Color** and **Sub-button Background Color**
- **Sub-button Corner Radius**: Empty keeps the theme value
- A sub-button's own **custom height** (Bubble Card option) always wins over the module size
- **Hide Sub-button Backgrounds**

### Name and State Text
- **Name Color**, **Name Font Size**, **State Color**, **State Font Size**: Empty keeps the theme

### State Colors
- **Use Home Assistant Theme State Colors**: Use the theme's `--state-*-color` instead of fixed green/grey
- **Color Main Icon / Sub-button Icons by Entity State**: Light color when on, otherwise a color per state
- **Custom Off/Offline/Function Color**: Apply a custom color to icons for inactive states, functional entities (scenes, scripts, automations), or entities without states
- Entities without states and non-existent entities are handled without errors

### Icon Contrast Helper
Adds a circular background behind icons to improve visibility and contrast regardless of the card's background color.
- **Enable Icon Contrast Helper**: Toggle the helper on and off (sub-button backgrounds are hidden while it is on, to avoid visual conflicts)
- **Apply to Main/Sub Icons**: Choose which icons get the contrast helper
- **Helper Color**: Background color of the helper
- **Helper Opacity**: Transparency of the helper background
- **Helper Size Ratio**: How much of the icon the background covers
- **Radial Fade Effect**: Smooth fade from color to transparent (off unless enabled)
- **Fade Strength**: How gradual the fade is

### Gradient Effects
- **Enable Gradient Effects**: Toggle dynamic gradients on and off
- **Apply Gradient to**: Slider fill or card background
- **Gradient Direction**: Angle in degrees, 90 is left to right as before
- **Gradient Entity**: Light group or single light the gradient follows (empty uses the card's light)
- **Hide Rainbow Fallback**: Without it, a rainbow gradient is shown while no colored light is on
- **Slider Brightness**: Opacity of the slider when using background gradients

### Slider Contrast Helper
Only active together with a card background gradient, it improves the visibility of the slider.
- **Enable Slider Contrast Helper**: Toggle the helper for sliders with background gradients
- **Slider Helper Color**: Background/glow color of the slider
- **Slider Helper Opacity**: Transparency of the helper effect
- **Slider Helper Size Ratio**: Size of the helper effect
- **Enable Radial Fade Effect**: Smooth fade of the slider glow (off unless enabled)
- **Slider Fade Strength**: Intensity of the fade

### Interaction Effects
- **Hover Highlight, Brighter Active Icon and Sub-icon Opacity**: On by default as in earlier versions, set `enable_interaction_effects: false` to use Bubble Card's native look

### Compatibility
- Works with all button layouts (normal, large, multi-row)
- Entity state tracking for dynamic changes, without extra Home Assistant subscriptions or polling
- Built against Bubble Card v3.4.2

## Changelog

### v2026.11.05

**Fixed**
- Pop-up cards are skipped by the module script. `unsupported` only disables the editor checkbox, so a module added by YAML or as a global module used to restyle the pop-up header and its cards.
- On the `sub-buttons` card a leftover `main` section in YAML no longer shifts the sub-button numbering, so the right icons get their colors.
- Always visible sub-button sliders follow the sub-button height instead of staying at 36px.

### v2026.10.30

**Fixed**
- The sub-button container margin follows the text direction (right-to-left languages).

### v2026.10.29

No migration needed: the module ID and every existing setting keep working.

**New**
- Name and state text: color and font size.
- Corner radius for card, icon background and sub-buttons through Bubble Card's own variables.
- Card background color and opacity.
- Gradient direction (angle), 90 keeps the previous left-to-right gradient.
- Optional Home Assistant theme state colors instead of fixed green/grey.

**Fixed**
- Without a Bubble theme the icon background circle is visible again; use **Hide Icon Background** to remove it.
- A sub-button's own `custom_height` wins over the module size.
- `sub-buttons` and `calendar` cards stay supported; the sub-button options work there.

### v2026.10.15

**Fixed**
- Repaired the module definition and display units.
- Native Bubble Card v3.4.2 sliders are used; the module's own slider update was removed.
- Entity colors, CSS overrides and entity inheritance work again, also in mixed main/bottom sub-button groups.
- Numeric zero values are kept and the saved configuration is never modified.
- The module only resets styles it set itself and cleans up when the card is removed or the module is disabled.

Configure this module via the editor or in YAML, for example:

```yaml
type: custom:bubble-card
card_type: button
button_type: slider
entity: light.living_room
icon: mdi:lightbulb
name: Living Room Light
show_state: true
sub_button:
  - entity: fan.living_room
    icon: mdi:fan
  - entity: switch.living_room_plug
    icon: mdi:power-socket-eu
modules:
  - visual_styling_center
visual_styling_center:
  height_multiplier: 1.5
  icon_size_multiplier: 1.2
  custom_icon_color: [255, 255, 255]
  custom_icon_background_color: [0, 0, 0]
  enable_entity_colored_main_icon: true
  enable_entity_colored_subicons: true
  enable_icon_helper: true
  helper_color: [255, 255, 255]
  helper_opacity: 0.7
  helper_size_ratio: 1.2
  enable_helper_fade: true
  fade_strength: 1.2
  enable_gradient: true
  gradient_target: background
  gradient_entity: light.living_room_group
  disable_default_gradient: false
  slider_bg_opacity: 0.8
  enable_slider_helper: true
  slider_helper_color: [0, 0, 0]
  slider_helper_opacity: 0.5
```

---

<details>

<summary><b>Get this Module</b></summary>

<br>

> To use this module, simply copy and paste the following configuration into your `/www/bubble/bubble-modules.yaml` file.

```yaml
visual_styling_center:
  name: "Visual Styling Center"
  version: "v2026.11.05"
  creator: "HyperCriSiS"
  link: "https://github.com/Clooos/Bubble-Card/discussions/1314"
  description: Comprehensive customization tool for Bubble Card elements with focus on gradient effects and icon styling for both card and sub-buttons.
  unsupported:
    - cover
    - climate
    - horizontal-buttons-stack
    - media-player
    - pop-up
    - select
    - separator
  editor:
    # Sections have no `name` on purpose: values stay flat under
    # visual_styling_center, so existing configurations keep working.
    - type: expandable
      title: "Card"
      icon: "mdi:card-outline"
      schema:
        - name: height_multiplier
          label: "Card Height Multiplier (not in sections layout)"
          default: 1
          selector:
            number:
              min: 0.8
              max: 5.0
              step: 0.1
              mode: slider
              unit_of_measurement: "×"
        - name: inner_padding
          label: "Inner Card Padding"
          default: 0
          selector:
            number:
              min: 0
              max: 30
              step: 1
              mode: slider
              unit_of_measurement: "px"
        - name: custom_card_background_color
          label: "Card Background Color (RGB, button cards)"
          selector:
            color_rgb: {}
        - name: manual_card_background_color
          label: "Card Background Color, manual (overrides RGB)"
          selector:
            text: {}
        - name: card_background_opacity
          label: "Card Background Opacity"
          default: 1
          selector:
            number:
              min: 0
              max: 1
              step: 0.05
              mode: slider
        - name: card_border_radius
          label: "Card Corner Radius (empty = theme)"
          selector:
            number:
              min: 0
              max: 60
              step: 1
              mode: box
              unit_of_measurement: "px"
    - type: expandable
      title: "Main Icon"
      icon: "mdi:circle-outline"
      schema:
        - name: icon_size_multiplier
          label: "Main Icon Size Multiplier"
          default: 1
          selector:
            number:
              min: 0.8
              max: 3.0
              step: 0.1
              mode: slider
              unit_of_measurement: "×"
        - name: icon_background_ratio
          label: "Icon Background Ratio"
          default: 1
          selector:
            number:
              min: 0.6
              max: 1.4
              step: 0.05
              mode: slider
              unit_of_measurement: "×"
        - name: icon_vertical_margin
          label: "Main Icon Margin (all sides)"
          default: 6
          selector:
            number:
              min: -10
              max: 30
              step: 1
              mode: slider
              unit_of_measurement: "px"
        - name: icon_border_radius
          label: "Icon Background Corner Radius (empty = theme)"
          selector:
            number:
              min: 0
              max: 40
              step: 1
              mode: box
              unit_of_measurement: "px"
        - name: custom_icon_color
          label: "Icon Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_icon_color
          label: "Icon Color, manual (overrides RGB, e.g. #FFFFFF or rgba(255,255,255,0.8))"
          selector:
            text: {}
        - name: hide_icon_background
          label: "Hide Icon Background"
          default: false
          selector:
            boolean: {}
        - name: custom_icon_background_color
          label: "Icon Background Color (RGB)"
          visible:
            - field: hide_icon_background
              operator: not_eq
              value: true
          selector:
            color_rgb: {}
        - name: manual_icon_background_color
          label: "Icon Background Color, manual (overrides RGB)"
          visible:
            - field: hide_icon_background
              operator: not_eq
              value: true
          selector:
            text: {}
    - type: expandable
      title: "Sub-buttons"
      icon: "mdi:dots-horizontal-circle-outline"
      schema:
        - name: subicon_size_multiplier
          label: "Sub-icon Size Multiplier"
          default: 1
          selector:
            number:
              min: 0.8
              max: 3.0
              step: 0.1
              mode: slider
              unit_of_measurement: "×"
        - name: subbutton_background_ratio
          label: "Sub-button Background Ratio"
          default: 1
          selector:
            number:
              min: 0.6
              max: 1.4
              step: 0.05
              mode: slider
              unit_of_measurement: "×"
        - name: subbutton_horizontal_margin
          label: "Sub-button Container Outer Margin (added to the default spacing)"
          default: 8
          selector:
            number:
              min: -10
              max: 30
              step: 1
              mode: slider
              unit_of_measurement: "px"
        - name: subbutton_row_spacing
          label: "Space Between Sub-button Rows"
          default: 10
          selector:
            number:
              min: 0
              max: 30
              step: 1
              mode: slider
              unit_of_measurement: "px"
        - name: subbutton_column_spacing
          label: "Space Between Sub-button Columns"
          default: 10
          selector:
            number:
              min: -10
              max: 30
              step: 1
              mode: slider
              unit_of_measurement: "px"
        - name: subbutton_border_radius
          label: "Sub-button Corner Radius (empty = theme)"
          selector:
            number:
              min: 0
              max: 30
              step: 1
              mode: box
              unit_of_measurement: "px"
        - name: custom_subicon_color
          label: "Sub-button Icon Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_subicon_color
          label: "Sub-button Icon Color, manual (overrides RGB)"
          selector:
            text: {}
        - name: hide_subbutton_background
          label: "Hide Sub-button Backgrounds (also hidden by Icon Contrast Helper)"
          default: false
          selector:
            boolean: {}
        - name: custom_subbutton_background_color
          label: "Sub-button Background Color (RGB)"
          visible:
            - field: hide_subbutton_background
              operator: not_eq
              value: true
          selector:
            color_rgb: {}
        - name: manual_subbutton_background_color
          label: "Sub-button Background Color, manual (overrides RGB)"
          visible:
            - field: hide_subbutton_background
              operator: not_eq
              value: true
          selector:
            text: {}
    - type: expandable
      title: "Name & State Text"
      icon: "mdi:format-text"
      schema:
        - name: custom_name_color
          label: "Name Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_name_color
          label: "Name Color, manual (overrides RGB)"
          selector:
            text: {}
        - name: name_font_size
          label: "Name Font Size (empty = theme)"
          selector:
            number:
              min: 8
              max: 32
              step: 1
              mode: box
              unit_of_measurement: "px"
        - name: custom_state_color
          label: "State Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_state_color
          label: "State Color, manual (overrides RGB)"
          selector:
            text: {}
        - name: state_font_size
          label: "State Font Size (empty = theme)"
          selector:
            number:
              min: 8
              max: 32
              step: 1
              mode: box
              unit_of_measurement: "px"
    - type: expandable
      title: "State Colors"
      icon: "mdi:palette"
      schema:
        - name: use_theme_state_colors
          label: "Use Home Assistant Theme State Colors (instead of fixed green/grey)"
          default: false
          selector:
            boolean: {}
        - name: enable_entity_colored_main_icon
          label: "Color Main Icon by Entity State"
          default: false
          selector:
            boolean: {}
        - name: enable_entity_colored_subicons
          label: "Color Sub-button Icons by Entity State"
          default: false
          selector:
            boolean: {}
        - name: enable_function_button_color
          label: "Custom Color for Off/Offline/Scene/Script/Automation Icons"
          default: false
          selector:
            boolean: {}
        - name: function_button_color
          label: "Off/Offline/Function Color (RGB)"
          visible:
            - field: enable_function_button_color
              operator: eq
              value: true
          selector:
            color_rgb: {}
        - name: manual_function_button_color
          label: "Off/Offline/Function Color, manual (overrides RGB)"
          visible:
            - field: enable_function_button_color
              operator: eq
              value: true
          selector:
            text: {}
    - type: expandable
      title: "Icon Contrast Helper"
      icon: "mdi:contrast-circle"
      schema:
        - name: enable_icon_helper
          label: "Enable Icon Contrast Helper (hides sub-button backgrounds)"
          default: false
          selector:
            boolean: {}
        - name: apply_to_main_icon
          label: "Apply Helper to Main Icon"
          default: true
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
          selector:
            boolean: {}
        - name: apply_to_sub_icons
          label: "Apply Helper to Sub-Icons"
          default: true
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
          selector:
            boolean: {}
        - name: helper_color
          label: "Helper Background Color (RGB)"
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
          selector:
            color_rgb: {}
        - name: manual_helper_color
          label: "Helper Color, manual (overrides RGB and opacity)"
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
          selector:
            text: {}
        - name: helper_opacity
          label: "Helper Background Opacity"
          default: 0.7
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
          selector:
            number:
              min: 0.1
              max: 1.0
              step: 0.05
              mode: slider
        - name: helper_size_ratio
          label: "Helper Size Ratio"
          default: 0.7
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
          selector:
            number:
              min: 0.3
              max: 1.5
              step: 0.05
              mode: slider
              unit_of_measurement: "×"
        - name: enable_helper_fade
          label: "Enable Radial Fade Effect"
          default: false
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
          selector:
            boolean: {}
        - name: fade_strength
          label: "Fade Strength"
          default: 1.0
          visible:
            - field: enable_icon_helper
              operator: eq
              value: true
            - field: enable_helper_fade
              operator: eq
              value: true
          selector:
            number:
              min: 0.5
              max: 2.0
              step: 0.1
              mode: slider
    - type: expandable
      title: "Gradient Effects"
      icon: "mdi:gradient-horizontal"
      schema:
        - name: enable_gradient
          label: "Enable Gradient Effects"
          default: false
          selector:
            boolean: {}
        - name: gradient_target
          label: "Apply Gradient to"
          default: "slider"
          visible:
            - field: enable_gradient
              operator: eq
              value: true
          selector:
            select:
              options:
                - value: "slider"
                  label: "Slider Fill"
                - value: "background"
                  label: "Card Background"
        - name: gradient_angle
          label: "Gradient Direction"
          default: 90
          visible:
            - field: enable_gradient
              operator: eq
              value: true
          selector:
            number:
              min: 0
              max: 360
              step: 5
              mode: slider
              unit_of_measurement: "°"
        - name: gradient_entity
          label: "Gradient Entity (light or light group, empty = card light)"
          visible:
            - field: enable_gradient
              operator: eq
              value: true
          selector:
            entity:
              domain: light
        - name: disable_default_gradient
          label: "Hide Rainbow Fallback When No Colored Light Is On"
          default: false
          visible:
            - field: enable_gradient
              operator: eq
              value: true
          selector:
            boolean: {}
        - name: slider_bg_opacity
          label: "Slider Brightness on Background Gradient"
          default: 0.6
          visible:
            - field: enable_gradient
              operator: eq
              value: true
            - field: gradient_target
              operator: eq
              value: background
          selector:
            number:
              min: 0.1
              max: 1.0
              step: 0.05
              mode: slider
    - type: expandable
      title: "Slider Contrast Helper (Background Gradient only)"
      icon: "mdi:contrast-box"
      schema:
        - name: enable_slider_helper
          label: "Enable Slider Contrast Helper"
          default: false
          selector:
            boolean: {}
        - name: slider_helper_color
          label: "Slider Helper Color (RGB)"
          visible:
            - field: enable_slider_helper
              operator: eq
              value: true
          selector:
            color_rgb: {}
        - name: manual_slider_helper_color
          label: "Slider Helper Color, manual (overrides RGB and opacity)"
          visible:
            - field: enable_slider_helper
              operator: eq
              value: true
          selector:
            text: {}
        - name: slider_helper_opacity
          label: "Slider Helper Opacity"
          default: 0.7
          visible:
            - field: enable_slider_helper
              operator: eq
              value: true
          selector:
            number:
              min: 0.1
              max: 1.0
              step: 0.05
              mode: slider
        - name: slider_helper_size_ratio
          label: "Slider Helper Size Ratio"
          default: 0.7
          visible:
            - field: enable_slider_helper
              operator: eq
              value: true
          selector:
            number:
              min: 0.3
              max: 4.0
              step: 0.1
              mode: slider
              unit_of_measurement: "×"
        - name: enable_slider_helper_fade
          label: "Enable Radial Fade Effect"
          default: false
          visible:
            - field: enable_slider_helper
              operator: eq
              value: true
          selector:
            boolean: {}
        - name: slider_fade_strength
          label: "Slider Fade Strength"
          default: 1.0
          visible:
            - field: enable_slider_helper
              operator: eq
              value: true
            - field: enable_slider_helper_fade
              operator: eq
              value: true
          selector:
            number:
              min: 0.5
              max: 2.0
              step: 0.1
              mode: slider
    - type: expandable
      title: "Interaction Effects"
      icon: "mdi:gesture-tap"
      schema:
        - name: enable_interaction_effects
          label: "Hover Highlight, Brighter Active Icon and Sub-icon Opacity"
          default: true
          selector:
            boolean: {}
  code: |
   ${(() => {
      const config = this.config.visual_styling_center || {};
      // "unsupported" only disables the editor checkbox. Applied by YAML or
      // is_global, a pop-up hands over the pop-up element as "card" and the
      // selectors below would reach its header and child cards. The static
      // CSS after this function still reaches the pop-up chrome; Bubble Card
      // confines it there.
      if (this.config.card_type === 'pop-up') return '';
      // Keep each inline CSS variable's pre-module value. Without ownership,
      // an unset VSC option would delete another module's or theme's overrides.
      const ownedVariables = card._vscOwnedVariables ?? (card._vscOwnedVariables = new Map());
      const restoreOwnedVariable = (name) => {
        const saved = ownedVariables.get(name);
        if (!saved) return;
        if (card.style.getPropertyValue(name) === saved.applied) {
          if (saved.previous) card.style.setProperty(name, saved.previous, saved.priority);
          else card.style.removeProperty(name);
        }
        ownedVariables.delete(name);
      };
      const setCardVariable = (name, value) => {
        if (value == null) {
          restoreOwnedVariable(name);
          return;
        }
        const desired = String(value);
        const current = card.style.getPropertyValue(name);
        let saved = ownedVariables.get(name);
        if (!saved) {
          saved = { previous: current, priority: card.style.getPropertyPriority(name), applied: desired };
          ownedVariables.set(name, saved);
        } else {
          saved.applied = desired;
        }
        if (current !== desired) card.style.setProperty(name, desired);
      };
      // onTeardown fires when Bubble Card detaches a card, including view
      // caching/re-attachment. Keep registration idempotent across style passes.
      const vscClassNames = [
        'slider-background-mode', 'vsc-custom-subbutton-background',
        'use-function-button-color', 'hide-icon-background',
        'hide-subbutton-background', 'icon-helper-enabled',
        'helper-fade-enabled', 'helper-main-icon', 'helper-sub-icons',
        'slider-helper-enabled', 'slider-helper-fade-enabled',
        'use-gradient-background', 'use-gradient-slider',
        'vsc-interaction-effects', 'vsc-custom-icon-background',
        'vsc-name-color', 'vsc-state-color', 'vsc-name-size', 'vsc-state-size'
      ];
      const initialClasses = card._vscInitialClasses ?? (card._vscInitialClasses =
        new Map(vscClassNames.map(name => [name, card.classList.contains(name)])));

      // Derive defaults without mutating the saved Bubble Card configuration.
      const gradientTarget = config.gradient_target ?? 'slider';
      const gradientEntity = config.gradient_entity ||
        (this.config.entity?.startsWith('light.') ? this.config.entity : null);
      if (gradientTarget === 'background' && config.enable_gradient) {
        card.classList.add('slider-background-mode');
      } else {
        card.classList.remove('slider-background-mode');
      }
      // Apply all size and spacing configurations
      setCardVariable('--height-multiplier', config.height_multiplier);
      setCardVariable('--inner-padding', config.inner_padding == null ? null : `${config.inner_padding}px`);
      setCardVariable('--icon-vertical-margin', config.icon_vertical_margin == null ? null : `${config.icon_vertical_margin}px`);
      setCardVariable('--subbutton-horizontal-margin', config.subbutton_horizontal_margin == null ? null : `${config.subbutton_horizontal_margin}px`);
      setCardVariable('--subbutton-row-spacing', config.subbutton_row_spacing == null ? null : `${config.subbutton_row_spacing}px`);
      setCardVariable('--subbutton-column-spacing', config.subbutton_column_spacing == null ? null : `${config.subbutton_column_spacing}px`);
      setCardVariable('--icon-size-multiplier', config.icon_size_multiplier);
      setCardVariable('--icon-background-ratio', config.icon_background_ratio);
      setCardVariable('--subicon-size-multiplier', config.subicon_size_multiplier);
      setCardVariable('--subbutton-background-ratio', config.subbutton_background_ratio);
      if (config.slider_bg_opacity !== undefined) {
        setCardVariable('--slider-bg-opacity', config.slider_bg_opacity);
      } else {
        setCardVariable('--slider-bg-opacity', 0.6);
      }

      // Only keep module-owned variables while an option has a value.
      const resolveColor = (manual, selected) => {
        if (typeof manual === 'string' && manual.trim()) return manual;
        if (Array.isArray(selected) && selected.length === 3) {
          return `rgb(${selected[0]}, ${selected[1]}, ${selected[2]})`;
        }
        return typeof selected === 'string' && selected.trim() ? selected : null;
      };
      setCardVariable('--icon-color', resolveColor(config.manual_icon_color, config.custom_icon_color));
      setCardVariable('--subicon-color', resolveColor(config.manual_subicon_color, config.custom_subicon_color));
      const customSubbuttonBackground = resolveColor(config.manual_subbutton_background_color, config.custom_subbutton_background_color);
      setCardVariable('--subbutton-background-color', customSubbuttonBackground);
      // Keep the native on/off background and v3.4.2 contrast unless overridden.
      card.classList.toggle('vsc-custom-subbutton-background', customSubbuttonBackground != null);
      const iconBackgroundColor = config.hide_icon_background === true ? 'transparent'
        : resolveColor(config.manual_icon_background_color, config.custom_icon_background_color);
      setCardVariable('--icon-background-color', iconBackgroundColor);
      // Without an explicit color the native chain applies. The old fallback
      // stopped at --bubble-secondary-background-color, which only Bubble
      // themes define, so the icon circle turned transparent everywhere else.
      card.classList.toggle('vsc-custom-icon-background', iconBackgroundColor != null);

      // Name and state text
      const nameColor = resolveColor(config.manual_name_color, config.custom_name_color);
      setCardVariable('--vsc-name-color', nameColor);
      card.classList.toggle('vsc-name-color', nameColor != null);
      const stateColor = resolveColor(config.manual_state_color, config.custom_state_color);
      setCardVariable('--vsc-state-color', stateColor);
      card.classList.toggle('vsc-state-color', stateColor != null);
      const px = (value) => (value == null || value === '') ? null : `${value}px`;
      setCardVariable('--vsc-name-font-size', px(config.name_font_size));
      card.classList.toggle('vsc-name-size', px(config.name_font_size) != null);
      setCardVariable('--vsc-state-font-size', px(config.state_font_size));
      card.classList.toggle('vsc-state-size', px(config.state_font_size) != null);

      // Corner radii and main background through Bubble Card's own variables
      // ('card-type' resolves to 'button' on button cards).
      setCardVariable('--bubble-button-border-radius', px(config.card_border_radius));
      setCardVariable('--bubble-button-icon-border-radius', px(config.icon_border_radius));
      setCardVariable('--bubble-sub-button-border-radius', px(config.subbutton_border_radius));
      const cardBackground = resolveColor(config.manual_card_background_color, config.custom_card_background_color);
      const cardBackgroundOpacity = config.card_background_opacity ?? 1;
      let cardBackgroundValue = null;
      if (cardBackground != null || cardBackgroundOpacity < 1) {
        const base = cardBackground ??
          'var(--bubble-main-background-color, var(--background-color-2, var(--secondary-background-color)))';
        cardBackgroundValue = cardBackgroundOpacity < 1
          ? `color-mix(in srgb, ${base} ${Math.round(cardBackgroundOpacity * 100)}%, transparent)`
          : base;
      }
      setCardVariable('--bubble-button-main-background-color', cardBackgroundValue);

      const functionButtonColor = config.enable_function_button_color === true
        ? (resolveColor(config.manual_function_button_color, config.function_button_color) ?? 'rgba(255, 255, 255, 0.9)')
        : null;
      setCardVariable('--function-button-color', functionButtonColor);
      card.classList.toggle('use-function-button-color', functionButtonColor != null);

      // Hover/active polish was always on before it got a switch, so only an
      // explicit false turns it off.
      card.classList.toggle('vsc-interaction-effects', config.enable_interaction_effects !== false);

      // Apply background visibility toggling
      card.classList.toggle('hide-icon-background', config.hide_icon_background === true);

      // Apply sub-button background visibility - automatically hide if helper is enabled
      if (config.hide_subbutton_background === true || config.enable_icon_helper === true) {
        card.classList.add('hide-subbutton-background');
      } else {
        card.classList.remove('hide-subbutton-background');
      }

      // The CSS .hide-subbutton-background class handles this; avoid inline
      // writes that could overwrite Bubble Card or another module's own styling.

      // Restore only inline styles owned by this module. Native Bubble Card
      // can update other inline styles independently during state changes.
      function applyOwnedIconColor(icon, color) {
        if (!icon) return;
        if (color != null) {
          if (!Object.prototype.hasOwnProperty.call(icon.dataset, 'vscAppliedColor')) {
            icon.dataset.vscPreviousColor = icon.style.getPropertyValue('color');
            icon.dataset.vscPreviousPriority = icon.style.getPropertyPriority('color');
          }
          if (icon.style.getPropertyValue('color') !== color || icon.style.getPropertyPriority('color') !== 'important') {
            icon.style.setProperty('color', color, 'important');
          }
          icon.dataset.vscAppliedColor = color;
        } else if (Object.prototype.hasOwnProperty.call(icon.dataset, 'vscAppliedColor')) {
          if (icon.style.getPropertyValue('color') === icon.dataset.vscAppliedColor) {
            if (icon.dataset.vscPreviousColor) {
              icon.style.setProperty('color', icon.dataset.vscPreviousColor, icon.dataset.vscPreviousPriority);
            } else {
              icon.style.removeProperty('color');
            }
          }
          delete icon.dataset.vscAppliedColor;
          delete icon.dataset.vscPreviousColor;
          delete icon.dataset.vscPreviousPriority;
        }
      }

      function getEntityColor(entityId) {
        const entityState = hass?.states?.[entityId];
        if (!entityId || !entityState) return null;
        if (entityState.state === 'on' && Array.isArray(entityState.attributes?.rgb_color)) {
          const rgb = entityState.attributes.rgb_color;
          return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
        }
        const activeStates = ['on', 'home', 'active', 'open', 'unlocked', 'detected'];
        const inactiveStates = ['off', 'away', 'inactive', 'closed', 'locked', 'clear'];
        const errorStates = ['unavailable', 'unknown'];
        const isFunction = /^(scene|script|automation)\./.test(entityId);
        // Home Assistant's theme state colors, falling back to the old fixed ones.
        const domain = entityId.split('.')[0];
        const themed = config.use_theme_state_colors === true;
        const activeColor = themed
          ? `var(--state-${domain}-active-color, var(--state-active-color, rgb(140, 200, 105)))` : 'rgb(140, 200, 105)';
        const inactiveColor = themed
          ? `var(--state-${domain}-inactive-color, var(--state-inactive-color, rgb(150, 150, 150)))` : 'rgb(150, 150, 150)';
        const errorColor = themed ? 'var(--state-unavailable-color, rgb(180, 180, 180))' : 'rgb(180, 180, 180)';
        if (isFunction && functionButtonColor != null) return functionButtonColor;
        if (activeStates.includes(entityState.state)) return activeColor;
        if (inactiveStates.includes(entityState.state) || errorStates.includes(entityState.state)) {
          if (functionButtonColor != null) return functionButtonColor;
          return inactiveStates.includes(entityState.state) ? inactiveColor : errorColor;
        }
        return null;
      }

      function getFunctionOnlyColor(entityId) {
        if (functionButtonColor == null) return null;
        const st = hass?.states?.[entityId];
        if (!entityId || !st || /^(scene|script|automation)\./.test(entityId)) return functionButtonColor;
        return ['off', 'away', 'inactive', 'closed', 'locked', 'clear', 'unavailable', 'unknown'].includes(st.state)
          ? functionButtonColor : null;
      }

      const mainEntityId = this.config.entity;
      const mainColor = (config.enable_entity_colored_main_icon === true && getEntityColor(mainEntityId)) ||
        getFunctionOnlyColor(mainEntityId);
      applyOwnedIconColor(card.querySelector('.bubble-icon'), mainColor);

      // Match Bubble Card's actual class numbering in updateGroupButtons().
      // In mixed layouts explicit groups are indexed first, followed by the
      // implicit main group, then bottom groups and bottom individual buttons.
      // Flattening YAML order directly would color the wrong icons.
      const subButtonConfigs = [];
      const collectSubButtons = (items) => {
        if (!Array.isArray(items)) return;
        items.forEach(item => {
          if (!item) return;
          if (Array.isArray(item.group)) collectSubButtons(item.group);
          else subButtonConfigs.push(item);
        });
      };
      const configuredSubButtons = this.config.sub_button;
      // The sub-buttons card renders only the bottom section and drops a
      // leftover main section before numbering (cards/sub-buttons/index.js).
      const mainItems = this.config.card_type === 'sub-buttons' ? []
        : Array.isArray(configuredSubButtons) ? configuredSubButtons
        : (Array.isArray(configuredSubButtons?.main) ? configuredSubButtons.main : []);
      const bottomItems = Array.isArray(configuredSubButtons?.bottom) ? configuredSubButtons.bottom : [];
      const mainGroups = mainItems.filter(item => Array.isArray(item?.group) && item.group.length > 0);
      const bottomGroups = bottomItems.filter(item => Array.isArray(item?.group) && item.group.length > 0);
      const mainSingles = mainItems.filter(item => item && !Array.isArray(item.group));
      const bottomSingles = bottomItems.filter(item => item && !Array.isArray(item.group));
      const mainLayout = configuredSubButtons?.main_layout ?? 'inline';
      const mainUsesAutoGroup = mainLayout === 'rows' || mainGroups.length > 0 ||
        bottomGroups.length > 0 || bottomSingles.length > 0;
      if (!mainUsesAutoGroup) collectSubButtons(mainSingles);
      mainGroups.forEach(item => collectSubButtons(item.group));
      if (mainUsesAutoGroup) collectSubButtons(mainSingles);
      bottomGroups.forEach(item => collectSubButtons(item.group));
      collectSubButtons(bottomSingles);
      subButtonConfigs.forEach((buttonConfig, index) => {
        const icon = card.querySelector(`.bubble-sub-button-${index + 1} .bubble-sub-button-icon`);
        // Bubble Card falls back to the parent entity when the sub-button has none.
        const entityId = buttonConfig.entity ?? this.config.entity;
        const color = (config.enable_entity_colored_subicons === true && getEntityColor(entityId)) ||
          getFunctionOnlyColor(entityId);
        applyOwnedIconColor(icon, color);
      });

      // Icon Contrast Helper Implementation
      if (config.enable_icon_helper === true) {
        card.classList.add('icon-helper-enabled');

        // Set helper colors and properties
        let helperColor;
        if (config.manual_helper_color) {
          helperColor = config.manual_helper_color;
        } else if (config.helper_color) {
          const colorArray = config.helper_color;
          helperColor = Array.isArray(colorArray)
            ? `rgba(${colorArray[0]}, ${colorArray[1]}, ${colorArray[2]}, ${config.helper_opacity ?? 0.7})`
            : colorArray;
        } else {
          // Default to a light grey if no color specified
          helperColor = `rgba(255, 255, 255, ${config.helper_opacity ?? 0.7})`;
        }

        setCardVariable('--helper-color', helperColor);
        setCardVariable('--helper-size', config.helper_size_ratio ?? 0.7);
        setCardVariable('--fade-strength', config.fade_strength ?? 1.0);

        if (config.enable_helper_fade === true) {
          card.classList.add('helper-fade-enabled');
        } else {
          card.classList.remove('helper-fade-enabled');
        }

        if (config.apply_to_main_icon !== false) {
          card.classList.add('helper-main-icon');
        } else {
          card.classList.remove('helper-main-icon');
        }

        if (config.apply_to_sub_icons !== false) {
          card.classList.add('helper-sub-icons');
        } else {
          card.classList.remove('helper-sub-icons');
        }
      } else {
        card.classList.remove('icon-helper-enabled', 'helper-fade-enabled', 'helper-main-icon', 'helper-sub-icons');
      }

      // Slider Contrast Helper Implementation - Only apply when Card Background gradient is active
      if (config.enable_slider_helper === true && gradientTarget === 'background' && config.enable_gradient === true) {
        card.classList.add('slider-helper-enabled');

        // Set slider helper colors and properties
        let sliderHelperColor;
        if (config.manual_slider_helper_color) {
          sliderHelperColor = config.manual_slider_helper_color;
        } else if (config.slider_helper_color) {
          const colorArray = config.slider_helper_color;
          sliderHelperColor = Array.isArray(colorArray)
            ? `rgba(${colorArray[0]}, ${colorArray[1]}, ${colorArray[2]}, ${config.slider_helper_opacity ?? 0.7})`
            : colorArray;
        } else {
          // Default to black if no color specified
          sliderHelperColor = `rgba(0, 0, 0, ${config.slider_helper_opacity ?? 0.7})`;
        }

        setCardVariable('--slider-helper-color', sliderHelperColor);
        setCardVariable('--slider-helper-size', config.slider_helper_size_ratio ?? 0.7);
        setCardVariable('--slider-fade-strength', config.slider_fade_strength ?? 1.0);

        if (config.enable_slider_helper_fade === true) {
          card.classList.add('slider-helper-fade-enabled');
        } else {
          card.classList.remove('slider-helper-fade-enabled');
        }
      } else {
        card.classList.remove('slider-helper-enabled', 'slider-helper-fade-enabled');
      }

      // Collect the final gradient before updating the DOM.
      let appliedGradient = null;

      if (config.enable_gradient === true && gradientEntity) {
        const entityId = gradientEntity;
        const entityState = hass?.states?.[entityId];
        let coloredLights = [];

        // Get light colors from group or single light
        if (Array.isArray(entityState?.attributes?.entity_id)) {
          entityState.attributes.entity_id.forEach(childId => {
            if (childId.startsWith('light.')) {
              const lightState = hass?.states?.[childId];
              if (lightState?.state === 'on' && Array.isArray(lightState.attributes?.rgb_color) && lightState.attributes.rgb_color.length >= 3) {
                coloredLights.push({
                  rgb: lightState.attributes.rgb_color,
                  brightness: lightState.attributes.brightness || 255,
                  friendly_name: lightState.attributes.friendly_name || childId
                });
              }
            }
          });
        } else if (entityState?.state === 'on' && Array.isArray(entityState.attributes?.rgb_color) && entityState.attributes.rgb_color.length >= 3) {
          coloredLights.push({
            rgb: entityState.attributes.rgb_color,
            brightness: entityState.attributes.brightness || 255,
            friendly_name: entityState.attributes.friendly_name || entityId
          });
        }

        // Always read child states above: Bubble Card's trackedHass observes
        // these dependencies and will refresh on external child RGB changes.
        // hasChanged only skips expensive hue sorting when the inputs are equal.
        const gradientProperty = gradientTarget === 'background' ? '--card-gradient' : '--slider-gradient';
        const gradientInputs = coloredLights.map(light => light.rgb.slice(0, 3).join(','));
        // 'to right' equals 90deg and keeps the previous output when unset.
        const gradientDirection = config.gradient_angle == null ? 'to right' : `${config.gradient_angle}deg`;
        const needsGradientRebuild = typeof hasChanged !== 'function' ||
          hasChanged('vsc-gradient', gradientEntity, gradientTarget, config.disable_default_gradient === true, gradientInputs, gradientDirection);
        const previousGradient = card.style.getPropertyValue(gradientProperty);

        if (!needsGradientRebuild && previousGradient) {
          appliedGradient = previousGradient;
        } else if (coloredLights.length > 0) {
          // RGB to HSL conversion helper
          const rgbToHsl = (r, g, b) => {
            r /= 255; g /= 255; b /= 255;
            const max = Math.max(r, g, b), min = Math.min(r, g, b);
            let h, s, l = (max + min) / 2;
            if (max === min) {
              h = s = 0;
            } else {
              const d = max - min;
              s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
              switch (max) {
                case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                case g: h = (b - r) / d + 2; break;
                case b: h = (r - g) / d + 4; break;
              }
              h /= 6;
            }
            return [h * 360, s * 100, l * 100];
          };

          // Sort lights by hue for smoother gradients
          const sortedLights = [...coloredLights].sort((a, b) => {
            const [h1] = rgbToHsl(a.rgb[0], a.rgb[1], a.rgb[2]);
            const [h2] = rgbToHsl(b.rgb[0], b.rgb[1], b.rgb[2]);
            return h1 - h2;
          });

          // Generate gradient based on number of lights
          let gradientColors = '';
          if (sortedLights.length === 1) {
            const light = sortedLights[0];
            const [h, s, l] = rgbToHsl(light.rgb[0], light.rgb[1], light.rgb[2]);
            gradientColors = `
              hsl(${h}, ${s}%, ${Math.max(l - 15, 0)}%) 0%,
              hsl(${h}, ${s}%, ${l}%) 50%,
              hsl(${h}, ${s}%, ${Math.min(l + 15, 100)}%) 100%
            `;
          } else if (sortedLights.length === 2) {
            gradientColors = `rgb(${sortedLights[0].rgb[0]}, ${sortedLights[0].rgb[1]}, ${sortedLights[0].rgb[2]}) 0%, rgb(${sortedLights[1].rgb[0]}, ${sortedLights[1].rgb[1]}, ${sortedLights[1].rgb[2]}) 100%`;
          } else {
            const stops = [];
            const n = sortedLights.length;

            // Create gradient stops distributed across the range
            for (let i = 0; i < n; i++) {
              let pos = (i / (n - 1)) * 100;
              stops.push({ rgb: sortedLights[i].rgb, position: Math.round(pos) });
            }
            gradientColors = stops.map(stop => `rgb(${stop.rgb[0]}, ${stop.rgb[1]}, ${stop.rgb[2]}) ${stop.position}%`).join(', ');
          }

          appliedGradient = `linear-gradient(${gradientDirection}, ${gradientColors})`;
        } else if (config.disable_default_gradient !== true) {
          // Fallback rainbow gradient if no colored lights are found and option is not disabled
          appliedGradient = `linear-gradient(${gradientDirection}, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #9400D3)`;
        }
      }

      const backgroundGradientActive = appliedGradient != null && gradientTarget === 'background';
      card.classList.toggle('use-gradient-background', backgroundGradientActive);
      card.classList.toggle('use-gradient-slider', appliedGradient != null && !backgroundGradientActive);
      setCardVariable('--card-gradient', backgroundGradientActive ? appliedGradient : null);
      setCardVariable('--slider-gradient', backgroundGradientActive ? null : appliedGradient);

      // Restore our own changes when disconnected OR when the module is
      // removed from a still-mounted card using setConfig(). Bubble Card's
      // native onTeardown currently runs on disconnect, not on this edit path.
      const cleanupVSC = () => {
        Array.from(ownedVariables.keys()).forEach(restoreOwnedVariable);
        applyOwnedIconColor(card.querySelector('.bubble-icon'), null);
        card.querySelectorAll('.bubble-sub-button-icon').forEach(icon => applyOwnedIconColor(icon, null));
        initialClasses.forEach((wasPresent, name) => card.classList.toggle(name, wasPresent));
        if (card._vscOwnedVariables === ownedVariables) delete card._vscOwnedVariables;
        if (card._vscInitialClasses === initialClasses) delete card._vscInitialClasses;
      };
      // Update the current cleanup callback on each pass without stacking hooks.
      this._vscCleanupCurrent = cleanupVSC;
      if (typeof this.setConfig === 'function' && !this._vscSetConfigWrapper) {
        const host = this;
        const originalSetConfig = this.setConfig;
        // VSC is applied either through the card's `modules:` list (the normal
        // way, "!id" excludes it) or embedded in `styles`. A global module is
        // in neither, so its removal cannot be seen here and is left alone.
        const usesVSC = (cfg) => {
          const modules = Array.isArray(cfg?.modules) ? cfg.modules
            : (typeof cfg?.modules === 'string' ? [cfg.modules] : []);
          return (modules.includes('visual_styling_center') &&
              !modules.includes('!visual_styling_center')) ||
            String(cfg?.styles ?? '').includes('this.config.visual_styling_center');
        };
        const wrappedSetConfig = function(nextConfig) {
          // Only react to removing VSC: a still-active VSC rewrites its own
          // state on the next style pass anyway.
          if (usesVSC(host.config) && !usesVSC(nextConfig)) {
            host._vscCleanupCurrent?.();
          }
          return originalSetConfig.call(this, nextConfig);
        };
        this._vscSetConfigWrapper = { originalSetConfig, wrappedSetConfig };
        this.setConfig = wrappedSetConfig;
      }
      if (typeof onTeardown === 'function') {
        onTeardown(() => {
          cleanupVSC();
          const wrapper = this._vscSetConfigWrapper;
          if (wrapper && this.setConfig === wrapper.wrappedSetConfig) {
            this.setConfig = wrapper.originalSetConfig;
          }
          delete this._vscSetConfigWrapper;
          delete this._vscCleanupCurrent;
        });
      }

      return '';
    })()}
    /* Card size adjustments */
    .bubble-button-card-container {
      height: calc(var(--height-multiplier, 1) * 50px) !important;
      box-sizing: border-box !important;
      /* Reduce z-index to avoid conflicts with editor menus */
      z-index: 0 !important; /* Further reduced to prevent any menu conflicts */
    }
    /* Inner padding adjustments */
    .bubble-button-card {
      padding: var(--inner-padding, 0px) !important;
      box-sizing: border-box !important;
      height: 100% !important;
    }
    /* Native Bubble Card manages default slider colors and interaction states.
       VSC only overrides the main slider when an explicit gradient is active. */

    /* Gradient slider styles - target only the slider fill */
    .use-gradient-slider .bubble-button-card-container > .bubble-range-slider > .bubble-range-fill {
      background: var(--slider-gradient) !important;
      background-size: 100% 100% !important;
      background-position: center !important;
      border-radius: 12px !important;
      opacity: 1 !important;
    }

    /* Card background gradient styles */
    .use-gradient-background .bubble-button-card {
      background: var(--card-gradient) !important;
      position: relative !important;
    }

    /* Improve slider visibility with background gradient - move to bottom edge */
    .use-gradient-background .bubble-button-card-container > .bubble-range-slider > .bubble-range-fill {
      background-color: rgba(255, 255, 255, var(--slider-bg-opacity, 0.6)) !important; /* Higher contrast */
      box-shadow: 0 0 4px rgba(255, 255, 255, 0.8) !important; /* Glow effect */
      height: 12px !important; /* Thinner height */
      border-radius: 6px !important;
      top: auto !important; /* Remove vertical centering */
      bottom: 0px !important; /* Position at bottom with small margin */
      z-index: 1 !important;
    }

    /* Slider Contrast Helper Implementation - creating a glow effect around the edges */
    .slider-helper-enabled.use-gradient-background .bubble-button-card-container > .bubble-range-slider > .bubble-range-fill {
      /* Maintain existing styles but add glow effect */
      box-shadow: 0 0 calc(3px * var(--slider-helper-size, 0.7)) var(--slider-helper-color, rgba(0, 0, 0, 0.7)) !important;
    }

    .slider-helper-fade-enabled.use-gradient-background .bubble-button-card-container > .bubble-range-slider > .bubble-range-fill {
      /* For the fade effect, a more complex shadow with variable fade strength */
      box-shadow: 
        0 0 calc(2px * var(--slider-helper-size, 0.7)) var(--slider-helper-color, rgba(0, 0, 0, 0.7)),
        0 0 calc(6px * var(--slider-helper-size, 0.7)) var(--slider-helper-color, rgba(0, 0, 0, 0.5)),
        0 0 calc(12px * var(--slider-fade-strength, 1.0)) var(--slider-helper-color, rgba(0, 0, 0, 0.3)) !important;
    }

    /* Make sure other elements stay on top but don't interfere with menus */
    .bubble-icon-container, 
    .bubble-name-container,
    .bubble-sub-button-container {
      z-index: 1 !important;
      position: relative !important;
    }
    /* Apply independent row and column spacing to sub-buttons */
    .bubble-sub-button-container {
      margin-inline-end: var(--subbutton-horizontal-margin, 8px) !important;
      row-gap: var(--subbutton-row-spacing, 10px) !important;
      column-gap: var(--subbutton-column-spacing, 10px) !important;
    }
    /* Since v3 the buttons can sit inside groups (rows layout, explicit or
       bottom groups), where the container gap no longer reaches them. The
       8px fallback is Bubble Card's own group gap, so unset options change
       nothing. */
    .bubble-sub-button-container .bubble-sub-button-group,
    .bubble-sub-button-bottom-container .bubble-sub-button-group {
      row-gap: var(--subbutton-row-spacing, 8px);
      column-gap: var(--subbutton-column-spacing, 8px);
    }
    /* Make sub-buttons size independent from main icon margin */
    /* A sub-button's own "custom_height" (set by Bubble Card as
       --bubble-sub-button-height on that button) wins over the module size. */
    .bubble-sub-button {
      height: var(--bubble-sub-button-height, calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 32px)) !important;
      min-height: var(--bubble-sub-button-height, calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 32px)) !important;
    }
    /* Always visible (inline) sub-sliders are not .bubble-sub-button elements;
       Bubble Card sizes them with this variable, so they follow the same height. */
    .bubble-sub-button-container,
    .bubble-sub-button-bottom-container {
      --bubble-sub-slider-height: calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 32px);
    }
    .vsc-custom-subbutton-background .bubble-sub-button {
      background-color: var(--subbutton-background-color) !important;
    }
    /* Hide sub-button backgrounds when option is enabled - with !important to override inline styles */
    .hide-subbutton-background .bubble-sub-button {
      background-color: transparent !important;
      background: none !important;
      border-color: transparent !important;
      box-shadow: none !important;
    }
    /* Apply margins to icon container - separate from sub-buttons */
    .bubble-icon-container {
      margin: var(--icon-vertical-margin, 6px) !important;
      min-height: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
      height: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
      width: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
      min-width: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
    }
    .vsc-custom-icon-background .bubble-icon-container {
      background-color: var(--icon-background-color) !important;
    }
    /* Name and state text (only while an option is set) */
    .vsc-name-color .bubble-name {
      color: var(--vsc-name-color) !important;
    }
    .vsc-state-color .bubble-state {
      color: var(--vsc-state-color) !important;
    }
    .vsc-name-size .bubble-name {
      font-size: var(--vsc-name-font-size) !important;
    }
    .vsc-state-size .bubble-state {
      font-size: var(--vsc-state-font-size) !important;
    }
    /* Specific rule to fully hide icon background when enabled */
    .hide-icon-background .bubble-icon-container {
      background-color: transparent !important;
      background: none !important;
    }
    /* Adjust main icon size and color according to multiplier */
    .bubble-icon-container .bubble-icon {
      --mdc-icon-size: calc(var(--icon-size-multiplier, 1) * 24px) !important;
      color: var(--icon-color, inherit) !important;
    }
    /* Scale sub-button icons with independent multiplier */
    .bubble-sub-button .bubble-sub-button-icon {
      --mdc-icon-size: calc(var(--subicon-size-multiplier, 1) * 18px) !important;
      color: var(--subicon-color, inherit) !important;
    }

    /* Function/Offline button color styling - now includes main icon */
    .use-function-button-color .bubble-sub-button ha-icon[style*="rgb(150, 150, 150)"],
    .use-function-button-color .bubble-sub-button ha-icon[style*="rgb(180, 180, 180)"] {
      color: var(--function-button-color, rgba(255, 255, 255, 0.9)) !important;
    }

    /* Enhanced styling for entity colored sub-icons */
    .bubble-sub-button ha-icon,
    .bubble-sub-button-icon ha-icon,
    .bubble-sub-button-icon,
    .bubble-icon-container .bubble-icon {
      transition: color 0.3s ease !important;
    }
    /* Large layout support */
    .large .bubble-button-card-container {
      height: calc(var(--height-multiplier, 1) * var(--row-height, 56px) * var(--row-size, 1) + var(--row-gap, 8px) * (var(--row-size, 1) - 1)) !important;
    }
    .large .bubble-icon-container {
      margin: var(--icon-vertical-margin, 8px) !important;
      min-height: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 42px) !important;
      height: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 42px) !important;
      width: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 42px) !important;
      min-width: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 42px) !important;
    }
    /* Large layout icon sizing */
    .large .bubble-icon-container .bubble-icon {
      --mdc-icon-size: calc(var(--icon-size-multiplier, 1) * 24px) !important;
    }
    /* Line height adjustment for name container */
    .bubble-name-container {
      line-height: calc(var(--height-multiplier, 1) * 18px);
    }
    /* Multi-row layout support with independent sub-button sizing */
    .rows-2 .bubble-sub-button {
      height: var(--bubble-sub-button-height, calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 20px)) !important;
    }
    .rows-2 .bubble-sub-button-container,
    .rows-2 .bubble-sub-button-bottom-container {
      --bubble-sub-slider-height: calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 20px);
    }
    /* Large layout sub-button margin */
    .large .bubble-sub-button-container {
      margin-inline-end: var(--subbutton-horizontal-margin, 14px) !important;
      row-gap: var(--subbutton-row-spacing, 10px) !important;
      column-gap: var(--subbutton-column-spacing, 10px) !important;
    }
    /* Large layout sub-button icon sizing */
    .large .bubble-sub-button .bubble-sub-button-icon {
      --mdc-icon-size: calc(var(--subicon-size-multiplier, 1) * 18px) !important;
    }

    /* Icon Contrast Helper */
    .icon-helper-enabled.helper-main-icon .bubble-icon {
      position: relative !important;
      z-index: 2 !important;
    }

    .icon-helper-enabled.helper-main-icon .bubble-icon::before {
      content: "" !important;
      position: absolute !important;
      width: calc(100% * var(--helper-size, 0.7)) !important;
      height: calc(100% * var(--helper-size, 0.7)) !important;
      background-color: var(--helper-color, rgba(255, 255, 255, 0.7)) !important;
      border-radius: 50% !important;
      z-index: -1 !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      transition: all 0.2s ease !important;
    }

    .icon-helper-enabled.helper-fade-enabled.helper-main-icon .bubble-icon::before {
      background: radial-gradient(circle, var(--helper-color, rgba(255, 255, 255, 0.7)) 0%, transparent calc(100% * var(--fade-strength, 1.0))) !important;
    }

    .icon-helper-enabled.helper-sub-icons .bubble-sub-button ha-icon,
    .icon-helper-enabled.helper-sub-icons .bubble-sub-button-icon ha-icon {
      position: relative !important;
      z-index: 2 !important;
    }

    .icon-helper-enabled.helper-sub-icons .bubble-sub-button ha-icon::before,
    .icon-helper-enabled.helper-sub-icons .bubble-sub-button-icon ha-icon::before {
      content: "" !important;
      position: absolute !important;
      width: calc(100% * var(--helper-size, 0.7)) !important;
      height: calc(100% * var(--helper-size, 0.7)) !important;
      background-color: var(--helper-color, rgba(255, 255, 255, 0.7)) !important;
      border-radius: 50% !important;
      z-index: -1 !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      transition: all 0.2s ease !important;
    }

    .icon-helper-enabled.helper-fade-enabled.helper-sub-icons .bubble-sub-button ha-icon::before,
    .icon-helper-enabled.helper-fade-enabled.helper-sub-icons .bubble-sub-button-icon ha-icon::before {
      background: radial-gradient(circle, var(--helper-color, rgba(255, 255, 255, 0.7)) 0%, transparent calc(100% * var(--fade-strength, 1.0))) !important;
    }

    /* Interaction effects (enable_interaction_effects, on unless set to false) */
    /* Make sub-button icons brighter and more visible */
    .vsc-interaction-effects .bubble-sub-button ha-icon {
      opacity: 0.9 !important;
    }

    /* Enhance icons in active states for better visibility */
    .vsc-interaction-effects .is-on .bubble-icon,
    .vsc-interaction-effects.is-on .bubble-icon {
      opacity: 1 !important;
      filter: brightness(1.1) !important;
    }

    /* Highlight elements on hover/focus for better interaction cues */
    .vsc-interaction-effects .bubble-sub-button:hover ha-icon,
    .vsc-interaction-effects .bubble-sub-button:focus ha-icon,
    .vsc-interaction-effects .bubble-icon-container:hover .bubble-icon,
    .vsc-interaction-effects .bubble-icon-container:focus .bubble-icon {
      filter: brightness(1.2) !important;
    }
```
</details>

### Screenshots:
<img width="406" height="633" alt="waterfox_VjDlqItfQ1" src="https://github.com/user-attachments/assets/dc3c4c4c-bc92-4827-a4dd-2a39479619d2" />

![waterfox_bF9E7AZtjY](https://github.com/user-attachments/assets/d940315b-7254-443c-ba35-a4342f4419fe)
![waterfox_hzipGGgXu0](https://github.com/user-attachments/assets/ea2f70c0-2e8c-4875-801f-4a9c03252c29)
![waterfox_4A6TiysRhb](https://github.com/user-attachments/assets/cf6af9a5-76b5-495e-8388-7c13581a5221)




