"""Real HA layout/theme matrix for VSC.

Each layout (normal, large, grid, pop-up, sections and a card combining VSC
with another styling module) is rendered by the real Lovelace frontend under
both the light and the dark default theme (driven by prefers-color-scheme).
"""
import json
import unittest

import test_lovelace as base
from playwright.sync_api import expect

RED="rgb(255, 0, 0)"
GREEN="rgb(0, 200, 20)"
SCHEMES=("light","dark")

# Reads every rendered bubble-card (shadow roots included) by its config name.
READ_CARDS="""els => els.map(el => {
    const card=el.card;
    const q=s=>card?.querySelector(s);
    const container=q('.bubble-button-card-container');
    const button=q('.bubble-button-card');
    const rect=card?.getBoundingClientRect();
    return {
        name:el.config?.name ?? null,
        owned:!!card?._vscOwnedVariables,
        icon:q('.bubble-icon')?.style.color||'',
        sub:q('.bubble-sub-button-1 .bubble-sub-button-icon')?.style.color||'',
        large:!!(card?.classList.contains('large')||q('.large')),
        background:container?getComputedStyle(container).backgroundColor:'',
        areas:button?getComputedStyle(button).gridTemplateAreas:'',
        height:rect?.height||0
    };
})"""

class LayoutThemeMatrix(base.RealLovelace):
    # Reuse the shared HA fixtures; the inherited cases run in test_lovelace.py.
    test_01_actual_renderer_and_native_slider = None
    test_02_external_main_state_update = None
    test_03_child_rgb_websocket_updates_gradient = None
    test_04_native_slider_pointer_drives_ha_service = None
    test_05_original_bubble_card_without_vsc = None
    test_06_navigation_and_reconnection = None

    def setUp(self):
        self.service("input_boolean","turn_on","input_boolean.vsc_main_enabled")
        self.service("input_boolean","turn_on","input_boolean.vsc_child_enabled")
        for slug,colors in (("main",(255,0,0)),("child",(0,200,20))):
            for name,v in zip(("red","green","blue"),colors):
                self.service("input_number","set_value",f"input_number.vsc_{slug}_{name}",value=v)
        for slug,rgb in (("main",[255,0,0]),("child",[0,200,20])):
            self.wait_entity(f"light.vsc_{slug}",
                             lambda e,rgb=rgb:e["state"]=="on" and e["attributes"].get("rgb_color")==rgb)
        self.contexts=[]

    def tearDown(self):
        for ctx in self.contexts: ctx.close()

    def open(self,scheme,path):
        ctx=self.browser.new_context(viewport={"width":1280,"height":900},color_scheme=scheme)
        self.contexts.append(ctx)
        tokens=json.dumps(self.auth,separators=(",",":"))
        ctx.add_init_script(script=f"""
            if (location.origin === {json.dumps(base.BASE)}) {{
                localStorage.setItem('hassTokens', {json.dumps(tokens)});
            }}
        """)
        self.page=ctx.new_page()
        self.errors=[]
        self.page.on("pageerror",lambda e:self.errors.append(str(e)))
        self.page.goto(base.BASE+"/lovelace-vsc-e2e/"+path,wait_until="domcontentloaded",timeout=65000)
        expect(self.page.locator("bubble-card").first).to_be_attached(timeout=65000)
        dark=self.wait_value(lambda:self.page.evaluate(
            "() => document.querySelector('home-assistant')?.hass?.themes?.darkMode ?? null"),
            lambda v:v is not None)
        self.assertEqual(dark,scheme=="dark","HA did not follow the emulated color scheme")
        return self.page

    def cards(self):
        return {c["name"]:c for c in self.page.locator("bubble-card").evaluate_all(READ_CARDS)}

    def wait_cards(self,names,ready):
        return self.wait_value(self.cards,lambda c:all(n in c and ready(c[n]) for n in names),timeout=30)

    def shot(self,name):
        self.page.screenshot(path=str(base.ARTIFACTS/f"matrix_{name}.png"),full_page=True,timeout=12000)

    def test_20_masonry_layouts_in_light_and_dark(self):
        names=("Matrix Normal","Matrix Large","Matrix Grid A","Matrix Grid B","Matrix Combined")
        backgrounds={}
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                self.open(scheme,"matrix")
                cards=self.wait_cards(names,lambda c:c["icon"]==RED and c["height"]>0)
                self.shot("masonry_"+scheme)
                for name in names:
                    self.assertTrue(cards[name]["owned"],cards[name])
                self.assertTrue(cards["Matrix Large"]["large"],cards["Matrix Large"])
                self.assertFalse(cards["Matrix Normal"]["large"],cards["Matrix Normal"])
                # Grid cells receive the same VSC treatment as stand-alone cards.
                self.assertEqual(cards["Matrix Grid A"]["icon"],cards["Matrix Grid B"]["icon"])
                backgrounds[scheme]=cards["Matrix Normal"]["background"]
                self.assertFalse(self.errors,self.errors)
        # VSC leaves the card surface to the theme.
        self.assertNotEqual(backgrounds["light"],backgrounds["dark"],backgrounds)

    def test_21_combined_with_sub_button_below_module(self):
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                self.open(scheme,"matrix")
                card=self.wait_cards(("Matrix Combined",),
                                     lambda c:c["icon"]==RED and c["sub"]==GREEN)["Matrix Combined"]
                self.assertTrue(card["owned"],card)
                # The other module's grid still wins for layout.
                self.assertIn('"b b b"',card["areas"],card)
                self.assertFalse(self.errors,self.errors)

    def test_22_popup_content_in_light_and_dark(self):
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                page=self.open(scheme,"matrix")
                self.wait_cards(("Matrix Normal",),lambda c:c["icon"]==RED)
                page.evaluate("() => { location.hash='#vsc-matrix'; }")
                card=self.wait_cards(("Matrix Popup",),
                                     lambda c:c["icon"]==RED and c["height"]>0)["Matrix Popup"]
                self.shot("popup_"+scheme)
                self.assertTrue(card["owned"],card)
                # External state changes still reach the card inside the pop-up.
                self.service("input_boolean","turn_off","input_boolean.vsc_main_enabled")
                self.wait_cards(("Matrix Popup",),lambda c:c["icon"]=="rgb(150, 150, 150)")
                self.service("input_boolean","turn_on","input_boolean.vsc_main_enabled")
                self.wait_entity("light.vsc_main",lambda e:e["state"]=="on")
                self.assertFalse(self.errors,self.errors)

    def test_23_sections_view_in_light_and_dark(self):
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                self.open(scheme,"sections")
                cards=self.wait_cards(("Sections VSC","Sections Native"),lambda c:c["height"]>0)
                cards=self.wait_cards(("Sections VSC",),lambda c:c["icon"]==RED)
                self.shot("sections_"+scheme)
                vsc,native=cards["Sections VSC"],cards["Sections Native"]
                self.assertTrue(vsc["owned"],vsc)
                self.assertFalse(native["owned"],native)
                # Sections default to the large layout in Bubble Card.
                self.assertTrue(vsc["large"] and native["large"],(vsc,native))
                self.assertEqual(vsc["background"],native["background"],(vsc,native))
                self.assertFalse(self.errors,self.errors)

if __name__=="__main__":unittest.main()
