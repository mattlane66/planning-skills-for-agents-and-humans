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
console.log('Shaping Board smoke: passed parser, per-candidate trace, gate, schema and draft export');
