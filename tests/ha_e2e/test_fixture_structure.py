"""Offline verification for isolated HA fixtures."""
from pathlib import Path
import unittest
import yaml
from generate_fixture import extract_module,make_config,make_dashboard
from bootstrap import require_loopback
ROOT=Path(__file__).resolve().parents[2]

class HAContracts(unittest.TestCase):
    def test_loopback_only(self):
        for url in ("https://example.org:8123","http://192.168.1.1:8123","http://ha.local:8123"):
            with self.subTest(url=url), self.assertRaises(ValueError): require_loopback(url)
        self.assertEqual(require_loopback("http://127.0.0.1:8123/"),"http://127.0.0.1:8123")

    def test_module_extraction(self):
        module=extract_module((ROOT/"Visual-Styling-Center/Visual-Styling-Center.md").read_text(encoding="utf-8"))
        self.assertIsInstance(module.get("editor"),list)
        self.assertGreater(len(module["code"]),15000)

    def test_virtual_entities_and_rgb_templates(self):
        cfg=make_config()
        self.assertEqual(len(cfg["template"][0]["light"]),2)
        self.assertEqual(len(cfg["input_number"]),8)
        self.assertEqual(set(cfg["input_boolean"]),{"vsc_main_enabled","vsc_child_enabled"})
        self.assertEqual(cfg["light"][0]["entities"],["light.vsc_main","light.vsc_child"])
        v=cfg["template"][0]["light"][0]
        self.assertIn("states('input_number.vsc_main_red')",v["rgb"])
        self.assertNotIn("{{ [{{",v["rgb"])
        self.assertEqual([x["data"]["value"] for x in v["set_rgb"]],
                        ["{{ r | int(0) }}","{{ g | int(0) }}","{{ b | int(0) }}"])
        self.assertEqual(yaml.safe_load(yaml.safe_dump(cfg))["template"][0]["light"][0]["rgb"],v["rgb"])

    def test_bct_fixture_contains_real_module(self):
        cfg=make_config()
        self.assertIn("lovelace",cfg)
        source=extract_module((ROOT/"Visual-Styling-Center/Visual-Styling-Center.md").read_text(encoding="utf-8"))
        self.assertEqual(len([item for section in source["editor"] for item in section.get("schema",[]) if "name" in item]),61)
        workflow=(ROOT/".github/workflows/test-vsc-ha-e2e.yml").read_text(encoding="utf-8")
        self.assertIn("2708319696513f5916f062723847c6cd80715dcc",workflow)
        self.assertIn("custom_components/bubble_card_tools",workflow)

    def test_lovelace_and_native_baseline(self):
        cards=make_dashboard(".bubble-icon { color:red }")["views"][0]["cards"]
        self.assertEqual(len(cards),4)
        self.assertNotIn("styles",cards[1])
        self.assertIn("styles",cards[0])
        self.assertIn("styles",cards[2])
        self.assertEqual(cards[3]["card_type"],"sub-buttons")
        self.assertIn("styles",cards[3])
        # v3.4.2 drops the main section on sub-buttons cards.
        self.assertEqual(list(cards[3]["sub_button"]),["bottom"])

    def test_layout_theme_matrix_views(self):
        views={v["path"]:v for v in make_dashboard("VSC","OTHER")["views"]}
        matrix=views["matrix"]["cards"]
        self.assertEqual(matrix[1]["card_layout"],"large")
        self.assertEqual(matrix[2]["type"],"grid")
        self.assertTrue(matrix[3]["styles"].startswith("VSC") and matrix[3]["styles"].endswith("OTHER"))
        self.assertTrue(matrix[4]["styles"].startswith("VSC"))
        self.assertIn("badgy-condition-helper",matrix[4])
        self.assertEqual(matrix[5]["card_type"],"pop-up")
        self.assertEqual(views["themed"]["theme"],"VSC E2E Theme")
        gestures=views["gestures"]["cards"]
        self.assertNotIn("always_visible",gestures[0]["sub_button"]["main"][0])
        self.assertEqual(gestures[1]["hold_action"]["action"],"perform-action")
        self.assertIn("VSC E2E Theme",make_config()["frontend"]["themes"])
        self.assertEqual(views["sections"]["type"],"sections")
        native=views["sections"]["sections"][0]["cards"][1]
        self.assertNotIn("styles",native)

    def test_ci_isolated_and_verified(self):
        text=(ROOT/".github/workflows/test-vsc-ha-e2e.yml").read_text(encoding="utf-8")
        for must in ("-p 127.0.0.1:8123:8123","--cap-drop=ALL",
                     "d526dfd815af6a022b8f7355874fc96f2df859aa213cff7b374f7d913a6436ae","if: always()"):
            self.assertIn(must,text)

if __name__=="__main__":unittest.main()
