function drawWires() {
  const board = $("#board"); const svg = $("#wire-svg"); if (!board || !svg || !state.nav.candidate) return;
  const candidate = candidateById(state, state.nav.candidate); if (!candidate) return;
  const br = board.getBoundingClientRect();
  svg.setAttribute("width", board.scrollWidth); svg.setAttribute("height", board.scrollHeight); svg.innerHTML = "";
  const previewId = hoverSlice || state.slicePreview;
  const preview = previewId ? suggestSlices(state, candidate.id).find((s) => s.id === previewId) : null;
  candidate.graph.wires.forEach((w) => {
    const source = $(`[data-element="${CSS.escape(w.from)}"]`); const target = $(`[data-element="${CSS.escape(w.to)}"]`);
    if (!source || !target) return;
    const sr = source.getBoundingClientRect(); const tr = target.getBoundingClientRect();
    const x1 = sr.right - br.left; const y1 = sr.top - br.top + sr.height / 2; const x2 = tr.left - br.left; const y2 = tr.top - br.top + tr.height / 2; const mid = x1 + Math.max(26, (x2 - x1) / 2);
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", `M ${x1} ${y1} C ${mid} ${y1}, ${mid} ${y2}, ${x2} ${y2}`);
    path.classList.add("wire-path");
    if (state.selection.wireId === w.id) path.classList.add("selected");
    if (state.selection.elementId === w.from || state.selection.elementId === w.to) path.classList.add("traced");
    if (preview) {
      if (preview.elements.includes(w.from) && preview.elements.includes(w.to)) path.classList.add("slice-wire"); else path.classList.add("dim");
    }
    path.dataset.wire = w.id; path.style.pointerEvents = "stroke"; path.style.cursor = "pointer";
    g.appendChild(path);
    if (w.label) {
      const tx = document.createElementNS("http://www.w3.org/2000/svg", "text");
      tx.setAttribute("x", String((x1 + x2) / 2)); tx.setAttribute("y", String((y1 + y2) / 2 - 6)); tx.textContent = w.label; tx.classList.add("wire-label"); if (preview && !(preview.elements.includes(w.from) && preview.elements.includes(w.to))) tx.classList.add("dim"); g.appendChild(tx);
    }
    svg.appendChild(g);
  });
  $$('[data-wire]', svg).forEach((p) => p.addEventListener("click", () => { state.selection = { elementId: null, elementType: null, criterionId: state.selection.criterionId, wireId: p.dataset.wire }; saveAndRender(); }));
}

function updateSlicePreview(id) {
  const board = $("#board"); if (!board || !state.nav.candidate) return;
  const candidate = candidateById(state, state.nav.candidate); const s = id ? suggestSlices(state, candidate.id).find((x) => x.id === id) : null;
  $$('[data-element]', board).forEach((el) => { el.classList.remove("slice-hit", "slice-dim"); if (s) el.classList.add(s.elements.includes(el.dataset.element) ? "slice-hit" : "slice-dim"); });
  $$('.system-chip', board).forEach((el) => { const sid = el.dataset.selectElement?.split(":")[1]; el.classList.remove("slice-hit", "slice-dim"); if (s) el.classList.add(s.systems.includes(sid) ? "slice-hit" : "slice-dim"); });
  drawWires();
}

