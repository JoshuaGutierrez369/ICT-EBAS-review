# -*- coding: utf-8 -*-
"""Fail if questions.js contains duplicate stems."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
raw = (ROOT / "questions.js").read_text(encoding="utf-8")
bank = json.loads(raw.split("window.ICT_QB=", 1)[1].strip().rstrip(";"))
texts = [q["text"].strip().lower() for q in bank]
c = Counter(texts)
dupes = [(t, n) for t, n in c.items() if n > 1]
print(f"{len(bank)} items, {len(set(texts))} unique stems, {len(dupes)} duplicate groups")
if dupes:
    raise SystemExit(f"Worst: {dupes[0][1]}x {dupes[0][0][:80]!r}")
