import './test-agent-bridge.mjs';
import './test-breadboard-core.mjs';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { JSDOM, VirtualConsole } from 'jsdom';

const html = readFileSync(new URL('./index.html', import.meta.url), 'utf8');
const errors = [];
const consoleCapture = new VirtualConsole();
consoleCapture.on('jsdomError', error => errors.push(error.message));
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://board.test/', virtualConsole: consoleCapture });
const { window: w } = dom;
const run = source => w.eval(source);
assert.equal(errors.length, 0, errors.join('\n'));
assert.equal(run('M.options.length'), 4);
assert.equal(run('M.schema_version'), 3);
assert.equal(run('M.reqs[0].id'), 'R1');
assert.equal(run('M.reqs[0].status'), 'Must-have');

assert.equal(run('traceInfo(M.stories[2],M.options[3]).valid'), true, 'supported D path must really connect');
assert.equal(run('traceInfo(M.stories[2],M.options[0]).valid'), false, 'other options must not inherit D tracing');
assert.ok(run('traceInfo(M.stories[0],M.options[3]).errors.length') > 0, 'broken path cannot silently pass');

const exported = run('planningFiles()');
assert.equal(exported.length, 6, 'frame, shaping and four candidate breadboards; no selected build scope');
assert.ok(exported.every(([name, body]) => name.startsWith('planning/') && body.includes('draft')));
assert.ok(exported.every(([name, body]) => !name.endsWith('04-slices.md')));
assert.ok(exported.filter(([name]) => name.includes('candidate-')).length === 4);
assert.ok(!exported.find(([name]) => name.includes('candidate-A'))[1].includes('from the board\'s story path'));
const shaping = exported.find(([name]) => name.endsWith('02-shaping.md'))[1];
assert.match(shaping, /- Status: exploring/);
assert.match(shaping, /\| R1 \| Work that has not been approved never starts \| Must-have \|/);
assert.doesNotMatch(shaping, /\|\s*❓\s*\|/, 'formal fit must use binary values');

run('M.pick="D"; M.why="Candidate D is strongest"');
assert.ok(run('decisionIssues().length') > 0, 'no acceptance with unknown appetite or requirements');
assert.equal(run('M.selectionAuthority'), 'Working');
assert.ok(run('planningFiles().find(([name])=>name.endsWith("02-shaping.md"))[1].includes("- Status: decision-ready")'));

assert.throws(() => run('norm({name:"Unsafe",options:[{id:"A",dsl:""},{id:"A",dsl:""}]})'), /Duplicate/);
assert.throws(() => run('norm({name:"Unsafe",options:[{id:"A",dsl:""}],reqs:[{id:"R1",text:"a"},{id:"R1",text:"b"}]})'), /Invalid requirement IDs/);
assert.match(run('draw({dsl:"P1 | place | A | | app\\nP1 -> P1 : foo ~ M0 0 \\" onclick=alert(1) @ 2,2"},null,"bad").html'), /<svg/);

// Story IDs are distinct from breadboard stores.
assert.match(run('M.stories[0].id'), /^SC-/);
run('M.reqs[0].star=false;M.reqs[0].status="Core goal"');
const faithful = run('planningFiles()');
const shaping2 = faithful.find(([path])=>path.endsWith('02-shaping.md'))[1];
const optionA = faithful.find(([path])=>path.endsWith('03-candidate-A-breadboard.md'))[1];
assert.match(shaping2, /\| R1 \| Work that has not been approved never starts \| Core goal \|/);
assert.match(shaping2, /\| A-P1 \|/);
assert.match(optionA, /\| A-P1 \|/);

// Compare thumbnails shrink fully; Paths retains an inspectable, scrollable minimum.
run('T.top="shape";T.sub="board";T.view="cmp";render()');
const comparison = w.document.querySelector('.cm .fb');
assert.ok(comparison);
Object.defineProperty(comparison.parentElement,'clientWidth',{value:Number(comparison.dataset.w)*.2,configurable:true});
run('fit()');
assert.ok(Math.abs(Number(comparison.firstChild.style.transform.match(/scale\(([^)]+)\)/)[1])-.2)<.001);
run('T.view="paths";render()');
const main = w.document.querySelector('#dia .fb');
Object.defineProperty(main.parentElement,'clientWidth',{value:Number(main.dataset.w)*.2,configurable:true});
run('fit()');
assert.ok(Number(main.firstChild.style.transform.match(/scale\(([^)]+)\)/)[1])>=.58);

