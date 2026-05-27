# -*- coding: utf-8 -*-
"""
Post-process ICT_QB: analytical level, stronger parallel distractors, expanded rationales.
Run after generate_questions.py or directly: python scripts/revise_bank_hard.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "questions.js"

try:
    from bank_config import TOTAL_EXPECTED_MCQS as _EXPECTED
except ImportError:
    _EXPECTED = None

# Exact replacement for wrong-only choice strings (verified no overlap as correct elsewhere)
CHOICE_REP: dict[str, str] = {
    # Orientation / commissioning padding
    "Unrelated acoustics RT60": "Assume corridor speech intelligibility (RT60) alone proves egress notification compliance",
    "Remove engineering": "Rely solely on AHJ anecdotal approvals without sealed engineering submissions",
    "Panel labels": "Treat FACP nomenclature as decorative—skip synchronized notification appliance zoning maps",
    "Only paint schedule": "Use interior finish milestones as the acceptance gate for suppressed notification circuits",
    "Only RJ45 jacks": "Specify IT-style modular jacks as the engineered medium for supervised NAC without Class A/B design",
    "No supervision": "Omit pathway supervision because voice messaging shares the VLAN with office traffic",
    "No enforcement ever": "Assume IRR penalties are illustrative and never applied in practice",
    "No UL listings": "Approve field-built appliances without Listed equipment constraints",
    "Menu pricing": "Benchmark life-safety cost using cafeteria price lists instead of prescriptive SPL coverage tests",
    "Guaranteed subsidy": "Expect LGU subsidy to negate redesign when STI maps fail occupant-notification codes",
    "Guarantee free materials": "Believe gratis vendor samples satisfy battery standby amp-hour calculations",
    "Free donuts": "Substitute stakeholder snacks for calibrated audibility surveys",
    "Delete liability": "Shift all post-occupancy FA liability to cabling subcontractors via oral side letters",
    "Code existence": "Claim mere adoption of PD 1096 text automatically voids TIA separation rules",
    "All solar output": "Blame nuisance trips on PV export without evaluating equipotential bonding continuity",
    "Nothing": "Assert inspection failures create zero schedule or cost exposure if drawings are stamped IFC",
    "No permits": "Proceed with above-ceiling pulls using only manufacturer cut-sheets as authority",
    "No peer review": "Skip third-party review because low-voltage scope is ‘non-structural’",
    "No measurements": "Accept alarm audibility by ear during walk-through without sound-level documentation",
    "No cable IDs": "Rely on patch cord color memory instead of cable schedule / CMDB linkage",
    "Lunch menus": "Use break schedules to infer occupant load factors for exit width checks",
    "Email chain only": "Treat uncollated email threads as the legal record of firestop shop drawings",
    "All gold plating luxuries blindly": "Reject any cost-neutral passive fire rating upgrade as unnecessary scope creep",
    "Only weekend BBQ": "Discount rework impact as limited to non-billable weekend social events",
    "Only photo of panel": "Submit a single cabinet photo in lieu of loop resistance and ground-fault logs",
    "Only cloud credits": "Offset field deficiency costs using unrelated SaaS subscription credits",
    "Unrelated spreadsheets": "Maintain inventory in finance-only workbooks decoupled from labeling IDs",
    "They only apply to ships": "Argue NBC fire-resistance language applies solely to vessels, not land-based telecom risers",
    "Oral approvals only": "Replace signed submittals with verbal sign-offs that cannot be audited",
    "Deleting as-built packs": "Withhold turnover geometry so future MAC crews guess penetration firestop restores",
    "Hiding deviations from inspectors": "Conceal as-built deltas to expedite provisional occupancy",
    "Random cable colors": "Avoid TIA606 color conventions to ‘simplify’ installation",
    "Avoiding labeling": "Defer labeling until after abandonment to save commissioning hours",
    "Eliminating FAT/SAT notions": "Skip factory/site acceptance citing schedule compression",
    "Only conceptual bubbles": "Deliver single-line fantasies instead of conduit fill and bend-radius details",
    "No cable lengths": "Omit attenuation budgeting because testers ‘will figure it out’",
    "Password lists only": "Misclassify cybersecurity exports as FA shop drawings turnover",
    "They ban all fiber optics": "Misread egress glazing rules as outlawing optical backbone pathways",
    "They replace TIA‑568 outright": "Assume localized NBC clauses supersede cabling performance categories without IRR crosswalk",
    "To increase EMI": "Advise co-routing HV feeders with shields removed to lower tray cost",
    "To delete bonding everywhere": "Remove TGB references to shorten grounding riser diagrams",
    "Only wallpaper": "Treat shaft wall ratings as décor-only when routing FA riser cables",
    "Only landscape": "Assume exterior planter routing exempts sprinkler coverage reviews",
    "All terminators removed": "Leave coax taps unterminated to ‘test hot’ continuously",
    "No testing": "Skip sweep tests because LEDs appear solid on handheld meters",
    "Transformer kVA alone": "Size notification appliance transformers only on HVAC kVA diversity",
    "Only weather": "Blame outdoor temperature only for fiber loss without bend-radius inspection",
    "Only paint": "Attribute STI failure to paint vendor instead of annunciator voltage drop",
    "HVAC zoning only": "Use comfort zoning maps as proxy for occupant notification partition boundaries",
    "Ethernet auto-negotiation brand": "Assume switch LLDP vendor ID satisfies audibility coverage math",
    "Aesthetics only": "Select strobe candela solely on lens color matching ceiling tiles",
    "Delete sprinklers blindly": "Remove heads to improve tray access without hydraulic recalculation",
    "Remove exits": "Convert rated corridors to open plan for cable tray maintenance",
    "Formalize scrutiny of drawings & inspections—not encourage clandestine builds": "Treat barangay clearances alone as NBC-equivalent scrutiny of stamped structural and fire envelopes",
    "Closure orders/fees calibrated by IRR schedules—education dependent": "Assume closure orders escalate only after informal education—not per published IRR tariff tables",
}


def stem_refine(q: dict) -> None:
    """Legacy placeholder cleanup only.

    Modern banks from ict_expansion.py already embed unique scenario frames per stem.
    Do NOT prepend a single section-wide prefix — that collapsed hundreds of items into clones.
    """
    tx = q.get("text", "")
    low = tx.lower().strip()
    if "placeholder" in low or "quiz variant" in low or low.startswith("l2 auxiliary concept"):
        core = tx.split(": ", 1)[-1] if ": " in tx else tx
        q["text"] = core.strip()
        if not q["text"].endswith("?"):
            q["text"] = q["text"].rstrip(".") + "?"


def deepen_expl(q: dict) -> None:
    ans = q.get("ans", "")
    parts = [q.get("expl", "").strip()]
    corr = next((c["text"] for c in q["choices"] if c["ltr"] == ans), "")
    parts.append(
        f"Best-supported choice ({ans}): aligns with {corr[:180]}{'…' if len(corr) > 180 else ''} given code + standards crosswalk in SOURCES.md."
    )
    trap: list[str] = []
    for c in q["choices"]:
        if c["ltr"] == ans:
            continue
        t = c["text"]
        if "misread" in t.lower() or "assume" in t.lower() or "treat" in t.lower():
            trap.append(f"({c['ltr']}) tempts a narrow misread: {t[:140]}{'…' if len(t) > 140 else ''}")
        else:
            trap.append(f"({c['ltr']}) conflicts with separation, supervision, or documentation rigor: {t[:120]}{'…' if len(t) > 120 else ''}")
    parts.append("Why others falter: " + " ".join(trap))
    q["expl"] = " ".join(p for p in parts if p)


def apply_hard_mode(bank: list[dict]) -> None:
    for q in bank:
        q["level"] = "Analysis"
        for ch in q["choices"]:
            old = ch["text"]
            if old in CHOICE_REP:
                ch["text"] = CHOICE_REP[old]
        stem_refine(q)
        deepen_expl(q)
        # de-duplicate identical choice texts within one item
        seen: set[str] = set()
        for ch in q["choices"]:
            base = ch["text"]
            if base in seen:
                ch["text"] = base + " (alternate framing)"
            seen.add(ch["text"])


def load_bank() -> list[dict]:
    raw = QUESTIONS.read_text(encoding="utf-8")
    payload = raw.split("window.ICT_QB=", 1)[1].strip().rstrip(";").strip()
    return json.loads(payload)


def save_bank(bank: list[dict]) -> None:
    js = "// Auto-generated bank — ICT/ECEN 106 examiner (hard analytical revision)\n"
    js += "window.ICT_QB=" + json.dumps(bank, ensure_ascii=False, indent=2) + ";\n"
    QUESTIONS.write_text(js, encoding="utf-8")


def main() -> None:
    bank = load_bank()
    if _EXPECTED is not None:
        assert len(bank) == _EXPECTED, len(bank)
    apply_hard_mode(bank)
    texts = [q["text"].strip().lower() for q in bank]
    if len(texts) != len(set(texts)):
        from collections import Counter

        dup = [t for t, c in Counter(texts).items() if c > 1]
        raise ValueError(f"Duplicate stems after revise ({len(texts) - len(set(texts))}), e.g. {dup[0][:100]!r}")
    save_bank(bank)
    print("Rewrote", QUESTIONS, "unique stems:", len(set(texts)))


if __name__ == "__main__":
    main()