function bind() {
  $$('[data-action]').forEach((el) => el.addEventListener("click", () => action(el.dataset.action)));
  $$('[data-matrix-mode]').forEach((el) => el.addEventListener("click", () => { state.matrix.mode = el.dataset.matrixMode; state.matrix.selectedCell = null; saveAndRender(); }));
  $('[data-rotate-candidate]')?.addEventListener("change", (e) => { state.matrix.rotatedCandidate = e.target.value; saveAndRender(); });
  $$('[data-open-candidate]').forEach((el) => el.addEventListener("click", () => openCandidate(el.dataset.openCandidate)));
  $$('[data-candidate-name]').forEach((el) => el.addEventListener("change", (e) => mutate("Candidate renamed", () => { candidateById(state, e.target.dataset.candidateName).name = e.target.value; })));
  $$('[data-candidate-desc]').forEach((el) => el.addEventListener("change", (e) => mutate("Candidate description changed", () => { candidateById(state, e.target.dataset.candidateDesc).desc = e.target.value; })));
  $$('[data-criterion-text]').forEach((el) => el.addEventListener("change", (e) => mutate(`${e.target.dataset.criterionText} revised`, () => { criterionById(state, e.target.dataset.criterionText).text = e.target.value; })));
  $$('[data-toggle-status]').forEach((el) => el.addEventListener("click", () => mutate(`${el.dataset.toggleStatus} status changed`, () => { const r = criterionById(state, el.dataset.toggleStatus); r.status = r.status === "accepted" ? "working" : "accepted"; })));
  $$('[data-fit-cell]').forEach((el) => el.addEventListener("click", () => { state.matrix.selectedCell = el.dataset.fitCell; saveAndRender(); }));
  $$('[data-open-criterion]').forEach((el) => el.addEventListener("click", () => { state.selection.criterionId = el.dataset.openCriterion; const cid = state.matrix.mode === "reverse" ? state.matrix.rotatedCandidate : "A"; openCandidate(cid, null, el.dataset.openCriterion); }));
  $$('[data-accept-provisional]').forEach((el) => el.addEventListener("click", () => mutate(null, () => acceptProvisionalCriterion(state, el.dataset.acceptProvisional))));
  $$('[data-dismiss-provisional]').forEach((el) => el.addEventListener("click", () => mutate("Criterion dismissed", () => removeProvisionalCriterion(state, el.dataset.dismissProvisional))));
  $$('[data-edit-provisional]').forEach((el) => el.addEventListener("click", () => { const p = state.provisionalCriteria.find((x) => x.key === el.dataset.editProvisional); const next = prompt("Edit provisional criterion", p?.text || ""); if (next) mutate("Provisional criterion edited", () => { p.text = next; }); }));
  $$('[data-cycle-fit]').forEach((el) => el.addEventListener("click", () => cycleFit(el.dataset.cycleFit)));
  $$('[data-jump-ref]').forEach((el) => el.addEventListener("click", () => { const [cid, ref] = el.dataset.jumpRef.split(":"); openCandidate(cid, ref); }));
  $$('[data-open-element]').forEach((el) => el.addEventListener("click", () => { const [cid, type, id] = el.dataset.openElement.split(":"); openCandidate(cid, id); state.selection.elementType = type; }));
  $$('[data-relation]').forEach((el) => el.addEventListener("click", () => { const [cid, id, rid] = el.dataset.relation.split(":"); openCandidate(cid, id, rid); }));
  $$('[data-conflict-action]').forEach((el) => el.addEventListener("click", () => handleConflictAction(el.dataset.conflictAction)));
  $$('[data-tab]').forEach((el) => el.addEventListener("click", () => { state.nav.tab = el.dataset.tab; saveAndRender(); }));
  $$('[data-mechanism]').forEach((el) => el.addEventListener("click", () => mutate(null, () => { const r = applyMechanism(state, el.dataset.mechanism); if (!r.ok) setTimeout(() => toast(r.reason), 0); })));
  $$('[data-select-element]').forEach((el) => el.addEventListener("click", () => { const [type, id] = el.dataset.selectElement.split(":"); state.selection.elementId = id; state.selection.elementType = type; state.selection.wireId = null; saveAndRender(); }));
  $$('[data-select-wire]').forEach((el) => el.addEventListener("click", () => { state.selection.wireId = el.dataset.selectWire; state.selection.elementId = null; saveAndRender(); }));
  $$('[data-trace-criterion]').forEach((el) => el.addEventListener("click", () => { state.selection.criterionId = el.dataset.traceCriterion; saveAndRender(); }));
  $$('[data-clear-criterion]').forEach((el) => el.addEventListener("click", () => { state.selection.criterionId = null; saveAndRender(); }));
  $$('[data-add-affordance]').forEach((el) => el.addEventListener("click", () => { const name = prompt("Affordance name", "New affordance"); if (name) mutate("Affordance added", () => { const id = addAffordance(state, state.nav.candidate, el.dataset.addAffordance, name); state.selection.elementId = id; state.selection.elementType = "affordance"; }); }));
  $$('[data-add-system]').forEach((el) => el.addEventListener("click", () => { const name = prompt("System object name", "NewSystemObject"); if (name) mutate("System object added", () => { const id = addSystemObject(state, state.nav.candidate, el.dataset.addSystem, name); state.selection.elementId = id; state.selection.elementType = "system"; }); }));
  $$('[data-delete-element]').forEach((el) => el.addEventListener("click", () => mutate("Behavior removed", () => { deleteElement(state, state.nav.candidate, el.dataset.deleteElement); state.selection.elementId = null; })));
  $$('[data-element-name]').forEach((el) => el.addEventListener("change", (e) => mutate("Behavior renamed", () => { const candidate = candidateById(state, state.nav.candidate); const item = elementById(candidate, e.target.dataset.elementName); if (item) { const p = candidate.graph.places.find((x) => x.id === item.id); if (p) p.name = e.target.value; else { for (const pl of candidate.graph.places) { const a = pl.affordances.find((x) => x.id === item.id); if (a) a.name = e.target.value; const s = pl.systems.find((x) => x.id === item.id); if (s) s.name = e.target.value; } } } })));
  $$('[data-add-wire-from]').forEach((el) => el.addEventListener("click", () => { const panel = el.closest(".connection-editor"); const target = $('[data-wire-target]', panel)?.value; const label = $('[data-wire-label]', panel)?.value || ""; if (target) mutate("Wire added", () => addWire(state, state.nav.candidate, el.dataset.addWireFrom, target, label)); }));
  $$('[data-delete-wire]').forEach((el) => el.addEventListener("click", () => mutate("Wire removed", () => { removeWire(state, state.nav.candidate, el.dataset.deleteWire); state.selection.wireId = null; })));
  $$('[data-wire-label-edit]').forEach((el) => el.addEventListener("change", (e) => mutate("Branch label changed", () => { const c = candidateById(state, state.nav.candidate); const w = c.graph.wires.find((x) => x.id === e.target.dataset.wireLabelEdit); if (w) w.label = e.target.value; })));
  $$('[data-slice-check]').forEach((el) => el.addEventListener("change", (e) => { const id = e.target.dataset.sliceCheck; state.sliceDraft = e.target.checked ? [...new Set([...state.sliceDraft, id])] : state.sliceDraft.filter((x) => x !== id); saveAndRender(); }));
  $$('[data-preview-slice]').forEach((el) => { el.addEventListener("mouseenter", () => { hoverSlice = el.dataset.previewSlice; updateSlicePreview(hoverSlice); }); el.addEventListener("mouseleave", () => { hoverSlice = null; updateSlicePreview(state.slicePreview); }); el.addEventListener("click", () => { state.slicePreview = el.dataset.previewSlice; saveAndRender(); }); });
  $$('[data-slice-card]').forEach((el) => { el.addEventListener("mouseenter", () => { hoverSlice = el.dataset.sliceCard; updateSlicePreview(hoverSlice); }); el.addEventListener("mouseleave", () => { hoverSlice = null; updateSlicePreview(state.slicePreview); }); });
  $$('[data-use-suggestion]').forEach((el) => el.addEventListener("click", () => useSuggestion(el.dataset.useSuggestion)));
  $$('[data-edit-suggestion]').forEach((el) => el.addEventListener("click", () => editSuggestion(el.dataset.editSuggestion)));
  $$('[data-dismiss-suggestion]').forEach((el) => el.addEventListener("click", () => { state.sliceSuggestionsVisible = false; state.slicePreview = null; saveAndRender(); }));
  $$('[data-delete-slice]').forEach((el) => el.addEventListener("click", () => mutate("Slice removed", () => { state.slices = state.slices.filter((s) => s.id !== el.dataset.deleteSlice); })));
  $$('[data-build-slice]').forEach((el) => el.addEventListener("click", () => mutate("Slice committed to build", () => { state.buildPacket = makeBuildPacket(state, el.dataset.buildSlice); })));
  $$('[data-open-spike]').forEach((el) => el.addEventListener("click", () => { state.hifi.spikeId = el.dataset.openSpike; state.hifi.selectedElement = null; saveAndRender(); }));
  $$('[data-hifi-select]').forEach((el) => el.addEventListener("click", (e) => { e.stopPropagation(); state.hifi.selectedElement = el.dataset.hifiSelect; saveAndRender(); }));
  $$('[data-hifi-prop]').forEach((el) => { const ev = el.type === "range" ? "input" : (el.tagName === "SELECT" ? "change" : "change"); el.addEventListener(ev, (e) => { const key = `${state.hifi.spikeId}:${state.hifi.selectedElement}`; state.hifi.edits[key] = { ...(state.hifi.edits[key] || {}), [e.target.dataset.hifiProp]: e.target.type === "range" ? Number(e.target.value) : e.target.value }; saveAndRender(); }); });
  $$('[data-frame]').forEach((el) => el.addEventListener("change", (e) => mutate("Frame refined", () => { state.frame[e.target.dataset.frame] = e.target.value; })));
  window.addEventListener("resize", onResize, { once: true });
}

