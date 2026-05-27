# -*- coding: utf-8 -*-
"""
Unique MCQ templates for ICT bank generation: cores × sentence frames = non-repeating stems.
Each core is a distinct learning point; frames rephrase the scenario without cloning the same stem.
"""
from __future__ import annotations

# --- Primary references: provided course PDFs (see MATERIALS.md) ---
L1 = ["ECEN106 L1 — Course Orientation v25.26.2 (PDF)"]
L2 = ["ECEN106 L2 — Introduction to Building Auxiliary Systems v25.26.2 (PDF)"]
L3X = ["ECEN106 L3 — Transmission Media v25.26.2 (PDF)"]
L3C = ["ECEN 106 L3 — Structured Cabling Standards v25.26.2 (PDF)"]
L6 = ["L6 Building Code and Fire Safety Issues v25.26.2 (PDF)"]
PD = ["PD-1096_National-Building-Code_2005 (PDF)"]
RA = ["RA-9514_Fire-Code_2019 (PDF)"]
NFPA = ["NFPA 72 2019 (PDF)"]
# Shorthand bundles per topic (lecture PDF first; statute PDF where applicable)
CRS = L1
TIA = L3C
NBC = PD
NBC_GEN = L1 + L6 + PD

# Prefixes must yield grammatical English when concatenated with core[0] starting lowercase.
STEM_FRAMES: list[str] = [
    "",
    "On a site with shared MEP/FA/ICT responsibility, ",
    "When submittals are compared to the basis-of-design narrative, ",
    "During O&M turnover and as-built reconciliation, ",
    "After a coordination clash is logged in the BIM tracker, ",
    "When training owner staff on alarm silencing and reset policies, ",
    "During insurance or third-party loss-control review, ",
    "When sequencing a tenant improvement above an occupied floor, ",
    "Under value engineering pressure but life-safety cannot be deleted, ",
    "When reconciling manufacturer cut-sheets to field measurements, ",
    "If AHJ comments reference penetrations and rated assemblies, ",
    "When commissioning scope includes audibility and pathway integrity, ",
    "During cable infrastructure warranty walk-down, ",
    "For documentation intended to survive staff turnover, ",
    "When harmonics and noise from VFD plant affect nearby pathways, ",
    "If tropical lightning exposure elevates surge and bonding risk, ",
    "When contractor scope overlap could orphan test records, ",
    "When mock-up or pilot rooms precede full roll-out, ",
]


def _mcq(
    stem: str,
    correct: str,
    w1: str,
    w2: str,
    w3: str,
    expl: str,
    refs: list[str],
) -> tuple[str, tuple[str, str, str, str], int, str, list[str]]:
    return (stem, (correct, w1, w2, w3), 0, expl, refs)


