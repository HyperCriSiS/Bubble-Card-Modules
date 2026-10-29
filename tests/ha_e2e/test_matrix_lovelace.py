"""Real HA layout/theme matrix for VSC.

Each layout (normal, large, grid, pop-up, sections, mobile pop-up and cards
combining VSC with other styling modules) is rendered by the real Lovelace
frontend under light and dark mode (driven by prefers-color-scheme), with the
default theme and with a user theme.
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
        width:rect?.width||0,
        height:rect?.height||0,
        badge:!!q('.bubble-sub-button-1 .badgy-owned-badge.icon-badge'),
        bgVar:card?.style.getPropertyValue('--bubble-button-main-background-color')||'',
        themeBg:card?getComputedStyle(card).getPropertyValue('--card-background-color').trim():''
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
            self.service("input_number","set_value",f"input_number.vsc_{slug}_brightness",value=128)
            for name,v in zip(("red","green","blue"),colors):
                self.service("input_number","set_value",f"input_number.vsc_{slug}_{name}",value=v)
        for slug,rgb in (("main",[255,0,0]),("child",[0,200,20])):
            self.wait_entity(f"light.vsc_{slug}",
                             lambda e,rgb=rgb:e["state"]=="on" and e["attributes"].get("rgb_color")==rgb)
        self.contexts=[]

    def tearDown(self):
        for ctx in self.contexts: ctx.close()

    def open(self,scheme,path,mobile=False):
        size={"viewport":{"width":390,"height":844},"device_scale_factor":2,"is_mobile":True,
              "has_touch":True} if mobile else {"viewport":{"width":1280,"height":900}}
        ctx=self.browser.new_context(color_scheme=scheme,**size)
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

    def test_24_user_theme_light_and_dark_modes(self):
        names=("Themed VSC","Themed Native","Themed Custom BG")
        native_bg,custom_bg={},{}
        expected={"light":"rgb(250, 240, 200)","dark":"rgb(20, 30, 60)"}
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                self.open(scheme,"themed")
                cards=self.wait_cards(names,lambda c:c["height"]>0 and c["background"])
                cards=self.wait_cards(("Themed VSC","Themed Custom BG"),lambda c:c["icon"]==RED)
                self.shot("theme_"+scheme)
                vsc,native,custom=(cards[n] for n in names)
                # The view's user theme is really active, in the right mode.
                self.assertEqual(native["themeBg"],expected[scheme],native)
                self.assertTrue(vsc["owned"] and custom["owned"],(vsc,custom))
                # Without a background option VSC leaves the theme surface alone ...
                self.assertEqual(vsc["background"],native["background"],(vsc,native))
                # ... and a VSC background option wins over the theme.
                self.assertIn("10, 20, 30",custom["bgVar"],custom)
                self.assertNotEqual(custom["background"],native["background"],(custom,native))
                native_bg[scheme],custom_bg[scheme]=native["background"],custom["background"]
                self.assertFalse(self.errors,self.errors)
        self.assertNotEqual(native_bg["light"],native_bg["dark"],native_bg)
        self.assertEqual(custom_bg["light"],custom_bg["dark"],custom_bg)

    def test_25_combined_with_badgy(self):
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                self.open(scheme,"matrix")
                card=self.wait_cards(("Matrix Badgy",),
                    lambda c:c["icon"]==RED and c["sub"]==GREEN and c["badge"])["Matrix Badgy"]
                self.assertTrue(card["owned"],card)
                # A child state change still reaches VSC's colors next to the badge.
                self.service("input_boolean","turn_off","input_boolean.vsc_child_enabled")
                card=self.wait_cards(("Matrix Badgy",),
                    lambda c:c["sub"]=="rgb(150, 150, 150)")["Matrix Badgy"]
                self.assertTrue(card["badge"],card)
                self.service("input_boolean","turn_on","input_boolean.vsc_child_enabled")
                self.wait_entity("light.vsc_child",lambda e:e["state"]=="on")
                self.assertFalse(self.errors,self.errors)

    def test_26_mobile_popup_touch(self):
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                self.service("input_number","set_value","input_number.vsc_main_brightness",value=128)
                self.wait_entity("light.vsc_main",lambda e:e["attributes"].get("brightness")==128)
                page=self.open(scheme,"matrix",mobile=True)
                self.wait_cards(("Matrix Normal",),lambda c:c["icon"]==RED)
                page.evaluate("() => { location.hash='#vsc-matrix'; }")
                card=self.wait_cards(("Matrix Popup",),
                                     lambda c:c["icon"]==RED and c["height"]>0)["Matrix Popup"]
                self.assertTrue(card["owned"],card)
                self.assertLessEqual(card["width"],390,card)
                index=page.locator("bubble-card").evaluate_all(
                    "els => els.findIndex(el => el.config?.name === 'Matrix Popup')")
                popup=page.locator("bubble-card").nth(index)
                slider=popup.locator(".bubble-range-slider").first
                bounds=self.wait_slider_layout(slider,page=page)
                y=bounds["y"]+bounds["height"]*0.5
                x0,x1=bounds["x"]+bounds["width"]*0.2,bounds["x"]+bounds["width"]*0.85
                client=page.context.new_cdp_session(page)
                client.send("Input.dispatchTouchEvent",{"type":"touchStart",
                    "touchPoints":[{"x":x0,"y":y,"id":1,"force":1}]})
                page.wait_for_timeout(110)
                for step in range(1,10):
                    client.send("Input.dispatchTouchEvent",{"type":"touchMove",
                        "touchPoints":[{"x":x0+(x1-x0)*step/9,"y":y,"id":1,"force":1}]})
                    page.wait_for_timeout(25)
                client.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]})
                self.wait_entity("input_number.vsc_main_brightness",
                                 lambda e:abs(float(e["state"])-128)>=10,timeout=25)
                self.shot("mobile_popup_"+scheme)
                self.assertFalse(self.errors,self.errors)

    def card_index(self,name):
        return self.page.locator("bubble-card").evaluate_all(
            "(els,n) => els.findIndex(el => el.config?.name === n)",name)

    def test_30_overlay_sub_slider_and_hold_gesture(self):
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme):
                self.service("input_number","set_value","input_number.vsc_child_brightness",value=128)
                self.service("input_boolean","turn_on","input_boolean.vsc_child_enabled")
                self.wait_entity("light.vsc_child",
                                 lambda e:e["state"]=="on" and e["attributes"].get("brightness")==128)
                page=self.open(scheme,"gestures")
                self.wait_cards(("Gesture Overlay",),lambda c:c["icon"]==RED)
                self.wait_cards(("Gesture Hold",),lambda c:c["icon"]==GREEN)
                card=page.locator("bubble-card").nth(self.card_index("Gesture Overlay"))
                state=lambda:card.evaluate("""el => ({
                    open:!!el.card?.querySelector('.bubble-sub-slider-wrapper:not(.is-hidden)'),
                    iconHidden:!!el.card?.querySelector('.bubble-icon-container.is-hidden'),
                    icon:el.card?.querySelector('.bubble-icon')?.style.color||'',
                    owned:!!el.card?._vscOwnedVariables
                })""")
                self.assertFalse(state()["open"],state())
                # Tap opens the native overlay slider in front of the card.
                card.locator(".bubble-sub-button-1").first.click()
                opened=self.wait_value(state,lambda d:d["open"] and d["iconHidden"])
                self.assertTrue(opened["owned"],opened)
                slider=card.locator(".bubble-sub-slider-wrapper .bubble-range-slider").first
                bounds=self.wait_slider_layout(slider,page=page)
                y=bounds["y"]+bounds["height"]/2
                page.mouse.move(bounds["x"]+bounds["width"]*0.2,y)
                page.mouse.down()
                page.mouse.move(bounds["x"]+bounds["width"]*0.85,y,steps=10)
                page.mouse.up()
                self.wait_entity("input_number.vsc_child_brightness",
                                 lambda e:abs(float(e["state"])-128)>=10,timeout=25)
                # The close button collapses it; VSC's colors are intact afterwards.
                card.locator(".bubble-sub-slider-close").first.click()
                closed=self.wait_value(state,lambda d:not d["open"] and not d["iconHidden"])
                self.assertEqual(closed["icon"],RED,closed)
                self.assertTrue(closed["owned"],closed)

                # A real long press fires the card's hold action in HA, with
                # and without VSC (the native card is the harness baseline).
                for name in ("Gesture Hold Native","Gesture Hold"):
                    self.service("input_boolean","turn_on","input_boolean.vsc_child_enabled")
                    self.wait_entity("light.vsc_child",lambda e:e["state"]=="on")
                    hold=page.locator("bubble-card").nth(self.card_index(name))
                    hold.scroll_into_view_if_needed()
                    page.evaluate("""() => {
                        window.__vscEvents=[];
                        const log=ev => window.__vscEvents.push(ev.type+':'+(ev.composedPath()[0]?.className||ev.composedPath()[0]?.localName||'')
                            +(ev.detail?.action?'/'+ev.detail.action:''));
                        for (const t of ['pointerdown','pointerup','click','contextmenu','hass-action','ll-custom','hass-more-info'])
                            window.addEventListener(t,log,{capture:true});
                    }""")
                    box=hold.bounding_box()
                    # Approach the card like a user before pressing: Bubble Card
                    # sets up its action handler on the first pointer contact.
                    page.mouse.move(box["x"]+box["width"]*0.3,box["y"]+box["height"]*0.5)
                    page.mouse.move(box["x"]+box["width"]*0.5,box["y"]+box["height"]*0.5,steps=5)
                    page.wait_for_timeout(400)
                    page.mouse.down()
                    page.wait_for_timeout(1000)
                    page.mouse.up()
                    try:
                        self.wait_entity("light.vsc_child",lambda e:e["state"]=="off",timeout=10)
                    except AssertionError as exc:
                        events=page.evaluate("() => window.__vscEvents")
                        raise AssertionError(f"hold on {name!r} did not fire; events={events}") from exc
                self.shot("gestures_"+scheme)
                self.assertFalse(self.errors,self.errors)

if __name__=="__main__":unittest.main()
