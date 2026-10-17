"""Real Bubble Card Tools integration in the isolated HA + Chromium frontend.

Uses the upstream BCT v1.1.1 backend, real config-entry flow, storage and
WebSocket commands. No fake HASS endpoints or production installation.
"""
import time
import yaml
import test_lovelace as base


class BubbleCardToolsStorage(base.RealLovelace):
    test_01_actual_renderer_and_native_slider = None
    test_02_external_main_state_update = None
    test_03_child_rgb_websocket_updates_gradient = None
    test_04_native_slider_pointer_drives_ha_service = None
    test_05_original_bubble_card_without_vsc = None
    test_06_navigation_and_reconnection = None

    def test_15_real_bct_registration_module_roundtrip(self):
        card = self.page.locator("bubble-card").first
        installed = card.evaluate("""async el => {
            const ha=document.querySelector('home-assistant');
            const hass=ha?.hass;
            if (!hass?.callWS) throw Error("Real Home Assistant websocket unavailable");
            let stage="flow/init";
            try {
            const init=await hass.callApi('POST','config/config_entries/flow',{
                handler:'bubble_card_tools'
            });
            if (init.type !== 'form' || !init.flow_id) {
                throw Error("BCT config-flow init failed: "+JSON.stringify(init));
            }
            stage="flow/configure";
            const result=await hass.callApi('POST',
                'config/config_entries/flow/'+init.flow_id, {});
            if (result.type !== 'create_entry') {
                throw Error("BCT config-entry setup failed: "+JSON.stringify(result));
            }
            return {result:result.type,entry:result.result?.entry_id ?? null};
            } catch (error) {
                return {error:JSON.stringify(error),message:String(error),stage};
            }
        }""")
        self.assertEqual(installed.get("result"),"create_entry",installed)

        def fetch():
            try:
                return card.evaluate("""async el => {
                    const ha=document.querySelector('home-assistant');
                    return await ha.hass.callWS({type:'bubble_card_tools/read_module',
                        name:'modules/visual_styling_center.yaml'});
                }""")
            except Exception:
                return None
        result=self.wait_value(fetch,lambda item:bool(item and item.get("content")),timeout=30)
        document=yaml.safe_load(result["content"])
        module=document["visual_styling_center"]
        fields=[f["name"] for section in module["editor"] for f in section.get("schema",[]) if "name" in f]
        self.assertEqual(len(fields),46,fields)
        self.assertEqual(len(set(fields)),46)
        self.assertGreater(len(module["code"]),15000)

        # Write into a throwaway file, verify exact BCT persistence, delete it.
        scratch="modules/vsc_ci_roundtrip.yaml"
        payload=yaml.safe_dump({"vsc_ci_roundtrip": module},
                               sort_keys=False,allow_unicode=True)
        written=card.evaluate("""async (el, args) => {
            const hass=document.querySelector('home-assistant').hass;
            return await hass.callWS({type:'bubble_card_tools/write_module',
                name:args.name,content:args.content});
        }""",{"name":scratch,"content":payload})
        self.assertEqual(written.get("status"),"written",written)
        echoed=card.evaluate("""async (el, name) => {
            return await document.querySelector('home-assistant').hass.callWS({
                type:'bubble_card_tools/read_module',name
            });
        }""",scratch)
        self.assertEqual(echoed["content"],payload)
        removed=card.evaluate("""async (el, name) => {
            return await document.querySelector('home-assistant').hass.callWS({
                type:'bubble_card_tools/delete_module',name
            });
        }""",scratch)
        self.assertEqual(removed.get("status"),"deleted",removed)

    def test_16_bct_real_editor_renders_module_form(self):
        """The v3.4.2 Bubble Card editor must render the VSC form from BCT YAML."""
        card=self.page.locator("bubble-card").first
        editor=card.evaluate("""host => {
            const ctor=customElements.get('bubble-card');
            const element=ctor.getConfigElement();
            document.body.appendChild(element);
            element.setConfig({...host.config,modules:['visual_styling_center']});
            const ha=document.querySelector('home-assistant');
            element.hass=ha.hass;
            element._expandedPanelStates={
                modules_editor_panel:true,visual_styling_center:true
            };
            element.requestUpdate();
            window.__vscRealBctEditor=element;
            return element.tagName.toLowerCase();
        }""")
        self.assertEqual(editor,"bubble-card-editor")
        def inspect():
            return card.evaluate("""host => {
                const editor=window.__vscRealBctEditor;
                if (!editor) return {loaded:false};
                const root=editor.shadowRoot;
                const module=root?.querySelector(
                    'ha-expansion-panel[data-module-id="visual_styling_center"]');
                const forms=module ? Array.from(module.querySelectorAll('ha-form')) : [];
                const flatten=(items) => (items||[]).flatMap(item =>
                    item?.name ? [item.name] : flatten(item?.schema)
                );
                return {
                    loaded:!!editor._modulesLoaded,
                    panel:!!module,
                    forms:forms.length,
                    names:forms.flatMap(f=>flatten(f.schema)),
                    bctWarning:root?.textContent?.includes('Bubble Card Tools')||false
                };
            }""")
        visible=self.wait_value(inspect,lambda data:data.get("loaded") and data.get("panel"),timeout=30)
        self.assertTrue(visible["panel"],visible)
        self.assertGreaterEqual(visible["forms"],1,visible)
        # The schema is drawn from BCT's installed YAML, not a fixture mock.
        self.assertEqual(len(set(visible["names"])),46,visible)
        self.assertEqual(len(visible["names"]),46,visible)
        card.evaluate("host => window.__vscRealBctEditor.remove()")
