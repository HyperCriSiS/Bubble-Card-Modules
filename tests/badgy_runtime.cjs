/* Browserless integration smoke test of the Bubble Card JS-template runtime. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");

const js = fs.readFileSync(0, "utf8");
const template = new Function(
  "hass", "entity", "state", "card", "checkConditionsMet", "renderTemplate",
  "return " + String.fromCharCode(96) + js + String.fromCharCode(96) + ";"
);

class Styles {
  constructor() { this.data = new Map(); }
  setProperty(k, v, priority = "") { this.data.set(k, [String(v), priority]); }
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
  supports(property, value) { return property === "color" && /^(#[0-9a-f]{3,8}|rgb\(|hsl\(|var\(--)/i.test(value); }
};

const root = new El("card");
const cardContainer = root.appendChild(new El("div", "bubble-button-card-container"));
const main = cardContainer.appendChild(new El("div", "bubble-icon-container"));
const mainIcon = main.appendChild(new El("ha-icon", "bubble-icon"));
mainIcon.setAttribute("icon", "mdi:home");
const sub = cardContainer.appendChild(new El("div", "bubble-sub-button-1"));
const subIcon = sub.appendChild(new El("ha-icon", "bubble-sub-button-icon"));
subIcon.setAttribute("icon", "mdi:fan");

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
  entity_badges: { "0": {entity: "sensor.power", scale: 1.7}, main: {entity: "binary_sensor.window", scale: 1.3} },
  icon_badges: { main: {icon: "mdi:alert"} },
  icon_effects: {sub_button_icon: {"0": {effect: "spin-360", condition: check}}},
  sub_button_effects: {"0": {effect: "pulse", condition: check}},
  entity_badge_effects: {"0": {effect: "spin-360"}},
  sub_buttons_background: {
    "0": {rules: [
      {condition: check, type: "solid", color: "#ff0000"},
      {condition: {condition:"state",entity_id:"sensor.flag",state:"off"}, type:"solid",color:"#0000ff"}
    ]}
  },
  icon_colors: {main_icon: {color: "#ffbb00", condition: check}},
  icons: {main_icon: {icon: "mdi:flash", condition: check}},
  card_effects: {effect: "glow", color: "#ffffff", condition: check}
};
const context = {config: {"badgy-condition-helper": cfg}};
function checkConditionsMet(items) {
  return items.every(x => {
    if (x.condition === "state") return hass.states[x.entity_id]?.state === x.state;
    return false;
  });
}
function renderTemplate(t) {
  return t.startsWith("{{") ? hass.states["sensor.palette"].attributes.hex : t;
}
function run() {
  const output = template.call(context, hass, "sensor.power", hass.states["sensor.power"].state, root, checkConditionsMet, renderTemplate);
  assert.equal(typeof output, "string");
}
run();
const subBadge = sub.querySelector(".entity-badge");
const mainBadge = main.querySelector(".entity-badge");
assert.ok(subBadge, "sub-button entity badge rendered");
assert.ok(mainBadge, "main icon entity badge rendered");
assert.equal(mainBadge.textContent, "Open", "binary sensor state is localized");
assert.equal(subBadge.textContent, "25W");
assert.equal(subBadge.style.getPropertyValue("--badge-scale"), "1.7");
assert.equal(mainBadge.style.getPropertyValue("--badge-scale"), "1.3");
assert.ok(main.querySelector(".icon-badge"), "main icon icon-badge rendered");
assert.ok(subIcon.classList.contains("effect-spin-360"));
assert.ok(sub.classList.contains("effect-pulse"));
assert.ok(cardContainer.classList.contains("badgy-card-glow"));
assert.equal(mainIcon.getAttribute("icon"), "mdi:flash");
assert.equal(sub.style.getPropertyValue("background"), "#ff0000");
const additions = subIcon.classList.addCount.get("effect-spin-360");
const amountCreated = created;
hass.states["sensor.power"].state = "26";
run();
assert.equal(created, amountCreated, "no badge DOM churn on sensor update");
assert.equal(sub.querySelector(".entity-badge"), subBadge, "badge identity is stable");
assert.equal(subBadge.textContent, "26W");
assert.equal(subIcon.classList.addCount.get("effect-spin-360"), additions, "animation is not restarted");
hass.states["sensor.flag"].state = "off";
hass.states["binary_sensor.window"].state = "off";
run();
assert.equal(mainBadge.textContent, "Closed", "binary sensor state updates in place");
assert.ok(!subIcon.classList.contains("effect-spin-360"), "icon effect stops on false");
assert.ok(!sub.classList.contains("effect-pulse"), "container effect stops on false");
assert.ok(!cardContainer.classList.contains("badgy-card-glow"), "card glow stops on false");
assert.equal(mainIcon.getAttribute("icon"), "mdi:home", "original icon restored on false");
assert.equal(sub.style.getPropertyValue("background"), "#0000ff", "second color rule matches");
cfg.sub_buttons_background["0"] = {type:"solid", color_template:"{{ state_attr('sensor.palette','hex') }}"};
run();
assert.equal(sub.style.getPropertyValue("background"), "#c02200", "template-based color resolves");
cfg.global_defaults = { badge_scale: 1.1, sub_button_effect: "none" };
delete cfg.entity_badges["0"].scale;
run();
assert.equal(subBadge.style.getPropertyValue("--badge-scale"), "1.1", "global badge size works");
assert.ok(!sub.classList.contains("has-effect"), "none is not treated as an effect");
console.log("Badgy runtime smoke tests: PASS");
