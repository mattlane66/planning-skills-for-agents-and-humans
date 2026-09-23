const candidateById = (state, id) => state.candidates.find((c) => c.id === id);
const criterionById = (state, id) => state.criteria.find((r) => r.id === id);

function allElements(candidate) {
  const out = [];
  candidate.graph.places.forEach((p) => {
    out.push({ id: p.id, type: "place", name: p.name, criteria: {}, placeId: p.id });
    p.affordances.forEach((a) => out.push({ ...a, type: "affordance", placeId: p.id }));
    p.systems.forEach((s) => out.push({ ...s, type: "system", placeId: p.id }));
  });
  return out;
}

function elementById(candidate, id) {
  return allElements(candidate).find((e) => e.id === id) || null;
}

function placeForElement(candidate, id) {
  return candidate.graph.places.find((p) => p.id === id || p.affordances.some((a) => a.id === id) || p.systems.some((s) => s.id === id)) || null;
}

function addChange(state, text, kind = "neutral") {
  state.changes.push({ id: uid("chg"), text, kind });
  state.changes = state.changes.slice(-10);
}

function setFit(state, candidateId, criterionId, next, cause, refs = []) {
  const candidate = candidateById(state, candidateId);
  if (!candidate) return;
  const current = candidate.fit[criterionId] || fit("unknown", "Not yet evaluated.");
  const from = current.state;
  candidate.fit[criterionId] = {
    ...current,
    state: next,
    cause,
    refs,
    history: [...(current.history || []), { from, to: next, cause, refs }].slice(-8),
  };
  if (from !== next) addChange(state, `${criterionId} ${labelFit(from)} → ${labelFit(next)}`, next === "strong" ? "good" : next === "weak" ? "hot" : "neutral");
}

const labelFit = (v) => ({ strong: "Strong", partial: "Partial", weak: "Weak", unknown: "Unknown" }[v] || v);

const insertBefore = (arr, beforeId, item) => {
  const i = arr.findIndex((x) => x.id === beforeId);
  if (i < 0) arr.push(item); else arr.splice(i, 0, item);
};

function applyQuickApprove(state, candidate) {
  const queue = candidate.graph.places.find((p) => p.id === "a-queue");
  if (!queue.affordances.some((a) => a.id === "a-quick")) {
    queue.affordances.push(affordance("a-quick", "Quick approve routine", { R1: "helps", R2: "threatens" }, "spike-a-quick"));
    state.spikes["spike-a-quick"] = { id: "spike-a-quick", candidateId: "A", targetType: "affordance", targetId: "a-quick", title: "Quick approval", uncertainty: "Can a one-click commitment remain fast without bypassing risk?", screen: "queue" };
  }
  candidate.graph.wires = candidate.graph.wires.filter((w) => w.from !== "a-quick");
  candidate.graph.wires.push(wire("aw-quick-confirm", "a-quick", "a-done", "commit"));
  setFit(state, "A", "R1", "strong", "Quick approve preserves the shortest routine path.", ["a-quick"]);
  setFit(state, "A", "R2", "weak", "Quick approve can commit before PolicyFlag has a chance to interrupt the reviewer.", ["a-quick"]);
  if (!state.provisionalCriteria.some((r) => r.key === "recoverability") && !criterionById(state, "R4")) {
    state.provisionalCriteria.push({ key: "recoverability", text: "A committed approval must be recoverable.", origin: "Path A · Quick approve", sourceRefs: ["a-quick", "a-done"] });
    addChange(state, "R? recoverability surfaced", "hot");
  }
}

function applyRiskGate(state, candidate) {
  const queue = candidate.graph.places.find((p) => p.id === "a-queue");
  if (!queue.systems.some((s) => s.id === "a-risk-class")) queue.systems.push(system("a-risk-class", "RiskClassification", { R2: "supports" }, "classifier"));
  const quick = queue.affordances.find((a) => a.id === "a-quick");
  if (quick) quick.criteria = { R1: "helps", R2: "helps" };
  candidate.graph.wires = candidate.graph.wires.filter((w) => w.from !== "a-quick");
  candidate.graph.wires.push(wire("aw-quick-confirm", "a-quick", "a-done", "routine"));
  candidate.graph.wires.push(wire("aw-quick-risk", "a-quick", "a-explain", "risk"));
  setFit(state, "A", "R2", "strong", "RiskClassification now intercepts risky quick approvals before commitment.", ["a-quick", "a-risk-class", "a-explain"]);
}

