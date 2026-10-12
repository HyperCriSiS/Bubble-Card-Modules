# Badgy Condition Helper

**Version:** v2026.10.12-beta
**Creator:** [HyperCriSiS](https://github.com/HyperCriSiS)

> [!IMPORTANT]
> **Unsupported cards:**
>  - Cover
>  - Horizontal buttons stack
>  - Media player
>  - Pop-up
>  - Separator


--> Large layout is recommended!

Badgy Condition Helper adds dynamic visual elements to your Bubble Card - display entity values or icons as badges, apply condition-based backgrounds and animations, and enhance your UI with reactive effects that respond to state changes in your Home Assistant environment.

## Feature Overview

### Badge System for Sub-Buttons
- **Entity Badges**: Displays states or attribute values from entities
- **Icon Badges**: Shows icons instead of values
- Color customization, positioning, and size adjustment

### Conditional Backgrounds
- For sub-buttons with various options:
  - Solid color backgrounds
  - Two-color gradients
  - Three-color gradients
- Adjustable opacity

### Main Icon Background
- Condition-based color change for the main icon
- Adjustable opacity

### Icon Effects
- For main icon and sub-button icons
- Various animation types
- Glow effects with customizable colors

### Badge Effects
- Separate effects for entity and icon badges
- Various animations and color options

### Sub-Button Effects
- Various animations and color options

### Supported Animation Types
- Standard: Pulse, Rotation, Glow, Shake, Float, Zoom, Heartbeat, Spin-360, Flip, Vibrate


Configure this module via the editor or in YAML, for example: 

```yaml
type: custom:bubble-card
card_type: button
entity: light.living_room
icon: mdi:lightbulb
name: Living Room Light
show_state: true
show_entity_picture: false
state_display: brightness
tap_action:
  action: toggle
sub_buttons:
  - entity: fan.living_room
    icon: mdi:fan
    name: Fan
  - entity: switch.living_room_plug
    icon: mdi:power-socket-eu
    name: Plug
modules:
  - name: badgy-condition-helper
    entity_badges:
      0:  # Sub-Button 1
        entity: sensor.living_room_temperature
        color: red
        show_unit: true
        decimals: 1
        h_pos: -8
        v_pos: -8
        scale: 1.2
        condition:
          condition: numeric_state
          entity: sensor.living_room_temperature
          above: 25
      1:  # Sub-Button 2
        entity: sensor.living_room_humidity
        color: blue
        show_unit: true
        decimals: 0
    icon_badges:
      0:  # Sub-Button 1
        icon: mdi:alert
        color: yellow
        condition:
          condition: state
          entity: binary_sensor.living_room_motion
          state: "on"
    sub_buttons_background:
      0:  # Sub-Button 1
        type: solid
        color: red
        opacity: 0.5
        condition:
          condition: state
          entity: light.living_room
          state: "on"
      1:  # Sub-Button 2
        type: two-color
        color1: blue
        color2: green
        opacity: 0.6
        condition:
          condition: state
          entity: fan.living_room
          state: "on"
    icon_effects:
      main_icon:
        effect: heartbeat
        color: yellow
        condition:
          condition: state
          entity: light.living_room
          state: "on"
      sub_button_icon:
        0:  # Sub-Button 1
          effect: spin-360
          condition:
            condition: state
            entity: binary_sensor.living_room_motion
            state: "on"
    main_icon_background:
      color: green
      opacity: 0.7
      condition:
        condition: state
        entity: light.living_room
        state: "on"
```

---

<details>

<summary><b>?? Get this Module</b></summary>

<br>

> To use this module, simply copy and paste the following configuration into your `/www/bubble/bubble-modules.yaml` file.

```yaml
badgy-condition-helper:
  name: "Badgy Condition Helper"
  version: "v2026.10.12-beta"
  creator: "HyperCriSiS"
  link: "https://github.com/Clooos/Bubble-Card/discussions/1333"
  description: |
    Advanced badge and effect helper module with conditional logic.

    Patched fork (v2026.06.19-mod) — tested against Home Assistant 2026.6.x:
    - Fixed: sub-button & icon effects now stop when their condition turns false
      (previously the animation kept running until a full page reload).
    - Improved: effects are applied idempotently, so animations are no longer
      restarted on every unrelated Home Assistant state change.
    - Improved: badges are updated in place instead of being recreated, which
      avoids restarting badge animations and reduces DOM churn.
    - Improved: conditions now use Bubble Card's native checkConditionsMet when
      available (adds support for time/template/sun/zone/...), with a safe
      fallback to the built-in evaluator.
    - Cleanup: removed the non-functional state_changed subscription and the
      custom disconnectedCallback override.

    Features:
    - Entity badges: Display entity states or attributes on sub-buttons
    - Icon badges: Show icon indicators on sub-buttons
    - Sub-button backgrounds: Change background colors based on conditions
    - Icon effects: Apply animations to main and sub-button icons
    - Badge effects: Apply animations to badges
    - Main icon background: Change the main icon background conditionally
    - Sub-button effects: Apply animations (including color for glow) to the entire sub-button container

    All features support Home Assistant-style conditions for state-based logic.
  code: |
    /* =============================
       CSS for the badge visuals
       ============================= */
    .bubble-sub-button-badge {
      position: absolute;
      min-width: calc(18px * var(--badge-scale, 1));
      height: calc(16px * var(--badge-scale, 1));
      border-radius: calc(8px * var(--badge-scale, 1));
      background-color: var(--badge-color, var(--primary-color));
      color: white;
      font-size: calc(11px * var(--badge-scale, 1));
      font-weight: bold;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 calc(4px * var(--badge-scale, 1));
      z-index: 1;
      box-sizing: border-box;
      box-shadow: 0 1px 2px rgba(0,0,0,0.2);
      /* Size is set on dimensions, never transform: animations own transform. */
      transform-origin: center;
      pointer-events: none;
    }
    .entity-badge { top: 0; right: 0; }
    .bubble-icon-container:has(> .bubble-sub-button-badge) { overflow: visible !important; }
    .badgy-card-glow { box-shadow: 0 0 var(--badgy-glow-size, 14px) var(--badgy-glow-color, var(--primary-color)) !important; }
    .badgy-card-glow.badgy-card-glow-pulse { animation: badgy-card-glow-pulse 2s ease-in-out infinite; }
    @keyframes badgy-card-glow-pulse { 0%,100% { filter: drop-shadow(0 0 1px var(--badgy-glow-color)); } 50% { filter: drop-shadow(0 0 8px var(--badgy-glow-color)); } }
    .icon-badge   { top: 0; left: 0;  }
    .without-background {
      background-color: transparent;
      box-shadow: none;
    }
    .badge-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: calc(13px * var(--badge-scale, 1));
      height: calc(13px * var(--badge-scale, 1));
      --mdc-icon-size: calc(13px * var(--badge-scale, 1));
    }

    .sub-button-direct-bg { /* tracking class for JS-controlled background */ }

    /* =============================
       Animations for effects
       ============================= */
    @keyframes pulse-scale {
      0%, 100% { transform: scale(1); }
      50%      { transform: scale(1.05); }
    }
    @keyframes gentle-rotate {
      0% { transform: rotate(0deg); }
      25% { transform: rotate(5deg); }
      75% { transform: rotate(-5deg); }
      100% { transform: rotate(0deg); }
    }
    @keyframes border-pulse {
      0%, 100% { box-shadow: 0 0 0 transparent; }
      50%      { box-shadow: 0 0 10px var(--effect-color, rgba(255,255,255,0.7)); }
    }
    @keyframes gentle-shake {
      0%, 100% { transform: translateX(0); }
      25%      { transform: translateX(-2px); }
      75%      { transform: translateX(2px); }
    }
    @keyframes float-up-down {
      0%, 100% { transform: translateY(0); }
      50%      { transform: translateY(-3px); }
    }
    @keyframes zoom {
      0%   { transform: scale(1); }
      50%  { transform: scale(1.15); }
      100% { transform: scale(1); }
    }
    @keyframes heartbeat {
      0%   { transform: scale(1); }
      25%  { transform: scale(1.07); }
      40%  { transform: scale(1); }
      60%  { transform: scale(1.07); }
      100% { transform: scale(1); }
    }
    @keyframes spin360 {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    @keyframes flip {
      0% { transform: rotateY(0deg); }
      50% { transform: rotateY(180deg); }
      100% { transform: rotateY(360deg); }
    }
    @keyframes vibrate {
      0%   { transform: translate(0,0); }
      20%  { transform: translate(-1px,0); }
      40%  { transform: translate(1px,0); }
      60%  { transform: translate(-1px,0); }
      80%  { transform: translate(1px,0); }
      100% { transform: translate(0,0); }
    }

    .effect-pulse       { animation: pulse-scale 2s infinite ease-in-out; }
    .effect-rotate      { animation: gentle-rotate 3s infinite ease-in-out; }
    .effect-glow        { animation: border-pulse 2s infinite ease-in-out; }
    .effect-shake       { animation: gentle-shake 0.8s infinite ease-in-out; }
    .effect-float       { animation: float-up-down 3s infinite ease-in-out; }
    .effect-zoom        { animation: zoom 1.5s infinite ease-in-out; }
    .effect-heartbeat   { animation: heartbeat 2s infinite ease-in-out; }
    .effect-spin-360    { animation: spin360 2s linear infinite; }
    .effect-flip        { animation: flip 2s linear infinite; }
    .effect-vibrate     { animation: vibrate 0.6s linear infinite; }

    .bubble-sub-button-icon.has-effect {
      position: relative;
      transform-origin: center;
      display: inline-flex;
    }
    .bubble-icon.has-effect {
      position: relative;
      transform-origin: center;
      display: inline-flex;
    }

    ${(() => {
      try {
        const DEBUG = false;

        // ---- Fallback condition evaluator (used only if the native
        //      checkConditionsMet helper is not available) ----
        function evaluateSingleCondition(condObj, hass) {
          if (!condObj || typeof condObj !== 'object') return false;
          if (!condObj.condition) return false;
          const t = condObj.condition;
          switch (t) {
            case 'state': {
              const eid = condObj.entity_id || condObj.entity;
              if (!eid || !hass.states[eid]) return false;
              let val;
              if (condObj.attribute) {
                val = hass.states[eid].attributes[condObj.attribute];
                if (val === undefined) return false;
              } else {
                val = hass.states[eid].state;
              }
              if (Array.isArray(condObj.state)) return condObj.state.includes(val);
              return val === condObj.state;
            }
            case 'numeric_state': {
              const eid = condObj.entity_id || condObj.entity;
              if (!eid || !hass.states[eid]) return false;
              let val;
              if (condObj.attribute) val = hass.states[eid].attributes[condObj.attribute];
              else val = hass.states[eid].state;
              const numVal = parseFloat(val);
              if (isNaN(numVal)) return false;
              let ok = true;
              if (condObj.above !== undefined) ok = ok && (numVal > parseFloat(condObj.above));
              if (condObj.below !== undefined) ok = ok && (numVal < parseFloat(condObj.below));
              return ok;
            }
            case 'and':
              if (!Array.isArray(condObj.conditions)) return false;
              return condObj.conditions.every(sc => evaluateSingleCondition(sc, hass));
            case 'or':
              if (!Array.isArray(condObj.conditions)) return false;
              return condObj.conditions.some(sc => evaluateSingleCondition(sc, hass));
            case 'not':
              if (Array.isArray(condObj.conditions) && condObj.conditions.length > 0) {
                return !evaluateSingleCondition(condObj.conditions[0], hass);
              }
              if (condObj.condition_obj) return !evaluateSingleCondition(condObj.condition_obj, hass);
              return false;
            default:
              return false;
          }
        }

        // Prefer Bubble Card's native checkConditionsMet (supports time,
        // template, sun, zone, etc.). Fall back to the local evaluator on
        // older Bubble Card versions or if the native call throws.
        function checkAllConditions(cProp, hass) {
          if (!cProp) return true;
          const arr = [].concat(cProp);
          if (typeof checkConditionsMet === 'function') {
            try { return checkConditionsMet(arr, hass); } catch (e) { /* fallback below */ }
          }
          return arr.every(x => evaluateSingleCondition(x, hass));
        }

        function processColor(color) {
          if (typeof color !== "string") return null;
          const value = color.trim();
          if (!value || value === "none") return null;
          if (value.startsWith("#") || value.startsWith("rgb") ||
              value.startsWith("hsl") || value.startsWith("var(")) return value;
          if (!/^[a-z][a-z0-9-]*$/i.test(value)) return null;
          // Bubble theme colors retain precedence; fall back to standard CSS
          // named colors (including black) if no matching --*-color exists.
          if (typeof CSS !== "undefined" && CSS.supports?.("color", value))
            return "var(--" + value + "-color, " + value + ")";
          return "var(--" + value + "-color)";
        }

        const ALL_EFFECT_CLASSES = [
          'effect-pulse','effect-rotate','effect-glow','effect-shake',
          'effect-float','effect-zoom','effect-heartbeat','effect-spin-360',
          'effect-flip','effect-vibrate'
        ];

        // Idempotent effect application: only mutates classes when the desired
        // state actually changes, so the CSS animation is NOT restarted on every
        // (global) Home Assistant state update.
        function setEffect(el, effect, color) {
          if (!el) return;
          const desired = effect && effect !== "none" ? `effect-${effect}` : null;
          for (const c of ALL_EFFECT_CLASSES) {
            if (c !== desired && el.classList.contains(c)) el.classList.remove(c);
          }
          if (desired) {
            if (!el.classList.contains(desired)) el.classList.add(desired);
            if (!el.classList.contains('has-effect')) el.classList.add('has-effect');
            const cProc = color ? processColor(color) : null;
            if (cProc) el.style.setProperty('--effect-color', cProc);
            else el.style.removeProperty('--effect-color');
          } else {
            if (el.classList.contains('has-effect')) el.classList.remove('has-effect');
            el.style.removeProperty('--effect-color');
          }
        }

        const config = this.config["badgy-condition-helper"] || {};
        const cardEl = card;

        // ---- createBadge: reuses an existing badge element instead of
        //      destroying/recreating it, so badge effect animations don't
        //      restart on every state update. ----
        function createBadge({subButtonNumber, content, icon, badgeColor, textColor, hPos, vPos, scale, showBackground, badgeType}) {
          const sb = subButtonNumber === 0
            ? cardEl.querySelector(".bubble-icon-container")
            : cardEl.querySelector(`.bubble-sub-button-${subButtonNumber}`);
          if (!sb) return;
          if (getComputedStyle(sb).position === 'static') sb.style.position = 'relative';

          let badge = sb.querySelector(`.${badgeType}`);
          if (!badge) {
            badge = document.createElement('div');
            badge.className = `bubble-sub-button-badge ${badgeType}`;
            sb.appendChild(badge);
          }
          badge.classList.toggle('without-background', !showBackground);

          if (scale !== undefined && scale !== 1) badge.style.setProperty('--badge-scale', scale);
          else badge.style.removeProperty('--badge-scale');

          badge.style.top = `${vPos}px`;
          if (badgeType === 'entity-badge') { badge.style.right = `${hPos}px`; badge.style.left = ''; }
          else { badge.style.left = `${hPos}px`; badge.style.right = ''; }
          badge.dataset.hPos = hPos;
          badge.dataset.vPos = vPos;

          badgeColor = badgeColor ?? config.global_defaults?.badge_color;
          if (badgeColor) badge.style.setProperty('--badge-color', processColor(badgeColor));
          else badge.style.removeProperty('--badge-color');
          textColor = textColor ?? config.global_defaults?.badge_text_color;
          if (textColor) badge.style.color = processColor(textColor);
          else badge.style.removeProperty('color');

          if (icon) {
            let ic = badge.querySelector('ha-icon.badge-icon');
            if (!ic) {
              badge.textContent = '';
              ic = document.createElement('ha-icon');
              ic.className = 'badge-icon';
              badge.appendChild(ic);
            }
            if (ic.getAttribute('icon') !== icon) ic.setAttribute('icon', icon);
          } else if (content !== undefined && content !== null) {
            const ic = badge.querySelector('ha-icon.badge-icon');
            if (ic) ic.remove();
            const str = String(content);
            if (badge.textContent !== str) badge.textContent = str;
          }
        }

        function formatBadgeState(stObj, bc) {
          if (bc.display_text !== undefined && bc.display_text !== "") return bc.display_text;
          const value = stObj.state;
          const translate = bc.translated_state === true ||
            (bc.translated_state !== false && stObj.entity_id?.startsWith("binary_sensor."));
          if (translate && typeof hass.formatEntityState === "function") {
            try { return hass.formatEntityState(stObj); } catch (err) { /* raw fallback */ }
          }
          return value;
        }

        function chooseRule(cfg) {
          if (!cfg) return null;
          if (Array.isArray(cfg.rules) && cfg.rules.length) {
            const selected = cfg.rules.find(rule => rule && checkAllConditions(rule.condition, hass));
            if (selected) return { ...cfg, ...selected, rules: null };
            return null;
          }
          return checkAllConditions(cfg.condition, hass) ? cfg : null;
        }

        function resolvedColor(cfg, name = "color") {
          const raw = cfg?.[name];
          const template = cfg?.[name + "_template"];
          if (typeof template === "string" && template.trim() &&
              typeof renderTemplate === "function") {
            try {
              const evaluated = renderTemplate(template);
              if (typeof evaluated === "string") {
                const color = evaluated.trim();
                if (typeof CSS !== "undefined" && CSS.supports?.("color", color)) return color;
              }
            } catch (err) { /* optional template fallback */ }
          }
          const entity = cfg?.[name + "_entity"];
          const attribute = cfg?.[name + "_attribute"];
          const st = entity && hass.states?.[entity];
          const dynamic = st ? (attribute ? st.attributes?.[attribute] : st.state) : null;
          if (dynamic !== undefined && dynamic !== null && dynamic !== "") {
            const value = String(dynamic).trim();
            // Color attributes can contain hex, hsl/rgb functions or CSS variables.
            // Only accept valid colors; ignore malformed device values.
            if (typeof CSS !== "undefined" && CSS.supports?.("color", value)) return value;
          }
          return processColor(raw);
        }

        function processEntityBadges() {
          const eBadges = config.entity_badges || {};
          const current = new Set();
          for (const [k, bc] of Object.entries(eBadges)) {
            if (!/^\d+$/.test(k) || !bc?.entity) continue;
            const sbNum = parseInt(k) + 1;
            if (!hass.states[bc.entity]) continue;
            const conditionMet = checkAllConditions(bc.condition, hass);
            const showBadge = conditionMet && !(bc.show_if_off === false && hass.states[bc.entity].state === 'off');
            if (showBadge) {
              current.add(sbNum);
              let dispVal;
              const stObj = hass.states[bc.entity];
              if (bc.attribute && stObj.attributes[bc.attribute] !== undefined) dispVal = stObj.attributes[bc.attribute];
              else dispVal = formatBadgeState(stObj, bc);
              if (bc.decimals !== undefined && !isNaN(parseFloat(dispVal))) dispVal = parseFloat(dispVal).toFixed(parseInt(bc.decimals));
              if (bc.show_unit !== false && stObj.attributes.unit_of_measurement) dispVal += stObj.attributes.unit_of_measurement;
              createBadge({
                subButtonNumber: sbNum, content: dispVal, badgeColor: bc.color, textColor: bc.text_color,
                hPos: bc.h_pos ?? config.global_defaults?.badge_h_pos ?? -8, vPos: bc.v_pos ?? config.global_defaults?.badge_v_pos ?? -8, scale: bc.scale ?? config.global_defaults?.badge_scale ?? 1,
                showBackground: bc.show_background !== false, badgeType: 'entity-badge'
              });
            }
          }
          for (let i = 1; i <= 10; i++) {
            if (!current.has(i)) {
              const sb = cardEl.querySelector(`.bubble-sub-button-${i}`);
              if (sb) { const b = sb.querySelector('.entity-badge'); if (b) sb.removeChild(b); }
            }
          }
        }

        function processIconBadges() {
          const iBadges = config.icon_badges || {};
          const current = new Set();
          for (const [k, bc] of Object.entries(iBadges)) {
            if (!/^\d+$/.test(k) || !bc?.icon) continue;
            const sbNum = parseInt(k) + 1;
            if (checkAllConditions(bc.condition, hass)) {
              current.add(sbNum);
              createBadge({
                subButtonNumber: sbNum, icon: bc.icon, badgeColor: bc.color, textColor: bc.text_color,
                hPos: bc.h_pos ?? config.global_defaults?.badge_h_pos ?? -8, vPos: bc.v_pos ?? config.global_defaults?.badge_v_pos ?? -8, scale: bc.scale ?? config.global_defaults?.badge_scale ?? 1,
                showBackground: bc.show_background !== false, badgeType: 'icon-badge'
              });
            }
          }
          for (let i = 1; i <= 10; i++) {
            if (!current.has(i)) {
              const sb = cardEl.querySelector(`.bubble-sub-button-${i}`);
              if (sb) { const b = sb.querySelector('.icon-badge'); if (b) sb.removeChild(b); }
            }
          }
        }

        function processSubButtonBackgrounds() {
          const perButton = config.sub_buttons_background || {};
          for (let i = 1; i <= 10; i++) {
            const sb = cardEl.querySelector(".bubble-sub-button-" + i);
            if (!sb) continue;
            const entry = perButton[String(i - 1)] || config.global_defaults?.sub_button_background;
            const bg = chooseRule(entry);
            let background = null;
            if (bg) {
              const type = bg.type ?? "solid";
              if (type === "solid") {
                background = resolvedColor(bg, "color");
              } else if (type === "two-color") {
                const a = resolvedColor(bg, "color1") || "#ff0000";
                const b = resolvedColor(bg, "color2") || "#0000ff";
                background = "linear-gradient(135deg, " + a + " 0%, " + b + " 100%)";
              } else if (type === "three-color") {
                const a = resolvedColor(bg, "color1") || "#ff0000";
                const b = resolvedColor(bg, "color2") || "#00ff00";
                const c = resolvedColor(bg, "color3") || "#0000ff";
                background = "linear-gradient(135deg, " + a + " 0%, " + b + " 50%, " + c + " 100%)";
              }
            }
            // Only touch properties that Badgy owns. Other modules must keep theirs.
            if (background) {
              if (sb.style.getPropertyValue("background") !== background)
                sb.style.setProperty("background", background, "important");
              const opacity = String(bg.opacity ?? 1);
              if (sb.style.getPropertyValue("opacity") !== opacity)
                sb.style.setProperty("opacity", opacity, "important");
              sb.classList.add("sub-button-direct-bg");
            } else if (sb.classList.contains("sub-button-direct-bg")) {
              sb.classList.remove("sub-button-direct-bg");
              sb.style.removeProperty("background");
              sb.style.removeProperty("opacity");
            }
          }
        }

        function processIconEffects() {
          const iE = config.icon_effects || {};
          const mCfg = iE.main_icon || {};
          const mainIconEl = cardEl.querySelector('.bubble-icon');
          if (mainIconEl) {
            const met = checkAllConditions(mCfg.condition, hass);
            setEffect(mainIconEl, (met && mCfg.effect) ? mCfg.effect : null, mCfg.color);
          }
          for (let i = 0; i < 10; i++) {
            const el = cardEl.querySelector(`.bubble-sub-button-${i+1} .bubble-sub-button-icon`);
            if (!el) continue;
            const eC = iE.sub_button_icon && iE.sub_button_icon[i.toString()];
            const met = eC && eC.effect && checkAllConditions(eC.condition, hass);
            setEffect(el, met ? eC.effect : null, eC && eC.color);
          }
        }

        function processSubButtonEffects() {
          const sBE = config.sub_button_effects || {};
          for (let i = 0; i < 10; i++) {
            const sb = cardEl.querySelector(`.bubble-sub-button-${i+1}`);
            if (!sb) continue;
            const eff = sBE[i.toString()] || (config.global_defaults?.sub_button_effect ? { effect: config.global_defaults.sub_button_effect, color: config.global_defaults.sub_button_effect_color } : null);
            const met = eff && eff.effect && checkAllConditions(eff.condition, hass);
            setEffect(sb, met ? eff.effect : null, eff && eff.color);
          }
        }

        function processEntityBadgeEffects() {
          const eBE = config.entity_badge_effects || {};
          const matched = new Set();
          for (const [k, ef] of Object.entries(eBE)) {
            if (!/^\d+$/.test(k) || !ef?.effect) continue;
            const sbN = parseInt(k) + 1;
            const badge = cardEl.querySelector(`.bubble-sub-button-${sbN} .entity-badge`);
            if (!badge) continue;
            const met = checkAllConditions(ef.condition, hass);
            setEffect(badge, met ? ef.effect : null, ef.color);
            if (met) matched.add(badge);
          }
          cardEl.querySelectorAll('.bubble-sub-button-badge.entity-badge').forEach(b => {
            if (b.closest('.bubble-icon-container')) return;
            if (!matched.has(b)) setEffect(b, null, null);
          });
        }

        function processIconBadgeEffects() {
          const iBE = config.icon_badge_effects || {};
          const matched = new Set();
          for (const [k, ef] of Object.entries(iBE)) {
            if (!/^\d+$/.test(k) || !ef?.effect) continue;
            const sbN = parseInt(k) + 1;
            const badge = cardEl.querySelector(`.bubble-sub-button-${sbN} .icon-badge`);
            if (!badge) continue;
            const met = checkAllConditions(ef.condition, hass);
            setEffect(badge, met ? ef.effect : null, ef.color);
            if (met) matched.add(badge);
          }
          cardEl.querySelectorAll('.bubble-sub-button-badge.icon-badge').forEach(b => {
            if (b.closest('.bubble-icon-container')) return;
            if (!matched.has(b)) setEffect(b, null, null);
          });
        }

        function processMainIconBackground() {
          const mBg = chooseRule(config.main_icon_background);
          const mainCont = cardEl.querySelector(".bubble-icon-container");
          if (!mainCont) return;
          const color = mBg ? resolvedColor(mBg) : null;
          if (color) {
            if (mainCont.style.getPropertyValue("background") !== color)
              mainCont.style.setProperty("background", color, "important");
            const opacity = String(mBg.opacity ?? 1);
            if (mainCont.style.getPropertyValue("opacity") !== opacity)
              mainCont.style.setProperty("opacity", opacity, "important");
            mainCont.dataset.badgyBackgroundManaged = "1";
          } else if (mainCont.dataset.badgyBackgroundManaged) {
            mainCont.style.removeProperty("background");
            mainCont.style.removeProperty("opacity");
            delete mainCont.dataset.badgyBackgroundManaged;
          }
        }

        function processMainBadges() {
          const parent = cardEl.querySelector(".bubble-icon-container");
          if (!parent) return;
          for (const type of ["entity", "icon"]) {
            const isEntity = type === "entity";
            const category = isEntity ? "entity_badges" : "icon_badges";
            const cfg = config[category]?.main;
            const cls = type + "-badge";
            const state = isEntity && cfg?.entity ? hass.states?.[cfg.entity] : null;
            const visible = Boolean(cfg && (isEntity ? state : cfg.icon) &&
              checkAllConditions(cfg.condition, hass) &&
              (!isEntity || cfg.show_if_off !== false || state.state !== "off"));
            if (!visible) {
              const old = parent.querySelector("." + cls);
              if (old) old.remove();
              continue;
            }
            let content;
            if (isEntity) {
              if (cfg.attribute && state.attributes?.[cfg.attribute] !== undefined)
                content = state.attributes[cfg.attribute];
              else content = formatBadgeState(state, cfg);
              if (cfg.decimals !== undefined && content !== "" && !isNaN(Number(content)))
                content = Number(content).toFixed(Number(cfg.decimals));
              if (cfg.show_unit !== false && state.attributes?.unit_of_measurement)
                content = String(content) + state.attributes.unit_of_measurement;
            }
            createBadge({
              subButtonNumber: 0, badgeType: cls, content,
              icon: !isEntity ? cfg.icon : undefined,
              badgeColor: cfg.color, textColor: cfg.text_color,
              scale: cfg.scale ?? config.global_defaults?.badge_scale ?? 1,
              hPos: cfg.h_pos ?? config.global_defaults?.badge_h_pos ?? -8,
              vPos: cfg.v_pos ?? config.global_defaults?.badge_v_pos ?? -8,
              showBackground: cfg.show_background !== false,
            });
            const effect = config[isEntity ? "entity_badge_effects" : "icon_badge_effects"]?.main;
            const matched = effect?.effect && checkAllConditions(effect.condition, hass);
            setEffect(parent.querySelector("." + cls), matched ? effect.effect : null, effect?.color);
          }
        }

        function updateManagedIcon(el, requested) {
          if (!el) return;
          if (requested) {
            if (!Object.prototype.hasOwnProperty.call(el.dataset, "badgyOriginalIcon")) {
              el.dataset.badgyOriginalIcon = el.getAttribute("icon") || "";
            }
            if (el.getAttribute("icon") !== requested) el.setAttribute("icon", requested);
          } else if (Object.prototype.hasOwnProperty.call(el.dataset, "badgyOriginalIcon")) {
            const original = el.dataset.badgyOriginalIcon;
            if (original) el.setAttribute("icon", original);
            else el.removeAttribute("icon");
            delete el.dataset.badgyOriginalIcon;
          }
        }

        function updateManagedColor(el, chosen) {
          if (!el) return;
          const value = chosen ? resolvedColor(chosen) : null;
          if (value) {
            if (!Object.prototype.hasOwnProperty.call(el.dataset, "badgyOriginalColor")) {
              el.dataset.badgyOriginalColor = el.style.getPropertyValue("color");
              el.dataset.badgyOriginalColorPriority = el.style.getPropertyPriority("color");
            }
            if (el.style.getPropertyValue("color") !== value)
              el.style.setProperty("color", value, "important");
          } else if (Object.prototype.hasOwnProperty.call(el.dataset, "badgyOriginalColor")) {
            const original = el.dataset.badgyOriginalColor;
            if (original) el.style.setProperty("color", original, el.dataset.badgyOriginalColorPriority || "");
            else el.style.removeProperty("color");
            delete el.dataset.badgyOriginalColor;
            delete el.dataset.badgyOriginalColorPriority;
          }
        }

        function processIconsAndColors() {
          const colorCfg = config.icon_colors || {};
          const iconCfg = config.icons || {};
          const apply = (el, colorOptions, iconOptions, useDefault) => {
            const chosenColor = chooseRule(colorOptions);
            updateManagedColor(el, chosenColor ||
              (useDefault && config.global_defaults?.icon_color ? {color: config.global_defaults.icon_color} : null));
            const chosenIcon = chooseRule(iconOptions);
            updateManagedIcon(el, chosenIcon?.icon || null);
          };
          apply(cardEl.querySelector(".bubble-icon"),
            colorCfg.main_icon, iconCfg.main_icon, false);
          for (let i = 1; i <= 10; i++) {
            const el = cardEl.querySelector(".bubble-sub-button-" + i + " .bubble-sub-button-icon");
            apply(el, colorCfg.sub_button_icon?.[String(i - 1)],
              iconCfg.sub_button_icon?.[String(i - 1)], true);
          }
        }

        function processCardGlow() {
          const effect = chooseRule(config.card_effects);
          const target = cardEl.querySelector("ha-card") ||
            cardEl.querySelector(".bubble-button-card-container") || cardEl;
          const active = effect?.effect === "glow";
          target.classList.toggle("badgy-card-glow", active);
          target.classList.toggle("badgy-card-glow-pulse", active && effect.animate === true);
          if (active) {
            const color = resolvedColor(effect) || "var(--primary-color)";
            target.style.setProperty("--badgy-glow-color", color);
            target.style.setProperty("--badgy-glow-size", String(effect.intensity ?? 14) + "px");
          } else {
            target.style.removeProperty("--badgy-glow-color");
            target.style.removeProperty("--badgy-glow-size");
          }
        }

        // The module code is re-evaluated by Bubble Card on every hass update,
        // so a single pass here is enough to keep everything in sync. No manual
        // state_changed subscription is needed (and the previous one relied on a
        // non-functional hass.connection.addEventListener('state_changed')).
        processEntityBadges();
        processIconBadges();
        processSubButtonBackgrounds();
        processIconEffects();
        processSubButtonEffects();
        processEntityBadgeEffects();
        processIconBadgeEffects();
        processMainIconBackground();
        processIconsAndColors();
        processMainBadges();
        processCardGlow();

      } catch (err) {
        console.error("Error in badgy-condition-helper module:", err);
      }
      return '';
    })()}
  editor:
    - type: expandable
      title: "Icon Colors"
      icon: "mdi:palette"
      name: icon_colors
      schema:
        - type: expandable
          title: "Main Icon"
          name: main_icon
          schema:
            - name: color
              label: "Icon color"
              selector:
                ui_color:
                  include_none: true
            - name: condition
              label: "Condition"
              selector:
                condition: {}
            - name: rules
              label: "Conditional colors"
              selector:
                object:
                  multiple: true
                  label_field: label
                  fields:
                    label:
                      label: Rule name
                      selector:
                        text: {}
                    condition:
                      label: Condition
                      selector:
                        condition: {}
                    color:
                      label: "Icon color"
                      selector:
                        ui_color: {}
        - type: expandable
          title: "Sub-Buttons Icon"
          name: sub_button_icon
          schema:
            - type: expandable
              title: "Sub-Button 1"
              name: "0"
              schema:
                - name: color
                  label: "Icon color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional colors (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        color:
                          label: "Icon color"
                          selector:
                            ui_color: {}
            - type: expandable
              title: "Sub-Button 2"
              name: "1"
              schema:
                - name: color
                  label: "Icon color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional colors (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        color:
                          label: "Icon color"
                          selector:
                            ui_color: {}
            - type: expandable
              title: "Sub-Button 3"
              name: "2"
              schema:
                - name: color
                  label: "Icon color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional colors (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        color:
                          label: "Icon color"
                          selector:
                            ui_color: {}
            - type: expandable
              title: "Sub-Button 4"
              name: "3"
              schema:
                - name: color
                  label: "Icon color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional colors (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        color:
                          label: "Icon color"
                          selector:
                            ui_color: {}
            - type: expandable
              title: "Sub-Button 5"
              name: "4"
              schema:
                - name: color
                  label: "Icon color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional colors (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        color:
                          label: "Icon color"
                          selector:
                            ui_color: {}
            - type: expandable
              title: "Sub-Button 6"
              name: "5"
              schema:
                - name: color
                  label: "Icon color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional colors (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        color:
                          label: "Icon color"
                          selector:
                            ui_color: {}
    - type: expandable
      title: "Backgrounds"
      icon: "mdi:format-color-fill"
      schema:
        - type: expandable
          title: "Main Icon Background"
          icon: "mdi:format-color-fill"
          name: main_icon_background
          schema:
            - name: color_template
              label: "Color template (e.g. Jinja {{ state_attr(...) }})"
              selector:
                text: {}
            - name: color_entity
              label: "Color entity (dynamic)"
              selector:
                entity: {}
            - name: color_attribute
              label: "Entity attribute containing the color"
              selector:
                text: {}
            - name: rules
              label: "Conditional color/background rules — first match wins"
              selector:
                object:
                  multiple: true
                  label_field: label
                  fields:
                    label:
                      label: Rule name
                      selector:
                        text: {}
                    condition:
                      label: Condition
                      selector:
                        condition: {}
                    type:
                      label: "Background type"
                      selector:
                        select:
                          options:
                            - label: Solid
                              value: solid
                            - label: Two-color gradient
                              value: two-color
                            - label: Three-color gradient
                              value: three-color
                    color:
                      label: "Color"
                      selector:
                        ui_color: {}
                    color1:
                      label: "Gradient Color 1"
                      selector:
                        ui_color: {}
                    color2:
                      label: "Gradient Color 2"
                      selector:
                        ui_color: {}
                    color3:
                      label: "Gradient Color 3"
                      selector:
                        ui_color: {}
                    opacity:
                      label: "Opacity"
                      selector:
                        number:
                          min: 0
                          max: 1
                          step: 0.05
            - name: color
              label: "Background Color"
              selector:
                ui_color: {}
            - name: opacity
              label: "Opacity"
              default: 1.0
              selector:
                number:
                  min: 0
                  max: 1
                  step: 0.05
                  mode: slider
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
    
        # Sub-Buttons Background
        - type: expandable
          title: "Sub-Buttons Background"
          icon: "mdi:format-color-fill"
          name: sub_buttons_background
          schema:
            - type: expandable
              title: "Sub-Button 1"
              name: "0"
              schema:
                - name: type
                  label: "Background Type"
                  selector:
                    select:
                      options:
                        - label: "Solid"
                          value: "solid"
                        - label: "Two-Color Gradient"
                          value: "two-color"
                        - label: "Three-Color Gradient"
                          value: "three-color"
                - name: color_template
                  label: "Color template (e.g. Jinja {{ state_attr(...) }})"
                  selector:
                    text: {}
                - name: color_entity
                  label: "Color entity (dynamic)"
                  selector:
                    entity: {}
                - name: color_attribute
                  label: "Entity attribute containing the color"
                  selector:
                    text: {}
                - name: rules
                  label: "Conditional color/background rules — first match wins"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        type:
                          label: "Background type"
                          selector:
                            select:
                              options:
                                - label: Solid
                                  value: solid
                                - label: Two-color gradient
                                  value: two-color
                                - label: Three-color gradient
                                  value: three-color
                        color:
                          label: "Color"
                          selector:
                            ui_color: {}
                        color1:
                          label: "Gradient Color 1"
                          selector:
                            ui_color: {}
                        color2:
                          label: "Gradient Color 2"
                          selector:
                            ui_color: {}
                        color3:
                          label: "Gradient Color 3"
                          selector:
                            ui_color: {}
                        opacity:
                          label: "Opacity"
                          selector:
                            number:
                              min: 0
                              max: 1
                              step: 0.05
                - name: color
                  label: "Solid Color"
                  selector:
                    ui_color:
                      include_none: true
                - name: color1
                  label: "Gradient Color 1"
                  selector:
                    ui_color: {}
                - name: color2
                  label: "Gradient Color 2"
                  selector:
                    ui_color: {}
                - name: color3
                  label: "Gradient Color 3"
                  selector:
                    ui_color: {}
                - name: opacity
                  label: "Background Opacity"
                  default: 1.0
                  selector:
                    number:
                      min: 0
                      max: 1
                      step: 0.05
                      mode: slider
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 2"
              name: "1"
              schema:
                - name: type
                  label: "Background Type"
                  selector:
                    select:
                      options:
                        - label: "Solid"
                          value: "solid"
                        - label: "Two-Color Gradient"
                          value: "two-color"
                        - label: "Three-Color Gradient"
                          value: "three-color"
                - name: color_template
                  label: "Color template (e.g. Jinja {{ state_attr(...) }})"
                  selector:
                    text: {}
                - name: color_entity
                  label: "Color entity (dynamic)"
                  selector:
                    entity: {}
                - name: color_attribute
                  label: "Entity attribute containing the color"
                  selector:
                    text: {}
                - name: rules
                  label: "Conditional color/background rules — first match wins"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        type:
                          label: "Background type"
                          selector:
                            select:
                              options:
                                - label: Solid
                                  value: solid
                                - label: Two-color gradient
                                  value: two-color
                                - label: Three-color gradient
                                  value: three-color
                        color:
                          label: "Color"
                          selector:
                            ui_color: {}
                        color1:
                          label: "Gradient Color 1"
                          selector:
                            ui_color: {}
                        color2:
                          label: "Gradient Color 2"
                          selector:
                            ui_color: {}
                        color3:
                          label: "Gradient Color 3"
                          selector:
                            ui_color: {}
                        opacity:
                          label: "Opacity"
                          selector:
                            number:
                              min: 0
                              max: 1
                              step: 0.05
                - name: color
                  label: "Solid Color"
                  selector:
                    ui_color:
                      include_none: true
                - name: color1
                  label: "Gradient Color 1"
                  selector:
                    ui_color: {}
                - name: color2
                  label: "Gradient Color 2"
                  selector:
                    ui_color: {}
                - name: color3
                  label: "Gradient Color 3"
                  selector:
                    ui_color: {}
                - name: opacity
                  label: "Background Opacity"
                  default: 1.0
                  selector:
                    number:
                      min: 0
                      max: 1
                      step: 0.05
                      mode: slider
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 3"
              name: "2"
              schema:
                - name: type
                  label: "Background Type"
                  selector:
                    select:
                      options:
                        - label: "Solid"
                          value: "solid"
                        - label: "Two-Color Gradient"
                          value: "two-color"
                        - label: "Three-Color Gradient"
                          value: "three-color"
                - name: color_template
                  label: "Color template (e.g. Jinja {{ state_attr(...) }})"
                  selector:
                    text: {}
                - name: color_entity
                  label: "Color entity (dynamic)"
                  selector:
                    entity: {}
                - name: color_attribute
                  label: "Entity attribute containing the color"
                  selector:
                    text: {}
                - name: rules
                  label: "Conditional color/background rules — first match wins"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        type:
                          label: "Background type"
                          selector:
                            select:
                              options:
                                - label: Solid
                                  value: solid
                                - label: Two-color gradient
                                  value: two-color
                                - label: Three-color gradient
                                  value: three-color
                        color:
                          label: "Color"
                          selector:
                            ui_color: {}
                        color1:
                          label: "Gradient Color 1"
                          selector:
                            ui_color: {}
                        color2:
                          label: "Gradient Color 2"
                          selector:
                            ui_color: {}
                        color3:
                          label: "Gradient Color 3"
                          selector:
                            ui_color: {}
                        opacity:
                          label: "Opacity"
                          selector:
                            number:
                              min: 0
                              max: 1
                              step: 0.05
                - name: color
                  label: "Solid Color"
                  selector:
                    ui_color:
                      include_none: true
                - name: color1
                  label: "Gradient Color 1"
                  selector:
                    ui_color: {}
                - name: color2
                  label: "Gradient Color 2"
                  selector:
                    ui_color: {}
                - name: color3
                  label: "Gradient Color 3"
                  selector:
                    ui_color: {}
                - name: opacity
                  label: "Background Opacity"
                  default: 1.0
                  selector:
                    number:
                      min: 0
                      max: 1
                      step: 0.05
                      mode: slider
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 4"
              name: "3"
              schema:
                - name: type
                  label: "Background Type"
                  selector:
                    select:
                      options:
                        - label: "Solid"
                          value: "solid"
                        - label: "Two-Color Gradient"
                          value: "two-color"
                        - label: "Three-Color Gradient"
                          value: "three-color"
                - name: color_template
                  label: "Color template (e.g. Jinja {{ state_attr(...) }})"
                  selector:
                    text: {}
                - name: color_entity
                  label: "Color entity (dynamic)"
                  selector:
                    entity: {}
                - name: color_attribute
                  label: "Entity attribute containing the color"
                  selector:
                    text: {}
                - name: rules
                  label: "Conditional color/background rules — first match wins"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        type:
                          label: "Background type"
                          selector:
                            select:
                              options:
                                - label: Solid
                                  value: solid
                                - label: Two-color gradient
                                  value: two-color
                                - label: Three-color gradient
                                  value: three-color
                        color:
                          label: "Color"
                          selector:
                            ui_color: {}
                        color1:
                          label: "Gradient Color 1"
                          selector:
                            ui_color: {}
                        color2:
                          label: "Gradient Color 2"
                          selector:
                            ui_color: {}
                        color3:
                          label: "Gradient Color 3"
                          selector:
                            ui_color: {}
                        opacity:
                          label: "Opacity"
                          selector:
                            number:
                              min: 0
                              max: 1
                              step: 0.05
                - name: color
                  label: "Solid Color"
                  selector:
                    ui_color:
                      include_none: true
                - name: color1
                  label: "Gradient Color 1"
                  selector:
                    ui_color: {}
                - name: color2
                  label: "Gradient Color 2"
                  selector:
                    ui_color: {}
                - name: color3
                  label: "Gradient Color 3"
                  selector:
                    ui_color: {}
                - name: opacity
                  label: "Background Opacity"
                  default: 1.0
                  selector:
                    number:
                      min: 0
                      max: 1
                      step: 0.05
                      mode: slider
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 5"
              name: "4"
              schema:
                - name: type
                  label: "Background Type"
                  selector:
                    select:
                      options:
                        - label: "Solid"
                          value: "solid"
                        - label: "Two-Color Gradient"
                          value: "two-color"
                        - label: "Three-Color Gradient"
                          value: "three-color"
                - name: color_template
                  label: "Color template (e.g. Jinja {{ state_attr(...) }})"
                  selector:
                    text: {}
                - name: color_entity
                  label: "Color entity (dynamic)"
                  selector:
                    entity: {}
                - name: color_attribute
                  label: "Entity attribute containing the color"
                  selector:
                    text: {}
                - name: rules
                  label: "Conditional color/background rules — first match wins"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        type:
                          label: "Background type"
                          selector:
                            select:
                              options:
                                - label: Solid
                                  value: solid
                                - label: Two-color gradient
                                  value: two-color
                                - label: Three-color gradient
                                  value: three-color
                        color:
                          label: "Color"
                          selector:
                            ui_color: {}
                        color1:
                          label: "Gradient Color 1"
                          selector:
                            ui_color: {}
                        color2:
                          label: "Gradient Color 2"
                          selector:
                            ui_color: {}
                        color3:
                          label: "Gradient Color 3"
                          selector:
                            ui_color: {}
                        opacity:
                          label: "Opacity"
                          selector:
                            number:
                              min: 0
                              max: 1
                              step: 0.05
                - name: color
                  label: "Solid Color"
                  selector:
                    ui_color:
                      include_none: true
                - name: color1
                  label: "Gradient Color 1"
                  selector:
                    ui_color: {}
                - name: color2
                  label: "Gradient Color 2"
                  selector:
                    ui_color: {}
                - name: color3
                  label: "Gradient Color 3"
                  selector:
                    ui_color: {}
                - name: opacity
                  label: "Background Opacity"
                  default: 1.0
                  selector:
                    number:
                      min: 0
                      max: 1
                      step: 0.05
                      mode: slider
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 6"
              name: "5"
              schema:
                - name: type
                  label: "Background Type"
                  selector:
                    select:
                      options:
                        - label: "Solid"
                          value: "solid"
                        - label: "Two-Color Gradient"
                          value: "two-color"
                        - label: "Three-Color Gradient"
                          value: "three-color"
                - name: color_template
                  label: "Color template (e.g. Jinja {{ state_attr(...) }})"
                  selector:
                    text: {}
                - name: color_entity
                  label: "Color entity (dynamic)"
                  selector:
                    entity: {}
                - name: color_attribute
                  label: "Entity attribute containing the color"
                  selector:
                    text: {}
                - name: rules
                  label: "Conditional color/background rules — first match wins"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        type:
                          label: "Background type"
                          selector:
                            select:
                              options:
                                - label: Solid
                                  value: solid
                                - label: Two-color gradient
                                  value: two-color
                                - label: Three-color gradient
                                  value: three-color
                        color:
                          label: "Color"
                          selector:
                            ui_color: {}
                        color1:
                          label: "Gradient Color 1"
                          selector:
                            ui_color: {}
                        color2:
                          label: "Gradient Color 2"
                          selector:
                            ui_color: {}
                        color3:
                          label: "Gradient Color 3"
                          selector:
                            ui_color: {}
                        opacity:
                          label: "Opacity"
                          selector:
                            number:
                              min: 0
                              max: 1
                              step: 0.05
                - name: color
                  label: "Solid Color"
                  selector:
                    ui_color:
                      include_none: true
                - name: color1
                  label: "Gradient Color 1"
                  selector:
                    ui_color: {}
                - name: color2
                  label: "Gradient Color 2"
                  selector:
                    ui_color: {}
                - name: color3
                  label: "Gradient Color 3"
                  selector:
                    ui_color: {}
                - name: opacity
                  label: "Background Opacity"
                  default: 1.0
                  selector:
                    number:
                      min: 0
                      max: 1
                      step: 0.05
                      mode: slider
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
    
        # Entity Badge Effects
        - type: expandable
          title: "Card Glow"
          icon: "mdi:brightness-6"
          name: card_effects
          schema:
            - name: effect
              label: "Card effect"
              default: "none"
              selector:
                select:
                  options:
                    - label: None
                      value: none
                    - label: Glow
                      value: glow
            - name: color
              label: "Glow color"
              selector:
                ui_color:
                  include_none: true
            - name: intensity
              label: "Glow radius in pixels"
              default: 14
              selector:
                number:
                  min: 2
                  max: 40
                  step: 1
            - name: animate
              label: "Pulse glow"
              default: false
              selector:
                boolean: {}
            - name: condition
              label: "Condition"
              selector:
                condition: {}
    - type: expandable
      title: "Icons"
      icon: "mdi:shape"
      name: icons
      schema:
        - type: expandable
          title: "Main Icon"
          name: main_icon
          schema:
            - name: icon
              label: "Replacement icon"
              selector:
                icon: {}
            - name: condition
              label: "Condition"
              selector:
                condition: {}
            - name: rules
              label: "Conditional icons"
              selector:
                object:
                  multiple: true
                  label_field: label
                  fields:
                    label:
                      label: Rule name
                      selector:
                        text: {}
                    condition:
                      label: Condition
                      selector:
                        condition: {}
                    icon:
                      label: "Icon"
                      selector:
                        icon: {}
        - type: expandable
          title: "Sub-Buttons Icon"
          name: sub_button_icon
          schema:
            - type: expandable
              title: "Sub-Button 1"
              name: "0"
              schema:
                - name: icon
                  label: "Replacement icon"
                  selector:
                    icon: {}
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional icons (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        icon:
                          label: "Icon"
                          selector:
                            icon: {}
            - type: expandable
              title: "Sub-Button 2"
              name: "1"
              schema:
                - name: icon
                  label: "Replacement icon"
                  selector:
                    icon: {}
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional icons (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        icon:
                          label: "Icon"
                          selector:
                            icon: {}
            - type: expandable
              title: "Sub-Button 3"
              name: "2"
              schema:
                - name: icon
                  label: "Replacement icon"
                  selector:
                    icon: {}
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional icons (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        icon:
                          label: "Icon"
                          selector:
                            icon: {}
            - type: expandable
              title: "Sub-Button 4"
              name: "3"
              schema:
                - name: icon
                  label: "Replacement icon"
                  selector:
                    icon: {}
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional icons (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        icon:
                          label: "Icon"
                          selector:
                            icon: {}
            - type: expandable
              title: "Sub-Button 5"
              name: "4"
              schema:
                - name: icon
                  label: "Replacement icon"
                  selector:
                    icon: {}
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional icons (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        icon:
                          label: "Icon"
                          selector:
                            icon: {}
            - type: expandable
              title: "Sub-Button 6"
              name: "5"
              schema:
                - name: icon
                  label: "Replacement icon"
                  selector:
                    icon: {}
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
                - name: rules
                  label: "Conditional icons (first match wins)"
                  selector:
                    object:
                      multiple: true
                      label_field: label
                      fields:
                        label:
                          label: Rule name
                          selector:
                            text: {}
                        condition:
                          label: Condition
                          selector:
                            condition: {}
                        icon:
                          label: "Icon"
                          selector:
                            icon: {}
    - type: expandable
      title: "Entity Badges"
      icon: "mdi:tag-text"
      name: entity_badges
      schema:
        - type: expandable
          title: "Main Icon"
          name: main
          schema:
            - name: entity
              label: "Entity"
              selector:
                entity: {}
            - name: attribute
              label: "Attribute"
              selector:
                text: {}
            - name: display_text
              label: "Custom display text"
              selector:
                text: {}
            - name: translated_state
              label: "Translate the entity state (e.g. Open/Closed)"
              selector:
                boolean: {}
            - name: color
              label: "Badge color"
              selector:
                ui_color:
                  include_none: true
            - name: text_color
              label: "Text color"
              selector:
                ui_color:
                  include_none: true
            - name: show_background
              label: "Show background"
              default: true
              selector:
                boolean: {}
            - name: decimals
              label: "Decimal places"
              selector:
                number:
                  min: 0
                  max: 5
                  step: 1
            - name: show_unit
              label: "Show unit"
              default: true
              selector:
                boolean: {}
            - name: show_if_off
              label: "Show when off"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge size"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  step: 0.1
                  mode: slider
            - name: h_pos
              label: "Horizontal position"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  step: 1
                  mode: slider
            - name: v_pos
              label: "Vertical position"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  step: 1
                  mode: slider
            - name: condition
              label: "Condition"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 1"
          name: "0"
          schema:
            - name: entity
              label: "Entity"
              selector:
                entity: {}
            - name: attribute
              label: "Attribute (optional)"
              selector:
                attribute: {}
            - name: display_text
              label: "Custom display text"
              selector:
                text: {}
            - name: translated_state
              label: "Translate state (default for binary sensors)"
              selector:
                boolean: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: decimals
              label: "Decimal Places (for numbers)"
              selector:
                number:
                  min: 0
                  max: 5
                  mode: slider
                  step: 1
            - name: show_unit
              label: "Show Unit"
              default: true
              selector:
                boolean: {}
            - name: show_if_off
              label: "Show When 'off'"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 2"
          name: "1"
          schema:
            - name: entity
              label: "Entity"
              selector:
                entity: {}
            - name: attribute
              label: "Attribute (optional)"
              selector:
                attribute: {}
            - name: display_text
              label: "Custom display text"
              selector:
                text: {}
            - name: translated_state
              label: "Translate state (default for binary sensors)"
              selector:
                boolean: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: decimals
              label: "Decimal Places (for numbers)"
              selector:
                number:
                  min: 0
                  max: 5
                  mode: slider
                  step: 1
            - name: show_unit
              label: "Show Unit"
              default: true
              selector:
                boolean: {}
            - name: show_if_off
              label: "Show When 'off'"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 3"
          name: "2"
          schema:
            - name: entity
              label: "Entity"
              selector:
                entity: {}
            - name: attribute
              label: "Attribute (optional)"
              selector:
                attribute: {}
            - name: display_text
              label: "Custom display text"
              selector:
                text: {}
            - name: translated_state
              label: "Translate state (default for binary sensors)"
              selector:
                boolean: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: decimals
              label: "Decimal Places (for numbers)"
              selector:
                number:
                  min: 0
                  max: 5
                  mode: slider
                  step: 1
            - name: show_unit
              label: "Show Unit"
              default: true
              selector:
                boolean: {}
            - name: show_if_off
              label: "Show When 'off'"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 4"
          name: "3"
          schema:
            - name: entity
              label: "Entity"
              selector:
                entity: {}
            - name: attribute
              label: "Attribute (optional)"
              selector:
                attribute: {}
            - name: display_text
              label: "Custom display text"
              selector:
                text: {}
            - name: translated_state
              label: "Translate state (default for binary sensors)"
              selector:
                boolean: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: decimals
              label: "Decimal Places (for numbers)"
              selector:
                number:
                  min: 0
                  max: 5
                  mode: slider
                  step: 1
            - name: show_unit
              label: "Show Unit"
              default: true
              selector:
                boolean: {}
            - name: show_if_off
              label: "Show When 'off'"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 5"
          name: "4"
          schema:
            - name: entity
              label: "Entity"
              selector:
                entity: {}
            - name: attribute
              label: "Attribute (optional)"
              selector:
                attribute: {}
            - name: display_text
              label: "Custom display text"
              selector:
                text: {}
            - name: translated_state
              label: "Translate state (default for binary sensors)"
              selector:
                boolean: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: decimals
              label: "Decimal Places (for numbers)"
              selector:
                number:
                  min: 0
                  max: 5
                  mode: slider
                  step: 1
            - name: show_unit
              label: "Show Unit"
              default: true
              selector:
                boolean: {}
            - name: show_if_off
              label: "Show When 'off'"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 6"
          name: "5"
          schema:
            - name: entity
              label: "Entity"
              selector:
                entity: {}
            - name: attribute
              label: "Attribute (optional)"
              selector:
                attribute: {}
            - name: display_text
              label: "Custom display text"
              selector:
                text: {}
            - name: translated_state
              label: "Translate state (default for binary sensors)"
              selector:
                boolean: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: decimals
              label: "Decimal Places (for numbers)"
              selector:
                number:
                  min: 0
                  max: 5
                  mode: slider
                  step: 1
            - name: show_unit
              label: "Show Unit"
              default: true
              selector:
                boolean: {}
            - name: show_if_off
              label: "Show When 'off'"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}

    # Icon Badges
    - type: expandable
      title: "Icon Badges"
      icon: "mdi:tag-outline"
      name: icon_badges
      schema:
        - type: expandable
          title: "Main Icon"
          name: main
          schema:
            - name: icon
              label: "Icon"
              selector:
                icon: {}
            - name: color
              label: "Badge color"
              selector:
                ui_color:
                  include_none: true
            - name: text_color
              label: "Text color"
              selector:
                ui_color:
                  include_none: true
            - name: show_background
              label: "Show background"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge size"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  step: 0.1
                  mode: slider
            - name: h_pos
              label: "Horizontal position"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  step: 1
                  mode: slider
            - name: v_pos
              label: "Vertical position"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  step: 1
                  mode: slider
            - name: condition
              label: "Condition"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 1"
          name: "0"
          schema:
            - name: icon
              label: "Icon"
              selector:
                icon: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 2"
          name: "1"
          schema:
            - name: icon
              label: "Icon"
              selector:
                icon: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 3"
          name: "2"
          schema:
            - name: icon
              label: "Icon"
              selector:
                icon: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 4"
          name: "3"
          schema:
            - name: icon
              label: "Icon"
              selector:
                icon: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 5"
          name: "4"
          schema:
            - name: icon
              label: "Icon"
              selector:
                icon: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}
        - type: expandable
          title: "Sub-Button 6"
          name: "5"
          schema:
            - name: icon
              label: "Icon"
              selector:
                icon: {}
            - name: color
              label: "Badge Color"
              selector:
                ui_color: {}
            - name: text_color
              label: "Text Color"
              selector:
                ui_color: {}
            - name: show_background
              label: "Show Background"
              default: true
              selector:
                boolean: {}
            - name: scale
              label: "Badge Size (scale)"
              default: 1
              selector:
                number:
                  min: 0.5
                  max: 3
                  mode: slider
                  step: 0.1
            - name: h_pos
              label: "Horizontal Position (px)"
              default: -8
              selector:
                number:
                  min: -500
                  max: 500
                  mode: slider
                  step: 1
            - name: v_pos
              label: "Vertical Position (px)"
              default: -8
              selector:
                number:
                  min: -100
                  max: 100
                  mode: slider
                  step: 1
            - name: condition
              label: "Condition (optional)"
              selector:
                condition: {}

    # Main Icon Background
    - type: expandable
      title: "Effects"
      icon: "mdi:animation"
      schema:
        - type: expandable
          title: "Icon Effects"
          icon: "mdi:weather-windy-variant"
          name: icon_effects
          schema:
            - type: expandable
              title: "Main Icon"
              name: main_icon
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button Icon Effects"
              name: sub_button_icon
              schema:
                - type: expandable
                  title: "Sub-Button Icon 1"
                  name: "0"
                  schema:
                    - name: effect
                      label: "Effect Type"
                      selector:
                        select:
                          options:
                            - label: "Pulse (Scale)"
                              value: "pulse"
                            - label: "Gentle Rotation"
                              value: "rotate"
                            - label: "Glow Effect"
                              value: "glow"
                            - label: "Gentle Shake"
                              value: "shake"
                            - label: "Float Up & Down"
                              value: "float"
                            - label: "Zoom"
                              value: "zoom"
                            - label: "Heartbeat"
                              value: "heartbeat"
                            - label: "Spin 360"
                              value: "spin-360"
                            - label: "Flip"
                              value: "flip"
                            - label: "Vibrate"
                              value: "vibrate"
                    - name: color
                      label: "Effect Color"
                      selector:
                        ui_color: {}
                    - name: condition
                      label: "Condition (optional)"
                      selector:
                        condition: {}
                - type: expandable
                  title: "Sub-Button Icon 2"
                  name: "1"
                  schema:
                    - name: effect
                      label: "Effect Type"
                      selector:
                        select:
                          options:
                            - label: "Pulse (Scale)"
                              value: "pulse"
                            - label: "Gentle Rotation"
                              value: "rotate"
                            - label: "Glow Effect"
                              value: "glow"
                            - label: "Gentle Shake"
                              value: "shake"
                            - label: "Float Up & Down"
                              value: "float"
                            - label: "Zoom"
                              value: "zoom"
                            - label: "Heartbeat"
                              value: "heartbeat"
                            - label: "Spin 360"
                              value: "spin-360"
                            - label: "Flip"
                              value: "flip"
                            - label: "Vibrate"
                              value: "vibrate"
                    - name: color
                      label: "Effect Color"
                      selector:
                        ui_color: {}
                    - name: condition
                      label: "Condition (optional)"
                      selector:
                        condition: {}
                - type: expandable
                  title: "Sub-Button Icon 3"
                  name: "2"
                  schema:
                    - name: effect
                      label: "Effect Type"
                      selector:
                        select:
                          options:
                            - label: "Pulse (Scale)"
                              value: "pulse"
                            - label: "Gentle Rotation"
                              value: "rotate"
                            - label: "Glow Effect"
                              value: "glow"
                            - label: "Gentle Shake"
                              value: "shake"
                            - label: "Float Up & Down"
                              value: "float"
                            - label: "Zoom"
                              value: "zoom"
                            - label: "Heartbeat"
                              value: "heartbeat"
                            - label: "Spin 360"
                              value: "spin-360"
                            - label: "Flip"
                              value: "flip"
                            - label: "Vibrate"
                              value: "vibrate"
                    - name: color
                      label: "Effect Color"
                      selector:
                        ui_color: {}
                    - name: condition
                      label: "Condition (optional)"
                      selector:
                        condition: {}
                - type: expandable
                  title: "Sub-Button Icon 4"
                  name: "3"
                  schema:
                    - name: effect
                      label: "Effect Type"
                      selector:
                        select:
                          options:
                            - label: "Pulse (Scale)"
                              value: "pulse"
                            - label: "Gentle Rotation"
                              value: "rotate"
                            - label: "Glow Effect"
                              value: "glow"
                            - label: "Gentle Shake"
                              value: "shake"
                            - label: "Float Up & Down"
                              value: "float"
                            - label: "Zoom"
                              value: "zoom"
                            - label: "Heartbeat"
                              value: "heartbeat"
                            - label: "Spin 360"
                              value: "spin-360"
                            - label: "Flip"
                              value: "flip"
                            - label: "Vibrate"
                              value: "vibrate"
                    - name: color
                      label: "Effect Color"
                      selector:
                        ui_color: {}
                    - name: condition
                      label: "Condition (optional)"
                      selector:
                        condition: {}
                - type: expandable
                  title: "Sub-Button Icon 5"
                  name: "4"
                  schema:
                    - name: effect
                      label: "Effect Type"
                      selector:
                        select:
                          options:
                            - label: "Pulse (Scale)"
                              value: "pulse"
                            - label: "Gentle Rotation"
                              value: "rotate"
                            - label: "Glow Effect"
                              value: "glow"
                            - label: "Gentle Shake"
                              value: "shake"
                            - label: "Float Up & Down"
                              value: "float"
                            - label: "Zoom"
                              value: "zoom"
                            - label: "Heartbeat"
                              value: "heartbeat"
                            - label: "Spin 360"
                              value: "spin-360"
                            - label: "Flip"
                              value: "flip"
                            - label: "Vibrate"
                              value: "vibrate"
                    - name: color
                      label: "Effect Color"
                      selector:
                        ui_color: {}
                    - name: condition
                      label: "Condition (optional)"
                      selector:
                        condition: {}
                - type: expandable
                  title: "Sub-Button Icon 6"
                  name: "5"
                  schema:
                    - name: effect
                      label: "Effect Type"
                      selector:
                        select:
                          options:
                            - label: "Pulse (Scale)"
                              value: "pulse"
                            - label: "Gentle Rotation"
                              value: "rotate"
                            - label: "Glow Effect"
                              value: "glow"
                            - label: "Gentle Shake"
                              value: "shake"
                            - label: "Float Up & Down"
                              value: "float"
                            - label: "Zoom"
                              value: "zoom"
                            - label: "Heartbeat"
                              value: "heartbeat"
                            - label: "Spin 360"
                              value: "spin-360"
                            - label: "Flip"
                              value: "flip"
                            - label: "Vibrate"
                              value: "vibrate"
                    - name: color
                      label: "Effect Color"
                      selector:
                        ui_color: {}
                    - name: condition
                      label: "Condition (optional)"
                      selector:
                        condition: {}
    
        # Sub-Button Effects
        - type: expandable
          title: "Sub-Button Effects"
          icon: "mdi:animation-outline"
          name: sub_button_effects
          schema:
            - type: expandable
              title: "Sub-Button 1"
              name: "0"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color (e.g. for Glow)"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 2"
              name: "1"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color (e.g. for Glow)"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 3"
              name: "2"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color (e.g. for Glow)"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 4"
              name: "3"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color (e.g. for Glow)"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 5"
              name: "4"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color (e.g. for Glow)"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 6"
              name: "5"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color (e.g. for Glow)"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
    
        - type: expandable
          title: "Entity Badge Effects"
          icon: "mdi:tag-text"
          name: entity_badge_effects
          schema:
            - type: expandable
              title: "Main Icon"
              name: main
              schema:
                - name: effect
                  label: "Effect type"
                  selector:
                    select:
                      options:
                        - label: None
                          value: none
                        - label: Pulse
                          value: pulse
                        - label: Rotate
                          value: rotate
                        - label: Glow
                          value: glow
                        - label: Shake
                          value: shake
                        - label: Float
                          value: float
                        - label: Zoom
                          value: zoom
                        - label: Heartbeat
                          value: heartbeat
                        - label: Spin
                          value: spin-360
                        - label: Flip
                          value: flip
                        - label: Vibrate
                          value: vibrate
                - name: color
                  label: "Effect color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 1"
              name: "0"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 2"
              name: "1"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 3"
              name: "2"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 4"
              name: "3"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 5"
              name: "4"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 6"
              name: "5"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
    
        # Icon Badge Effects
        - type: expandable
          title: "Icon Badge Effects"
          icon: "mdi:tag-outline"
          name: icon_badge_effects
          schema:
            - type: expandable
              title: "Main Icon"
              name: main
              schema:
                - name: effect
                  label: "Effect type"
                  selector:
                    select:
                      options:
                        - label: None
                          value: none
                        - label: Pulse
                          value: pulse
                        - label: Rotate
                          value: rotate
                        - label: Glow
                          value: glow
                        - label: Shake
                          value: shake
                        - label: Float
                          value: float
                        - label: Zoom
                          value: zoom
                        - label: Heartbeat
                          value: heartbeat
                        - label: Spin
                          value: spin-360
                        - label: Flip
                          value: flip
                        - label: Vibrate
                          value: vibrate
                - name: color
                  label: "Effect color"
                  selector:
                    ui_color:
                      include_none: true
                - name: condition
                  label: "Condition"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 1"
              name: "0"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 2"
              name: "1"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 3"
              name: "2"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 4"
              name: "3"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 5"
              name: "4"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
            - type: expandable
              title: "Sub-Button 6"
              name: "5"
              schema:
                - name: effect
                  label: "Effect Type"
                  selector:
                    select:
                      options:
                        - label: "Pulse (Scale)"
                          value: "pulse"
                        - label: "Gentle Rotation"
                          value: "rotate"
                        - label: "Glow Effect"
                          value: "glow"
                        - label: "Gentle Shake"
                          value: "shake"
                        - label: "Float Up & Down"
                          value: "float"
                        - label: "Zoom"
                          value: "zoom"
                        - label: "Heartbeat"
                          value: "heartbeat"
                        - label: "Spin 360"
                          value: "spin-360"
                        - label: "Flip"
                          value: "flip"
                        - label: "Vibrate"
                          value: "vibrate"
                - name: color
                  label: "Effect Color"
                  selector:
                    ui_color: {}
                - name: condition
                  label: "Condition (optional)"
                  selector:
                    condition: {}
    
        # Icon Effects
    - type: expandable
      title: "Global Defaults"
      icon: "mdi:tune-variant"
      name: global_defaults
      schema:
        - name: badge_color
          label: "Global badge background color"
          selector:
            ui_color:
              include_none: true
        - name: badge_text_color
          label: "Global badge text color"
          selector:
            ui_color:
              include_none: true
        - name: badge_scale
          label: "Global badge scale (unless overridden)"
          default: 1
          selector:
            number:
              min: 0.5
              max: 3
              step: 0.1
              mode: slider
        - name: badge_h_pos
          label: "Global badge horizontal offset"
          default: -8
          selector:
            number:
              min: -100
              max: 100
              step: 1
              mode: slider
        - name: badge_v_pos
          label: "Global badge vertical offset"
          default: -8
          selector:
            number:
              min: -100
              max: 100
              step: 1
              mode: slider
        - name: icon_color
          label: "Global sub-button icon color"
          selector:
            ui_color:
              include_none: true
        - name: sub_button_effect
          label: "Global sub-button effect"
          default: "none"
          selector:
            select:
              options:
                - label: None
                  value: none
                - label: Pulse
                  value: pulse
                - label: Rotate
                  value: rotate
                - label: Glow
                  value: glow
                - label: Shake
                  value: shake
                - label: Float
                  value: float
                - label: Zoom
                  value: zoom
                - label: Heartbeat
                  value: heartbeat
                - label: Spin
                  value: spin-360
                - label: Flip
                  value: flip
                - label: Vibrate
                  value: vibrate
        - name: sub_button_effect_color
          label: "Global effect color"
          selector:
            ui_color:
              include_none: true
        - name: sub_button_background
          label: "Global sub-button background"
          selector:
            object:
              fields:
                type:
                  label: Background type
                  selector:
                    select:
                      options:
                        - label: Solid
                          value: solid
                        - label: Two-color gradient
                          value: two-color
                        - label: Three-color gradient
                          value: three-color
                color:
                  label: Solid color
                  selector:
                    ui_color: {}
                condition:
                  label: Condition
                  selector:
                    condition: {}
```

</details>

---

### Screenshots:
![Options](https://github.com/user-attachments/assets/05af8dac-5a6b-4c0d-8edc-5572ff2836e2)
![Badgy_sample](https://github.com/user-attachments/assets/8983ea13-0adb-4e94-ac95-d465ef2c94f4)
