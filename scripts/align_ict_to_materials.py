# -*- coding: utf-8 -*-
"""Normalize ICT_QB refs so every item leads with the matching provided PDF."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "questions.js"

PRIMARY_BY_SECTION: dict[str, str] = {
    "orient": "ECEN106 L1 — Course Orientation v25.26.2 (PDF)",
    "aux": "ECEN106 L2 — Introduction to Building Auxiliary Systems v25.26.2 (PDF)",
    "xmit": "ECEN106 L3 — Transmission Media v25.26.2 (PDF)",
    "cabling": "ECEN 106 L3 — Structured Cabling Standards v25.26.2 (PDF)",
    "bflec": "L6 Building Code and Fire Safety Issues v25.26.2 (PDF)",
    "pd1096": "PD-1096_National-Building-Code_2005 (PDF)",
    "ra9514": "RA-9514_Fire-Code_2019 (PDF)",
    "nfpa72": "NFPA 72 2019 (PDF)",
}

SECONDARY_LECTURE: dict[str, str] = {
    "pd1096": "L6 Building Code and Fire Safety Issues v25.26.2 (PDF)",
    "ra9514": "L6 Building Code and Fire Safety Issues v25.26.2 (PDF)",
    "nfpa72": "L6 Building Code and Fire Safety Issues v25.26.2 (PDF)",
    "orient": "L6 Building Code and Fire Safety Issues v25.26.2 (PDF)",
}

EXTERNAL = re.compile(
    r"chan robles|lawphil|elibrary|supreme court|ansi/tia(?!-)|tia cabling installation|"
    r"adb|world bank|nathanson|glasson|masters|canter|ieee 802|unfccc|undp|http",
    re.I,
)


def _load_bank() -> list[dict]:
    raw = QUESTIONS.read_text(encoding="utf-8")
    m = re.search(r"window\.ICT_QB\s*=\s*(\[.*\])\s*;", raw, re.DOTALL)
    if not m:
        raise SystemExit("Could not parse window.ICT_QB from questions.js")
    return json.loads(m.group(1))


def _normalize_refs(q: dict) -> list[str]:
    sec = q.get("section", "")
    primary = PRIMARY_BY_SECTION.get(sec, PRIMARY_BY_SECTION["orient"])
    lecture2 = SECONDARY_LECTURE.get(sec)
    existing = list(q.get("refs") or [])
    kept: list[str] = []
    for r in existing:
        rs = r.strip()
        if not rs or rs == primary or (lecture2 and rs == lecture2):
            continue
        if re.search(r"ECEN106|ECEN 106|L6 Building|PD-1096|RA-9514|NFPA 72", rs, re.I):
            if primary.lower() not in rs.lower():
                kept.append(rs)
            continue
        if EXTERNAL.search(rs):
            kept.append(rs + " (optional cross-check)")
        else:
            kept.append(rs)
    out = [primary]
    if lecture2 and lecture2 != primary:
        out.append(lecture2)
    return out + kept


def main() -> None:
    bank = _load_bank()
    for q in bank:
        q["refs"] = _normalize_refs(q)
    header = (
        "// Auto-generated bank — ICT/ECEN 106 examiner\n"
        "// Keyed answers grounded in provided lecture/statute PDFs (see MATERIALS.md).\n"
    )
    js = header + "window.ICT_QB=" + json.dumps(bank, ensure_ascii=False, indent=2) + ";\n"
    QUESTIONS.write_text(js, encoding="utf-8")
    print("aligned", len(bank), "questions ->", QUESTIONS)


if __name__ == "__main__":
    main()
