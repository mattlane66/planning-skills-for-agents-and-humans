(function(){
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const NS = 'http://www.w3.org/2000/svg';
const reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
const wideMQ = window.matchMedia('(min-width:560px) and (min-aspect-ratio:6/5)');

/* ---------------- content ---------------- */
const PARTS = [
  { t:'The claim', a:1, b:5 }, { t:'Two tests', a:6, b:9 }, { t:'Framing', a:10, b:13 },
  { t:'Choosing', a:14, b:19 }, { t:'After launch', a:20, b:22 }, { t:'Learning', a:23, b:25 }
];
const X_ = '<span class="cx">x</span>', F_ = '<span class="cf">f()</span>', Y_ = '<span class="cy">y</span>', R_ = '<span class="cr">R</span>', M_ = '<span class="cm">M</span>';
const STEPS = [
  { t:'Meet a team of catalog editors. They often make <b>the same change to 200 products</b>, one at a time. It takes about <b>45 minutes</b>.', hint:true },
  { t:'That’s the situation today. We’ll call it ' + X_ + '.' },
  { t:'They want those updates done right, with far less repetitive work. That’s the outcome they want: ' + Y_ + '.' },
  { t:'In between sits whatever they’ll build: ' + F_ + '. Together, ' + X_ + ' → ' + F_ + ' → ' + Y_ + ' says: <i>this will move us from x toward y.</i>' },
  { t:'Notice the word <i>will</i>. It’s a claim, not a fact. Everything that follows is about testing it.' },
  { t:'Before building anything, the team writes down what any good answer must do. These are the requirements: ' + R_ + '.' },
  { t:'Before building, <b>design fit</b> asks whether the proposed solution plausibly meets ' + R_ + ' under ' + M_ + '—our model of the relevant operating world. After building, <b>realized fit</b> asks whether the thing actually built and operated still does. The article calls both <b>conformance</b>, written E<sup>c</sup>. At design time, the team accepts this proposal as fitting all three requirements.' },
  { t:'The other test asks: <b>did reality actually move toward ' + Y_ + '?</b> The article calls this <b>effect</b>, written E<sup>e</sup>. After launch, a batch takes 31 minutes.' },
  { t:'Now reality gives us two things to inspect. The built workflow misses the 10-minute requirement, and the effect falls short of ' + Y_ + '. The pre-build fit judgment looked good; the operating result did not. <b>That gap is a diagnosis problem, not automatically an execution problem.</b>' },
  { t:'How does that happen? Often the trouble starts before anything is built, in how the problem gets written down. Compare these two.' },
  { t:'The second sounds efficient, but it’s an answer in disguise. It drops the reason, and it rules out other solutions before anyone compares them.' },
  { t:'Good requirements say where they came from: the situation, the outcome, the gap between them, the operating model, or a limit someone imposed, like a contract.' },
  { t:'Some requirements come from ' + M_ + ', the operating model introduced earlier. Here, M includes a belief that editors avoid bulk changes they can’t undo. That condition never became a requirement. <b>Remember that.</b>', a:'M describes relevant operating conditions and causal dynamics; it must not assume that our chosen solution will work.' },
  { t:'Now the options. Come up with a few that work in different ways, and keep today’s way, CURRENT, as a baseline. Together, the options actually considered are the candidate set <b>S</b>.' },
  { t:'This is the <b>Fit Check</b>: requirements down the rows, candidate paths across the columns. Hold the frame fixed and compare every path against the same requirements. <span class="ok sym">✓</span> meets it; <span class="no sym">✗</span> doesn’t. The last row is only a nice-to-have.' },
  { t:'B has a question mark. <b>An unknown isn’t a pass</b>, so the team tests it before relying on it. It holds up.' },
  { t:'Count the checks and A, B and C tie. But A and C each miss a must-have, and <b>no score can make up for that</b>. B is the only candidate here that clears the Must-haves. That makes it eligible—not automatically worth building. Selection still considers the time and resources you’re willing to spend, uncertainty, tradeoffs, or no investment.' },
  { t:'One thing the table can’t show: the better option nobody thought of. <b>It never fails a test. It’s just missing.</b> So search wide before you compare.' },
  { t:'Now <b>rotate the selected path</b>. Open B up: its parts go down the side and the requirements go across the top. This is the <b>Rotated / Reverse Fit Check</b>. It shows which parts contribute to which requirements—and why each meaningful part exists. “Share rules” has no current justification in ' + R_ + ': cut it, put it outside this bet, or justify it through an accepted requirement. <b>Coverage is an account, not proof of sufficiency.</b>' },
  { t:'Launch day. B ships, and batch time drops from 45 to 31 minutes. Was that B?' },
  { t:'Only partly. Editors without B sped up too, to 39 minutes. So B earns about <b>8 of the 14 minutes</b>.' },
  { t:'Judging effect can go wrong in two places: measuring the wrong things (<b>observation</b>), and drawing the wrong conclusion from what you measured (<b>inference</b>).' },
  { t:'The <b>pre-build</b> fit judgment said yes. After launch, realized fit fails and the effect is only partial. The easy answer is to blame the build.' },
  { t:'Instead, start at the verdict and walk backward, asking one question at each stop, all the way back to the frame.' },
  { t:'The gap was upstream. Editors used the rule on only a third of batches, because there was no way to undo one. M said so, but it never became a requirement. <b>Add it to R, rerun the relevant tests, and preserve the old R as a versioned record.</b>' }
];
const N = STEPS.length;
const partOf = n => PARTS.findIndex(p => n >= p.a && n <= p.b);

/* ---------------- build scene pieces ---------------- */
// tiles
let th = '';
for (let i = 0; i < 200; i++) th += '<span class="tile" style="--d:' + ((i % 20) * 0.012 + Math.floor(i / 20) * 0.03).toFixed(3) + 's"></span>';
$('#tiles').innerHTML = th;
const tiles = Array.from($('#tiles').children);

// options grid
const COLS = [['CURRENT','by hand','col-cur'],['A','multi-select','col-a'],['B','reusable rule','col-b'],['C','import','col-c']];
const ROWS = [['R1','Right items',1,['n','y','y','y']],['R2','Rest untouched',1,['y','y','q','n']],['R3','10 min or less',1,['n','n','y','y']],['R4','Import format kept',1,['y','y','y','y']],['R5','Shortcuts',0,['y','y','n','y']]];
let g = '<div class="hd rl"></div>';
COLS.forEach(c => { g += '<div class="hd ' + c[2] + '"><b>' + c[0] + '</b><small>' + c[1] + '</small></div>'; });
g += '<div class="hd gh"><b>D?</b><small>missing</small></div>';
ROWS.forEach(r => {
  g += '<div class="rl"><span class="id">' + r[0] + '</span>' + r[1] + '</div>';
  r[3].forEach((m, j) => {
    const k = 'mk c' + (j + 1) + (r[2] ? ' must' : '');
    const inner = m === 'y' ? '<span class="' + k + ' y">✓</span>' : m === 'n' ? '<span class="' + k + ' n">✗</span>'
      : '<span class="' + k + ' q qb"><span class="qq">?</span><span class="yy">✓</span><span class="tested">tested</span></span>';
    g += '<div class="' + COLS[j][2] + '">' + inner + '</div>';
  });
  g += '<div class="gh cell">–</div>';
});
g += '<div class="rl tot">Checks</div>';
['3/5','4/5','4/5','4/5'].forEach((t, j) => { g += '<div class="tot ' + COLS[j][2] + '">' + t + '</div>'; });
g += '<div class="gh cell last tot"></div>';
$('#grid').innerHTML = g;

// rotated grid
const RC = [['R1','right items'],['R2','rest untouched'],['R3','10 min or less']];
const PT = [['Rule builder',[0,0,1]],['Preview of matches',[1,1,0]],['One-step apply',[0,0,1]],['Share rules',[0,0,0],1]];
let r = '<div class="hd rl"><b>B’s parts</b></div>';
RC.forEach(c => { r += '<div class="hd"><b>' + c[0] + '</b><small>' + c[1] + '</small></div>'; });
PT.forEach(p => {
  const cut = p[2] ? 'cut' : '';
  r += '<div class="rl ' + cut + '">' + p[0] + (p[2] ? '<small>no current justification</small>' : '') + '</div>';
  p[1].forEach(v => { r += '<div class="' + cut + '">' + (v ? '<span class="dotc"></span>' : '<span class="dash">—</span>') + '</div>'; });
});
$('#rotgrid').innerHTML = r;

// chart
const svg = $('#chart');
const X = w => 44 + (w - 1) / 11 * 244;
const Y = m => 20 + (50 - m) / 25 * 192;
function el(tag, at, parent){ const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); parent.appendChild(e); return e; }
function tx(x, y, s, cls, anchor, parent){ const t = el('text', { x, y, class: cls || '', 'text-anchor': anchor || 'start' }, parent); t.textContent = s; return t; }
const base = el('g', {}, svg);
[30,35,40,45,50].forEach(v => { el('line', { class:'gl', x1:44, x2:288, y1:Y(v), y2:Y(v) }, base); tx(36, Y(v) + 4, String(v), '', 'end', base); });
el('line', { class:'ax', x1:44, x2:288, y1:212, y2:212 }, base);
[[1,'week 1'],[6,'week 6'],[12,'week 12']].forEach(([w, s]) => tx(X(w), 230, s, '', 'middle', base));
tx(44, 12, 'minutes per 200-item batch', '', 'start', base);
el('line', { class:'launch', x1:X(6.5), x2:X(6.5), y1:20, y2:212 }, base);
tx(X(6.5) + 5, 36, 'launch', 't-ink', 'start', base);
const WITH = [45,46,45,45,44,45,40,36,34,32,31,31];
const WITHOUT = [45,43,42,41,40,39,39];
const gW = el('g', { class:'fade', id:'g-with' }, svg);
el('polyline', { class:'ln lb', pathLength:1, points: WITH.map((v, i) => X(i + 1) + ',' + Y(v)).join(' ') }, gW);
WITH.forEach((v, i) => el('circle', { class:'dt', cx:X(i + 1), cy:Y(v), r:3.3 }, gW));
tx(294, Y(31) + 4, '31', 't-f', 'start', gW);
tx(44, 254, '— editors with B', 't-f', 'start', gW);
const gT = el('g', { class:'fade', id:'g-tot' }, svg);
el('path', { class:'brk b-tot', d:'M312 ' + Y(45) + 'H320V' + Y(31) + 'H312' }, gT);
tx(326, (Y(45) + Y(31)) / 2 + 4, '−14 min', 't-ink', 'start', gT);
const gWo = el('g', { class:'fade', id:'g-without' }, svg);
el('polyline', { class:'ln lc', pathLength:1, points: WITHOUT.map((v, i) => X(i + 6) + ',' + Y(v)).join(' ') }, gWo);
WITHOUT.forEach((v, i) => { if (i) el('circle', { class:'dtc', cx:X(i + 6), cy:Y(v), r:2.8 }, gWo); });
tx(294, Y(39) + 4, '39', 't-m', 'start', gWo);
tx(44, 273, '— editors without B', 't-m', 'start', gWo);
const gS = el('g', { class:'fade', id:'g-split' }, svg);
el('path', { class:'brk b-cmp', d:'M312 ' + Y(45) + 'H320V' + (Y(39) - 2) + 'H312' }, gS);
el('path', { class:'brk b-f', d:'M312 ' + (Y(39) + 2) + 'H320V' + Y(31) + 'H312' }, gS);
tx(326, (Y(45) + Y(39)) / 2 + 4, '−6 anyway', 't-m', 'start', gS);
tx(326, (Y(39) + Y(31)) / 2 + 4, '−8 from B', 't-f', 'start', gS);
const gA = el('g', { class:'fade ann', id:'g-ann' }, svg);
el('line', { x1:X(5), y1:Y(44) + 5, x2:X(5), y2:96 }, gA);
el('rect', { x:X(5) - 48, y:96, width:96, height:24, rx:12 }, gA);
tx(X(5), 112.5, 'observation', '', 'middle', gA);
el('line', { x1:350, y1:50, x2:320, y2:(Y(45) + Y(39)) / 2 }, gA);
el('rect', { x:310, y:26, width:80, height:24, rx:12 }, gA);
tx(350, 42.5, 'inference', '', 'middle', gA);

// part segments
$('#segs').innerHTML = PARTS.map((p, i) => '<button type="button" class="seg" data-i="' + i + '" aria-label="Part ' + (i + 1) + ': ' + p.t + '"><i></i></button>').join('');

/* ---------------- layout ---------------- */
const story = $('#story'), player = $('#player'), stagebox = $('#stagebox'), art = $('#art');
let S = 1, stepH = 400, storyTop = 0;
function fitArt(){
  const w = stagebox.clientWidth - 16, h = stagebox.clientHeight - 16;
  if (w <= 0 || h <= 0) return;
  S = Math.min(w / 400, h / 400, 1.4);
  const ox = (stagebox.clientWidth - 400 * S) / 2, oy = (stagebox.clientHeight - 400 * S) / 2;
  art.style.transform = 'translate(' + ox.toFixed(1) + 'px,' + oy.toFixed(1) + 'px) scale(' + S.toFixed(4) + ')';
}
function measureTiles(){
  const nx = $('#nx'), det = $('.a-detail');
  const cx = nx.offsetLeft + nx.offsetWidth / 2, cy = nx.offsetTop + nx.offsetHeight / 2;
  tiles.forEach(t => {
    t.style.setProperty('--dx', (cx - (t.offsetLeft + t.offsetWidth / 2)).toFixed(1) + 'px');
    t.style.setProperty('--dy', (cy - (det.offsetTop + t.offsetTop + t.offsetHeight / 2)).toFixed(1) + 'px');
  });
  const b = $('#clock b');
  $('#clock').style.setProperty('--cdx', (cx - (b.offsetLeft + b.offsetWidth / 2)).toFixed(1) + 'px');
  $('#clock').style.setProperty('--cdy', (cy - (b.offsetTop + b.offsetHeight / 2)).toFixed(1) + 'px');
}
function layout(){
  const ph = player.getBoundingClientRect().height;
  stepH = Math.max(260, Math.round(ph * 0.62));
  story.style.height = (N * stepH + ph) + 'px';
  storyTop = story.getBoundingClientRect().top + window.scrollY;
  fitArt();
  measureTiles();
}

/* ---------------- state ---------------- */
const on = (s, c) => { const e = $(s); if (e) e.classList.toggle('on', !!c); };
const cls = (s, k, c) => { const e = $(s); if (e) e.classList.toggle(k, !!c); };
const setText = (s, v) => { const e = $(s); if (e && e.textContent !== v) e.textContent = v; };
let cur = 0;
function scene(n){
  // s1–2: the clock and 200 tiles fold into x
  on('#clock', n <= 2); cls('#clock', 'away', n >= 2);
  on('#p-tiles', n <= 2); cls('#tiles', 'away', n >= 2); cls('#p-tiles', 'gone', n >= 2);
  // the spine
  on('#nx', n >= 2); on('#ny', n >= 3); on('#nf', n >= 4); on('#ar1', n >= 4); on('#ar2', n >= 4);
  on('#bracket', n >= 5 && n <= 9);
  const HL = { 2:'x', 3:'y', 4:'f', 5:'xfy', 6:'f', 7:'f', 8:'y', 9:'fy', 10:'x', 11:'x' };
  const h = HL[n] || (n >= 14 && n <= 19 ? 'f' : n >= 20 && n <= 22 ? 'y' : '');
  cls('#nx', 'hl', h.includes('x')); cls('#nf', 'hl', h.includes('f')); cls('#ny', 'hl', h.includes('y'));
  setText('#sub-f', n < 14 ? 'what they’ll build' : n <= 16 ? 'which option?' : n <= 18 ? 'B: reusable rule' : n === 19 ? 'B’s parts' : 'B, shipped');
  setText('#sub-y', n >= 20 ? 'did it move?' : 'right, with less work');
  on('#fitb', (n >= 7 && n <= 9) || n >= 23);
  on('#effb', (n >= 8 && n <= 9) || n >= 20);
  const realizedFail = n === 9 || n >= 23;
  cls('#fitb', 'fail', realizedFail);
  setText('#fitb', realizedFail ? 'realized fit ✗ 10 min' : 'design fit ✓ accepted');
  setText('#effb', n === 20 ? 'effect: 45 → 31 min' : (n === 21 || n === 22) ? 'effect: ≈ 8 of 14 min' : 'effect: only partly');
  // requirements and the side box
  const rm = (n >= 6 && n <= 9) || n === 12 || n === 13 || n === 25;
  on('#p-rm', rm);
  cls('#p-rm', 'noside', n === 6 || n === 7);
  cls('#rbox', 'checks', n >= 7 && n <= 9);
  cls('#r3', 'fail', n === 9);
  setText('#r3 .ck', n === 9 ? '✗' : '✓');
  cls('#rbox', 'src', n === 12 || n === 13 || n === 25);
  cls('#r4', 'hide', n !== 12);
  cls('#slot', 'hide', !(n === 13 || n === 25));
  cls('#slot', 'filled', n === 25);
  $('#slot-t').innerHTML = n === 25 ? 'A batch can be undone<span class="newtag">new</span>' : '<span class="q">?</span>nothing yet';
  on('#meterbox', n === 8 || n === 9);
  cls('#meter', 'moved', n === 8 || n === 9);
  setText('#mk-t', n === 8 || n === 9 ? '31 min' : '45 min');
  on('#srcbox', n === 12);
  on('#mbox', n === 13 || n === 25);
  setText('#mnote', n === 25 ? 'Now it’s a requirement. Rerun the fit test against it.' : 'This never made it into R.');
  cls('#mnote', 'later', n === 25);
  // framing
  on('#p-frame', n === 10 || n === 11);
  const judged = n >= 11;
  cls('#fc-good', 'judged', judged); cls('#fc-bad', 'judged', judged);
  $('#lab-good').innerHTML = judged ? '<span class="sym">✓</span><span>Describes the situation</span>' : 'One way to write it';
  $('#lab-bad').innerHTML = judged ? '<span class="sym">✗</span><span>An answer in disguise</span>' : 'Another way';
  ['#chips-good','#chips-bad','#note-good','#note-bad'].forEach(s => on(s, judged));
  // options
  on('#p-grid', n >= 14 && n <= 19);
  on('#og', n >= 14 && n <= 18); on('#rot', n === 19);
  cls('#og', 'marks', n >= 15); cls('#og', 'resolved', n >= 16); cls('#og', 'judged', n >= 17); cls('#og', 'ghost', n >= 18);
  // chart
  on('#p-chart', n >= 20 && n <= 22);
  on('#g-with', n >= 20); on('#g-tot', n === 20); on('#g-without', n >= 21); on('#g-split', n >= 21); on('#g-ann', n === 22);
  // diagnose backward
  on('#p-diag', n === 23 || n === 24);
  cls('.qs li.bld', 'sus', n === 23);
  cls('#qs', 'sweep', n === 24);
}
function chrome(n){
  const pi = partOf(n), p = PARTS[pi];
  $('#meta-part').innerHTML = '<b>Part ' + (pi + 1) + '</b> · ' + p.t;
  setText('#meta-count', n + ' / ' + N);
  $$('.seg').forEach((s, i) => {
    const q = PARTS[i];
    const v = n > q.b ? 1 : n < q.a ? 0 : (n - q.a + 1) / (q.b - q.a + 1);
    s.style.setProperty('--p', v);
    s.setAttribute('aria-current', i === pi ? 'step' : 'false');
  });
  const st = STEPS[n - 1];
  const first = n === p.a;
  $('#tp-body').innerHTML = '<div class="tp-in">' + (first ? '<p class="tp-part">Part ' + (pi + 1) + ' · ' + p.t + '</p>' : '') +
    '<p class="tp-text">' + st.t + '</p>' + (st.a ? '<p class="tp-aside">' + st.a + '</p>' : '') +
    (st.hint ? '<p class="tp-hint">Scroll or tap Next.</p>' : '') + '</div>';
  $('#back').disabled = n === 1;
  $('#next').innerHTML = n === N ? 'Recap <span aria-hidden="true">↓</span>' : 'Next <span aria-hidden="true">→</span>';
}
function setStep(n){
  if (n === cur) return;
  cur = n;
  scene(n);
  chrome(n);
}

/* ---------------- scroll + navigation ---------------- */
let lock = 0, lockTimer = null;
function stepFromScroll(){
  const y = window.scrollY - storyTop;
  return Math.max(1, Math.min(N, Math.floor(y / stepH) + 1));
}
function onScroll(){
  const n = stepFromScroll();
  if (lock) { if (n === lock) { lock = 0; clearTimeout(lockTimer); } else return; }
  setStep(n);
}
let ticking = false;
window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; onScroll(); }); } }, { passive: true });
function go(n){
  n = Math.max(1, Math.min(N, n));
  lock = n; clearTimeout(lockTimer);
  lockTimer = setTimeout(() => { lock = 0; }, 1400);
  setStep(n);
  try { history.replaceState(null, '', '#step-' + n); } catch(e) {}
  window.scrollTo({ top: storyTop + (n - 1) * stepH + Math.round(stepH * 0.3), behavior: reduce ? 'auto' : 'smooth' });
}
function toRecap(){ lock = 0; $('#recap').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }
$('#next').addEventListener('click', () => { if (cur >= N) toRecap(); else go(cur + 1); });
$('#back').addEventListener('click', () => go(cur - 1));
$('#tp-body').addEventListener('click', e => { if (wideMQ.matches || e.target.closest('a')) return; if (cur >= N) toRecap(); else go(cur + 1); });
$('#segs').addEventListener('click', e => { const s = e.target.closest('.seg'); if (s) go(PARTS[+s.dataset.i].a); });
$('#start').addEventListener('click', () => go(1));
$('#again').addEventListener('click', () => go(1));
document.addEventListener('keydown', e => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const y = window.scrollY;
  if (y < storyTop - 40 || y > storyTop + N * stepH) return;
  const onButton = e.target.closest && e.target.closest('button, a, input, textarea, select');
  const fwd = e.key === 'ArrowRight' || e.key === 'ArrowDown' || (e.key === ' ' && !e.shiftKey && !onButton);
  const bwd = e.key === 'ArrowLeft' || e.key === 'ArrowUp' || (e.key === ' ' && e.shiftKey && !onButton);
  if (fwd) { e.preventDefault(); if (cur >= N) toRecap(); else go(cur + 1); }
  else if (bwd) { e.preventDefault(); go(cur - 1); }
});


