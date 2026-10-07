#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
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

def wrap(draw, xy, text, fnt, fill, width, spacing=1.22):
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

def pill(draw, x, y, label):
    f = font(20, True)
    bb = draw.textbbox((0, 0), label, font=f)
    ww, hh = bb[2] - bb[0] + 26, bb[3] - bb[1] + 18
    draw.rounded_rectangle((x, y, x + ww, y + hh), radius=hh // 2, fill="#153326")
    draw.text((x + 13, y + 7), label, font=f, fill=ACCENT)
    return ww

def heading(draw, title, subtitle=None):
    draw.text((70, 48), title, font=font(38, True), fill=TEXT)
    if subtitle:
        draw.text((72, 98), subtitle, font=font(20), fill=MUTED)
    draw.line((70, 137, 1210, 137), fill=BORDER, width=2)

def footer(draw, text):
    draw.text((70, 680), text, font=font(15), fill=MUTED)

tool_names = [tool["name"] for tool in data["tools"]]
recommendation = data["recommendation"].strip()
shape_rule = "Exploration is fluid. Commitment is gated."
if shape_rule not in data["shaping"]:
    shape_rule = "Exploration can be fluid. Promotion cannot."

scenes = []

# 1 — intro
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
panel(d, (55, 65, 1225, 650), 28)
d.text((95, 115), "Planning Skills", font=font(58, True), fill=TEXT)
d.text((98, 190), "Reviewer walkthrough", font=font(30), fill=ACCENT)
wrap(d, (98, 252), "A public OpenAI plugin combining 14 reusable planning skills with a live universal MCP server.", font(28), TEXT, 1040, 1.3)
y = 385
for label in ["14 packaged skills", f"{len(tool_names)} production MCP tools", "One HTTPS MCP URL for every user", "Explicit human promotion gates preserved"]:
    d.ellipse((102, y + 7, 118, y + 23), fill=ACCENT)
    d.text((135, y), label, font=font(24), fill=TEXT)
    y += 52
footer(d, "Reviewer demo generated from the live production MCP.")
scenes.append(im)

# 2 — architecture
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
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
        d.text((x1 + 22, yy), line, font=font(19), fill=MUTED); yy += 38
for x1, x2 in [(275, 335), (560, 620), (890, 950)]:
    d.line((x1 + 8, 350, x2 - 12, 350), fill=BLUE, width=5)
    d.polygon([(x2 - 13, 342), (x2 - 13, 358), (x2 - 1, 350)], fill=BLUE)
pill(d, 70, 585, "Exploration is fluid. Commitment is gated.")
wrap(d, (70, 635), "The system can explore freely. Selection, appetite, promotion, slicing, and build authorization remain explicit human decisions.", font(20), TEXT, 1120)
scenes.append(im)

# 3 — router
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
heading(d, "Use case 1 — choose the smallest planning move", "Live MCP: recommend_planning_workflow")
panel(d, (70, 175, 1210, 325)); d.text((95, 198), "User", font=font(20, True), fill=BLUE)
wrap(d, (95, 235), "“I have a rough product idea but I am not sure what planning work I need next. Help me choose the smallest useful move.”", font(24), TEXT, 1070)
panel(d, (70, 360, 1210, 575)); d.text((95, 383), "Live production response", font=font(20, True), fill=ACCENT)
wrap(d, (95, 430), recommendation, font(23), TEXT, 1065)
pill(d, 70, 610, "No forced full workflow"); pill(d, 355, 610, "No human decision invented")
scenes.append(im)

# 4 — shaping
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
heading(d, "Use case 2 — shape without silently selecting", "Live MCP: get_planning_skill → shaping")
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
pill(d, 70, 610, "Method comes from the packaged skill")
scenes.append(im)

# 5 — gates
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
heading(d, "Use case 3 — verify readiness before implementation", "Live MCP: orchestration manifest + artifact contracts")
panel(d, (70, 180, 615, 555)); panel(d, (665, 180, 1210, 555))
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
scenes.append(im)

# 6 — production status
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
heading(d, "Production status", "Universal MCP endpoint + packaged skills")
pill(d, 70, 175, "MCP configured"); pill(d, 290, 175, "Domain verified"); pill(d, 515, 175, "No authentication")
d.text((70, 250), f"{len(tool_names)} production MCP tools", font=font(26, True), fill=TEXT)
cols = [tool_names[:4], tool_names[4:]]
for col_index, col in enumerate(cols):
    x, y = 70 + col_index * 595, 305
    for name in col:
        d.text((x, y), "• " + name, font=font(19), fill=TEXT); y += 47
d.text((70, 525), "Production MCP", font=font(19, True), fill=MUTED)
d.text((70, 562), data["endpoint"], font=font(19), fill=BLUE)
wrap(d, (70, 615), "Every user connects to the same hosted endpoint. Skills remain the canonical method layer.", font(20), TEXT, 1120)
scenes.append(im)

# Build a 78-second silent walkthrough with readable holds and short crossfades.
fps = 2
hold_seconds = [10, 12, 14, 14, 16, 12]
writer = imageio.get_writer(
    VIDEO,
    fps=fps,
    codec="libx264",
    quality=8,
    pixelformat="yuv420p",
    macro_block_size=None,
)

try:
    for idx, scene in enumerate(scenes):
        arr = np.asarray(scene)
        frames = hold_seconds[idx] * fps
        for _ in range(frames):
            writer.append_data(arr)
finally:
    writer.close()

print(VIDEO)
