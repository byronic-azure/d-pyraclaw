"""
RSFS Core Service — Recursive Self-Fixing Scorecard
Patent: PCT/EP2025/080977 | ORCID: 0009-0009-7256-9337
"""

import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Constants ───────────────────────────────────────────────────────────────
SERVICE_NAME = "rsfs-core"
SERVICE_VERSION = "1.0.0"
PORT = 8006
START_TIME = time.time()

PHI_TARGET = 0.77
KAPPA = 0.618

DIMENSIONS = {
    "correctness":      {"weight": 0.85, "description": "Functional correctness of outputs"},
    "alignment":        {"weight": 0.88, "description": "Alignment with stated objectives"},
    "stability":        {"weight": 0.82, "description": "Runtime stability and resilience"},
    "ui_integrity":     {"weight": 0.80, "description": "UI rendering fidelity"},
    "deploy_readiness": {"weight": 0.78, "description": "Deployment pipeline readiness"},
    "evidence_quality": {"weight": 0.85, "description": "Evidence trail completeness"},
    "security_posture": {"weight": 0.90, "description": "Security hardening level"},
    "compliance_gate":  {"weight": 0.80, "description": "Regulatory compliance status"},
}

C_CRIT = 52.79
C_OPT = 78.42

# ── State ───────────────────────────────────────────────────────────────────
evaluation_log: List[Dict[str, Any]] = []
feedback_loop: List[Dict[str, Any]] = []

# ── Models ──────────────────────────────────────────────────────────────────

class ScoreInput(BaseModel):
    scores: Dict[str, float] = Field(
        ...,
        description="Dimension name -> score (0.0 to 1.0)",
    )
    context: str = Field(default="manual")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DimensionResult(BaseModel):
    dimension: str
    raw_score: float
    weight: float
    weighted_score: float

class EvaluationResult(BaseModel):
    eval_id: str
    Q: float
    N: float
    T: float
    C: float
    gate: str
    dimensions: List[DimensionResult]
    feedback: Optional[str]
    timestamp: float

class FeedbackEntry(BaseModel):
    eval_id: str
    dimension: str
    action: str
    applied_at: float

class RSFSStatus(BaseModel):
    total_evaluations: int
    average_C: float
    pass_count: int
    hold_count: int
    fail_count: int
    dimensions: Dict[str, Any]
    feedback_actions: int

# ── Helpers ─────────────────────────────────────────────────────────────────

def _compute_scores(scores: Dict[str, float]):
    dim_results = []
    total_weighted = 0.0
    total_weight = 0.0

    for dim_name, dim_info in DIMENSIONS.items():
        raw = scores.get(dim_name, 0.5)
        raw = max(0.0, min(1.0, raw))
        w = dim_info["weight"]
        ws = round(raw * w, 4)
        dim_results.append(DimensionResult(
            dimension=dim_name,
            raw_score=raw,
            weight=w,
            weighted_score=ws,
        ))
        total_weighted += ws
        total_weight += w

    Q = round(total_weighted / total_weight, 4) if total_weight > 0 else 0.0
    N = round(len([d for d in dim_results if d.weighted_score >= 0.6]) / len(DIMENSIONS), 4)
    T = round(1.0 - (time.time() % 100) / 1000.0, 4)  # temporal factor
    C = round(PHI_TARGET * Q * N * T * KAPPA * 100, 4)

    if C >= C_OPT:
        gate = "PASS"
    elif C >= C_CRIT:
        gate = "HOLD"
    else:
        gate = "FAIL"

    return Q, N, T, C, gate, dim_results


def _generate_feedback(gate: str, dim_results: List[DimensionResult]) -> Optional[str]:
    if gate == "PASS":
        return None
    weakest = min(dim_results, key=lambda d: d.weighted_score)
    action = f"Improve '{weakest.dimension}' (scored {weakest.raw_score:.2f}, weighted {weakest.weighted_score:.2f})"
    return action


# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="PyRaClaw RSFS Core", version=SERVICE_VERSION)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": round(time.time() - START_TIME, 2),
    }


@app.post("/api/rsfs/evaluate", response_model=EvaluationResult)
async def evaluate(req: ScoreInput):
    Q, N, T, C, gate, dims = _compute_scores(req.scores)
    fb = _generate_feedback(gate, dims)
    eval_id = str(uuid.uuid4())

    result = EvaluationResult(
        eval_id=eval_id,
        Q=Q, N=N, T=T, C=C,
        gate=gate,
        dimensions=dims,
        feedback=fb,
        timestamp=time.time(),
    )
    evaluation_log.append(result.model_dump())

    if fb:
        weakest = min(dims, key=lambda d: d.weighted_score)
        feedback_loop.append({
            "eval_id": eval_id,
            "dimension": weakest.dimension,
            "action": fb,
            "applied_at": time.time(),
        })

    return result


@app.get("/api/rsfs/status", response_model=RSFSStatus)
async def status():
    total = len(evaluation_log)
    if total == 0:
        return RSFSStatus(
            total_evaluations=0, average_C=0.0,
            pass_count=0, hold_count=0, fail_count=0,
            dimensions=DIMENSIONS, feedback_actions=len(feedback_loop),
        )
    avg_c = round(sum(e["C"] for e in evaluation_log) / total, 4)
    pc = sum(1 for e in evaluation_log if e["gate"] == "PASS")
    hc = sum(1 for e in evaluation_log if e["gate"] == "HOLD")
    fc = sum(1 for e in evaluation_log if e["gate"] == "FAIL")

    return RSFSStatus(
        total_evaluations=total, average_C=avg_c,
        pass_count=pc, hold_count=hc, fail_count=fc,
        dimensions=DIMENSIONS, feedback_actions=len(feedback_loop),
    )


@app.get("/api/rsfs/feedback", response_model=List[FeedbackEntry])
async def get_feedback():
    return [FeedbackEntry(**f) for f in feedback_loop]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
