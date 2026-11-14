# Button Stack Gestures

**Version:** v2026.11.14
**Creator:** [HyperCriSiS](https://github.com/HyperCriSiS)

> [!IMPORTANT]
> **Supported cards:**
>  - Horizontal buttons stack

Adds freely configurable gestures to the buttons of the horizontal buttons stack card:

- **Hold** (long press)
- **Swipe up**
- **Swipe down**
- **Tap** (optional, replaces the native tap of the button)

Every gesture accepts any Home Assistant action: open a pop-up (navigate to its hash, for example `#kitchen`), toggle an entity, show more info, perform an action (service), open a URL, start Assist or fire a DOM event.

## How it works

- Gestures are configured per button. `button` is the position of the button in the card (`1` is `1_link`, `2` is `2_link`, and so on).
- An entry without `button` applies to every button. An entry with a `button` number wins over it gesture by gesture, so set an action to `none` there to switch a gesture off for that button.
- `entity` is the entity used by toggle and more info. Without it the button's light entity (`1_entity`, `2_entity`, ...) is used.
- A gesture that fires never also triggers the native tap, so a hold or swipe does not open the button's pop-up as well.
- Without a `tap_action` the native tap stays exactly as it is.
- Swipes left and right are not offered, because they scroll the stack.
- On a button with a swipe gesture, a vertical drag or pinch zoom that starts on it no longer moves the page. The stack is fixed to the bottom of the screen, so this only affects gestures that start on such a button.
- The space below the stack is small, so keep the swipe distance low (default 30 px) if you use swipe down.
- Avoid a gesture that opens the button's own `link` pop-up. The native tap does not notice it, so the first tap afterwards does nothing and only the second one closes the pop-up.

Configure this module via the editor or in YAML, for example:

```yaml
type: custom:bubble-card
card_type: horizontal-buttons-stack
modules:
  - button_stack_gestures
1_name: Kitchen
1_icon: mdi:fridge
1_link: '#kitchen'
1_entity: light.kitchen
2_name: Living room
2_icon: mdi:sofa
2_link: '#living-room'
button_stack_gestures:
  hold_time: 500
  swipe_distance: 30
  buttons:
    - button: 1
      hold_action:
        action: toggle
      swipe_up_action:
        action: navigate
        navigation_path: '#kitchen-lights'
    - swipe_down_action:
        action: perform-action
        perform_action: scene.turn_on
        target:
          entity_id: scene.good_night
```

---

<details>

<summary><b>🧩 Get this Module</b></summary>

<br>

> To use this module, simply copy and paste the following configuration into your `/www/bubble/bubble-modules.yaml` file.

```yaml
button_stack_gestures:
  name: Button Stack Gestures
  version: "v2026.11.14"
  creator: HyperCriSiS
  link: https://github.com/HyperCriSiS/Bubble-Card-Modules/tree/main/Button-Stack-Gestures
  supported:
    - horizontal-buttons-stack
  description: |
    Hold, swipe up, swipe down and tap actions for the buttons of the horizontal buttons stack.
    Every gesture accepts any Home Assistant action, for example navigate to a pop-up hash.
    An entry without a button number applies to every button.
  code: |
    ${(() => {
      const host = card;
      if (!host) return '';
      const options = () => this.config?.button_stack_gestures ?? {};
      const items = () => (Array.isArray(options().buttons) ? options().buttons : []).filter((item) => item && typeof item === 'object');
      const real = (action) => (action && action.action && action.action !== 'none' ? action : null);
      const number = (value, fallback, min) => (Number.isFinite(Number(value)) && Number(value) >= min ? Number(value) : fallback);

      if (!host._buttonStackGestures) {
        const findButton = (event) => {
          const button = event.target?.closest?.('.bubble-button');
          return button && host.contains(button) ? button : null;
        };
        const actionsFor = (button) => {
          const index = Number(button.index);
          const list = items();
          const exact = list.find((item) => Number(item.button) === index);
          const all = list.find((item) => item.button === undefined || item.button === null || item.button === '');
          const pick = (key) => real(exact && key in exact ? exact[key] : all?.[key]);
          return {
            tap: pick('tap_action'),
            hold: pick('hold_action'),
            up: pick('swipe_up_action'),
            down: pick('swipe_down_action'),
            entity: exact?.entity || all?.entity || this.config?.[index + '_entity'] || undefined,
          };
        };
        const fire = (button, action, entity) => {
          const event = new Event('hass-action', { bubbles: true, composed: true });
          event.detail = { config: { entity, entity_id: entity, tap_action: action }, action: 'tap' };
          button.dispatchEvent(event);
          const haptic = new Event('haptic');
          haptic.detail = 'medium';
          window.dispatchEvent(haptic);
        };

        const state = { gesture: null, suppress: false };
        const end = () => {
          clearTimeout(state.gesture?.timer);
          state.gesture = null;
          window.removeEventListener('pointermove', move);
          window.removeEventListener('pointerup', up);
          window.removeEventListener('pointercancel', cancel);
          document.removeEventListener('visibilitychange', end);
        };
        const move = (event) => {
          const gesture = state.gesture;
          if (!gesture || event.pointerId !== gesture.id) return;
          if (Math.hypot(event.clientX - gesture.x, event.clientY - gesture.y) > 10) clearTimeout(gesture.timer);
        };
        const up = (event) => {
          const gesture = state.gesture;
          if (!gesture || event.pointerId !== gesture.id) return;
          end();
          if (gesture.held) return;
          const dx = event.clientX - gesture.x;
          const dy = event.clientY - gesture.y;
          if (Math.abs(dy) < number(options().swipe_distance, 30, 5) || Math.abs(dy) <= Math.abs(dx)) return;
          const action = dy < 0 ? gesture.actions.up : gesture.actions.down;
          if (!action) return;
          state.suppress = true;
          fire(gesture.button, action, gesture.actions.entity);
        };
        const cancel = (event) => {
          if (state.gesture && event.pointerId === state.gesture.id) end();
        };
        const down = (event) => {
          end();
          state.suppress = false;
          if (event.button > 0) return;
          const button = findButton(event);
          if (!button) return;
          const actions = actionsFor(button);
          if (!actions.hold && !actions.up && !actions.down) return;
          const gesture = { button, actions, id: event.pointerId, x: event.clientX, y: event.clientY, held: false };
          if (actions.hold) {
            gesture.timer = setTimeout(() => {
              if (state.gesture !== gesture) return;
              gesture.held = true;
              state.suppress = true;
              fire(button, actions.hold, actions.entity);
            }, number(options().hold_time, 500, 100));
          }
          state.gesture = gesture;
          window.addEventListener('pointermove', move);
          window.addEventListener('pointerup', up);
          window.addEventListener('pointercancel', cancel);
          // A press cut short by leaving the app never fires the hold on return.
          document.addEventListener('visibilitychange', end);
        };
        const click = (event) => {
          const button = findButton(event);
          if (!button) return;
          if (state.suppress) {
            state.suppress = false;
            event.stopPropagation();
            event.preventDefault();
            return;
          }
          const actions = actionsFor(button);
          if (!actions.tap) return;
          event.stopPropagation();
          event.preventDefault();
          fire(button, actions.tap, actions.entity);
        };
        const menu = (event) => {
          if (state.gesture?.actions.hold || state.suppress) event.preventDefault();
        };

        host.addEventListener('pointerdown', down);
        host.addEventListener('click', click, true);
        host.addEventListener('contextmenu', menu);
        host._buttonStackGestures = () => {
          end();
          host.removeEventListener('pointerdown', down);
          host.removeEventListener('click', click, true);
          host.removeEventListener('contextmenu', menu);
          delete host._buttonStackGestures;
        };
      }
      if (typeof onTeardown === 'function') onTeardown(() => host._buttonStackGestures?.());

      const list = items();
      if (!list.length) return '';
      // Vertical page drags stay possible on buttons without a swipe gesture.
      const swipes = list.filter((item) => real(item.swipe_up_action) || real(item.swipe_down_action));
      const all = swipes.some((item) => item.button === undefined || item.button === null || item.button === '');
      const selectors = all ? ['.bubble-button'] : swipes.map((item) => '.bubble-button-' + Number(item.button));
      return '.bubble-button { -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; }'
        + (selectors.length ? ' ' + selectors.join(', ') + ' { touch-action: pan-x; }' : '');
    })()}
  editor:
    - name: hold_time
      label: Hold time
      selector:
        number:
          min: 200
          max: 2000
          step: 50
          unit_of_measurement: ms
      default: 500
    - name: swipe_distance
      label: Swipe distance
      selector:
        number:
          min: 15
          max: 150
          step: 5
          unit_of_measurement: px
      default: 30
    - name: buttons
      label: Button gestures
      selector:
        object:
          multiple: true
          label_field: button
          fields:
            button:
              label: Button number (empty applies to every button)
              selector:
                number:
                  min: 1
                  max: 30
                  step: 1
                  mode: box
            entity:
              label: Entity for toggle and more info (default is the button's light entity)
              selector:
                entity: {}
            tap_action:
              label: Tap action (empty keeps the native tap)
              selector:
                ui_action: {}
            hold_action:
              label: Hold action
              selector:
                ui_action: {}
            swipe_up_action:
              label: Swipe up action
              selector:
                ui_action: {}
            swipe_down_action:
              label: Swipe down action
              selector:
                ui_action: {}
```

</details>