// Problem changes invalidate previous selection.
run('M.selectionAuthority="Accepted";T.top="shape";T.sub="board";render()');
const problem = w.document.querySelector('textarea[data-l="problem"]');
problem.value='Changed problem definition';
problem.dispatchEvent(new w.Event('input',{bubbles:true}));
assert.equal(run('M.selectionAuthority'),'Working');

// Product impact is read-only evidence, not a planning authority.
run('M.product_status={schema_version:1,kind:"ShapingBoardProductStatus",product:"Sample",verdict:"DRIFT",impacts:[{id:"INV-1",title:"Draft isolation",status:"DRIFT",statement:"Failed saves preserve state",refs:["R1"],changed_paths:["src/profile.py"],reason:"Trusted regression",scenarios:[{scenario:"SC-1",case:"failed-save",status:"DRIFT"}]}],unmapped_changed_paths:[]};T.top="review";render()');
assert.match(w.document.querySelector('main').textContent,/Draft isolation/);
assert.match(w.document.querySelector('main').textContent,/Failed saves preserve state/);
assert.match(w.document.querySelector('main').textContent,/R1/);
assert.match(w.document.querySelector('main').textContent,/DRIFT/);


 // Automatic reports are advisory, commit-scoped and fail closed.
const sha='a'.repeat(40),otherSha='b'.repeat(40);
const auto={schema_version:1,kind:'ShapingBoardProductStatus',product:'DWC Requests',verdict:'PASS',
 revision:sha,generated_at:new Date().toISOString(),
 impacts:[{id:'INV-1',title:'Approved isolation',status:'PASS',statement:'Preserve draft',
 refs:['R1'],changed_paths:['src/profile.py'],scenarios:[{scenario:'SC-1',case:'save',status:'PASS'}]}],
 unmapped_changed_paths:[],accepted_contract_changes:[],bindings_changed:false,trusted_baseline_missing:false};
assert.equal(run('validateStatusReport('+JSON.stringify(auto)+','+JSON.stringify(sha)+').verdict'),'PASS');
assert.throws(()=>run('validateStatusReport('+JSON.stringify(auto)+','+JSON.stringify(otherSha)+')'),/revision/);
assert.throws(()=>run('validateStatusReport('+JSON.stringify({...auto,generated_at:new Date(Date.now()-73*3600000).toISOString()})+','+JSON.stringify(sha)+')'),/72 hours/);
assert.throws(()=>run('validateStatusReport('+JSON.stringify({...auto,impacts:[]})+','+JSON.stringify(sha)+')'),/PASS without/);
assert.throws(()=>run('validateStatusReport('+JSON.stringify({...auto,impacts:[{...auto.impacts[0],scenarios:[]}]})+','+JSON.stringify(sha)+')'),/PASS without/);
assert.throws(()=>run('checkFeedConfig("http://untrusted.test/feed.json","owner/repo","main")'),/HTTPS/);
assert.throws(()=>run('checkFeedConfig("https://untrusted.test/feed.json?token=secret","owner/repo","main")'),/HTTPS/);
run('M.name="DWC Requests";M.status_feed={url:"https://feed.test/product-status.json",repo:"owner/repo",ref:"main"};M.product_status={verdict:"PASS"};feedRuntime.state="unavailable";feedRuntime.projectId=M.project_id;T.top="review";render()');
assert.equal(run('currentStatus()'),null,'failed refresh must hide a cached PASS');
assert.doesNotMatch(w.document.querySelector('main').textContent,/Covered check passed/);
w.fetch=async url=>new URL(url).hostname === 'api.github.com'?{ok:true,json:async()=>({sha})}:{ok:true,text:async()=>JSON.stringify(auto)};
await run('refreshStatusFeed()');
assert.equal(run('feedRuntime.state'),'current');
assert.equal(run('currentStatus().verdict'),'PASS');
assert.match(w.document.querySelector('main').textContent,/Approved isolation/);
assert.match(w.document.querySelector('main').textContent,/a{40}/);
w.fetch=async url=>new URL(url).hostname === 'api.github.com'?{ok:true,json:async()=>({sha:otherSha})}:{ok:true,text:async()=>JSON.stringify(auto)};
await run('refreshStatusFeed()');
assert.equal(run('feedRuntime.state'),'unavailable','outdated commit must not stay green');
assert.equal(run('currentStatus()'),null);
assert.doesNotMatch(w.document.querySelector('main').textContent,/Covered check passed/);
assert.match(w.document.querySelector('main').textContent,/Unverified/);
const portableAuto=run('(()=>{const {product_status,status_feed,...portable}=M;return portable})()');
assert.equal(portableAuto.status_feed,undefined);
run('delete M.status_feed;M.product_status=null;resetStatusFeed();render()');

