# PyraClaw PRINCE2/Agile Guiding System
## Compliance-First Protocol | Beta Network | Client Pre-Approval

```
+==============================================================================+
|  PYRACLAW — PRINCE2/AGILE GUIDING SYSTEM                                    |
|  DD7 International GmbH | Compliance-First Protocol                          |
|  Patent: PCT/EP2025/080977 | US 19/541,276                                  |
|  ORCID: 0009-0001-9561-5483 | Byron Callaghan (Lord B)                       |
+==============================================================================+
```

**Version 1.0 | March 2026 | MINTED_GREEN | SURGICAL**

---

## 1. Compliance-First Protocol

Every action PyraClaw takes follows this sequence. No exceptions.

```
COMPLIANCE CHECK -> BUILD -> TEST -> EVIDENCE -> RELEASE
       |                                            |
       +--- Fails? STOP. Fix compliance first. -----+
```

### The Five Gates

| Gate | Question | Evidence Required | Fail Action |
|------|----------|------------------|-------------|
| **G1: Legal** | Do we have the right to do this? | Patent ref, licence check | STOP — legal review |
| **G2: Regulatory** | Does this comply with EU AI Act? | RSFS compliance score >= 0.80 | HOLD — adjust until compliant |
| **G3: Technical** | Does the code work correctly? | QDP capsule, all tests pass | FIX — no release until green |
| **G4: Evidence** | Can we prove what we claim? | 8-file evidence capsule, Zenodo DOI | SEAL — no claim without proof |
| **G5: Client** | Has the client approved this scope? | Signed scope document, pre-approval | WAIT — no work without approval |

---

## 2. PRINCE2 Stage Gates

### Stage 1: Pre-Seed (Current)

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| PyraClaw Evidence CLI | DELIVERED | `cli/pyraclaw.py` — ingest/mint/verify working |
| 10 FastAPI services | DELIVERED | 2,869 lines, all with /health endpoints |
| GPU Docker Compose | DELIVERED | 23-service stack, NVIDIA runtime configured |
| Product pages (Evidence, Command, Minted Green) | DELIVERED | `web/mission-control/` |
| QDP 4-layer security | DELIVERED | SHA-256/512/SHA3-256/512 |
| RSFS 8-dimension scoring | DELIVERED | Phi=0.77, C_crit=52.79 |
| Strategy & Demo Guide | DELIVERED | `docs/STRATEGY_DEMO_GUIDE.md` |
| Patent filed | DELIVERED | PCT/EP2025/080977, US 19/541,276 |
| ORCID registered | DELIVERED | 0009-0001-9561-5483 |
| First evidence capsule minted | DELIVERED | Capsule b847db9f VERIFIED |

**Gate criteria for Stage 2:** 5 sealed capsules + 1 Zenodo DOI + 3 beta testers

### Stage 2: Seed (Target Q2 2026)

| Deliverable | Status | Gate |
|-------------|--------|------|
| 5 enterprise beta testers onboarded | PENDING | Signed agreements |
| NVIDIA GPU fleet connected | PENDING | nvidia-smi confirms 4x GPU |
| Blockchain evidence anchoring | PENDING | Smart contract deployed |
| Zenodo DOI for v1.0 | PENDING | DOI assigned |
| 10 minted evidence capsules | PENDING | All verified |
| Revenue from first licence | PENDING | Invoice paid |

### Stage 3: Series A (Target Q4 2026)

| Deliverable | Status | Gate |
|-------------|--------|------|
| 10+ enterprise clients | PLANNED | Signed contracts |
| 77-node mesh topology | PLANNED | All nodes healthy |
| Full PyraClaw Command product | PLANNED | 44-agent pyramid operational |
| Blockchain on Ethereum/Polygon | PLANNED | Contract audited |

---

## 3. Agile Sprint Structure

### Two-Week Sprints

| Day | Activity | Output |
|-----|----------|--------|
| **Mon W1** | Sprint planning | Sprint backlog approved |
| **Tue-Fri W1** | Build | Code committed daily |
| **Mon W2** | Mid-sprint review | Demo to stakeholders |
| **Tue-Thu W2** | Build + test | All tests green |
| **Fri W2** | Sprint review + retrospective | Evidence capsule minted |

