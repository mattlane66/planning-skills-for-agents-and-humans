const FIT=["strong","partial","weak","unknown"];

const seed=()=>({
  frame:{
    x:"Managers face one dense expense queue. Routine reviews feel slow and risky cases are easy to skim past.",
    y:"Routine approvals happen almost instantly while unusual expenses reliably interrupt attention.",
    m:"People need more guidance when unfamiliar or when risk is high; expertise should reduce presentation overhead without changing decision semantics."
  },
  criteria:[
    {id:"R1",text:"Routine approvals should take only a few seconds.",status:"accepted"},
    {id:"R2",text:"Unusual expenses must remain conspicuous.",status:"accepted"},
    {id:"R3",text:"Decision semantics stay stable across presentations.",status:"working"}
  ],
  candidates:[
    {id:"A",name:"Adaptive composition",desc:"One ReviewExpense capability and ReviewDecision model; context changes presentation.",fits:{R1:"strong",R2:"strong",R3:"strong"}},
    {id:"B",name:"Separate workflows",desc:"Novice and experienced reviewers get independent flows.",fits:{R1:"strong",R2:"partial",R3:"weak"}},
    {id:"C",name:"Recommendation first",desc:"AI recommends; detail expands when confidence or risk warrants.",fits:{R1:"strong",R2:"partial",R3:"partial"}}
  ],
  active:null,tab:"breadboard",quick:false,riskGate:false,undo:false,provisional:null,
  traceAff:null,traceCriterion:null,selectedFit:null,checked:[],slices:[],suggestions:false,
  hifi:null,hifiSelected:null,hifiEdits:{},
  changes:[{text:"Frame shaped"},{text:"R1–R3 selected"},{text:"Path A shaped"}]
});

let state=seed();

const $=(q,r=document)=>r.querySelector(q);
const $$=(q,r=document)=>Array.from(r.querySelectorAll(q));
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]));
const cBy=id=>state.candidates.find(c=>c.id===id);
const rBy=id=>state.criteria.find(r=>r.id===id);
const fitSymbol=v=>v==="strong"?"●":v==="partial"?"◐":v==="weak"?"○":"?";
const fitLabel=v=>v[0].toUpperCase()+v.slice(1);
const cycle=v=>FIT[(FIT.indexOf(v)+1)%FIT.length];
const addChange=(text,kind="")=>{state.changes.push({text,kind});state.changes=state.changes.slice(-9)};

const pages=()=>[
 {id:"queue",name:"Queue",state:"Frequent manager",hifi:true,systems:["Expense[]","ReviewerContext"].concat(state.riskGate?["RiskClassification"]:[]),aff:[
   {id:"open",name:"Open expense",to:["review:inspect","review:approve"],criteria:["R1"]},
   ...(state.quick?[{id:"quick",name:"Quick approve routine",to:state.riskGate?["confirmation:done","exception:explain"]:["confirmation:done"],criteria:["R1","R2"]}]:[])
 ]},
 {id:"review",name:"Review",state:"Expense selected",hifi:true,systems:["Expense","ReviewDecision"],aff:[
   {id:"inspect",name:"Inspect receipt",to:["review:approve","review:flag"],criteria:["R2"]},
   {id:"approve",name:"Approve",to:["confirmation:done"],criteria:["R1","R3"]},
   {id:"flag",name:"Flag",to:["exception:explain"],criteria:["R2"]}
 ]},
 {id:"exception",name:"Exception",state:"Policy risk",hifi:true,systems:["PolicyFlag","PolicyEvidence","ReviewDecision.reason"],aff:[
   {id:"explain",name:"Explain exception",to:["exception:approveX","exception:flagX"],criteria:["R2"]},
   {id:"approveX",name:"Approve exception",to:["confirmation:done"],criteria:["R3"]},
   {id:"flagX",name:"Flag exception",to:["confirmation:done"],criteria:["R2","R3"]}
 ]},
 {id:"confirmation",name:"Confirmation",state:"Decision persisted",hifi:true,systems:["ReviewDecision","AuditEvent"].concat(state.undo?["Reversal"]:[]),aff:[
   {id:"done",name:state.undo?"Undo decision":"Decision persisted",to:state.undo?["queue:open"]:[],criteria:["R3"].concat(state.undo?["R4"]:[])}
 ]}
];

const pageBy=id=>pages().find(p=>p.id===id);
const affByKey=k=>{const [p,a]=k.split(":");return pageBy(p)?.aff.find(x=>x.id===a)};
const label=k=>{const [p,a]=k.split(":");const pg=pageBy(p),af=pg?.aff.find(x=>x.id===a);return pg&&af?pg.name+" · "+af.name:k};

