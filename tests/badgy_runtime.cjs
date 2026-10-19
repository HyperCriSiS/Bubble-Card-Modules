/* Browserless integration smoke test of the Bubble Card JS-template runtime. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");

const js = fs.readFileSync(0, "utf8");
const template = new Function(
  "hass", "entity", "state", "card", "checkConditionsMet", "renderTemplate", "hasChanged", "onTeardown",
  "return " + String.fromCharCode(96) + js + String.fromCharCode(96) + ";"
);

class Styles {
  constructor() { this.data = new Map(); this.writes = new Map(); }
  setProperty(k, v, priority = "") { this.data.set(k, [String(v), priority]); this.writes.set(k, (this.writes.get(k)||0)+1); }
  getPropertyValue(k) { return this.data.get(k)?.[0] || ""; }
  getPropertyPriority(k) { return this.data.get(k)?.[1] || ""; }
  removeProperty(k) { this.data.delete(k); }
}
class Classes {
  constructor(value = "") { this.set = new Set(value.split(/\s+/).filter(Boolean)); this.addCount = new Map(); }
  contains(c) { return this.set.has(c); }
  add(...cs) { for (const c of cs) { this.set.add(c); this.addCount.set(c, (this.addCount.get(c) || 0) + 1); } }
  remove(...cs) { cs.forEach(c => this.set.delete(c)); }
  toggle(c, enabled) { if (enabled === undefined) enabled = !this.contains(c); enabled ? this.add(c) : this.remove(c); return enabled; }
}
class El {
  constructor(tag = "div", cls = "") {
    this.tag = tag;
    this.style = new Styles();
    this.dataset = {};
    this._attributes = new Map();
    this._text = "";
    this.children = [];
    this.parent = null;
    this.className = cls;
  }
  set className(v) { this._className = v; this.classList = new Classes(v); }
  get className() { return this._className; }
  set textContent(v) { this._text = String(v); this.children.forEach(c => c.parent = null); this.children = []; }
  get textContent() { return this._text; }
  appendChild(child) { child.parent = this; this.children.push(child); return child; }
  removeChild(child) { this.children.splice(this.children.indexOf(child), 1); child.parent = null; }
  remove() { if (this.parent) this.parent.removeChild(this); }
  getAttribute(k) { return this._attributes.has(k) ? this._attributes.get(k) : null; }
  setAttribute(k, v) { this._attributes.set(k, String(v)); }
  removeAttribute(k) { this._attributes.delete(k); }
  matches(s) {
    const bits = s.split(".").filter(Boolean);
    if (s[0] === ".") return bits.every(b => this.classList.contains(b));
    if (s.startsWith("ha-icon.")) return this.tag === "ha-icon" && bits.slice(1).every(b => this.classList.contains(b));
    if (s === "ha-card") return this.tag === "ha-card";
    return false;
  }
  querySelector(s) {
    if (s.includes(" ")) {
      const split = s.indexOf(" ");
      const parent = this.querySelector(s.slice(0, split));
      return parent?.querySelector(s.slice(split + 1)) || null;
    }
    for (const child of this.children) {
      if (child.matches(s)) return child;
      const nested = child.querySelector(s);
      if (nested) return nested;
    }
    return null;
  }
  querySelectorAll(s) {
    let matches = [];
    for (const child of this.children) {
      if (child.matches(s)) matches.push(child);
      matches.push(...child.querySelectorAll(s));
    }
    return matches;
  }
  closest(s) {
    for (let p = this; p; p = p.parent) if (p.matches(s)) return p;
    return null;
  }
}
let created = 0;
global.document = { createElement(tag) { created++; return new El(tag); } };
global.getComputedStyle = () => ({ position: "relative" });
global.CSS = {
  supports(property, value) { return property === "color" && /^(#[0-9a-f]{3,8}|rgb\(|hsl\(|var\(--|black$|red$|blue$)/i.test(value); }
};

const root = new El("card");
const cardContainer = root.appendChild(new El("div", "bubble-button-card-container"));
const main = cardContainer.appendChild(new El("div", "bubble-icon-container"));
const mainIcon = main.appendChild(new El("ha-icon", "bubble-icon"));
mainIcon.setAttribute("icon", "mdi:home");
const sub = cardContainer.appendChild(new El("div", "bubble-sub-button-1"));
const subIcon = sub.appendChild(new El("ha-icon", "bubble-sub-button-icon"));
subIcon.setAttribute("icon", "mdi:fan");
const groupedContainer = cardContainer.appendChild(new El("div", "bubble-sub-button-group"));
const groupedSub = groupedContainer.appendChild(new El("div", "bubble-sub-button-2"));
const groupedIcon = groupedSub.appendChild(new El("ha-icon", "bubble-sub-button-icon"));
groupedIcon.setAttribute("icon", "mdi:fan");
// Legacy tracking markers do not grant CSS property ownership.
sub.classList.add("sub-button-direct-bg");
sub.style.setProperty("opacity", "0.60");
main.dataset.badgyBackgroundManaged = "1";
main.style.setProperty("opacity", "0.75");
const externalBadge = sub.appendChild(new El("div", "bubble-sub-button-badge entity-badge"));
externalBadge.textContent = "external";
const externalMain = main.appendChild(new El("div", "bubble-sub-button-badge entity-badge"));
externalMain.textContent = "native";
global.getComputedStyle = node => ({ position: node === groupedSub ? "static" : "relative" });

const state = (id, value, attributes = {}) => ({entity_id: id, state: value, attributes});
const hass = {
  states: {
    "binary_sensor.window": state("binary_sensor.window", "on", {device_class: "window"}),
    "sensor.power": state("sensor.power", "25", {unit_of_measurement: "W"}),
    "sensor.flag": state("sensor.flag", "on"),
    "sensor.palette": state("sensor.palette", "idle", {hex: "#c02200"})
  },
  formatEntityState(s) { return s.entity_id.startsWith("binary_sensor.") ? (s.state === "on" ? "Open" : "Closed") : s.state; }
};
const check = {condition: "state", entity_id: "sensor.flag", state: "on"};
const cfg = {
  entity_badges: { "0": {entity: "sensor.power", scale: 1.7}, "1": {entity: "sensor.power"}, main: {entity: "binary_sensor.window", scale: 1.3} },
  icon_badges: { main: {icon: "mdi:alert"} },
  icon_effects: {sub_button_icon: {"0": {effect: "spin-360", condition: check}, "1": {effect: "rotate", condition: check}}},
  sub_button_effects: {"0": {effect: "pulse", condition: check}},
  entity_badge_effects: {"0": {effect: "spin-360"}},
  sub_buttons_background: {
    "0": {rules: [
      {condition: check, type: "solid", color: "#ff0000"},
      {condition: {condition:"state",entity_id:"sensor.flag",state:"off"}, type:"solid",color:"black"}
    ]}
  },
  icon_colors: {main_icon: {color: "#ffbb00", condition: check}},
  icons: {main_icon: {icon: "mdi:flash", condition: check}},
  card_effects: {effect: "glow", color: "#ffffff", condition: check}
};
const context = {config: {"badgy-condition-helper": cfg}};
let forceFallback = false;
function checkConditionsMet(items) {
  if (forceFallback) throw Error("Native conditions unavailable");
  return items.every(x => {
    if (x.condition === "state") return hass.states[x.entity_id]?.state === x.state;
    return false;
  });
}
function renderTemplate(t) {
  return t.startsWith("{{") ? hass.states["sensor.palette"].attributes.hex : t;
}
const fingerprints = new Map();
let gateSkips = 0;
// Mirrors Bubble Card 3.4.2 src/tools/module-gate.js: values are compared by
// String(value), so a DOM element never carries its identity into the gate.
function hasChanged(key, ...values) {
  let signature = "";
  for (const value of values) {
    if (Array.isArray(value)) signature += value.join(",");
    else if (value !== null && value !== undefined) signature += String(value);
    signature += "";
  }
  if (fingerprints.get(key) === signature) {
    gateSkips++;
    return false;
  }
  fingerprints.set(key, signature);
  return true;
}
let teardown = null;
function onTeardown(callback) { teardown = callback; }
function run() {
  const output = template.call(context, hass, "sensor.power", hass.states["sensor.power"].state, root, checkConditionsMet, renderTemplate, hasChanged, onTeardown);
  assert.equal(typeof output, "string");
}
run();
const subBadge = sub.querySelector(".badgy-owned-badge.entity-badge");
const mainBadge = main.querySelector(".badgy-owned-badge.entity-badge");
assert.ok(subBadge, "sub-button entity badge rendered");
assert.ok(mainBadge, "main icon entity badge rendered");
assert.equal(externalBadge.textContent, "external", "do not hijack another module's badge");
assert.equal(externalMain.textContent, "native", "do not hijack existing main badges");
assert.ok(!externalBadge.classList.contains("badgy-owned-badge"));
assert.equal(sub.style.getPropertyValue("opacity"), "0.60", "native sub opacity survives legacy cleanup");
assert.equal(main.style.getPropertyValue("opacity"), "0.75", "native main opacity survives legacy cleanup");
assert.equal(groupedSub.style.getPropertyValue("position"), "relative", "position managed during rendering");
assert.equal(mainBadge.textContent, "Open", "binary sensor state is localized");
assert.equal(subBadge.textContent, "25W");
assert.equal(subBadge.style.getPropertyValue("--badge-scale"), "1.7");
assert.equal(mainBadge.style.getPropertyValue("--badge-scale"), "1.3");
assert.ok(main.querySelector(".icon-badge"), "main icon icon-badge rendered");
assert.ok(groupedSub.querySelector(".entity-badge"), "badge works on grouped sub-button");
assert.ok(groupedIcon.classList.contains("badgy-effect-rotate"), "grouped sub-button icon effect works");
assert.ok(subIcon.classList.contains("badgy-effect-spin-360"));
assert.ok(sub.classList.contains("badgy-effect-pulse"));
assert.ok(cardContainer.classList.contains("badgy-card-glow"));
assert.equal(mainIcon.getAttribute("icon"), "mdi:flash");
assert.equal(sub.style.getPropertyValue("background"), "#ff0000");
const additions = subIcon.classList.addCount.get("badgy-effect-spin-360");
const amountCreated = created;
hass.states["sensor.power"].state = "26";
run();
assert.equal(created, amountCreated, "no badge DOM churn on sensor update");
assert.equal(sub.querySelector(".badgy-owned-badge.entity-badge"), subBadge, "badge identity is stable");
assert.equal(subBadge.textContent, "26W");
assert.equal(subIcon.classList.addCount.get("badgy-effect-spin-360"), additions, "animation is not restarted");
hass.states["sensor.flag"].state = "off";
hass.states["binary_sensor.window"].state = "off";
run();
assert.equal(mainBadge.textContent, "Closed", "binary sensor state updates in place");
assert.ok(!subIcon.classList.contains("badgy-effect-spin-360"), "icon effect stops on false");
assert.ok(!groupedIcon.classList.contains("badgy-effect-rotate"), "grouped icon effect stops on false");
assert.ok(!sub.classList.contains("badgy-effect-pulse"), "container effect stops on false");
assert.ok(!cardContainer.classList.contains("badgy-card-glow"), "card glow stops on false");
assert.equal(mainIcon.getAttribute("icon"), "mdi:home", "original icon restored on false");
assert.equal(sub.style.getPropertyValue("background"), "var(--black-color, black)", "named color uses theme with CSS fallback");
cfg.sub_buttons_background["0"] = {type:"solid", color_template:"{{ state_attr('sensor.palette','hex') }}"};
run();
assert.equal(sub.style.getPropertyValue("background"), "#c02200", "template-based color resolves");
cfg.global_defaults = { badge_scale: 1.1, sub_button_effect: "none" };
delete cfg.entity_badges["0"].scale;
run();
assert.equal(subBadge.style.getPropertyValue("--badge-scale"), "1.1", "global badge size works");
assert.ok(!sub.classList.contains("badgy-has-effect"), "none is not treated as an effect");

assert.equal(sub.style.getPropertyValue("opacity"), "0.60", "no opacity overwritten by Badgy");
const badgeWriteBefore = subBadge.style.writes.get("--badge-scale") || 0;
run();
run();
assert.ok(gateSkips > 0, "hasChanged gate avoids repeated badge work");
assert.equal(subBadge.style.writes.get("--badge-scale") || 0, badgeWriteBefore,
  "unchanged badge scale does not trigger further writes");

// Set an external background, then verify that Badgy records that newer
// value as the restoration target instead of deleting it.
cfg.sub_buttons_background["0"] = {type:"solid", color:"#1155ff", opacity:0.4};
run();
assert.match(sub.style.getPropertyValue("background"), /^color-mix\(in srgb,/);
assert.equal(sub.style.getPropertyValue("opacity"), "0.60", "background alpha never changes element opacity");
sub.style.setProperty("background", "#339900");
run();
assert.match(sub.style.getPropertyValue("background"), /^color-mix\(in srgb,/);
delete cfg.sub_buttons_background["0"];
run();
assert.equal(sub.style.getPropertyValue("background"), "#339900",
  "new native/external background restored on disabling Badgy");

// Same behavior for colors and icons; if the underlying HA icon changes
// while an override is active we must restore that latest native icon.
hass.states["sensor.flag"].state = "on";
run();
assert.equal(mainIcon.getAttribute("icon"), "mdi:flash");
mainIcon.setAttribute("icon", "mdi:ceiling-light");
mainIcon.style.setProperty("color", "#445566");
run();
assert.equal(mainIcon.getAttribute("icon"), "mdi:flash");
assert.notEqual(mainIcon.style.getPropertyValue("color"), "#445566");
hass.states["sensor.flag"].state = "off";
run();
assert.equal(mainIcon.getAttribute("icon"), "mdi:ceiling-light",
  "updated native icon preserved after override ends");
assert.equal(mainIcon.style.getPropertyValue("color"), "#445566",
  "external color restored after override ends");

// An explicitly supplied display_text must override formatting and units.
const oldMainCfg = cfg.entity_badges.main;
cfg.entity_badges["0"].display_text = "STANDBY";
cfg.entity_badges.main = {entity: "sensor.power", display_text: "0007", decimals: 2};
run();
assert.equal(subBadge.textContent, "STANDBY", "custom sub-button label must not add units");
assert.equal(mainBadge.textContent, "0007", "main custom label must not round or add units");
delete cfg.entity_badges["0"].display_text;
cfg.entity_badges.main = oldMainCfg;
hass.states["sensor.power"].state = "unavailable";
run();
assert.equal(subBadge.textContent, "unavailable", "unavailable sensor must not display numeric unit");
hass.states["sensor.power"].state = "26";
run();
assert.equal(subBadge.textContent, "26W", "numeric sensor still has unit");

// A badge node removed by a Bubble Card rebuild must be filled again, even
// though Bubble Card's hasChanged() cannot tell two elements apart.
subBadge.remove();
run();
const rebuiltBadge = sub.querySelector(".badgy-owned-badge.entity-badge");
assert.ok(rebuiltBadge && rebuiltBadge !== subBadge, "lost badge is recreated");
assert.equal(rebuiltBadge.textContent, "26W", "recreated badge is filled despite string gate");
assert.equal(rebuiltBadge.style.top, "-8px", "recreated badge is positioned");
rebuiltBadge.remove();
sub.appendChild(subBadge);
run();

// A matching rule's own color wins over a dynamic color on the parent entry.
hass.states["sensor.flag"].state = "on";
cfg.sub_buttons_background["0"] = {
  type: "solid", color_template: "{{ state_attr('sensor.palette','hex') }}",
  rules: [{condition: check, color: "#ff0000"}]
};
run();
assert.equal(sub.style.getPropertyValue("background"), "#ff0000",
  "rule color is not overridden by the parent color_template");
cfg.sub_buttons_background["0"].rules = [{condition: check, type: "solid"}];
run();
assert.equal(sub.style.getPropertyValue("background"), "#c02200",
  "a rule without its own color still inherits the parent template");

// Unset gradient colors keep the v2025 fallbacks (three-color middle is green).
cfg.sub_buttons_background["0"] = {type: "three-color"};
run();
assert.equal(sub.style.getPropertyValue("background"),
  "linear-gradient(135deg, #ff0000 0%, #00ff00 50%, #0000ff 100%)");
cfg.sub_buttons_background["0"] = {type: "two-color"};
run();
assert.equal(sub.style.getPropertyValue("background"),
  "linear-gradient(135deg, #ff0000 0%, #0000ff 100%)");
delete cfg.sub_buttons_background["0"];
hass.states["sensor.flag"].state = "off";
run();

// beta.6: rules on badges and effects, badge-attached effects, fallback and
// separate global offsets for main icon badges.
hass.states["sensor.flag"].state = "on";
cfg.entity_badges["0"].rules = [
  {label: "Hot", condition: {condition: "state", entity_id: "sensor.flag", state: "off"}, color: "#ff0000"},
  {label: "Flag", condition: check, color: "#0000ff", display_text: "FLAG"}
];
run();
assert.equal(subBadge.textContent, "FLAG", "first matching badge rule overrides text");
assert.equal(subBadge.style.getPropertyValue("--badge-color"), "#0000ff", "matching badge rule overrides color");
hass.states["sensor.flag"].state = "off";
cfg.entity_badges["0"].rules[0].condition = {condition: "state", entity_id: "sensor.flag", state: "never"};
run();
assert.equal(sub.querySelector(".badgy-owned-badge.entity-badge"), null, "no matching badge rule hides the badge");
cfg.entity_badges["0"].fallback_to_static = true;
run();
const fallbackBadge = sub.querySelector(".badgy-owned-badge.entity-badge");
assert.ok(fallbackBadge, "fallback_to_static shows the static badge when no rule matches");
assert.equal(fallbackBadge.textContent, "26W", "fallback uses the static badge settings");
delete cfg.entity_badges["0"].rules;
delete cfg.entity_badges["0"].fallback_to_static;
run();

// An effect set on the badge wins over the separate entity_badge_effects entry.
const liveBadge = sub.querySelector(".badgy-owned-badge.entity-badge");
assert.ok(liveBadge.classList.contains("badgy-effect-spin-360"), "separate badge effect still applies");
cfg.entity_badges["0"].effect = "pulse";
run();
assert.ok(liveBadge.classList.contains("badgy-effect-pulse"), "badge-attached effect applies");
assert.ok(!liveBadge.classList.contains("badgy-effect-spin-360"), "badge-attached effect has precedence");
delete cfg.entity_badges["0"].effect;
run();
assert.ok(liveBadge.classList.contains("badgy-effect-spin-360"), "separate effect returns without inline effect");

// Effect rules: first match wins, none matching stops the effect.
cfg.sub_button_effects["0"] = {rules: [
  {condition: {condition: "state", entity_id: "sensor.flag", state: "on"}, effect: "pulse"},
  {condition: {condition: "state", entity_id: "sensor.flag", state: "off"}, effect: "shake"}
]};
run();
assert.ok(sub.classList.contains("badgy-effect-shake"), "matching effect rule applies");
hass.states["sensor.flag"].state = "on";
run();
assert.ok(sub.classList.contains("badgy-effect-pulse") && !sub.classList.contains("badgy-effect-shake"),
  "effect rule switches with the condition");
cfg.sub_button_effects["0"].rules = [{condition: {condition: "state", entity_id: "sensor.flag", state: "never"}, effect: "pulse"}];
run();
assert.ok(!sub.classList.contains("badgy-has-effect"), "no matching effect rule stops the effect");
delete cfg.sub_button_effects["0"];

// Global sub-button offsets no longer move main icon badges.
cfg.global_defaults.badge_h_pos = -8;
run();
assert.equal(mainBadge.style.right, "0px", "sub-button global offset does not move main badges");
cfg.global_defaults.main_badge_h_pos = 4;
run();
assert.equal(mainBadge.style.right, "4px", "main badges use their own global offset");
delete cfg.global_defaults.badge_h_pos;
delete cfg.global_defaults.main_badge_h_pos;
hass.states["sensor.flag"].state = "off";
run();

// Fallback NOT must negate all nested conditions, not just the first one.
forceFallback = true;
cfg.icon_badges["0"] = {icon: "mdi:alert", condition: {condition: "not", conditions: [
  {condition: "state", entity_id: "sensor.flag", state: "on"},
  {condition: "state", entity_id: "sensor.power", state: "26"}
]}};
run();
assert.equal(sub.querySelector(".badgy-owned-badge.icon-badge"), null,
  "fallback NOT hides badge when the second condition matches");
hass.states["sensor.power"].state = "27";
run();
assert.ok(sub.querySelector(".badgy-owned-badge.icon-badge"),
  "fallback NOT shows badge when no nested condition matches");
forceFallback = false;

// An inactive grouped badge must not leave a static container positioned.
delete cfg.entity_badges["1"];
run();
assert.equal(groupedSub.querySelector('.badgy-owned-badge'), null,
  "grouped badge removed when no longer configured");
assert.equal(groupedSub.style.getPropertyValue('position'), '',
  "temporary positioning restored immediately without tearing down card");

assert.equal(typeof teardown, "function", "onTeardown registered");
teardown();
assert.equal(main.querySelector(".badgy-owned-badge.entity-badge"), null, "main badge removed on teardown");
assert.equal(main.querySelector(".entity-badge"), externalMain, "foreign main badge survives teardown");
assert.equal(sub.querySelector(".badgy-owned-badge.entity-badge"), null, "sub badge removed on teardown");
assert.equal(sub.querySelector(".entity-badge"), externalBadge, "foreign sub badge survives teardown");
assert.equal(groupedSub.style.getPropertyValue("position"), "", "container position restored on teardown");
assert.equal(sub.style.getPropertyValue("opacity"), "0.60", "native opacity survives teardown");
assert.equal(mainIcon.getAttribute("icon"), "mdi:ceiling-light", "native icon stays restored after cleanup");
assert.equal(mainIcon.style.getPropertyValue("color"), "#445566", "restored color survives teardown");
assert.ok(!sub.classList.contains("badgy-has-effect"), "effect class cleaned");
console.log("Badgy runtime smoke tests: PASS");