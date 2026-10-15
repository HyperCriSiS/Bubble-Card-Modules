"""Mount the real Bubble Card v3.4.2 custom element in Chromium.
This uses a simulated HA object, NOT a running Home Assistant server.
"""
import re
import faulthandler
from pathlib import Path
import unittest
import yaml
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BUNDLE=ROOT/"artifacts/upstream-bubble-card.js"
OUT=ROOT/"artifacts/vsc-upstream-browser"

def read_styles():
    data=(ROOT/"Visual-Styling-Center/Visual-Styling-Center.md").read_text()
    fence=re.escape(chr(96)*3)
    for m in re.finditer(fence+r"yaml\s*\n(.*?)\n"+fence,data,re.S):
        obj=yaml.safe_load(m.group(1))
        if "code" in obj.get("visual_styling_center",{}):
            return obj["visual_styling_center"]["code"]
    raise ValueError("No executable VSC module found")

class OfficialBubbleCard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert BUNDLE.is_file(), "Verified official Bubble Card bundle is required"
        OUT.mkdir(parents=True,exist_ok=True)
        cls.playwright=sync_playwright().start()
        cls.browser=cls.playwright.chromium.launch(headless=True,args=["--no-sandbox"])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        faulthandler.dump_traceback_later(18, repeat=True)
        print("starting upstream runtime browser",flush=True)
        self.page=self.browser.new_page(viewport={"width":1280,"height":800})
        self.errors=[]
        self.page.on("pageerror",lambda e:self.errors.append(str(e)))
        self.page.on("console",lambda e:self.errors.append(e.text) if e.type=="error" else None)
        self.page.set_content("<!doctype html><style>body{background:#15212a;padding:20px}ha-card{display:block}ha-icon{display:inline-block;width:24px;height:24px}</style><div id=target></div>")
        self.page.evaluate("""() => {
            window.customCards=[];
            window.loadCardHelpers=async()=>({createCardElement:()=>document.createElement('div')});
            customElements.define('ha-card',class extends HTMLElement{});
            customElements.define('ha-icon',class extends HTMLElement{});
            const ent=(id,state,attributes)=>({entity_id:id,state,attributes,
                last_changed:'2026-10-15T10:00:00Z',last_updated:'2026-10-15T10:00:00Z',context:{id:'x'}});
            window.hass={
              states:{
                'light.main':ent('light.main','on',{rgb_color:[255,0,0],brightness:180,friendly_name:'Main'}),
                'light.child':ent('light.child','on',{rgb_color:[0,255,0],brightness:190,friendly_name:'Child'}),
                'light.group':ent('light.group','on',{entity_id:['light.main','light.child'],friendly_name:'Group'})
              },
              config:{components:['light'],time_zone:'UTC',unit_system:{temperature:'°C'},location_name:'CI'},
              themes:{default_theme:'default',themes:{}},locale:{language:'en',number_format:'decimal_dot',time_format:'24'},
              language:'en',selectedLanguage:'en',user:{name:'CI',is_admin:true},
              entities:{},devices:{},areas:{},
              connection:{subscribeEvents:async()=>()=>{},subscribeMessage:async()=>()=>{},sendMessagePromise:async()=>({})},
              callService:async()=>{},callWS:async()=>({}),localize:key=>key,
              formatEntityState:s=>s?.state??'unknown'
            };
            window.changeEntity=(id,state,attributes)=>{
              window.hass={...window.hass,states:{...window.hass.states,
                [id]:{...window.hass.states[id],state,attributes,last_updated:new Date().toISOString()}}};
              window.card.hass=window.hass;
            };
        }""")
        print("loading verified upstream bundle",flush=True)
        self.page.add_script_tag(path=str(BUNDLE),type="module")
        print("script tag added; checking component registration",flush=True)
        self.page.wait_for_function("Boolean(customElements.get('bubble-card'))",timeout=15000)
        print("upstream bubble-card element registered",flush=True)

    def tearDown(self):
        try:
            self.page.screenshot(path=str(OUT/(self._testMethodName+".png")),full_page=True)
        finally:
            self.page.close()
            faulthandler.cancel_dump_traceback_later()

    def mount(self,options):
        print("phase 1: creating custom element",flush=True)
        self.page.evaluate("""() => {
            window.card=document.createElement('bubble-card');
        }""")
        print("phase 2: applying full card configuration",flush=True)
        self.page.evaluate("""input => {
            window.card.setConfig({
              type:'custom:bubble-card',card_type:'button',button_type:'slider',
              entity:'light.main',sub_button:{main:[{entity:'light.child'}]},
              styles:input.styles,visual_styling_center:input.options
            });
        }""",{"styles":read_styles(),"options":options})
        print("phase 3: appending custom element",flush=True)
        self.page.evaluate("() => document.querySelector('#target').append(window.card)")
        print("phase 4: assigning hass snapshot",flush=True)
        self.page.evaluate("() => {window.card.hass=window.hass}")
        print("phase 5: waiting for styles",flush=True)
        self.page.wait_for_timeout(700)
        print("phase 6: mount completed",flush=True)

    def test_actual_renderer_and_state_dependencies(self):
        self.mount({"enable_entity_colored_main_icon":True,"enable_gradient":True,
                    "gradient_target":"background","gradient_entity":"light.group"})
        first=self.page.evaluate("""() => ({
            rendered:!!window.card.card,
            icon:window.card.card?.querySelector('.bubble-icon')?.style.color,
            gradient:window.card.card?.style.getPropertyValue('--card-gradient')
        })""")
        self.assertTrue(first["rendered"],(first,self.errors))
        self.assertEqual(first["icon"],"rgb(255, 0, 0)",(first,self.errors))
        self.assertIn("linear-gradient",first["gradient"],(first,self.errors))
        self.page.evaluate("() => window.changeEntity('light.child','on',{rgb_color:[0,0,255],brightness:190})")
        self.page.wait_for_timeout(350)
        after=self.page.evaluate("() => window.card.card?.style.getPropertyValue('--card-gradient')")
        self.assertNotEqual(first["gradient"],after,(first,after,self.errors))

    def test_actual_card_disconnection_cleanup(self):
        self.mount({"hide_icon_background":True,"manual_icon_background_color":"#123456"})
        before=self.page.evaluate("() => window.card.card?.style.getPropertyValue('--icon-background-color')")
        self.assertEqual(before,"transparent",(before,self.errors))
        self.page.evaluate("() => window.card.remove()")
        after=self.page.evaluate("() => window.card.card?.style.getPropertyValue('--icon-background-color')")
        self.assertEqual(after,"",(after,self.errors))