function render(){
  $("#app").innerHTML=
    '<header class="topbar"><div class="brand"><div class="mark">A</div><div><div>Adaptive App Builder</div><div class="crumb">Expense review · working model</div></div></div>'+
    '<div class="actions"><button class="btn quiet" data-action="reset">Reset demo</button>'+(state.active?'<button class="btn" data-action="back">← Matrix</button>':'')+'</div></header>'+
    '<main class="wrap">'+frameView()+(state.active?candidateView():homeView())+'</main>'+
    fitPopover()+hifiModal()+'<div id="toast" class="toast hidden"></div>';
  bind();
  if(state.active)requestAnimationFrame(drawWires);
}

function frameView(){
  return '<section class="surface pad"><div class="between"><div><div class="ey">Frame</div><div class="title">What transformation are we designing?</div></div><div class="sub">x → <b>f(?)</b> → y &nbsp; under M</div></div>'+
   '<div class="frame-grid">'+
   '<div class="frame-field"><div class="ey">x · current situation</div><textarea data-frame="x">'+esc(state.frame.x)+'</textarea></div>'+
   '<div class="frame-field"><div class="ey">y · desired outcome</div><textarea data-frame="y">'+esc(state.frame.y)+'</textarea></div>'+
   '<div class="frame-field"><div class="ey">M · working model</div><textarea data-frame="m">'+esc(state.frame.m)+'</textarea></div>'+
   '</div><div class="formula">x → <b>f(?)</b> → y &nbsp; under M</div></section>';
}

function homeView(){
  return '<div class="home-grid"><section class="surface pad">'+
   '<div class="between"><div><div class="ey">Solution matrix</div><div class="title">Criteria ↔ candidate solutions</div></div><div class="actions"><button class="btn" data-action="add-row">+ Requirement</button><button class="btn" data-action="add-col">+ Path</button></div></div>'+
   '<div class="sub" style="margin-top:5px">Edit the comparison directly. Candidate exploration can push back on the criteria.</div>'+
   '<div class="matrix-wrap">'+matrixTable()+'</div>'+provisionalView()+
   '</section><aside class="side">'+changeThread()+aiPanel()+'</aside></div>';
}

function matrixTable(){
  let h='<table><thead><tr><th class="criterion-cell">Criterion</th>';
  state.candidates.forEach(c=>{
    h+='<th class="candidate-head"><input class="editable candidate-name" data-cname="'+c.id+'" value="'+esc(c.name)+'">'+
      '<textarea class="editable candidate-desc" data-cdesc="'+c.id+'" rows="2">'+esc(c.desc)+'</textarea>'+
      '<button class="btn" style="width:100%;margin-top:4px" data-open="'+c.id+'">Open candidate →</button></th>';
  });
  h+='</tr></thead><tbody>';
  state.criteria.forEach(r=>{
    h+='<tr><td class="criterion-cell"><div class="criterion-row"><button class="btn quiet" style="padding:4px 6px" data-trace-r="'+r.id+'">'+r.id+'</button>'+
      '<input class="editable" data-rtext="'+r.id+'" value="'+esc(r.text)+'"><button class="status-pill" data-rstatus="'+r.id+'">'+r.status+'</button></div></td>';
    state.candidates.forEach(c=>{
      const v=c.fits[r.id]||"unknown";
      const delta=c.id==="A"&&r.id==="R2"&&state.quick&&!state.riskGate?"Strong → Weak":
                  c.id==="A"&&r.id==="R4"&&state.undo?"Weak → Strong":"";
      h+='<td><button class="fit '+v+(delta?' delta':'')+'" data-fit="'+c.id+':'+r.id+'"><span class="symbol">'+fitSymbol(v)+'</span><strong>'+esc(delta||fitLabel(v))+'</strong></button></td>';
    });
    h+='</tr>';
  });
  if(state.provisional){
    h+='<tr class="ghost-row"><td><div class="ghost-label"><span class="ghost-dot"></span><div><b>R?</b> '+esc(state.provisional.text)+'<div class="sub">Emerged from '+esc(state.provisional.origin)+'</div></div></div></td>'+
      '<td colspan="'+state.candidates.length+'"><div class="between"><div class="sub">This candidate introduced a consequence the current criteria do not judge.</div><div class="actions"><button class="btn primary" data-action="accept-r4">Accept</button><button class="btn" data-action="edit-r4">Edit</button><button class="btn" data-action="dismiss-r4">Dismiss</button></div></div></td></tr>';
  }
  return h+'</tbody></table>';
}

