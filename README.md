# Bubble Card Modules

**Modules that add styling, badges and gestures to Bubble Card in Home Assistant.**

[![License](https://img.shields.io/github/license/HyperCriSiS/Bubble-Card-Modules)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-dashboard-41BDF5?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![Bubble Card](https://img.shields.io/badge/Bubble%20Card-module-8A2BE2)](https://github.com/Clooos/Bubble-Card)

Bubble Card can be extended with modules: YAML snippets that bring their own editor, CSS and JavaScript. This repository collects independent modules, each in its own folder with its documentation, changelog and the module YAML. The modules change how existing Bubble Card cards look and react; they add no new card types.

> [!IMPORTANT]
> The modules need [Bubble Card](https://github.com/Clooos/Bubble-Card) in Home Assistant. Each module lists the cards it supports.

## 📦 Installation

1. Open a Bubble Card in the dashboard editor and go to **Modules**.
2. Install the module from the **Module Store**, or copy the YAML from the module's documentation and use **My Modules → Import from YAML** (requires Bubble Card Tools).
3. Enable the module on the card and configure it in the editor.

## 🧩 Available modules

| Module | Description |
|---|---|
| [Visual Styling Center](Visual-Styling-Center/Visual-Styling-Center.md) | Sizes, spacing, colors, state colors, contrast helpers and gradients for buttons and sub-buttons. |
| [Badgy Condition Helper](Badgy-Conditions/Badgy-Conditions.md) | Value and icon badges, condition-based backgrounds, icons and animations. |
| [Button Stack Gestures](Button-Stack-Gestures/Button-Stack-Gestures.md) | Hold, swipe and tap actions for the buttons of the horizontal buttons stack. |

## 💬 Support

Report problems in the [issue tracker](https://github.com/HyperCriSiS/Bubble-Card-Modules/issues). Name the module, its version and your Bubble Card and Home Assistant versions.

## 📄 License

MIT. See [LICENSE](LICENSE).