function action(name) {
  if (name === "undo") return undo();
  if (name === "redo") return redo();
  if (name === "reset") { if (confirm("Reset the prototype to its seeded state?")) { undoStack.push(snapshot()); state = seedState(); saveAndRender(); } return; }
  if (name === "home") { state.nav.candidate = null; state.nav.tab = "behavior"; state.selection.elementId = null; state.selection.wireId = null; state.sliceSuggestionsVisible = false; saveAndRender(); return; }
  if (name === "toggle-frame") { state.frame.collapsed = !state.frame.collapsed; saveAndRender(); return; }
  if (name === "add-criterion") { const text = prompt("Criterion", "New criterion"); if (text) mutate("Criterion added", () => addCriterion(state, text)); return; }
  if (name === "add-candidate") { mutate("Candidate path added", () => addCandidate(state)); return; }
  if (name === "close-drawer") { state.matrix.selectedCell = null; saveAndRender(); return; }
  if (name === "rotate-current") { state.matrix.mode = "reverse"; state.matrix.rotatedCandidate = state.nav.candidate; state.nav.candidate = null; saveAndRender(); return; }
  if (name === "add-place") { const n = prompt("Place / state name", "New place"); if (n) mutate("Place added", () => { const id = addPlace(state, state.nav.candidate, n); state.selection.elementId = id; state.selection.elementType = "place"; }); return; }
  if (name === "investigate-part") { mutate("Unknown routed to investigation", () => { addChange(state, "Part marked for reverse-fit investigation", "neutral"); }); toast("Marked as an explicit unknown"); return; }
  if (name === "suggest-slices") { state.sliceSuggestionsVisible = true; state.slicePreview = suggestSlices(state, state.nav.candidate)[0]?.id || null; saveAndRender(); return; }
  if (name === "close-slice-overlay") { state.sliceSuggestionsVisible = false; state.slicePreview = null; saveAndRender(); return; }
  if (name === "clear-slice-draft") { state.sliceDraft = []; saveAndRender(); return; }
  if (name === "save-human-slice") { saveHumanSlice(); return; }
  if (name === "close-hifi") { state.hifi.spikeId = null; state.hifi.selectedElement = null; saveAndRender(); return; }
  if (name === "reconcile-hifi") { state.hifi.reconcileProposal = proposeReconciliation(state, state.hifi.spikeId); saveAndRender(); return; }
  if (name === "discard-reconcile") { state.hifi.reconcileProposal = null; state.hifi.spikeId = null; state.hifi.selectedElement = null; saveAndRender(); return; }
  if (name === "adjust-reconcile") { const p = state.hifi.reconcileProposal; const next = prompt("Adjust proposed learning", p?.detail || ""); if (p && next) { p.detail = next; saveAndRender(); } return; }
  if (name === "apply-reconcile") { applyReconcile(); return; }
  if (name === "move-earlier" || name === "move-later") {
    const key = `${state.hifi.spikeId}:${state.hifi.selectedElement}`;
    const current = state.hifi.edits[key]?.order || 0;
    state.hifi.edits[key] = { ...(state.hifi.edits[key] || {}), order: current + (name === "move-earlier" ? -1 : 1) };
    saveAndRender();
    return;
  }
  if (name === "toggle-hifi-hidden") { const key = `${state.hifi.spikeId}:${state.hifi.selectedElement}`; state.hifi.edits[key] = { ...(state.hifi.edits[key] || {}), hidden: !state.hifi.edits[key]?.hidden }; saveAndRender(); return; }
  if (name === "close-packet") { state.buildPacket = null; saveAndRender(); return; }
  if (name === "copy-packet") { navigator.clipboard?.writeText(JSON.stringify(state.buildPacket, null, 2)); toast("Build packet copied"); return; }
}

