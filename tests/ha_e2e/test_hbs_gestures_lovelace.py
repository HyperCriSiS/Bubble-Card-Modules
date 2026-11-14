"""HBS Gestures on the real horizontal buttons stack in an isolated Home Assistant.

Mouse gestures go through Playwright, touch gestures through CDP touch events,
so touch-action and pointer cancellation behave like on a phone.
"""
import json
import time
import unittest

from playwright.sync_api import expect

# A module import, so unittest discovery does not run RealLovelace a second time.
import test_lovelace as base
from test_lovelace import ARTIFACTS, BASE

CHILD = "input_boolean.vsc_child_enabled"


class HbsGestures(unittest.TestCase):
    api = classmethod(base.RealLovelace.api.__func__)
    service = classmethod(base.RealLovelace.service.__func__)
    entity = classmethod(base.RealLovelace.entity.__func__)
    wait_entity = classmethod(base.RealLovelace.wait_entity.__func__)

    @classmethod
    def setUpClass(cls):
        base.RealLovelace.setUpClass.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        base.RealLovelace.tearDownClass.__func__(cls)

    def setUp(self):
        self.service("input_boolean", "turn_on", "input_boolean.vsc_main_enabled")
        self.service("input_boolean", "turn_on", CHILD)
        self.wait_entity("light.vsc_main", lambda e: e["state"] == "on")
        self.wait_entity(CHILD, lambda e: e["state"] == "on")
        self.context = self.browser.new_context(viewport={"width": 420, "height": 860}, has_touch=True)
        tokens = json.dumps(self.auth, separators=(",", ":"))
        self.context.add_init_script(script=f"""
            if (location.origin === {json.dumps(BASE)}) {{
                localStorage.setItem('hassTokens', {json.dumps(tokens)});
            }}
        """)
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))
        self.page.goto(BASE + "/lovelace-vsc-e2e/hbs", wait_until="domcontentloaded", timeout=65000)
        expect(self.page.get_by_text("HBS gestures")).to_be_visible(timeout=65000)
        for index in (1, 2, 3):
            expect(self.button(index)).to_be_visible(timeout=30000)
        # The stack rises in with an animation; wait until it stands still.
        self.page.wait_for_timeout(1800)

    def tearDown(self):
        try:
            self.page.screenshot(path=str(ARTIFACTS / ("hbs_" + self._testMethodName + ".png")), timeout=12000)
        finally:
            self.context.close()
        self.assertEqual(self.errors, [])

    def button(self, index):
        return self.page.locator(f"bubble-card .bubble-button-{index}").first

    def center(self, index):
        box = self.button(index).bounding_box()
        return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2

    def hash(self):
        return self.page.evaluate("location.hash")

    def wait_hash(self, expected, timeout=10):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.hash() == expected:
                return
            self.page.wait_for_timeout(150)
        raise AssertionError(f"hash={self.hash()!r}, expected {expected!r}; JS={self.errors}")

    def assert_no_native_tap(self):
        self.page.wait_for_timeout(700)
        self.assertNotIn(self.hash(), ("#hbs-one", "#hbs-two", "#hbs-three"))

    def mouse_drag(self, index, dy, hold_ms=0):
        x, y = self.center(index)
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        if hold_ms:
            self.page.wait_for_timeout(hold_ms)
        if dy:
            self.page.mouse.move(x, y + dy, steps=8)
        self.page.mouse.up()

    def touch_drag(self, index, dy, hold_ms=0):
        cdp = self.context.new_cdp_session(self.page)
        x, y = self.center(index)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
        if hold_ms:
            self.page.wait_for_timeout(hold_ms)
        for step in range(1, 9):
            if not dy:
                break
            cdp.send("Input.dispatchTouchEvent",
                     {"type": "touchMove", "touchPoints": [{"x": x, "y": y + dy * step / 8}]})
            self.page.wait_for_timeout(16)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        cdp.detach()

    def test_01_native_tap_unchanged(self):
        self.button(2).click()
        self.wait_hash("#hbs-two")

    def test_02_mouse_hold_toggles_without_native_tap(self):
        self.mouse_drag(1, 0, hold_ms=900)
        self.wait_entity("light.vsc_main", lambda e: e["state"] == "off")
        self.assert_no_native_tap()

    def test_03_mouse_swipe_up_opens_popup(self):
        self.mouse_drag(1, -120)
        self.wait_hash("#hbs-swipe")
        expect(self.page.get_by_text("Swipe pop-up").first).to_be_visible(timeout=10000)

    def test_04_touch_swipe_down_uses_fallback_entry(self):
        self.touch_drag(2, 34)
        self.wait_entity(CHILD, lambda e: e["state"] == "off")
        self.assert_no_native_tap()

    def test_05_touch_hold_toggles(self):
        self.touch_drag(1, 0, hold_ms=900)
        self.wait_entity("light.vsc_main", lambda e: e["state"] == "off")
        self.assert_no_native_tap()

    def test_06_touch_swipe_up_opens_popup(self):
        self.touch_drag(1, -120)
        self.wait_hash("#hbs-swipe")
        expect(self.page.get_by_text("Swipe pop-up").first).to_be_visible(timeout=10000)

    def test_07_tap_override_and_none_blocks_fallback(self):
        self.button(3).click()
        self.wait_entity(CHILD, lambda e: e["state"] == "off")
        self.assert_no_native_tap()
        # Button 3 sets swipe down to none, so the fallback must not turn it off again.
        self.service("input_boolean", "turn_on", CHILD)
        self.wait_entity(CHILD, lambda e: e["state"] == "on")
        self.mouse_drag(3, 34)
        self.page.wait_for_timeout(1200)
        self.assertEqual(self.entity(CHILD)["state"], "on")

    def test_08_short_hold_is_a_native_tap(self):
        self.mouse_drag(1, 0, hold_ms=100)
        self.wait_hash("#hbs-one")
        self.assertEqual(self.entity("light.vsc_main")["state"], "on")


if __name__ == "__main__":
    unittest.main()
