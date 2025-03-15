# Visual Styling Center

**Version:** v2025.03.15
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

A comprehensive customization module for Bubble Card with focus on gradient effects and icon styling for both cards and sub-buttons, most awesome with light entities.

## Overview

The Slider Control Center module offers advanced customization options for Bubble Card elements with a focus on visual enhancements. It provides precise control over sizes, spacing, colors, and visual effects for all supported card types.

## Core Features

- **Comprehensive size adjustments** for cards, icons, and sub-buttons
- **Advanced color options** for all elements
- **Icon Contrast Helper** for better readability with radial background effects
- **Dynamic gradient effects** based on light entities
- **Hover effects** for improved user experience
- **Automatic adjustments** for optimal display
- **Custom Slider** to see more of the visuals 

## Detailed Feature Description

### Card Size Adjustments

- **Card Height Multiplier**: Scale the overall height of your Bubble Card 

### Margin & Spacing Adjustments

- **Main Icon Vertical Margin**: Adjust vertical spacing for the main icon 
- **Sub-button Container Right Margin**: Control the right margin of the sub-button container 
- **Sub-button Row Spacing**: Set the spacing between rows of sub-buttons 
- **Sub-button Column Spacing**: Set the spacing between columns of sub-buttons 
- **Inner Card Padding**: Add padding inside the card for more spacing

### Icon Size Adjustments

- **Main Icon Size Multiplier**: Scale the size of the main icon 
- **Icon Background Ratio**: Adjust the size ratio of the icon background 
- **Sub-icon Size Multiplier**: Scale the size of sub-button icons 
- **Sub-button Background Ratio**: Adjust the size ratio of sub-button backgrounds 

### Visual Enhancements

- **Hide Icon Background**: Remove the background from the main icon
- **Hide Sub-button Backgrounds**: Remove backgrounds from all sub-buttons
- **Custom Icon Colors**: Set custom colors for main icon and sub-icons
- **Custom Background Colors**: Set custom colors for icon and sub-button backgrounds
- **Entity-Colored Sub-Icons**: Automatically color sub-buttons based on their entity state

### Icon Contrast Helper

The Icon Contrast Helper adds circular background behind icons to improve visibility and contrast regardless of the card's background color.

- **Enable Icon Contrast Helper**: Toggle the helper feature on/off
- **Apply to Main/Sub Icons**: Choose which icons get the contrast helper
- **Helper Color**: Select the background color for the helper
- **Helper Opacity**: Control the transparency of the helper background 
- **Helper Size Ratio**: Adjust how much of the icon the background covers 
- **Radial Fade Effect**: Enable a smooth fade from color to transparent
- **Fade Strength**: Control how gradual the fade effect is 

> **Note**: When enabling the Icon Contrast Helper, sub-button backgrounds are automatically hidden to prevent visual conflicts.

## Usage Examples

### Basic Height Adjustment

```yaml
visual_styling_center:
  height_multiplier: 1.5
```

### Custom Colors with Icon Helper

```yaml
visual_styling_center:
  custom_icon_color: [255, 255, 255]
  custom_icon_background_color: [0, 0, 0]
  enable_icon_helper: true
  helper_color: [255, 255, 255]
  helper_opacity: 0.7
  helper_size_ratio: 1.2
  enable_helper_fade: true
  fade_strength: 1.2
```

### Dynamic Gradient Effects

```yaml
visual_styling_center:
  enable_gradient: true
  gradient_target: background
  gradient_entity: light.living_room_group
  disable_default_gradient: false
  slider_bg_opacity: 0.8
```

---

<details>

<summary><b>ðŸ§© Get this Module</b></summary>

<br>

> To use this module, simply copy and paste the following configuration into your `/www/bubble/bubble-modules.yaml` file.

