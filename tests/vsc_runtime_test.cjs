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
    querySelectorAll(){return []}
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
const run=()=>runner.call(ctx,card,hass,nativeHasChanged);
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
