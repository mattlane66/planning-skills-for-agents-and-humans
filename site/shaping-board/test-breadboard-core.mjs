import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
const require=createRequire(import.meta.url);
const BB=require("./breadboard-core.cjs");
const model=[
  BB.VERSION,
  "P1 | place | Request form | Enter request | app",
  "U1 | ui | Submit request | Click send | app | in=P1",
  "N1 | nonui | Validate | Check input | backend",
  "Q1 | decision | Valid? | Continue or reject | backend",
  "S1 | store | Requests | Persist accepted requests | db",
  "U2 | ui | Confirmation | Shows status | app | in=P1",
  "U1 -> N1 : control",
  "N1 -> Q1 : control",
  "Q1 -> S1 : yes",
  "Q1 -> U2 : no",
  "S1 -> U2 : return",
  ""
].join("\n");
const g=BB.parse(model);
assert.deepEqual(g.err,[]);
assert.equal(g.nodes.length,6);
assert.equal(g.edges.length,5);
assert.equal(BB.canonical(model),model);
const first=BB.render(model,null,"m");
assert.equal(first.err.length,0);
assert.equal(first.html,BB.render(model,null,"m").html,"same model must render identically");
assert.match(first.html,/UI · U1/);
assert.match(first.html,/Request form/);
assert.deepEqual(BB.parse(model.replace("in=P1","in=P9")).err.some(s=>s.includes("missing place")),true);
assert.ok(BB.parse(model.replace("U1 -> N1 : control","U1 -> N1 : surprise")).err.some(s=>s.includes("Unsupported wire")));
assert.ok(BB.parse(model.replace("Q1 -> S1 : yes","U1 -> S1 : yes")).err.some(s=>s.includes("must originate")));
assert.ok(BB.parse(model.replace("U1 | ui","O1 | ui")).err.length);
assert.ok(BB.parse(model.replace("U1 -> N1 : control","U1 -> N1 : control\nU1 -> N1 : control")).err.length);
assert.ok(BB.parse(model.replace("U1 -> N1 : control","U1 -> N1 : control ~ M1 2")).err.length,"arbitrary SVG paths disallowed");
const proposal={kind:"BreadboardPatch",schema_version:1,base_dsl:model,operations:[
  {op:"update_node",id:"U1",set:{title:"Send request"}},
  {op:"add_node",node:{id:"N2",kind:"nonui",title:"Notify",detail:"Send receipt",system:"backend"}},
  {op:"add_edge",from:"S1",to:"N2",kind:"control"}
]};
const result=BB.patch(model,proposal);
assert.equal(result.changes.length,3);
assert.match(result.dsl,/U1 \| ui \| Send request/);
assert.ok(result.changes.some(x=>x.type==="wire"));
assert.equal(BB.patch(model,proposal).dsl,result.dsl);
assert.throws(()=>BB.patch(result.dsl,proposal),/Stale/);
assert.throws(()=>BB.patch(model,{...proposal,operations:[{op:"remove_node",id:"P1"}]}),/connected wires\/children/);
assert.throws(()=>BB.patch(model,{...proposal,operations:[{op:"add_node",node:{id:"X9",kind:"magic",title:"foo",detail:"",system:"app"}}]}),/Invalid kind/);
const html=readFileSync(new URL("./index.html",import.meta.url),"utf8");
const markerStart="/* BEGIN INLINED BREADBOARD CORE — generated from breadboard-core.cjs */";
const markerEnd="/* END INLINED BREADBOARD CORE */";
assert.ok(html.includes(markerStart)&&html.includes(markerEnd));
const embedded=html.split(markerStart)[1].split(markerEnd)[0].trim();
const source=readFileSync(new URL("./breadboard-core.cjs",import.meta.url),"utf8").trim();
assert.equal(embedded,source,"standalone HTML and canonical compiler must stay byte-identical");
console.log("Breadboard core: strict grammar, deterministic view, semantic patches, stale protection and offline inline sync passed");