function provisionalView(){
  if(!state.provisional)return "";
  return '<div class="mini-panel" style="margin-top:10px"><div class="ey">Emergent criterion</div><div class="between" style="margin-top:5px"><div><div style="font-size:12px;font-weight:730">'+esc(state.provisional.text)+'</div><div class="sub">Origin: '+esc(state.provisional.origin)+'</div></div><div class="actions"><button class="btn primary" data-action="accept-r4">Accept</button><button class="btn" data-action="dismiss-r4">Dismiss</button></div></div></div>';
}

function changeThread(){
  return '<div class="mini-panel"><div class="ey">Change thread</div><div class="thread">'+state.changes.map(e=>'<span class="event '+(e.kind||"")+'">'+esc(e.text)+'</span>').join("")+'</div></div>';
}

function aiPanel(){
  let t="Change a candidate and I’ll reverse-fit it against the criteria.";
  if(state.quick&&!state.riskGate)t="R2 is now weak. Quick approve can bypass the risk interrupt.";
  if(state.provisional)t="This also introduced a new judging question: should committed approvals be recoverable?";
  if(state.riskGate&&rBy("R4")&&!state.undo)t="R2 is repaired. R4 is accepted but still weak in Path A.";
  if(state.undo)t="Path A now fits the accepted criteria again.";
  return '<div class="mini-panel"><div class="ey">AI</div><div class="insight">'+esc(t)+'</div>'+(state.quick?'<button class="btn" style="width:100%;margin-top:9px" data-open="A">Show affected behavior →</button>':'')+'</div>';
}

function candidateView(){
  const c=cBy(state.active);
  return '<section class="surface candidate-view"><div class="candidate-shell"><aside class="candidate-nav"><div class="ey">'+esc(c.id)+' · candidate</div>'+
   '<div class="title" style="font-size:15px;margin-top:4px">'+esc(c.name)+'</div><div class="sub" style="margin:5px 0 12px">'+esc(c.desc)+'</div>'+
   '<button class="navbtn '+(state.tab==="breadboard"?"active":"")+'" data-tab="breadboard">Behavior</button>'+
   '<button class="navbtn '+(state.tab==="slices"?"active":"")+'" data-tab="slices">Slices</button>'+
   '<div style="height:10px"></div><div class="ey">Candidate edits</div>'+
   (c.id==="A"?'<button class="btn primary" style="width:100%;margin-top:7px" data-action="quick" '+(state.quick?"disabled":"")+'>+ One-click approve</button>'+
   '<button class="btn" style="width:100%;margin-top:6px" data-action="risk" '+(!state.quick||state.riskGate?"disabled":"")+'>Add risk gate</button>'+
   '<button class="btn" style="width:100%;margin-top:6px" data-action="undo" '+(!rBy("R4")||state.undo?"disabled":"")+'>Add Undo</button>':'<div class="empty" style="margin-top:7px">Behavioral depth is seeded on Path A.</div>')+
   '</aside><div class="canvas">'+(state.tab==="breadboard"?breadboard(c):sliceView())+'</div></div></section>';
}

function breadboard(c){
  if(c.id!=="A")return '<div class="toolbar"><div><div class="ey">Breadboard</div><div class="title">'+esc(c.name)+'</div></div><button class="btn" data-action="back">← Matrix</button></div><div class="empty" style="margin-top:14px">The prototype focuses behavioral depth on Path A.</div>';
  return '<div class="toolbar"><div><div class="ey">Breadboard</div><div class="title">Places, affordances, wiring, system language</div></div><div class="actions"><button class="btn" data-action="clear-trace">Clear trace</button><button class="btn primary" data-action="ai-slices">AI spike · Suggest slices</button></div></div>'+
   '<div class="sub" style="margin-top:5px">Click an affordance to trace one-to-many wiring. Check affordances to define a slice.</div>'+
   '<div class="board-scroll"><div class="board" id="board"><svg class="wire-svg" id="wire-svg"></svg>'+pages().map(pageCard).join("")+'</div></div>'+
   traceSummary()+
   '<div class="ai-bar"><div class="ai-copy">'+reverseFitText()+'</div><button class="btn" data-action="save-slice">Save checked slice</button></div>'+
   (state.suggestions?suggestionCards():"");
}

