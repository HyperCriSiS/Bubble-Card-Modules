"""Additional genuine Home Assistant + Bubble Card tests for edge layouts/lifecycle.

The shared fixtures come from test_lovelace.py, and the inherited six tests
are explicitly masked to avoid running the same cases twice.
"""
import test_lovelace as base
from playwright.sync_api import expect

class ExtendedRealLovelace(base.RealLovelace):
    test_01_actual_renderer_and_native_slider = None
    test_02_external_main_state_update = None
    test_03_child_rgb_websocket_updates_gradient = None
    test_04_native_slider_pointer_drives_ha_service = None
    test_05_original_bubble_card_without_vsc = None
    test_06_navigation_and_reconnection = None

    def test_07_mixed_group_icon_color_order(self):
        def colors():
            return self.page.locator("bubble-card").nth(2).evaluate("""el => {
                const selectors=[1,2,3].map(n=>'.bubble-sub-button-'+n+' .bubble-sub-button-icon');
                return selectors.map(s=>el.card?.querySelector(s)?.style.color??null);
            }""")
        before=self.wait_value(colors,lambda c:all(x is not None for x in c))
        self.assertEqual(before,["rgb(0, 200, 20)","rgb(255, 0, 0)","rgb(255, 0, 0)"],before)
        self.service("input_boolean","turn_off","input_boolean.vsc_child_enabled")
        self.wait_entity("light.vsc_child",lambda e:e["state"]=="off")
        updated=self.wait_value(colors,lambda c:c[0]=="rgb(150, 150, 150)")
        self.assertEqual(updated[1:],[before[1],before[2]],updated)

    def test_08_native_inline_sub_slider_updates_child_light(self):
        card=self.page.locator("bubble-card").first
        slider=card.locator(".bubble-sub-button-slider .bubble-range-slider").first
        bounds=self.wait_slider_layout(slider)
        self.assertIsNotNone(bounds,"Native inline slider must have a bounding box")
        self.assertGreater(bounds["width"],15)
        y=bounds["y"]+bounds["height"]*0.5
        self.page.mouse.move(bounds["x"]+bounds["width"]*0.22,y)
        self.page.mouse.down()
        self.page.mouse.move(bounds["x"]+bounds["width"]*0.88,y,steps=12)
        self.page.mouse.up()
        self.wait_entity("input_number.vsc_child_brightness",
                         lambda s:abs(float(s["state"])-128)>=10,timeout=25)

    def test_09_native_disconnect_cleans_module_owned_styles(self):
        card=self.page.locator("bubble-card").first
        before=card.evaluate("""el => ({
            gradient:el.card?.style.getPropertyValue('--card-gradient'),
            owned:!!el.card?._vscOwnedVariables
        })""")
        self.assertTrue(before["owned"],before)
        self.assertIn("linear-gradient",before["gradient"],before)
        after=card.evaluate("""el => {
            const card=el.card;
            el.remove();
            return {owned:!!card?._vscOwnedVariables,
                    gradient:card?.style.getPropertyValue('--card-gradient')||''};
        }""")
        self.assertFalse(after["owned"],after)
        self.assertEqual(after["gradient"],"",after)

    def test_18_icon_background_matches_native_card_with_red_light(self):
        """VSC with no icon background option keeps Bubble Card's own circle."""
        def backgrounds():
            loc=self.page.locator("bubble-card")
            read="""el => {
                const icon=el.card?.querySelector('.bubble-icon-container');
                return icon ? getComputedStyle(icon).backgroundColor : null;
            }"""
            return [loc.nth(0).evaluate(read), loc.nth(1).evaluate(read)]
        vsc,native=self.wait_value(backgrounds,lambda v:all(v))
        self.assertEqual(self.entity("light.vsc_main")["attributes"]["rgb_color"],[255,0,0])
        self.assertEqual(vsc,native,(vsc,native))
        self.assertNotEqual(vsc,"rgba(0, 0, 0, 0)",(vsc,native))

    def test_19_sub_buttons_card_type_with_vsc(self):
        """The sub-buttons card has no main icon or slider; VSC styles its sub-buttons."""
        card=self.page.locator("bubble-card").nth(3)
        def data():
            return card.evaluate("""el => {
                const b=n=>el.card?.querySelector('.bubble-sub-button-'+n);
                const box=n=>b(n)?.getBoundingClientRect().height||0;
                return {
                    color:b(1)?.querySelector('.bubble-sub-button-icon')?.style.color||'',
                    first:box(1), second:box(2),
                    owned:!!el.card?._vscOwnedVariables
                };
            }""")
        # Height transitions natively for 0.5 s.
        self.page.wait_for_timeout(700)
        result=self.wait_value(data,lambda d:d["color"]=="rgb(255, 0, 0)" and d["second"]>0)
        self.assertTrue(result["owned"],result)
        self.assertAlmostEqual(result["first"],40,delta=0.5,msg=result)
        # The sub-button's own custom_height beats the module size.
        self.assertAlmostEqual(result["second"],44,delta=0.5,msg=result)
        self.assertFalse(self.errors,self.errors)
