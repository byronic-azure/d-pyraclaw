# PyraClaw Strategy & Demo Guide
## Go-To-Market Playbook | v1.0.0

```
+==============================================================================+
|  PYRACLAW — STRATEGY & DEMO GUIDE                                            |
|  DD7 International GmbH | MINTED_GREEN | SURGICAL                            |
|  Patent: PCT/EP2025/080977 | US 19/541,276                                  |
|  ORCID: 0009-0001-9561-5483 | Byron Callaghan (Lord B)                       |
+==============================================================================+
```

---

## 1. Strategic Focus: Evidence Product First

PyraClaw ships two core products. The order matters.

### Product 1: PyraClaw Evidence (Lead Product)

**What it is:** A sovereign evidence minting system that seals every AI output with
cryptographic proof — four independent hash layers, RSFS quality scoring, and optional
blockchain anchoring.

**Why it leads:**
- Regulatory demand is immediate (EU AI Act enforcement begins 2026)
- Every enterprise AI buyer asks: "Can you prove what your AI did?"
- Evidence is the trust primitive — once trust exists, everything else sells
- Low hardware barrier — runs on CPU, scales to GPU
- Zenodo DOI integration gives academic credibility from day one

**Positioning:** "The notary for AI decisions."

### Product 2: PyraClaw Command (Follow-On)

**What it is:** The 44-agent CognitivePyraClaw swarm with Mission Control dashboard,
neural mesh routing, and Fractal Synthesis Engine.

**Why it follows:**
- Command requires Evidence to function (every agent output gets sealed)
- Higher hardware requirements (GPU, Groq LPU)
- Longer sales cycle (enterprise integration)
- More impressive demo, but Evidence closes deals first

**Positioning:** "The department you hire, not the employee."

---

## 2. The iAiA Repository Strategy

### byronic-azure/iAiA

The iAiA repository powers the agent swarm behind PyraClaw. It is the open-source
intelligence layer that:

- Orchestrates multi-agent task routing via OwlMind
- Manages inference flows across NemoClaw instances
- Provides the ClawSync mesh for inter-agent communication
- Emits QDP-compatible inputs.json/outputs.json for evidence sealing

### Integration Flow

```
iAiA Repository (Agent Core)
      |
      v
PyraClaw Runtime (Evidence + Command)
      |
      +---> Evidence Product: QDP seal + Zenodo DOI + blockchain anchor
      |
      +---> Command Product: Mission Control + 44-channel mesh + PFSE
```

### How Agents Contribute to Evidence

Every iAiA agent emits structured output in QDP format:
1. `inputs.json` — what the agent received
2. `outputs.json` — what the agent produced
3. `digests.json` — 4-layer hash of inputs + outputs
4. `signature.json` — ORCID-linked attestation
5. `verify.sh` — standalone verification script
6. `node_trace.json` — which agents participated
7. `route_map.json` — how the task flowed through the mesh
8. `manifest.json` — master capsule linking all 7 files

---

## 3. Phased Roadmap

| Phase | Product | Focus | Gate |
|-------|---------|-------|------|
| **1 — Now** | Evidence MVP | QDP sealing, RSFS scoring, Zenodo DOI | 5 sealed capsules + 1 DOI |
| **2 — Q2 2026** | Evidence + Demo | Minted Green demo, product pages, investor deck | Live demo server |
| **3 — Q3 2026** | Command Beta | 44-agent swarm, Mission Control, PFSE | 3 enterprise pilots |
| **4 — Q4 2026** | Full Platform | GPU fleet, blockchain anchoring, 77-node mesh | First revenue |

---

## 4. Demo Playbook

### Demo 1: Minted Green (Evidence Product)

**Duration:** 5 minutes
**Audience:** Investors, enterprise buyers, regulators

**Script:**
1. Show a high-resolution RAW photograph (architectural shot, 16-bit TIFF)
2. Run `pyraclaw ingest photo.tiff` — iAiA decomposes into fractal components
3. Run `pyraclaw mint output.claw` — FSE synthesises + QDP seals
4. Show the evidence capsule: 8 JSON files, each with 4-layer hash
5. Show the .claw file size (100KB vs 50MB original)
6. Zoom to 500% — no artefacts, no blockiness, infinite resolution
7. Show the Zenodo DOI link — permanent, citable, auditable
8. Show the blockchain transaction — immutable proof of existence