function pageCard(pg){
  const implicated=state.traceCriterion&&pg.aff.some(a=>a.criteria.includes(state.traceCriterion));
  return '<div class="page-card '+(implicated?"criterion":"")+'" data-page="'+pg.id+'"><div class="page-head"><div><div class="ey">Page / state</div><div class="page-name">'+esc(pg.name)+'</div><div class="state">'+esc(pg.state)+'</div></div>'+
    '<button class="hifi-chip" data-hifi="'+pg.id+'">Hi-fi ↗</button></div>'+
    pg.aff.map(a=>affCard(pg,a)).join("")+
    '<div class="ey sys-title">System language</div><div class="chips">'+pg.systems.map(s=>'<span class="chip">'+esc(s)+'</span>').join("")+'</div></div>';
}

function affCard(pg,a){
  const k=pg.id+":"+a.id;
  const active=state.traceAff===k || (state.traceAff&&affByKey(state.traceAff)?.to.includes(k));
  const violate=(k==="queue:quick"&&state.quick&&!state.riskGate)||(k==="confirmation:done"&&rBy("R4")&&!state.undo);
  return '<div class="affordance '+(active?"active ":"")+(violate?"violate":"")+'" data-aff-box="'+k+'"><div class="aff-top"><button class="aff-btn" data-trace-aff="'+k+'">'+esc(a.name)+'</button>'+
    '<label class="slice-check"><input type="checkbox" data-check="'+k+'" '+(state.checked.includes(k)?"checked":"")+'> slice</label></div>'+
    '<div class="wire-tags">'+(a.to.length?a.to.map(t=>'<span class="wire-tag">→ '+esc(label(t))+'</span>').join(""):'<span class="wire-tag">terminal</span>')+'</div></div>';
}

function traceSummary(){
  if(state.traceAff){
    const a=affByKey(state.traceAff);
    return '<div class="trace-panel"><div class="ey">Wiring trace</div><div class="trace-path"><b>'+esc(label(state.traceAff))+'</b> → '+(a?.to.length?a.to.map(label).join(" + "):"terminal")+'</div></div>';
  }
  if(state.traceCriterion)return '<div class="trace-panel"><div class="ey">Criterion trace · '+state.traceCriterion+'</div><div class="trace-path">Highlighted behavior embodies or threatens this criterion.</div></div>';
  return "";
}

function reverseFitText(){
  if(!state.quick)return "<b>AI:</b> Change the candidate and I’ll reverse-fit it against the criteria.";
  if(state.quick&&!state.riskGate)return "<b>AI:</b> Quick approve improved speed but weakened R2. A risk gate is the smallest repair.";
  if(state.riskGate&&rBy("R4")&&!state.undo)return "<b>AI:</b> R2 is repaired. R4 now pushes back on the commitment boundary.";
  if(state.undo)return "<b>AI:</b> R2 and R4 are strong again. The candidate is coherent enough to slice.";
  return "<b>AI:</b> This candidate surfaced a recoverability question.";
}

function suggestions(){
  return [
   {name:"Routine approval",why:"Smallest visible end-to-end proof of fast routine review.",keys:["queue:open","review:approve","confirmation:done"]},
   {name:"Exception handling",why:"Keeps the PolicyFlag / PolicyEvidence risk boundary demoable.",keys:["review:flag","exception:explain","exception:approveX","confirmation:done"]},
   {name:"Adaptive expert review",why:"Tests adaptive presentation while preserving shared ReviewDecision semantics.",keys:state.quick?["queue:quick"].concat(state.riskGate?["exception:explain"]:[]).concat(["confirmation:done"]):["queue:open","review:approve"]}
  ];
}

function suggestionCards(){
  return '<div class="suggestions">'+suggestions().map((s,i)=>'<div class="suggestion"><div class="suggestion-title">'+esc(s.name)+'</div><p>'+esc(s.why)+'</p><div class="slice-meta">'+s.keys.map(label).join(" → ")+'</div><div class="actions" style="margin-top:8px"><button class="btn primary" data-use="'+i+'">Use</button><button class="btn" data-edit="'+i+'">Edit</button><button class="btn quiet" data-ignore="'+i+'">Ignore</button></div></div>').join("")+'</div>';
}

