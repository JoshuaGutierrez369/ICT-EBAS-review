# ECEN 106 — ICT & Building Auxiliary Systems — Reviewer / Quiz Bee

Standalone **GitHub Pages** app (same interaction pattern as the CA3 Communications & ENVS reviewers):

- Overlay landing → **Reviewer** (answers + expandable rationale/refs) / **Quiz Bee** (pick topic decks, shuffle, timer) / **Key concepts** cheatsheet  
- **`questions.js`** — **2000 MCQs** = **250 × 8 topics** (5× the original 50/topic; `scripts/generate_questions.py` rebuilds this file, then automatically runs `scripts/revise_bank_hard.py` to upgrade stems, parallel distractors, and long-form rationales). The quiz “# Questions” input **sets `max` from the loaded bank** so it always matches `window.ICT_QB.length`.
- **PWA-lite:** `manifest.json` + `sw.js` (+ `.nojekyll`).

### Deploy URL

**Repository:** https://github.com/JoshuaGutierrez369/ICT-EBAS-review  

After Pages is enabled on `main` (root):

**→ https://joshuagutierrez369.github.io/ICT-EBAS-review/**

### Rebuild question bank

Per-topic size is controlled in `scripts/bank_config.py` (`BASE_PER_TOPIC` × `MULTIPLIER`; currently **50 × 5 = 250** per deck, **2000** total).

```bash
python scripts/generate_questions.py
```

### Offline PDF materials (your machine)

Keyed answers follow the PDFs listed in [`MATERIALS.md`](./MATERIALS.md). Reference filenames from the course pack (path may vary):

- ECEN106 L1 — Course Orientation  
- ECEN106 L2 — Introduction to Building Auxiliary Systems  
- ECEN106 L3 — Structured Cabling Standards  
- ECEN106 L3 — Transmission Media  
- L6 — Building Code and Fire Safety Issues  
- PD 1096 — National Building Code  
- RA 9514 — Fire Code  
- NFPA 72 (2019)