**Key message:** "Every AI output your company produces can have this level of proof.
Not a promise — a running system."

### Demo 2: Evidence Viewer (Trust Demo)

**Duration:** 3 minutes
**Audience:** CTOs, compliance officers

**Script:**
1. Open the Evidence Room web interface
2. Select any sealed capsule
3. Show the 4-layer hash verification (all green)
4. Show the RSFS scores across 8 dimensions
5. Click "Verify" — runs the standalone verify.sh in real-time
6. Show the audit trail: who, when, what, why

**Key message:** "Your auditors and regulators can verify any AI decision
without calling us. The proof is self-contained."

### Demo 3: iAiA Agent Integration (Technical Demo)

**Duration:** 10 minutes
**Audience:** Engineering teams, CTOs

**Script:**
1. Show the iAiA repository structure
2. Create a simple agent (style transfer model)
3. Run it as a pre-processing node in the FSE pipeline
4. Show the agent's outputs being QDP-sealed automatically
5. Show the route_map.json — which agents touched the data
6. Show the ClawSync mesh status with 44 channels active

**Key message:** "Your existing AI models plug into PyraClaw.
Every model output gets evidence-grade proof automatically."

---

## 5. Narrative Discipline

### What We Say

- "Sovereign AI with built-in proof"
- "Every output has a receipt"
- "Resolution-independent fractal compression"
- "EU AI Act compliant by design"
- "44 agents, one command"
- "Evidence first, always"

### What We Do NOT Say

- No claims of consciousness or sentience
- No claims of quantum supremacy (quantum-inspired, not quantum computing)
- No claims that LoRaWAN/radio is currently deployed in hardware
- No performance claims without benchmarks
- No "we're better than OpenAI" — different category, different value
- No promises about future features without working code

### The Trust Narrative

Every conversation returns to trust:
1. Trust in AI outputs (QDP evidence)
2. Trust in quality (RSFS 8-dimension scoring)
3. Trust in provenance (ORCID + Zenodo DOI + blockchain)
4. Trust in compliance (EU AI Act alignment)
5. Trust in the team (50,000+ CTO hours, patent portfolio)

---

## 6. Product Page Structure

### Page 1: PyraClaw Evidence

**Hero:** "Every AI decision. Proven."
- What it does: 4-layer cryptographic sealing of every AI output
- How it works: QDP protocol diagram (SHA-256 > SHA-512 > SHA3-256 > SHA3-512)
- Why it matters: EU AI Act, audit trail, regulator-ready
- Evidence capsule walkthrough: 8 files explained
- CTA: "Start sealing your AI outputs today"

### Page 2: PyraClaw Command

**Hero:** "44 agents. One command."
- What it does: CognitivePyraClaw agent pyramid
- How it works: Boss > 3 Ultra > 30 Workers, orchestrated by OwlMind
- Neural mesh: 44 channels across messaging, IoT, frequency, cortex
- Fractal Forge: resolution-independent asset synthesis
- CTA: "Deploy your AI department"

### Page 3: Minted Green Demo

**Hero:** "See it. Verify it. Trust it."
- Before/after comparison: RAW photo vs .claw file
- File size comparison: 50MB TIFF > 100KB .claw (500x compression)
- Zoom comparison: JPEG artefacts vs infinite fractal resolution
- Evidence capsule breakdown: all 8 files visible
- Live verification: click to run verify.sh
- CTA: "Try the demo"

---

## 7. Brand Guidelines

| Element | Value |
|---------|-------|
| Primary colour | Midnight Blue (#0a0f1a) |
| Accent 1 | Electric Cyan (#06b6d4) |
| Accent 2 | Royal Purple (#7c3aed) |
| Success | Minted Green (#10b981) |
| Error | Signal Red (#ef4444) |
| Font (headings) | Inter 600/700 |
| Font (code) | JetBrains Mono 400/600 |
| Logo | PyraClaw glyph + wordmark |
| Badge | "Minted Green" seal on verified assets |

---

*DD7 International GmbH | PyraClaw Strategy & Demo Guide v1.0.0 | March 2026*
*Patent: PCT/EP2025/080977 | US 19/541,276 | ORCID: 0009-0001-9561-5483*
*Evidence first. No overclaiming. Results-driven.*