function sliceView(){
  const mine=state.slices.filter(s=>s.candidate===state.active);
  return '<div class="toolbar"><div><div class="ey">Vertical slices</div><div class="title">Human + AI boundaries</div></div><button class="btn primary" data-action="ai-slices">AI spike · Suggest slices</button></div>'+
    (state.suggestions?suggestionCards():"")+
    '<div class="slice-list">'+(mine.length?mine.map(s=>'<div class="slice"><div class="between"><div><div style="font-size:12px;font-weight:730">'+esc(s.name)+'</div><div class="slice-meta">'+esc(s.source)+'</div></div><button class="btn quiet danger" data-del="'+s.id+'">Delete</button></div><div class="sub" style="margin-top:6px">'+s.keys.map(label).join(" → ")+'</div></div>').join(""):'<div class="empty">No slices yet. Define one manually or ask the AI for suggestions.</div>')+'</div>';
}

function fitPopover(){
  if(!state.selectedFit)return "";
  const [cid,rid]=state.selectedFit.split(":"),c=cBy(cid),r=rBy(rid);
  if(!c||!r)return "";
  let cause="This is the current fit judgment.",jump="";
  if(cid==="A"&&rid==="R2"&&state.quick&&!state.riskGate){cause="Quick approve can commit before PolicyFlag has a chance to interrupt the reviewer.";jump='<button class="btn primary" data-jump="R2">Show in breadboard</button>'}
  if(cid==="A"&&rid==="R4"&&rBy("R4")&&!state.undo){cause="Path A commits ReviewDecision without a reversal affordance.";jump='<button class="btn primary" data-jump="R4">Show in breadboard</button>'}
  return '<div class="cell-pop"><div class="between"><div><div class="ey">'+rid+' × '+cid+'</div><div style="font-weight:740;font-size:12px;margin-top:3px">'+fitLabel(c.fits[rid]||"unknown")+'</div></div><button class="btn quiet" data-action="close-fit">×</button></div>'+
    '<div class="sub" style="margin-top:8px">'+esc(cause)+'</div><div class="actions" style="margin-top:10px">'+jump+'<button class="btn" data-cycle="'+cid+':'+rid+'">Change fit</button></div></div>';
}

function hifiModal(){
  if(!state.hifi)return "";
  const screen=state.hifi;
  return '<div class="modal-backdrop"><div class="modal"><div class="modal-head"><div><div class="ey">Targeted fidelity spike</div><div style="font-weight:750;font-size:13px">'+esc(pageBy(screen)?.name||screen)+' · Expense review</div></div><div class="actions"><button class="btn" data-action="reconcile">Reconcile learning</button><button class="btn" data-action="close-hifi">Close</button></div></div>'+
   '<div class="editor"><aside class="layers"><div class="ey">Elements</div>'+layerList(screen).map(x=>'<button class="layer '+(state.hifiSelected===x.id?"active":"")+'" data-layer="'+x.id+'">'+x.label+'</button>').join("")+'</aside>'+
   '<div class="stage">'+mockScreen(screen)+'</div><aside class="inspector">'+inspector()+'</aside></div></div></div>';
}

function layerList(screen){
  const common=[{id:"brand",label:"Brand"},{id:"search",label:"Search"},{id:"user",label:"User context"}];
  const per={
    queue:[{id:"title",label:"Queue title"},{id:"expense",label:"Expense row"},{id:"quick",label:"Quick approve"}],
    review:[{id:"title",label:"Review title"},{id:"receipt",label:"Receipt summary"},{id:"flag",label:"Flag"},{id:"approve",label:"Approve"}],
    exception:[{id:"title",label:"Review title"},{id:"warning",label:"Policy warning"},{id:"evidence",label:"Evidence"},{id:"flagX",label:"Flag"},{id:"approveX",label:"Approve exception"}],
    confirmation:[{id:"success",label:"Confirmation"},{id:"undo",label:"Undo"}]
  };
  return common.concat(per[screen]||[]);
}

function editKey(id){return state.hifi+":"+id}
function edit(id){return state.hifiEdits[editKey(id)]||{}}
function txt(id,fallback){return edit(id).text??fallback}
function ui(id,html,cls=""){
  const e=edit(id),style=(e.emphasis==="quiet"?"opacity:.5;":"")+(e.emphasis==="strong"?"font-weight:800;":"")+(e.hidden?"visibility:hidden;":"")+(e.align?"text-align:"+e.align+";":"");
  return '<div class="ui '+(state.hifiSelected===id?"selected ":"")+cls+'" data-ui="'+id+'" style="'+style+'">'+html+'</div>';
}

