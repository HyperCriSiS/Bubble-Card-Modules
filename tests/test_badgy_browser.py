#!/usr/bin/env python3
"""Chromium smoke tests with a synthetic Bubble Card DOM (not a real HA UI)."""
import os
import shutil
import unittest
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MODULE = 'badgy-condition-helper-beta'
HTML = '''<!doctype html><style>
:root {--red-color:red; --blue-color:blue; --primary-color:#09f}
.bubble-container {position:relative;width:320px;height:130px;overflow:clip}
.bubble-icon-container {position:relative;width:50px;height:50px;display:inline-flex}
.bubble-sub-button-1,.bubble-sub-button-2 {position:relative;width:70px;height:40px;display:inline-flex}
ha-icon {display:inline-block;width:24px;height:24px}
</style><div class="bubble-container" id="card"><div class="bubble-button-card-container">
<div class="bubble-main-icon-container bubble-icon-container"><ha-icon class="bubble-icon" icon="mdi:home"></ha-icon></div>
<div class="bubble-sub-button-1"><ha-icon class="bubble-sub-button-icon" icon="mdi:fan"></ha-icon>
<span id="foreign" class="bubble-sub-button-badge entity-badge">Foreign</span></div>
<div class="bubble-sub-button-group"><div class="bubble-sub-button-2"><ha-icon class="bubble-sub-button-icon"></ha-icon></div></div>
</div></div>'''
BOOT = '''([code,id]) => {
 const card=document.querySelector('#card');
 const state=(entity_id,state,attributes={})=>({entity_id,state,attributes});
 const hass={states:{'sensor.power':state('sensor.power','25',{unit_of_measurement:'W'}),
 'binary_sensor.window':state('binary_sensor.window','on'),
 'sensor.flag':state('sensor.flag','on')},
 formatEntityState:s=>s.state==='on'?'Open':'Closed'};
 const active={condition:'state',entity_id:'sensor.flag',state:'on'};
 const cfg={entity_badges:{'0':{entity:'sensor.power',scale:1.6,color:'red'},
 main:{entity:'binary_sensor.window'}},icon_badges:{main:{icon:'mdi:alert',show_background:false}},
 icon_effects:{sub_button_icon:{'0':{effect:'spin-360',condition:active}}},
 sub_buttons_background:{'0':{type:'solid',color:'blue',opacity:0.5}},
 icons:{main_icon:{icon:'mdi:flash',condition:active}}};
 const ctx={config:{[id]:cfg}},memo=new Map();let cleanup;
 const template=new Function('hass','entity','state','card','checkConditionsMet',
 'renderTemplate','hasChanged','onTeardown','return '+String.fromCharCode(96)+code+String.fromCharCode(96)+';');
 const check=a=>a.every(c=>c.condition==='state' && hass.states[c.entity_id]?.state===c.state);
 // Same string signature as Bubble Card 3.4.2 module-gate.js.
 const changed=(name,...values)=>{
  const sig=values.map(v=>Array.isArray(v)?v.join(','):(v==null?'':String(v))).join('\u0001');
  if(memo.get(name)===sig)return false;memo.set(name,sig);return true;};
 const styles=document.createElement('style');document.head.append(styles);
 const run=()=>{styles.textContent=template.call(ctx,hass,'sensor.power',hass.states['sensor.power'].state,
  card,check,x=>x,changed,fn=>cleanup=fn)};
 window.fixture={card,hass,cfg,run,teardown:()=>cleanup?.()};run();
}'''


class BadgyBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        obj=yaml.safe_load((ROOT/'Badgy-Conditions/Badgy-Conditions-beta.yaml').read_text(encoding='utf-8'))
        cls.code=obj[MODULE]['code']
        cls.playwright=sync_playwright().start()
        executable=next((str(p) for p in (
            os.environ.get('CHROMIUM_EXECUTABLE'),shutil.which('chromium'),
            shutil.which('google-chrome'),shutil.which('google-chrome-stable'))
            if p and Path(p).exists()),None)
        cls.browser=cls.playwright.chromium.launch(headless=True, executable_path=executable,
                                                     args=['--no-sandbox'])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page=self.browser.new_page(viewport={'width':375,'height':720})
        self.errors=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.on('console',lambda m:self.errors.append(m.text) if m.type == 'error' else None)
        self.page.set_content(HTML)
        self.page.evaluate(BOOT,[self.code,MODULE])

    def tearDown(self):
        self.assertFalse(self.errors,f'Browser errors: {self.errors}')
        self.page.close()

    def test_badge_style_and_foreign_isolation(self):
        result=self.page.evaluate('''() => {
        const card=window.fixture.card,main=card.querySelector('.bubble-icon-container'),
        sub=card.querySelector('.bubble-sub-button-1'),badge=sub.querySelector('.badgy-owned-badge.entity-badge'),
        mainBadge=main.querySelector('.badgy-owned-badge.entity-badge'),
        iconBadge=main.querySelector('.badgy-owned-badge.icon-badge');
        return {foreign:document.querySelector('#foreign').textContent,
        foreignOwned:document.querySelector('#foreign').classList.contains('badgy-owned-badge'),
        foreignPosition:getComputedStyle(document.querySelector('#foreign')).position,
        text:badge.textContent,height:parseFloat(getComputedStyle(badge).height),
        color:getComputedStyle(badge).backgroundColor,main:mainBadge.textContent,
        iconBg:getComputedStyle(iconBadge).backgroundColor,
        overflow:getComputedStyle(main).overflow,clip:getComputedStyle(card).overflowClipMargin,
        background:sub.style.background,computedBackground:getComputedStyle(sub).backgroundColor,
        opacity:getComputedStyle(sub).opacity};}''')
        self.assertEqual(result['foreign'],'Foreign')
        self.assertFalse(result['foreignOwned'])
        self.assertNotEqual(result['foreignPosition'],'absolute')
        self.assertEqual(result['text'],'25W')
        self.assertAlmostEqual(result['height'],25.6,delta=.05)
        self.assertEqual(result['color'],'rgb(255, 0, 0)')
        self.assertEqual(result['main'],'Open')
        self.assertEqual(result['iconBg'],'rgba(0, 0, 0, 0)')
        self.assertEqual(result['overflow'],'visible')
        self.assertEqual(result['clip'],'16px')
        self.assertIn('color-mix(',result['background'])
        self.assertIn('/ 0.5',result['computedBackground'],
                      'Background transparency must render in Chromium, not just parse')
        self.assertEqual(result['opacity'],'1')

    def test_real_animation_stop_and_icon_restoration(self):
        icon='.bubble-sub-button-1 .bubble-sub-button-icon'
        self.assertEqual(self.page.evaluate(f"getComputedStyle(document.querySelector('{icon}')).animationName"),
                         'badgy-spin360')
        self.page.evaluate("window.fixture.hass.states['sensor.flag'].state='off';window.fixture.run()")
        self.assertEqual(self.page.evaluate(f"getComputedStyle(document.querySelector('{icon}')).animationName"),'none')
        self.assertEqual(self.page.locator('.bubble-icon').get_attribute('icon'),'mdi:home')

    def test_dynamic_updates_and_teardown(self):
        self.page.evaluate("""() => {
          const sub=window.fixture.card.querySelector('.bubble-sub-button-1');
          const badge=sub.querySelector('.badgy-owned-badge.entity-badge');
          for (let i=0;i<60;i++) {
            window.fixture.hass.states['sensor.power'].state=String(i);
            window.fixture.run();
            if (sub.querySelector('.badgy-owned-badge.entity-badge')!==badge)
              throw new Error('Sensor updates must reuse the exact badge DOM node');
          }
        }""")
        self.assertEqual(self.page.locator('.bubble-sub-button-1 .badgy-owned-badge.entity-badge').text_content(),'59W')
        # A card may rebuild an individual badge while its entity is unchanged.
        self.page.evaluate("""() => {
          const badge=window.fixture.card.querySelector('.bubble-sub-button-1 .badgy-owned-badge.entity-badge');
          badge.remove();
          window.fixture.run();
        }""")
        self.assertEqual(self.page.locator('.bubble-sub-button-1 .badgy-owned-badge.entity-badge').text_content(),'59W')
        self.page.evaluate('window.fixture.teardown()')
        self.assertEqual(self.page.locator('.badgy-owned-badge').count(),0)
        self.assertEqual(self.page.locator('#foreign').text_content(),'Foreign')
        self.assertEqual(self.page.locator('.bubble-icon').get_attribute('icon'),'mdi:home')


if __name__=='__main__':
    unittest.main(verbosity=2)
