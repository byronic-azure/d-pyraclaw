# PyraClaw Stealth Sovereign Runtime
## Security-First | Safety-Only | Exponentiated Orders

```
+==============================================================================+
|  PYRACLAW STEALTH SOVEREIGN RUNTIME                                          |
|  Security-First. Safety-Only. No Exceptions.                                 |
|  Sovereign Guard: QDP-SOC2-PRINCE2/Agile Hybrid                             |
|  Only Byron Callaghan (ORCID: 0009-0001-9561-5483) can override.            |
|  Patent: PCT/EP2025/080977 | US 19/541,276                                  |
+==============================================================================+
```

---

## Principle: Security First, Safety Only

Every layer, every service, every agent action passes through the Sovereign Guard
before execution. The order is absolute:

```
SECURITY CHECK -> COMPLIANCE CHECK -> SAFETY CHECK -> EXECUTE -> EVIDENCE SEAL
       |                 |                 |                          |
       +--- Any fail? ---+--- STOP. ------+--- NO EXECUTION. ------+
```

No agent can bypass this. No configuration can disable it. No API call can override it.
The only human authority is ORCID `0009-0001-9561-5483` (Byron Callaghan).

---

## 8-Layer Architecture (Stealth Build Plan Integration)

| Layer | Service | Port | Security Gate | Stealth Rule |
|-------|---------|------|---------------|-------------|
| **0** | **Sovereign Guard** | 9090 | ROOT AUTHORITY | Overrides everything |
| **1** | Freedom Engine | 8001 | 7-axiom governance | Freedom decides before swarm |
| **2** | iAiA Orchestrator | 8002 | Task decomposition | Stealth mode: neutral naming |
| **3** | Engine Adapter (b0140) | 8003 | Sealed boundary | b0140 NEVER called raw |
| **4** | RAG Gateway | 8004 | Source provenance | HTML via RAG, not direct dump |
| **5** | Swarm Manager | 8005 | Worker isolation | Workers cannot deploy directly |
| **6** | RSFS Core | 8006 | 8-dimension gate | Measurable, not rhetorical |
| **7** | Deploy Gate | 8007 | Promotion criteria | Every deploy has rollback |
| **8** | Evidence Ledger | 8009 | QDP 4-layer seal | Every action has proof |

### Layer 0 — Sovereign Guard (NEW: Super Script)

The Sovereign Guard sits above all 8 layers. It:
- Intercepts every agent action via `/api/guard/intercept`
- Enforces QDP 4-layer hashing on every payload
- Enforces RSFS 8-dimension gate on every output
- Blocks 14 protected actions without sovereign ORCID
- Maintains immutable audit log
- Generates SOC 2 / SOC 3 / GDPR / EU AI Act compliance reports

```
                    +-------------------+
                    | SOVEREIGN GUARD   |  Layer 0
                    | (Super Script)    |  Root authority
                    | Port 9090         |  Cannot be bypassed
                    +--------+----------+
                             |
              +--------------+--------------+
              |                             |
    +---------v---------+         +---------v---------+
    | Freedom Engine    |         | Evidence Ledger   |
    | (Constitutional)  |         | (Proof Chain)     |
    | Port 8001         |         | Port 8009         |
    +--------+----------+         +-------------------+
             |
    +--------v----------+
    | iAiA Orchestrator  |
    | Port 8002          |
    +--------+-----------+
             |
    +--------v----------+    +------------------+    +------------------+
    | b0140 Adapter     |--->| RAG Gateway      |--->| Swarm Manager    |
    | Port 8003         |    | Port 8004        |    | Port 8005        |
    +-------------------+    +------------------+    +--------+---------+
                                                              |
                                                     +--------v---------+
                                                     | RSFS Core        |
                                                     | Port 8006        |
                                                     +--------+---------+
                                                              |
                                                     +--------v---------+
                                                     | Deploy Gate      |
                                                     | Port 8007        |
                                                     +------------------+
```

---

## Stealth-Mode Rules (From Build Plan)

These rules are IMMUTABLE. They are enforced by the Sovereign Guard.

| # | Rule | Enforcement |
|---|------|-------------|
| 1 | No public claims before metrics exist | Sovereign Guard blocks `publish` without evidence |
| 2 | No references to live 100k swarm unless measured | RSFS dimension check required |
| 3 | b0140 hash stays internal to adapter | Sovereign Guard blocks `export_source_code` |
| 4 | Deploy via feature flags and canaries | Deploy Gate enforces canary before full rollout |
| 5 | Neutral internal naming in commits | Code review gate |
| 6 | Isolate experimental from public | Network policy enforces mesh boundaries |
| 7 | Freedom decides before swarm activation | Freedom Engine must PASS before swarm spawns |
| 8 | Workers cannot deploy directly | Swarm Manager enforces integration queue |
| 9 | Every merge carries provenance + rollback | Evidence Ledger seals every merge |
| 10 | RSFS is measurable, not rhetorical | Real scores, real thresholds, real gates |

---

