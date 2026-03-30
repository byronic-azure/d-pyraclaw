"""
Frequency Engine Service — PyRaClaw iTrifactor Coherence
Patent: PCT/EP2025/080977 | ORCID: 0009-0001-9561-5483
"""

import math
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Constants ───────────────────────────────────────────────────────────────
SERVICE_NAME = "frequency-engine"
SERVICE_VERSION = "1.0.0"
PORT = 9045
START_TIME = time.time()

ITRIFACTOR_HZ = {
    "earth": 432.0,
    "love": 528.0,
    "connection": 639.0,
    "awakening": 963.0,
}
PHI = 1.6180339887
COHERENCE_THRESHOLD = 0.77

# ── State ───────────────────────────────────────────────────────────────────
process_log: List[Dict[str, Any]] = []

# ── Models ──────────────────────────────────────────────────────────────────

class FrequencyRequest(BaseModel):
    signal_data: List[float] = Field(..., min_length=1)
    target_hz: Optional[float] = None
    mode: str = Field(default="coherence", pattern="^(coherence|entrain|analyse)$")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class FrequencyResult(BaseModel):
    id: str
    mode: str
    dominant_hz: float
    itrifactor_alignment: Dict[str, float]
    coherence_score: float
    phi_ratio: float
    gate: str
    timestamp: float

class CoherenceReport(BaseModel):
    total_processed: int
    average_coherence: float
    pass_rate: float
    itrifactor_frequencies: Dict[str, float]

# ── Helpers ─────────────────────────────────────────────────────────────────

def _dominant_frequency(signal: List[float]) -> float:
    """Estimate dominant frequency from zero crossings."""
    if len(signal) < 2:
        return 0.0
    crossings = 0
    for i in range(1, len(signal)):
        if (signal[i - 1] >= 0 and signal[i] < 0) or (signal[i - 1] < 0 and signal[i] >= 0):
            crossings += 1
    return crossings / (2.0 * len(signal)) * 1000.0


def _itrifactor_alignment(hz: float) -> Dict[str, float]:
    """Compute closeness to each iTrifactor frequency."""
    alignment = {}
    for name, ref in ITRIFACTOR_HZ.items():
        if ref == 0:
            alignment[name] = 0.0
        else:
            delta = abs(hz - ref) / ref
            alignment[name] = round(max(0.0, 1.0 - delta), 4)
    return alignment


def _coherence_score(alignment: Dict[str, float]) -> float:
    if not alignment:
        return 0.0
    vals = list(alignment.values())
    return round(sum(vals) / len(vals), 4)


def _phi_ratio(hz: float) -> float:
    if hz <= 0:
        return 0.0
    ratio = hz / (hz / PHI) if hz > 0 else 0.0
    return round(ratio, 6)


# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="PyRaClaw Frequency Engine", version=SERVICE_VERSION)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": round(time.time() - START_TIME, 2),
    }


@app.post("/api/frequency/process", response_model=FrequencyResult)
async def process_signal(req: FrequencyRequest):
    dom_hz = _dominant_frequency(req.signal_data)
    if req.target_hz is not None:
        dom_hz = req.target_hz

    alignment = _itrifactor_alignment(dom_hz)
    coherence = _coherence_score(alignment)
    phi = _phi_ratio(dom_hz)
    gate = "PASS" if coherence >= COHERENCE_THRESHOLD else "HOLD"

    result = FrequencyResult(
        id=str(uuid.uuid4()),
        mode=req.mode,
        dominant_hz=round(dom_hz, 2),
        itrifactor_alignment=alignment,
        coherence_score=coherence,
        phi_ratio=phi,
        gate=gate,
        timestamp=time.time(),
    )

    process_log.append(result.model_dump())
    return result


@app.get("/api/frequency/coherence", response_model=CoherenceReport)
async def coherence_report():
    total = len(process_log)
    if total == 0:
        avg = 0.0
        pr = 0.0
    else:
        scores = [e["coherence_score"] for e in process_log]
        avg = round(sum(scores) / total, 4)
        pr = round(sum(1 for s in scores if s >= COHERENCE_THRESHOLD) / total, 4)

    return CoherenceReport(
        total_processed=total,
        average_coherence=avg,
        pass_rate=pr,
        itrifactor_frequencies=ITRIFACTOR_HZ,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
