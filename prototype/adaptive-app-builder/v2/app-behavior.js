function candidateWorkspace() {
  const candidate = candidateById(state, state.nav.candidate);
  if (!candidate) return "";
  return `<section class="candidate-workspace surface">
    <aside class="candidate-rail">
      <div class="candidate-kicker">${candidate.id} · candidate</div>
      <input class="rail-title" data-candidate-name="${candidate.id}" value="${attr(candidate.name)}">
      <textarea class="rail-desc" data-candidate-desc="${candidate.id}" rows="3">${esc(candidate.desc)}</textarea>
      <nav class="rail-nav">
        <button class="rail-tab ${state.nav.tab === "behavior" ? "active" : ""}" data-tab="behavior">Behavior</button>
        <button class="rail-tab ${state.nav.tab === "slices" ? "active" : ""}" data-tab="slices">Slices</button>
      </nav>
      <div class="rail-section">
        <div class="ey">Reverse-fit candidate</div>
        ${mechanismControls(candidate)}
      </div>
      <div class="rail-section">
        <button class="btn full" data-action="rotate-current">↻ Rotate fit check</button>
      </div>
    </aside>
    <div class="candidate-main">${state.nav.tab === "behavior" ? behaviorView(candidate) : slicesView(candidate)}</div>
  </section>`;
}

function mechanismControls(candidate) {
  if (candidate.id !== "A") return `<div class="rail-note">This path is behaviorally modeled. Edit its breadboard directly or rotate the fit check.</div>`;
  return Object.values(MECHANISMS).map((m) => {
    const applied = candidate.mechanisms.includes(m.id);
    const disabled = applied || (m.dependsOn && !candidate.mechanisms.includes(m.dependsOn)) || (m.dependsOnCriterion && !criterionById(state, m.dependsOnCriterion));
    return `<button class="mechanism ${applied ? "applied" : ""}" data-mechanism="${m.id}" ${disabled ? "disabled" : ""}><span>${applied ? "✓" : "+"}</span><div><b>${esc(m.label)}</b><small>${esc(m.description)}</small></div></button>`;
  }).join("");
}

function behaviorView(candidate) {
  const selection = currentSelection(candidate);
  return `<div class="candidate-toolbar">
      <div><div class="ey">Behavioral canvas</div><div class="title">Places · affordances · system language</div><div class="sub">Select a part to trace criteria, wiring, and slice membership.</div></div>
      <div class="actions"><button class="btn" data-action="add-place">+ Place</button><button class="btn primary" data-action="suggest-slices">AI · Suggest slices</button></div>
    </div>
    ${criterionTraceBar(candidate)}
    ${reverseFitBanner(candidate)}
    <div class="board-shell ${hoverSlice || state.slicePreview ? "slice-previewing" : ""}">
      <div class="board-scroll"><div class="board" id="board">
        <svg class="wire-svg" id="wire-svg"></svg>
        ${candidate.graph.places.map((p) => placeCard(candidate, p)).join("")}
      </div></div>
      ${state.sliceSuggestionsVisible ? sliceOverlay(candidate) : ""}
    </div>
    <div class="behavior-lower">
      ${selection ? behaviorInspector(candidate, selection) : reverseFitNudge(candidate)}
      ${humanSliceBar(candidate)}
    </div>`;
}

function reverseFitBanner(candidate) {
  const provisional = state.provisionalCriteria[0];
  const conflicts = state.criteria.filter((r) => r.status === "accepted" && candidate.fit?.[r.id]?.state === "weak");
  if (!provisional && !conflicts.length) return "";
  const conflict = conflicts[0];
  return `<div class="reverse-banner ${conflict ? "conflict" : "provisional"}">
    <div class="reverse-banner-main">
      <span class="ey">Reverse fit check</span>
      ${conflict ? `<b>${conflict.id} ${labelFit(candidate.fit[conflict.id].history?.at(-1)?.from || "strong")} → ${labelFit(candidate.fit[conflict.id].state)}</b><span>${esc(candidate.fit[conflict.id].cause)}</span>` : ""}
      ${provisional ? `<b>R? ${esc(provisional.text)}</b><span>${esc(provisional.origin)} introduced a consequence the current criteria do not judge.</span>` : ""}
    </div>
    <div class="actions">
      ${conflict ? `<button class="btn primary" data-conflict-action="candidate:${conflict.id}">Revise candidate</button><button class="btn" data-conflict-action="criterion:${conflict.id}">Revise criterion</button><button class="btn quiet" data-conflict-action="investigate:${conflict.id}">Investigate</button>` : ""}
      ${provisional ? `<button class="btn primary" data-accept-provisional="${provisional.key}">Accept R?</button><button class="btn" data-edit-provisional="${provisional.key}">Edit</button><button class="btn quiet" data-dismiss-provisional="${provisional.key}">Dismiss</button>` : ""}
    </div>
  </div>`;
}

