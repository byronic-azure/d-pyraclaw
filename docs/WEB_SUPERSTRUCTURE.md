# PyraClaw Web Superstructure
## Mission Control Architecture | v1.0.0

```
+==============================================================================+
|  PYRACLAW WEB SUPERSTRUCTURE — MISSION CONTROL                               |
|  DD7 International GmbH | MINTED_GREEN | SURGICAL                            |
|  Patent: PCT/EP2025/080977 | US 19/541,276                                  |
|  ORCID: 0009-0009-7256-9337 | Byron Callaghan (Lord B)                       |
+==============================================================================+
```

---

## Domain Architecture

### Web 2.0 (Public-Facing) -> Web 3.0 (Sovereign Infrastructure)

```
WEB 2.0 — PUBLIC ENTRY POINTS
+------------------+     +------------------+     +------------------+
|  pyraclaw.com    |     |  pyraclaw.ai     |     |  pyraclaw.uk     |
|  Corporate Hub   |     |  AI Platform     |     |  UK Operations   |
|  Investor Deck   |     |  API Gateway     |     |  Compliance Hub  |
|  Documentation   |     |  Model Registry  |     |  EU AI Act       |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                          +-------v--------+
                          |  MISSION       |
                          |  CONTROL       |
                          |  (Unified)     |
                          +-------+--------+
                                  |
         +------------------------+------------------------+
         |                        |                        |
+--------v---------+     +--------v---------+     +--------v---------+
|  pyraclaw.xyz    |     |  pyraclaw.io     |     |  pyraclaw.ai     |
|  Web3 Sovereign  |     |  Developer API   |     |  AI Operations   |
|  Blockchain      |     |  SDK Access      |     |  Inference Hub   |
|  Evidence Mint   |     |  Documentation   |     |  Swarm Mgmt      |
+------------------+     +------------------+     +------------------+

WEB 3.0 — SOVEREIGN INFRASTRUCTURE
```

---

## Domain Roles

| Domain | Role | Stack | Audience |
|--------|------|-------|----------|
| **pyraclaw.com** | Corporate hub, investor materials, company info | Static + CMS | Investors, partners, press |
| **pyraclaw.ai** | AI platform entry, model registry, inference API | FastAPI + Next.js | Developers, enterprise customers |
| **pyraclaw.uk** | UK/EU operations, compliance, regulatory hub | Static + compliance API | Regulators, legal, UK operations |
| **pyraclaw.xyz** | Web3 sovereign layer, blockchain evidence, NFT mint | Solidity + IPFS | Web3 community, evidence verification |
| **pyraclaw.io** | Developer platform, SDK, API docs, playground | FastAPI + Docs | Developers, integrators |

---

## Mission Control — Unified Dashboard

All 5 domains resolve to a single **Mission Control** backend that routes based on domain:

```
                    +---------------------------+
                    |     NGINX / Cloudflare     |
                    |     (Domain Routing)       |
                    +------------+--------------+
                                 |
                    +------------v--------------+
                    |     PyraClaw Mission       |
                    |     Control API            |
                    |     (FastAPI :3000)        |
                    +---+--------+----------+---+
                        |        |          |
               +--------v--+ +--v------+ +-v---------+
               | Dashboard  | | API     | | Evidence  |
               | (Web UI)   | | Gateway | | Minting   |
               +------------+ +---------+ +-----------+
```

### Mission Control Pages

| Route | Domain(s) | Content |
|-------|-----------|---------|
| `/` | pyraclaw.com | Corporate landing — live service status, key metrics |
| `/platform` | pyraclaw.ai | AI platform — model selection, inference, swarm management |
| `/compliance` | pyraclaw.uk | EU AI Act status, RSFS scores, audit trail |
| `/evidence` | pyraclaw.xyz | Blockchain evidence viewer, QDP capsule browser, mint history |
| `/developers` | pyraclaw.io | API docs, SDK download, playground, code samples |
| `/mission` | All | Unified Mission Control — full 22-service health grid |
| `/mesh` | All | 44-channel neural mesh status with real-time routing |
| `/forge` | All | Fractal Forge — PFSE synthesis runs, minted capsules |

---

## Technical Implementation

### DNS Configuration (Cloudflare)

