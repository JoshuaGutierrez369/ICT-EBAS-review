# -*- coding: utf-8 -*-
"""Extract ICT/ECEN 106 course PDFs into materials_corpus.txt."""
from __future__ import annotations

from pathlib import Path

import pypdf

DOWNLOADS = Path(r"C:\Users\joshu\Downloads")
OUT = Path(__file__).resolve().parent / "materials_corpus.txt"

PDFS: list[tuple[str, Path]] = [
    ("L1 orient", DOWNLOADS / "ECEN106 L1 -Course Orientation v25.26.2.pdf"),
    ("L2 aux", DOWNLOADS / "ECEN106 L2 - Introduction to Building Auxiliary Systems v25.26.2.pdf"),
    ("L3 xmit", DOWNLOADS / "ECEN106 L3 - Transmission Media v25.26.2.pdf"),
    ("L3 cabling", DOWNLOADS / "ECEN 106 L3 - Structured Cabling Standards v25.26.2.pdf"),
    ("L6 bflec", DOWNLOADS / "L6 Building Code and Fire Safety Issues v25.26.2.pdf"),
    ("PD 1096", DOWNLOADS / "PD-1096_National-Building-Code_2005_2025-01-09.pdf"),
    ("RA 9514", DOWNLOADS / "RA-9514_Fire-Code_2019_2025-01-09.pdf"),
    ("NFPA 72", DOWNLOADS / "NFPA 72 2019.pdf"),
]


def main() -> None:
    parts: list[str] = []
    for label, path in PDFS:
        if not path.exists():
            parts.append(f"\n\n{'=' * 60}\nMISSING: {label} — {path}\n{'=' * 60}\n")
            continue
        r = pypdf.PdfReader(str(path))
        text = "\n".join((p.extract_text() or "") for p in r.pages)
        parts.append(f"\n\n{'=' * 60}\n{label} — {path.name}\n{'=' * 60}\n{text}")
    OUT.write_text("".join(parts), encoding="utf-8")
    print("wrote", OUT, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