## Quad-Core Embedded Safety

Four compliance frameworks embedded at the architecture level:

### Core 1: QDP (Cryptographic)
```
Payload -> SHA-256 -> SHA-512 -> SHA3-256 -> SHA3-512 -> Capsule
```
- 4 independent hash algorithms
- All 4 must verify
- Cannot be disabled (Sovereign Guard enforced)
- Patent-protected: PCT/EP2025/080977

### Core 2: SOC 2 Type II (Operational)
```
CC1 Control Environment      -> Freedom Engine + Sovereign Guard
CC2 Communication            -> 44-channel neural mesh + QDP routing
CC3 Risk Assessment          -> RSFS 8-dimension scoring
CC4 Monitoring               -> Prometheus + Grafana + OTel
CC5 Control Activities       -> Deploy Gate + Sovereign Guard
CC6 Access Controls          -> Zero-trust + ORCID-gated
CC7 System Operations        -> Docker healthchecks + circuit breakers
CC8 Change Management        -> PRINCE2 gates + QDP per change
CC9 Risk Mitigation          -> Fail-closed on any breach
```

### Core 3: GDPR (Data Protection)
```
Art 5  Lawfulness            -> Evidence capsule per output
Art 5  Purpose limitation    -> Scope Definition (Gate G5)
Art 5  Data minimisation     -> Sovereign mesh, no leakage
Art 5  Accuracy              -> RSFS correctness >= 0.85
Art 5  Storage limitation    -> Configurable retention
Art 5  Integrity             -> QDP + zero-trust + encryption
Art 25 By design             -> Compliance in architecture
Art 30 Records               -> Evidence Ledger permanent log
Art 35 DPIA                  -> RSFS security + compliance dimensions
```

### Core 4: EU AI Act (Regulatory)
```
Art 9  Risk management       -> RSFS fail-closed gate
Art 10 Data governance       -> QDP integrity + sovereign mesh
Art 11 Technical docs        -> 8-file evidence capsule + Zenodo
Art 12 Record-keeping        -> Evidence Ledger audit trail
Art 13 Transparency          -> Rationale + agent trace + route map
Art 14 Human oversight       -> RSFS HOLD gate + Sovereign Guard
Art 15 Accuracy/robustness   -> QDP + circuit breakers + canary
```

---

## PRINCE2/Agile Hybrid Execution

### PRINCE2 Controls (Strategic)

| Control | PyraClaw Implementation |
|---------|------------------------|
| Business Case | Evidence product revenue model + beta network |
| Organisation | Sovereign Owner (Byron) + Agent Pyramid |
| Quality | RSFS 8-dimension scoring + quality register |
| Plans | Stage gates: Pre-Seed > Seed > Series A |
| Risk | Sovereign Guard risk interception |
| Change | Deploy Gate promotion criteria |
| Progress | Sprint reviews + evidence capsule per sprint |

### Agile Execution (Tactical)

| Element | Implementation |
|---------|---------------|
| Sprint | 2-week cycles |
| Backlog | Prioritised by RSFS impact scores |
| Daily standup | Agent swarm status report |
| Review | Demo + evidence capsule |
| Retro | RSFS feedback loop analysis |
| Definition of Done | QDP sealed + RSFS PASS + compliance gates green |

### Hybrid Integration

```
PRINCE2 Stage Gate
    |
    v
Sprint Planning (Agile)
    |
    v
Daily Execution (Swarm Manager)
    |
    v
RSFS Quality Gate (Every output)
    |
    v
QDP Evidence Seal (Every output)
    |
    v
Deploy Gate (Canary + rollback)
    |
    v
Sprint Review (Evidence capsule)
    |
    v
PRINCE2 Stage Review (Milestone check)
```

---

## Non-Negotiables (From Stealth Build Plan)

1. Freedom decides before swarm activation
2. b0140 is wrapped and never called raw from the UI
3. Assets enter through RAG and component extraction, not direct production dump
4. Every deploy includes provenance, tests, and rollback
5. RSFS is measurable, not rhetorical
6. No public claims before metrics exist
7. Sovereign Guard cannot be disabled by any agent
8. Only ORCID 0009-0001-9561-5483 authorises protected operations

---

## Exponentiated Orders

The system scales through the pyramid, not through direct human intervention:

```
1 Command from Byron
    -> 1 Sovereign Guard check
        -> 1 Freedom Engine evaluation
            -> 3 Ultra Agents decompose
                -> 9 Spectacular Agents research
                    -> 9 Super Agents execute
                        -> 12 Execution Agents deliver
                            -> 4 Frequency Agents monitor
                                -> 9 Mesh Agents route

1 input -> 44 parallel agents -> exponential output
All sealed. All scored. All proven.
```

---

*DD7 International GmbH | PyraClaw Stealth Sovereign Runtime v1.0*
*Security-first. Safety-only. No overclaiming. No exceptions.*
*Patent: PCT/EP2025/080977 | US 19/541,276 | ORCID: 0009-0001-9561-5483*
