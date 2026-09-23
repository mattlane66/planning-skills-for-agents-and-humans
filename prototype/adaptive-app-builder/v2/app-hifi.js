function hifiModal() {
  const spikeId = state.hifi.spikeId;
  if (!spikeId || state.hifi.reconcileProposal) return "";
  const spike = state.spikes[spikeId]; if (!spike) return "";
  const candidate = candidateById(state, spike.candidateId);
  const selected = state.hifi.selectedElement;
  return `<div class="modal-backdrop"><section class="hifi-modal">
    <header class="hifi-head"><div><div class="ey">Targeted fidelity spike · ${esc(candidate.name)}</div><div class="hifi-title">${esc(spike.title)}</div><div class="sub">${esc(spike.uncertainty)}</div></div><div class="actions"><button class="btn" data-action="reconcile-hifi">Reconcile learning</button><button class="icon-btn" data-action="close-hifi">×</button></div></header>
    <div class="hifi-workspace ${selected ? "inspecting" : ""}">
      <aside class="layer-panel"><div class="ey">Elements</div>${hifiLayers(spike).map((l) => `<button class="layer ${selected === l.id ? "active" : ""}" data-hifi-select="${l.id}">${esc(l.label)}</button>`).join("")}</aside>
      <div class="hifi-stage">${mockScreen(spike)}</div>
      ${selected ? hifiInspector(spike, selected) : `<aside class="inspector-placeholder"><div class="ey">Direct edit</div><div class="sub">Click any element on the canvas to edit it.</div></aside>`}
    </div>
  </section></div>`;
}

function hifiLayers(spike) {
  const common = [{ id: "brand", label: "Brand" }, { id: "search", label: "Search" }, { id: "user", label: "Reviewer context" }];
  const per = {
    queue: [{ id: "title", label: "Queue title" }, { id: "expense", label: "Expense row" }, { id: "quick", label: "Quick approve" }],
    review: [{ id: "title", label: "Review title" }, { id: "receipt", label: "Receipt summary" }, { id: "flag", label: "Flag" }, { id: "approve", label: "Approve" }],
    exception: [{ id: "title", label: "Expense title" }, { id: "warning", label: "Policy warning" }, { id: "evidence", label: "Risk evidence" }, { id: "flagX", label: "Flag" }, { id: "approveX", label: "Approve exception" }],
    confirmation: [{ id: "success", label: "Confirmation" }, { id: "undo", label: "Undo" }],
    recommend: [{ id: "recommend", label: "Recommendation" }, { id: "confidence", label: "Confidence" }, { id: "accept", label: "Accept" }, { id: "inspect", label: "Inspect rationale" }],
  };
  return common.concat(per[spike.screen] || []);
}
function hifiEditKey(spikeId, elementId) { return `${spikeId}:${elementId}`; }
function hifiEdit(spikeId, elementId) { return state.hifi.edits[hifiEditKey(spikeId, elementId)] || {}; }
function hifiText(spikeId, elementId, fallback) { return hifiEdit(spikeId, elementId).text ?? fallback; }
function uiElement(spikeId, id, html, cls = "") {
  const e = hifiEdit(spikeId, id);
  const style = `${e.hidden ? "display:none;" : ""}${e.emphasis === "quiet" ? "opacity:.5;" : ""}${e.emphasis === "strong" ? "font-weight:800;" : ""}${e.align ? `text-align:${e.align};` : ""}${e.width ? `max-width:${e.width}%;` : ""}${Number.isFinite(e.order) ? `order:${e.order};` : ""}`;
  return `<div class="ui-element ${state.hifi.selectedElement === id ? "selected" : ""} ${cls}" data-hifi-select="${id}" style="${style}">${html}</div>`;
}
function mockScreen(spike) {
  const id = spike.id;
  let body = "";
  if (spike.screen === "queue") {
    body = `${uiElement(id, "title", `<div class="screen-kicker">Expert review</div><h2>${esc(hifiText(id, "title", "Review expenses"))}</h2>`)}
      ${uiElement(id, "expense", `<div class="expense-card"><div><span class="screen-kicker">HOTEL</span><b>Acme offsite</b><span>Sep 18 · Receipt attached</span></div><strong>$1,842</strong>${candidateById(state, "A")?.mechanisms.includes("quick") ? `<button class="product-button primary">${esc(hifiText(id, "quick", "Quick approve"))}</button>` : ""}</div>`)}`;
  }
  if (spike.screen === "review") {
    body = `${uiElement(id, "title", `<div class="screen-kicker">Expense review</div><h2>${esc(hifiText(id, "title", "Acme offsite"))}</h2>`)}
      ${uiElement(id, "receipt", `<div class="receipt-card"><span>Total</span><strong>$1,842</strong><small>Hotel · Sep 18 · Receipt attached ✓</small></div>`)}
      <div class="product-actions">${uiElement(id, "flag", `<button class="product-button">${esc(hifiText(id, "flag", "Flag"))}</button>`)}${uiElement(id, "approve", `<button class="product-button primary">${esc(hifiText(id, "approve", "Approve"))}</button>`)}</div>`;
  }
  if (spike.screen === "exception") {
    body = `${uiElement(id, "title", `<div class="screen-kicker">Expense review</div><h2>${esc(hifiText(id, "title", "Acme offsite"))}</h2><p>Hotel · Sep 18 · $1,842</p>`)}
      ${uiElement(id, "warning", `<div class="policy-warning"><b>${esc(hifiText(id, "warning", "Rate is above policy"))}</b><span>$412/night · normal threshold $325</span></div>`, "critical")}
      ${uiElement(id, "evidence", `<div class="evidence-card"><span class="screen-kicker">Why this is unusual</span><p>${esc(hifiText(id, "evidence", "Hotel rate is 27% above the normal threshold. The receipt is valid; the exception is rate-based."))}</p></div>`)}
      <div class="product-actions">${uiElement(id, "flagX", `<button class="product-button">${esc(hifiText(id, "flagX", "Flag"))}</button>`)}${uiElement(id, "approveX", `<button class="product-button primary">${esc(hifiText(id, "approveX", "Approve exception"))}</button>`)}</div>`;
  }
  if (spike.screen === "confirmation") {
    const hasUndo = candidateById(state, "A")?.mechanisms.includes("undo");
    body = `${uiElement(id, "success", `<div class="receipt-card"><span class="screen-kicker">Saved</span><h2>${esc(hifiText(id, "success", "Expense approved"))}</h2><p>Decision recorded in the audit trail.</p>${hasUndo ? `<button class="product-button">${esc(hifiText(id, "undo", "Undo decision"))}</button>` : ""}</div>`)}`;
  }
  if (spike.screen === "recommend") {
    body = `${uiElement(id, "recommend", `<div class="receipt-card"><span class="screen-kicker">Recommendation</span><h2>${esc(hifiText(id, "recommend", "Approve"))}</h2><p>No policy exception detected.</p></div>`)}
      ${uiElement(id, "confidence", `<div class="confidence">High confidence · 94%</div>`)}
      <div class="product-actions">${uiElement(id, "inspect", `<button class="product-button">${esc(hifiText(id, "inspect", "Inspect rationale"))}</button>`)}${uiElement(id, "accept", `<button class="product-button primary">${esc(hifiText(id, "accept", "Accept recommendation"))}</button>`)}</div>`;
  }
  return `<div class="product-frame"><div class="product-top">${uiElement(id, "brand", `<b>${esc(hifiText(id, "brand", "Ledgerly"))}</b>`)}${uiElement(id, "search", `<span>${esc(hifiText(id, "search", "Search expenses…"))}</span>`)}${uiElement(id, "user", `<span>${esc(hifiText(id, "user", "Maya · Manager"))}</span>`)}</div><div class="product-body"><nav><b>Review</b><span>Expenses</span><span>History</span><span>Policy</span></nav><main>${body}</main></div></div>`;
}
function hifiInspector(spike, selected) {
  const e = hifiEdit(spike.id, selected);
  return `<aside class="hifi-inspector"><div class="ey">Selected element</div><div class="selected-name">${esc(selected)}</div>
    <label class="control"><span>Text / label</span><input data-hifi-prop="text" value="${attr(e.text ?? selected)}"></label>
    <label class="control"><span>Emphasis</span><select data-hifi-prop="emphasis"><option value="normal">Normal</option><option value="strong" ${e.emphasis === "strong" ? "selected" : ""}>Strong</option><option value="quiet" ${e.emphasis === "quiet" ? "selected" : ""}>Quiet</option></select></label>
    <label class="control"><span>Alignment</span><select data-hifi-prop="align"><option value="left">Left</option><option value="center" ${e.align === "center" ? "selected" : ""}>Center</option><option value="right" ${e.align === "right" ? "selected" : ""}>Right</option></select></label>
    <label class="control"><span>Width</span><input type="range" min="40" max="100" value="${e.width || 100}" data-hifi-prop="width"><small>${e.width || 100}%</small></label>
    <div class="actions"><button class="btn" data-action="move-earlier">Earlier</button><button class="btn" data-action="move-later">Later</button></div>
    <button class="btn full" data-action="toggle-hifi-hidden">${e.hidden ? "Show" : "Hide"}</button>
  </aside>`;
}

