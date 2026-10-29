#!/usr/bin/env python3
"""Compatibility entry point for the current public example collector.

Explicit --weather-csv and --arabidopsis-root inputs are now required.
See docs/application-examples.md for the retrieval commands.
"""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('refresh-site-examples.py')), run_name='__main__')
