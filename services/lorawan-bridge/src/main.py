"""
LoRaWAN Bridge Service — PyRaClaw EU868/US915 Gateway
Patent: PCT/EP2025/080977 | ORCID: 0009-0001-9561-5483
"""

import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Constants ───────────────────────────────────────────────────────────────
SERVICE_NAME = "lorawan-bridge"
SERVICE_VERSION = "1.0.0"
PORT = 9047
START_TIME = time.time()

SUPPORTED_BANDS = {
    "EU868": {"min_freq": 863.0, "max_freq": 870.0, "max_power_dbm": 14, "channels": 8},
    "US915": {"min_freq": 902.0, "max_freq": 928.0, "max_power_dbm": 22, "channels": 64},
}

# ── State ───────────────────────────────────────────────────────────────────
registered_nodes: Dict[str, Dict[str, Any]] = {}
message_log: List[Dict[str, Any]] = []

# ── Models ──────────────────────────────────────────────────────────────────

class NodeRegistration(BaseModel):
    dev_eui: str = Field(..., min_length=16, max_length=16)
    app_eui: str = Field(..., min_length=16, max_length=16)
    band: str = Field(default="EU868", pattern="^(EU868|US915)$")
    name: Optional[str] = None

class TransmitRequest(BaseModel):
    dev_eui: str
    payload: str
    port: int = Field(default=1, ge=1, le=223)
    confirmed: bool = False

class TransmitResponse(BaseModel):
    message_id: str
    dev_eui: str
    status: str
    band: str
    rssi: float
    snr: float
    timestamp: float

class NodeInfo(BaseModel):
    dev_eui: str
    app_eui: str
    band: str
    name: Optional[str]
    registered_at: float
    message_count: int

# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="PyRaClaw LoRaWAN Bridge", version=SERVICE_VERSION)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": round(time.time() - START_TIME, 2),
        "registered_nodes": len(registered_nodes),
        "bands": list(SUPPORTED_BANDS.keys()),
    }


@app.post("/api/lorawan/register", response_model=NodeInfo)
async def register_node(req: NodeRegistration):
    if req.dev_eui in registered_nodes:
        raise HTTPException(status_code=409, detail=f"Node {req.dev_eui} already registered")
    if req.band not in SUPPORTED_BANDS:
        raise HTTPException(status_code=400, detail=f"Unsupported band: {req.band}")

    node = {
        "dev_eui": req.dev_eui,
        "app_eui": req.app_eui,
        "band": req.band,
        "name": req.name,
        "registered_at": time.time(),
        "message_count": 0,
    }
    registered_nodes[req.dev_eui] = node
    return NodeInfo(**node)


@app.post("/api/lorawan/transmit", response_model=TransmitResponse)
async def transmit(req: TransmitRequest):
    if req.dev_eui not in registered_nodes:
        raise HTTPException(status_code=404, detail=f"Node {req.dev_eui} not registered")

    node = registered_nodes[req.dev_eui]
    node["message_count"] += 1

    import random
    rssi = round(random.uniform(-120.0, -30.0), 1)
    snr = round(random.uniform(-5.0, 15.0), 1)

    entry = {
        "message_id": str(uuid.uuid4()),
        "dev_eui": req.dev_eui,
        "payload": req.payload,
        "port": req.port,
        "confirmed": req.confirmed,
        "band": node["band"],
        "rssi": rssi,
        "snr": snr,
        "timestamp": time.time(),
    }
    message_log.append(entry)

    return TransmitResponse(
        message_id=entry["message_id"],
        dev_eui=req.dev_eui,
        status="transmitted" if not req.confirmed else "confirmed",
        band=node["band"],
        rssi=rssi,
        snr=snr,
        timestamp=entry["timestamp"],
    )


@app.get("/api/lorawan/nodes", response_model=List[NodeInfo])
async def list_nodes():
    return [NodeInfo(**n) for n in registered_nodes.values()]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
