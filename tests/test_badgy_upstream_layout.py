#!/usr/bin/env python3
"""Chromium smoke tests using Bubble Card's mirrored v3.4.2 base CSS.

DOM nesting follows upstream src/components/base-card/create.js. This is not a
live Home Assistant instance, editor or full custom-card runtime.
"""
from pathlib import Path
import os
import shutil
import unittest

import yaml
from playwright.sync_api import sync_playwright
from test_badgy_browser import BOOT, MODULE

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "docs/upstream/bubble-card/stable/src/components/base-card/styles.css"
BETA = ROOT / "Badgy-Conditions/Badgy-Conditions-beta.yaml"

DOM = '''<meta name="viewport" content="width=device-width, initial-scale=1">
<div style="width:300px;margin:60px"><div class="bubble-button-container bubble-container" id="card">
 <div class="bubble-button bubble-wrapper">
  <div class="bubble-content-container">
   <div class="bubble-main-icon-container bubble-icon-container"><ha-icon icon="mdi:home" class="bubble-main-icon bubble-icon"></ha-icon></div>
   <div class="bubble-name-container"><div class="bubble-name">Kitchen</div></div>
  </div>
  <div class="bubble-buttons-container"></div>
  <div class="bubble-sub-button-container">
   <div class="bubble-sub-button bubble-sub-button-1"><ha-icon class="bubble-sub-button-icon" icon="mdi:fan"></ha-icon><span id="foreign" class="bubble-sub-button-badge entity-badge">Foreign</span></div>
   <div class="bubble-sub-button-group"><div class="bubble-sub-button bubble-sub-button-2"><ha-icon class="bubble-sub-button-icon"></ha-icon></div></div>
  </div>
 </div>
</div></div>'''


class UpstreamLayoutTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        obj = yaml.safe_load(BETA.read_text(encoding="utf8"))
        cls.code = obj[MODULE]["code"]
        cls.css = UPSTREAM.read_text(encoding="utf8")
        assert "overflow: clip;" in cls.css
        assert ".bubble-icon-container {" in cls.css
        cls.playwright = sync_playwright().start()
        executable = next((str(p) for p in (
            os.environ.get("CHROMIUM_EXECUTABLE"), shutil.which("chromium"),
            shutil.which("google-chrome"), shutil.which("google-chrome-stable"))
            if p and Path(p).exists()), None)
        cls.browser = cls.playwright.chromium.launch(
            headless=True, executable_path=executable, args=["--no-sandbox"])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page(viewport={"width": 440, "height": 260})
        self.errors = []
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))
        variables = ":root {--primary-color:#03a9f4;--red-color:red;--blue-color:blue;--card-background-color:#333;--primary-text-color:#222;--secondary-background-color:#eee}"
        self.page.set_content("<style>" + variables + self.css + "</style>" + DOM)
        self.page.evaluate(BOOT, [self.code, MODULE])

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.page.close()

    def test_actual_container_selectors_and_clip_margin(self):
        details = self.page.evaluate("""() => {
         const card=document.querySelector('#card'),icon=card.querySelector('.bubble-icon-container');
         const badge=icon.querySelector('.badgy-owned-badge.entity-badge');
         return {mainClasses:icon.className,cardOverflow:getComputedStyle(card).overflow,
                 clipMargin:getComputedStyle(card).overflowClipMargin,
                 iconOverflow:getComputedStyle(icon).overflow,
                 badgeBg:getComputedStyle(badge).backgroundColor}; }""")
        self.assertIn("bubble-main-icon-container", details["mainClasses"])
        self.assertEqual(details["cardOverflow"], "clip")
        self.assertEqual(details["clipMargin"], "16px")
        self.assertEqual(details["iconOverflow"], "visible")
        self.assertEqual(details["badgeBg"], "rgb(3, 169, 244)")

        # Badge edge protrudes beyond the card, where a normal clip would hide it.
        result = self.page.evaluate("""() => {
         window.fixture.cfg.entity_badges.main.v_pos=-8;window.fixture.run();
         const card=document.querySelector('#card');
         const badge=card.querySelector('.bubble-icon-container .badgy-owned-badge.entity-badge');
         const rect=badge.getBoundingClientRect(),parent=card.getBoundingClientRect();
         const before=badge.style.pointerEvents;badge.style.pointerEvents='auto';
         const hit=document.elementFromPoint(rect.left+rect.width/2,parent.top-1)===badge;
         badge.style.pointerEvents=before;
         return {top:rect.top,cardTop:parent.top,hit}; }""")
        self.assertLess(result["top"], result["cardTop"])
        self.assertTrue(result["hit"], str(result))

    def test_badges_do_not_break_native_button_clicks(self):
        result = self.page.evaluate("""() => {
         let clicks=0;const sub=document.querySelector('.bubble-sub-button-1');
         sub.addEventListener('click',()=>clicks++);
         const badge=sub.querySelector('.badgy-owned-badge.entity-badge');
         const style=getComputedStyle(badge),r=badge.getBoundingClientRect();
         document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.click();
         return {clicks,pointer:style.pointerEvents,foreign:document.querySelector('#foreign').textContent}; }""")
        self.assertEqual(result["pointer"], "none")
        self.assertEqual(result["clicks"], 1)
        self.assertEqual(result["foreign"], "Foreign")

    def test_temporary_position_restored_when_last_badge_hides(self):
        status = self.page.evaluate("""() => {
         const group=document.querySelector('.bubble-sub-button-2');
         group.style.setProperty('position','static');
         window.fixture.cfg.entity_badges['1']={entity:'sensor.power'};
         window.fixture.run();
         const during=group.style.getPropertyValue('position');
         delete window.fixture.cfg.entity_badges['1'];
         window.fixture.run();
         return {during,after:group.style.getPropertyValue('position'),
                 badges:group.querySelectorAll('.badgy-owned-badge').length}; }""")
        self.assertEqual(status["during"], "relative")
        self.assertEqual(status["after"], "static")
        self.assertEqual(status["badges"], 0)

    def test_normal_and_large_layout_badge_rendering(self):
        for mode in ("normal", "large"):
            self.page.evaluate(
                '(mode)=>document.body.classList.toggle("large",mode==="large")', mode)
            data = self.page.evaluate("""() => {
             window.fixture.run();const card=document.querySelector('#card');
             const b=card.querySelector('.bubble-icon-container .badgy-owned-badge.entity-badge');
             return {visible:getComputedStyle(b).display!=='none',
                     width:b.getBoundingClientRect().width}; }""")
            self.assertTrue(data["visible"], mode)
            self.assertGreater(data["width"], 15, mode)


if __name__ == "__main__":
    unittest.main(verbosity=2)
