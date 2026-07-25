#!/usr/bin/env python3
"""CLI entry: python run.py [--skip-download] [--force-download]"""

from tool.pipeline import main

if __name__ == "__main__":
    raise SystemExit(main())
