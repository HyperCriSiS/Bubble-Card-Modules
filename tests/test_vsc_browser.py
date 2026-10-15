"""Chromium/CSS integration tests using mirrored Bubble Card v3.4.2 CSS.

The DOM and Home Assistant state are simulated. These are not live HA E2E tests.
"""
import os
import re
import unittest
from pathlib import Path
import yaml
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "docs/upstream/bubble-card/stable/src"
OUT = ROOT / "artifacts/vsc-browser"
CSS_FILES = [REF / x for x in (
    "components/base-card/styles.css", "cards/button/styles.css",
    "components/sub-button/styles.css")]
HTML = """<!doctype html><meta charset=utf-8>
<style id=native></style><style id=module></style>
<style>
body{background:#20232a;color:white;padding:20px;font-family:Arial}
#card{--row-height:56px;--row-size:2;--row-gap:8px;--accent-color:rgb(60,140,220);--bubble-accent-color:rgb(60,140,220);max-width:700px;position:relative}
.bubble-button-card-container{position:relative;display:flex;align-items:center;overflow:visible}
.bubble-button-card{position:relative;display:flex;align-items:center;min-width:100%;z-index:1}
.bubble-name-container{flex:1;min-width:60px}
.bubble-sub-button-container,.bubble-sub-button-bottom-container{display:flex;gap:8px}
.bubble-range-fill{position:absolute;left:0;top:0;width:40%;height:100%;background:rgb(60,140,220)}
.bubble-range-slider{position:absolute;left:0;top:0;width:100%;height:100%;z-index:0}
ha-icon{display:inline-block;width:24px;height:24px}
</style>
<div id=card><div class='bubble-container bubble-button-card-container'>
<div class=bubble-range-slider><div id=fill class=bubble-range-fill></div></div>
<div class='bubble-wrapper bubble-button-card'>
<div class=bubble-icon-container><ha-icon class='bubble-icon bubble-main-icon' id=main>●</ha-icon></div>
<div class=bubble-name-container>Sample Light</div>
<div class=bubble-sub-button-container>
<div class='bubble-sub-button bubble-sub-button-1 background-on bright-background'><ha-icon class=bubble-sub-button-icon id=sub1>●</ha-icon></div>
<div class='bubble-sub-button bubble-sub-button-2'><ha-icon class=bubble-sub-button-icon id=sub2>●</ha-icon></div>
<div class=bubble-sub-button-slider><div class=bubble-range-slider><div id=subfill class=bubble-range-fill style='background-color:rgb(24,48,96)'></div></div></div>
</div><div class=bubble-sub-button-bottom-container>
<div class='bubble-sub-button bubble-sub-button-3'><ha-icon class=bubble-sub-button-icon id=sub3>●</ha-icon></div>
</div></div></div></div>"""

def module_parts():
    text = (ROOT / "Visual-Styling-Center/Visual-Styling-Center.md").read_text()
    fence = re.escape(chr(96)*3)
    blocks = (yaml.safe_load(m.group(1)) for m in re.finditer(fence+r"yaml\s*\n(.*?)\n"+fence, text, re.S))
    code = next(b["visual_styling_center"]["code"] for b in blocks
                if isinstance(b, dict) and "code" in b.get("visual_styling_center", {}))
    start, stop = code.index(chr(36)+chr(123)+"(() => {"), code.index("})()}") + 5
    return code[start+2:stop-1], code[stop:]

class VSCBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert all(p.is_file() for p in CSS_FILES), "Bubble Card snapshot is missing"
        cls.expr, cls.css = module_parts()
        cls.native = "\n".join(p.read_text() for p in CSS_FILES)
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True, args=["--no-sandbox"],
                                             executable_path=os.environ.get("VSC_CHROMIUM_PATH"))
        OUT.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.page = self.browser.new_page(viewport={"width":1280,"height":800})
        self.errors = []
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))
        self.page.set_content(HTML)
        self.page.locator("#native").evaluate("(e,v)=>e.textContent=v", self.native)
        self.page.locator("#module").evaluate("(e,v)=>e.textContent=v", self.css)
        self.page.evaluate("""expr => {
            window.runner = new Function('card','hass','hasChanged','return '+expr+';');
            window.cfg={entity:'light.main',visual_styling_center:{},sub_button:{
                main:[{group:[{entity:'light.first'},{entity:'light.second'}]}],
                bottom:[{entity:'light.main'}]}};
            window.hass={states:{
                'light.main':{state:'on',attributes:{rgb_color:[255,0,0]}},
                'light.first':{state:'on',attributes:{rgb_color:[0,255,0]}},
                'light.second':{state:'off',attributes:{}},
                'light.group':{state:'on',attributes:{entity_id:['light.first','light.second']}}
            }};
            window.gradientGates=new Map();
            window.hasChanged=(key,...values)=>{
                const sig=JSON.stringify(values),old=window.gradientGates.get(key);
                window.gradientGates.set(key,sig);
                return old!==sig;
            };
            window.render=()=>window.runner.call({config:window.cfg},document.querySelector('#card'),window.hass,window.hasChanged);
            window.render();
        }""", self.expr)

    def tearDown(self):
        try:
            self.assertFalse(self.errors, self.errors)
        finally:
            self.page.screenshot(path=str(OUT / (self._testMethodName+".png")), full_page=True)
            self.page.close()

    def change(self, cfg=None, states=None, classes=None):
        self.page.evaluate("""data=>{
            Object.assign(window.cfg.visual_styling_center,data.cfg||{});
            Object.assign(window.hass.states,data.states||{});
            for(const [k,v] of Object.entries(data.classes||{})) document.querySelector('#card').classList.toggle(k,v);
            window.render();
        }""", {"cfg":cfg,"states":states,"classes":classes})

    def cssval(self, selector, key):
        return self.page.locator(selector).evaluate("(e,k)=>getComputedStyle(e).getPropertyValue(k).trim()", key)

    def test_card_scaling_and_large_layout(self):
        self.assertEqual(self.cssval('.bubble-icon-container','width'),'38px')
        self.change(cfg={'height_multiplier':2,'icon_size_multiplier':1.5,'subbutton_background_ratio':1.25})
        self.assertEqual(self.cssval('.bubble-button-card-container','height'),'100px')
        self.assertEqual(self.cssval('.bubble-icon-container','width'),'57px')
        # Native Bubble Card animates sub-button geometry for 0.5 s.
        self.page.wait_for_timeout(650)
        self.assertEqual(self.cssval('.bubble-sub-button-1','height'),'80px')
        self.change(classes={'large':True})
        self.assertEqual(self.cssval('.bubble-icon-container','width'),'63px')
        self.assertEqual(self.cssval('.bubble-button-card-container','height'),'232px')

    def test_external_state_changes_and_cleanup(self):
        self.change(cfg={'enable_entity_colored_main_icon':True,'enable_entity_colored_subicons':True})
        self.page.wait_for_timeout(400)
        self.assertEqual(self.cssval('#main','color'),'rgb(255, 0, 0)')
        self.assertEqual(self.cssval('#sub1','color'),'rgb(0, 255, 0)')
        self.change(states={'light.main':{'state':'off','attributes':{}},
                            'light.first':{'state':'unavailable','attributes':{}}})
        self.page.wait_for_timeout(400)
        self.assertEqual(self.cssval('#main','color'),'rgb(150, 150, 150)')
        self.assertEqual(self.cssval('#sub1','color'),'rgb(180, 180, 180)')
        self.change(cfg={'enable_entity_colored_main_icon':False,'enable_entity_colored_subicons':False})
        self.assertEqual(self.page.locator('#main').evaluate('e=>e.style.color'),'')
        self.assertEqual(self.page.locator('#sub1').evaluate('e=>e.style.color'),'')

    def test_gradient_switch_and_child_state(self):
        self.change(cfg={'enable_gradient':True,'gradient_target':'slider','gradient_entity':'light.group'})
        self.assertIn('linear-gradient',self.cssval('#fill','background-image'))
        self.change(cfg={'gradient_target':'background'})
        before=self.cssval('.bubble-button-card','background-image')
        self.assertIn('linear-gradient',before)
        self.change(states={'light.second':{'state':'on','attributes':{'rgb_color':[0,0,255]}}})
        self.assertNotEqual(self.cssval('.bubble-button-card','background-image'),before)
        self.change(cfg={'enable_gradient':False})
        self.assertEqual(self.cssval('.bubble-button-card','background-image'),'none')

    def test_background_hide_and_restore(self):
        self.change(cfg={'manual_icon_background_color':'#123456'})
        self.assertEqual(self.cssval('.bubble-icon-container','background-color'),'rgb(18, 52, 86)')
        self.change(cfg={'hide_icon_background':True,'hide_subbutton_background':True})
        self.page.wait_for_timeout(650)
        self.assertEqual(self.cssval('.bubble-icon-container','background-color'),'rgba(0, 0, 0, 0)')
        self.assertEqual(self.cssval('.bubble-sub-button-1','background-color'),'rgba(0, 0, 0, 0)')
        self.change(cfg={'hide_icon_background':False,'hide_subbutton_background':False})
        self.page.wait_for_timeout(650)
        self.assertEqual(self.cssval('.bubble-icon-container','background-color'),'rgb(18, 52, 86)')
        self.change(cfg={'enable_gradient':True,'gradient_target':'background','enable_slider_helper':True})
        self.assertIn('rgb',self.cssval('#fill','box-shadow'))

    def test_contrast_helper_and_mobile_spacing(self):
        self.change(cfg={'enable_icon_helper':True,'enable_helper_fade':False,'helper_color':[90,100,110],'helper_opacity':0.25})
        self.assertEqual(self.page.locator('#main').evaluate("e=>getComputedStyle(e,'::before').content"),'""')
        self.assertIn('0.25',self.page.locator('#main').evaluate("e=>getComputedStyle(e,'::before').backgroundColor"))
        self.page.set_viewport_size({'width':390,'height':844})
        self.change(cfg={'subbutton_column_spacing':12})
        self.assertEqual(self.cssval('.bubble-sub-button-container','column-gap'),'12px')

    def test_native_slider_restored_when_gradient_disabled(self):
        self.assertEqual(self.cssval('#fill','background-image'),'none')
        self.change(cfg={'enable_gradient':True,'gradient_target':'slider','gradient_entity':'light.main'})
        self.assertIn('linear-gradient',self.cssval('#fill','background-image'))
        self.change(cfg={'enable_gradient':False})
        self.assertEqual(self.cssval('#fill','background-image'),'none')
        self.assertNotEqual(self.cssval('#fill','background-color'),'rgba(0, 0, 0, 0)')


    def test_subslider_keeps_native_v342_colors(self):
        # Main gradient must never restyle a nested sub-slider fill.
        self.assertEqual(self.cssval('#subfill', 'background-color'), 'rgb(24, 48, 96)')
        self.page.wait_for_timeout(650)
        native_height = self.cssval('#subfill', 'height')
        self.change(cfg={'enable_gradient':True,'gradient_target':'slider','gradient_entity':'light.main'})
        self.assertIn('linear-gradient', self.cssval('#fill','background-image'))
        self.assertEqual(self.cssval('#subfill', 'background-image'), 'none')
        self.assertEqual(self.cssval('#subfill','background-color'), 'rgb(24, 48, 96)')
        self.change(cfg={'gradient_target':'background','enable_slider_helper':True})
        self.page.wait_for_timeout(650)
        self.assertAlmostEqual(float(self.cssval('#subfill','height').removesuffix('px')),float(native_height.removesuffix('px')),delta=0.1)
        self.assertEqual(self.cssval('#subfill','background-color'), 'rgb(24, 48, 96)')

    def test_subbutton_native_background_except_explicit_override(self):
        self.page.wait_for_timeout(650)
        native = self.cssval('.bubble-sub-button-1','background-color')
        self.assertEqual(native, 'rgb(60, 140, 220)')
        self.change(cfg={'manual_subbutton_background_color':'#123456'})
        self.page.wait_for_timeout(650)
        self.assertEqual(self.cssval('.bubble-sub-button-1','background-color'),'rgb(18, 52, 86)')
        self.change(cfg={'manual_subbutton_background_color':''})
        self.page.wait_for_timeout(650)
        self.assertEqual(self.cssval('.bubble-sub-button-1','background-color'),native)
