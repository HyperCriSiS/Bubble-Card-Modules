# Bubble Card Modules

**Modules that add styling, badges and gestures to Bubble Card in Home Assistant.**

[![License](https://img.shields.io/github/license/HyperCriSiS/Bubble-Card-Modules)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-dashboard-41BDF5?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![Bubble Card](https://img.shields.io/badge/Bubble%20Card-module-8A2BE2)](https://github.com/Clooos/Bubble-Card)

Bubble Card can be extended with modules: YAML snippets that bring their own editor, CSS and JavaScript. This repository collects independent modules, each in its own folder with its documentation, changelog and the module YAML. The modules change how existing Bubble Card cards look and react; they add no new card types.

> [!IMPORTANT]
> The modules need [Bubble Card](https://github.com/Clooos/Bubble-Card) in Home Assistant. Each module lists the cards it supports.

## 📦 Installation

1. Install [Bubble Card Tools](https://github.com/Clooos/Bubble-Card-Tools). The integration enables the Module Store.
2. Open a Bubble Card in the dashboard editor, go to **Modules** and switch to the **Module Store** tab.
3. Search for the module and click **Install**. The Module Store also shows updates for installed modules.
4. Apply the module to the card in the **My Modules** tab and configure it in the editor.

> [!TIP]
> Without the Module Store, copy the YAML from the module's documentation and use **My Modules → Import from YAML**.

## 🧩 Available modules

| Module | Description |
|---|---|
| [Visual Styling Center](Visual-Styling-Center/Visual-Styling-Center.md) | Sizes, spacing, colors, state colors, contrast helpers and gradients for buttons and sub-buttons. |
| [Badgy Condition Helper](Badgy-Conditions/Badgy-Conditions.md) | Value and icon badges, condition-based backgrounds, icons and animations. |
| [Button Stack Gestures](Button-Stack-Gestures/Button-Stack-Gestures.md) | Experimental. Hold, swipe and tap actions for the buttons of the horizontal buttons stack. |

### Visual Styling Center

Precise control over the look of button cards, from sizes and spacing to colors and light-following gradients.

- **Card:** height multiplier, inner padding, background color and opacity, corner radius.
- **Main icon:** size, background ratio, margin, corner radius, icon and background color, hidden background.
- **Sub-buttons:** icon size, background ratio, outer margin, row and column spacing (also inside groups), icon and background color, corner radius, hidden backgrounds. Always visible sub-button sliders follow the sub-button height.
- **Name and state text:** color and font size for both.
- **State colors:** Home Assistant theme state colors, main icon and sub-button icons colored by entity state (light color when on), custom colors for off, offline and function entities such as scenes and scripts.
- **Icon contrast helper:** a background circle behind main and sub-button icons with color, opacity, size and an optional radial fade.
- **Gradient effects:** gradients on the slider fill or the card background that follow a light or light group, with direction, slider brightness and an optional rainbow fallback.
- **Slider contrast helper:** glow behind the slider on gradient backgrounds, with color, opacity, size and radial fade.
- **Interaction effects:** hover highlight and brighter active icons, or Bubble Card's native look.
- Works with the normal, large and multi-row layouts and tracks entity states without polling.

Not supported: cover, climate, horizontal buttons stack, media player, pop-up, select and separator cards.

### Badgy Condition Helper

Badges, condition-based colors, icons and animations that react to the state of your home.

- **Entity badges:** state or attribute values on sub-buttons and the main icon, with translated states or custom text.
- **Icon badges:** icons instead of values.
- **Badge styling:** color, position and size per badge, plus global defaults.
- **Conditional backgrounds:** solid color, two-color or three-color gradients for sub-buttons and the main icon, with an opacity that keeps icon and text fully visible.
- **Dynamic colors:** from a Jinja template or an entity or attribute.
- **Icon colors and icons:** conditional colors and icon replacement for the main icon and sub-button icons.
- **Card glow:** a conditional glow around the whole card.
- **Effects:** pulse, rotation, glow, shake, float, zoom, heartbeat, spin, flip and vibrate for icons, badges and sub-buttons, with custom glow colors.
- **Rule lists everywhere:** several conditions in priority order, first match wins, with an optional fallback. A badge rule can change color, text, icon and effect at once.
- **Bubble Card conditions:** state, numeric state, time, screen, user and template conditions.

Not supported: cover, horizontal buttons stack, media player, pop-up and separator cards. The large layout is recommended.

### Button Stack Gestures

> [!WARNING]
> Experimental and not yet available in the Module Store. Install it with **My Modules → Import from YAML** using the YAML from its [documentation](Button-Stack-Gestures/Button-Stack-Gestures.md).

Extra gestures for the buttons of the horizontal buttons stack.

- **Hold, swipe up, swipe down and tap** per button, or one entry for all buttons with per-button overrides.
- **Any Home Assistant action:** open a pop-up, toggle, more info, perform an action, open a URL, start Assist or fire a DOM event.
- **Own entity per gesture,** falling back to the button's light entity.
- **Native tap untouched** unless a tap action is set, and a gesture never also triggers it.
- **Adjustable** hold time and swipe distance.

Supported: horizontal buttons stack only.

## 💬 Support

Report problems in the [issue tracker](https://github.com/HyperCriSiS/Bubble-Card-Modules/issues). Name the module, its version and your Bubble Card and Home Assistant versions.

## 📄 License

MIT. See [LICENSE](LICENSE).