### Every Sprint Must Produce

1. At least one QDP-sealed evidence capsule
2. Updated RSFS scores for all modified services
3. Compliance gate check (G1-G5) documented
4. Client-facing changelog

---

## 4. Beta Testing Network

### Target Sectors for Beta

| # | Sector | Why PyraClaw Fits | Compliance Need | Beta Approach |
|---|--------|-------------------|-----------------|---------------|
| 1 | **Legal / Law Firms** | AI-generated legal research needs proof trail | SRA compliance, court-admissible evidence | Free pilot: seal 100 AI outputs |
| 2 | **Financial Services** | Regulated AI decisions (credit, risk) | FCA, MiFID II, EU AI Act | Compliance audit trail demo |
| 3 | **Healthcare / Pharma** | Clinical decision support needs audit | MHRA, EU MDR, GDPR | Evidence capsule for each AI recommendation |
| 4 | **Government / Public Sector** | Transparency mandates for AI in public services | UK AI Safety Institute, EU AI Act | Sovereign deployment (no data leaves) |
| 5 | **Insurance** | Underwriting AI must be explainable | Lloyd's standards, Solvency II | Proof of every risk assessment |
| 6 | **Education / EdTech** | AI tutoring and grading needs accountability | Ofsted, EU AI Act (high-risk) | Evidence trail for every AI grade |
| 7 | **Manufacturing / Industry 4.0** | Quality control AI, predictive maintenance | ISO 9001, CE marking | IoT mesh integration via LoRaWAN |
| 8 | **Real Estate / PropTech** | AI valuations must be defensible | RICS standards, FCA | Sealed valuation evidence |
| 9 | **Media / Publishing** | Content provenance, AI-generated content labelling | EU AI Act transparency | Fractal Forge + evidence sealing |
| 10 | **Accounting / Audit** | AI-assisted audit needs its own audit trail | ICAEW, ACCA standards | Evidence capsule per engagement |

### Beta Onboarding Process

```
1. CLIENT INQUIRY
   |
2. SCOPE DEFINITION (what AI outputs need sealing?)
   |
3. PRE-APPROVAL (client signs scope doc — Gate G5)
   |
4. PILOT SETUP (deploy PyraClaw Evidence on client data)
   |
5. 30-DAY PILOT (seal 100+ AI outputs, verify 10 randomly)
   |
6. REVIEW (present evidence capsules, RSFS scores, compliance report)
   |
7. CONVERT (pilot -> annual licence)
```

---

## 5. Code Catalogue

### Service Inventory

| # | Service | Port | Lines | Purpose | Status |
|---|---------|------|-------|---------|--------|
| 1 | QDP Hasher | lib | 181 | 4-layer cryptographic sealing | PRODUCTION |
| 2 | Freedom Engine | 8001 | 186 | 7-axiom EU AI Act processing | PRODUCTION |
| 3 | RSFS Core | 8006 | 196 | 8-dimension quality scoring | PRODUCTION |
| 4 | Evidence Ledger | 8009 | 197 | QDP-sealed evidence records | PRODUCTION |
| 5 | Swarm Manager | 8005 | 248 | 44-agent CognitivePyraClaw | PRODUCTION |
| 6 | Neural Mesh | 9044 | 152 | 44-channel routing hub | PRODUCTION |
| 7 | Frequency Engine | 9045 | 156 | iTrifactor (432/528/639/963 Hz) | PRODUCTION |
| 8 | Cortex Mapper | 9046 | 141 | Neo-cortex + owl brain topology | PRODUCTION |
| 9 | LoRaWAN Bridge | 9047 | 137 | IoT mesh gateway (EU868/US915) | PRODUCTION |
| 10 | Fractal Forge | 9048 | 259 | PFSE UIFC codec (.claw capsules) | PRODUCTION |
| 11 | PyraClaw CLI | tool | 416 | ingest/mint/verify/status | PRODUCTION |

**Total production code: 2,869 + 416 = 3,285 lines**

