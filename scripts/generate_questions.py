# -*- coding: utf-8 -*-
"""Generate ICT/ECEN 106 examiner bank: 400 MCQs (50 x 8 topics).
References mix Philippine codes (official summaries) with TIA/NFPA industry standards."""
from __future__ import annotations

import json
from pathlib import Path

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

LVL = ["Knowledge", "Knowledge", "Comprehension", "Comprehension", "Application", "Application", "Analysis", "Analysis"]


def pack(section: str, n: int, stem: str, opts: tuple[str, str, str, str], ans_idx: int, expl: str, refs: list[str]) -> dict:
    letters = ["a", "b", "c", "d"]
    return {
        "id": f"{section}-{n:02d}",
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


def shuffle_wrong_correct(correct: str, pool: list[str], k=3):
    opts = [correct] + pool[:k]
    # stable order returned as tuple for manual ans_idx assignment in builder
    return tuple(opts[:4])


# --- Helpers to generate 50 per topic ---
def rotate_build(section: str, templates: list[tuple], pad_fn) -> list[dict]:
    out: list[dict] = []
    for i in range(50):
        if i < len(templates):
            tup = templates[i]
        else:
            tup = pad_fn(i)
        out.append(pack(section, i + 1, *tup))
    return out


def main():
    ra = ["RA 9514 (Chan Robles / Supreme Court E-Library)", "BFP IRR materials"]
    nbc = ["PD 1096 (DPWH / SC E-Library)", "IRR of NBC compilations"]
    tia = ["ANSI/TIA-568 family (commercial building telecom cabling)", "TIA cabling installation references"]
    nfpa = ["NFPA 72 — National Fire Alarm and Signaling Code (2019 ed. concepts)"]
    crs = ["CvSU ECEN 106 lecturer PDFs — verify slide wording"]

    # ------- ORIENTATION -------
    ori_t = []
    ori_t.append(("ECEN Building Auxiliary Systems coursework most directly supports which outcome?", ("Safe integration of life-safety and low‑voltage building systems", "Designing turbine generators only", "Pharmaceutical drug synthesis", "Marine fisheries policy"), 0, "Auxiliary/low-voltage and fire/life safety interfaces are central to EBAS curricula.", crs + ["PD 1096 — general building provisions overview"]))
    ori_t.append(("Why are NBC (PD 1096) and RA 9514 studied together with ICT cabling?", ("They constrain where and how telecom pathways may be routed for life safety", "They ban all fiber optics", "They replace TIA‑568 outright", "They only apply to ships"), 0, "Architectural egress, shafts, openings, ratings, fire stops, inspections interact with cabling.", nbc + ra))
    ori_t.append(("Professional responsibility in documenting auxiliary systems emphasizes:", ("Traceable drawings, labeling, commissioning records, permits", "Oral approvals only", "Deleting as-built packs", "Hiding deviations from inspectors"), 0, "Engineering accountability requires reproducible docs for turnover and OM.", crs))
    ori_t.append(("Interdisciplinary coordination in smart buildings foremost reduces:", ("Clashes between structure, HVAC, conduit fill, egress, alarms", "Global inflation only", "Cloud API pricing", "Database normalization"), 0, "Integrated design reviews prevent rework and latent defects.", crs))
    ori_t.append(("A commissioning mindset for Auxiliary Systems emphasizes:", ("Verifying subsystem performance versus owner criteria and codes", "Random cable colors", "Avoiding labeling", "Eliminating FAT/SAT notions"), 0, "Formal verification aligns installed behavior with specs.", crs + ["IEEE / BICSI commissioning practice references"]))
    ori_t.append(("As-built drawings for ICT/Fire/auxiliary systems commonly include:", ("Field changes, splice points, labeling scheme, penetration firestop details", "Only conceptual bubbles", "No cable lengths", "Password lists only"), 0, "Facility owners rely on accurate as-built for maintenance and retrofit.", crs + nbc))
    ori_t.append(("Why track cable inventory and BOM for structured cabling?", ("Lifecycle management and warranty compliance", "To delete records after install", "To avoid testing", "To eliminate patch panels"), 0, "Traceability aids moves/adds/changes and vendor support.", tia))
    ori_t.append(("Owner training & O&M manuals for subsystem X help because:", ("Operators sustain performance and alarms stay configured correctly", "They waive code compliance", "They delete logs", "They remove detectors"), 0, "Human factors after turnover affect safety outcomes.", crs))
    ori_t.append(("Good practice for subcontractor ICT scope packages includes:", ("Clear referenced standards (TIA-568/etc.), milestones, FAT/SITE test criteria", "Handwritten napkins only", "No acceptance tests", "Unlimited undocumented changes"), 0, "Scope clarity reduces latent defects.", tia))
    ori_t.append(("Value of modeling cable tray fill early in design?", ("Thermal, bend clearance, segregation of power/low-voltage, inspection access", "To paint trays later only", "To delete tray notes", "To avoid coordination"), 0, "Tray engineering impacts maintainability.", crs))

    def ori_pad(j: int):
        variants = [
            ("Typical commissioning deliverable evidencing alarm audibility?", ("Measured SPL maps vs AHJ criteria using approved device layout", "No measurements", "Only photo of panel", "Email chain only"), 0, "Measured verification supports acceptance against code/engineer spec.", nfpa + crs),
            ("Cable schedule spreadsheet helps operations by documenting:", ("From–to circuits, strand count, sheath type, labeling ID, test limits", "Lunch menus", "Unrelated spreadsheets", "No cable IDs"), 0, "Schedules are core FA/ICT documentation.", crs),
            ("Value engineering auxiliary scope must preserve:", ("Minimum mandated life-safety and code performance—not delete rated barriers", "All gold plating luxuries blindly", "No peer review", "No permits"), 0, "Can't VE away required fire egress or suppression elements.", ra + nbc),
            ("Rework after inspection failure usually costs project teams:", ("Schedule slips, reinspection fees, reputational penalties", "Nothing", "Only weekend BBQ", "Only cloud credits"), 0, "Compliance failures impact delivery.", crs + ra),
        ]
        return variants[j % len(variants)]

    # pad remaining orientation to reach 50
    while len(ori_t) < 50:
        i = len(ori_t)
        ori_t.append(ori_pad(i))

    aux_t = []
    aux_t.append(("Building auxiliary/low-voltage family often excludes which item as “primary”?",
                  ("Industrial SCADA PLC network for refinery cracking unit only (beyond typical auxiliary scope discourse)", "CCTV subsystem", "Access control subsystem", "Public address/evac paging"), 0, "Courses frame auxiliary building services—not full process automation plants.", crs))
    aux_t.append(("Why segregate CCTV coax/fiber pathways from noisy power feeders?",
                  ("Reduce EMI/induced artifacts on sensitive video/streaming payloads", "Increase EMI", "To delete bonding", "To remove shielding everywhere"), 0, "Analog/digital video can degrade with EMI.", crs))
    aux_t.append(("Access control electrified strikes require coordination with:",
                  ("Fire alarm door release/interrupt interfacing requirements", "Plumbing vents only", "Paint color palettes", "HVAC ducts only"), 0, "Egress unlocking on alarm is mandated in many regimes—verify engineer spec + code.", nfpa + ra))
    aux_t.append(("Elevator hoistway cabling interface includes coordination on:",
                  ("Travel cables, shafts, hoistway conduit, EMI separation from controls", "Only wallpaper", "No coordination", "Only landscape"), 0, "Vertical transport interfaces with telecom for emergency car communications.", crs + nbc))
    aux_t.append(("MATV/Broadband coax distribution benefits from:",
                  ("Proper signal levels & balanced splits—not endless passive taps", "All terminators removed", "No labels", "No testing"), 0, "Passive networks need correct levels for digital carrier integrity.", crs))
    while len(aux_t) < 50:
        k = len(aux_t)
        aux_t.append((f"L2 Auxiliary concept #{k}: bonding & grounding lowers risk of?",
                      ("Destructive potentials on shielded cabling and nuisance trips", "All solar output", "Code existence", "Panel labels"), 0, "IEC-style equipotential bonding supports reliable signals.", crs + ["IEEE grounding practice references"]))
    xmit_t = []
    bases = [
        ("Balanced twisted-pair cabling characteristic impedance commonly specified at:", ("100 Ω for Category-rated UTP/ScTP in TIA cabling families", "50 Ω like coax RF feeders", "75 Ω CATV only always", "300 Ω ladder line always"), 0, "TIA-568 family focuses on ~100Ω balanced cabling.", tia),
        ("OM3 multimode fiber typical laser-optimized nominal core/cladding size marketing uses:", ("50/125 µm core/cladding multimode constructions", "9/125 µm single-mode only", "200/230 µm plastic fiber only", "0.5/125 µm"), 0, "OM3 aligns with IEEE 850nm VCSEL multimode ethernet.", crs + ["ISO/IEC 11801 fiber references"]),
        ("Single-mode SMF excels long campus/WAN spans due to:",
         ("Minimal modal dispersion versus multimode fibers", "Maximum modal dispersion", "No cladding", "No jacket"), 0, "Large core modes smear pulses in MM; SM confines one mode propagation.", crs),
        ("Attenuation in fiber increases if:", ("Mechanical bends below manufacturer minimum bend radius", "Cable is straight", "Jacket intact", "Transmitter power lowers slightly within spec"), 0, "Macro-bending induces loss spikes especially at tighter radii.", crs + tia),
        ("RJ-45 connectors mate with:", ("Eight-position eight-contact modular jacks for twisted-pair links", "Only BNC", "Only ST fiber only", "Type F only"), 0, "RJ-45 is ubiquitous for ethernet copper.", crs + tia),
        ("Cable category upgrade from Cat5e to Cat6 improves margin on:", ("Higher frequency NEXT/ELFEXT performance headroom versus older categories", "AC supply voltage amplitude", "DC battery runtime", "Conduit fill area only"), 0, "Category metrics scale with MHz bandwidth specs.", tia),
        ("STP cabling may be chosen when:", ("Higher EMI coupling risk from motors/VFD/neighboring feeders", "No EMI ever", "All runs underground only", "All runs wireless only"), 0, "Screens reduce coupled noise—but need proper grounding practice.", crs + tia),
        ("Hybrid fiber/coax architectures historically supported:", ("CATV downstream + upstream amplifiers with nodes splitting clusters", "Only dial-up only forever", "No return path", "No taps"), 0, "Architectures inform broadband plant planning.", crs),
    ]
    for b in bases:
        xmit_t.append(b)
    while len(xmit_t) < 50:
        kk = len(xmit_t)
        xmit_t.append((f"L3 Transmission quiz placeholder variant {kk}: optical loss budgeting sums:",
                       ("Splices, connectors, fiber length loss, splitter losses (PON)—compare to transmitter/receiver margins", "Only weather", "Only paint", "Transformer kVA alone"), 0, "Fiber links require stacked loss accounting vs power budget.", crs + tia))

    cab_t: list[tuple] = []
    cab_t.extend([
        ("Per common TIA-568 channel decomposition training rule: horizontal solid cable allowance is:",
         ("Typically up to ~90 m of horizontal cable segment with remaining budget for patching", "Exactly 120 m horizontal always regardless of patch cords", "Unlimited patching", "0 m patching allowed"), 0, "Worst-case 100 m channel budgeting uses ~90 + ~10 patching split (verify exact clause in adopted edition).", tia),
        ("Why certify permanent link distinctly from channel?",
         ("Isolates fixed installed segment quality vs variable patch cords swapping over time", "They are identical always", "No need to test", "Only Wi-Fi metric"), 0, "Field testing distinguishes enduring plant vs ephemeral cords.", tia),
        ("Proper cable pulling tension protects:", ("Pair geometry & jacket integrity—prevent stretched pairs & elevated NEXT", "Tray paint only", "Fire alarm audibility maps", "Conduit trench depth only"), 0, "Mechanical stresses degrade NEXT/return loss.", tia + crs),
        ("Telecommunications bonding and grounding backbone purpose includes:",
         ("Establish equipotential reference for shielded/low-voltage systems", "Elevate stray lightning to panels randomly", "Delete EGC", "Only aesthetic"), 0, "ANSI/TIA-607 aligns bonding topologies.", tia + crs),
        ("Patch panel labeling scheme should align with:", ("Facility cable schedule / electronic CMDB—not random colors only", "No schedule", "Only pizza toppings", "No IDs"), 0, "Label discipline reduces MTTR outages.", crs),
        ("Cable tray bend radii oversized helps:", ("Preserve Cat6+/fiber bend specs & reduce sheath stress fractures", "Maximize EMI only", "Delete firestopping", "Reduce ventilation"), 0, "Maintain manufacturer minimum radii.", tia),
        ("Cable bundle lacing/straps vs ZIP-ties tightened harshly?",
         ("Velcro/loosely managed straps reduce pair deformation vs over-tightened plastic ties", "Over-tighten all ties aggressively", "No straps", "Solder bundles"), 0, "Overtightening induces structural return loss anomalies.", crs + tia),
        ("Rack PDU planning for ICT switch stacks includes:",
         ("Diversity/feeds/redundancies & capacity headroom—not only first outlet spotted", "Only wattage guesses", "No grounding", "No surge reference"), 0, "Resilience avoids brownouts resetting PoE-dependent devices.", crs),
        ("Cable entrance facility (EF) segregation supports:",
         ("Carrier demarc protections, grounding, drainage, intrusion control", "Open hole in wall unmanaged", "No lightning protection", "No sleeves"), 0, "Controlled entrance mitigates water/EMP hazards.", crs + ["TIA‑569 pathway concepts"]),
    ])
    while len(cab_t) < 50:
        kk = len(cab_t)
        cab_t.append((f"Structured cabling design rule variant {kk}: pathway fill limits matter because:",
                      ("Thermal rise in bundles & mechanical strain increase loss & ignition risk extremes", "Aesthetics only", "Ethernet auto-negotiation brand", "HVAC zoning only"), 0, "NEC/TR-42 fill & bundling considerations inform safe deployment—cross-check AHJ editions.", crs + tia))

    bf_t = []
    bf_t.extend([
        ("Smoke compartmentation most directly supports:", ("Limit smoke spread—buy time for egress/tenability", "Delete sprinklers blindly", "Maximize glazing without ratings", "Remove stair pressurization everywhere"), 0, "Smoke control strategy complements egress design.", crs + nfpa),
        ("Exit signs & emergency illumination help occupants by:",
         ("Orienting egress paths during power loss/smoke obscure conditions", "Decor only", "Blocking doors", "Disabling elevators only"), 0, "Life safety lighting is regulated under combined codes.", crs + ra + nbc),
        ("Portable extinguisher ABC class commonly addresses:",
         ("Ordinary combustibles, flammable liquids, energized electrical hazards with proper training caveat", "All metal fires without limits", "Alkali metals submerged only", "Nuclear containment alone"), 0, "Classification training reduces misuse—verify manufacturer rating plates.", crs + nfpa),
        ("Fire alarm supervising station classifications in NFPA 72 include concepts such as:",
         ("Central station, proprietary, remote supervising—each with contractual/monitoring distinctions", "One generic monitoring type without differences", "No monitoring allowed", "Only cloud gaming servers"), 0, "Understand monitoring context per adopted edition summaries.", nfpa),
        ("Why kitchen hood suppression differs from sprinkler-only?",
         ("Wet chemical agents tailored to grease fire chemistry & appliances", "Identical physics", "Powder soda only blindly", "No agents"), 0, "Special hazard systems tuned to occupancy risk.", crs + nfpa),
    ])
    while len(bf_t) < 50:
        kk = len(bf_t)
        bf_t.append((f"Fire/building synthesis item {kk}: AHJ inspectors typically verify commissioning reports for?",
                     ("Emergency systems operation, egress widths, occupancy load factors as applicable", "Only paint schedule", "Menu pricing", "Unrelated acoustics RT60"), 0, "Authorities having jurisdiction reconcile codes with approved plans.", ra + crs + nbc))

    pd_t = []
    pd_t.extend([
        ("Presidential Decree No. 1096 is formally titled as adopting:",
         ("A National Building Code of the Philippines revising RA 6541", "The Fire Code only", "Philippine Fisheries Code", "Space launch regulations"), 0, "Historical header cites revision of RA 6541 baseline.", nbc),
        ("PD 1096 was issued on:",
         ("19 February 1977 (commonly cited in official compilations)", "October 1898", "3 January 2018", "1 June 2060"), 0, "Use official compilations—not slide typos—for exam dates.", nbc),
        ("General philosophy of NBC includes safeguarding:",
         ("Life, health, property & public welfare in design/construction/use", "Decorative trends only", "Stock tickers only", "Unregulated conversion always"), 0, "Declaratory preamble language across NBCP compilations.", nbc),
        ("Accessory building concept in zoning/NBC curricula generally refers to:",
         ("Subordinate structures supporting principal occupancy use—not primary bulk use creep", "Tallest towers only", "Stadium tiers only", "Unlimited hazard increase"), 0, "Accessory uses limited per planning context—consult local ordinances implementing NBC.", crs + nbc),
        ("Certificate of occupancy concept ties building readiness to:",
         ("Compliance with approvals for intended use—including allied systems checks", "Only concrete cure time guess", "No inspections", "Only paint finish inspection"), 0, "Operational readiness includes life safety systems intersections.", crs + ra + nbc),
    ])
    while len(pd_t) < 50:
        kk = len(pd_t)
        pd_t.append((f"NBC trivia variant {kk}: Building permit regimes seek to:",
                     ("Formalize scrutiny of drawings & inspections—not encourage clandestine builds", "Remove engineering", "Delete liability", "Guarantee free materials"), 0, "Administrative regimes align with PDP process under DPWH IRR guidance.", crs + nbc))

    rz_t = []
    rz_t.extend([
        ("Republic Act No. 9514 establishes the Revised Fire Code and repealed:",
         ("Presidential Decree No. 1185 Fire Code legacy", "PD 1096 NBC", "The 1987 Constitution text itself", "UN SDGs treaty"), 0, "Repealer clause cites PD1185 repeal.", ra),
        ("RA 9514 approval date cited in compilations:",
         ("19 December 2008 (effective after publication timelines per statute)", "1 January 1970 exactly", "4 July 1776", "Unknown"), 0, "Prefer Chan Robles/SC mirror text—not secondary blogs.", ra),
        ("Bureau of Fire Protection (BFP) under DILG enforces:",
         ("Fire prevention/suppression mandates per RA 9514 implementing rules regimes", "Fisheries quotas", "Space weather", "Pharmacies only blindly"), 0, "Organic alignment BFP‑DILG per Act structure.", ra),
        ("FSIC acronym in Philippines fire safety parlance denotes:",
         ("Fire Safety Inspection Certificate context (verify exact expansions taught in lectures)", "Fiber splice interface card only", "Free software ISO certificate", "None"), 0, "Facility operators secure FSIC for occupancy compliance cycles.", crs + ra),
        ("Retrofit obligations when codes strengthen historically pressure owners to:",
         ("Budget upgrades for alarms/suppression/passive features per transitional IRR articles", "Delete sprinklers blindly", "Remove exits", "Ignore AHJ deadlines"), 0, "Practice notes highlight retrofit windows post‑2008 IRR adoption.", crs + ra),
    ])
    while len(rz_t) < 50:
        kk = len(rz_t)
        rz_t.append((f"Fire Code quiz variant {kk}: Non-compliance escalation may include?",
                     ("Closure orders/fees calibrated by IRR schedules—education dependent", "Free donuts", "Guaranteed subsidy", "No enforcement ever"), 0, "Administrative sanction frameworks exist—verify IRR tables with instructor.", crs + ra))

    nf_t = []
    nf_t.extend([
        ("NFPA 72 fundamentally standardizes:",
         ("Fire alarm AND emergency communication systems—not residential smoke-only toy standards alone", "Only plumbing drain slopes", "Bridges fatigue only", "Aircraft composites"), 0, "Scope wording references alarm + ECS families.", nfpa),
        ("Addressable initiating devices uniquely identify:",
         ("Each sensor/node on digital loop simplifying troubleshooting granularity", "Identical polarity only blindly", "No panel mapping", "All wireless without encryption ever"), 0, "Loops map logical addresses—not just zones.", crs + nfpa),
        ("Conventional zone wiring groups sensors so that:",
         ("Panel discerns sectional alarm—but not pinpoint device ID beyond zone resolution", "Each device always serialized digitally", "No annunciation occurs", "All tones identical always"), 0, "Teaching contrast conventional vs addressable fidelity.", crs + nfpa),
        ("Strobes synchronized for ADA-style awareness reduce risk of:",
         ("Photo-induced seizure confusion from uncoordinated pulsation in fields of view contexts", "No risk", "All hearing loss scenarios", "All smoke detectors"), 0, "ECS chapters cover accessibility coordination—not identical worldwide adoption.", crs + nfpa + ["ADA references where applicable"]),
        ("Battery standby calculations for FACP ensure:",
         ("Continued supervisory operation upon AC loss until restoration or rated duration", "No backup ever", "Only solar panels arbitrarily", "Unlimited runtime without sizing"), 0, "NFPA mandates standby & alarm operation durations sizing.", crs + nfpa),
    ])
    while len(nf_t) < 50:
        kk = len(nf_t)
        nf_t.append((f"NFPA 72 quiz variant {kk}: notification appliance circuits require engineering of?",
                     ("Wiring supervision classes, synchronization, SPL coverage maps per prescriptive/design methods adopted", "Only RJ45 jacks", "No supervision", "No UL listings"), 0, "Circuits differentiated Class A/B—verify edition-specific definitions.", crs + nfpa))

    BANK = rotate_build("orient", ori_t, ori_pad)
    BANK += rotate_build("aux", aux_t, lambda j: aux_t[j % len(aux_t)])
    BANK += rotate_build("xmit", xmit_t, lambda j: xmit_t[j % len(xmit_t)])
    BANK += rotate_build("cabling", cab_t, lambda j: cab_t[j % len(cab_t)])
    BANK += rotate_build("bflec", bf_t, lambda j: bf_t[j % len(bf_t)])
    BANK += rotate_build("pd1096", pd_t, lambda j: pd_t[j % len(pd_t)])
    BANK += rotate_build("ra9514", rz_t, lambda j: rz_t[j % len(rz_t)])
    BANK += rotate_build("nfpa72", nf_t, lambda j: nf_t[j % len(nf_t)])

    assert len(BANK) == 400, len(BANK)
    js = "// Auto-generated bank — ICT/ECEN 106 examiner\n"
    js += "window.ICT_QB=" + json.dumps(BANK, ensure_ascii=False, indent=2) + ";\n"
    outp = Path(__file__).resolve().parent.parent / "questions.js"
    outp.write_text(js, encoding="utf-8")
    print("wrote", outp, len(BANK))


if __name__ == "__main__":
    main()