/* ---------------- break-the-model lab ---------------- */
const FAULTS = {
  intent:{node:'frame',symptom:'The measured outcome improves, yet the work still feels wrong or irrelevant.',origin:'The chosen y no longer represents the relevant want or priority. The team can execute and measure perfectly against the wrong outcome.',repair:'Reopen intent and priority. Decide whose outcome counts, revise y if needed, then rerun the affected derivation and checks.'},
  model:{node:'model',symptom:'The design looked plausible, but real behavior or operating conditions defeat it.',origin:'M misdescribed how the world works or projected the relevant dynamics badly.',repair:'Correct the operating model, trace what R changes because of it, and rerun candidate fit where those assumptions mattered.'},
  requirements:{node:'requirements',symptom:'The solution passes every recorded requirement but still underperforms in use.',origin:'R omitted a condition the solution needed to handle. Conformance was real—against an incomplete specification.',repair:'Derive the missing requirement from x, y, the gap, M, or an imposed boundary. Record its provenance, then rerun fit.'},
  choice:{node:'choice',symptom:'Every considered candidate looks acceptable or mediocre, yet the decision still feels artificially narrow.',origin:'The candidate set S omitted a materially better route. Nothing in the matrix can reject or select an option that was never generated.',repair:'Widen generation toward different mechanisms and tradeoffs, then rerun design fit and selection against the same frame.'},
  build:{node:'build',symptom:'The proposed design had a credible fit, but the operating product behaves differently.',origin:'The realization drifted from the selected design, or conditions changed during implementation.',repair:'Check realized conformance. Repair the build or explicitly revise the affected frame, model, or requirement before judging effect.'},
  observation:{node:'observation',symptom:'The effect verdict looks weak or contradictory even though important change may have occurred.',origin:'The evidence represents the wrong population, window, instrument, signal, or comparison.',repair:'Fix observation first. Then redo the effect inference; better reasoning cannot recover information that was never observed.'},
  inference:{node:'verdict',symptom:'The evidence is adequate, but the conclusion about movement or attribution is still wrong.',origin:'Eᵉ made a poor inference from good observations—the comparison, attribution assumptions, threshold, or confidence judgment failed.',repair:'Revisit the inference itself. Better measurement is not the repair when the evidence was already adequate.'}
};
const faultOrder=['frame','model','requirements','choice','build','observation','verdict'];
function renderFault(k){
  const d=FAULTS[k] || FAULTS.requirements, oi=faultOrder.indexOf(d.node);
  $$('#fault-controls button').forEach(b=>b.setAttribute('aria-selected', b.dataset.fault===k ? 'true':'false'));
  $$('#fault-flow .fault-node').forEach(n=>{
    const i=faultOrder.indexOf(n.dataset.node);
    n.classList.toggle('origin', i===oi);
    n.classList.toggle('downstream', i>oi);
    n.classList.toggle('symptom', n.dataset.node==='verdict');
  });
  setText('#fault-symptom',d.symptom); setText('#fault-origin',d.origin); setText('#fault-repair',d.repair);
}
$('#fault-controls').addEventListener('click',e=>{const b=e.target.closest('button[data-fault]');if(b)renderFault(b.dataset.fault);});
renderFault('requirements');