function handleConflictAction(value) {
  const [kind, rid] = value.split(":");
  const candidate = candidateById(state, state.nav.candidate);
  if (!candidate) return;
  if (kind === "candidate") {
    const ref = candidate.fit[rid]?.refs?.[0] || null;
    state.selection.criterionId = rid;
    state.selection.elementId = ref;
    state.selection.elementType = ref ? elementById(candidate, ref)?.type || null : null;
    saveAndRender();
    toast("Candidate behavior highlighted");
    return;
  }
  if (kind === "criterion") {
    const r = criterionById(state, rid);
    const next = prompt(`Revise ${rid}`, r?.text || "");
    if (next && r) mutate(`${rid} explicitly revised`, () => { r.text = next; r.status = "working"; });
    return;
  }
  if (kind === "investigate") {
    mutate(`${rid} routed to investigation`, () => setFit(state, candidate.id, rid, "unknown", "Conflict is unresolved; evidence is required before judging fit.", candidate.fit[rid]?.refs || []));
    return;
  }
}

function openCandidate(cid, elementId = null, criterionId = null) {
  state.nav.candidate = cid; state.nav.tab = "behavior"; state.matrix.selectedCell = null; state.sliceSuggestionsVisible = false; state.slicePreview = null;
  state.selection.elementId = elementId; state.selection.wireId = null; state.selection.criterionId = criterionId ?? state.selection.criterionId;
  if (elementId) state.selection.elementType = elementById(candidateById(state, cid), elementId)?.type || null;
  saveAndRender();
}