function mockScreen(screen){
  let main="";
  if(screen==="queue")main=ui("title",'<div class="ey">Expert review</div><div style="font-size:20px;font-weight:760">'+esc(txt("title","Review expenses"))+'</div>')+
    ui("expense",'<div class="mock-card"><div class="sub">HOTEL</div><div style="font-weight:740">Acme offsite</div><div>$1,842</div>'+(state.quick?'<button class="mock-btn primary" style="margin-top:10px">'+esc(txt("quick","Quick approve"))+'</button>':'')+'</div>');
  if(screen==="review")main=ui("title",'<div class="ey">Expense review</div><div style="font-size:20px;font-weight:760">'+esc(txt("title","Acme offsite"))+'</div>')+
    ui("receipt",'<div class="mock-card" style="margin-top:12px"><div class="sub">Total</div><div style="font-size:28px;font-weight:760">$1,842</div><div class="sub">Receipt attached ✓</div></div>')+
    '<div class="mock-actions">'+ui("flag",'<button class="mock-btn">'+esc(txt("flag","Flag"))+'</button>')+ui("approve",'<button class="mock-btn primary">'+esc(txt("approve","Approve"))+'</button>')+'</div>';
  if(screen==="exception")main=ui("title",'<div class="ey">Expense review</div><div style="font-size:20px;font-weight:760">'+esc(txt("title","Acme offsite"))+'</div><div class="sub">Hotel · Sep 18 · $1,842</div>')+
    ui("warning",'<div class="mock-warning" style="margin-top:12px"><div style="font-weight:760">'+esc(txt("warning","Rate is above policy"))+'</div><div class="sub">$412/night · normal threshold $325</div></div>')+
    ui("evidence",'<div class="mock-card" style="margin-top:10px"><div class="ey">Why this is unusual</div><div class="sub" style="margin-top:5px">'+esc(txt("evidence","Hotel rate is 27% above the normal threshold."))+'</div></div>')+
    '<div class="mock-actions">'+ui("flagX",'<button class="mock-btn">'+esc(txt("flagX","Flag"))+'</button>')+ui("approveX",'<button class="mock-btn primary">'+esc(txt("approveX","Approve exception"))+'</button>')+'</div>';
  if(screen==="confirmation")main=ui("success",'<div class="mock-card"><div class="ey">Saved</div><div style="font-size:20px;font-weight:760">'+esc(txt("success","Expense approved"))+'</div><div class="sub">Decision recorded.</div>'+(state.undo?'<button class="mock-btn" style="margin-top:12px">'+esc(txt("undo","Undo decision"))+'</button>':'')+'</div>');
  return '<div class="mock"><div class="mock-top">'+ui("brand",'<b>'+esc(txt("brand","Ledgerly"))+'</b>')+ui("search",'<span class="sub">'+esc(txt("search","Search expenses…"))+'</span>')+ui("user",'<span class="sub">'+esc(txt("user","Maya · Manager"))+'</span>')+'</div>'+
    '<div class="mock-body"><nav class="mock-nav"><div class="ey">Review</div><div class="ui" style="margin-top:8px">Expenses</div><div class="ui">History</div><div class="ui">Policy</div></nav><main class="mock-main">'+main+'</main></div></div>';
}

function inspector(){
  if(!state.hifiSelected)return '<div class="ey">Inspector</div><div class="empty" style="margin-top:10px">Select any visible element or layer.</div>';
  const e=edit(state.hifiSelected);
  return '<div class="ey">Selected element</div><div style="font-weight:750;font-size:12px;margin-top:4px">'+esc(state.hifiSelected)+'</div>'+
   '<div class="control"><label>Text / label</label><input data-inspector="text" value="'+esc(e.text??state.hifiSelected)+'"></div>'+
   '<div class="control"><label>Emphasis</label><select data-inspector="emphasis"><option value="normal">Normal</option><option value="strong" '+(e.emphasis==="strong"?"selected":"")+'>Strong</option><option value="quiet" '+(e.emphasis==="quiet"?"selected":"")+'>Quiet</option></select></div>'+
   '<div class="control"><label>Align</label><select data-inspector="align"><option value="left">Left</option><option value="center" '+(e.align==="center"?"selected":"")+'>Center</option><option value="right" '+(e.align==="right"?"selected":"")+'>Right</option></select></div>'+
   '<div class="actions" style="margin-top:12px"><button class="btn" data-action="earlier">Earlier</button><button class="btn" data-action="later">Later</button></div>'+
   '<button class="btn" style="width:100%;margin-top:8px" data-action="toggle-ui">'+(e.hidden?"Show":"Hide")+'</button>';
}

