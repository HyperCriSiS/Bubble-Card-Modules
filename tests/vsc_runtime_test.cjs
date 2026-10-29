"use strict";
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const runner = vm.runInNewContext(fs.readFileSync(process.argv[2], "utf8") + "\nrunner;", {});
function style() {
  const values = new Map(), priorities = new Map();
  let writes = 0;
  return {
    setProperty(k,v,p=""){writes++;values.set(k,String(v));priorities.set(k,p)},
    removeProperty(k){writes++;values.delete(k);priorities.delete(k)},
    getPropertyValue(k){return values.get(k)||""},
    getPropertyPriority(k){return priorities.get(k)||""},
    getWrites(){return writes}
  };
}
function classes() {
  const s = new Set();
  return {
    add(...k){k.forEach(x=>s.add(x))},remove(...k){k.forEach(x=>s.delete(x))},
    contains(x){return s.has(x)},toggle(x,on){if(on)s.add(x);else s.delete(x)}
  };
}
function icon(){return {style:style(),dataset:{}}}
function makeCard(){
  const main=icon(),sub=[icon(),icon(),icon()];
  return {main,sub,style:style(),classList:classes(),
    querySelector(q){
      if(q===".bubble-icon")return main;
      const m=q.match(/^\.bubble-sub-button-(\d+) \.bubble-sub-button-icon$/);
      return m?sub[+m[1]-1]??null:null;
    },
    querySelectorAll(q){return q===".bubble-sub-button-icon"?sub:[]}
  };
}
function st(state,rgb){return {state,attributes:rgb?{rgb_color:rgb}:{}}}
function test(n,fn){try{fn();console.log("PASS",n)}catch(e){console.error("FAIL",n,e);process.exitCode=1}}
const hass={states:{"light.a":st("on",[100,20,40]),"light.b":st("off")}};
const ctx={config:{entity:"light.a",sub_button:[{entity:"light.b"}],visual_styling_center:{
  enable_entity_colored_main_icon:true,enable_entity_colored_subicons:true
}}};
const cfg=ctx.config.visual_styling_center,card=makeCard();
const gradientGates = new Map();
const nativeHasChanged = (key,...values) => {
  const sig = JSON.stringify(values);
  const was = gradientGates.get(key);
  gradientGates.set(key,sig);
  return was !== sig;
};
let teardownVSC = null;
const run=()=>runner.call(ctx,card,hass,nativeHasChanged,fn=>{teardownVSC=fn});
test("entity state colors update",()=>{
  run();assert.equal(card.main.style.getPropertyValue("color"),"rgb(100, 20, 40)");
  assert.equal(card.sub[0].style.getPropertyValue("color"),"rgb(150, 150, 150)");
  hass.states["light.a"]=st("off");run();
  assert.equal(card.main.style.getPropertyValue("color"),"rgb(150, 150, 150)");
});
test("old inline colors are restored",()=>{
  cfg.enable_entity_colored_main_icon=false;run();
  assert.equal(card.main.style.getPropertyValue("color"),"");
});
test("zero values are honored",()=>{
  cfg.enable_icon_helper=true;cfg.helper_color=[1,2,3];cfg.helper_opacity=0;cfg.helper_size_ratio=0;run();
  assert.equal(card.style.getPropertyValue("--helper-color"),"rgba(1, 2, 3, 0)");
  assert.equal(card.style.getPropertyValue("--helper-size"),"0");
});
test("gradient recalculates without mutating config",()=>{
  cfg.enable_gradient=true;cfg.gradient_target="background";
  const before=JSON.stringify(cfg);
  hass.states["light.a"]=st("on",[10,20,30]);run();
  assert.equal(JSON.stringify(cfg),before);
  assert.equal(card.classList.contains("use-gradient-background"),true);
  hass.states["light.a"]=st("on",[80,90,10]);run();
  assert.match(card.style.getPropertyValue("--card-gradient"),/80/);
});
test("sectioned sub-buttons work",()=>{
  ctx.config.sub_button={main:[{group:[{entity:"light.a"},{entity:"light.b"}]}],bottom:[{entity:"light.a"}]};
  run();
  assert.equal(card.sub[0].style.getPropertyValue("color"),"rgb(80, 90, 10)");
  assert.equal(card.sub[1].style.getPropertyValue("color"),"rgb(150, 150, 150)");
  assert.equal(card.sub[2].style.getPropertyValue("color"),"rgb(80, 90, 10)");
});
test("function-color reset and native ownership",()=>{
  cfg.enable_function_button_color=true;cfg.enable_entity_colored_subicons=false;run();
  assert.equal(card.sub[1].style.getPropertyValue("color"),"rgba(255, 255, 255, 0.9)");
  cfg.enable_function_button_color=false;run();
  assert.equal(card.sub[1].style.getPropertyValue("color"),"");
  cfg.enable_entity_colored_main_icon=true;run();
  card.main.style.setProperty("color","magenta","important");
  cfg.enable_entity_colored_main_icon=false;run();
  assert.equal(card.main.style.getPropertyValue("color"),"magenta");
});
test("scene state uses configured function color",()=>{
  hass.states["scene.demo"]=st("on");
  ctx.config.entity="scene.demo";
  cfg.enable_entity_colored_main_icon=false;
  cfg.enable_function_button_color=true;
  run();
  assert.equal(card.main.style.getPropertyValue("color"),"rgba(255, 255, 255, 0.9)");
  ctx.config.entity="light.a";
  cfg.enable_function_button_color=false;
  run();
});
test("gradient follows child light RGB changes",()=>{
  cfg.enable_gradient=true;
  cfg.gradient_target="background";
  cfg.gradient_entity="light.group";
  hass.states["light.group"]={state:"on",attributes:{entity_id:["light.a","light.b"]}};
  hass.states["light.b"]=st("on",[200,20,20]);
  run();
  const initial=card.style.getPropertyValue("--card-gradient");
  hass.states["light.b"]=st("on",[15,220,210]);
  run();
  assert.notEqual(card.style.getPropertyValue("--card-gradient"),initial);
});
test("mixed groups use Bubble Card's class index rather than YAML order",()=>{
  ctx.config.entity="light.a";
  ctx.config.sub_button={
    main:[{entity:"light.a"},{group:[{entity:"light.b"}]}],
    bottom:[{entity:"light.a"}]
  };
  cfg.enable_entity_colored_subicons=true;
  cfg.enable_function_button_color=false;
  hass.states["light.a"]=st("on",[11,22,33]);
  hass.states["light.b"]=st("off");
  run();
  assert.equal(card.sub[0].style.getPropertyValue("color"),"rgb(150, 150, 150)");
  assert.equal(card.sub[1].style.getPropertyValue("color"),"rgb(11, 22, 33)");
  assert.equal(card.sub[2].style.getPropertyValue("color"),"rgb(11, 22, 33)");
});
test("sub-button without entity inherits parent light state",()=>{
  ctx.config.entity="light.a";
  ctx.config.sub_button={main:[{entity:null}]};
  cfg.enable_entity_colored_subicons=true;
  cfg.enable_function_button_color=false;
  hass.states["light.a"]=st("on",[17,34,51]);
  run();
  assert.equal(card.sub[0].style.getPropertyValue("color"),"rgb(17, 34, 51)");
  hass.states["light.a"]=st("off");
  run();
  assert.equal(card.sub[0].style.getPropertyValue("color"),"rgb(150, 150, 150)");
});
test("hide background resets custom styling correctly",()=>{
  cfg.manual_icon_background_color="#123456";cfg.hide_icon_background=true;run();
  assert.equal(card.style.getPropertyValue("--icon-background-color"),"transparent");
  cfg.hide_icon_background=false;run();
  assert.equal(card.style.getPropertyValue("--icon-background-color"),"#123456");
  delete cfg.manual_icon_background_color;run();
  assert.equal(card.style.getPropertyValue("--icon-background-color"),"");
});

