# PyraClaw Sovereign AI Runtime

**MINTED_GREEN | SURGICAL | GPU x4 | 44-Channel Neural Mesh**

DD7 International GmbH | Patent: PCT/EP2025/080977 | US 19/541,276 | ORCID: 0009-0001-9561-5483

---

## Architecture

22-service sovereign AI runtime with NVIDIA GPU acceleration, 44-channel neural mesh, and QDP cryptographic evidence sealing.

### Service Stack

| Port | Service | Function |
|------|---------|----------|
| 19000-19002 | NemoClaw x3 | GPU inference (NVIDIA H200/B200) |
| 19080 | NemoClaw Router | Load balancer |
| 8001 | Freedom Engine | 7-axiom EU AI Act aligned processing |
| 8002 | Orchestrator | Task routing and pipeline execution |
| 8003 | Engine Adapter | Sealed runtime boundary |
| 8004 | RAG Gateway | Hybrid search with reranking |
| 8005 | Swarm Manager | 44-agent CognitivePyraClaw pyramid |
| 8006 | RSFS Core | 8-dimension recursive self-feedback scoring |
| 8007 | Deploy Gate | Release promotion, canary, rollback |
| 8009 | Evidence Ledger | QDP-sealed evidence records |
| 9044 | Neural Mesh | 44-channel nodal routing hub |
| 9045 | Frequency Engine | iTrifactor (432/528/639/963 Hz) |
| 9046 | Cortex Mapper | Neo-cortex + owl brain topology |
| 9047 | LoRaWAN Bridge | IoT mesh gateway (EU868/US915) |
| 9048 | Fractal Forge | PFSE UIFC codec (.claw capsules) |
| 3000 | Mission Control | Unified dashboard |

### Infrastructure

PostgreSQL (pgvector), Qdrant, Redis, Prometheus, Grafana, OpenTelemetry

## Quick Start

```bash
# CPU (development)
cp .env.example .env
docker compose up -d --build

# GPU (production)
docker compose -f docker-compose.pyraclaw-gpu.yml up -d --build
```

## Security

Every output sealed with the Quadruple-Dipped Protocol (QDP):
1. SHA-256 (NIST FIPS 180-4)
2. SHA-512 (doubled digest)
3. SHA3-256 (Keccak, quantum-ready)
4. SHA3-512 (sovereign maximum)

All four must match. One failure = full rejection.

## EU AI Act Compliance

- Transparency: all decisions logged with rationale
- Human oversight: RSFS gate requires review for HOLD/FAIL
- Robustness: circuit breakers, canary deploys, rollback
- Audit trail: QDP capsule for every output

## No Overclaiming

This system provides computational services. It does not claim consciousness, quantum supremacy, or capabilities beyond what the code implements. Every claim is backed by running code and verifiable evidence.

---

*DD7 International GmbH | Byron Callaghan (Lord B) + Jan Esderts*