function drawWires(){
  const board=$("#board"),svg=$("#wire-svg"); if(!board||!svg)return;
  const br=board.getBoundingClientRect(); svg.setAttribute("width",board.scrollWidth);svg.setAttribute("height",board.scrollHeight);svg.innerHTML="";
  pages().forEach(pg=>pg.aff.forEach(a=>{
    const source=$('[data-aff-box="'+pg.id+":"+a.id+'"]');if(!source)return;
    const sr=source.getBoundingClientRect();
    a.to.forEach(t=>{
      const target=$('[data-aff-box="'+t+'"]');if(!target)return;
      const tr=target.getBoundingClientRect(),x1=sr.right-br.left,y1=sr.top-br.top+sr.height/2,x2=tr.left-br.left,y2=tr.top-br.top+tr.height/2,mid=(x1+x2)/2;
      const path=document.createElementNS("http://www.w3.org/2000/svg","path");
      path.setAttribute("d","M "+x1+" "+y1+" C "+mid+" "+y1+", "+mid+" "+y2+", "+x2+" "+y2);
      const sk=pg.id+":"+a.id;
      if(state.traceAff===sk || (state.traceAff&&affByKey(state.traceAff)?.to.includes(t)))path.classList.add("active");
      if(sk==="queue:quick"&&state.quick&&!state.riskGate)path.classList.add("violate");
      svg.appendChild(path);
    });
  }));
}

function toast(msg){const t=$("#toast");if(!t)return;t.textContent=msg;t.classList.remove("hidden");clearTimeout(window.__toast);window.__toast=setTimeout(()=>t.classList.add("hidden"),1400)}

function quick(){
  if(state.quick)return;
  state.quick=true;cBy("A").fits.R2="weak";
  state.provisional={text:"A committed approval must be recoverable.",origin:"Path A · Quick approve affordance"};
  addChange("Quick approve added","hot");addChange("R2 Strong → Weak","hot");addChange("R? suggested","hot");
  state.traceAff="queue:quick";render();toast("R2 weakened; new criterion surfaced");
}
function acceptR4(){
  if(!state.provisional)return;
  state.criteria.push({id:"R4",text:state.provisional.text,status:"accepted"});
  cBy("A").fits.R4="weak";cBy("B").fits.R4="strong";cBy("C").fits.R4="partial";
  state.provisional=null;addChange("R4 accepted");addChange("Path A re-evaluated","hot");render();toast("R4 accepted and candidates re-evaluated");
}
function risk(){
  if(!state.quick||state.riskGate)return;
  state.riskGate=true;cBy("A").fits.R2="strong";addChange("Risk gate added","good");addChange("R2 Weak → Strong","good");state.traceAff="queue:quick";render();toast("R2 restored");
}
function undo(){
  if(!rBy("R4")||state.undo)return;
  state.undo=true;cBy("A").fits.R4="strong";addChange("Undo added","good");addChange("R4 Weak → Strong","good");state.traceCriterion="R4";render();toast("R4 restored");
}
function jump(rid){state.active="A";state.tab="breadboard";state.traceCriterion=rid;state.traceAff=rid==="R2"&&state.quick?"queue:quick":rid==="R4"?"confirmation:done":null;state.selectedFit=null;render()}
function saveSlice(name,keys,source){state.slices.push({id:"S"+(state.slices.length+1),candidate:state.active,name,keys:[...keys],source});state.tab="slices";render();toast("Slice saved")}