test("unchanged render does not rewrite CSS variables",()=>{
  run();
  const before=card.style.getWrites();
  run();
  assert.equal(card.style.getWrites(),before);
});
test("removing layout configuration resets module-owned CSS variables",()=>{
  cfg.inner_padding=13;
  run();
  assert.equal(card.style.getPropertyValue("--inner-padding"),"13px");
  delete cfg.inner_padding;
  run();
  assert.equal(card.style.getPropertyValue("--inner-padding"),"");
});

test("foreign CSS variables survive empty settings and return after override",()=>{
  delete cfg.manual_icon_color;
  delete cfg.custom_icon_color;
  card.style.setProperty("--icon-color","rgb(1, 2, 3)","important");
  run();
  assert.equal(card.style.getPropertyValue("--icon-color"),"rgb(1, 2, 3)");
  cfg.manual_icon_color="#abcdef";
  run();
  assert.equal(card.style.getPropertyValue("--icon-color"),"#abcdef");
  delete cfg.manual_icon_color;
  run();
  assert.equal(card.style.getPropertyValue("--icon-color"),"rgb(1, 2, 3)");
  assert.equal(card.style.getPropertyPriority("--icon-color"),"important");
});
test("native teardown restores VSC owned variables, classes and icon colors",()=>{
  cfg.manual_icon_background_color="#aabbcc";
  cfg.hide_icon_background=true;
  cfg.enable_entity_colored_main_icon=true;
  ctx.config.entity="light.a";
  hass.states["light.a"]=st("on",[45,56,67]);
  run();
  assert.equal(card.classList.contains("hide-icon-background"),true);
  assert.equal(card.main.style.getPropertyValue("color"),"rgb(45, 56, 67)");
  assert.equal(typeof teardownVSC,"function");
  teardownVSC();
  assert.equal(card.main.style.getPropertyValue("color"),"magenta");
  assert.equal(card.classList.contains("hide-icon-background"),false);
  assert.equal(card.style.getPropertyValue("--icon-background-color"),"");
  assert.equal(card.style.getPropertyValue("--icon-color"),"rgb(1, 2, 3)");
});
// A card that applies VSC through `modules:` the way the Bubble Card editor
// stores it, with a real setConfig for the cleanup wrapper to hook into.
const moduleCard=makeCard();
const moduleCtx={
  config:{entity:"light.a",modules:["visual_styling_center"],visual_styling_center:{inner_padding:5}},
  setConfig(next){this.config=next;}
};
const runModule=()=>runner.call(moduleCtx,moduleCard,hass,nativeHasChanged,()=>{});
test("interaction effects stay on unless explicitly disabled",()=>{
  runModule();
  assert.equal(moduleCard.classList.contains("vsc-interaction-effects"),true);
  moduleCtx.config.visual_styling_center.enable_interaction_effects=false;
  runModule();
  assert.equal(moduleCard.classList.contains("vsc-interaction-effects"),false);
  delete moduleCtx.config.visual_styling_center.enable_interaction_effects;
  runModule();
  assert.equal(moduleCard.classList.contains("vsc-interaction-effects"),true);
});
test("editing a card that keeps VSC in modules does not clean up",()=>{
  moduleCtx.setConfig({...moduleCtx.config,name:"Renamed"});
  assert.equal(moduleCard.style.getPropertyValue("--inner-padding"),"5px");
});
test("removing VSC from the modules list cleans up a mounted card",()=>{
  runModule();
  moduleCtx.setConfig({...moduleCtx.config,modules:["!visual_styling_center"]});
  assert.equal(moduleCard.style.getPropertyValue("--inner-padding"),"");
  assert.equal(moduleCard.classList.contains("vsc-interaction-effects"),false);
});
// v2026.10.29: options from the D list and the measured icon background fix.
const dCard=makeCard();
const dCtx={config:{entity:"light.a",visual_styling_center:{}}};
const dCfg=dCtx.config.visual_styling_center;
const runD=()=>runner.call(dCtx,dCard,hass,nativeHasChanged,()=>{});
test("icon background is only overridden on request",()=>{
  runD();
  assert.equal(dCard.classList.contains("vsc-custom-icon-background"),false);
  dCfg.custom_icon_background_color=[1,2,3];runD();
  assert.equal(dCard.classList.contains("vsc-custom-icon-background"),true);
  assert.equal(dCard.style.getPropertyValue("--icon-background-color"),"rgb(1, 2, 3)");
  delete dCfg.custom_icon_background_color;dCfg.hide_icon_background=true;runD();
  assert.equal(dCard.style.getPropertyValue("--icon-background-color"),"transparent");
  delete dCfg.hide_icon_background;runD();
  assert.equal(dCard.classList.contains("vsc-custom-icon-background"),false);
  assert.equal(dCard.style.getPropertyValue("--icon-background-color"),"");
});
test("name/state text, radii and card background use native variables",()=>{
  Object.assign(dCfg,{manual_name_color:"#ff0000",custom_state_color:[0,0,255],
    name_font_size:16,state_font_size:0,card_border_radius:4,icon_border_radius:0,
    subbutton_border_radius:6,custom_card_background_color:[10,20,30],card_background_opacity:0.5});
  runD();
  assert.equal(dCard.style.getPropertyValue("--vsc-name-color"),"#ff0000");
  assert.equal(dCard.style.getPropertyValue("--vsc-state-color"),"rgb(0, 0, 255)");
  assert.equal(dCard.style.getPropertyValue("--vsc-name-font-size"),"16px");
  assert.equal(dCard.style.getPropertyValue("--vsc-state-font-size"),"0px");
  assert.equal(dCard.style.getPropertyValue("--bubble-button-border-radius"),"4px");
  assert.equal(dCard.style.getPropertyValue("--bubble-button-icon-border-radius"),"0px");
  assert.equal(dCard.style.getPropertyValue("--bubble-sub-button-border-radius"),"6px");
  assert.equal(dCard.style.getPropertyValue("--bubble-button-main-background-color"),
    "color-mix(in srgb, rgb(10, 20, 30) 50%, transparent)");
  ["vsc-name-color","vsc-state-color","vsc-name-size","vsc-state-size"].forEach(c=>assert.equal(dCard.classList.contains(c),true,c));
  for (const k of Object.keys(dCfg)) delete dCfg[k];
  runD();
  ["--vsc-name-color","--bubble-button-border-radius","--bubble-button-main-background-color"].forEach(v=>assert.equal(dCard.style.getPropertyValue(v),"",v));
  assert.equal(dCard.classList.contains("vsc-name-color"),false);
});
test("opacity alone fades the native background",()=>{
  dCfg.card_background_opacity=0.25;runD();
  assert.match(dCard.style.getPropertyValue("--bubble-button-main-background-color"),
    /^color-mix\(in srgb, var\(--bubble-main-background-color.* 25%, transparent\)$/);
  delete dCfg.card_background_opacity;runD();
});
test("theme state colors keep fixed colors as fallback",()=>{
  hass.states["switch.s"]=st("on");hass.states["light.off"]=st("off");
  dCtx.config.entity="switch.s";dCfg.enable_entity_colored_main_icon=true;runD();
  assert.equal(dCard.main.style.getPropertyValue("color"),"rgb(140, 200, 105)");
  dCfg.use_theme_state_colors=true;runD();
  assert.equal(dCard.main.style.getPropertyValue("color"),
    "var(--state-switch-active-color, var(--state-active-color, rgb(140, 200, 105)))");
  dCtx.config.entity="light.off";runD();
  assert.equal(dCard.main.style.getPropertyValue("color"),
    "var(--state-light-inactive-color, var(--state-inactive-color, rgb(150, 150, 150)))");
  delete dCfg.use_theme_state_colors;delete dCfg.enable_entity_colored_main_icon;dCtx.config.entity="light.a";runD();
});
test("gradient angle keeps the old direction unless set",()=>{
  Object.assign(dCfg,{enable_gradient:true,gradient_target:"background"});
  hass.states["light.a"]=st("on",[10,20,30]);runD();
  assert.match(dCard.style.getPropertyValue("--card-gradient"),/^linear-gradient\(to right,/);
  dCfg.gradient_angle=135;runD();
  assert.match(dCard.style.getPropertyValue("--card-gradient"),/^linear-gradient\(135deg,/);
  hass.states["light.a"]=st("off");runD();
  assert.match(dCard.style.getPropertyValue("--card-gradient"),/^linear-gradient\(135deg, #FF0000/);
});
