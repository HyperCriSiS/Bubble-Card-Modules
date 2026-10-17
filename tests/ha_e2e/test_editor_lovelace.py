"""Native Bubble Card editor config-load smoke against the real HA frontend.

Unlike a static schema parse, this mounts the actual upstream editor element.
It does not pretend that the full BCT module GUI is installed or exercised.
"""
from pathlib import Path
import test_lovelace as base
from generate_fixture import extract_module


class RealEditorSmoke(base.RealLovelace):
    test_01_actual_renderer_and_native_slider = None
    test_02_external_main_state_update = None
    test_03_child_rgb_websocket_updates_gradient = None
    test_04_native_slider_pointer_drives_ha_service = None
    test_05_original_bubble_card_without_vsc = None
    test_06_navigation_and_reconnection = None

    def test_13_real_editor_preserves_all_vsc_fields_on_set_config(self):
        root = Path(__file__).resolve().parents[2]
        module = extract_module((root / "Visual-Styling-Center" /
                                 "Visual-Styling-Center.md").read_text(encoding="utf-8"))
        # This is the existing editor schema, not a manually retyped test list.
        schema = module["editor"]
        fields = [field for section in schema for field in section.get("schema", [])
                  if isinstance(field, dict) and "name" in field]
        names = [field["name"] for field in fields]
        self.assertEqual(len(names), 46, names)
        self.assertEqual(len(set(names)), 46, names)
        defaults = {field["name"]: field.get("default") for field in fields}
        result = self.page.evaluate("""options => {
            const host = document.querySelector('bubble-card');
            const ctor = customElements.get('bubble-card');
            const editor = ctor.getConfigElement();
            const original = {...host.config,
                visual_styling_center: {...options}};
            document.body.appendChild(editor);
            const ha = document.querySelector('home-assistant');
            editor.setConfig(original);
            if (ha?.hass) editor.hass=ha.hass;
            window.__vscTestEditor = editor;
            return {
                tag:editor.tagName.toLowerCase(),
                config:editor._config?.visual_styling_center,
                actual:!!customElements.get('bubble-card-editor'),
            };
        }""", defaults)
        self.assertEqual(result["tag"], "bubble-card-editor", result)
        self.assertTrue(result["actual"], result)
        self.assertEqual(result["config"], defaults, result)

    def test_14_real_editor_reload_preserves_nested_module_values(self):
        result = self.page.evaluate("""() => {
            const editor=customElements.get('bubble-card').getConfigElement();
            const config={...document.querySelector('bubble-card').config,
                visual_styling_center:{
                    height_multiplier:1.8,enable_gradient:true,
                    gradient_target:'background',custom_icon_color:[12,34,56],
                    inner_padding:0,enable_entity_colored_subicons:false
                }};
            document.body.appendChild(editor);
            editor.setConfig(config);
            const first=structuredClone(editor._config.visual_styling_center);
            // Equivalent to an edit-dialog re-open receiving serialized config.
            editor.setConfig(structuredClone(editor._config));
            const second=structuredClone(editor._config.visual_styling_center);
            editor.remove();
            return {first,second};
        }""")
        self.assertEqual(result["first"], result["second"], result)
        self.assertEqual(result["second"]["inner_padding"], 0, result)
        self.assertEqual(result["second"]["custom_icon_color"], [12, 34, 56], result)