function bind(){
  $$("[data-frame]").forEach(el=>el.oninput=e=>state.frame[e.target.dataset.frame]=e.target.value);
  $$("[data-rtext]").forEach(el=>el.oninput=e=>{const r=rBy(e.target.dataset.rtext);if(r)r.text=e.target.value});
  $$("[data-cname]").forEach(el=>el.oninput=e=>{const c=cBy(e.target.dataset.cname);if(c)c.name=e.target.value});
  $$("[data-cdesc]").forEach(el=>el.oninput=e=>{const c=cBy(e.target.dataset.cdesc);if(c)c.desc=e.target.value});
  $$("[data-open]").forEach(b=>b.onclick=()=>{state.active=b.dataset.open;state.tab="breadboard";state.selectedFit=null;render()});
  $$("[data-fit]").forEach(b=>b.onclick=()=>{state.selectedFit=b.dataset.fit;render()});
  $$("[data-rstatus]").forEach(b=>b.onclick=()=>{const r=rBy(b.dataset.rstatus);r.status=r.status==="accepted"?"working":"accepted";render()});
  $$("[data-trace-r]").forEach(b=>b.onclick=()=>jump(b.dataset.traceR));
  $$("[data-tab]").forEach(b=>b.onclick=()=>{state.tab=b.dataset.tab;render()});
  $$("[data-trace-aff]").forEach(b=>b.onclick=()=>{state.traceAff=b.dataset.traceAff;state.traceCriterion=null;render()});
  $$("[data-check]").forEach(ch=>ch.onchange=e=>{const k=e.target.dataset.check;if(e.target.checked&&!state.checked.includes(k))state.checked.push(k);if(!e.target.checked)state.checked=state.checked.filter(x=>x!==k)});
  $$("[data-hifi]").forEach(b=>b.onclick=()=>{state.hifi=b.dataset.hifi;state.hifiSelected=null;render()});
  $$("[data-use]").forEach(b=>b.onclick=()=>{const s=suggestions()[+b.dataset.use];saveSlice(s.name,s.keys,"AI suggestion")});
  $$("[data-edit]").forEach(b=>b.onclick=()=>{const s=suggestions()[+b.dataset.edit];state.checked=[...s.keys];state.tab="breadboard";state.suggestions=false;render();toast("Suggestion loaded into manual selection")});
  $$("[data-ignore]").forEach(b=>b.onclick=()=>{state.suggestions=false;render()});
  $$("[data-del]").forEach(b=>b.onclick=()=>{state.slices=state.slices.filter(s=>s.id!==b.dataset.del);render()});
  $$("[data-cycle]").forEach(b=>b.onclick=()=>{const [cid,rid]=b.dataset.cycle.split(":"),c=cBy(cid);c.fits[rid]=cycle(c.fits[rid]||"unknown");state.selectedFit=null;render()});
  $$("[data-jump]").forEach(b=>b.onclick=()=>jump(b.dataset.jump));
  $$("[data-layer]").forEach(b=>b.onclick=()=>{state.hifiSelected=b.dataset.layer;render()});
  $$("[data-ui]").forEach(el=>el.onclick=e=>{e.stopPropagation();state.hifiSelected=el.dataset.ui;render()});
  $$("[data-inspector]").forEach(el=>{const ev=el.tagName==="SELECT"?"onchange":"oninput";el[ev]=e=>{const k=editKey(state.hifiSelected);state.hifiEdits[k]={...(state.hifiEdits[k]||{}),[e.target.dataset.inspector]:e.target.value};render()}});
  $$("[data-action]").forEach(b=>b.onclick=()=>act(b.dataset.action));
}
function act(a){
  if(a==="reset"){state=seed();render()}
  if(a==="back"){state.active=null;state.selectedFit=null;render()}
  if(a==="add-row"){const id="R"+(state.criteria.length+1);state.criteria.push({id,text:"New criterion",status:"working"});state.candidates.forEach(c=>c.fits[id]="unknown");render()}
  if(a==="add-col"){const id="P"+(state.candidates.length+1),fits={};state.criteria.forEach(r=>fits[r.id]="unknown");state.candidates.push({id,name:"New path",desc:"Describe a materially different approach.",fits});render()}
  if(a==="accept-r4")acceptR4();
  if(a==="dismiss-r4"){state.provisional=null;addChange("R? dismissed");render()}
  if(a==="edit-r4"){const v=prompt("Edit provisional criterion",state.provisional?.text||"");if(v){state.provisional.text=v;render()}}
  if(a==="close-fit"){state.selectedFit=null;render()}
  if(a==="quick")quick(); if(a==="risk")risk(); if(a==="undo")undo();
  if(a==="clear-trace"){state.traceAff=null;state.traceCriterion=null;render()}
  if(a==="ai-slices"){state.suggestions=true;render()}
  if(a==="save-slice"){if(!state.checked.length)return toast("Check at least one affordance");saveSlice("Manual slice "+(state.slices.length+1),state.checked,"Human selected")}
  if(a==="close-hifi"){state.hifi=null;state.hifiSelected=null;render()}
  if(a==="reconcile"){addChange("Hi-fi learning ready to reconcile");state.hifi=null;state.hifiSelected=null;render();toast("Learning returned to shaping model")}
  if(a==="toggle-ui"){const k=editKey(state.hifiSelected),e=state.hifiEdits[k]||{};state.hifiEdits[k]={...e,hidden:!e.hidden};render()}
  if(a==="earlier"||a==="later")toast((a==="earlier"?"Move earlier":"Move later")+" recorded for this spike");
}

render();
window.__app={get state(){return state},quick,acceptR4,risk,undo,render};
