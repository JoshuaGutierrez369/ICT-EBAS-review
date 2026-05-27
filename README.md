# ECEN 106 — ICT & Building Auxiliary Systems — Reviewer / Quiz Bee

Standalone **GitHub Pages** app (same interaction pattern as the CA3 Communications & ENVS reviewers):

- Overlay landing → **Reviewer** (answers + expandable rationale/refs) / **Quiz Bee** (pick topic decks, shuffle, timer) / **Key concepts** cheatsheet  
- **`questions.js`** — **400 MCQs** = **50 × 8 topics** (`scripts/generate_questions.py` rebuilds this file).  
- **PWA-lite:** `manifest.json` + `sw.js` (+ `.nojekyll`).

### Deploy URL

**Repository:** https://github.com/JoshuaGutierrez369/ICT-EBAS-review  

After Pages is enabled on `main` (root):

**→ https://joshuagutierrez369.github.io/ICT-EBAS-review/**

### Rebuild question bank

```bash
python scripts/generate_questions.py
```

### Offline PDF materials (your machine)

Reference filenames from the course pack (path may vary):

- ECEN106 L1 — Course Orientation  
- ECEN106 L2 — Introduction to Building Auxiliary Systems  
- ECEN106 L3 — Structured Cabling Standards  
- ECEN106 L3 — Transmission Media  
- L6 — Building Code and Fire Safety Issues  
- PD 1096 — National Building Code  
- RA 9514 — Fire Code  
- NFPA 72 (2019)
