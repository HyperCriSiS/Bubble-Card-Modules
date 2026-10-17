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
            const init=await hass.callWS({
                type:'config_entries/flow/init',
                handler:'bubble_card_tools',
                context:{source:'user'}
            });
            if (init.type !== 'form' || !init.flow_id) {
                throw Error("BCT config-flow init failed: "+JSON.stringify(init));
            }
            const result=await hass.callWS({
                type:'config_entries/flow/configure',
                flow_id:init.flow_id,
                user_input:{}
            });
            if (result.type !== 'create_entry') {
                throw Error("BCT config-entry setup failed: "+JSON.stringify(result));
            }
            return {result:result.type,entry:result.result?.entry_id ?? null};
        }""")
        self.assertEqual(installed["result"],"create_entry",installed)

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
