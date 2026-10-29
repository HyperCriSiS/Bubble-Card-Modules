"""Real HA persistence, long-run stability and physical editor interaction.

* A storage-mode dashboard is saved through HA's own lovelace/config/save
  WebSocket command and reloaded from the HA backend.
* Many state changes and navigations must not leak styles or VSC state.
* Every VSC field of the real Bubble Card v3.4.2 editor (schema from Bubble
  Card Tools) is operated with real mouse clicks and keyboard input.
"""
from pathlib import Path
import time

import test_lovelace as base
from generate_fixture import MODULE_ID, extract_module
from playwright.sync_api import expect

ROOT=Path(__file__).resolve().parents[2]
DASHBOARD="vsc-storage"
RED="rgb(255, 0, 0)"

READ_CARD="""el => ({
    owned:!!el.card?._vscOwnedVariables,
    ownedCount:el.card?._vscOwnedVariables?.size ?? 0,
    icon:el.card?.querySelector('.bubble-icon')?.style.color||'',
    styles:(el.shadowRoot?.querySelectorAll('style').length||0)
          +(el.card?.querySelectorAll('style').length||0)
})"""

def module_code():
    return extract_module((ROOT/"Visual-Styling-Center/Visual-Styling-Center.md").read_text(encoding="utf-8"))

def flat_fields(items):
    for item in items or []:
        if "name" in item: yield item
        else: yield from flat_fields(item.get("schema"))


