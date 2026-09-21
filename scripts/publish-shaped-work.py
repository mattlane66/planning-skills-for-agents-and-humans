#!/usr/bin/env python3
"""Stable command entry point for Planning Publisher."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("publish_shaped_work.py")), run_name="__main__")
