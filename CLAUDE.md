# PyraClaw Sovereign AI Runtime

## Architecture
- Template: MINTED_GREEN (clean, evidence-backed, production-grade)
- Style: SURGICAL (zero bloat, every endpoint justified)
- Security: QDP 4-layer hashing mandatory on all evidence endpoints
- Compliance: EU AI Act aligned — every service maintains audit trail

## Deploy
- GPU: `docker compose -f docker-compose.pyraclaw-gpu.yml up -d --build`
- CPU: `docker compose up -d --build`

## Rules
- Do NOT duplicate services from CallaBridge — PyraClaw is standalone
- All services MUST have `/health` endpoint
- No overclaiming. No grand claims. Results-driven only.
- Every evidence record gets QDP sealed (SHA-256 + SHA-512 + SHA3-256 + SHA3-512)
- Patent: PCT/EP2025/080977 | US 19/541,276
- ORCID: 0009-0009-7256-9337
