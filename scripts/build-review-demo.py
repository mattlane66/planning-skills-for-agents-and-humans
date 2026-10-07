#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DATA = Path(sys.argv[1])
OUTDIR = Path(sys.argv[2])
OUTDIR.mkdir(parents=True, exist_ok=True)
VIDEO = OUTDIR / "planning-skills-review-demo.mp4"

data = json.loads(DATA.read_text(encoding="utf-8"))

W, H = 1280, 720
BG = "#0b0f14"
PANEL = "#121821"
TEXT = "#f5f7fa"
MUTED = "#aab4c0"
ACCENT = "#5ee2a0"
BLUE = "#78b7ff"
BORDER = "#263241"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill: str, width: int, spacing=1.22):
    x, y = xy
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    line_h = int(fnt.size * spacing)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def panel(draw, box, radius=22):
    draw.rounded_rectangle(box, radius=radius, fill=PANEL, outline=BORDER, width=2)


def pill(draw, x, y, label, fill="#153326", textfill=ACCENT):
    f = font(20, True)
    bb = draw.textbbox((0, 0), label, font=f)
    ww, hh = bb[2] - bb[0] + 26, bb[3] - bb[1] + 18
    draw.rounded_rectangle((x, y, x + ww, y + hh), radius=hh // 2, fill=fill)
    draw.text((x + 13, y + 7), label, font=f, fill=textfill)
    return ww


def heading(draw, title, subtitle=None):
    draw.text((70, 48), title, font=font(38, True), fill=TEXT)
    if subtitle:
        draw.text((72, 98), subtitle, font=font(20), fill=MUTED)
    draw.line((70, 137, 1210, 137), fill=BORDER, width=2)


def save_scene(im, index):
    path = OUTDIR / f"scene{index}.png"
    im.save(path)
    return path


tool_names = [tool["name"] for tool in data["tools"]]
recommendation = data["recommendation"].strip()
shape_rule = "Exploration is fluid. Commitment is gated."
if shape_rule not in data["shaping"]:
    shape_rule = "Exploration can be fluid. Promotion cannot."

# Scene 1
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
panel(d, (55, 65, 1225, 655), 28)
d.text((95, 120), "Planning Skills", font=font(58, True), fill=TEXT)
d.text((98, 195), "Reviewer walkthrough", font=font(30), fill=ACCENT)
wrap(d, (98, 260),
     "A public OpenAI plugin combining 14 reusable planning skills with a live universal MCP server.",
     font(28), TEXT, 1040, 1.3)
y = 400
for label in [
    "14 packaged skills",
    f"{len(tool_names)} live production MCP tools",
    "One HTTPS MCP URL for every user",
    "Explicit human promotion gates preserved",
]:
    d.ellipse((102, y + 7, 118, y + 23), fill=ACCENT)
    d.text((135, y), label, font=font(24), fill=TEXT)
    y += 52
save_scene(im, 1)

# Scene 2
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
heading(d, "How the plugin works", "Skills carry the method. MCP carries canonical infrastructure.")
boxes = [
    (70, 235, 275, 485, "User work", "requirements\nevidence\ncode"),
    (335, 210, 560, 510, "Planning Router", "smallest useful\nnext move"),
    (620, 185, 890, 535, "14 Skills", "framing • shaping\nbreadboarding\ncontracts • reflection"),
    (950, 235, 1210, 485, "MCP", "routing\ncanonical resources\ncontracts"),
]
for x1, y1, x2, y2, h, sub in boxes:
    panel(d, (x1, y1, x2, y2))
    d.text((x1 + 22, y1 + 28), h, font=font(25, True), fill=TEXT)
    yy = y1 + 85
    for line in sub.split("\n"):
        d.text((x1 + 22, yy), line, font=font(19), fill=MUTED)
        yy += 38
for x1, x2 in [(275, 335), (560, 620), (890, 950)]:
    d.line((x1 + 8, 350, x2 - 12, 350), fill=BLUE, width=5)
    d.polygon([(x2 - 13, 342), (x2 - 13, 358), (x2 - 1, 350)], fill=BLUE)
pill(d, 70, 585, "Exploration is fluid. Commitment is gated.")
wrap(d, (70, 640),
     "The system can explore freely. Selection, appetite, promotion, slicing, and build authorization remain explicit human decisions.",
     font(20), TEXT, 1120)
save_scene(im, 2)

# Scene 3
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
heading(d, "Use case 1 — choose the smallest planning move",
        "Live production MCP call: recommend_planning_workflow")
panel(d, (70, 175, 1210, 325))
d.text((95, 198), "User", font=font(20, True), fill=BLUE)
wrap(d, (95, 235),
     "“I have a rough product idea but I am not sure what planning work I need next. Help me choose the smallest useful move.”",
     font(24), TEXT, 1070)
panel(d, (70, 360, 1210, 575))
d.text((95, 383), "Live MCP response", font=font(20, True), fill=ACCENT)
wrap(d, (95, 430), recommendation, font(23), TEXT, 1065, 1.22)
pill(d, 70, 610, "No forced full workflow")
pill(d, 355, 610, "No human decision invented")
save_scene(im, 3)

# Scene 4
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
heading(d, "Use case 2 — shape a proposed solution without selecting it",
        "Live production MCP call: get_planning_skill → shaping")
panel(d, (70, 175, 1210, 555))
d.text((98, 210), "Canonical Shaping method", font=font(27, True), fill=TEXT)
d.text((98, 270), f"“{shape_rule}”", font=font(31, True), fill=ACCENT)
items = [
    ("Start anywhere useful", "Requirements, a rough solution, evidence, a prototype, or a focused uncertainty."),
    ("Keep states separate", "Working requirement ≠ accepted requirement. Candidate shape ≠ selected shape."),
    ("Use evidence economically", "Fit checks, spikes, sketches, and candidate breadboards only when they resolve uncertainty."),
    ("Stop at the gate", "Shaping may end decision-ready. It does not begin implementation."),
]
y = 340
for h, b in items:
    d.ellipse((100, y + 7, 116, y + 23), fill=ACCENT)
    d.text((130, y), h, font=font(20, True), fill=TEXT)
    wrap(d, (365, y), b, font(18), MUTED, 790, 1.16)
    y += 50
pill(d, 70, 610, "Method comes from the packaged skill, not a rewritten system prompt")
save_scene(im, 4)

# Scene 5
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
heading(d, "Use case 3 — verify readiness before implementation",
        "Live production MCP: orchestration manifest + artifact contracts")
panel(d, (70, 180, 615, 555))
panel(d, (665, 180, 1210, 555))
d.text((98, 215), "Select shape", font=font(26, True), fill=TEXT)
d.text((695, 215), "Build", font=font(26, True), fill=TEXT)
left = ["accepted requirements", "accepted appetite", "decision-ready fit", "explicit human selection"]
right = ["active scope", "context packet", "execution appetite", "human appetite acceptance", "execution contract"]
for base_x, items in [(98, left), (695, right)]:
    y = 285
    for item in items:
        d.rounded_rectangle((base_x, y, base_x + 28, y + 28), radius=7, fill="#153b2a")
        d.text((base_x + 6, y - 3), "✓", font=font(23, True), fill=ACCENT)
        d.text((base_x + 43, y + 1), item, font=font(20), fill=TEXT)
        y += 57
pill(d, 70, 610, "Contracts check structure; they do not replace human judgment.")
save_scene(im, 5)

# Scene 6
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
heading(d, "Production status", "Universal MCP endpoint + packaged skills")
pill(d, 70, 175, "MCP configured")
pill(d, 290, 175, "Domain verified")
pill(d, 515, 175, "No authentication")
d.text((70, 250), f"{len(tool_names)} production MCP tools", font=font(26, True), fill=TEXT)
cols = [tool_names[:4], tool_names[4:]]
for col_index, col in enumerate(cols):
    x = 70 + col_index * 595
    y = 305
    for name in col:
        d.text((x, y), "• " + name, font=font(19), fill=TEXT)
        y += 47
d.text((70, 525), "Production MCP", font=font(19, True), fill=MUTED)
d.text((70, 562), data["endpoint"], font=font(19), fill=BLUE)
wrap(d, (70, 620),
     "Every user connects to the same hosted endpoint. The skills remain the canonical planning-method layer.",
     font(20), TEXT, 1120)
save_scene(im, 6)

narrations = {
    1: "Planning Skills is a public OpenAI plugin that combines fourteen reusable planning skills with a live remote MCP server. The goal is to help humans and agents shape product work without silently inventing scope or making human promotion decisions.",
    2: "The architecture separates method from infrastructure. The planning router is the front door. It chooses the smallest useful next move. Fourteen packaged skills contain the planning methods. The MCP server provides canonical resources, contracts, orchestration rules, and deterministic routing support. Exploration stays fluid while commitment remains gated.",
    3: "First, a fuzzy planning request. This is a live call to the production recommend planning workflow tool. The user asks for the smallest useful move. The server recommends the planning router rather than forcing the entire process. That keeps the system proportional to the uncertainty and avoids inventing downstream commitments.",
    4: "Second, solution shaping. The live server returns the canonical shaping skill. Its governing rule is exploration is fluid, commitment is gated. Users may start from requirements, a rough solution, evidence, or a prototype. Working material stays distinct from accepted material, and the skill stops before implementation unless the required human gates have been crossed.",
    5: "Third, implementation readiness. The orchestration manifest and artifact contracts make promotion gates explicit. Selecting a shape requires accepted requirements, accepted appetite, decision ready fit, and explicit human selection. Building requires active scope, a context packet, execution appetite, human acceptance of that appetite, and an execution contract. Contracts check structure, but do not replace human judgment.",
    6: "The production server is configured, domain verified, and uses no authentication. It exposes seven planning tools from one universal HTTPS endpoint for every user. The skills remain the canonical method layer, while the MCP server makes those methods reliable and inspectable in supported OpenAI hosts.",
}

scene_files = []
for index, narration in narrations.items():
    wav = OUTDIR / f"scene{index}.wav"
    mp4 = OUTDIR / f"scene{index}.mp4"
    subprocess.run([
        "espeak", "-v", "en-us", "-s", "150", "-p", "45", "-w", str(wav), narration
    ], check=True)

    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(wav)
    ], text=True).strip())
    total = duration + 1.0

    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(OUTDIR / f"scene{index}.png"),
        "-i", str(wav),
        "-t", f"{total:.3f}",
        "-vf", "scale=1280:720",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k",
        "-shortest", str(mp4),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    scene_files.append(mp4)

concat = OUTDIR / "concat.txt"
concat.write_text("".join(f"file '{path.name}'\n" for path in scene_files), encoding="utf-8")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
    "-c", "copy", str(VIDEO)
], check=True, cwd=OUTDIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print(VIDEO)
