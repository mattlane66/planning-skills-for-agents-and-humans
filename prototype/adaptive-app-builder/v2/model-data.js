const STORAGE_KEY = "adaptive-app-builder-v2";

const deepClone = (value) => JSON.parse(JSON.stringify(value));
const uid = (prefix = "id") => `${prefix}-${Math.random().toString(36).slice(2, 8)}${Date.now().toString(36).slice(-3)}`;

const fit = (state, cause, refs = []) => ({
  state,
  cause,
  refs,
  history: [{ from: null, to: state, cause, refs }],
});

const system = (id, name, criteria = {}, kind = "domain") => ({ id, name, criteria, kind });
const affordance = (id, name, criteria = {}, spikeId = null) => ({ id, name, criteria, spikeId });
const wire = (id, from, to, label = "") => ({ id, from, to, label });
const place = (id, name, state, affordances, systems, spikeId = null) => ({ id, name, state, affordances, systems, spikeId });

const graphA = () => ({
  places: [
    place("a-queue", "Queue", "Frequent manager", [
      affordance("a-open", "Open expense", { R1: "helps" }),
    ], [
      system("a-expenses", "Expense[]", { R1: "supports" }),
      system("a-context", "ReviewerContext", { R1: "supports", R3: "supports" }),
    ], "spike-a-queue"),
    place("a-review", "Review", "Expense selected", [
      affordance("a-inspect", "Inspect receipt", { R2: "helps" }),
      affordance("a-approve", "Approve", { R1: "helps", R3: "helps" }),
      affordance("a-flag", "Flag", { R2: "helps", R3: "helps" }),
    ], [
      system("a-expense", "Expense", { R1: "supports" }),
      system("a-decision", "ReviewDecision", { R3: "supports" }),
    ], "spike-a-review"),
    place("a-exception", "Exception", "Policy risk", [
      affordance("a-explain", "Explain exception", { R2: "helps" }, "spike-a-risk-interrupt"),
      affordance("a-approve-x", "Approve exception", { R3: "helps" }),
      affordance("a-flag-x", "Flag exception", { R2: "helps", R3: "helps" }),
    ], [
      system("a-policy-flag", "PolicyFlag", { R2: "supports" }),
      system("a-policy-evidence", "PolicyEvidence", { R2: "supports" }),
      system("a-reason", "ReviewDecision.reason", { R2: "supports", R3: "supports" }),
    ], "spike-a-exception"),
    place("a-confirm", "Confirmation", "Decision persisted", [
      affordance("a-done", "Decision persisted", { R3: "helps" }),
    ], [
      system("a-decision-confirm", "ReviewDecision", { R3: "supports" }),
      system("a-audit", "AuditEvent", { R3: "supports" }),
    ], "spike-a-confirm"),
  ],
  wires: [
    wire("aw1", "a-open", "a-inspect"),
    wire("aw2", "a-open", "a-approve", "routine"),
    wire("aw3", "a-inspect", "a-approve"),
    wire("aw4", "a-inspect", "a-flag", "concern"),
    wire("aw5", "a-approve", "a-done"),
    wire("aw6", "a-flag", "a-explain", "policy risk"),
    wire("aw7", "a-explain", "a-approve-x", "override"),
    wire("aw8", "a-explain", "a-flag-x", "reject / escalate"),
    wire("aw9", "a-approve-x", "a-done"),
    wire("aw10", "a-flag-x", "a-done"),
  ],
});

