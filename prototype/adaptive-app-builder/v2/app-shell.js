let state = loadState();
let undoStack = [];
let redoStack = [];
let hoverSlice = null;
let resizeTimer = null;

const $ = (q, root = document) => root.querySelector(q);
const $$ = (q, root = document) => Array.from(root.querySelectorAll(q));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[m]));
const attr = (s) => esc(s).replace(/`/g, "&#096;");
const fitSymbol = (v) => ({ strong: "●", partial: "◐", weak: "○", unknown: "?" }[v] || "?");
const relationSymbol = (v) => ({ helps: "+", supports: "+", threatens: "−", partial: "◐", none: "·" }[v] || "·");
const relationLabel = (v) => ({ helps: "helps", supports: "supports", threatens: "threatens", partial: "partial", none: "—" }[v] || v);

function snapshot() { return JSON.stringify(state); }
function restore(raw) { state = JSON.parse(raw); saveState(state); render(); }
function mutate(label, fn) {
  undoStack.push(snapshot());
  if (undoStack.length > 60) undoStack.shift();
  redoStack = [];
  fn();
  if (label) addChange(state, label, "neutral");
  saveState(state);
  render();
}
function undo() {
  if (!undoStack.length) return toast("Nothing to undo");
  redoStack.push(snapshot());
  restore(undoStack.pop());
}
function redo() {
  if (!redoStack.length) return toast("Nothing to redo");
  undoStack.push(snapshot());
  restore(redoStack.pop());
}
function saveAndRender() { saveState(state); render(); }

function render() {
  document.querySelector("#app").innerHTML = `
    <header class="topbar">
      <div class="brand">
        <div class="mark">A</div>
        <div><div>Adaptive App Builder</div><div class="crumb">Expense review · living model</div></div>
      </div>
      <div class="actions">
        <button class="icon-btn" data-action="undo" title="Undo" ${undoStack.length ? "" : "disabled"}>↶</button>
        <button class="icon-btn" data-action="redo" title="Redo" ${redoStack.length ? "" : "disabled"}>↷</button>
        ${state.nav.candidate ? `<button class="btn" data-action="home">← Matrix</button>` : ""}
        <button class="btn quiet" data-action="reset">Reset demo</button>
      </div>
    </header>
    <main class="wrap">
      ${frameStrip()}
      ${state.nav.candidate ? candidateWorkspace() : matrixHome()}
    </main>
    ${fitDrawer()}
    ${hifiModal()}
    ${reconcileModal()}
    ${buildPacketModal()}
    <div id="toast" class="toast hidden"></div>
  `;
  bind();
  requestAnimationFrame(() => {
    drawWires();
    updateSlicePreview(hoverSlice || state.slicePreview);
  });
}

function frameStrip() {
  if (state.frame.collapsed) {
    return `<section class="frame-strip surface">
      <button class="frame-toggle" data-action="toggle-frame" title="Expand frame">Frame</button>
      <div class="frame-mini"><span class="frame-label">x</span><span>${esc(short(state.frame.x, 72))}</span></div>
      <div class="formula-inline">→ <b>f(?)</b> →</div>
      <div class="frame-mini"><span class="frame-label">y</span><span>${esc(short(state.frame.y, 72))}</span></div>
      <div class="frame-mini model"><span class="frame-label">M</span><span>${esc(short(state.frame.m, 66))}</span></div>
      <button class="icon-btn" data-action="toggle-frame">⌄</button>
    </section>`;
  }
  return `<section class="surface frame-open">
    <div class="between"><div><div class="ey">Frame</div><div class="title">x → f(?) → y under M</div></div><button class="icon-btn" data-action="toggle-frame">⌃</button></div>
    <div class="frame-grid">
      ${frameField("x", "x · current situation", state.frame.x)}
      ${frameField("y", "y · desired outcome", state.frame.y)}
      ${frameField("m", "M · working model", state.frame.m)}
    </div>
  </section>`;
}
function frameField(key, label, value) {
  return `<label class="frame-field"><span class="ey">${label}</span><textarea data-frame="${key}">${esc(value)}</textarea></label>`;
}

function matrixHome() {
  const mode = state.matrix.mode;
  return `<section class="workspace home">
    <div class="workspace-head">
      <div>
        <div class="ey">Shaping surface</div>
        <div class="title">${mode === "fit" ? "Fit check" : "Reverse fit · rotated"}</div>
        <div class="sub">${mode === "fit" ? "Do the candidate paths satisfy what must be true?" : "Does every part earn its place, and does every criterion have support?"}</div>
      </div>
      <div class="actions">
        <div class="segmented">
          <button class="seg ${mode === "fit" ? "active" : ""}" data-matrix-mode="fit">Fit check</button>
          <button class="seg ${mode === "reverse" ? "active" : ""}" data-matrix-mode="reverse">↻ Rotate / reverse fit</button>
        </div>
        ${mode === "fit" ? `<button class="btn" data-action="add-criterion">+ Criterion</button><button class="btn" data-action="add-candidate">+ Path</button>` : candidatePicker()}
      </div>
    </div>
    <div class="matrix-shell surface">
      ${mode === "fit" ? fitMatrix() : reverseFitMatrix()}
    </div>
    <div class="home-lower">
      ${changeThread()}
      ${aiNudge()}
    </div>
  </section>`;
}

function candidatePicker() {
  return `<label class="compact-select"><span>Candidate</span><select data-rotate-candidate>${state.candidates.map((c) => `<option value="${c.id}" ${c.id === state.matrix.rotatedCandidate ? "selected" : ""}>${esc(c.id)} · ${esc(c.name)}</option>`).join("")}</select></label>`;
}

function fitMatrix() {
  return `<div class="matrix-scroll"><table class="fit-table"><thead><tr>
    <th class="criterion-col"><span class="ey">Criteria</span></th>
    ${state.candidates.map(candidateHeader).join("")}
  </tr></thead><tbody>
    ${state.criteria.map(fitCriterionRow).join("")}
    ${state.provisionalCriteria.map(provisionalRow).join("")}
  </tbody></table></div>`;
}
function candidateHeader(c) {
  return `<th class="candidate-head">
    <div class="candidate-kicker">${esc(c.id)} · candidate</div>
    <input class="matrix-input candidate-title" data-candidate-name="${c.id}" value="${attr(c.name)}">
    <textarea class="matrix-input candidate-desc" data-candidate-desc="${c.id}" rows="2">${esc(c.desc)}</textarea>
    <button class="open-candidate" data-open-candidate="${c.id}">Open behavior →</button>
  </th>`;
}
function fitCriterionRow(r) {
  return `<tr>
    <td class="criterion-cell">
      <div class="criterion-line">
        <button class="criterion-id" data-open-criterion="${r.id}">${r.id}</button>
        <div class="criterion-main">
          <input class="matrix-input criterion-text" data-criterion-text="${r.id}" value="${attr(r.text)}">
          <div class="criterion-meta"><button class="status-pill ${r.status}" data-toggle-status="${r.id}">${r.status}</button><span>${esc(r.origin || "")}</span></div>
        </div>
      </div>
    </td>
    ${state.candidates.map((c) => fitCell(c, r)).join("")}
  </tr>`;
}
function fitCell(c, r) {
  const f = c.fit[r.id] || { state: "unknown", cause: "Not evaluated", refs: [], history: [] };
  const history = f.history || [];
  const last = history[history.length - 1];
  const delta = last?.from && last.from !== last.to ? `${labelFit(last.from)} → ${labelFit(last.to)}` : "";
  const isSelected = state.matrix.selectedCell === `${c.id}:${r.id}`;
  return `<td class="fit-cell-wrap"><button class="fit-cell ${f.state} ${delta ? "changed" : ""} ${isSelected ? "selected" : ""}" data-fit-cell="${c.id}:${r.id}">
    <span class="fit-mark">${fitSymbol(f.state)}</span>
    <span class="fit-name">${esc(delta || labelFit(f.state))}</span>
    ${f.refs?.length ? `<span class="fit-cause-dot" title="Causal trace available"></span>` : ""}
  </button></td>`;
}
function provisionalRow(r) {
  return `<tr class="provisional-row"><td class="criterion-cell">
    <div class="criterion-line ghost"><span class="criterion-id ghost-id">R?</span><div class="criterion-main"><div class="criterion-text-static">${esc(r.text)}</div><div class="criterion-meta"><span class="status-pill provisional">provisional</span><span>${esc(r.origin)}</span></div></div></div>
  </td><td colspan="${state.candidates.length}"><div class="provisional-actions"><span>This candidate introduced a consequence the current criteria do not judge.</span><div class="actions"><button class="btn primary" data-accept-provisional="${r.key}">Accept</button><button class="btn" data-edit-provisional="${r.key}">Edit</button><button class="btn quiet" data-dismiss-provisional="${r.key}">Dismiss</button></div></div></td></tr>`;
}

function reverseFitMatrix() {
  const candidate = candidateById(state, state.matrix.rotatedCandidate) || state.candidates[0];
  const rows = reverseFitRows(state, candidate.id);
  const accepted = state.criteria.filter((r) => r.status === "accepted");
  const gaps = accepted.filter((r) => criterionCoverage(state, candidate.id, r.id).gap);
  const orphans = rows.filter((row) => Object.values(row.relations).every((v) => v === "none"));
  return `<div class="reverse-shell">
    <div class="reverse-summary">
      <div><div class="ey">Rotation</div><div class="reverse-title">${esc(candidate.name)} · parts × criteria</div></div>
      <div class="coverage-chips">
        <button class="coverage-chip ${gaps.length ? "hot" : "good"}">${gaps.length ? `${gaps.length} coverage gap${gaps.length > 1 ? "s" : ""}` : "No accepted-criterion gaps"}</button>
        <button class="coverage-chip ${orphans.length ? "warn" : "good"}">${orphans.length ? `${orphans.length} orphan part${orphans.length > 1 ? "s" : ""}` : "No orphan parts"}</button>
      </div>
    </div>
    <div class="matrix-scroll"><table class="reverse-table"><thead><tr><th class="part-col"><span class="ey">Candidate part</span></th>${state.criteria.map((r) => `<th><button class="rotate-criterion" data-open-criterion="${r.id}">${r.id}<span>${esc(short(r.text, 34))}</span></button></th>`).join("")}</tr></thead><tbody>
      ${rows.map((row) => reverseRow(candidate, row)).join("")}
    </tbody></table></div>
    <div class="reverse-foot"><span>+ / − shows how each part relates to each criterion.</span><button class="btn primary" data-open-candidate="${candidate.id}">Open candidate behavior →</button></div>
  </div>`;
}
function reverseRow(candidate, row) {
  const place = placeForElement(candidate, row.id);
  const orphan = Object.values(row.relations).every((v) => v === "none");
  return `<tr class="${orphan ? "orphan-row" : ""}"><td class="part-cell"><button class="part-button" data-open-element="${candidate.id}:${row.type}:${row.id}">
    <span class="part-icon">${row.type === "affordance" ? "↗" : "◇"}</span><span><b>${esc(row.name)}</b><small>${esc(place?.name || "")}${orphan ? " · why does this exist?" : ""}</small></span>
  </button></td>${state.criteria.map((r) => {
    const rel = row.relations[r.id] || "none";
    return `<td><button class="relation ${rel}" data-relation="${candidate.id}:${row.id}:${r.id}" title="${relationLabel(rel)} ${r.id}"><span>${relationSymbol(rel)}</span><small>${relationLabel(rel)}</small></button></td>`;
  }).join("")}</tr>`;
}

function changeThread() {
  return `<section class="surface mini-panel"><div class="ey">Change thread</div><div class="thread">${state.changes.slice(-7).map((e) => `<span class="event ${e.kind}">${esc(e.text)}</span>`).join("")}</div></section>`;
}
function aiNudge() {
  let text = "Shape a candidate. I’ll reverse-fit the change against accepted criteria.";
  const a = candidateById(state, "A");
  if (a?.mechanisms.includes("quick") && !a.mechanisms.includes("riskGate")) text = "One thing changed: Quick approve weakens R2 because risk can be bypassed before commitment.";
  if (state.provisionalCriteria.length) text = "This also introduced a new judging question. Accept it only if recoverability should constrain every candidate.";
  if (a?.mechanisms.includes("riskGate") && criterionById(state, "R4") && !a.mechanisms.includes("undo")) text = "R2 is repaired. R4 is accepted, but Path A still lacks a recovery mechanism.";
  if (a?.mechanisms.includes("undo")) text = "The current Path A model is coherent enough to compare, spike, or slice.";
  return `<section class="surface mini-panel ai-nudge"><div><div class="ey">AI</div><div class="nudge-text">${esc(text)}</div></div>${a?.mechanisms.includes("quick") ? `<button class="btn" data-open-candidate="A">Show behavior</button>` : ""}</section>`;
}