// End-to-end Markdown import -> UI -> exporter -> real repo publisher contract.
const {mkdtempSync,mkdirSync,writeFileSync,readFileSync:read} = await import('node:fs');
const {tmpdir} = await import('node:os');
const {join,resolve,dirname} = await import('node:path');
const {fileURLToPath} = await import('node:url');
const {spawnSync} = await import('node:child_process');
const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const tmp = mkdtempSync(join(tmpdir(),'shaping-board-'));
const boardfile = join(tmp,'imported.board.json');
let cmd=spawnSync('python3',[join(root,'scripts/build_shaping_board_data.py'),'--planning-dir',join(root,'examples/simple-grocery-list'),'--output',boardfile],{encoding:'utf8'});
assert.equal(cmd.status,0,cmd.stderr||cmd.stdout);
const imported = JSON.parse(read(boardfile,'utf8'));
assert.deepEqual(imported.reqs.map(x=>x.id),['R0','R1','R2','R3','R4','R5']);
run('M=norm('+JSON.stringify(imported)+')');
assert.equal(run('M.reqs[0].status'),'Core goal');
assert.equal(run('M.reqs[0].auth'),'Accepted');
assert.equal(run('M.appetiteAuthority'),'Accepted');
const generated = run('planningFiles()');
for(const [name,content] of generated) {
 const file=join(tmp,name);
 mkdirSync(dirname(file),{recursive:true});
 writeFileSync(file,content,'utf8');
}
cmd=spawnSync('python3',[join(root,'scripts/publish_shaped_work.py'),'--planning-dir',join(tmp,'planning'),'--check'],{encoding:'utf8'});
assert.equal(cmd.status,0,'Canonical planning publisher rejected exported Markdown:\n'+cmd.stdout+'\n'+cmd.stderr);

assert.equal(errors.length, 0, errors.join('\n'));

// AI Workspace uses existing exports and does not manufacture accepted scope.
const aiFiles=run('bridgePackageFiles()');
assert.ok(aiFiles.some(([name])=>name==='planning/shaping.board.json'));
assert.match(aiFiles.find(([name])=>name==='planning/BREADBOARD-LANGUAGE.md')[1],/BreadboardPatch/);
assert.ok(aiFiles.some(([name])=>name==='planning/AI-START-HERE.md'));
assert.ok(aiFiles.some(([name])=>name==='README-SHAPING-WORKSPACE.md'));
assert.ok(aiFiles.find(([name])=>name==='planning/AI-START-HERE.md')[1].includes('planning-router'));
assert.ok(aiFiles.find(([name])=>name==='README-SHAPING-WORKSPACE.md')[1].includes('NOT a connected AI chat'));
assert.match(run('bridgePrompt()'),/STOP and list what is missing|Do not alter acceptance authority/);
run('T.top="workspace";render()');
assert.match(w.document.querySelector('main').textContent,/AI Workspace/);
assert.ok(w.document.querySelector('[data-act="bridge-package"]'));
run('T.top="ontology";render()');
assert.match(w.document.querySelector('main').textContent,/working ontology/);
assert.ok(w.document.querySelector('[data-ontology-rq="0"]'));

// Same-project AI revisions must be compared, never silently treated as accepted.
run('M.project_id="bridge-test"; M.selectionAuthority="Accepted";M.frameAuthority="Accepted";M.appetiteAuthority="Accepted"; M.reqs.forEach(r=>r.auth="Accepted"); B.proposal=norm(clone(M)); B.proposal.reqs[0].text="Proposed requirement"; B.proposal.selectionAuthority="Accepted"; B.proposal.product_status={verdict:"PASS"}');
assert.equal(run('bridgeDiff().map(s=>s.id).join(",")'),'design');
assert.match(run('bridgeProposal()'),/Apply reviewed section as Working/);
assert.match(run('bridgeProposal()'),/Proposed requirement/);
run('bridgeApply("design")');
assert.equal(run('M.reqs[0].text'),'Proposed requirement');
assert.equal(run('M.reqs.every(r=>r.auth==="Working")'),true);
assert.equal(run('M.selectionAuthority'),'Working');
assert.equal(run('M.product_status'),undefined);
assert.equal(run('bridgeDiff().length'),0);
run('B.proposal=norm(clone(M));B.proposal.problem=["Updated problem"];B.proposal.appetite="2 weeks"; B.proposal.frameAuthority="Accepted"; B.proposal.appetiteAuthority="Accepted"');
assert.equal(run('bridgeDiff().map(s=>s.id).join(",")'),'frame,appetite');
run('bridgeApply("frame")');
assert.equal(run('M.frameAuthority'),'Working');
run('bridgeApply("appetite")');
assert.equal(run('M.appetiteAuthority'),'Working');
run('B.proposal.project_id="another-project"');
assert.equal(run('bridgeDiff().length'),0);


