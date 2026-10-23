/* Shaping Board breadboard/v1: a portable, deterministic, dependency-free compiler.
   Legacy diagrams remain supported by the Board's original renderer. */
"use strict";
const BreadboardCore = (() => {
  const VERSION = "version: breadboard/v1";
  const KINDS = Object.freeze({P:"place",U:"ui",N:"nonui",Q:"decision",S:"store"});
  const WIRES = new Set(["control","navigate","read","write","return","yes","no","show"]);
  const idPattern = /^[PUNQS][1-9]\d*(?:\.[1-9]\d*)?$/;
  const safeText = value => typeof value === "string" && value.length <= 500 && !/[\r\n|]/.test(value);
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const asNode = value => {
    const n = {id:value.id,kind:value.kind,title:value.title,detail:value.detail,system:value.system};
    if(value.kind === "ui") n.parent=value.parent;
    return n;
  };
  const asEdge = value => ({from:value.from,to:value.to,kind:value.kind});
  function isV1(src) { return typeof src === "string" && /^\s*(?:#.*\n\s*)*version:\s*breadboard\/v1\s*(?:\r?\n|$)/.test(src); }
  function validate(graph) {
    const errors=[],seen=new Set(),by=new Map(),wires=new Set();
    if(graph.nodes.length > 160 || graph.edges.length > 400) errors.push("Breadboard exceeds supported size");
    for(const n of graph.nodes){
      if(!idPattern.test(n.id||"") || KINDS[n.id?.[0]] !== n.kind) errors.push("Invalid kind or stable ID: "+String(n.id));
      if(seen.has(n.id)) errors.push("Duplicate node ID: "+n.id);
      seen.add(n.id);by.set(n.id,n);
      for(const key of ["title","detail","system"])if(!safeText(n[key]) || (key!=="detail"&&!n[key].trim()))errors.push(n.id+" has invalid "+key);
      if(n.kind==="ui"&&(!/^P[1-9]\d*(?:\.[1-9]\d*)?$/.test(n.parent||"")))errors.push(n.id+" needs an in=P# parent");
      if(n.kind!=="ui"&&n.parent!==undefined)errors.push(n.id+" cannot have a parent");
    }
    for(const n of graph.nodes)if(n.kind==="ui"&&by.get(n.parent)?.kind!=="place")errors.push(n.id+" references missing place "+n.parent);
    for(const e of graph.edges){
      const key=[e.from,e.to,e.kind].join("\u0000");
      if(!by.has(e.from)||!by.has(e.to))errors.push("Unknown node in wire "+e.from+" -> "+e.to);
      if(!WIRES.has(e.kind))errors.push("Unsupported wire type "+e.kind);
      if((e.kind==="yes"||e.kind==="no")&&by.get(e.from)?.kind!=="decision")errors.push(e.kind+" must originate at a decision: "+e.from);
      if(wires.has(key))errors.push("Duplicate wire "+e.from+" -> "+e.to+" : "+e.kind);
      wires.add(key);
    }
    return errors;
  }
  function parse(src){
    const graph={version:1,nodes:[],edges:[],groups:[],err:[]};
    if(typeof src!=="string"||src.length>100000)return {...graph,err:["Invalid or oversized breadboard source"]};
    const lines=src.split(/\r?\n/);let header=false;
    for(let i=0;i<lines.length;i++){
      const line=lines[i].trim();if(!line||line.startsWith("#"))continue;
      if(!header){header=true;if(line!==VERSION)graph.err.push("Line "+(i+1)+": expected "+VERSION);continue;}
      const edge=line.match(/^([PUNQS][1-9]\d*(?:\.[1-9]\d*)?)\s*->\s*([PUNQS][1-9]\d*(?:\.[1-9]\d*)?)\s*:\s*([a-z]+)$/);
      if(edge){graph.edges.push({from:edge[1],to:edge[2],kind:edge[3],a:edge[1],b:edge[2],l:edge[3]});continue;}
      const fields=line.split("|").map(s=>s.trim());
      if(fields.length===5||(fields.length===6&&fields[1]==="ui")){
        const [id,kind,title,detail,system,extra]=fields;
        const node={id,kind,title,detail,system};
        if(kind==="ui"){
          if(!extra||!/^in=P[1-9]\d*(?:\.[1-9]\d*)?$/.test(extra))graph.err.push("Line "+(i+1)+": UI needs in=P#");
          else node.parent=extra.slice(3);
        }else if(fields.length===6)graph.err.push("Line "+(i+1)+": only UI can specify a parent");
        graph.nodes.push({...node,i:id,k:kind,t:title,r:detail.split(";").map(s=>s.trim()).filter(Boolean),s:system,pos:[]});
      }else graph.err.push("Line "+(i+1)+": unsupported breadboard statement");
    }
    if(!header)graph.err.push("Missing "+VERSION);
    graph.err.push(...validate(graph));
    return graph;
  }
  function serialize(graph){
    return [VERSION,...graph.nodes.map(value=>{const n=asNode(value);return [n.id,n.kind,n.title,n.detail,n.system,...(n.kind==="ui"?["in="+n.parent]:[])].join(" | ");}),
      ...graph.edges.map(value=>{const e=asEdge(value);return e.from+" -> "+e.to+" : "+e.kind;})].join("\n")+"\n";
  }
  function assertValid(graph){const problems=validate(graph);if(problems.length)throw Error(problems.join("; "));return graph;}
  function canonical(src){const graph=parse(src);if(graph.err.length)throw Error(graph.err.join("; "));return serialize(graph);}
  function layout(graph){
    const rects=new Map(),places=graph.nodes.filter(n=>n.kind==="place"),inside=graph.nodes.filter(n=>n.kind==="ui");
    const others=graph.nodes.filter(n=>n.kind!=="place"&&n.kind!=="ui");
    const columns=Math.max(places.length,1);
    places.forEach((p,i)=>{
      const x=30+i*255;rects.set(p.id,{x,y:35,w:215,h:65});
      inside.filter(n=>n.parent===p.id).forEach((n,j)=>rects.set(n.id,{x:x+8,y:125+j*86,w:199,h:64}));
    });
    const userBottom=Math.max(150,...[...rects.values()].map(p=>p.y+p.h));
    const railTop=userBottom+85;
    others.forEach((n,i)=>rects.set(n.id,{x:30+(i%columns)*255,y:railTop+Math.floor(i/columns)*112,w:215,h:72}));
    const width=Math.max(300,...[...rects.values()].map(p=>p.x+p.w+35));
    const height=Math.max(240,...[...rects.values()].map(p=>p.y+p.h+65));
    return {rects,width,height};
  }
  function render(src,highlight=null,uid="breadboard"){
    const graph=parse(src);
    if(graph.err.length)return {err:graph.err,html:'<div class="wn" role="alert">'+graph.err.map(esc).join("<div></div>")+"</div>"};
    const {rects,width,height}=layout(graph),validUID=/^[a-zA-Z0-9_-]{1,40}$/.test(uid)?uid:"breadboard";
    const h=highlight instanceof Set?highlight:null;
    const nodes=graph.nodes.map(n=>{
      const p=rects.get(n.id),dim=h&&!h.has(n.id)?" dim":"",hit=h&&h.has(n.id)?" hit":"";
      const cls=n.kind==="decision"?"n q":n.kind==="store"?"n st":n.kind==="ui"?"n ui":n.kind==="nonui"?"n o":"n";
      const label=n.kind==="ui"?"UI · "+n.id:n.kind==="nonui"?"System · "+n.id:n.kind+" · "+n.id;
      return '<div class="'+cls+dim+hit+'" style="left:'+p.x+'px;top:'+p.y+'px;width:'+p.w+'px;height:'+p.h+'px"><div class="tp">'+esc(label)+'</div><div class="ti">'+esc(n.title)+'</div><div class="sub">'+esc(n.detail)+'</div></div>';
    }).join("");
    const edges=graph.edges.map(e=>{
      const a=rects.get(e.from),b=rects.get(e.to);let d,x,y;
      if(b.x>a.x+a.w/2){const mx=(a.x+a.w+b.x)/2;d='M'+(a.x+a.w)+' '+(a.y+a.h/2)+' H'+mx+' V'+(b.y+b.h/2)+' H'+b.x;x=mx;y=(a.y+a.h/2+b.y+b.h/2)/2;}
      else{const mx=a.x+a.w/2,tx=b.x+b.w/2,dy=Math.max(a.y+a.h,b.y+b.h)+22;d='M'+mx+' '+(a.y+a.h)+' V'+dy+' H'+tx+' V'+b.y;x=(mx+tx)/2;y=dy-6;}
      const active=!h||(h.has(e.from)&&h.has(e.to));
      return '<path d="'+d+'" fill="none" stroke="var(--mu)" stroke-width="1.5" opacity="'+(active?1:.15)+'" marker-end="url(#'+validUID+')"/>'+
        '<text x="'+x+'" y="'+y+'" font-size="10" fill="var(--ac)" text-anchor="middle">'+esc(e.kind)+'</text>';
    }).join("");
    const html='<div class="fb" data-w="'+width+'" data-h="'+height+'"'+(uid==="m"?' data-zm="1"':"")+'><div class="bx" style="width:'+width+'px;height:'+height+'px">'+
      '<svg width="'+width+'" height="'+height+'" viewBox="0 0 '+width+' '+height+'" xmlns="http://www.w3.org/2000/svg"><defs><marker id="'+validUID+'" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="var(--mu)"/></marker></defs>'+edges+'</svg>'+nodes+'</div></div>';
    return {err:[],html};
  }
  function patch(src,proposal){
    if(!proposal||proposal.kind!=="BreadboardPatch"||proposal.schema_version!==1||!Array.isArray(proposal.operations)||proposal.operations.length<1||proposal.operations.length>50)throw Error("Invalid breadboard patch envelope");
    const current=canonical(src);
    if(proposal.base_dsl!==current)throw Error("Stale breadboard revision: rebase against the current model");
    const original=parse(current);
    const nodes=original.nodes.map(asNode),edges=original.edges.map(asEdge);
    for(const [index,op] of proposal.operations.entries()){
      if(!op||typeof op!=="object")throw Error("Invalid operation "+index);
      const i=nodes.findIndex(n=>n.id===op.id);
      if(op.op==="add_node"){
        const n=asNode(op.node||{});
        if(nodes.some(x=>x.id===n.id))throw Error("Node already exists: "+n.id);
        nodes.push(n);
      }else if(op.op==="update_node"){
        if(i<0)throw Error("Missing node: "+op.id);
        if(!op.set||typeof op.set!=="object"||Array.isArray(op.set)||!Object.keys(op.set).length||
           Object.keys(op.set).some(k=>!["title","detail","system","parent"].includes(k)))throw Error("Invalid update fields");
        Object.assign(nodes[i],op.set);
      }else if(op.op==="remove_node"){
        if(i<0)throw Error("Missing node: "+op.id);
        if(edges.some(e=>e.from===op.id||e.to===op.id)||nodes.some(n=>n.parent===op.id))throw Error("Remove connected wires/children before deleting "+op.id);
        nodes.splice(i,1);
      }else if(op.op==="add_edge"||op.op==="remove_edge"){
        const e=asEdge(op),j=edges.findIndex(x=>x.from===e.from&&x.to===e.to&&x.kind===e.kind);
        if(op.op==="add_edge"){if(j>=0)throw Error("Wire already exists");edges.push(e);}
        else{if(j<0)throw Error("Wire does not exist");edges.splice(j,1);}
      }else throw Error("Unsupported patch operation "+String(op.op));
    }
    const updated=assertValid({nodes,edges});
    return {dsl:serialize(updated),before:original,after:parse(serialize(updated)),changes:diff(original,updated)};
  }
  function diff(before,after){
    const items=[],map=(values,key)=>new Map(values.map(v=>[key(v),v]));
    for(const [type,keyFn,a,b] of [["node",v=>v.id,before.nodes,after.nodes],["wire",v=>[v.from,v.to,v.kind].join(" -> "),before.edges,after.edges]]){
      const x=map(a,keyFn),y=map(b,keyFn);
      for(const id of new Set([...x.keys(),...y.keys()])){
        const l=x.get(id),r=y.get(id),left=l?(type==="node"?asNode(l):asEdge(l)):null,right=r?(type==="node"?asNode(r):asEdge(r)):null;
        if(JSON.stringify(left)!==JSON.stringify(right))items.push({type,id,before:left,after:right});
      }
    }
    return items;
  }
  return Object.freeze({VERSION,KINDS,isV1,parse,serialize,canonical,validate,render,patch,diff});
})();
if(typeof module!=="undefined"&&module.exports)module.exports=BreadboardCore;
