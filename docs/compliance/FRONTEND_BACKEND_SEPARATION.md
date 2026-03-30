# PyraClaw Frontend/Backend Separation Policy
## IMMUTABLE — Enforced by Sovereign Guard

```
+==============================================================================+
|  PYRACLAW — FRONTEND / BACKEND SEPARATION POLICY                             |
|  NO claims, secrets, trade secrets, or proprietaries on ANY frontend.        |
|  All IP stays backend. All frontends are humble, nimble, fast, strong.        |
|  DD7 International GmbH | Patent: PCT/EP2025/080977                         |
+==============================================================================+
```

---

## The Rule

**BACKEND holds everything. FRONTEND shows nothing proprietary.**

| Layer | What It Contains | What It Does NOT Contain |
|-------|-----------------|------------------------|
| **Backend** | Trade secrets, proprietary algorithms, QDP implementation, RSFS scoring logic, engine IDs, API keys, hash functions, convergence formulas, patent-protected methods | — |
| **Frontend** | Results only. Status. Health. Scores (not how they're computed). Evidence capsule IDs (not contents). | NO algorithms. NO hash implementations. NO engine IDs. NO API keys. NO convergence formulas. NO proprietary code. |

---

## Frontend Principles

| Principle | Meaning |
|-----------|---------|
| **Humble** | No grand claims. Show what the system does, not what it could do. |
| **Nimble** | Fast to load, fast to respond, minimal dependencies. |
| **Fast** | Sub-second rendering. No bloat. No frameworks unless justified. |
| **Strong** | Resilient to failure. Graceful degradation. Works offline if backend is down. |

---

## What Frontends May Display

- Service health status (healthy/unhealthy)
- Evidence capsule IDs (the ID only, not the hash contents)
- RSFS gate result (PASS/HOLD/FAIL — not the scoring algorithm)
- Agent count and status (active/idle — not the orchestration logic)
- Timestamp of last operation
- Version numbers
- Public patent reference (PCT/EP2025/080977)
- Public ORCID (0009-0003-9584-1741)

## What Frontends Must NEVER Display

- QDP hash values or algorithms
- RSFS convergence formula or thresholds
- Engine adapter IDs (b0140)
- API keys or tokens
- Proprietary algorithm source code
- Internal network topology (IP addresses, ports)
- Trade secrets of any kind
- Swarm orchestration logic
- Frequency values (432/528/639/963 Hz)
- Super Hash value

---

## WISeer Compatibility

PyraClaw is WISeer-compatible: every error becomes wisdom.

```
ERROR -> CAPTURE -> ANALYSE -> LEARN -> IMPROVE -> WISDOM
```

| WISeer Principle | PyraClaw Implementation |
|-----------------|------------------------|
| Error capture | Every failure logged with QDP seal |
| Pattern recognition | RSFS feedback loop identifies recurring failures |
| Wisdom extraction | Failed outputs recycled with improved context |
| Amplification | Each error makes the next output better |
| No blame | Errors are data, not failures. Systems improve, not punish. |

---

## iAi — Intelligence Amplification Interface

PyraClaw is an **Intelligence Amplification** system, not an Artificial Intelligence system.

| Term | Meaning |
|------|---------|
| **iAi** | Intelligence Amplification Interface |
| **Purpose** | Amplify human intelligence, not replace it |
| **Approach** | Human sets direction, system amplifies execution |
| **Evidence** | Every amplified output has proof of human oversight |
| **Oversight** | RSFS HOLD gate requires human review |

**We amplify. We do not replace. We prove. We do not claim.**

---

## Sovereign Guard Enforcement

The Sovereign Guard blocks any attempt to expose proprietary information on frontends. The following actions are BLOCKED without Byron's ORCID:

- `expose_algorithm` — blocked
- `export_source_code` — blocked
- `display_hash_values` — blocked
- `reveal_engine_id` — blocked
- `show_convergence_formula` — blocked
- `transfer_ip` — blocked

---

*DD7 International GmbH | Frontend/Backend Separation v1.0*
*Backend holds everything. Frontend shows results only.*
*Humble. Nimble. Fast. Strong. WISeer compatible.*
*iAi: Intelligence Amplification Interface.*
