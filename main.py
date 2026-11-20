#!/usr/bin/env python3
"""news-image-20261120 entry (Python 3.13, standard library only).

The image (news.png, drawn by build_image.py from 20 Nov 2026 reporting) sits
beside this file. The program copies it to /output/entry.png, the one file the
judge reads. It runs with no network, so the copy is the whole job; the bytes
are identical on every run.

Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