class PersistenceAndEditor(base.RealLovelace):
    test_01_actual_renderer_and_native_slider = None
    test_02_external_main_state_update = None
    test_03_child_rgb_websocket_updates_gradient = None
    test_04_native_slider_pointer_drives_ha_service = None
    test_05_original_bubble_card_without_vsc = None
    test_06_navigation_and_reconnection = None

    def ws(self,message):
        return self.page.evaluate("""async msg => {
            try { return {ok:true,result:await document.querySelector('home-assistant').hass.callWS(msg)}; }
            catch (error) { return {ok:false,error:JSON.stringify(error)}; }
        }""",message)

    def ensure_storage_dashboard(self):
        listed=self.ws({"type":"lovelace/dashboards/list"})
        self.assertTrue(listed["ok"],listed)
        if not any(d["url_path"]==DASHBOARD for d in listed["result"]):
            created=self.ws({"type":"lovelace/dashboards/create","url_path":DASHBOARD,"title":"VSC storage",
                             "mode":"storage","require_admin":False,"show_in_sidebar":False})
            self.assertTrue(created["ok"],created)

    def save_card(self,card):
        config={"title":"VSC storage","views":[{"title":"Stored","path":"stored","cards":[card]}]}
        saved=self.ws({"type":"lovelace/config/save","url_path":DASHBOARD,"config":config})
        self.assertTrue(saved["ok"],saved)

    def stored_card(self):
        loaded=self.ws({"type":"lovelace/config","url_path":DASHBOARD,"force":True})
        self.assertTrue(loaded["ok"],loaded)
        return loaded["result"]["views"][0]["cards"][0]

    def open_stored(self,reload=False):
        if reload: self.page.reload(wait_until="domcontentloaded")
        else: self.page.goto(base.BASE+"/"+DASHBOARD+"/stored",wait_until="domcontentloaded")
        card=self.page.locator("bubble-card").first
        expect(card).to_be_attached(timeout=45000)
        return card

    def test_27_lovelace_save_and_reload_persist_vsc(self):
        options={"enable_entity_colored_main_icon":True,"enable_entity_colored_subicons":False,
                 "inner_padding":7,"card_background_opacity":0,"custom_card_background_color":[10,20,30]}
        card={"type":"custom:bubble-card","card_type":"button","button_type":"slider",
              "entity":"light.vsc_main","name":"Stored VSC","styles":module_code()["code"],MODULE_ID:options}
        self.ensure_storage_dashboard()
        self.save_card(card)
        element=self.open_stored()
        data=self.wait_value(lambda:element.evaluate(READ_CARD),lambda d:d["icon"]==RED)
        self.assertTrue(data["owned"],data)
        element=self.open_stored(reload=True)
        self.wait_value(lambda:element.evaluate(READ_CARD),lambda d:d["icon"]==RED)
        # Zero, false and the RGB list survive HA's own storage round trip.
        self.assertEqual(self.stored_card()[MODULE_ID],options)

        changed=dict(options,enable_entity_colored_main_icon=False)
        self.save_card(dict(card,**{MODULE_ID:changed}))
        element=self.open_stored(reload=True)
        data=self.wait_value(lambda:element.evaluate(READ_CARD),lambda d:d["owned"])
        self.page.wait_for_timeout(600)
        # Bubble Card's own icon color is back instead of VSC's entity color.
        icon=element.evaluate(READ_CARD)["icon"]
        self.assertNotEqual(icon,RED,data)
        self.assertTrue(icon.startswith("var(--bubble-icon-color"),icon)
        self.assertEqual(self.stored_card()[MODULE_ID],changed)
        self.assertFalse(self.errors,self.errors)

    def test_28_long_run_updates_and_navigation_do_not_leak(self):
        card=self.page.locator("bubble-card").first
        before=self.wait_value(lambda:card.evaluate(READ_CARD),lambda d:d["icon"]==RED)
        latencies=[]
        for cycle in range(20):
            for state,color in (("off","rgb(150, 150, 150)"),("on",RED)):
                started=time.monotonic()
                self.service("input_boolean","turn_"+state,"input_boolean.vsc_main_enabled")
                self.wait_value(lambda:card.evaluate(READ_CARD),lambda d,c=color:d["icon"]==c)
                latencies.append(time.monotonic()-started)
        for cycle in range(8):
            self.page.goto(base.BASE+"/lovelace-vsc-e2e/away",wait_until="domcontentloaded")
            expect(self.page.get_by_text("Lifecycle navigation target")).to_be_visible(timeout=25000)
            self.page.goto(base.BASE+"/lovelace-vsc-e2e/vsc",wait_until="domcontentloaded")
            expect(self.page.locator("bubble-card")).to_have_count(4,timeout=45000)
        card=self.page.locator("bubble-card").first
        after=self.wait_value(lambda:card.evaluate(READ_CARD),lambda d:d["icon"]==RED)
        self.assertEqual(after["styles"],before["styles"],(before,after))
        self.assertEqual(after["ownedCount"],before["ownedCount"],(before,after))
        latencies.sort()
        # 40 real WebSocket round trips; the median must stay interactive.
        self.assertLess(latencies[len(latencies)//2],1.5,latencies)
        self.assertFalse(self.errors,self.errors)

    def open_editor(self):
        """Mount the real editor visibly so mouse and keyboard reach it."""
        self.page.locator("bubble-card").first.evaluate("""host => {
            const frame=document.createElement('div');
            frame.id='vsc-editor-frame';
            frame.style.cssText='position:fixed;inset:0;overflow:auto;z-index:99999;'
                +'background:var(--card-background-color,#fff);padding:12px';
            document.body.appendChild(frame);
            const editor=customElements.get('bubble-card').getConfigElement();
            editor.hass=document.querySelector('home-assistant').hass;
            editor.setConfig({...host.config,modules:['visual_styling_center']});
            frame.appendChild(editor);
            editor._expandedPanelStates={modules_editor_panel:true,visual_styling_center:true};
            // Behave like HA's card editor dialog: feed every change back in.
            editor.addEventListener('config-changed', ev => {
                window.__vscConfig=ev.detail.config;
                editor.setConfig(ev.detail.config);
            });
            window.__vscConfig=editor._config;
            editor.requestUpdate();
            window.__vscEditor=editor;
        }""")

    def tag_fields(self):
        """Mark each rendered VSC selector so Playwright can target it."""
        return self.page.evaluate("""() => {
            const panel=window.__vscEditor?.shadowRoot?.querySelector(
                'ha-expansion-panel[data-module-id="visual_styling_center"]');
            if (!panel) return [];
            const found=[];
            const walk=root => {
                for (const el of root.querySelectorAll('*')) {
                    if (el.localName==='ha-selector' && el.name && !el.dataset.vscField) {
                        el.dataset.vscField=el.name;
                    }
                    if (el.dataset?.vscField) found.push(el.dataset.vscField);
                    if (el.shadowRoot) walk(el.shadowRoot);
                }
            };
            walk(panel);
            return [...new Set(found)];
        }""")

    def config_value(self,name):
        return self.page.evaluate("n => window.__vscConfig?.visual_styling_center?.[n]",name)

    def expand_sections(self):
        panels=self.page.locator('#vsc-editor-frame ha-expansion-panel[data-module-id="visual_styling_center"] '
                                 'ha-form-expandable ha-expansion-panel')
        for i in range(panels.count()):
            panel=panels.nth(i)
            if panel.evaluate("p => !p.expanded"):
                summary=panel.locator("#summary").first
                summary.scroll_into_view_if_needed()
                summary.click()

    def operate(self,field):
        name=field["name"]
        kind,options=next(iter(field["selector"].items()))
        options=options or {}
        root=self.page.locator(f'[data-vsc-field="{name}"]').first
        root.scroll_into_view_if_needed()
        if kind=="boolean":
            current=self.config_value(name)
            if current is None: current=field.get("default",False)
            root.locator("ha-switch").first.click()
            return not current
        if kind=="number":
            box=root.locator("input").last
            box.click()
            self.page.keyboard.press("Control+a")
            current=self.config_value(name)
            if current is None: current=field.get("default")
            value=options.get("max",9)
            if current==value: value=options.get("min",0)
            self.page.keyboard.type(str(value))
            self.page.keyboard.press("Tab")
            return value
        if kind=="text":
            box=root.locator("input, textarea").first
            box.click()
            self.page.keyboard.press("Control+a")
            self.page.keyboard.type("12px")
            self.page.keyboard.press("Tab")
            return "12px"
        if kind=="color_rgb":
            root.locator('input[type="color"]').first.fill("#0a141e")
            return [10,20,30]
        if kind=="select":
            choices=[o["value"] if isinstance(o,dict) else o for o in options.get("options",[])]
            current=self.config_value(name) or field.get("default")
            target=next(c for c in choices if c!=current)
            radios=root.locator("ha-radio")
            if radios.count():
                # HA draws short option lists as radio buttons.
                radios.nth(choices.index(target)).click()
                return target
            root.locator("ha-select").first.click()
            self.page.locator(f'#vsc-editor-frame ha-list-item[value="{target}"], '
                              f'#vsc-editor-frame mwc-list-item[value="{target}"]').first.click()
            return target
        if kind=="entity":
            # HA 2026.10 opens a search popup from the picker field.
            root.click()
            self.page.wait_for_timeout(400)
            self.page.keyboard.type("light.vsc_child")
            self.page.wait_for_timeout(600)
            option=self.page.locator('ha-combo-box-item, [role="option"]').filter(
                has_text="light.vsc_child")
            if option.count(): option.first.click()
            else: self.page.keyboard.press("Enter")
            return "light.vsc_child"
        raise AssertionError("Unhandled selector "+kind)

    def test_29_physical_editor_interaction_for_every_field(self):
        module=module_code()
        fields=[f for f in flat_fields(module["editor"]) if "selector" in f]
        self.assertEqual(len(fields),len(list(flat_fields(module["editor"]))))
        # Fields with `visible:` rules appear/disappear with their switches.
        dependents={}
        for f in fields:
            for rule in f.get("visible") or []:
                dependents.setdefault(rule["field"],set()).add(f["name"])
        stacks=[]
        self.page.on("pageerror",lambda e:stacks.append((e.stack or str(e))[:700]))
        self.open_editor()
        self.wait_value(lambda:self.page.evaluate("() => !!window.__vscEditor?._modulesLoaded"),bool,timeout=30)
        self.page.wait_for_timeout(500)
        pending={f["name"]:f for f in fields}
        failures={}
        def run(field):
            name=field["name"]
            try:
                expected=self.operate(field)
                self.wait_value(lambda n=name:self.config_value(n),
                                lambda v,e=expected:v==e or (isinstance(e,(int,float))
                                    and isinstance(v,(int,float)) and abs(v-e)<1e-6),timeout=6)
            except Exception as exc:
                failures[name]=f"{next(iter(field['selector']))}: {str(exc)[:160]}"
            del pending[name]
        for _ in range(6):
            if not pending: break
            self.expand_sections()
            visible=set(self.wait_value(self.tag_fields,bool,timeout=20))
            progressed=False
            # Operate plain fields first, then switches whose shown dependents are done.
            for name in [n for n in list(pending) if n in visible and n not in dependents]:
                run(pending[name]); progressed=True
            for name in [n for n in list(pending) if n in visible and n in dependents]:
                if not (dependents[name]&visible&set(pending)):
                    run(pending[name]); progressed=True
            if not progressed: break
        self.assertEqual(sorted(pending),[],"fields never became visible")
        self.page.screenshot(path=str(base.ARTIFACTS/"test_29_editor.png"),full_page=True,timeout=12000)
        self.assertFalse(failures,f"{len(failures)}/{len(fields)} fields failed:\n"
                         +"\n".join(f"{k}: {v}" for k,v in failures.items()))

        # Live CSS update: hand the edited config to the mounted VSC card.
        final=self.page.evaluate("() => window.__vscConfig")
        self.page.evaluate("() => document.getElementById('vsc-editor-frame').remove()")
        card=self.page.locator("bubble-card").first
        card.evaluate("(el,cfg) => el.setConfig(cfg)",final)
        self.wait_value(lambda:card.evaluate(READ_CARD),lambda d:d["owned"])
        # Save through HA storage and reload: every edited value persists.
        self.ensure_storage_dashboard()
        self.save_card(dict(final,name="Edited VSC"))
        element=self.open_stored()
        self.wait_value(lambda:element.evaluate(READ_CARD),lambda d:d["owned"])
        element=self.open_stored(reload=True)
        self.wait_value(lambda:element.evaluate(READ_CARD),lambda d:d["owned"])
        self.assertEqual(self.stored_card()[MODULE_ID],final[MODULE_ID])
        self.assertFalse(self.errors,"\n\n".join(stacks))

if __name__=="__main__":
    import unittest
    unittest.main()
