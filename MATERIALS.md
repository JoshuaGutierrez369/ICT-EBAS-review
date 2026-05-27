# Study materials (answer key source)

All **keyed answers** in this reviewer are written to match the **PDF pack you provided** for ECEN 106 — not generic web summaries alone.

## Required PDFs (Downloads folder)

| File | App topic (`section`) |
|------|------------------------|
| `ECEN106 L1 -Course Orientation v25.26.2.pdf` | orient |
| `ECEN106 L2 - Introduction to Building Auxiliary Systems v25.26.2.pdf` | aux |
| `ECEN106 L3 - Transmission Media v25.26.2.pdf` | xmit |
| `ECEN 106 L3 - Structured Cabling Standards v25.26.2.pdf` | cabling |
| `L6 Building Code and Fire Safety Issues v25.26.2.pdf` | bflec (+ cross-topic) |
| `PD-1096_National-Building-Code_2005_2025-01-09.pdf` | pd1096 |
| `RA-9514_Fire-Code_2019_2025-01-09.pdf` | ra9514 |
| `NFPA 72 2019.pdf` | nfpa72 |

## How questions cite sources

- Each item’s `refs` array **starts with** the matching PDF above.
- L6 slides cross-reference NBC/FC/NFPA where the course integrates them.
- External links (Chan Robles, etc.) appear only as **“(optional cross-check)”** when retained.

## Rebuild & audit

```bash
python scripts/extract_ict_materials.py
python scripts/generate_questions.py
python scripts/align_ict_to_materials.py
python scripts/audit_ict_materials.py
```

`scripts/materials_corpus.txt` is the searchable extract (~4.6 MB) used for automated grounding checks.