```yaml
visual_styling_center:
  name: "Visual Styling Center"
  version: "v2025.03.15"
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
      title: "Icon Contrast Helper"
      icon: "mdi:contrast-circle"
      schema:
        - name: enable_icon_helper
          label: "Enable Icon Contrast Helper"
          default: false
          selector:
            boolean: {}
        - name: apply_to_main_icon
          label: "Apply Helper to Main Icon"
          default: true
          selector:
            boolean: {}
        - name: apply_to_sub_icons
          label: "Apply Helper to Sub-Icons"
          default: true
          selector:
            boolean: {}
        - name: helper_color
          label: "Helper Background Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_helper_color
          label: "Manual Helper Color (e.g. #FFFFFF or rgba(255,255,255,0.8))"
          selector:
            text: {}
        - name: helper_opacity
          label: "Helper Background Opacity"
          default: 0.7
          selector:
            number:
              min: 0.1
              max: 1.0
              step: 0.05
              mode: slider
        - name: helper_size_ratio
          label: "Helper Size Ratio"
          default: 0.7
          selector:
            number:
              min: 0.3
              max: 1.5
              step: 0.05
              mode: slider
              unit_of_measurement: "×"
        - name: enable_helper_fade
          label: "Enable Radial Fade Effect"
          default: true
          selector:
            boolean: {}
        - name: fade_strength
          label: "Fade Strength"
          default: 1.0
          selector:
            number:
              min: 0.5
              max: 2.0
              step: 0.1
              mode: slider
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
        - name: custom_subicon_color
          label: "Sub-Button Icon Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_subicon_color
          label: "Manual Sub-Button Icon Color (e.g. #FFFFFF or rgba(255,255,255,0.8))"
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
        - name: custom_subbutton_background_color
          label: "Sub-Button Background Color (RGB)"
          selector:
            color_rgb: {}
        - name: manual_subbutton_background_color
          label: "Manual Sub-Button Background Color (e.g. #FFFFFF or rgba(255,255,255,0.8))"
          selector:
            text: {}
        - name: enable_entity_colored_subicons
          label: "Color Sub-Button Icons by Entity State"
          default: false
          selector:
            boolean: {}
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
          selector:
            select:
              options:
                - value: "slider"
                  label: "Slider Fill"
                - value: "background"
                  label: "Card Background"
        - name: gradient_entity
          label: "Gradient Entity (Light Group or Single Light)"
          selector:
            entity:
              domain: light
        - name: disable_default_gradient
          label: "Hide Gradient When All Lights Off"
          default: false
          selector:
            boolean: {}
        - name: slider_bg_opacity
          label: "Slider Brightness with Background Gradient"
          default: 0.6
          selector:
            number:
              min: 0.1
              max: 1.0
              step: 0.05
              mode: slider
  code: |
   ${(() => {
      const config = this.config.visual_styling_center || {};

      // Default gradient configuration
      if (config.gradient_target === undefined) {
        config.gradient_target = "slider";
      }
      if (config.gradient_target === 'background' && config.enable_gradient) {
        card.classList.add('slider-background-mode');
      } else {
        card.classList.remove('slider-background-mode');
      }
      if (!config.gradient_entity && this.config.entity && this.config.entity.startsWith('light.')) {
        config.gradient_entity = this.config.entity;
      }

      // Apply all size and spacing configurations
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
      if (config.slider_bg_opacity !== undefined) {
        card.style.setProperty('--slider-bg-opacity', config.slider_bg_opacity);
      } else {
        card.style.setProperty('--slider-bg-opacity', 0.6);
      }

      // Apply custom colors
      if (config.manual_icon_color) {
        card.style.setProperty('--icon-color', config.manual_icon_color);
      } else if (config.custom_icon_color) {
        const iconColor = config.custom_icon_color;
        const colorValue = Array.isArray(iconColor)
          ? `rgb(${iconColor[0]}, ${iconColor[1]}, ${iconColor[2]})`
          : iconColor;
        card.style.setProperty('--icon-color', colorValue);
      }
      if (config.manual_subicon_color) {
        card.style.setProperty('--subicon-color', config.manual_subicon_color);
      } else if (config.custom_subicon_color) {
        const subiconColor = config.custom_subicon_color;
        const colorValue = Array.isArray(subiconColor)
          ? `rgb(${subiconColor[0]}, ${subiconColor[1]}, ${subiconColor[2]})`
          : subiconColor;
        card.style.setProperty('--subicon-color', colorValue);
      }
      if (config.manual_icon_background_color) {
        card.style.setProperty('--icon-background-color', config.manual_icon_background_color);
      } else if (config.custom_icon_background_color) {
        const bgColor = config.custom_icon_background_color;
        const colorValue = Array.isArray(bgColor)
          ? `rgb(${bgColor[0]}, ${bgColor[1]}, ${bgColor[2]})`
          : bgColor;
        card.style.setProperty('--icon-background-color', colorValue);
      }
      if (config.manual_subbutton_background_color) {
        card.style.setProperty('--subbutton-background-color', config.manual_subbutton_background_color);
      } else if (config.custom_subbutton_background_color) {
        const subbgColor = config.custom_subbutton_background_color;
        const colorValue = Array.isArray(subbgColor)
          ? `rgb(${subbgColor[0]}, ${subbgColor[1]}, ${subbgColor[2]})`
          : subbgColor;
        card.style.setProperty('--subbutton-background-color', colorValue);
      }

      // Apply background visibility toggling
      if (config.hide_icon_background === true) {
        card.style.setProperty('--icon-background-color', 'transparent');
        card.classList.add('hide-icon-background');
      } else {
        card.classList.remove('hide-icon-background');
      }

      // Apply sub-button background visibility - automatically hide if helper is enabled
      if (config.hide_subbutton_background === true || config.enable_icon_helper === true) {
        card.classList.add('hide-subbutton-background');
      } else {
        card.classList.remove('hide-subbutton-background');
      }

      // Apply sub-button background visibility to individual elements
      const subButtonElements = card.querySelectorAll('.bubble-sub-button');
      subButtonElements.forEach(button => {
        if (config.hide_subbutton_background === true || config.enable_icon_helper === true) {
          button.style.backgroundColor = 'transparent';
          button.style.boxShadow = 'none';
          button.style.border = 'none';
        } else {
          button.style.backgroundColor = '';
          button.style.boxShadow = '';
          button.style.border = '';
        }
      });

      // Apply entity-colored sub-icons
      if (config.enable_entity_colored_subicons === true) {
        const subButtons = this.config.sub_button || [];
        function getEntityColor(entityId) {
          if (!entityId || !hass.states[entityId]) return null;
          const entity = hass.states[entityId];
          if (entity.state === 'on' && entity.attributes.rgb_color) {
            const rgb = entity.attributes.rgb_color;
            return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
          }
          const activeStates = ['on', 'home', 'active', 'open', 'unlocked', 'detected'];
          const inactiveStates = ['off', 'away', 'inactive', 'closed', 'locked', 'clear'];
          const errorStates = ['unavailable', 'unknown'];
          if (activeStates.indexOf(entity.state) >= 0) {
            return `rgb(140, 200, 105)`;
          } else if (inactiveStates.indexOf(entity.state) >= 0) {
            return `rgb(150, 150, 150)`;
          } else if (errorStates.indexOf(entity.state) >= 0) {
            return `rgb(180, 180, 180)`;
          }
          return null;
        }

        subButtons.forEach((buttonConfig, index) => {
          if (!buttonConfig || !buttonConfig.entity) return;
          const entityId = buttonConfig.entity;
          if (!entityId || !hass.states[entityId]) return;
          const buttonNumber = index + 1;
          try {
            const subButton = card.querySelector(`.bubble-sub-button-${buttonNumber}`);
            if (!subButton) return;
            const iconElement = subButton.querySelector('ha-icon');
            if (!iconElement) return;
            const color = getEntityColor(entityId);
            if (color) {
              iconElement.style.setProperty('color', color, 'important');
            }
          } catch (error) {
            console.error("Error applying color to sub-button " + buttonNumber, error);
          }
        });
      } else {
        const iconElements = card.querySelectorAll('.bubble-sub-button ha-icon');
        iconElements.forEach(icon => {
          icon.style.removeProperty('color');
        });
      }

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
            ? `rgba(${colorArray[0]}, ${colorArray[1]}, ${colorArray[2]}, ${config.helper_opacity || 0.7})`
            : colorArray;
        } else {
          // Default to a light grey if no color specified
          helperColor = `rgba(255, 255, 255, ${config.helper_opacity || 0.7})`;
        }

        card.style.setProperty('--helper-color', helperColor);
        card.style.setProperty('--helper-size', config.helper_size_ratio || 0.7);
        card.style.setProperty('--fade-strength', config.fade_strength || 1.0);

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

      // Reset and apply gradient effects
      card.classList.remove('use-gradient-slider');
      card.classList.remove('use-gradient-background');
      card.style.removeProperty('--slider-gradient');
      card.style.removeProperty('--card-gradient');

      if (config.enable_gradient === true && config.gradient_entity) {
        const entityId = config.gradient_entity;
        const entityState = hass.states[entityId];
        let coloredLights = [];

        // Get light colors from group or single light
        if (entityState && entityState.attributes && entityState.attributes.entity_id) {
          entityState.attributes.entity_id.forEach(childId => {
            if (childId.startsWith('light.')) {
              const lightState = hass.states[childId];
              if (lightState && lightState.state === 'on' && lightState.attributes.rgb_color) {
                coloredLights.push({
                  rgb: lightState.attributes.rgb_color,
                  brightness: lightState.attributes.brightness || 255,
                  friendly_name: lightState.attributes.friendly_name || childId
                });
              }
            }
          });
        } else if (entityState && entityState.state === 'on' && entityState.attributes.rgb_color) {
          coloredLights.push({
            rgb: entityState.attributes.rgb_color,
            brightness: entityState.attributes.brightness || 255,
            friendly_name: entityState.attributes.friendly_name || entityId
          });
        }

        if (coloredLights.length > 0) {
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

          // Apply the gradient to the target element
          const gradient = `linear-gradient(to right, ${gradientColors})`;
          if (config.gradient_target === 'background') {
            card.style.setProperty('--card-gradient', gradient);
            card.classList.add('use-gradient-background');
          } else {
            card.style.setProperty('--slider-gradient', gradient);
            card.classList.add('use-gradient-slider');
          }
        } else if (config.disable_default_gradient !== true) {
          // Fallback rainbow gradient if no colored lights are found and option is not disabled
          const defaultGradient = 'linear-gradient(to right, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #9400D3)';
          if (config.gradient_target === 'background') {
            card.style.setProperty('--card-gradient', defaultGradient);
            card.classList.add('use-gradient-background');
          } else {
            card.style.setProperty('--slider-gradient', defaultGradient);
            card.classList.add('use-gradient-slider');
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
    /* Style for regular range fill (slider) */
    .bubble-range-fill {
      background-color: var(--slider-color, var(--bubble-accent-color, var(--accent-color))) !important;
      z-index: 2 !important;
      opacity: 1 !important;
    }

    /* Enhance clickability of slider */
    .bubble-range-slider {
      cursor: pointer !important;
      z-index: 2 !important;
    }

    .bubble-range-slider:hover {
      cursor: ew-resize !important;
    }

    /* Gradient slider styles - target only the slider fill */
    .use-gradient-slider .bubble-range-fill {
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
    .use-gradient-background .bubble-range-fill {
      background-color: rgba(255, 255, 255, var(--slider-bg-opacity, 0.6)) !important; /* Higher contrast */
      box-shadow: 0 0 4px rgba(255, 255, 255, 0.8) !important; /* Glow effect */
      height: 12px !important; /* Thinner height */
      border-radius: 6px !important;
      top: auto !important; /* Remove vertical centering */
      bottom: 0px !important; /* Position at bottom with small margin */
      z-index: 1 !important;
    }

    /* Make slider more interactive */
    .use-gradient-background .bubble-range-slider {
      z-index: 5 !important; /* Ensure top position */
      cursor: ew-resize !important; /* Better cursor indication */
    }

    /* Make sure other elements stay on top */
    .bubble-icon-container, 
    .bubble-name-container,
    .bubble-sub-button-container {
      z-index: 6 !important;
      position: relative !important;
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
      background-color: var(--subbutton-background-color, var(--bubble-sub-button-background-color, var(--bubble-secondary-background-color))) !important;
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
      color: var(--subicon-color, inherit) !important;
    }

    /* Enhanced styling for entity colored sub-icons */
    .bubble-sub-button ha-icon,
    .bubble-sub-button-icon ha-icon,
    .bubble-sub-button-icon {
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

    /* Make sub-button icons brighter and more visible */
    .bubble-sub-button ha-icon {
      opacity: 0.9 !important;
    }

    /* Enhance icons in active states for better visibility */
    .is-on .bubble-icon {
      opacity: 1 !important;
      filter: brightness(1.1) !important;
    }

    /* Highlight elements on hover/focus for better interaction cues */
    .bubble-sub-button:hover ha-icon,
    .bubble-sub-button:focus ha-icon,
    .bubble-icon-container:hover .bubble-icon,
    .bubble-icon-container:focus .bubble-icon {
      filter: brightness(1.2) !important;
    }

   return '';
    })()}



```

</details>

---

### Screenshot:
![Slider-Control-Center](https://github.com/HyperCriSiS/Bubble-Card-Modules/blob/main/Slider-Control-Center/Slider-Control-Center.png)