function criterionTraceBar(candidate) {
  const rid = state.selection.criterionId;
  if (!rid) return `<div class="trace-strip"><span class="ey">Criterion trace</span><span class="sub">Click a criterion in the matrix, or a part below, to trace the relationship in both directions.</span></div>`;
  const r = criterionById(state, rid);
  const coverage = criterionCoverage(state, candidate.id, rid);
  return `<div class="trace-strip active"><button class="criterion-id" data-clear-criterion>${rid}</button><div><b>${esc(r?.text || rid)}</b><span class="sub">${coverage.supporting.length} supporting · ${coverage.threatening.length} threatening${coverage.gap ? " · coverage gap" : ""}</span></div><button class="btn quiet" data-clear-criterion>Clear</button></div>`;
}

function placeCard(candidate, p) {
  const selected = state.selection.elementId === p.id;
  const criterion = state.selection.criterionId;
  const implicated = criterion && [...p.affordances, ...p.systems].some((e) => e.criteria?.[criterion] && e.criteria[criterion] !== "none");
  const pageSpike = p.spikeId ? state.spikes[p.spikeId] : null;
  return `<article class="place-card ${selected ? "selected" : ""} ${implicated ? "criterion-hit" : ""}" data-place="${p.id}">
    <div class="place-head">
      <button class="place-title" data-select-element="place:${p.id}"><span class="ey">Place / state</span><b>${esc(p.name)}</b><small>${esc(p.state)}</small></button>
      ${pageSpike ? `<button class="spike-link" data-open-spike="${pageSpike.id}" title="${attr(pageSpike.uncertainty)}">Hi-fi ↗</button>` : ""}
    </div>
    <div class="affordance-list">${p.affordances.map((a) => affordanceRow(candidate, p, a)).join("")}</div>
    <button class="inline-add" data-add-affordance="${p.id}">+ affordance</button>
    <div class="system-block"><div class="ey">System language</div><div class="systems">${p.systems.map((s) => systemChip(candidate, p, s)).join("")}</div><button class="inline-add tiny" data-add-system="${p.id}">+ object</button></div>
  </article>`;
}

function affordanceRow(candidate, p, a) {
  const selected = state.selection.elementId === a.id;
  const rid = state.selection.criterionId;
  const relation = rid ? a.criteria?.[rid] : null;
  const sliceClass = sliceClassFor(a.id);
  const spike = a.spikeId ? state.spikes[a.spikeId] : null;
  const outgoing = candidate.graph.wires.filter((w) => w.from === a.id);
  return `<div class="affordance ${selected ? "selected" : ""} ${relation === "threatens" ? "threat" : relation ? "criterion-hit" : ""} ${sliceClass}" data-element="${a.id}">
    <span class="port out-port" aria-hidden="true"></span>
    <div class="aff-main">
      <button class="aff-name" data-select-element="affordance:${a.id}">${esc(a.name)}</button>
      <div class="aff-meta">${outgoing.length ? outgoing.map((w) => `<button class="wire-pill" data-select-wire="${w.id}">→ ${esc(targetName(candidate, w.to))}${w.label ? ` · ${esc(w.label)}` : ""}</button>`).join("") : `<span class="wire-pill terminal">terminal</span>`}</div>
    </div>
    <div class="aff-actions">
      ${spike ? `<button class="spike-dot" data-open-spike="${spike.id}" title="Hi-fi · ${attr(spike.uncertainty)}">◇</button>` : ""}
      <label class="slice-check" title="Add to human slice"><input type="checkbox" data-slice-check="${a.id}" ${state.sliceDraft.includes(a.id) ? "checked" : ""}><span></span></label>
    </div>
  </div>`;
}

function systemChip(candidate, p, s) {
  const selected = state.selection.elementId === s.id;
  const rid = state.selection.criterionId;
  const relation = rid ? s.criteria?.[rid] : null;
  return `<button class="system-chip ${selected ? "selected" : ""} ${relation === "threatens" ? "threat" : relation ? "criterion-hit" : ""} ${sliceClassFor(s.id)}" data-select-element="system:${s.id}">${esc(s.name)}</button>`;
}

function targetName(candidate, id) {
  const e = elementById(candidate, id); return e?.name || id;
}
function currentSelection(candidate) {
  if (!state.selection.elementId && !state.selection.wireId) return null;
  if (state.selection.wireId) return { type: "wire", wire: candidate.graph.wires.find((w) => w.id === state.selection.wireId) };
  return elementById(candidate, state.selection.elementId);
}