const graphB = () => ({
  places: [
    place("b-entry", "Queue", "Route by reviewer mode", [
      affordance("b-open-novice", "Open guided review", { R2: "helps" }),
      affordance("b-open-expert", "Open expert review", { R1: "helps", R3: "threatens" }),
    ], [
      system("b-expenses", "Expense[]", { R1: "supports" }),
      system("b-mode", "ReviewerMode", { R1: "supports", R3: "threatens" }),
    ], "spike-b-route"),
    place("b-guided", "Guided review", "Novice workflow", [
      affordance("b-check", "Step through receipt + policy", { R2: "helps" }),
      affordance("b-decide-g", "Decide", { R3: "helps" }),
    ], [
      system("b-guided-state", "GuidedReviewState", { R2: "supports" }),
      system("b-decision-g", "ReviewDecision", { R3: "supports" }),
    ]),
    place("b-expert", "Fast review", "Expert workflow", [
      affordance("b-quick-review", "Compact review", { R1: "helps", R2: "partial" }),
      affordance("b-decide-e", "Decide", { R1: "helps", R3: "threatens" }),
    ], [
      system("b-expert-state", "ExpertReviewState", { R1: "supports", R3: "threatens" }),
      system("b-decision-e", "ExpertDecision", { R3: "threatens" }),
    ], "spike-b-expert"),
    place("b-confirm", "Confirmation", "Workflow-specific persistence", [
      affordance("b-confirmed", "Decision persisted", { R3: "partial" }),
    ], [
      system("b-audit", "AuditEvent", { R3: "supports" }),
    ]),
  ],
  wires: [
    wire("bw1", "b-open-novice", "b-check", "novice"),
    wire("bw2", "b-open-expert", "b-quick-review", "expert"),
    wire("bw3", "b-check", "b-decide-g"),
    wire("bw4", "b-decide-g", "b-confirmed"),
    wire("bw5", "b-quick-review", "b-decide-e"),
    wire("bw6", "b-decide-e", "b-confirmed"),
  ],
});

const graphC = () => ({
  places: [
    place("c-queue", "Queue", "Expense selected", [
      affordance("c-open", "Ask for recommendation", { R1: "helps" }),
    ], [
      system("c-expenses", "Expense[]", { R1: "supports" }),
      system("c-context", "ReviewerContext", { R1: "supports" }),
    ]),
    place("c-recommend", "Recommendation", "AI proposes decision", [
      affordance("c-accept", "Accept recommendation", { R1: "helps", R2: "threatens" }, "spike-c-recommend"),
      affordance("c-expand", "Inspect rationale", { R2: "helps" }),
    ], [
      system("c-rec", "DecisionRecommendation", { R1: "supports" }),
      system("c-confidence", "Confidence", { R2: "partial" }),
    ], "spike-c-recommend"),
    place("c-risk", "Risk review", "Low confidence / policy exception", [
      affordance("c-evidence", "Review evidence", { R2: "helps" }),
      affordance("c-decide", "Make decision", { R3: "helps" }),
    ], [
      system("c-policy", "PolicyEvidence", { R2: "supports" }),
      system("c-decision", "ReviewDecision", { R3: "supports" }),
    ]),
    place("c-confirm", "Confirmation", "Decision persisted", [
      affordance("c-done", "Decision persisted", { R3: "helps" }),
    ], [
      system("c-audit", "AuditEvent", { R3: "supports" }),
    ]),
  ],
  wires: [
    wire("cw1", "c-open", "c-accept", "high confidence"),
    wire("cw2", "c-open", "c-expand", "inspect"),
    wire("cw3", "c-expand", "c-evidence", "risk / low confidence"),
    wire("cw4", "c-evidence", "c-decide"),
    wire("cw5", "c-decide", "c-done"),
    wire("cw6", "c-accept", "c-done"),
  ],
});