// AI proposal is checked before norm() could silently coerce or pad malformed values.
run('M=norm(clone(E)); M.project_id="hardened-test";B.proposal=null;M.selectionAuthority="Accepted"');
const safe=run('bridgePortable()');
const importedSafe=JSON.stringify(safe);
assert.equal(run('bridgeValidateProposal('+importedSafe+').project_id'),"hardened-test");
const invalidCases=[
 [x=>{[x.options[0],x.options[1]]=[x.options[1],x.options[0]]},/options: candidate IDs or order changed/],
 [x=>{x.options.push({...x.options[0],id:"E"})},/options: candidate IDs or order changed/],
 [x=>{x.reqs[0].f="yyyyy"},/reqs\[0\]\.f: expected exactly/],
 [x=>{x.reqs[0].l[0]=[1,2]},/reqs\[0\]\.l\[0\]: expected text/],
 [x=>{x.reqs[0].part_refs={UNKNOWN:["P1"]}},/reqs\[0\]\.part_refs\.UNKNOWN: unknown candidate ID/],
 [x=>{x.stories[0].fit="aaa0"},/stories\[0\]\.fit: expected exactly/],
 [x=>{x.stories[0].paths={UNKNOWN:"P1 P2"}},/stories\[0\]\.paths\.UNKNOWN: unknown candidate ID/],
 [x=>{x.project_id="other"},/project_id: must match/],
 [x=>{x.reqs[0].id="R2"},/reqs: duplicate requirement ID/],
 [x=>{x.things[0].name={bad:true}},/things\[0\]\.name: expected text/],
 [x=>{x.pick="E"},/pick: must identify a candidate/]
];
for(const [mutate,error] of invalidCases){
 const value=structuredClone(safe);mutate(value);
 assert.throws(()=>run('bridgeValidateProposal('+JSON.stringify(value)+')'),error);
}
const huge=structuredClone(safe);
huge.reqs[0].text="Very long proposed requirement: "+"X".repeat(6000);
run('B.proposal=bridgeValidateProposal('+JSON.stringify(huge)+')');
const diffHtml=run('bridgeProposal()');
assert.ok(diffHtml.includes("X".repeat(6000)),"entire 6,000-character change must be inspectable");
assert.ok(!diffHtml.includes("… (preview shortened"),"full preview must not hide any content");
assert.match(diffHtml,/reqs · R1/);
assert.equal(run('bridgeEntries(bridgeDiff()[0]).filter(row=>row.label==="reqs · R1").length'),1);
assert.equal(run('M.reqs[0].text'),safe.reqs[0].text,"untrusted proposal is not applied automatically");
run('bridgeApply("design")');
assert.equal(run('M.reqs[0].text'),huge.reqs[0].text);
assert.equal(run('M.reqs.every(r=>r.auth==="Working")'),true);
assert.equal(run('M.selectionAuthority'),"Working");
run('M.reqs[0].part_refs={D:"bad"}; M.pick="D"; T.top="ontology";render()');
assert.match(w.document.querySelector('main').textContent,/Product map/,"invalid legacy part_refs should not crash the view");

// Fixed-language integration: render, diff, stale-revision guard and human Working gate.
const fixedModel=[
 'version: breadboard/v1',
 'P1 | place | Request form | Enter request | app',
 'U1 | ui | Submit | Click send | app | in=P1',
 'N1 | nonui | Validate | Check request | backend',
 'U1 -> N1 : control',
 ''
].join('\n');
run('M.options[0].dsl='+JSON.stringify(fixedModel)+';T.top="shape";T.sub="board";T.view="paths";T.opt=0;render()');
const fixedWorkspace=run('bridgePackageFiles()');
assert.equal(fixedWorkspace.find(([name])=>name==='planning/breadboard-A.dsl')[1],fixedModel);
assert.equal(run('parse(M.options[0].dsl).err.length'),0);

