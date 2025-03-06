# Slider-Control-Center

**Version:** v1.0
**Creator:** [HyperCriSiS](https://github.com/my_username)

> [!IMPORTANT] 
> **Unsupported cards:**
>  - Button
>  - Cover
>  - Climate
>  - Horizontal buttons stack
>  - Media player
>  - Pop-up
>  - Select
>  - Separator

Comprehensive customization tool for Bubble Card elements. Adjust sizes, spacing, colors, and visual effects.
Optimized for Slider and 2-row-sub-buttons, but also works for normal layouts.

Configure this module via the editor or in YAML, for example: 

```yaml
slider_control_center:
entity: climate.thermostat_buro
icon: mdi:thermostat
card_layout: large
sub_button:
  - entity: sensor.thermostat_bad_temperatur
    name: Bad
    show_state: true
    show_name: false
    show_icon: true
    icon: mdi:faucet
  hide_subbutton_background: true
  custom_icon_color:
    - 255
    - 0
    - 0
```

---

<details>

<summary><b>🧩 Get this Module</b></summary>

<br>

> To use this module, simply copy and paste the following configuration into your `/www/bubble/bubble-modules.yaml` file.

```yaml
slider_control_center:
  name: Slider Control Center
  version: "v1.0"
  creator: "HyperCriSiS"
  link: "https://github.com/Clooos/Bubble-Card/discussions/1314"
  description: Comprehensive customization tool for Bubble Card elements. Adjust sizes, spacing, colors, and visual effects with focus on slider controls.
  unsupported:
      - cover
      - climate
      - horizontal-buttons-stack
      - media-player
      - pop-up
      - select
      - separator

  editor:
    - type: expandable
      title: "Card Size Adjustments"
      icon: "mdi:resize"
      schema:
        - name: height_multiplier
          label: "Card Height Multiplier"
          default: 1
          selector:
            number:
              min: 0.8
              max: 5.0
              step: 0.1
              mode: slider
              unit_of_measurement: "×"
    - type: expandable
      title: "Margin & Spacing Adjustments"
      icon: "mdi:arrow-expand"
      schema:
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
        - name: icon_vertical_margin
          label: "Main Icon Vertical Margin"
          default: 6
          selector:
            number:
              min: -10
              max: 30
              step: 1
              mode: slider
              unit_of_measurement: "px"
        - name: subbutton_horizontal_margin
          label: "Sub-button Container Right Margin"
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
    - type: expandable
      title: "Icon Size Adjustments"
      icon: "mdi:shape"
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
    - type: expandable
      title: "Visual Enhancements"
      icon: "mdi:palette"
      schema:
        - name: hide_icon_background
          label: "Hide Icon Background"
          default: false
          selector:
            boolean: {}
        - name: hide_subbutton_background
          label: "Hide Sub-button Backgrounds"
          default: false
          selector:
            boolean: {}
        - name: custom_icon_color
          label: "Icon Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_icon_color
          label: "Manual Icon Color (e.g. #FFFFFF or rgba(255,255,255,0.8))"
          selector:
            text: {}
        - name: custom_icon_background_color
          label: "Icon Background Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_icon_background_color
          label: "Manual Icon Background Color (e.g. #FFFFFF or rgba(255,255,255,0.8))"
          selector:
            text: {}
        - name: use_entity_color
          label: "Use Light Entity Color for Slider"
          default: false
          selector:
            boolean: {}
  code: |
    ${(() => {
      // Get configuration values
      const config = this.config.slider_control_center || {};

      // Only set CSS variables for values that are explicitly defined
      if (config.height_multiplier !== undefined) {
        card.style.setProperty('--height-multiplier', config.height_multiplier);
      }

      if (config.inner_padding !== undefined) {
        card.style.setProperty('--inner-padding', `${config.inner_padding}px`);
      }

      if (config.icon_vertical_margin !== undefined) {
        card.style.setProperty('--icon-vertical-margin', `${config.icon_vertical_margin}px`);
      }

      if (config.subbutton_horizontal_margin !== undefined) {
        card.style.setProperty('--subbutton-horizontal-margin', `${config.subbutton_horizontal_margin}px`);
      }

      if (config.subbutton_row_spacing !== undefined) {
        card.style.setProperty('--subbutton-row-spacing', `${config.subbutton_row_spacing}px`);
      }

      if (config.subbutton_column_spacing !== undefined) {
        card.style.setProperty('--subbutton-column-spacing', `${config.subbutton_column_spacing}px`);
      }

      if (config.icon_size_multiplier !== undefined) {
        card.style.setProperty('--icon-size-multiplier', config.icon_size_multiplier);
      }

      if (config.icon_background_ratio !== undefined) {
        card.style.setProperty('--icon-background-ratio', config.icon_background_ratio);
      }

      if (config.subicon_size_multiplier !== undefined) {
        card.style.setProperty('--subicon-size-multiplier', config.subicon_size_multiplier);
      }

      if (config.subbutton_background_ratio !== undefined) {
        card.style.setProperty('--subbutton-background-ratio', config.subbutton_background_ratio);
      }

      // Handle icon colors with priority: manual > custom RGB picker
      if (config.manual_icon_color) {
        card.style.setProperty('--icon-color', config.manual_icon_color);
      } else if (config.custom_icon_color) {
        // Convert RGB array to color string if needed
        const iconColor = config.custom_icon_color;
        const colorValue = Array.isArray(iconColor) ? 
          `rgb(${iconColor[0]}, ${iconColor[1]}, ${iconColor[2]})` : iconColor;
        card.style.setProperty('--icon-color', colorValue);
      }

      // Handle icon background colors with priority: manual > custom RGB picker
      if (config.manual_icon_background_color) {
        card.style.setProperty('--icon-background-color', config.manual_icon_background_color);
      } else if (config.custom_icon_background_color) {
        // Convert RGB array to color string if needed
        const bgColor = config.custom_icon_background_color;
        const colorValue = Array.isArray(bgColor) ? 
          `rgb(${bgColor[0]}, ${bgColor[1]}, ${bgColor[2]})` : bgColor;
        card.style.setProperty('--icon-background-color', colorValue);
      }

      // Handle hiding the icon background
      if (config.hide_icon_background === true) {
        card.style.setProperty('--icon-background-color', 'transparent');
        // Add a class to ensure the background is truly hidden
        card.classList.add('hide-icon-background');
      } else {
        card.classList.remove('hide-icon-background');
      }

      // Handle hiding the sub-button backgrounds
      if (config.hide_subbutton_background === true) {
        // Add a class to ensure all sub-button backgrounds are hidden
        card.classList.add('hide-subbutton-background');
      } else {
        card.classList.remove('hide-subbutton-background');
      }

      // Use entity color for slider
      if (config.use_entity_color === true) {
        const entityId = this.config.entity;
        if (entityId && entityId.startsWith('light.')) {
          const entityState = hass.states[entityId];
          if (entityState && entityState.attributes.rgb_color) {
            const rgb = entityState.attributes.rgb_color;
            card.style.setProperty('--slider-color', `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`);
          }
        }
      }

      return '';
    })()}

    /* Card size adjustments */
    .bubble-button-card-container {
      height: calc(var(--height-multiplier, 1) * 50px) !important;
      box-sizing: border-box !important;
    }

    /* Inner padding adjustments */
    .bubble-button-card {
      padding: var(--inner-padding, 0px) !important;
      box-sizing: border-box !important;
      height: 100% !important;
    }

    /* Range slider fixes */
    .bubble-range-slider {
      height: 100% !important;
      box-sizing: border-box !important;
      touch-action: none; /* Prevents default touch actions for better pointer tracking */
    }

    /* Style for range fill (slider) */
    .bubble-range-fill {
      background-color: var(--slider-color, var(--bubble-accent-color, var(--accent-color))) !important;
      opacity: 1 !important;
    }

    /* Apply independent row and column spacing to sub-buttons */
    .bubble-sub-button-container {
      margin-right: var(--subbutton-horizontal-margin, 8px) !important;
      row-gap: var(--subbutton-row-spacing, 10px) !important;
      column-gap: var(--subbutton-column-spacing, 10px) !important;
    }

    /* Make sub-buttons size independent from main icon margin */
    .bubble-sub-button {
      height: calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 32px) !important;
      min-height: calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 32px) !important;
    }

    /* Hide sub-button backgrounds when option is enabled */
    .hide-subbutton-background .bubble-sub-button {
      background-color: transparent !important;
      background: none !important;
    }

    /* Apply margins to icon container - separate from sub-buttons */
    .bubble-icon-container {
      margin: var(--icon-vertical-margin, 6px) !important;
      min-height: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
      height: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
      width: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
      min-width: calc(var(--icon-size-multiplier, 1) * var(--icon-background-ratio, 1) * 38px) !important;
      background-color: var(--icon-background-color, var(--bubble-icon-background-color, var(--bubble-secondary-background-color))) !important;
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
      height: calc(var(--subbutton-background-ratio, 1) * var(--height-multiplier, 1) * 20px) !important;
    }

    /* Large layout sub-button margin */
    .large .bubble-sub-button-container {
      margin-right: var(--subbutton-horizontal-margin, 14px) !important;
      row-gap: var(--subbutton-row-spacing, 10px) !important;
      column-gap: var(--subbutton-column-spacing, 10px) !important;
    }

    /* Large layout sub-button icon sizing */
    .large .bubble-sub-button .bubble-sub-button-icon {
      --mdc-icon-size: calc(var(--subicon-size-multiplier, 1) * 18px) !important;


```

</details>

---

### Screenshot:
![Slider-Control-Center](https://github.com/HyperCriSiS/Bubble-Card-Modules/blob/main/Slider-Control-Center/Slider-Control-Center.png)

