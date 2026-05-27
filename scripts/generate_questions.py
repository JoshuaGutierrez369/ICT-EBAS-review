# -*- coding: utf-8 -*-
"""Generate ICT/ECEN 106 examiner bank: 2000 MCQs (250 x 8 topics; 5× the original 50/topic).
Each stem is unique: 15 substantive cores × 18 scenario frames per section (270 combinations; use 250)."""
from __future__ import annotations

import json
from pathlib import Path
import importlib.util

from bank_config import TOTAL_EXPECTED_MCQS, TOPIC_QUESTION_TARGET
from ict_expansion import tuples_for_section

SEC = {
    "orient": "L1 — Course Orientation (ECEN 106)",
    "aux": "L2 — Introduction to Building Auxiliary Systems",
    "xmit": "L3 — Transmission Media",
    "cabling": "L3 — Structured Cabling Standards (TIA/EIA)",
    "bflec": "L6 — Building Code & Fire Safety Issues",
    "pd1096": "PD 1096 — National Building Code highlights",
    "ra9514": "RA 9514 — Fire Code highlights",
    "nfpa72": "NFPA 72 — Alarm & signalling concepts",
}

LVL = ["Analysis", "Analysis", "Analysis", "Analysis", "Analysis", "Analysis", "Analysis", "Analysis"]

SECTION_ORDER = ("orient", "aux", "xmit", "cabling", "bflec", "pd1096", "ra9514", "nfpa72")


def pack(section: str, n: int, stem: str, opts: tuple[str, str, str, str], ans_idx: int, expl: str, refs: list[str]) -> dict:
    letters = ["a", "b", "c", "d"]
    return {
        "id": f"{section}-{n:03d}",
        "section": section,
        "secTitle": SEC[section],
        "level": LVL[n % len(LVL)],
        "type": "mcq",
        "text": stem,
        "choices": [{"ltr": letters[i], "text": opts[i]} for i in range(4)],
        "ans": letters[ans_idx],
        "expl": expl,
        "refs": refs,
    }


def build_section(section: str) -> list[dict]:
    tuples_list = tuples_for_section(section, TOPIC_QUESTION_TARGET)
    return [pack(section, i + 1, *tup) for i, tup in enumerate(tuples_list)]


def main() -> None:
    BANK: list[dict] = []
    for sec in SECTION_ORDER:
        BANK.extend(build_section(sec))

    assert len(BANK) == TOTAL_EXPECTED_MCQS, len(BANK)

    _spec = importlib.util.spec_from_file_location(
        "revise_bank_hard", Path(__file__).resolve().parent / "revise_bank_hard.py"
    )
    _mod = importlib.util.module_from_spec(_spec)
    assert _spec.loader is not None
    _spec.loader.exec_module(_mod)
    _mod.apply_hard_mode(BANK)

    texts = [q["text"].strip().lower() for q in BANK]
    if len(texts) != len(set(texts)):
        from collections import Counter

        dup = [t for t, c in Counter(texts).items() if c > 1]
        raise ValueError(f"Duplicate stems after revise step ({len(texts)-len(set(texts))} dupes), e.g.: {dup[:3]!r}")

    js = "// Auto-generated bank — ICT/ECEN 106 examiner (hard analytical revision)\n"
    js += "window.ICT_QB=" + json.dumps(BANK, ensure_ascii=False, indent=2) + ";\n"
    outp = Path(__file__).resolve().parent.parent / "questions.js"
    outp.write_text(js, encoding="utf-8")
    print("wrote", outp, len(BANK), "unique stems:", len(set(texts)))


if __name__ == "__main__":
    main()