function applyUndo(state, candidate) {
  const confirm = candidate.graph.places.find((p) => p.id === "a-confirm");
  const done = confirm.affordances.find((a) => a.id === "a-done");
  if (done) done.name = "Decision persisted";
  if (!confirm.affordances.some((a) => a.id === "a-undo")) confirm.affordances.push(affordance("a-undo", "Undo decision", { R4: "helps" }, "spike-a-confirm"));
  if (!confirm.systems.some((s) => s.id === "a-reversal")) confirm.systems.push(system("a-reversal", "Reversal", { R4: "supports" }, "event"));
  if (!candidate.graph.wires.some((w) => w.id === "aw-undo")) candidate.graph.wires.push(wire("aw-undo", "a-undo", "a-open", "reverse"));
  setFit(state, "A", "R4", "strong", "A committed ReviewDecision can be reversed through Undo.", ["a-undo", "a-reversal"]);
}

function applyRiskAcknowledgement(state, candidate) {
  const exception = candidate.graph.places.find((p) => p.id === "a-exception");
  if (!exception.affordances.some((a) => a.id === "a-ack-risk")) {
    insertBefore(exception.affordances, "a-approve-x", affordance("a-ack-risk", "Acknowledge policy risk", { R2: "helps" }));
    exception.systems.push(system("a-risk-ack", "RiskAcknowledgement", { R2: "supports" }, "event"));
    candidate.graph.wires = candidate.graph.wires.filter((w) => w.id !== "aw7");
    candidate.graph.wires.push(wire("aw-ack", "a-explain", "a-ack-risk", "understand"));
    candidate.graph.wires.push(wire("aw-ack-approve", "a-ack-risk", "a-approve-x", "override"));
  }
  setFit(state, "A", "R2", "strong", "Exception approval now requires explicit acknowledgement of the policy risk.", ["a-explain", "a-ack-risk", "a-risk-ack"]);
}

const MECHANISMS = {
  quick: { id: "quick", candidateId: "A", label: "One-click approve", description: "Allow routine expenses to commit directly from Queue.", apply: applyQuickApprove },
  riskGate: { id: "riskGate", candidateId: "A", label: "Risk gate", description: "Classify risk before quick approval can commit.", dependsOn: "quick", apply: applyRiskGate },
  undo: { id: "undo", candidateId: "A", label: "Undo", description: "Make committed decisions reversible.", dependsOnCriterion: "R4", apply: applyUndo },
  riskAck: { id: "riskAck", candidateId: "A", label: "Risk acknowledgement", description: "Require explicit acknowledgement before exception approval.", apply: applyRiskAcknowledgement },
};

function applyMechanism(state, mechanismId) {
  const mechanism = MECHANISMS[mechanismId];
  if (!mechanism) return { ok: false, reason: "Unknown mechanism" };
  const candidate = candidateById(state, mechanism.candidateId);
  if (!candidate) return { ok: false, reason: "Candidate not found" };
  if (candidate.mechanisms.includes(mechanismId)) return { ok: false, reason: "Already applied" };
  if (mechanism.dependsOn && !candidate.mechanisms.includes(mechanism.dependsOn)) return { ok: false, reason: `Requires ${MECHANISMS[mechanism.dependsOn]?.label || mechanism.dependsOn}` };
  if (mechanism.dependsOnCriterion && !criterionById(state, mechanism.dependsOnCriterion)) return { ok: false, reason: `Requires ${mechanism.dependsOnCriterion}` };
  candidate.mechanisms.push(mechanismId);
  mechanism.apply(state, candidate);
  addChange(state, `${mechanism.label} added`, mechanismId === "quick" ? "hot" : "good");
  return { ok: true };
}

function acceptProvisionalCriterion(state, key) {
  const idx = state.provisionalCriteria.findIndex((r) => r.key === key);
  if (idx < 0) return null;
  const provisional = state.provisionalCriteria[idx];
  let n = state.criteria.length + 1;
  while (criterionById(state, `R${n}`)) n += 1;
  const id = `R${n}`;
  state.criteria.push({ id, text: provisional.text, status: "accepted", origin: provisional.origin });
  state.candidates.forEach((candidate) => {
    if (candidate.id === "A") candidate.fit[id] = fit("weak", "Path A can commit a decision but has no reversal mechanism yet.", provisional.sourceRefs);
    else if (candidate.id === "B") candidate.fit[id] = fit("strong", "Separate workflows retain a post-decision confirmation path where reversal can be added consistently.", []);
    else candidate.fit[id] = fit("partial", "Recommendation-first can defer commitment, but recovery after acceptance is not explicit.", []);
  });
  state.provisionalCriteria.splice(idx, 1);
  addChange(state, `${id} accepted`, "neutral");
  return id;
}