function behaviorInspector(candidate, selection) {
  if (selection.type === "wire") return wireInspector(candidate, selection.wire);
  const place = placeForElement(candidate, selection.id);
  const relations = Object.entries(selection.criteria || {}).filter(([, v]) => v && v !== "none");
  const relatedSlices = state.slices.filter((s) => s.candidateId === candidate.id && (s.elements.includes(selection.id) || s.systems.includes(selection.id)));
  const incoming = candidate.graph.wires.filter((w) => w.to === selection.id);
  const outgoing = candidate.graph.wires.filter((w) => w.from === selection.id);
  return `<section class="inspector-panel surface">
    <div class="between"><div><div class="ey">Selected ${esc(selection.type)}</div><input class="inspector-name" data-element-name="${selection.id}" value="${attr(selection.name)}"><div class="sub">${esc(place?.name || "")}</div></div><button class="icon-btn danger" data-delete-element="${selection.id}" title="Delete">×</button></div>
    <div class="impact-row"><span class="ey">Criteria</span>${relations.length ? relations.map(([rid, rel]) => `<button class="impact ${rel}" data-trace-criterion="${rid}"><b>${rid}</b> ${relationLabel(rel)}</button>`).join("") : `<button class="impact unknown" data-action="investigate-part">No criterion yet · investigate</button>`}</div>
    ${selection.type === "affordance" ? `<div class="connection-editor"><div><span class="ey">Wiring</span><div class="sub">${incoming.length} incoming · ${outgoing.length} outgoing</div></div><div class="connect-row"><select data-wire-target>${affordanceOptions(candidate, selection.id)}</select><input data-wire-label placeholder="branch label"><button class="btn" data-add-wire-from="${selection.id}">Connect</button></div></div>` : ""}
    <div class="inspector-foot"><span class="sub">${relatedSlices.length ? `In ${relatedSlices.map((s) => s.name).join(", ")}` : "Not in an accepted slice."}</span>${selection.spikeId ? `<button class="btn" data-open-spike="${selection.spikeId}">Open fidelity spike</button>` : ""}</div>
  </section>`;
}

function wireInspector(candidate, wire) {
  if (!wire) return reverseFitNudge(candidate);
  return `<section class="inspector-panel surface"><div class="between"><div><div class="ey">Selected wire</div><div class="wire-title">${esc(targetName(candidate, wire.from))} → ${esc(targetName(candidate, wire.to))}</div></div><button class="icon-btn danger" data-delete-wire="${wire.id}">×</button></div>
  <label class="control"><span>Branch label</span><input data-wire-label-edit="${wire.id}" value="${attr(wire.label || "")}" placeholder="e.g. risk"></label></section>`;
}

function affordanceOptions(candidate, exclude) {
  return allElements(candidate).filter((e) => e.type === "affordance" && e.id !== exclude).map((e) => `<option value="${e.id}">${esc(placeForElement(candidate, e.id)?.name || "")} · ${esc(e.name)}</option>`).join("");
}

function reverseFitNudge(candidate) {
  const accepted = state.criteria.filter((r) => r.status === "accepted");
  const gaps = accepted.filter((r) => criterionCoverage(state, candidate.id, r.id).gap);
  const orphan = reverseFitRows(state, candidate.id).filter((row) => Object.values(row.relations).every((v) => v === "none"));
  return `<section class="inspector-panel surface"><div><div class="ey">Reverse fit</div><div class="inspector-headline">${gaps.length || orphan.length ? "There are unresolved parts." : "Every accepted criterion has supporting behavior."}</div></div><div class="impact-row">${gaps.map((r) => `<button class="impact threatens" data-trace-criterion="${r.id}">${r.id} coverage gap</button>`).join("")}${orphan.slice(0, 3).map((o) => `<button class="impact unknown" data-select-element="${o.type}:${o.id}">${esc(short(o.name, 28))} · orphan</button>`).join("") || (!gaps.length ? `<span class="sub">Select any behavior to inspect what it earns.</span>` : "")}</div><button class="btn" data-action="rotate-current">Open rotated matrix</button></section>`;
}

function humanSliceBar(candidate) {
  return `<section class="slice-draft surface"><div><div class="ey">Human slice</div><div class="sub">${state.sliceDraft.length ? `${state.sliceDraft.length} affordance${state.sliceDraft.length > 1 ? "s" : ""} selected` : "Check affordances directly on the breadboard."}</div></div><div class="actions"><button class="btn quiet" data-action="clear-slice-draft" ${state.sliceDraft.length ? "" : "disabled"}>Clear</button><button class="btn primary" data-action="save-human-slice" ${state.sliceDraft.length ? "" : "disabled"}>Save slice</button></div></section>`;
}