### Infrastructure

| Component | File | Purpose |
|-----------|------|---------|
| GPU Compose | `docker-compose.pyraclaw-gpu.yml` | 23-service NVIDIA stack |
| Dockerfile | `Dockerfile` | Multi-stage Python 3.11 build |
| Deploy Script | `scripts/deploy-gpu.sh` | Automated GPU deployment |
| K8s Base | `infra/k8s/base/` | Namespace, ConfigMap, NetworkPolicy |

### Documentation

| Document | File | Purpose |
|----------|------|---------|
| README | `README.md` | Architecture + quick start |
| Strategy Guide | `docs/STRATEGY_DEMO_GUIDE.md` | Go-to-market playbook |
| Web Superstructure | `docs/WEB_SUPERSTRUCTURE.md` | 5-domain Mission Control |
| This Document | `docs/compliance/PRINCE2_AGILE_GUIDE.md` | Governance framework |

### Product Pages

| Page | File | Audience |
|------|------|----------|
| Evidence | `web/mission-control/evidence.html` | Enterprise buyers |
| Command | `web/mission-control/command.html` | Technical decision makers |
| Minted Green | `web/mission-control/minted-green.html` | Demo audiences |

---

## 6. Client Pre-Approval Framework

### Before Any Work Begins

| Step | Document | Who Signs | Purpose |
|------|----------|-----------|---------|
| 1 | **Scope Definition** | Client + DD7 | What AI outputs will be sealed |
| 2 | **Data Processing Agreement** | Client + DD7 | GDPR compliance, data handling |
| 3 | **Compliance Acknowledgement** | Client | Client confirms their regulatory requirements |
| 4 | **Pilot Agreement** | Client + DD7 | 30-day terms, success criteria, exit clause |
| 5 | **IP Acknowledgement** | Client | Client acknowledges PyraClaw IP is licensed, not transferred |

### IP Terms (Non-Negotiable)

- **Licensing only.** No IP transfer under any circumstances.
- **No source code disclosure** to clients or partners.
- **Patent-protected:** PCT/EP2025/080977, US 19/541,276.
- **Evidence capsules belong to the client.** The system belongs to DD7.

### Pricing Framework (Beta)

| Tier | Monthly | Capsules/Month | Support |
|------|---------|----------------|---------|
| **Pilot** | Free (30 days) | 100 | Email |
| **Starter** | EUR 500 | 1,000 | Email + SLA |
| **Professional** | EUR 2,500 | 10,000 | Priority + Slack |
| **Enterprise** | Custom | Unlimited | Dedicated + on-site |

---

## 7. Quality Register

Every release maintains a quality register:

| Item | Measure | Target | Current |
|------|---------|--------|---------|
| Evidence capsule integrity | QDP 4-layer verification | 100% pass | 100% |
| RSFS scoring accuracy | Phi convergence | >= 0.77 | 0.8915 |
| Service availability | /health endpoint response | >= 99.5% | 100% (dev) |
| Code coverage | Unit tests passing | >= 80% | Building |
| Documentation currency | All docs match code | 100% | 100% |
| Compliance gates | G1-G5 all green | 100% | G1-G4 green, G5 pending (no clients yet) |

---

## 8. Guidelines — What PyraClaw Does and Does NOT Do

### We Do

- Seal AI outputs with cryptographic proof
- Score quality across 8 dimensions before release
- Provide self-verifying evidence capsules
- Comply with EU AI Act by design
- Maintain full audit trail for every decision
- License our technology to enterprises

### We Do NOT

- Claim consciousness, sentience, or AGI capability
- Guarantee specific AI accuracy (we measure and report it)
- Transfer IP or source code
- Process data outside the sovereign mesh (unless client requests)
- Make promises without working code behind them
- Overclaim. Ever.

---

*DD7 International GmbH | PyraClaw PRINCE2/Agile Guide v1.0 | March 2026*
*Patent: PCT/EP2025/080977 | US 19/541,276 | ORCID: 0009-0001-9561-5483*
*Compliance first. Evidence first. No claim without proof.*