def interleave_unique(
    cores: list[tuple[str, tuple[str, str, str, str], int, str, list[str]]],
    frames: list[str],
    target: int,
) -> list[tuple[str, tuple[str, str, str, str], int, str, list[str]]]:
    nc, nf = len(cores), len(frames)
    if nc * nf < target:
        raise ValueError(f"Need {target} unique stems; expand cores or frames (have {nc}×{nf}={nc * nf}).")
    out: list[tuple[str, tuple[str, str, str, str], int, str, list[str]]] = []
    seen: set[str] = set()
    for i in range(target):
        ci = i % nc
        fi = (i // nc) % nf
        stem0, opts, ai, expl, refs = cores[ci]
        frame = frames[fi]
        if not frame:
            stem = stem0
        else:
            rest = stem0[0].lower() + stem0[1:] if stem0 else ""
            stem = frame + rest
        if stem in seen:
            raise RuntimeError(f"Duplicate stem after frame expand: {stem[:120]!r}")
        seen.add(stem)
        out.append((stem, opts, ai, expl, refs))
    return out


# --- 15 cores per section: distinct topics (no numbered “variant” clones) ---

ORIENT_CORES = [
    _mcq("which outcome is the primary purpose of integrated auxiliary-systems coordination?", "Reducing destructive clashes between structure, life-safety, and low-voltage pathways", "Eliminating all peer review to save calendar", "Delegating code compliance to furniture vendors only", "Using cloud API pricing as the sole design driver", "Coordination exists to keep rated barriers, egress, FA, and ICT aligned—see PD 1096 + RA 9514 interfaces with pathways.", NBC_GEN + RA),
    _mcq("why must NBC (PD 1096) and fire codes be read alongside ICT routing rules?", "They govern penetrations, shaft ratings, egress widths, and inspection evidence that bound where cable may run", "They ban optical fiber outright", "They replace TIA performance categories without testing", "They apply only to maritime vessels", "Telecom paths must respect rated barriers and egress—legal crosswalk, not optional.", NBC + RA),
    _mcq("what does defensible documentation for auxiliary systems emphasize?", "Traceable drawings, labels, test forms, permits, and as-built deltas", "Verbal sign-offs that cannot be audited", "Withholding firestop details from facilities", "Password exports mislabeled as shop drawings", "Accountability needs reproducible records for O&M and enforcement.", CRS),
    _mcq("what is the main benefit of a formal commissioning mindset for FA/ICT interfaces?", "Evidence that installed behavior meets owner criteria and adopted codes before acceptance", "Random cable colors without maps", "Skipping FAT/SAT because schedule is tight", "Deleting loop resistance logs", "Commissioning produces verification artifacts beyond ‘it powered on’.", CRS + NFPA),
    _mcq("what should structured cabling inventories and project BOQs support?", "Moves/adds/changes tracking, market-priced quantities, and commissioning test evidence", "Deleting serials after install", "Avoiding any cable ID scheme", "Replacing schedules with lunch menus", "Per L1 project deliverables: BOQ with pricing and commissioning pass/fail logs; schedules tie labels to routes and tests.", L1 + L3C),
    _mcq("what is a realistic cost of failing inspection for penetrations or FA circuits?", "Re-work, re-inspection, schedule slip, and reputational risk with the AHJ", "Zero cost if drawings are stamped", "Only a weekend social event", "Offset by unrelated SaaS credits", "Authority having jurisdiction can stop work or issue orders—plan for it.", RA + CRS),
    _mcq("how should subcontractor ICT packages reduce latent defects?", "Referenced standards, test limits, milestones, and acceptance criteria in the contract data", "Handwritten scope on napkins", "No acceptance tests", "Unlimited undocumented changes", "Clear criteria prevent ‘we thought it was done’ disputes.", TIA + CRS),
    _mcq("why model cable tray fill and bend zones early?", "Thermal rise, bend-radius compliance, segregation, and maintenance access", "Tray notes exist only for paint schedules", "Ignore coordination to go fast", "Tray fill is purely decorative", "Tray engineering interacts with code and cable performance.", CRS + TIA),
    _mcq("what is a credible commissioning artifact for occupant notification audibility?", "Sound-level maps or measurements tied to device layout vs approved criteria", "A single panel photo", "An informal email thread only", "Guessing loudness by ear without data", "Acceptance should reference measurable evidence where required.", NFPA + CRS),
    _mcq("what must value engineering never remove from auxiliary scope?", "Minimum code-mandated life-safety and egress performance", "All budget padding blindly", "Peer review on every bolt", "Permits for interior paint only", "VE cannot delete rated barriers or required detection/notification where prescribed.", RA + NBC),
    _mcq("why are O&M manuals and operator training material for FA/ICT still important post-handover?", "Misconfiguration after turnover can defeat supervision, silencing rules, and maintenance discipline", "They automatically waive code", "They replace listed equipment", "They delete event logs legally", "Human factors determine whether engineered systems stay compliant.", CRS),
    _mcq("what does a cable schedule row credibly document?", "From–to IDs, media type, strand/fiber count, test class, and label scheme", "Unrelated finance pivot tables", "Only Wi-Fi SSIDs", "No correlation to jack labels", "Schedules underpin troubleshooting and MAC.", CRS + TIA),
    _mcq("why keep penetration firestop packets aligned to cable schedule changes?", "Rated assemblies must reflect actual penetrating items and sealing methods for inspection", "Firestop is unrelated to cabling", "Use caulk colors only as proof", "Abandon bundles after commissioning", "Pathway edits without firestop updates fail inspection.", NBC + CRS),
    _mcq("what distinguishes as-built documents from record-drawing folklore in auxiliary work?", "As-built documents capture field deviations and revised labels against issued IFC drawings", "As-built means pristine concept diagrams only", "They should omit lengths and routes", "They are optional if email exists", "Per L6/cabling turnover: as-built documents reflect implemented changes; record drawings document the built state.", L6 + L3C),
    _mcq("when multidisciplinary RFI queues grow, what practice best protects auxiliary quality?", "Triage RFIs that affect pathways, bonding, FA interfaces, and inspection hold points", "Close all RFIs as ‘N/A’", "Defer bonding questions indefinitely", "Answer only interior finish RFIs", "Critical RFIs affect code and performance—prioritize them.", CRS),
]

AUX_CORES = [
    _mcq("which subsystem is least central to typical ‘building auxiliary’ coursework versus full plant automation?", "Standalone refinery cracking-unit SCADA unrelated to tenancy life-safety", "CCTV for concourse surveillance", "Access control securing stair doors", "PA paging for phased evacuation cues", "Curricula center on tenancy-scale auxiliary services—not distant process automation.", CRS),
    _mcq("why route sensitive video/coax/fiber away from aggressive power feeders?", "Reduce EMI/induced artifacts and ground-loop tendencies on shields and receivers", "Guarantee more EMI by co-binding neutrals", "Delete equipotential bonding references", "Remove shield drains everywhere", "Video and signaling can degrade when coupled to noisy feeders.", CRS + TIA),
    _mcq("what must electrified access hardware coordinate with for life safety?", "Fire alarm–initiated door release/hold-open interfaces per code and engineer spec", "Plumbing fixture finishes only", "Only paint sheen schedules", "HVAC chilled-water reset alone", "Egress unlocking on alarm is a recurring FA interface—verify listing and wiring class.", NFPA + RA),
    _mcq("what is a primary hoistway/elevator telecom coordination item?", "Travel cable, shaft conduit, and EMI separation for car emergency communications", "Wallpaper pattern alignment", "Ignoring shaft drawings", "Landscape irrigation timing", "Vertical transport has code-driven emergency comms paths.", CRS + NBC),
    _mcq("what keeps broadband/MATV-like coax plants stable?", "Balanced tap levels and controlled splits—not unterminated endless taps", "Removing all terminators", "Skipping sweep tests", "Random label colors only", "Passive RF networks need engineered levels.", CRS),
    _mcq("how does equipotential bonding mainly help ICT and low-voltage reliability?", "It limits destructive potential differences and nuisance trips on shields and racks", "It removes all solar inverter output issues alone", "It voids NEC-style equipment grounding concepts", "It replaces FACP programming", "Bonding supports consistent reference potentials per IEEE-style practice.", CRS + TIA),
    _mcq("when PoE switch ports feed many access devices, what design issue matters beyond port count?", "Heat grouping, cable bundle temperature, and supply headroom per IEEE 802.3bt-era practice", "Only paint on rack doors", "Disabling LLDP only", "Assume all UTP handles any DC loss", "Higher classes concentrate heat; check switch and cable thermal guidance.", CRS + TIA),
    _mcq("what is a sound reason to segregate FA speaker and data pathways in documentation?", "Fault isolation, interference control, and inspection clarity even if cables share trays in some regimes", "They must occupy the same pair without supervision", "Voice evac may use office Wi-Fi without design", "NAC wiring never needs labeling", "Separation discipline supports testing and AHJ comprehension.", NFPA + CRS),
    _mcq("why specify SPD coordination at telecom entrance rooms in lightning-exposed sites?", "Limit surges entering sensitive electronics and coordinate with bonding/EGC networks", "Delete primary protectors to save space", "Float all shields at both ends unconditionally", "Use Type 5 SPDs only (nonexistent gag)", "Entrance facility practice couples surge, bonding, and carrier demarc protections.", CRS + TIA),
    _mcq("what practice reduces ground-loop hum on shielded analog AV homeruns?", "Planned shield termination and single-point video ground reference per design—no ad hoc lifts", "Ground every shield at both ends without analysis", "Use AC neutral as signal return", "Parallel unshielded extension cords as ‘reference’", "Ground topology must follow equipment and BICSI-style guidance.", CRS),
    _mcq("when BMS and FA share only ‘informational’ links, what still cannot be assumed?", "That either system waives listing, supervision, or separation rules for the other", "That BACnet automatically equals fire alarm listing", "That Wi-Fi credentials prove NAC Class", "That smoke control is ‘optional BACnet’", "Listed FA equipment and pathways retain their constraints.", NFPA + CRS),
    _mcq("what is a prudent rack-level grounding practice?", "Mechanical bonding of rack frames to telecom bonding busbar/backbone with short low-Z paths", "Rely on carpet static alone", "Loop EGC paths for aesthetics", "Share a single conductor for lightning and FA NAC without analysis", "Rack bonding is part of equipotential design for ICT.", TIA + CRS),
    _mcq("why maintain emergency elevator phone pathways independent of tenant phone MAC?", "Responder call integrity must survive tenant churn and carrier changes", "Tenants may delete emergency dialers casually", "Hoistway phones are optional decor", "Use consumer mobile only without backup", "Survivability and code expectations favor engineered, labeled paths.", CRS + NBC),
    _mcq("what is a common risk of mixing high-harmonic VFD feeders with unshielded signal pairs in one tight bundle?", "Coupled noise that raises BER or disturbs analog baselines without planned segregation", "Guaranteed fiber fusion without splicing", "Automatic improvement of Cat3 performance", "Elimination of utility demand charges", "Magnetic and capacitive coupling rises with proximity and poor segregation.", CRS + TIA),
    _mcq("what should a PA/evac interface study verify beyond ‘it plays audio’?", "Intelligibility criteria, gain structure, backup power, and FA priority over background music", "Only speaker color", "Only Bluetooth pairing", "Only streaming playlist rights", "Mass notification and voice evac have performance and priority rules.", NFPA + CRS),
]

XMIT_CORES = [
    _mcq("what nominal characteristic impedance aligns with balanced twisted-pair in TIA-568-class channels?", "Near 100 Ω for Category-rated UTP/ScTP", "Always 50 Ω coax feedline", "Always 300 Ω twin-lead television", "75 Ω only for every Ethernet link", "Category copper is engineered around ~100 Ω balanced lines.", TIA),
    _mcq("what construction typifies OM3 multimode at 850 nm VCSEL Ethernet?", "50/125 µm graded-index core/cladding", "9/125 µm single-mode only", "200/230 µm POF for all campus", "0.5/125 µm fictional core", "OM3 marketing centers on laser-optimized 50 µm MMF.", CRS + TIA),
    _mcq("why does single-mode fiber favor very long spans versus MMF?", "Modal dispersion is negligible with one propagating mode", "Modal dispersion is maximized by design", "SMF deletes the cladding entirely", "SMF removes the jacket requirement", "SM confines energy to one mode; MM smears pulses at distance.", CRS),
    _mcq("what field condition most commonly spikes optical loss beyond budget?", "Bends tighter than manufacturer minimum bend radius", "Perfectly straight cable only", "Intact nominal jacket thickness", "Slight transmitter power trimming within datasheet", "Macro-bending and stress induce localized attenuation.", TIA + CRS),
    _mcq("what does an eight-position modular plug interface with for structured copper?", "Eight-contact RJ-45 style jacks on twisted-pair links", "BNC-only video", "ST fiber patch field exclusively", "Type-F satellite drop only", "RJ-45 is the dominant copper Ethernet interface.", TIA + CRS),
    _mcq("what improves when moving from Cat5e to higher categories at similar length?", "High-frequency NEXT/ELFEXT/return-loss headroom enabling higher PHY rates", "AC mains voltage amplitude at outlets", "Battery amp-hour for FACP", "Concrete cure time", "Category numbers track MHz-class performance.", TIA),
    _mcq("when is screened twisted pair more defensible?", "High EMI environments with motors/VFDs and poor proximity control", "Zero EMI environments only", "Only if all wireless", "Never—screened cable is decorative", "Screens help when coupled noise threatens margins—ground them properly.", TIA + CRS),
    _mcq("what does a hybrid fiber/coax broadband plant emphasize pedagogically?", "Forward/return amplifiers, nodes, and tap hierarchies—not flat coax only", "Dial-up modulation forever", "No return path notion", "Unlimited unmanaged taps without levels", "Legacy plant informs modern PON-vs-HFC contrasts.", CRS),
    _mcq("what components belong in an optical loss budget spreadsheet?", "Connectors, splices, fiber length attenuation, splitters—and compare to Rx sensitivity", "Only outdoor temperature", "Only interior paint VOC", "Only transformer nameplate kVA unrelated to optics", "Link budgets stack losses versus power margins.", TIA + CRS),
    _mcq("why care about polarization-mode dispersion on some long single-mode WAN links?", "It can limit ultra-long high-bitrate coherent systems—campus context may ignore, but coursework links concepts", "It helps MMF carry more modes faster", "It removes need for connectors", "It increases modal dispersion magically", "PMD is a SMF impairment at extremes—note for design awareness.", CRS + TIA),
    _mcq("what distinguishes OM4 from OM3 at a high level?", "Higher effective modal bandwidth supporting longer OM4 links at same data rate/wavelength family", "OM4 forbids VCSELs", "OM4 is always single-mode", "OM4 deletes cladding", "OMx families differ by bandwidth-length product.", CRS + TIA),
    _mcq("what is a reason installers avoid excess fiber pigtail slack in crowded trays?", "Tight bends and kinks beyond minimum bend radius raise optical loss", "Bending always improves laser linewidth", "Slack lowers connector loss unconditionally", "Trays desire maximum random loops", "Per L3 transmission media: fiber is fragile if bent beyond minimum bend radius; kinked cable elevates loss.", L3X + L3C),
    _mcq("what Ethernet physical concern rises with marginal copper plant?", "Flapping link due to frame errors from marginal NEXT/RETURNLOSS—not ‘Wi-Fi jealousy’ alone", "CPU fan speed spikes", "Printer toner levels", "HVAC zoning labels", "Layer-1 anomalies masquerade as flaky upper layers.", TIA),
    _mcq("why specify cleaning before fiber mating?", "Dirty end-faces elevate reflection/loss and can damage ferrules under pressure", "Dirt deliberately improves polish", "Alcohol swaps are outlawed universally", "No inspection microscope should be used ever", "Contamination dominates field failures.", TIA + CRS),
    _mcq("what is a classroom-faithful contrast between multimode and single-mode laser sources?", "MM often uses 850 nm VCSELs; SM often uses 1310/1550 nm lasers on smaller cores", "Both always use identical 2.4 GHz radios", "SM always uses VCSEL into 50 µm only", "MM forbids LEDs pedantically forever", "Transmitter/core matching is fundamental.", CRS + TIA),
]

CABLING_CORES = [
    _mcq("what horizontal solid-copper segment length is commonly taught as the fixed plant portion of a 100 m channel?", "About 90 m horizontal cable with remaining budget for cords—verify edition", "Always 120 m horizontal regardless of patch leads", "Zero meters of horizontal allowed", "Unlimited patch cords without testing", "Channel models split permanent vs patch contributions.", TIA),
    _mcq("why test permanent link separately from channel?", "It isolates installed cable quality from variable patch cord swaps", "They are always identical by definition", "Only Wi-Fi needs testing", "Permanent link ignores connectors", "Owners change patch cords; plant should stand alone.", TIA),
    _mcq("what mechanical failure mode does excessive pull tension risk on UTP?", "Pair geometry deformation elevating NEXT/return loss", "Only tray paint cracking", "Improved alien crosstalk automatically", "Increased DC battery life", "Do not exceed cable tension limits.", TIA + CRS),
    _mcq("what is a core purpose of TIA-607-style telecommunications bonding?", "Equipotential reference for racks, shields, and protectors", "Floating all EGC connections", "Decorative copper patterns", "Deleting primary protectors", "Bonding backbone supports reliable low-voltage operation.", TIA + CRS),
    _mcq("patch panel labels should map to what operational artifact?", "Cable schedule / CMDB jack IDs", "Pizza topping codes only", "Random colors without legend", "No correlation to tests", "Label discipline drives MTTR.", CRS + TIA),
    _mcq("why oversize tray bend radii for Cat6A/fiber?", "Meet minimum radii and reduce jacket micro-cracks under heat/flex", "Maximize alien crosstalk on purpose", "Delete firestopping obligations", "Reduce ventilation intentionally", "Bend control protects margin.", TIA),
    _mcq("why prefer hook-and-loop over over-torqued plastic ties on high-rate pairs?", "Avoid pair deformation and structural return loss spikes", "Tight plastic ties improve gigabit by crushing pairs", "Never strap bundles", "Solder bundles for strength", "Mechanical abuse changes impedance.", TIA + CRS),
    _mcq("what should rack PDU planning include for PoE-heavy switches?", "Diversity/feeds, capacity headroom, and grounding references", "Only first outlet seen", "Ignore inrush on stack reboot", "No surge reference context", "Stacked PoE loads stress branch circuits.", CRS),
    _mcq("what is a cable entrance facility (EF) responsibility?", "Demarc protection, grounding, drainage, and controlled carrier handoff", "Open sleeve with no labels", "Delete lightning protection outright", "No sleeves through envelope", "EF is a security and surge boundary.", CRS + TIA),
    _mcq("why do pathway-fill and bundle-temperature narratives matter ethically?", "Overfill can elevate temperature and impair dielectric performance or accelerate aging extremes", "Fill is unrelated to NEC/TR-42 thought exercises", "Bundle heat only affects HVAC tonnage contracts", "Fill is aesthetics", "Responsible designers model fill and airflow.", CRS + TIA),
    _mcq("what best describes a consolidation point in zone cabling pedagogy?", "An intermediate splice/connection point between horizontal and work-area flexibility", "The building main breaker only", "A Wi-Fi SSID VLAN", "A paint color sample board", "Zone models support open-plan churn.", TIA),
    _mcq("why administer TIA-606 color/label schemes?", "Moves/adds/changes speed and error reduction", "Make racks pretty only", "Replace testing entirely", "Obfuscate jack IDs for security through obscurity", "Consistent IDs reduce human error.", TIA + CRS),
    _mcq("what is tested in alien crosstalk heavy designs?", "Cable-to-cable coupling in six-around-one bundles—not just pair NEXT in one cable", "CPU temperature", "Printer queue depth", "Only fiber chromatic dispersion", "AXT matters for 10GBASE-T class plants.", TIA),
    _mcq("what is an advantage of factory-terminated fiber assemblies where quality is controlled?", "Repeatable polish/geometry lowering field variability", "They always violate bend radius", "They delete need for any testing", "They forbid OTDR traces", "Preterms speed reliable deployment.", TIA + CRS),
    _mcq("why document test limits (e.g., NEXT/RL) per standard on reports?", "Prove compliance to purchase spec and enable warranty claims", "Decorative PDF footers", "Hide failures from owner", "Replace AHJ inspection", "Field reports are contract artifacts.", TIA + CRS),
]

BFLEC_CORES = [
    _mcq("what is the primary life-safety aim of smoke compartmentation?", "Slow smoke spread to protect egress and tenability windows", "Delete sprinklers without analysis", "Maximize un-rated glazing everywhere", "Remove stair pressurization always", "Compartmentation complements active systems.", CRS + NFPA),
    _mcq("how do exit signs/emergency lighting assist occupants?", "Orient egress during power loss or smoke obscuration", "Serve only interior decor", "Block doors intentionally", "Disable elevators only without signage context", "Wayfinding is codified in combined regimes.", CRS + RA + NBC),
    _mcq("what does a typical ABC portable extinguisher cover with training caveats?", "Ordinary combustibles, flammable liquids, energized equipment—within rating limits", "All alkali-metal fires blindly", "Unlimited metal fires without class D agents", "Nuclear containment alone", "Classification reduces misuse.", CRS + NFPA),
    _mcq("what contrast exists among NFPA 72 supervising station concepts?", "Central, proprietary, remote supervising differ in contracts and monitoring duties", "There is only one monitoring type", "Monitoring is illegal", "Only gaming servers qualify", "Students must know vocabulary context.", NFPA),
    _mcq("why are kitchen hood suppression systems not ‘just sprinklers’?", "Wet chemical agents target grease chemistry and appliance plenums", "Identical to office pendant spray only", "No agent is required ever", "Only portable fans matter", "Special hazards differ from hydraulics of ordinary sprinklers.", CRS + NFPA),
    _mcq("what should AHJ review tie to for emergency systems?", "Approved plans, test reports, egress elements, and occupancy factors", "Only paint schedules", "Cafeteria menu pricing", "Unrelated RT60 speech tests alone", "Inspection scope is broad.", RA + NBC + CRS),
    _mcq("what is a purpose of stair pressurization or smokeproof stairs where used?", "Keep escape routes tenable vs smoke migration", "Increase smoke in stairs", "Replace exit width math", "Guarantee elevator use in fire unconditionally", "Smoke control interacts with egress strategy.", NFPA + CRS),
    _mcq("why maintain fire-rated penetrations documentation for telecom sleeves?", "Restores rating integrity and proves listed systems were installed as tested", "Firestop is optional decor", "Any caulk color suffices", "Penetrations never affect FA", "Penetrations are inspection hot spots.", NBC + CRS),
    _mcq("what is a classroom takeaway on photoluminescent egress markings?", "They provide passive wayfinding when power fails—subject to local adoption", "They replace all electrical exit signs everywhere always", "They glow forever without charging light", "They are banned globally", "Adoption varies—check local code pack.", CRS + RA),
    _mcq("what does ‘occupant load’ influence in building design reviews?", "Exit widths, exit numbers, and assembly seating patterns", "Only carpet fiber type", "Only cloud VM counts", "Only marketing headcount guesses", "Load factors drive egress capacity.", NBC + CRS),
    _mcq("what is a credible reason for duct-type smoke detectors in some HVAC configurations?", "Detect smoke transported by HVAC—subject to engineered placement and approvals", "Replace spot detectors everywhere", "Guarantee no FA wiring", "Only measure airflow temperature", "Duct detectors are selective tools.", NFPA + CRS),
    _mcq("why might clean-agent systems appear in auxiliary discussions?", "They protect valued assets/server rooms where water damage risk is unacceptable—listing still governs", "They replace egress", "They delete detection", "They are unrestricted DIY foam parties", "Gaseous suppression is a special hazard trade.", CRS + NFPA),
    _mcq("what failure mode motivates maintaining exit discharge clarity?", "Crowd confusion during emergencies at discharge points", "Hide exits behind merchandise racks legally", "Discharge only into kitchens", "Discharge requires revolving doors only without clauses", "Exit discharge paths must remain identifiable.", NBC + CRS),
    _mcq("what interplay exists between NBC egress philosophy and telecom shaft penetrations?", "Shafts must preserve ratings and pathways must not defeat compartment goals", "Telecom may ignore shafts entirely", "All shafts may be unrated if fiber", "Shafts only carry plumbing", "Risers intersect rated construction.", NBC + CRS),
    _mcq("why study portable extinguisher training alongside ICT/auxiliary coursework?", "Technicians routinely enter IDF/MPO rooms with energized gear and combustible loading risks", "Extinguishers are irrelevant in buildings", "Only homes need training", "Training waives NEC", "Facility access safety is holistic.", CRS + NFPA),
]

PD1096_CORES = [
    _mcq("PD 1096’s formal role in curriculum is best described as:", "A national building code framework revising prior building law lineages—not the fire-code-only act", "The sole fisheries code", "The Clean Air Act for vehicles", "The Space Launch Act", "PD 1096 is the NBC family header in materials.", NBC),
    _mcq("which date is cited in the provided PD 1096 materials for NBC issuance?", "19 February 1977", "4 July 1776", "19 December 2008", "1 June 2060", "Per PD 1096 / L6 materials: NBC issued 19 February 1977. (b)–(d) are distractor dates.", PD + L6),
    _mcq("what broad public goals does NBC philosophy usually declare?", "Life, health, property, and welfare in the built environment", "Stock tickers only", "Decor trends only", "Unlimited conversion without review", "Preambles express protective purposes.", NBC),
    _mcq("how is ‘accessory building’ commonly framed versus principal use?", "Subordinate structure supporting principal occupancy within limits", "Tallest tower always", "Unlimited hazard upgrade free", "Primary revenue generator by definition", "Zoning/NBC coursework stresses subordination.", NBC + CRS),
    _mcq("what does certificate of occupancy readiness generally imply?", "Approved use per submitted plans and allied system compliance checks", "Concrete cure guess only", "No inspections ever", "Paint finish alone", "CO ties occupancy to compliance.", NBC + RA + CRS),
    _mcq("why do local building permits persist even with national codes?", "LGUs implement review, fee, and inspection administration per rules", "Permits are abolished nationally", "Engineering seals delete permits", "Barangay permits alone equal full structural review always", "Implementation is layered.", NBC + CRS),
    _mcq("what is a defensible reason NBC study pairs with auxiliary systems?", "Pathways and openings affect rated assemblies, egress, and inspection evidence", "NBC forbids all fiber", "NBC ignores shafts", "NBC replaces TIA testing", "Cross-discipline routing is constrained.", NBC + TIA + CRS),
    _mcq("which practice best matches NBC intent for changes of occupancy?", "Re-evaluate structural, egress, and system adequacy for the new use", "Ignore new use if paint is fresh", "Assume prior CO covers all futures automatically", "Only update marketing brochures", "Use changes trigger technical review.", NBC + CRS),
    _mcq("what is an ethical issue with undisclosed mezzanine inserts?", "They can defeat egress, structural, and smoke plans approved on original occupation", "They always reduce loads magically", "They are invisible to inspectors", "They increase exit width automatically", "Concealed changes are professional misconduct risks.", NBC + CRS),
    _mcq("what is a classroom point about setbacks and height controls?", "They manage exposure, daylight, fire access, and urban form under local zoning implementing rules", "They are meaningless lines on paper always", "They only apply to boats", "They replace structural engineering", "Setbacks interplay with roads and exposures.", NBC + CRS),
    _mcq("why study mechanical equipment screens and roof plant in NBC context?", "They affect firefighter access, smoke venting, and structural loading", "They are purely aesthetic", "They delete FA needs", "They never need maintenance access", "Roofscapes interact with operations.", NBC + CRS),
    _mcq("what role do ‘approved plans’ play in auxiliary documentation chains?", "They become the baseline for inspections and as-built reconciliation", "They are optional sketches", "They are replaced by oral promises", "They forbid any changes ever", "Plan approval anchors compliance.", NBC + CRS),
    _mcq("which issue arises if exit signage is occluded by new tenant build-outs?", "Egress markings may violate visibility rules requiring redesign", "Signage never matters", "Only Wi-Fi roaming matters", "Glazing ratings are unrelated", "Tenant improvements can defeat life-safety visuals.", NBC + RA + CRS),
    _mcq("what is the risk of interpreting NBC clauses without IRR/local ordinances?", "Miss enforceable thresholds and administrative steps", "IRR is never relevant", "Local rules are illegal", "NBC is self-enforcing without LGU", "Layered implementation matters.", NBC + CRS),
    _mcq("why might accessibility provisions intersect auxiliary design?", "Controls, annunciators, and strobes have reach, height, and notification rules in combined codes", "Accessibility ignores FA", "Strobes never synchronize", "Only ramps matter", "Multi-code projects must be read together.", NBC + CRS + NFPA),
]

RA9514_CORES = [
    _mcq("RA 9514’s relationship to PD 1185 is best stated as:", "RA 9514 repeals/replaces the legacy fire code framework cited in textbooks", "RA 9514 adopts NBC as fire code verbatim only", "PD 1185 remains untouched forever", "RA 9514 governs fisheries only", "Students track repealer clauses.", RA),
    _mcq("RA 9514 is formally titled in course materials as which fire code vintage?", "Fire Code of the Philippines of 2008", "Fire Code of 1977 only (PD 1185 never repealed)", "Clean Water Act of 2004", "Renewable Energy Act of 2008", "Per RA 9514 PDF and L6: Republic Act No. 9514 of 2008. PD 1185 is repealed in lecture crosswalk.", RA + L6),
    _mcq("which agency alignment is textbook for BFP?", "BFP under DILG enforces RA 9514 implementing rules regimes", "BFAR under DA", "DOTr only", "Private insurers only", "Organic structure is exam-ready.", RA),
    _mcq("what does FSIC generally represent in facility operations?", "Fire safety inspection certificate context tied to occupancy compliance cycles", "Fiber splice interface card", "Free software ISO label", "Fuel storage interface code", "Acronym literacy matters.", CRS + RA),
    _mcq("what economic pressure arises when codes retroactively strengthen?", "Retrofit budgeting for alarms, suppression, or passive measures", "Delete sprinklers blindly", "Ignore AHJ timelines", "Always free upgrades from vendors", "Retrofit windows affect owners.", CRS + RA),
    _mcq("what is a classroom-true distinction for fire exits versus ordinary doors?", "Exits satisfy width, discharge, signage, and hardware rules for evacuation", "Any labeled ‘private’ door suffices", "Revolving doors are always unrestricted", "Exit hardware may be any slide bolt", "Exit assembly is regulated.", RA + CRS),
    _mcq("why study hot-work programs with RA 9514 enforcement context?", "Ignition risk control under permits, watches, and coverage rules", "Hot work never starts fires", "Welding ignores combustibles magically", "No permits exist", "Hot work is a recurring enforcement theme.", RA + CRS),
    _mcq("what can escalate from repeated non-compliance narratives in lectures?", "Orders, fines, or operational restrictions calibrated by rules—verify IRR tables with instructor", "Guaranteed donuts", "Automatic fiscal subsidies", "Permanent immunity if trained once", "Sanctions frameworks exist.", RA + CRS),
    _mcq("why are fire lanes and access widths stressed?", "Appliance maneuvering and emergency response staging", "Lanes are for food trucks only", "They replace interior exits", "They delete hydrant spacing thought", "Access for BFP apparatus matters.", RA + CRS),
    _mcq("what storage issue ties RA 9514 study to auxiliary spaces?", "Housekeeping of combustible loading near electrical/FA gear in IDF and work rooms", "Storage is irrelevant indoors", "Only ship holds matter", "NFPA 72 deletes storage codes", "Good housekeeping interfaces with ignition risk.", RA + CRS),
    _mcq("what does ‘occupant load calculation’ interact with under fire code lens?", "Number and width of exits, exit signs, and sometimes standpipe demands", "Only interior design mood boards", "Only cloud billing", "Only lighting lux for aesthetics", "Load drives exits.", RA + NBC + CRS),
    _mcq("why might temporary structures still need FSIC pathways thought?", "Temporary uses still carry inspection and mitigation expectations in many LGU flows", "Tents never need review", "Pop-ups waive all rules", "FSIC applies only to ships", "Temp events still regulated variably.", RA + CRS),
    _mcq("what is the risk of skipping fire drills in assembly occupancies?", "Occupants unfamiliar with egress options under stress", "Drills guarantee zero emergencies", "Drills replace extinguishers", "Drills are illegal", "Training reveals path issues.", RA + CRS),
    _mcq("how does RA 9514 study complement NFPA 72 in these courses?", "RA sets enforcement; NFPA informs engineered system behaviors you must reconcile", "They are interchangeable word-for-word", "One deletes the other", "Only NFPA applies in Philippines always", "Crosswalk engineering vs statute.", RA + NFPA + CRS),
    _mcq("what is an ethical stance on ‘informal approval’ bypassing FSIC?", "It can expose operators to closure risk and invalidates insurance narratives", "Informal is always legal if friendly", "FSIC is optional decor", "Inspectors never check paperwork", "Formal compliance protects stakeholders.", RA + CRS),
]

NFPA72_CORES = [
    _mcq("what dual families does NFPA 72 standardize per common teaching?", "Fire alarm systems and emergency communications systems—not residential toy-only scopes alone", "Plumbing slopes only", "Bridge welding only", "Aircraft composites only", "Scope clarifies ECS + FA.", NFPA),
    _mcq("what does addressable initiation uniquely provide?", "Device-level identification on loops for pinpoint troubleshooting", "No panel map at all", "Identical anonymous contacts only", "Guarantee wireless without security", "Addressing beats zone-only granularity for large sites.", CRS + NFPA),
    _mcq("what limitation defines conventional zoning versus addressable fidelity?", "Zone tells section alarm—not always individual device identity", "Every device is always uniquely digital historically", "Zones cannot annunciate", "All tones must be identical", "Pedagogical contrast matters.", CRS + NFPA),
    _mcq("why synchronize visible notification appliances in some accessibility contexts?", "Reduce confusion or seizure-risk from uncoordinated flash fields in view", "Synchronization never matters", "Strobes must be random-phase always", "Only hearing loss scenarios exist", "ECS chapters coordinate accessibility.", CRS + NFPA),
    _mcq("what do battery calculations for FACP demonstrate?", "Standby and alarm operation duration must be engineered for AC loss", "Batteries are decorative", "Any car battery suffices", "Unlimited runtime without math", "NFPA mandates duration classes—verify edition.", CRS + NFPA),
    _mcq("what must notification appliance circuits engineer beyond ‘ copper runs’ ?", "Supervision class, synchronization, voltage drop, SPL coverage methods", "Only patch panel tonnage", "No supervision permitted", "Only consumer audio taps", "NAC engineering is richer than pulling wire.", CRS + NFPA),
    _mcq("what is a pedagogical contrast for Class A vs Class B pathways?", "Class A offers redundant pathway return varieties in classic teaching—confirm edition wording", "They are identical always", "Class B forbids supervision", "Class A means Wi-Fi mesh only", "Students must track edition definitions.", NFPA + CRS),
    _mcq("what is the role of duct smoke detection in ECS/FA coordination?", "Detect smoke movement via HVAC—not a universal substitute for area detection", "Replace all spot detectors", "Delete manual stations", "Only measure humidity", "Application-specific tool.", NFPA + CRS),
    _mcq("what is a classroom point on CO detection where adopted?", "CO appliances address colorless/odorless poisoning risk—placement and listing govern", "CO detectors replace FA entirely", "CO is irrelevant indoors", "CO requires no listing", "Selective adoption by jurisdiction.", CRS + NFPA),
    _mcq("what is the difference between alarm, supervisory, and trouble signals conceptually?", "Alarm=emergency presence; supervisory=off-normal equipment; trouble=system fault", "They are identical tones always", "Trouble means imminent fire always", "Supervisory means evacuation now always", "Signal taxonomy drives response.", NFPA + CRS),
    _mcq("why are voice-evac messages prioritized over background audio in design thought?", "Intelligibility and code-driven override of non-emergency programming", "Background music always wins", "Paging never needs backup", "STI is irrelevant", "ECS prioritization is engineered.", NFPA + CRS),
    _mcq("what is mass notification layered with fire alarm in some campuses?", "Broader crisis comms beyond fire—still requires integration discipline and listing awareness", "It deletes fire alarm entirely", "It is consumer SMS only without design", "It bans strobes always", "MNS intersects ECS chapters in modern study.", CRS + NFPA),
    _mcq("why might ground-fault isolation be taught on loops?", "Legs can fail to earth; isolation helps maintain continuity on remaining segments per design", "Ground faults improve detection", "Isolation removes all supervision", "Ground faults are irrelevant on digital loops", "Ground integrity is NFPA vocabulary.", NFPA + CRS),
    _mcq("what is walk test mode used for pedagogically?", "Technician verification of initiation/notification without full occupant evacuation panic", "Replace annual inspection wholly", "Disable batteries forever", "Silence AHJ mandates", "Walk test supports commissioning.", CRS + NFPA),
    _mcq("why might cyber-hardening appear in lecture notes about modern panels?", "Networked FACP/NIC interfaces introduce attack surfaces—segmentation matters", "Panels are air-gapped always in reality", "Password ‘admin’ is best practice", "Cyber is never part of FA", "Modern systems network to central stations.", CRS + NFPA),
]


SECTION_CORES: dict[str, list] = {
    "orient": ORIENT_CORES,
    "aux": AUX_CORES,
    "xmit": XMIT_CORES,
    "cabling": CABLING_CORES,
    "bflec": BFLEC_CORES,
    "pd1096": PD1096_CORES,
    "ra9514": RA9514_CORES,
    "nfpa72": NFPA72_CORES,
}


def tuples_for_section(section: str, target: int) -> list[tuple]:
    cores = SECTION_CORES[section]
    return interleave_unique(cores, STEM_FRAMES, target)