function removeProvisionalCriterion(state, key) {
  state.provisionalCriteria = state.provisionalCriteria.filter((r) => r.key !== key);
  addChange(state, "Provisional criterion dismissed", "neutral");
}

function addCriterion(state, text = "New criterion") {
  let n = state.criteria.length + 1;
  while (criterionById(state, `R${n}`)) n += 1;
  const id = `R${n}`;
  state.criteria.push({ id, text, status: "working", origin: "Human added" });
  state.candidates.forEach((candidate) => { candidate.fit[id] = fit("unknown", "Not yet evaluated against this criterion.", []); });
  return id;
}

function addCandidate(state) {
  const id = `P${state.candidates.length + 1}`;
  const fitMap = {};
  state.criteria.forEach((r) => { fitMap[r.id] = fit("unknown", "Not yet evaluated.", []); });
  state.candidates.push({
    id, name: "New path", desc: "Describe a materially different approach.", fit: fitMap, mechanisms: [],
    graph: { places: [place(`${id}-start`, "Start", "Working state", [], [])], wires: [] },
  });
  return id;
}

function addPlace(state, candidateId, name = "New place") {
  const candidate = candidateById(state, candidateId); if (!candidate) return null;
  const id = uid(`${candidateId.toLowerCase()}-place`);
  candidate.graph.places.push(place(id, name, "Working state", [], []));
  addChange(state, `${name} added`, "neutral");
  return id;
}

function addAffordance(state, candidateId, placeId, name = "New affordance") {
  const candidate = candidateById(state, candidateId); if (!candidate) return null;
  const p = candidate.graph.places.find((x) => x.id === placeId); if (!p) return null;
  const id = uid(`${candidateId.toLowerCase()}-aff`);
  p.affordances.push(affordance(id, name, {}));
  addChange(state, `${name} added`, "neutral");
  return id;
}

function addSystemObject(state, candidateId, placeId, name = "NewSystemObject") {
  const candidate = candidateById(state, candidateId); if (!candidate) return null;
  const p = candidate.graph.places.find((x) => x.id === placeId); if (!p) return null;
  const id = uid(`${candidateId.toLowerCase()}-sys`);
  p.systems.push(system(id, name, {}, "domain"));
  addChange(state, `${name} added`, "neutral");
  return id;
}

function deleteElement(state, candidateId, elementId) {
  const candidate = candidateById(state, candidateId); if (!candidate) return false;
  const placeIndex = candidate.graph.places.findIndex((p) => p.id === elementId);
  if (placeIndex >= 0) {
    const ids = new Set([candidate.graph.places[placeIndex].id, ...candidate.graph.places[placeIndex].affordances.map((a) => a.id), ...candidate.graph.places[placeIndex].systems.map((s) => s.id)]);
    candidate.graph.places.splice(placeIndex, 1);
    candidate.graph.wires = candidate.graph.wires.filter((w) => !ids.has(w.from) && !ids.has(w.to));
    return true;
  }
  for (const p of candidate.graph.places) {
    const ai = p.affordances.findIndex((a) => a.id === elementId);
    if (ai >= 0) { p.affordances.splice(ai, 1); candidate.graph.wires = candidate.graph.wires.filter((w) => w.from !== elementId && w.to !== elementId); return true; }
    const si = p.systems.findIndex((s) => s.id === elementId);
    if (si >= 0) { p.systems.splice(si, 1); return true; }
  }
  return false;
}

function addWire(state, candidateId, from, to, label = "") {
  const candidate = candidateById(state, candidateId); if (!candidate || from === to) return null;
  if (candidate.graph.wires.some((w) => w.from === from && w.to === to)) return null;
  const id = uid("wire"); candidate.graph.wires.push(wire(id, from, to, label)); return id;
}

function removeWire(state, candidateId, wireId) {
  const candidate = candidateById(state, candidateId); if (!candidate) return;
  candidate.graph.wires = candidate.graph.wires.filter((w) => w.id !== wireId);
}

function reverseFitRows(state, candidateId) {
  const candidate = candidateById(state, candidateId); if (!candidate) return [];
  return allElements(candidate)
    .filter((e) => e.type !== "place")
    .map((e) => ({
      ...e,
      relations: Object.fromEntries(state.criteria.map((r) => [r.id, e.criteria?.[r.id] || "none"])),
    }));
}