/* ---------------- live Fit Check workbench ---------------- */
const wbDefaults={
  x:'The same edit across 200 items takes 45 minutes.',
  y:'Complete intended updates accurately with far less repetitive effort.',
  m:'Editors avoid bulk changes they cannot undo.',
  r:['Change the right items','Leave the rest alone','200 items in 10 min or less','Keep the import format','A batch can be undone'],
  c:['CURRENT · edit one by one','A · multi-select + batch action','B · reusable rule + preview','C · validated import'],
  p:['Rule builder','Preview of matches','One-step apply','Import adapter','Undo','Share rules']
};
let wbMode='fit';
let wbSelected=2;
let wbFitState={};
let wbRotState={};
const esc=v=>String(v).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));
const wbLines=s=>$(s).value.split(/\n+/).map(v=>v.trim()).filter(Boolean);
const fitKey=(ri,ci)=>ri+'␟'+ci;
const rotKey=(pi,ri)=>pi+'␟'+ri;
function seedWB(){
  wbFitState={}; wbRotState={}; wbSelected=2;
  const fs=[
    ['strong','strong','strong','strong'],
    ['strong','strong','strong','partial'],
    ['weak','partial','strong','strong'],
    ['strong','strong','strong','strong'],
    ['weak','partial','strong','partial']
  ];
  fs.forEach((row,ri)=>row.forEach((st,ci)=>wbFitState[fitKey(ri,ci)]=st));
  const A=(pi,ri,state='accepted')=>wbRotState[rotKey(pi,ri)]=state;
  A(0,2);                 // Rule builder -> speed
  A(1,0); A(1,1);         // Preview -> accuracy / preserve
  A(2,2);                 // Apply -> speed
  A(3,3);                 // Adapter -> import
  A(4,4,'unknown');       // Undo -> undo requirement, still unresolved
}
function fitLabel(st){return st==='strong'?'✓':st==='partial'?'○':st==='weak'?'✕':'?';}
function rotLabel(st){return st==='accepted'?'●':st==='unknown'?'●?':'—';}
function fitNext(st){return st==='unresolved'?'weak':st==='weak'?'partial':st==='partial'?'strong':'unresolved';}
function rotNext(st){return st==='none'?'unknown':st==='unknown'?'accepted':'none';}
function wbCandidateLabel(c,i){
  const m=c.match(/^([^·:–—-]{1,14})\s*[·:–—-]\s*(.+)$/);
  return m?'<span class="cand-id">'+esc(m[1].trim())+'</span>'+esc(m[2].trim()):'<span class="cand-id">Path '+(i+1)+'</span>'+esc(c);
}
function syncWBInputs(){
  const fit=wbMode==='fit';
  $$('.wb-fit-only').forEach(e=>e.hidden=!fit);
  $$('.wb-rotate-only').forEach(e=>e.hidden=fit);
}
function syncSelected(cands){
  if(!cands.length){wbSelected=0; $('#wb-selected').innerHTML=''; return;}
  wbSelected=Math.max(0,Math.min(wbSelected,cands.length-1));
  const sel=$('#wb-selected');
  sel.innerHTML=cands.map((c,i)=>'<option value="'+i+'">'+esc(c)+'</option>').join('');
  sel.value=String(wbSelected);
}
function diagCard(title,items,empty,kind='warn'){
  const arr=Array.isArray(items)?items:(items?[items]:[]);
  return '<div class="diag-card '+(arr.length?kind:'good')+'"><b>'+esc(title)+'</b><span>'+(arr.length?arr.map(esc).join(' · '):esc(empty))+'</span></div>';
}
function renderFit(reqs,cands){
  $('#wb-matrix-title').textContent='Requirements × candidate paths';
  $('#wb-matrix-desc').textContent='Hold x, y, M, and R fixed. Compare whole paths before opening any one of them up.';
  $('#wb-legend').textContent='tap: ? → ✕ → ○ → ✓';
  $('#wb-mode-title').textContent='Fit Check · R × S';
  $('#wb-mode-help').textContent='Requirements run down the side. Candidate paths run across the top.';
  $('#wb-footnote').innerHTML='<b>Compare first; decompose second.</b> A path can fit strongly, partially, weakly, or remain unresolved. Selection still considers the time and resources you’re willing to spend, uncertainty, tradeoffs, and the option not to invest.';
  if(!reqs.length||!cands.length){$('#wb-scroll').innerHTML='<p class="wb-note" style="padding:14px">Add at least one requirement and two candidate paths.</p>';$('#wb-diag').innerHTML='';return;}
  let h='<table class="wb-table wb-fit-table"><thead><tr><th scope="col">Requirements (R)</th>';
  cands.forEach((c,ci)=>{
    const picked=ci===wbSelected;
    h+='<th scope="col" class="'+(picked?'candidate-selected':'')+'">'+wbCandidateLabel(c,ci)+'<button type="button" class="wb-pick" data-pick="'+ci+'" aria-pressed="'+(picked?'true':'false')+'">'+(picked?'Selected ↻':'Rotate this')+'</button></th>';
  });
  h+='</tr></thead><tbody>';
  reqs.forEach((r,ri)=>{
    h+='<tr><th scope="row"><span class="req-id">R'+(ri+1)+'</span>'+esc(r)+'</th>';
    cands.forEach((c,ci)=>{const st=wbFitState[fitKey(ri,ci)]||'unresolved';h+='<td><button type="button" class="wb-cell" data-fit-ri="'+ri+'" data-fit-ci="'+ci+'" data-state="'+st+'" aria-label="'+esc(c)+' against R'+(ri+1)+' '+esc(r)+': '+st+'">'+fitLabel(st)+'</button></td>';});
    h+='</tr>';
  });
  h+='</tbody></table>';
  $('#wb-scroll').innerHTML=h;
  const selectedName=cands[wbSelected]||'Selected path';
  const weak=reqs.filter((_,ri)=>(wbFitState[fitKey(ri,wbSelected)]||'unresolved')==='weak').map((r,ri)=>'R'+(reqs.indexOf(r)+1));
  const partial=reqs.filter((_,ri)=>['partial','unresolved'].includes(wbFitState[fitKey(ri,wbSelected)]||'unresolved')).map(r=>'R'+(reqs.indexOf(r)+1));
  const unresolvedCells=[];
  reqs.forEach((r,ri)=>cands.forEach((c,ci)=>{if((wbFitState[fitKey(ri,ci)]||'unresolved')==='unresolved')unresolvedCells.push('R'+(ri+1)+' × '+(ci+1));}));
  $('#wb-diag').innerHTML=
    diagCard('Selected to rotate',[selectedName],'Choose a path','good')+
    diagCard('Weak fit in selected',weak,'No weak-fit cells','bad')+
    diagCard('Partial / unresolved in selected',partial,'None','warn')+
    diagCard('Still unjudged',unresolvedCells,'Every comparison has a judgment','warn');
}
function renderRotate(reqs,cands,parts){
  const selectedName=cands[wbSelected]||'Selected path';
  $('#wb-matrix-title').textContent='Parts × requirements';
  $('#wb-matrix-desc').textContent='Open '+selectedName+' into meaningful parts. Trace which parts contribute to each requirement.';
  $('#wb-legend').textContent='tap: — → ●? → ●';
  $('#wb-mode-title').textContent='Rotated / Reverse Fit · Parts × R';
  $('#wb-mode-help').textContent='Parts run down the side. Requirements run across the top.';
  $('#wb-footnote').innerHTML='<b>Rotation explains the candidate; it does not prove it.</b> Empty columns expose missing accounts. Empty rows expose parts with no current justification. Multiple dots can reveal shared or overloaded responsibility worth inspecting.';
  if(!reqs.length||!parts.length){$('#wb-scroll').innerHTML='<p class="wb-note" style="padding:14px">Add requirements and the meaningful parts of the selected path.</p>';$('#wb-diag').innerHTML='';return;}
  const claimed=(pi,ri)=>['accepted','unknown'].includes(wbRotState[rotKey(pi,ri)]||'none');
  const gaps=reqs.map((r,ri)=>({r,ri})).filter(x=>!parts.some((_,pi)=>claimed(pi,x.ri))).map(x=>'R'+(x.ri+1));
  const orphan=parts.map((p,pi)=>({p,pi})).filter(x=>!reqs.some((_,ri)=>claimed(x.pi,ri))).map(x=>x.p);
  const unresolved=[];parts.forEach((p,pi)=>reqs.forEach((r,ri)=>{if((wbRotState[rotKey(pi,ri)]||'none')==='unknown')unresolved.push(p+' → R'+(ri+1));}));
  const overloaded=parts.map((p,pi)=>({p,n:reqs.filter((_,ri)=>claimed(pi,ri)).length})).filter(x=>x.n>=3).map(x=>x.p+' ('+x.n+' R)');
  const shared=reqs.map((r,ri)=>({ri,n:parts.filter((_,pi)=>claimed(pi,ri)).length})).filter(x=>x.n>=2).map(x=>'R'+(x.ri+1)+' ('+x.n+' parts)');
  let h='<table class="wb-table wb-rot-table"><thead><tr><th scope="col">Parts of '+esc(selectedName)+'</th>';
  reqs.forEach((r,ri)=>h+='<th scope="col" class="'+(gaps.includes('R'+(ri+1))?'col-gap':'')+'"><span class="req-id">R'+(ri+1)+'</span>'+esc(r)+'</th>');
  h+='</tr></thead><tbody>';
  parts.forEach((p,pi)=>{
    const isOrphan=orphan.includes(p);
    h+='<tr class="'+(isOrphan?'row-orphan':'')+'"><th scope="row">'+esc(p)+(isOrphan?'<span class="cand-id">no current justification</span>':'')+'</th>';
    reqs.forEach((r,ri)=>{const st=wbRotState[rotKey(pi,ri)]||'none';h+='<td><button type="button" class="wb-cell" data-rot-pi="'+pi+'" data-rot-ri="'+ri+'" data-state="'+st+'" aria-label="'+esc(p)+' contribution to R'+(ri+1)+' '+esc(r)+': '+(st==='accepted'?'accepted':st==='unknown'?'unresolved':'none')+'">'+rotLabel(st)+'</button></td>';});
    h+='</tr>';
  });
  h+='</tbody></table>';
  $('#wb-scroll').innerHTML=h;
  $('#wb-diag').innerHTML=
    diagCard('Coverage gaps',gaps,'Every requirement has an account','bad')+
    diagCard('Unjustified parts',orphan,'Every part has a current reason','bad')+
    diagCard('Unresolved claims',unresolved,'None','warn')+
    diagCard('Overloaded parts · inspect',overloaded,'None flagged','warn')+
    diagCard('Shared responsibility · inspect',shared,'None flagged','warn');
}
function renderWB(){
  const reqs=wbLines('#wb-r'),cands=wbLines('#wb-c'),parts=wbLines('#wb-p');
  syncSelected(cands); syncWBInputs();
  if(wbMode==='fit')renderFit(reqs,cands);else renderRotate(reqs,cands,parts);
  $$('.wb-matrix-card [data-wb-mode]').forEach(b=>b.setAttribute('aria-selected',b.dataset.wbMode===wbMode?'true':'false'));
}
$('.wb-phase').addEventListener('click',e=>{const b=e.target.closest('button[data-wb-mode]');if(!b)return;wbMode=b.dataset.wbMode;renderWB();});
$('#wb-selected').addEventListener('change',e=>{wbSelected=+e.target.value||0;renderWB();});
$('#wb-scroll').addEventListener('click',e=>{
  const pick=e.target.closest('.wb-pick');
  if(pick){wbSelected=+pick.dataset.pick||0;wbMode='rotate';renderWB();return;}
  const f=e.target.closest('[data-fit-ri]');
  if(f){const k=fitKey(+f.dataset.fitRi,+f.dataset.fitCi),st=wbFitState[k]||'unresolved';wbFitState[k]=fitNext(st);renderWB();return;}
  const r=e.target.closest('[data-rot-pi]');
  if(r){const k=rotKey(+r.dataset.rotPi,+r.dataset.rotRi),st=wbRotState[k]||'none';wbRotState[k]=rotNext(st);renderWB();}
});
['#wb-x','#wb-y','#wb-m','#wb-r','#wb-c','#wb-p'].forEach(s=>$(s).addEventListener('input',renderWB));
function resetWB(){
  wbMode='fit';
  $('#wb-x').value=wbDefaults.x;$('#wb-y').value=wbDefaults.y;$('#wb-m').value=wbDefaults.m;
  $('#wb-r').value=wbDefaults.r.join('\n');$('#wb-c').value=wbDefaults.c.join('\n');$('#wb-p').value=wbDefaults.p.join('\n');
  seedWB();renderWB();
}
$('#wb-reset').addEventListener('click',resetWB);
function wbSnapshot(){
  const reqs=wbLines('#wb-r'),cands=wbLines('#wb-c'),parts=wbLines('#wb-p');
  const md=v=>String(v).replace(/\|/g,'\\|').replace(/\n/g,' ');
  let out='# Fit Check snapshot\n\n## Frame\n\n- x: '+$('#wb-x').value.trim()+'\n- y: '+$('#wb-y').value.trim()+'\n- M: '+$('#wb-m').value.trim()+'\n\n';
  out+='## Phase 1 — Fit Check (Requirements × Candidate Paths)\n\n| Requirement | '+cands.map(md).join(' | ')+' |\n| --- | '+cands.map(()=>':---:').join(' | ')+' |\n';
  reqs.forEach((r,ri)=>{out+='| R'+(ri+1)+' · '+md(r)+' | '+cands.map((_,ci)=>fitLabel(wbFitState[fitKey(ri,ci)]||'unresolved')).join(' | ')+' |\n';});
  out+='\nSelected path to rotate: '+(cands[wbSelected]||'')+'\n\n✓ = strong fit · ○ = partial fit · ✕ = weak fit · ? = unresolved\n\n';
  out+='## Phase 2 — Rotated / Reverse Fit (Parts × Requirements)\n\n| Part | '+reqs.map((_,ri)=>'R'+(ri+1)).join(' | ')+' |\n| --- | '+reqs.map(()=>':---:').join(' | ')+' |\n';
  parts.forEach((p,pi)=>{out+='| '+md(p)+' | '+reqs.map((_,ri)=>rotLabel(wbRotState[rotKey(pi,ri)]||'none')).join(' | ')+' |\n';});
  out+='\n● = accepted contribution claim · ●? = unresolved contribution claim · — = no contribution claimed\n\nFirst compare whole candidate paths against the same requirements. Then rotate the selected path to inspect which parts contribute to which requirements and why each meaningful part exists.\n';
  return out;
}
async function copyPlain(text){
  try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);return true;}}catch(e){}
  const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();
  let ok=false;try{ok=document.execCommand('copy');}catch(e){}ta.remove();return ok;
}
$('#wb-copy').addEventListener('click',async()=>{const b=$('#wb-copy'),old=b.textContent,ok=await copyPlain(wbSnapshot());b.textContent=ok?'Copied':'Select & copy failed';setTimeout(()=>b.textContent=old,1400);});
seedWB();renderWB();

let rt = null;
function relayout(){ clearTimeout(rt); rt = setTimeout(() => { layout(); cur = 0; onScroll(); }, 120); }
window.addEventListener('resize', relayout);
window.addEventListener('orientationchange', relayout);
if (window.ResizeObserver) new ResizeObserver(() => { fitArt(); }).observe(stagebox);

layout();
const deepStep = location.hash.match(/^#step-(\d+)$/);
if (deepStep) requestAnimationFrame(() => go(+deepStep[1]));
else { setStep(1); onScroll(); }
if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => {
  layout();
  if (deepStep) go(+deepStep[1]);
});
})();
