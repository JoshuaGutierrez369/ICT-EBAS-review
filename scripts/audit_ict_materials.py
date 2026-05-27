# -*- coding: utf-8 -*-
"""Audit ICT_QB: correct answers should be supportable from provided PDF corpus."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "questions.js"
CORPUS = Path(__file__).resolve().parent / "materials_corpus.txt"
REPORT = Path(__file__).resolve().parent / "audit_report.txt"

SECTION_TO_CORPUS: dict[str, list[str]] = {
    "orient": ["L1 orient"],
    "aux": ["L2 aux"],
    "xmit": ["L3 xmit"],
    "cabling": ["L3 cabling"],
    "bflec": ["L6 bflec"],
    "pd1096": ["PD 1096", "L6 bflec"],
    "ra9514": ["RA 9514", "L6 bflec"],
    "nfpa72": ["NFPA 72", "L6 bflec"],
}

LECTURE_SECTIONS: dict[str, str] = {}


def _norm(s: str) -> str:
    s = s.lower()
    for a, b in (("₂", "2"), ("₃", "3"), ("°", " "), ("–", "-"), ("—", "-"), ("·", " ")):
        s = s.replace(a, b)
    s = re.sub(r"[^\w\s.%-]", " ", s)
    return re.sub(r"\s+", " ", s)


def load_corpus() -> None:
    raw = CORPUS.read_text(encoding="utf-8")
    parts = re.split(r"={60}\n([^=]+)\n={60}", raw)
    for i in range(1, len(parts), 2):
        label = parts[i].strip().split("—")[0].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        LECTURE_SECTIONS[label] = _norm(body)


def load_bank() -> list[dict]:
    raw = QUESTIONS.read_text(encoding="utf-8")
    m = re.search(r"window\.ICT_QB\s*=\s*(\[.*\])\s*;", raw, re.DOTALL)
    return json.loads(m.group(1)) if m else []


def keywords(text: str) -> list[str]:
    text = _norm(text)
    out: list[str] = []
    for num in re.findall(r"\d+(?:\.\d+)?", text):
        if len(num) >= 2:
            out.append(num)
    words = re.findall(r"[a-z0-9]{3,}", text)
    bigrams = [words[i] + " " + words[i + 1] for i in range(min(len(words) - 1, 6))]
    return list(dict.fromkeys(out + words[:12] + bigrams[:6]))


def correct_text(q: dict) -> str:
    ans = q.get("ans", "")
    for c in q.get("choices") or []:
        if c.get("ltr") == ans:
            return c.get("text", "")
    return ""


def grounded(q: dict) -> tuple[bool, str]:
    labels = SECTION_TO_CORPUS.get(q.get("section", ""), [])
    corpuses = " ".join(LECTURE_SECTIONS.get(l, "") for l in labels)
    if not corpuses.strip():
        return False, f"no corpus for {labels}"
    kws = keywords(correct_text(q) or q.get("text", ""))
    if not kws:
        return False, "no keywords"
    hits = [k for k in kws if k in corpuses]
    need = max(1, min(3, len(kws) // 4))
    if len(hits) >= need:
        return True, f"{len(hits)}/{len(kws)} in {labels}"
    return False, f"{len(hits)}/{len(kws)}; missed {kws[0]!r}"


def has_primary_ref(q: dict) -> bool:
    refs = " ".join(q.get("refs") or [])
    return bool(re.search(r"ECEN106|ECEN 106|L6 Building|PD-1096|RA-9514|NFPA 72", refs, re.I))


def main() -> None:
    if not CORPUS.exists():
        raise SystemExit("Run extract_ict_materials.py first")
    load_corpus()
    bank = load_bank()
    lines = [f"Audited {len(bank)} ICT questions\n"]
    no_ref = [q["id"] for q in bank if not has_primary_ref(q)]
    lines.append(f"Missing primary PDF ref: {len(no_ref)}\n")
    if no_ref[:20]:
        lines.append("  " + ", ".join(no_ref[:20]) + ("..." if len(no_ref) > 20 else "") + "\n")
    bad = []
    for q in bank:
        ok, msg = grounded(q)
        if not ok:
            bad.append((q, msg))
    lines.append(f"Corpus grounding failures: {len(bad)}\n")
    for q, msg in bad[:40]:
        lines.append(f"  {q['id']} [{q['section']}]: {msg}\n")
        lines.append(f"    Q: {q.get('text','')[:90]}\n")
        lines.append(f"    A: {correct_text(q)[:70]}\n")
    REPORT.write_text("".join(lines), encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