All 5 domains point to the same origin via Cloudflare proxy:

```
pyraclaw.com     A     -> VM_IP (proxied)
pyraclaw.ai      A     -> VM_IP (proxied)
pyraclaw.uk      A     -> VM_IP (proxied)
pyraclaw.xyz     A     -> VM_IP (proxied)
pyraclaw.io      A     -> VM_IP (proxied)
```

### NGINX Routing

```nginx
server {
    listen 443 ssl http2;
    server_name pyraclaw.com www.pyraclaw.com;
    location / { proxy_pass http://mission-control:3000/corporate; }
}

server {
    listen 443 ssl http2;
    server_name pyraclaw.ai;
    location / { proxy_pass http://mission-control:3000/platform; }
    location /api/ { proxy_pass http://orchestrator:8002/; }
}

server {
    listen 443 ssl http2;
    server_name pyraclaw.uk;
    location / { proxy_pass http://mission-control:3000/compliance; }
}

server {
    listen 443 ssl http2;
    server_name pyraclaw.xyz;
    location / { proxy_pass http://mission-control:3000/evidence; }
    location /api/mint/ { proxy_pass http://evidence-ledger:8009/; }
}

server {
    listen 443 ssl http2;
    server_name pyraclaw.io;
    location / { proxy_pass http://mission-control:3000/developers; }
    location /api/ { proxy_pass http://orchestrator:8002/; }
}
```

### Mission Control Service

The Mission Control dashboard is an evolution of the Prototype Casa concept:
- Real-time polling of all 22 services every 15 seconds
- QDP layer visualisation with 4-hash status
- RSFS Phi convergence bar with gate indicators
- 44-channel mesh topology map
- Fractal Forge run history with minted capsule viewer
- EU AI Act compliance scorecard

---

## EU AI Act Compliance Layer

### pyraclaw.uk serves as the compliance hub:

| Requirement | Implementation | Service |
|-------------|---------------|---------|
| **Transparency** | All AI decisions logged with rationale | Evidence Ledger |
| **Human Oversight** | RSFS gate requires human review for HOLD/FAIL | RSFS Core |
| **Robustness** | Circuit breakers, canary deploys, rollback | Deploy Gate |
| **Data Governance** | QDP sealing, no data leaves sovereign mesh | QDP Hasher |
| **Risk Classification** | Automated risk scoring per interaction | Freedom Engine |
| **Audit Trail** | Every output has QDP capsule + Zenodo DOI | Evidence Ledger |
| **Accountability** | ORCID-linked researcher identity | QDP Hasher |

### Compliance Endpoints

```
GET  /api/compliance/status       -> Current compliance posture
GET  /api/compliance/audit-trail  -> Full audit log with QDP capsules
GET  /api/compliance/risk-scores  -> Risk classification per service
POST /api/compliance/report       -> Generate compliance report
```

---

## Swarm-Enhanced Architecture

The Mission Control is swarm-enhanced — it doesn't just monitor, it actively manages:

1. **Auto-scaling:** Monitor RSFS scores; if any dimension drops below threshold, spawn additional agents via Swarm Manager
2. **Self-healing:** If a service fails health check, Deploy Gate triggers automatic rollback
3. **Evidence minting:** Every deployment, every configuration change, every significant event gets a QDP capsule
4. **Frequency alignment:** iTrifactor frequencies (432/528/639/963 Hz) used as heartbeat signals across the mesh

---

## Implementation Priority

| Phase | Deliverable | Timeline |
|-------|-------------|----------|
| **1** | Mission Control API (FastAPI :3000) with domain routing | Now |
| **2** | NGINX config for 5-domain routing | After DNS setup |
| **3** | Cloudflare DNS + SSL for all 5 domains | When domains acquired |
| **4** | Web3 evidence minting on pyraclaw.xyz | After smart contract |
| **5** | Developer portal on pyraclaw.io | After SDK |

---

*DD7 International GmbH | PyraClaw Web Superstructure v1.0.0 | March 2026*
*MINTED_GREEN | SURGICAL | No overclaiming. Results-driven.*
*Patent: PCT/EP2025/080977 | US 19/541,276 | ORCID: 0009-0009-7256-9337*
