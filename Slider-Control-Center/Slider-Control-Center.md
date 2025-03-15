# Slider-Control-Center

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
- **Inner Card Padding**: Add padding inside the card for more spacing

### Margin & Spacing Adjustments

- **Main Icon Vertical Margin**: Adjust vertical spacing for the main icon 
- **Sub-button Container Right Margin**: Control the right margin of the sub-button container 
- **Sub-button Row Spacing**: Set the spacing between rows of sub-buttons 
- **Sub-button Column Spacing**: Set the spacing between columns of sub-buttons 

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
slider_control_center:
  height_multiplier: 1.5
```

### Custom Colors with Icon Helper

```yaml
slider_control_center:
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
slider_control_center:
  enable_gradient: true
  gradient_target: background
  gradient_entity: light.living_room_group
  disable_default_gradient: false
  slider_bg_opacity: 0.8
```

---

<details>

<summary><b>🧩 Get this Module</b></summary>

<br>

> To use this module, simply copy and paste the following configuration into your `/www/bubble/bubble-modules.yaml` file.

```yaml


```

</details>

---

### Screenshot:
![Slider-Control-Center](https://github.com/HyperCriSiS/Bubble-Card-Modules/blob/main/Slider-Control-Center/Slider-Control-Center.png)

