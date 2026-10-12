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
assert.equal(errors.length, 0, errors.join('\n'));
console.log('Shaping Board smoke: passed parser, per-candidate trace, gate, schema and draft export');
