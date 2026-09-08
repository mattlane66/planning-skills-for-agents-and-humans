#!/usr/bin/env python3
from pathlib import Path
import subprocess

skill_path = Path("lead-user-research/SKILL.md")
skill = skill_path.read_text(encoding="utf-8")
start = skill.index("## Relationship to the planning workflow")
end = skill.index("## Hard methodological rules", start)
replacement = """## Relationship to the planning workflow

Use this as an optional upstream evidence move when a consequential decision needs future-facing trends, advanced users, pyramiding, or advanced analogs. It is not a mandatory predecessor to framing or a synonym for ordinary customer research. If the problem is already concrete, route directly to framing or shaping.

Research state is authoritative only for what the study found; it does not become planning truth. After Phase G/H, use [study-templates/research-to-frame-handoff.md](study-templates/research-to-frame-handoff.md) to produce the **Research-to-Planning Handoff**: evidence-backed planning inputs with explicit provenance. The research record remains cited evidence.

A human must accept, reject, or revise the handoff before downstream planning proceeds. For an E-only study, accept, reject, or revise it before invoking `framing-doc`; when Phase F already produced useful research-local frame/criteria/mechanism material, route directly to collaborative `shaping` after that same gate and import it as **Working** planning material with namespaced research provenance.

Choose the smallest downstream move. Do not make the human reconstruct or reselect the same material solely because the package boundary was crossed. Revisit a decision when a planning promotion gate remains unmet or a consequential planning input differs, especially project requirements, Appetite/cut line, project boundary, material evidence, or viable alternatives.

"""
skill = skill[:start] + replacement + skill[end:]
skill_path.write_text(skill, encoding="utf-8")

boundary_path = Path("lead-user-research/PACKAGE_BOUNDARY.md")
boundary = boundary_path.read_text(encoding="utf-8")
old_boundary = "- **Phase F present:** if Phase F already produced a defensible transformation frame, research-local fit criteria, or candidate mechanisms,"
new_boundary = "- **Phase F present:** if Phase F material already includes a defensible transformation frame, research-local fit criteria, or candidate mechanisms,"
if old_boundary not in boundary and new_boundary not in boundary:
    raise SystemExit("Phase F package-boundary route marker not found")
boundary = boundary.replace(old_boundary, new_boundary, 1)
boundary_path.write_text(boundary, encoding="utf-8")

phase_g_path = Path("lead-user-research/prompts/phase-g-decide.md")
phase_g = phase_g_path.read_text(encoding="utf-8")
marker = "When Phase F ran, explicitly state that its `ACCEPTED`, research `R##`, and `SELECTED`\nstates are research-local under `PACKAGE_BOUNDARY.md`."
if marker not in phase_g:
    raise SystemExit("Phase G marker not found")
replacement_marker = marker + " A research-local mechanism selection is\nnot a selected project shape and not a selected planning shape."
phase_g = phase_g.replace(marker, replacement_marker, 1)
phase_g_path.write_text(phase_g, encoding="utf-8")

controller_path = Path("lead-user-research/scripts/next_research_move.py")
controller = controller_path.read_text(encoding="utf-8")
old_phase_f_reason = "reason=\"At least one supported need passed the Concept Generation Gate and requires an evidence-backed x → f() → y research concept-evaluation frame.\"," 
new_phase_f_reason = "reason=\"At least one supported need passed the Concept Generation Gate and requires an evidence-backed x → f() → y research shaping frame for concept evaluation.\"," 
if old_phase_f_reason not in controller and new_phase_f_reason not in controller:
    raise SystemExit("Phase F controller reason not found")
controller = controller.replace(old_phase_f_reason, new_phase_f_reason, 1)
old_complete_reason = 'reason="The research study is complete. Its implications do not become accepted planning truth automatically.",'
new_complete_reason = 'reason="The research study is complete. Its research shaping frame and implications do not become accepted planning truth automatically.",'
if old_complete_reason not in controller and new_complete_reason not in controller:
    raise SystemExit("Controller completion reason not found")
controller = controller.replace(old_complete_reason, new_complete_reason, 1)
controller_path.write_text(controller, encoding="utf-8")

line_count = len(skill.splitlines())
if line_count > 500:
    raise SystemExit(f"Canonical SKILL.md still exceeds 500 lines: {line_count}")
print(f"Canonical SKILL.md line count: {line_count}")

# The repository owns packaged parity; use its canonical sync command rather than
# maintaining a second ad-hoc mirror list in this temporary helper.
subprocess.run(["bash", "scripts/sync-packaged-skills.sh", "sync"], check=True)
subprocess.run(["bash", "scripts/build-claude-plugin.sh"], check=True)
subprocess.run(
    ["python", "-m", "unittest", "tests.test_lead_user_package_boundary", "tests.test_lead_user_research"],
    check=True,
)
subprocess.run(["npm", "--prefix", "site", "ci"], check=True)
subprocess.run(["npm", "--prefix", "site", "run", "check"], check=True)
