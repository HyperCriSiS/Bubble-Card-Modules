#!/usr/bin/env python3
"""Generate a fresh virtual-only Home Assistant fixture and VSC Lovelace dashboard."""
from pathlib import Path
import argparse
import re
import yaml

MODULE_ID = "visual_styling_center"
COMBINED_MODULE_ID = "subbutton_below_normal_layout"
BADGY_MODULE_ID = "badgy-condition-helper"
THEME = "VSC E2E Theme"

def extract_module(markdown, module_id=MODULE_ID):
    fence = re.escape(chr(96) * 3)
    for match in re.finditer(fence+r"(?:yaml|yml)[ \t]*\n(.*?)\n"+fence, markdown, re.S):
        data = yaml.safe_load(match.group(1))
        if isinstance(data, dict) and isinstance(data.get(module_id), dict):
            if isinstance(data[module_id].get("code"), str):
                return data[module_id]
    raise ValueError("No executable "+module_id+" YAML found")

def light(name, slug):
    key = "vsc_" + slug
    def number(ch):
        return "states('input_number."+key+"_"+ch+"') | int(0)"
    return {
        "name": "VSC "+name,
        "unique_id": "vsc_e2e_"+slug,
        "state": "{{ is_state('input_boolean."+key+"_enabled', 'on') }}",
        "level": "{{ "+number("brightness")+" }}",
        "rgb": "{{ ["+number("red")+", "+number("green")+", "+number("blue")+"] }}",
        "turn_on": [{"action":"input_boolean.turn_on","target":{"entity_id":"input_boolean."+key+"_enabled"}}],
        "turn_off": [{"action":"input_boolean.turn_off","target":{"entity_id":"input_boolean."+key+"_enabled"}}],
        "set_level": [{"action":"input_number.set_value",
                       "target":{"entity_id":"input_number."+key+"_brightness"},
                       "data":{"value":"{{ brightness | int(0) }}"}}],
        "set_rgb": [{"action":"input_number.set_value",
                     "target":{"entity_id":"input_number."+key+"_"+channel},
                     "data":{"value":"{{ "+var+" | int(0) }}"}} for channel,var in (("red","r"),("green","g"),("blue","b"))]
    }

def make_config():
    lights=(("Main","main",(255,0,0)),("Child","child",(0,200,20)))
    inputs={}
    for _,slug,colors in lights:
        key="vsc_"+slug
        inputs[key+"_brightness"]={"name":key+" brightness","initial":128,"min":0,"max":255,"step":1}
        for ch,v in zip(("red","green","blue"),colors):
            inputs[key+"_"+ch]={"name":key+" "+ch,"initial":v,"min":0,"max":255,"step":1}
    return {
        "default_config": {},
        "homeassistant":{"name":"VSC isolated CI","time_zone":"Etc/UTC"},
        "input_boolean":{"vsc_"+slug+"_enabled":{"name":"VSC "+slug+" enabled","initial":True} for _,slug,_ in lights},
        "input_number": inputs,
        "template":[{"light":[light(name,slug) for name,slug,_ in lights]}],
        "light":[{"platform":"group","name":"VSC Group","unique_id":"vsc_e2e_group",
                  "entities":["light.vsc_main","light.vsc_child"]}],
        "lovelace":{
            "resource_mode":"yaml",
            "resources":[{"url":"/local/bubble-card.js","type":"module"}],
            "dashboards":{"lovelace-vsc-e2e":{"mode":"yaml","filename":"ui-lovelace-vsc-e2e.yaml",
                "title":"VSC E2E","icon":"mdi:test-tube","show_in_sidebar":True}}
        },
        # A user theme with distinct light/dark surfaces for the theme matrix.
        "frontend":{"themes":{THEME:{"modes":{
            "light":{"card-background-color":"rgb(250, 240, 200)",
                     "secondary-background-color":"rgb(250, 240, 200)"},
            "dark":{"card-background-color":"rgb(20, 30, 60)",
                    "secondary-background-color":"rgb(20, 30, 60)"}}}}},
        "logger":{"default":"warning"}
    }