function seedState() {
  return {
    version: 2,
    frame: {
      x: "Managers face one dense expense queue. Routine reviews feel slow and risky cases are easy to skim past.",
      y: "Routine approvals happen almost instantly while unusual expenses reliably interrupt attention.",
      m: "People need more guidance when unfamiliar or when risk is high; expertise should reduce presentation overhead without changing decision semantics.",
      collapsed: true,
    },
    criteria: [
      { id: "R1", text: "Routine approvals should take only a few seconds.", status: "accepted", origin: "Frame · desired outcome" },
      { id: "R2", text: "Unusual expenses must remain conspicuous.", status: "accepted", origin: "Frame · risk condition" },
      { id: "R3", text: "Decision semantics stay stable across presentations.", status: "working", origin: "M · stable capability assumption" },
    ],
    candidates: [
      {
        id: "A", name: "Adaptive composition",
        desc: "One ReviewExpense capability and ReviewDecision model; context changes presentation, disclosure, and pacing.",
        fit: {
          R1: fit("strong", "One compact path can reduce routine review overhead.", ["a-open", "a-approve"]),
          R2: fit("strong", "Policy risk has a dedicated exception path.", ["a-flag", "a-explain"]),
          R3: fit("strong", "ReviewDecision is shared across presentations.", ["a-decision", "a-decision-confirm"]),
        },
        graph: graphA(), mechanisms: [],
      },
      {
        id: "B", name: "Separate workflows",
        desc: "Novice and experienced reviewers receive independent workflows optimized for each mode.",
        fit: {
          R1: fit("strong", "The expert flow is compact and direct.", ["b-open-expert", "b-quick-review"]),
          R2: fit("partial", "Guided review surfaces risk, but expert review can compress it.", ["b-check", "b-quick-review"]),
          R3: fit("weak", "Separate workflows introduce separate decision-state concepts.", ["b-decision-g", "b-decision-e"]),
        },
        graph: graphB(), mechanisms: [],
      },
      {
        id: "C", name: "Recommendation first",
        desc: "AI recommends a decision; detail expands when confidence or risk warrants attention.",
        fit: {
          R1: fit("strong", "High-confidence recommendations reduce decision effort.", ["c-accept"]),
          R2: fit("partial", "Risk is visible when rationale expands, but high-confidence acceptance can bypass it.", ["c-accept", "c-expand"]),
          R3: fit("partial", "Final ReviewDecision is stable, but recommendation semantics add another layer.", ["c-rec", "c-decision"]),
        },
        graph: graphC(), mechanisms: [],
      },
    ],
    provisionalCriteria: [],
    matrix: { mode: "fit", rotatedCandidate: "A", selectedCell: null },
    nav: { candidate: null, tab: "behavior" },
    selection: { elementId: null, elementType: null, criterionId: null, wireId: null },
    sliceDraft: [], sliceSuggestionsVisible: false, slicePreview: null,
    slices: [],
    spikes: {
      "spike-a-queue": { id: "spike-a-queue", candidateId: "A", targetType: "place", targetId: "a-queue", title: "Expert queue compression", uncertainty: "Can the expert queue become materially faster without hiding risk?", screen: "queue" },
      "spike-a-review": { id: "spike-a-review", candidateId: "A", targetType: "place", targetId: "a-review", title: "Compact expense review", uncertainty: "How much review detail can be compressed safely?", screen: "review" },
      "spike-a-risk-interrupt": { id: "spike-a-risk-interrupt", candidateId: "A", targetType: "affordance", targetId: "a-explain", title: "Risk interruption", uncertainty: "Does the exception interrupt command enough attention to prevent skimming?", screen: "exception" },
      "spike-a-exception": { id: "spike-a-exception", candidateId: "A", targetType: "place", targetId: "a-exception", title: "Exception state", uncertainty: "What must be visible before an exception can be approved?", screen: "exception" },
      "spike-a-confirm": { id: "spike-a-confirm", candidateId: "A", targetType: "place", targetId: "a-confirm", title: "Commitment + recovery", uncertainty: "What must remain available after a decision commits?", screen: "confirmation" },
      "spike-b-route": { id: "spike-b-route", candidateId: "B", targetType: "place", targetId: "b-entry", title: "Mode routing", uncertainty: "Will people understand which workflow they are entering?", screen: "queue" },
      "spike-b-expert": { id: "spike-b-expert", candidateId: "B", targetType: "place", targetId: "b-expert", title: "Expert workflow", uncertainty: "Can a separate expert flow preserve the same meaning?", screen: "review" },
      "spike-c-recommend": { id: "spike-c-recommend", candidateId: "C", targetType: "affordance", targetId: "c-accept", title: "Recommendation acceptance", uncertainty: "When is a recommendation safe to accept without inspecting rationale?", screen: "recommend" },
    },
    hifi: { spikeId: null, selectedElement: null, edits: {}, reconcileProposal: null },
    changes: [
      { id: uid("chg"), text: "Frame shaped", kind: "neutral" },
      { id: uid("chg"), text: "R1–R3 selected", kind: "neutral" },
      { id: uid("chg"), text: "Three paths shaped", kind: "neutral" },
    ],
    buildPacket: null,
  };
}