function reconcileModal() {
  const p = state.hifi.reconcileProposal;
  if (!p) return "";
  return `<div class="modal-backdrop"><section class="reconcile-card"><div class="ey">Reconcile fidelity → model</div><div class="reconcile-title">${esc(p.title)}</div><p>${esc(p.detail)}</p><div class="reconcile-impact">${esc(p.fit)}</div><div class="actions"><button class="btn quiet" data-action="discard-reconcile">Discard</button><button class="btn" data-action="adjust-reconcile">Adjust</button><button class="btn primary" data-action="apply-reconcile">Apply to breadboard</button></div></section></div>`;
}

function buildPacketModal() {
  const packet = state.buildPacket;
  if (!packet) return "";
  const slice = state.slices.find((s) => s.id === packet.sliceId);
  const candidate = candidateById(state, packet.candidateId);
  return `<div class="modal-backdrop"><section class="packet-card"><div class="between"><div><div class="ey">Committed build packet</div><div class="packet-title">${esc(slice?.name || "Selected slice")}</div><div class="sub">${esc(candidate?.name || "")} · frozen from accepted intent</div></div><button class="icon-btn" data-action="close-packet">×</button></div>
    <div class="packet-grid"><div><span class="ey">Accepted criteria</span>${packet.acceptedCriteria.map((r) => `<div class="packet-row"><b>${r.id}</b><span>${esc(r.text)}</span><small>${labelFit(r.fit.state)}</small></div>`).join("")}</div><div><span class="ey">Included behavior</span>${packet.elements.map((e) => `<div class="packet-row"><b>${e.type === "affordance" ? "↗" : "◇"}</b><span>${esc(e.name)}</span></div>`).join("")}</div></div>
    <div class="packet-foot"><span class="sub">Exploration outside this slice remains editable.</span><button class="btn" data-action="copy-packet">Copy JSON</button></div>
  </section></div>`;
}