const mappedGraph=run('parse(M.options[0].dsl)');
assert.equal(Array.from(mappedGraph.nodes,n=>n.i).join(','),'P1,U1,N1','typed IDs must project into existing Board consumers');
assert.equal(mappedGraph.edges[0].a,'U1');
assert.equal(mappedGraph.edges[0].b,'N1');
const typedStory={id:'SC-LIVE',text:'Submit then validate',fit:'1000',paths:{A:'U1 N1'},anti:false};
assert.equal(run('traceInfo('+JSON.stringify(typedStory)+',M.options[0]).valid'),true,'typed wires must support scenario tracing');
const typedExport=run('bbMd(M.options[0],"candidate-shape")');
assert.match(typedExport,/Submit/,'typed UI affordances must survive planning export');
assert.match(typedExport,/Validate/,'typed non-UI mechanisms must survive planning export');

assert.match(w.document.querySelector('#dia').textContent,/Submit/);
assert.equal(run('BB.render(M.options[0].dsl,null,"m").html'),run('BB.render(M.options[0].dsl,null,"m").html'));
const fixedPatch={kind:'BreadboardPatch',schema_version:1,project_id:run('M.project_id'),option_id:'A',base_dsl:fixedModel,
 operations:[{op:'update_node',id:'U1',set:{title:'Send request'}}]};
run('B.patch='+JSON.stringify(fixedPatch)+';T.top="workspace";render()');
assert.match(w.document.querySelector('main').textContent,/U1/);
assert.ok(!run('M.options[0].dsl').includes('Send request'),'loading an agent patch never mutates the model');
run('applyBreadboardPatch()');
assert.ok(run('M.options[0].dsl').includes('Send request'));
assert.equal(run('M.selectionAuthority'),'Working');
assert.equal(run('M.reqs.every(r=>r.f[0]==="u")'),true);
assert.equal(run('M.stories.every(s=>s.fit[0]==="0")'),true);
assert.throws(()=>run('breadboardPatchPreview('+JSON.stringify(fixedPatch)+')'),/Stale/);


// Continuous localhost Codex loop: review before apply, and invalidate stale mappings/paths.
run('window.__SHAPING_AGENT_SESSION="a".repeat(64);T.top="agent";T.opt=0;Agent.instruction="Make validation more explicit"; M.reqs[0].l[0]="U1";M.stories[0].paths.A="P1 U1";M.selectionAuthority="Accepted"; render()');
assert.match(w.document.querySelector('main').textContent,/Shape with AI/);
assert.ok(w.document.querySelector('[data-act="agent-run"]'));
const nextPatch={
 kind:'BreadboardPatch',schema_version:1,project_id:run('M.project_id'),option_id:'A',
 base_dsl:run('BB.canonical(M.options[0].dsl)'),
 operations:[{op:'update_node',id:'N1',set:{title:'Validate and report'}}]
};
let posted;
w.fetch=async (url,options)=>{
 posted={url,options};
 return {ok:true,json:async()=>({proposal:nextPatch,change_count:1})};
};
await run('requestAgent()');
assert.equal(posted.url,'/api/propose');
assert.equal(posted.options.method,'POST');
assert.equal(posted.options.headers['X-Shaping-Session'],'a'.repeat(64));
assert.equal(run('B.patch.operations.length'),1);
assert.ok(!run('M.options[0].dsl').includes('Validate and report'),'local Codex must not apply before review');
assert.match(w.document.querySelector('main').textContent,/Proposed/);
assert.ok(w.document.querySelectorAll('main .cm .fb').length>=2,'before and after diagrams are inspectable');
w.document.querySelector('[data-act="bb-apply"]').click();
assert.match(run('M.options[0].dsl'),/Validate and report/);
assert.equal(run('M.reqs[0].l[0]'),'','old shape mapping must not survive semantic change');
assert.equal(run('M.stories[0].paths.A'),undefined,'old trace must not survive semantic change');
assert.equal(run('M.selectionAuthority'),'Working');
assert.equal(run('M.reconciliation.option_id'),'A');
assert.match(run('reconciliationDraft()'),/Restore requirement-to-part mappings/);
assert.equal(run('B.patch'),null);
assert.ok(w.document.querySelector('[data-act="agent-run"]'),'agent can continue from changed model');
run('delete window.__SHAPING_AGENT_SESSION;Agent.instruction="Try";render()');
assert.equal(w.document.querySelector('[data-act="agent-run"]').disabled,true,'static hosted Board must not contact localhost');

console.log('Shaping Board smoke: passed parser, per-candidate trace, gate, schema draft export and AI bridge validation, inspectability and review');