def make_dashboard(code, combined_code="", badgy_code=""):
    def button(name,entity,options=None,subs=None):
        card={"type":"custom:bubble-card","card_type":"button","button_type":"slider",
              "entity":entity,"name":name}
        if subs is not None: card["sub_button"]=subs
        if options is not None:
            card["styles"]=code
            card[MODULE_ID]=options
        return card
    single={"main":[{"entity":"light.vsc_child","sub_button_type":"slider","always_visible":True}]}
    options={"enable_entity_colored_main_icon":True,"enable_entity_colored_subicons":True,
             "enable_gradient":True,"gradient_target":"background","gradient_entity":"light.vsc_group"}
    matrix={"enable_entity_colored_main_icon":True,"enable_entity_colored_subicons":True}
    mixed={"main":[{"entity":"light.vsc_main"},{"group":[{"entity":"light.vsc_child"}]}],
           "bottom":[{"entity":"light.vsc_main"}]}
    return {"title":"VSC isolated E2E","views":[
        {"title":"VSC","path":"vsc","cards":[
            button("VSC Primary","light.vsc_main",options,single),
            button("Native baseline (no VSC)","light.vsc_main",None,single),
            button("VSC Mixed Groups","light.vsc_group",
                   {"enable_entity_colored_main_icon":True,"enable_entity_colored_subicons":True},mixed),
            # Sub-buttons card type: VSC only reaches its sub-buttons there.
            # v3.4.2 renders only the bottom section of this card type.
            {"type":"custom:bubble-card","card_type":"sub-buttons","styles":code,
             MODULE_ID:{"enable_entity_colored_subicons":True,"subbutton_background_ratio":1.25},
             "sub_button":{"bottom":[{"entity":"light.vsc_main"},
                                   {"entity":"light.vsc_child","custom_height":44}]}}
        ]},
        # Layout/theme matrix: the same VSC options in every container type.
        {"title":"Matrix","path":"matrix","cards":[
            button("Matrix Normal","light.vsc_main",matrix),
            dict(button("Matrix Large","light.vsc_main",matrix),card_layout="large"),
            {"type":"grid","columns":2,"square":False,"cards":[
                button("Matrix Grid A","light.vsc_main",matrix),
                button("Matrix Grid B","light.vsc_main",matrix)]},
            # VSC combined with another styling module of this repository.
            dict(button("Matrix Combined","light.vsc_main",matrix,
                        {"main":[{"entity":"light.vsc_child"}]}),styles=code+"\n"+combined_code),
            # VSC together with Badgy on the same sub-button.
            dict(button("Matrix Badgy","light.vsc_main",matrix,{"main":[{"entity":"light.vsc_child"}]}),
                 styles=code+"\n"+badgy_code,
                 **{BADGY_MODULE_ID:{"icon_badges":{0:{"icon":"mdi:alert","color":"yellow"}}}}),
            {"type":"custom:bubble-card","card_type":"pop-up","hash":"#vsc-matrix","name":"VSC pop-up",
             "cards":[button("Matrix Popup","light.vsc_main",matrix)]}
        ]},
        {"title":"Sections","path":"sections","type":"sections","max_columns":2,"sections":[
            {"type":"grid","cards":[button("Sections VSC","light.vsc_main",matrix),
                                    button("Sections Native","light.vsc_main")]}]},
        {"title":"Themed","path":"themed","theme":THEME,"cards":[
            button("Themed VSC","light.vsc_main",matrix),
            button("Themed Native","light.vsc_main"),
            button("Themed Custom BG","light.vsc_main",
                   dict(matrix,custom_card_background_color=[10,20,30]))]},
        {"title":"Away","path":"away","cards":[{"type":"markdown","content":"Lifecycle navigation target"}]}
    ]}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument("--config-dir",type=Path,required=True)
    args=parser.parse_args()
    module=extract_module((args.repo/"Visual-Styling-Center/Visual-Styling-Center.md").read_text(encoding="utf-8"))
    combined=extract_module((args.repo/"Sub-Button-Below-Normal-Layout/Sub-button-below-normal-layout.md")
                            .read_text(encoding="utf-8"),COMBINED_MODULE_ID)
    badgy=extract_module((args.repo/"Badgy-Conditions/Badgy-Conditions.md").read_text(encoding="utf-8"),
                         BADGY_MODULE_ID)
    dest=args.config_dir.resolve()
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"www").mkdir(exist_ok=True)
    # BCT's source of truth is an on-disk YAML module in this throwaway HA.
    modules_dir=dest/"bubble_card"/"modules"
    modules_dir.mkdir(parents=True,exist_ok=True)
    (modules_dir/"visual_styling_center.yaml").write_text(
        yaml.safe_dump({MODULE_ID:module},sort_keys=False,allow_unicode=True,width=120),
        encoding="utf-8")
    (dest/"configuration.yaml").write_text(yaml.safe_dump(make_config(),sort_keys=False,allow_unicode=True),encoding="utf-8")
    (dest/"ui-lovelace-vsc-e2e.yaml").write_text(
        yaml.safe_dump(make_dashboard(module["code"],combined["code"],badgy["code"]),sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")
    print("Generated isolated Home Assistant configuration and Lovelace dashboard")

if __name__=="__main__":
    main()
