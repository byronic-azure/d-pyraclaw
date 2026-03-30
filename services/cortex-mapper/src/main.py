"""
Cortex Mapper Service — PyRaClaw 6-Layer Cortical Hierarchy
Patent: PCT/EP2025/080977 | ORCID: 0009-0009-7256-9337
"""

import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Constants ───────────────────────────────────────────────────────────────
SERVICE_NAME = "cortex-mapper"
SERVICE_VERSION = "1.0.0"
PORT = 9046
START_TIME = time.time()

CORTICAL_LAYERS = {
    "L1-molecular": {"depth": 1, "role": "input_gating", "owl_region": "owl-instinct"},
    "L2-external-granular": {"depth": 2, "role": "pattern_recognition", "owl_region": "owl-vision-l"},
    "L3-external-pyramidal": {"depth": 3, "role": "lateral_association", "owl_region": "owl-spatial"},
    "L4-internal-granular": {"depth": 4, "role": "thalamic_relay", "owl_region": "owl-auditory-l"},
    "L5-internal-pyramidal": {"depth": 5, "role": "motor_output", "owl_region": "owl-temporal"},
    "L6-multiform": {"depth": 6, "role": "feedback_modulation", "owl_region": "owl-memory"},
}

OWL_TOPOLOGY = {
    "owl-vision-l": ["L2-external-granular", "L3-external-pyramidal"],
    "owl-vision-r": ["L2-external-granular", "L3-external-pyramidal"],
    "owl-auditory-l": ["L4-internal-granular"],
    "owl-auditory-r": ["L4-internal-granular"],
    "owl-spatial": ["L3-external-pyramidal", "L5-internal-pyramidal"],
    "owl-temporal": ["L5-internal-pyramidal", "L6-multiform"],
    "owl-memory": ["L6-multiform", "L1-molecular"],
    "owl-instinct": ["L1-molecular", "L5-internal-pyramidal"],
}

# ── State ───────────────────────────────────────────────────────────────────
mapping_log: List[Dict[str, Any]] = []

# ── Models ──────────────────────────────────────────────────────────────────

class CortexMapRequest(BaseModel):
    signal_id: str
    signal_type: str = Field(default="generic", pattern="^(generic|visual|auditory|motor|memory|spatial)$")
    intensity: float = Field(default=0.5, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LayerActivation(BaseModel):
    layer: str
    role: str
    activation: float
    owl_region: str

class CortexMapResponse(BaseModel):
    map_id: str
    signal_id: str
    activations: List[LayerActivation]
    dominant_layer: str
    owl_pathway: List[str]
    timestamp: float

class TopologyResponse(BaseModel):
    cortical_layers: Dict[str, Any]
    owl_topology: Dict[str, List[str]]
    total_layers: int
    total_owl_regions: int

# ── Helpers ─────────────────────────────────────────────────────────────────

SIGNAL_LAYER_WEIGHTS = {
    "visual": {"L2-external-granular": 0.9, "L3-external-pyramidal": 0.7},
    "auditory": {"L4-internal-granular": 0.9, "L3-external-pyramidal": 0.5},
    "motor": {"L5-internal-pyramidal": 0.9, "L6-multiform": 0.6},
    "memory": {"L6-multiform": 0.9, "L1-molecular": 0.7},
    "spatial": {"L3-external-pyramidal": 0.9, "L5-internal-pyramidal": 0.6},
    "generic": {},
}


def _compute_activations(signal_type: str, intensity: float) -> List[LayerActivation]:
    weights = SIGNAL_LAYER_WEIGHTS.get(signal_type, {})
    activations = []
    for layer_name, info in CORTICAL_LAYERS.items():
        base = weights.get(layer_name, 0.3)
        act = round(min(1.0, base * intensity * 1.2), 4)
        activations.append(LayerActivation(
            layer=layer_name,
            role=info["role"],
            activation=act,
            owl_region=info["owl_region"],
        ))
    return activations


# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="PyRaClaw Cortex Mapper", version=SERVICE_VERSION)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": round(time.time() - START_TIME, 2),
    }


@app.post("/api/cortex/map", response_model=CortexMapResponse)
async def map_signal(req: CortexMapRequest):
    activations = _compute_activations(req.signal_type, req.intensity)
    dominant = max(activations, key=lambda a: a.activation)
    owl_path = OWL_TOPOLOGY.get(dominant.owl_region, [dominant.layer])

    resp = CortexMapResponse(
        map_id=str(uuid.uuid4()),
        signal_id=req.signal_id,
        activations=activations,
        dominant_layer=dominant.layer,
        owl_pathway=owl_path,
        timestamp=time.time(),
    )
    mapping_log.append(resp.model_dump())
    return resp


@app.get("/api/cortex/topology", response_model=TopologyResponse)
async def topology():
    return TopologyResponse(
        cortical_layers=CORTICAL_LAYERS,
        owl_topology=OWL_TOPOLOGY,
        total_layers=len(CORTICAL_LAYERS),
        total_owl_regions=len(OWL_TOPOLOGY),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
