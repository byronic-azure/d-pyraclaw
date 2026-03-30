"""
Neural Mesh Service — PyRaClaw 44-Channel Router
Patent: PCT/EP2025/080977 | ORCID: 0009-0009-7256-9337
"""

import time
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Constants ───────────────────────────────────────────────────────────────
SERVICE_NAME = "neural-mesh"
SERVICE_VERSION = "1.0.0"
PORT = 9044
START_TIME = time.time()

CHANNEL_MAP: Dict[str, List[str]] = {
    "messaging": ["msg-alpha", "msg-beta", "msg-gamma"],
    "lorawan": ["lora-eu868-0", "lora-eu868-1", "lora-eu868-2", "lora-eu868-3",
                 "lora-us915-0", "lora-us915-1", "lora-us915-2", "lora-us915-3"],
    "rf": ["rf-433", "rf-868", "rf-915", "rf-2400", "rf-5800", "rf-sub1g-a", "rf-sub1g-b", "rf-uwb"],
    "cerebral": ["ctx-prefrontal", "ctx-motor", "ctx-sensory", "ctx-parietal",
                  "ctx-temporal", "ctx-occipital", "ctx-limbic", "ctx-brainstem"],
    "owl": ["owl-vision-l", "owl-vision-r", "owl-auditory-l", "owl-auditory-r",
             "owl-spatial", "owl-temporal", "owl-memory", "owl-instinct"],
    "neo-cortex": ["neo-layer1", "neo-layer2", "neo-layer3", "neo-layer4",
                    "neo-layer5", "neo-layer6", "neo-assoc-a", "neo-assoc-b", "neo-integrator"],
}

ALL_CHANNELS: List[str] = []
for ch_list in CHANNEL_MAP.values():
    ALL_CHANNELS.extend(ch_list)

assert len(ALL_CHANNELS) == 44, f"Expected 44 channels, got {len(ALL_CHANNELS)}"

# ── State ───────────────────────────────────────────────────────────────────
route_log: List[Dict[str, Any]] = []
channel_stats: Dict[str, int] = {ch: 0 for ch in ALL_CHANNELS}

# ── Models ──────────────────────────────────────────────────────────────────

class RouteRequest(BaseModel):
    payload: Any
    source_channel: str
    target_channels: List[str] = Field(default_factory=list)
    priority: int = Field(default=5, ge=1, le=10)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RouteResponse(BaseModel):
    route_id: str
    status: str
    source: str
    targets_reached: List[str]
    targets_failed: List[str]
    timestamp: float

class ChannelInfo(BaseModel):
    name: str
    category: str
    message_count: int

class MeshStatus(BaseModel):
    total_channels: int
    active_routes: int
    categories: Dict[str, int]
    channel_stats: Dict[str, int]

# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="PyRaClaw Neural Mesh", version=SERVICE_VERSION)


def _find_category(channel: str) -> Optional[str]:
    for cat, channels in CHANNEL_MAP.items():
        if channel in channels:
            return cat
    return None


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": round(time.time() - START_TIME, 2),
    }


@app.post("/api/mesh/route", response_model=RouteResponse)
async def route_message(req: RouteRequest):
    if req.source_channel not in ALL_CHANNELS:
        raise HTTPException(status_code=400, detail=f"Unknown source channel: {req.source_channel}")

    targets = req.target_channels if req.target_channels else ALL_CHANNELS
    reached = []
    failed = []

    for t in targets:
        if t in ALL_CHANNELS:
            channel_stats[t] += 1
            reached.append(t)
        else:
            failed.append(t)

    channel_stats[req.source_channel] += 1

    entry = {
        "route_id": str(uuid.uuid4()),
        "source": req.source_channel,
        "targets_reached": reached,
        "targets_failed": failed,
        "priority": req.priority,
        "timestamp": time.time(),
        "payload_size": len(str(req.payload)),
    }
    route_log.append(entry)

    return RouteResponse(
        route_id=entry["route_id"],
        status="routed",
        source=req.source_channel,
        targets_reached=reached,
        targets_failed=failed,
        timestamp=entry["timestamp"],
    )


@app.get("/api/mesh/channels", response_model=List[ChannelInfo])
async def list_channels():
    result = []
    for cat, channels in CHANNEL_MAP.items():
        for ch in channels:
            result.append(ChannelInfo(name=ch, category=cat, message_count=channel_stats.get(ch, 0)))
    return result


@app.get("/api/mesh/status", response_model=MeshStatus)
async def mesh_status():
    return MeshStatus(
        total_channels=len(ALL_CHANNELS),
        active_routes=len(route_log),
        categories={cat: len(chs) for cat, chs in CHANNEL_MAP.items()},
        channel_stats=channel_stats,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