function criterionCoverage(state, candidateId, criterionId) {
  const rows = reverseFitRows(state, candidateId);
  const supporting = rows.filter((r) => ["helps", "supports"].includes(r.relations[criterionId]));
  const threatening = rows.filter((r) => r.relations[criterionId] === "threatens");
  return { supporting, threatening, gap: supporting.length === 0 };
}

function suggestSlices(state, candidateId) {
  if (candidateId === "A") return [
    { id: "sg-a-routine", name: "Routine approval", source: "AI", reason: "Smallest visible end-to-end proof of fast routine review.", elements: ["a-open", "a-approve", "a-done"], systems: ["a-decision"] },
    { id: "sg-a-exception", name: "Exception handling", source: "AI", reason: "Keeps the risk path and PolicyEvidence boundary demoable.", elements: ["a-flag", "a-explain", ...(candidateById(state, "A").mechanisms.includes("riskAck") ? ["a-ack-risk"] : []), "a-approve-x", "a-done"], systems: ["a-policy-flag", "a-policy-evidence"] },
    { id: "sg-a-adaptive", name: "Adaptive expert review", source: "AI", reason: "Tests adaptive presentation without creating a second decision system.", elements: candidateById(state, "A").mechanisms.includes("quick") ? ["a-quick", ...(candidateById(state, "A").mechanisms.includes("riskGate") ? ["a-explain"] : []), "a-done"] : ["a-open", "a-approve", "a-done"], systems: ["a-context", "a-decision"] },
  ];
  if (candidateId === "B") return [
    { id: "sg-b-guided", name: "Guided novice review", source: "AI", reason: "A coherent end-to-end guided workflow.", elements: ["b-open-novice", "b-check", "b-decide-g", "b-confirmed"], systems: ["b-guided-state", "b-decision-g"] },
    { id: "sg-b-expert", name: "Expert workflow", source: "AI", reason: "Tests whether the fast path can preserve decision meaning.", elements: ["b-open-expert", "b-quick-review", "b-decide-e", "b-confirmed"], systems: ["b-expert-state", "b-decision-e"] },
  ];
  return [
    { id: "sg-c-rec", name: "Recommendation acceptance", source: "AI", reason: "Smallest end-to-end recommendation loop.", elements: ["c-open", "c-accept", "c-done"], systems: ["c-rec"] },
    { id: "sg-c-risk", name: "Risk expansion", source: "AI", reason: "Tests uncertainty disclosure and human override.", elements: ["c-open", "c-expand", "c-evidence", "c-decide", "c-done"], systems: ["c-confidence", "c-policy", "c-decision"] },
  ];
}

function makeBuildPacket(state, sliceId) {
  const slice = state.slices.find((s) => s.id === sliceId); if (!slice) return null;
  const candidate = candidateById(state, slice.candidateId); if (!candidate) return null;
  const acceptedCriteria = state.criteria.filter((r) => r.status === "accepted").map((r) => ({ ...r, fit: deepClone(candidate.fit[r.id]) }));
  const elements = allElements(candidate).filter((e) => slice.elements.includes(e.id) || slice.systems.includes(e.id));
  const wires = candidate.graph.wires.filter((w) => slice.elements.includes(w.from) && slice.elements.includes(w.to));
  return { id: uid("packet"), candidateId: candidate.id, sliceId, acceptedCriteria, elements, wires, createdAt: new Date().toISOString() };
}

function proposeReconciliation(state, spikeId) {
  const spike = state.spikes[spikeId]; if (!spike) return null;
  if (spike.id === "spike-a-quick" || spike.id === "spike-a-queue") {
    const a = candidateById(state, "A");
    if (a.mechanisms.includes("quick") && !a.mechanisms.includes("riskGate")) return { id: "reconcile-risk-gate", title: "Treat risk as a pre-commit branch", detail: "The high-fidelity quick action works only if risky expenses can interrupt before commitment.", action: "riskGate", fit: "R2 would move toward Strong." };
  }
  if (spike.screen === "exception" && !candidateById(state, "A").mechanisms.includes("riskAck")) return { id: "reconcile-risk-ack", title: "Make acknowledgement behavioral", detail: "The warning reads like a gate rather than passive copy. Add an explicit acknowledgement before exception approval.", action: "riskAck", fit: "R2 gains an explicit embodied mechanism." };
  return { id: "reconcile-note", title: "No structural change required", detail: "The fidelity spike clarified presentation without changing accepted behavior.", action: null, fit: "Keep the breadboard unchanged." };
}

function saveState(state) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) {}
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return seedState();
    const parsed = JSON.parse(raw);
    return parsed?.version === 2 ? parsed : seedState();
  } catch (_) { return seedState(); }
}