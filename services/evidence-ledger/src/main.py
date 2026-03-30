"""
Evidence Ledger Service — PyRaClaw QDP-Sealed Record Store
Patent: PCT/EP2025/080977 | ORCID: 0009-0001-9561-5483
"""

import hashlib
import hmac
import json
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Constants ───────────────────────────────────────────────────────────────
SERVICE_NAME = "evidence-ledger"
SERVICE_VERSION = "1.0.0"
PORT = 8009
START_TIME = time.time()

SUPER_HASH = "9146ce69652472be6ab914e84d2ff76fa64b6ae71c19a0365858c73ee68cda88"
PATENT = "PCT/EP2025/080977"
ORCID = "0009-0001-9561-5483"
HMAC_KEY = SUPER_HASH.encode("utf-8")

ZENODO_STAGING_URL = "https://sandbox.zenodo.org/api/deposit/depositions"

# ── State ───────────────────────────────────────────────────────────────────
ledger: List[Dict[str, Any]] = []

# ── Models ──────────────────────────────────────────────────────────────────

class RecordRequest(BaseModel):
    title: str
    payload: Any
    source: str = "manual"
    tags: List[str] = Field(default_factory=list)
    orcid_link: bool = True
    zenodo_stage: bool = False

class QDPLayers(BaseModel):
    sha256: str
    sha512: str
    blake2b: str
    hmac_sha256: str

class LedgerEntry(BaseModel):
    entry_id: str
    title: str
    source: str
    qdp_layers: QDPLayers
    payload_digest: str
    tags: List[str]
    orcid: Optional[str]
    patent: str
    zenodo_staged: bool
    timestamp: float

class VerifyRequest(BaseModel):
    entry_id: str
    payload: Any

class VerifyResult(BaseModel):
    entry_id: str
    sha256_match: bool
    sha512_match: bool
    blake2b_match: bool
    hmac_match: bool
    all_valid: bool
    verified_at: float

# ── QDP Hashing ─────────────────────────────────────────────────────────────

def _normalise(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _qdp_hash(payload: Any) -> Dict[str, str]:
    raw = _normalise(payload)
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sha512": hashlib.sha512(raw).hexdigest(),
        "blake2b": hashlib.blake2b(raw, digest_size=64).hexdigest(),
        "hmac_sha256": hmac.new(HMAC_KEY, raw, hashlib.sha256).hexdigest(),
    }


# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="PyRaClaw Evidence Ledger", version=SERVICE_VERSION)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": round(time.time() - START_TIME, 2),
        "entries": len(ledger),
    }


@app.post("/record", response_model=LedgerEntry)
async def create_record(req: RecordRequest):
    hashes = _qdp_hash(req.payload)
    raw = _normalise(req.payload)

    entry = {
        "entry_id": str(uuid.uuid4()),
        "title": req.title,
        "source": req.source,
        "qdp_layers": hashes,
        "payload_digest": hashlib.sha256(raw).hexdigest(),
        "tags": req.tags,
        "orcid": ORCID if req.orcid_link else None,
        "patent": PATENT,
        "zenodo_staged": req.zenodo_stage,
        "timestamp": time.time(),
    }

    if req.zenodo_stage:
        entry["zenodo_metadata"] = {
            "target_url": ZENODO_STAGING_URL,
            "status": "staged",
            "orcid": ORCID,
            "title": req.title,
            "staged_at": time.time(),
        }

    ledger.append(entry)

    return LedgerEntry(
        entry_id=entry["entry_id"],
        title=entry["title"],
        source=entry["source"],
        qdp_layers=QDPLayers(**hashes),
        payload_digest=entry["payload_digest"],
        tags=entry["tags"],
        orcid=entry.get("orcid"),
        patent=entry["patent"],
        zenodo_staged=entry["zenodo_staged"],
        timestamp=entry["timestamp"],
    )


@app.post("/verify", response_model=VerifyResult)
async def verify_record(req: VerifyRequest):
    entry = next((e for e in ledger if e["entry_id"] == req.entry_id), None)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Entry {req.entry_id} not found")

    hashes = _qdp_hash(req.payload)
    stored = entry["qdp_layers"]

    results = {
        "sha256_match": stored["sha256"] == hashes["sha256"],
        "sha512_match": stored["sha512"] == hashes["sha512"],
        "blake2b_match": stored["blake2b"] == hashes["blake2b"],
        "hmac_match": stored["hmac_sha256"] == hashes["hmac_sha256"],
    }
    results["all_valid"] = all(results.values())

    return VerifyResult(
        entry_id=req.entry_id,
        verified_at=time.time(),
        **results,
    )


@app.get("/entries", response_model=List[LedgerEntry])
async def list_entries(limit: int = 100, offset: int = 0):
    subset = ledger[offset:offset + limit]
    return [
        LedgerEntry(
            entry_id=e["entry_id"],
            title=e["title"],
            source=e["source"],
            qdp_layers=QDPLayers(**e["qdp_layers"]),
            payload_digest=e["payload_digest"],
            tags=e["tags"],
            orcid=e.get("orcid"),
            patent=e["patent"],
            zenodo_staged=e["zenodo_staged"],
            timestamp=e["timestamp"],
        )
        for e in subset
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
