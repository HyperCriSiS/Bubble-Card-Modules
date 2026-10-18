"""Actual Home Assistant E2E: hot configuration, CSS isolation and mobile touch.

The tests inherit only the real HA fixture setup, never the mocked DOM setup.
"""
import json
import time

from playwright.sync_api import expect
import test_lovelace as base


class LiveConfigurationAndTouch(base.RealLovelace):
    # unittest discovers inherited methods unless explicitly masked.
    test_01_actual_renderer_and_native_slider = None
    test_02_external_main_state_update = None
    test_03_child_rgb_websocket_updates_gradient = None
    test_04_native_slider_pointer_drives_ha_service = None
    test_05_original_bubble_card_without_vsc = None
    test_06_navigation_and_reconnection = None

    def test_10_no_vsc_style_leak_to_native_card(self):
        """VSC must not write inline vars or overrides on another Bubble Card."""
        vsc = self.page.locator("bubble-card").nth(0)
        native = self.page.locator("bubble-card").nth(1)
        result = self.wait_value(
            lambda: {
                "vsc": vsc.evaluate("""el => ({
                    gradient:el.card?.style.getPropertyValue('--card-gradient') ?? '',
                    owned:!!el.card?._vscOwnedVariables
                })"""),
                "native": native.evaluate("""el => ({
                    gradient:el.card?.style.getPropertyValue('--card-gradient') ?? '',
                    owned:!!el.card?._vscOwnedVariables,
                    vscClass:el.card?.classList.contains('use-gradient-background') ?? false
                })"""),
            },
            lambda v: v["vsc"]["owned"] and "linear-gradient" in v["vsc"]["gradient"],
        )
        self.assertEqual(result["native"]["gradient"], "", result)
        self.assertFalse(result["native"]["owned"], result)
        self.assertFalse(result["native"]["vscClass"], result)

    def test_11_disable_and_reenable_vsc_while_card_is_mounted(self):
        """Reconfiguring a mounted card must not leave stale owned styles."""
        card = self.page.locator("bubble-card").first
        original = card.evaluate("""el => {
            const config = el.config || el._config;
            if (!config?.styles) return {hasStyles:false};
            window.__vsc_original_config = {...config};
            return {hasStyles:true,
                gradient:el.card?.style.getPropertyValue('--card-gradient') ?? '',
                owned:!!el.card?._vscOwnedVariables};
        }""")
        self.assertTrue(original["hasStyles"], original)
        self.assertIn("linear-gradient", original["gradient"])
        card.evaluate("""el => {
            el.setConfig({...window.__vsc_original_config, styles:'',
                visual_styling_center:{}});
            const ha=document.querySelector('home-assistant');
            if(ha?.hass) el.hass=ha.hass;
        }""")
        disabled = self.wait_value(
            lambda: card.evaluate("""el => ({
                gradient:el.card?.style.getPropertyValue('--card-gradient') ?? '',
                owned:!!el.card?._vscOwnedVariables,
                vscClass:el.card?.classList.contains('use-gradient-background') ?? false
            })"""),
            lambda d: not d["owned"] and not d["vscClass"] and not d["gradient"],
            timeout=12,
        )
        self.assertEqual(disabled["gradient"], "")
        card.evaluate("""el => {
            el.setConfig({...window.__vsc_original_config});
            const ha=document.querySelector('home-assistant');
            if(ha?.hass) el.hass=ha.hass;
        }""")
        self.wait_value(
            lambda: card.evaluate("""el => ({
                gradient:el.card?.style.getPropertyValue('--card-gradient') ?? '',
                owned:!!el.card?._vscOwnedVariables
            })"""),
            lambda d: d["owned"] and "linear-gradient" in d["gradient"],
            timeout=12,
        )

    def test_12_mobile_touch_drag_updates_real_light(self):
        """A genuine touch stream must drive the native slider service."""
        context = self.browser.new_context(
            viewport={"width":390, "height":844},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        tokens = json.dumps(self.auth, separators=(",", ":"))
        context.add_init_script(script=f"""
            if (location.origin === {json.dumps(base.BASE)}) {{
                localStorage.setItem('hassTokens', {json.dumps(tokens)});
            }}
        """)
        page = context.new_page()
        try:
            page.goto(base.BASE + "/lovelace-vsc-e2e/vsc", wait_until="domcontentloaded", timeout=65000)
            slider = page.locator("bubble-card").first.locator(".bubble-range-slider").first
            expect(slider).to_be_visible(timeout=45000)
            # Wait for the real HA state pass to position the native slider
            # before sending CDP touch events. Avoid automatic gesture retries.
            expect(page.locator("bubble-card").first.locator(".bubble-range-fill").first).to_be_attached(timeout=45000)
            bounds = self.wait_slider_layout(slider, page=page)
            self.assertIsNotNone(bounds)
            self.assertGreater(bounds["width"], 20)
            y = bounds["y"] + bounds["height"] * 0.5
            x0 = bounds["x"] + bounds["width"] * 0.22
            x1 = bounds["x"] + bounds["width"] * 0.82
            client = context.new_cdp_session(page)
            client.send("Input.dispatchTouchEvent", {
                "type": "touchStart", "touchPoints": [{"x":x0, "y":y, "id":1, "force":1}]
            })
            page.wait_for_timeout(110)
            for step in range(1, 10):
                x = x0 + (x1 - x0) * step / 9
                client.send("Input.dispatchTouchEvent", {
                    "type": "touchMove", "touchPoints": [{"x":x, "y":y, "id":1, "force":1}]
                })
                time.sleep(0.025)
            client.send("Input.dispatchTouchEvent", {"type":"touchEnd", "touchPoints":[]})
            self.wait_entity(
                "input_number.vsc_main_brightness",
                lambda item: abs(float(item["state"]) - 128) >= 10,
                timeout=25,
            )
            page.screenshot(path=str(base.ARTIFACTS / "test_12_mobile_touch.png"), full_page=True)
        finally:
            context.close()