function sliceOverlay(candidate) {
  const suggestions = suggestSlices(state, candidate.id);
  return `<aside class="slice-overlay"><div class="between"><div><div class="ey">AI slice spike</div><div class="overlay-title">Coherent demoable boundaries</div></div><button class="icon-btn" data-action="close-slice-overlay">×</button></div>
    <div class="slice-suggestions">${suggestions.map((s) => `<div class="slice-suggestion ${state.slicePreview === s.id ? "active" : ""}" data-slice-card="${s.id}">
      <button class="slice-card-main" data-preview-slice="${s.id}"><b>${esc(s.name)}</b><span>${esc(s.reason)}</span></button>
      <div class="actions"><button class="btn primary" data-use-suggestion="${s.id}">Use</button><button class="btn" data-edit-suggestion="${s.id}">Edit boundary</button><button class="btn quiet" data-dismiss-suggestion="${s.id}">Ignore</button></div>
    </div>`).join("")}</div>
  </aside>`;
}

function sliceClassFor(id) {
  const previewId = hoverSlice || state.slicePreview;
  if (!previewId) return "";
  const candidateId = state.nav.candidate;
  const s = suggestSlices(state, candidateId).find((x) => x.id === previewId);
  if (!s) return "slice-dim";
  return s.elements.includes(id) || s.systems.includes(id) ? "slice-hit" : "slice-dim";
}

function slicesView(candidate) {
  const suggestions = suggestSlices(state, candidate.id);
  const accepted = state.slices.filter((s) => s.candidateId === candidate.id);
  return `<div class="candidate-toolbar"><div><div class="ey">Vertical slices</div><div class="title">Bounded buildable behavior</div><div class="sub">AI and human slices share the same breadboard model.</div></div><button class="btn primary" data-action="suggest-slices">AI · Suggest slices</button></div>
    ${state.sliceSuggestionsVisible ? `<div class="slice-list suggestions-list">${suggestions.map((s) => sliceListCard(s, true)).join("")}</div>` : ""}
    <div class="slice-list">${accepted.length ? accepted.map((s) => sliceListCard(s, false)).join("") : `<div class="empty">No accepted slices yet. Define one on the breadboard or use an AI suggestion.</div>`}</div>`;
}
function sliceListCard(s, suggestion) {
  return `<article class="slice-card"><div><div class="slice-source">${esc(s.source || "AI")}${suggestion ? " · suggestion" : " · accepted slice"}</div><div class="slice-name">${esc(s.name)}</div><div class="sub">${esc(s.reason || "Human-selected behavior boundary.")}</div><div class="slice-flow">${(s.elements || []).map((id) => esc(targetName(candidateById(state, state.nav.candidate), id))).join(" → ")}</div></div><div class="actions">${suggestion ? `<button class="btn primary" data-use-suggestion="${s.id}">Use</button><button class="btn" data-edit-suggestion="${s.id}">Edit</button>` : `<button class="btn primary" data-build-slice="${s.id}">Build this slice</button><button class="btn quiet danger" data-delete-slice="${s.id}">Delete</button>`}</div></article>`;
}

function fitDrawer() {
  const key = state.matrix.selectedCell;
  if (!key) return "";
  const [cid, rid] = key.split(":");
  const candidate = candidateById(state, cid); const criterion = criterionById(state, rid);
  const f = candidate?.fit?.[rid]; if (!candidate || !criterion || !f) return "";
  const hist = (f.history || []).slice().reverse();
  return `<aside class="drawer">
    <div class="drawer-head"><div><div class="ey">Causal fit · ${rid} × ${cid}</div><div class="drawer-title">${fitSymbol(f.state)} ${labelFit(f.state)}</div></div><button class="icon-btn" data-action="close-drawer">×</button></div>
    <div class="drawer-criterion">${esc(criterion.text)}</div>
    <div class="causal-card"><div class="ey">Why</div><p>${esc(f.cause)}</p>${f.refs?.length ? `<div class="ref-list">${f.refs.map((id) => `<button class="ref-chip" data-jump-ref="${cid}:${id}">${esc(targetName(candidate, id))}</button>`).join("")}</div>` : ""}</div>
    ${hist.length > 1 ? `<div class="history"><div class="ey">Fit history</div>${hist.map((h) => `<div class="history-row"><span>${h.from ? `${labelFit(h.from)} → ` : ""}${labelFit(h.to)}</span><small>${esc(h.cause)}</small></div>`).join("")}</div>` : ""}
    <div class="drawer-actions"><button class="btn" data-cycle-fit="${cid}:${rid}">Change judgment</button>${f.refs?.length ? `<button class="btn primary" data-jump-ref="${cid}:${f.refs[0]}">Show behavior</button>` : ""}</div>
  </aside>`;
}