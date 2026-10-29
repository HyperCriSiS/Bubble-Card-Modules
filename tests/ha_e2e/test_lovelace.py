"""Real Home Assistant + Lovelace + Bubble Card + VSC browser integration.

Unlike lightweight CSS tests, the HA state, WebSocket updates, native slider
and render lifecycle are not mocked. The only devices are temporary fixtures.
"""
import json
import os
from pathlib import Path
import time
import unittest
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright, expect

BASE=os.environ.get("HA_E2E_BASE","http://127.0.0.1:8123").rstrip("/")
if urlparse(BASE).scheme!="http" or urlparse(BASE).hostname not in {"127.0.0.1","localhost"}:
    raise RuntimeError("HA E2E is restricted to an isolated localhost fixture")
AUTH_FILE=Path(os.environ.get("HA_E2E_AUTH_FILE","/tmp/vsc-ha-e2e-auth.json"))
ARTIFACTS=Path(os.environ.get("HA_E2E_ARTIFACTS","artifacts/vsc-ha-e2e"))

class RealLovelace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.auth=json.loads(AUTH_FILE.read_text(encoding="utf-8"))
        cls.headers={"Authorization":"Bearer "+cls.auth["access_token"]}
        cls.http=requests.Session()
        ARTIFACTS.mkdir(parents=True,exist_ok=True)
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(headless=True,args=["--no-sandbox"])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.http.close()

    @classmethod
    def api(cls,method,path,data=None):
        response=cls.http.request(method,BASE+path,headers=cls.headers,json=data,timeout=20)
        if not response.ok: raise AssertionError(f"HA {method} {path} HTTP {response.status_code}")
        return response.json() if response.content else None

    @classmethod
    def service(cls,domain,action,entity_id,**data):
        return cls.api("POST",f"/api/services/{domain}/{action}",{"entity_id":entity_id,**data})

    @classmethod
    def entity(cls,entity_id):
        return cls.api("GET","/api/states/"+entity_id)

    @classmethod
    def wait_entity(cls,entity_id,predicate,timeout=25):
        deadline=time.monotonic()+timeout
        last=None
        while time.monotonic()<deadline:
            last=cls.entity(entity_id)
            if predicate(last):return last
            time.sleep(0.25)
        raise AssertionError(f"Entity did not update: {entity_id} current={last}")

    def setUp(self):
        self.service("input_boolean","turn_on","input_boolean.vsc_main_enabled")
        self.service("input_boolean","turn_on","input_boolean.vsc_child_enabled")
        for slug,colors in (("main",(255,0,0)),("child",(0,200,20))):
            self.service("input_number","set_value",f"input_number.vsc_{slug}_brightness",value=128)
            for name,v in zip(("red","green","blue"),colors):
                self.service("input_number","set_value",f"input_number.vsc_{slug}_{name}",value=v)
        for slug in ("main","child"):
            self.wait_entity(f"light.vsc_{slug}",lambda e:e["state"]=="on" and e["attributes"].get("brightness")==128)
        self.context=self.browser.new_context(viewport={"width":1280,"height":820})
        # The frontend expects a JSON object, not a JSON-string containing JSON.
        tokens=json.dumps(self.auth,separators=(",",":"))
        self.context.add_init_script(script=f"""
            if (location.origin === {json.dumps(BASE)}) {{
                localStorage.setItem('hassTokens', {json.dumps(tokens)});
            }}
        """)
        self.page=self.context.new_page()
        self.errors=[]
        self.page.on("pageerror",lambda e:self.errors.append(str(e)))
        self.page.goto(BASE+"/lovelace-vsc-e2e/vsc",wait_until="domcontentloaded",timeout=65000)
        try:
            expect(self.page.locator("bubble-card")).to_have_count(4,timeout=65000)
            expect(self.page.locator("bubble-card").first.locator(".bubble-icon")).to_be_attached(timeout=45000)
        except Exception as exc:
            try: body=self.page.locator("body").inner_text(timeout=4000)[:800]
            except Exception: body="<unavailable>"
            raise AssertionError(f"HA dashboard failed: url={self.page.url} body={body!r} JS={self.errors}") from exc

    def tearDown(self):
        try:
            self.page.screenshot(path=str(ARTIFACTS/(self._testMethodName+".png")),full_page=True,timeout=12000)
        finally:
            self.context.close()

    def card_data(self,index=0):
        return self.page.locator("bubble-card").nth(index).evaluate("""el => ({
            icon:el.card?.querySelector('.bubble-icon')?.style.color || '',
            gradient:el.card?.style.getPropertyValue('--card-gradient') || '',
            inner:Boolean(el.content),
            subCount:el.card?.querySelectorAll('.bubble-sub-button-icon')?.length||0,
            subSliderCount:el.card?.querySelectorAll('.bubble-sub-button-slider')?.length||0,
            range:el.card?.querySelector('.bubble-range-fill')?.getBoundingClientRect().width||0
        })""")

    def wait_value(self,getter,predicate,timeout=20):
        deadline=time.monotonic()+timeout
        last=None
        while time.monotonic()<deadline:
            last=getter()
            if predicate(last):return last
            self.page.wait_for_timeout(180)
        raise AssertionError(f"Browser did not update, last={last!r}; JS errors={self.errors}")

    def test_01_actual_renderer_and_native_slider(self):
        data=self.card_data()
        self.assertTrue(data["inner"],data)
        self.assertGreater(data["range"],0,data)
        # Always-visible sub-sliders are rendered without a host icon in
        # Bubble Card v3.4.2; the real control uses .bubble-sub-button-slider.
        self.assertGreaterEqual(data["subSliderCount"],1,data)
        self.assertIn("linear-gradient",data["gradient"],data)
        self.assertEqual(data["icon"],"rgb(255, 0, 0)",data)

    def test_02_external_main_state_update(self):
        self.service("input_boolean","turn_off","input_boolean.vsc_main_enabled")
        self.wait_entity("light.vsc_main",lambda e:e["state"]=="off")
        self.wait_value(lambda:self.card_data()["icon"],lambda c:c=="rgb(150, 150, 150)")
        self.service("input_boolean","turn_on","input_boolean.vsc_main_enabled")
        self.wait_entity("light.vsc_main",lambda e:e["state"]=="on")
        self.wait_value(lambda:self.card_data()["icon"],lambda c:c=="rgb(255, 0, 0)")

    def test_03_child_rgb_websocket_updates_gradient(self):
        before=self.card_data()["gradient"]
        self.assertIn("linear-gradient",before)
        self.service("input_number","set_value","input_number.vsc_child_blue",value=230)
        self.service("input_number","set_value","input_number.vsc_child_green",value=10)
        self.wait_entity("light.vsc_child",lambda e:e["attributes"].get("rgb_color",[None]*3)[2]==230)
        self.wait_value(lambda:self.card_data()["gradient"],lambda v:bool(v) and v!=before)

    def wait_slider_layout(self, slider, page=None):
        """Wait until the actual rendered native control stops shifting.

        A non-zero box alone can be a transitional frame (card load/animation).
        We do not retry a failed drag or suppress a failed HA service assertion.
        """
        viewport_page = page or self.page
        expect(slider).to_be_visible(timeout=15000)
        slider.scroll_into_view_if_needed(timeout=10000)
        def box():
            return slider.bounding_box()
        previous=box()
        end=time.monotonic()+5
        while time.monotonic()<end:
            viewport_page.wait_for_timeout(160)
            current=box()
            if previous and current and all(
                abs(current[key]-previous[key])<1 for key in ("x","y","width","height")
            ) and current["width"]>15 and current["height"]>2:
                return current
            previous=current
        raise AssertionError(f"Native slider layout is not stable: {previous}")

    def test_04_native_slider_pointer_drives_ha_service(self):
        slider=self.page.locator("bubble-card").first.locator(".bubble-range-slider").first
        box=self.wait_slider_layout(slider)
        self.assertIsNotNone(box,"Native slider is not laid out")
        y=box["y"]+box["height"]/2
        self.page.mouse.move(box["x"]+box["width"]*0.32,y)
        self.page.mouse.down()
        self.page.mouse.move(box["x"]+box["width"]*0.82,y,steps=10)
        self.page.mouse.up()
        self.wait_entity("input_number.vsc_main_brightness",
                         lambda e:abs(float(e["state"])-128)>=10)

    def test_05_original_bubble_card_without_vsc(self):
        data=self.card_data(1)
        self.assertTrue(data["inner"],data)
        self.assertGreater(data["range"],0,data)
        self.assertGreaterEqual(data["subSliderCount"],1,data)

    def test_06_navigation_and_reconnection(self):
        self.page.goto(BASE+"/lovelace-vsc-e2e/away",wait_until="domcontentloaded")
        expect(self.page.get_by_text("Lifecycle navigation target")).to_be_visible(timeout=25000)
        self.page.goto(BASE+"/lovelace-vsc-e2e/vsc",wait_until="domcontentloaded")
        expect(self.page.locator("bubble-card")).to_have_count(4,timeout=45000)
        self.wait_value(lambda:self.card_data()["icon"],lambda v:v=="rgb(255, 0, 0)")

if __name__=="__main__":unittest.main()
