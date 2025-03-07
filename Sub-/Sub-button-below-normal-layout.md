


					# Subbutton_Below_Normal_Layout

**Version:** v2025.03.07
**Creator:** [HyperCriSiS](https://github.com/HyperCriSiS)

> [!IMPORTANT] 
> **Unsupported cards:**
>  - horizontal-buttons-stack
>  - pop-up
>  - empty-column

This module adds all the necessary CSS to move the subbuttons below the main content in normal layout cards. It gives the main feature and title more room while positioning subbuttons in a row at the bottom.

Configure this module via the editor or in YAML, for example: 

```yaml
type: custom:bubble-card
card_type: button
modules:
  - default
  - subbutton_below_normal
entity: light.schlafzimmer
sub_button:
  - entity: light.schlafzimmer
  - entity: light.schlafzimmer
  - entity: light.schlafzimmer
  - entity: light.schlafzimmer
  - entity: light.schlafzimmer
  - entity: light.schlafzimmer
  - entity: light.schlafzimmer
  - entity: light.schlafzimmer
card_layout: normal
button_type: slider
grid_options:
  columns: 12
  rows: 2
```

---

<details>

<summary><b>?? Get this Module</b></summary>

<br>

> To use this module, simply copy and paste the following configuration into your `/www/bubble/bubble-modules.yaml` file.

```yaml
subbutton_below_normal_layout:
    name: Sub-button below (normal layout)
    version: "v2025.07.03"
    creator: "HyperCriSiS (Modified from MrBearPresident's original, optimized for large layout)"
    link: "https://github.com/Clooos/Bubble-Card/discussions/1291"
    description: This module adds all the necessary CSS to move the subbuttons below the main content in normal layout cards. It gives the main feature and title more room while positioning subbuttons in a row at the bottom.
    unsupported:
      - horizontal-buttons-stack
      - pop-up
      - empty-column
    code: |
          :host{
            --row-size-copy: var(--row-size,1);
          }

          /* Normal layout styles */
          .bubble-button-card, .bubble-climate, 
          .bubble-select-card, .bubble-separator, 
          .bubble-cover-card-container{
            display: grid;
            grid-template-areas:
              'i n a'
              'b b b' !important;
            grid-template-columns: auto 1fr auto;
            grid-template-rows: 50px 50px;
            justify-self: start;
            justify-items: start;
            align-self: center;
            align-items: center;
            width: 100%;
            gap: 0px;
            height: 100px;
          }

          .bubble-cover-card-container .bubble-header {
            display: contents;
          }

          .bubble-cover-card-container .bubble-buttons {
            display: flex;
            align-self: center;
            grid-area: a !important;
            right: 0;
            padding: 0 18px 0 0;
          }

          .bubble-separator.separator-container{
            grid-template-columns: auto auto 1fr;
          }

          .bubble-media-player{
            display: grid;
            grid-template-areas:
              'i n a1 a2 a3 a4 a5'
              'b b b b b b b' !important;
            grid-template-columns: auto 1fr auto auto auto auto auto;
            grid-template-rows: 50px 50px;
            justify-self: start;
            justify-items: start;
            align-self: center;
            align-items: center;
            height: 100px;
          }

          .bubble-climate .bubble-button-container{
            grid-area: a;
            display: contents !important;
          }

          .bubble-climate .bubble-temperature-container{
            grid-area: a;
            height: 30px;
            width: auto;
            justify-self: center;
            margin-right: var(--gap-to-edge,7px);
          }

          .bubble-select-card > .bubble-dropdown-container{
            grid-area: a;
            display: contents !important;
          }

          .bubble-select-card .bubble-dropdown-arrow{
            grid-area: a;
          }

          .bubble-media-player-container .bubble-power-button{
            grid-area: a1;
            margin: 0px 6px;
          }

          .bubble-media-player-container .bubble-previous-button{
            grid-area: a2;
            margin: 0px 6px;
          }

          .bubble-media-player-container .bubble-next-button{
            grid-area: a3;
            margin: 0px 6px;
          }

          .bubble-media-player-container .bubble-volume-button{
            grid-area: a4;
            margin: 0px 6px;
          }

          .bubble-line{
            grid-area: a;
            width: 100%;
          }

          .bubble-media-player-container .bubble-play-pause-button {
            display: flex;
            height: 38px;
            width: 38px;
            padding: 0;
            grid-area: a5;
            align-items: center;
            justify-content: center;
            margin: 7px 7px 7px 6px;
          }

          .bubble-media-player-container .bubble-button-container{
            grid-area: a1;
            display: contents;
          }

          .bubble-name-container {
            justify-content: flex-start;
            grid-area: n;
            overflow: hidden;
            max-width: calc(100% - 2 * var(--gap-to-edge,7px));
          }

          .bubble-sub-button-container {
            max-width: calc(100% - 20px);
            height: 50px;
            min-height: 38px;
            grid-area: b;
            justify-self: center;
            align-self: center;
            justify-content: center;
            align-content: center;
            justify-items: center;
            margin: 0;
            left: 0;
            right: 0;
            display: flex !important;
            flex-wrap: wrap;
            gap: 8px;
            overflow: visible !important;
          }

          .bubble-icon-container {
            grid-area: i;
          }

          /* Adjust sub-buttons styling */
          .bubble-sub-button {
            margin: 0 !important;
          }

          /* Keep large layout support */
          .large .bubble-button-card, .large .bubble-climate, .large
          .bubble-select-card, .large .bubble-separator, .large
          .bubble-cover-card-container{
            grid-template-rows: var(--row-height,56px) 1fr;
          }

          .large .bubble-climate .bubble-temperature-container{
            height: calc(var(--row-height,56px) - 20px);
          }

          .large .bubble-sub-button-container {
            --row-size: calc( var(--row-size-copy) - 1);
            max-height: calc(100% - 20px);
          }

          .large .bubble-media-player-container .bubble-play-pause-button {
            height: 42px;
            width: 42px;
          }

          /* Increase container height to accommodate sub-buttons */
          .bubble-button-card-container,
          .bubble-cover-card-container,
          .bubble-climate-container,
          .bubble-select-card-container,
          .bubble-media-player-container {
            height: 100px !important; /* Fixed height to show both rows without scrolling */
            min-height: 100px;
            padding-bottom: 0;
            overflow: visible !important; /* Ensure content isn't cut off */
          }
```

</details>

---

### Screenshot:
![Slider-Control-Center](https://github.com/HyperCriSiS/Bubble-Card-Modules/blob/main/Slider-Control-Center/Slider-Control-Center.png)