function cycleFit(key) {
  const [cid, rid] = key.split(":"); const candidate = candidateById(state, cid); const current = candidate.fit[rid]?.state || "unknown"; const order = ["strong", "partial", "weak", "unknown"]; const next = order[(order.indexOf(current) + 1) % order.length];
  mutate(`${rid} judgment changed`, () => setFit(state, cid, rid, next, "Human changed the fit judgment directly in the matrix.", candidate.fit[rid]?.refs || []));
  state.matrix.selectedCell = `${cid}:${rid}`;
}

function useSuggestion(id) {
  const candidateId = state.nav.candidate; const s = suggestSlices(state, candidateId).find((x) => x.id === id); if (!s) return;
  mutate("AI slice accepted", () => { state.slices.push({ ...deepClone(s), id: uid("slice"), candidateId, source: "AI suggestion" }); state.sliceSuggestionsVisible = false; state.slicePreview = null; state.nav.tab = "slices"; });
}
function editSuggestion(id) {
  const candidateId = state.nav.candidate; const s = suggestSlices(state, candidateId).find((x) => x.id === id); if (!s) return;
  state.sliceDraft = [...s.elements]; state.sliceSuggestionsVisible = false; state.slicePreview = null; state.nav.tab = "behavior"; saveAndRender(); toast("Suggestion loaded as an editable human boundary");
}
function saveHumanSlice() {
  if (!state.sliceDraft.length) return;
  const name = prompt("Slice name", `Human slice ${state.slices.filter((s) => s.candidateId === state.nav.candidate).length + 1}`); if (!name) return;
  mutate("Human slice saved", () => { state.slices.push({ id: uid("slice"), candidateId: state.nav.candidate, name, source: "Human selected", reason: "Human-selected boundary on the behavior graph.", elements: [...state.sliceDraft], systems: [] }); state.sliceDraft = []; state.nav.tab = "slices"; });
}
function applyReconcile() {
  const p = state.hifi.reconcileProposal; if (!p) return;
  mutate("Hi-fi learning reconciled", () => {
    if (p.action) applyMechanism(state, p.action);
    addChange(state, `Hi-fi → model: ${p.title}`, "good");
    state.hifi.reconcileProposal = null; state.hifi.spikeId = null; state.hifi.selectedElement = null;
  });
}
function onResize() {
  clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { drawWires(); }, 120);
}
function short(s, n) { const t = String(s || ""); return t.length > n ? `${t.slice(0, n - 1)}…` : t; }
function toast(message) {
  requestAnimationFrame(() => {
    const el = $("#toast"); if (!el) return; el.textContent = message; el.classList.remove("hidden"); clearTimeout(window.__toastTimer); window.__toastTimer = setTimeout(() => el.classList.add("hidden"), 1800);
  });
}

render();
window.__adaptiveApp = { get state() { return state; }, render, undo, redo, seedState };