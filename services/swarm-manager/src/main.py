"""
Swarm Manager Service — PyRaClaw 44-Agent Orchestrator
Patent: PCT/EP2025/080977 | ORCID: 0009-0009-7256-9337
"""

import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Constants ───────────────────────────────────────────────────────────────
SERVICE_NAME = "swarm-manager"
SERVICE_VERSION = "1.0.0"
PORT = 8005
START_TIME = time.time()

MAX_AGENTS = 44

ROLES = {
    "scout": {"max_agents": 6, "description": "Reconnaissance and data gathering"},
    "worker": {"max_agents": 8, "description": "Primary task execution"},
    "validator": {"max_agents": 5, "description": "Output verification and QDP sealing"},
    "router": {"max_agents": 4, "description": "Neural mesh message routing"},
    "guardian": {"max_agents": 4, "description": "Security posture and freedom-engine checks"},
    "analyst": {"max_agents": 5, "description": "RSFS scoring and evidence analysis"},
    "bridge": {"max_agents": 4, "description": "LoRaWAN and external protocol bridging"},
    "cortex": {"max_agents": 4, "description": "Cortical mapping and frequency coherence"},
    "orchestrator": {"max_agents": 4, "description": "Swarm coordination and QEDO optimisation"},
}

PHI_TARGET = 0.77
KAPPA = 0.618

# ── State ───────────────────────────────────────────────────────────────────
agents: Dict[str, Dict[str, Any]] = {}
assignments: List[Dict[str, Any]] = []
reconciliation_log: List[Dict[str, Any]] = []
ultra_mode: bool = False

# ── Models ──────────────────────────────────────────────────────────────────

class SpawnRequest(BaseModel):
    role: str
    count: int = Field(default=1, ge=1, le=10)
    ultra: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentInfo(BaseModel):
    agent_id: str
    role: str
    status: str
    spawned_at: float
    task_count: int
    ultra: bool

class SpawnResponse(BaseModel):
    spawned: List[AgentInfo]
    total_agents: int
    ultra_mode: bool

class AssignRequest(BaseModel):
    agent_id: str
    task: str
    priority: int = Field(default=5, ge=1, le=10)
    payload: Dict[str, Any] = Field(default_factory=dict)

class AssignResponse(BaseModel):
    assignment_id: str
    agent_id: str
    task: str
    status: str
    timestamp: float

class ReconcileRequest(BaseModel):
    scope: str = Field(default="all", pattern="^(all|role|agent)$")
    target: Optional[str] = None

class ReconcileResult(BaseModel):
    reconcile_id: str
    agents_checked: int
    agents_recycled: int
    qedo_score: float
    gate: str
    timestamp: float

class SwarmStatus(BaseModel):
    total_agents: int
    max_agents: int
    ultra_mode: bool
    roles: Dict[str, int]
    total_assignments: int
    total_reconciliations: int
    uptime: float

# ── Helpers ─────────────────────────────────────────────────────────────────

def _role_count(role: str) -> int:
    return sum(1 for a in agents.values() if a["role"] == role)


def _qedo_score() -> float:
    if not agents:
        return 0.0
    active = sum(1 for a in agents.values() if a["status"] == "active")
    utilisation = active / len(agents) if agents else 0.0
    task_density = min(1.0, sum(a["task_count"] for a in agents.values()) / max(len(agents), 1) / 5.0)
    return round(PHI_TARGET * utilisation * task_density * KAPPA * 100, 4)


# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="PyRaClaw Swarm Manager", version=SERVICE_VERSION)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": round(time.time() - START_TIME, 2),
        "agents": len(agents),
    }


@app.post("/api/swarm/spawn", response_model=SpawnResponse)
async def spawn_agents(req: SpawnRequest):
    global ultra_mode
    if req.role not in ROLES:
        raise HTTPException(status_code=400, detail=f"Unknown role: {req.role}. Valid: {list(ROLES.keys())}")

    role_info = ROLES[req.role]
    current = _role_count(req.role)
    available_role = role_info["max_agents"] - current
    available_total = MAX_AGENTS - len(agents)
    can_spawn = min(req.count, available_role, available_total)

    if can_spawn <= 0:
        raise HTTPException(status_code=409, detail=f"Cannot spawn: role has {current}/{role_info['max_agents']}, total {len(agents)}/{MAX_AGENTS}")

    if req.ultra:
        ultra_mode = True

    spawned = []
    for _ in range(can_spawn):
        agent_id = f"{req.role}-{uuid.uuid4().hex[:8]}"
        agent = {
            "agent_id": agent_id,
            "role": req.role,
            "status": "active",
            "spawned_at": time.time(),
            "task_count": 0,
            "ultra": req.ultra or ultra_mode,
        }
        agents[agent_id] = agent
        spawned.append(AgentInfo(**agent))

    return SpawnResponse(
        spawned=spawned,
        total_agents=len(agents),
        ultra_mode=ultra_mode,
    )


@app.post("/api/swarm/assign", response_model=AssignResponse)
async def assign_task(req: AssignRequest):
    if req.agent_id not in agents:
        raise HTTPException(status_code=404, detail=f"Agent {req.agent_id} not found")

    agent = agents[req.agent_id]
    if agent["status"] != "active":
        raise HTTPException(status_code=409, detail=f"Agent {req.agent_id} is {agent['status']}, not active")

    agent["task_count"] += 1
    assignment = {
        "assignment_id": str(uuid.uuid4()),
        "agent_id": req.agent_id,
        "task": req.task,
        "priority": req.priority,
        "payload": req.payload,
        "status": "assigned",
        "timestamp": time.time(),
    }
    assignments.append(assignment)

    return AssignResponse(
        assignment_id=assignment["assignment_id"],
        agent_id=req.agent_id,
        task=req.task,
        status="assigned",
        timestamp=assignment["timestamp"],
    )


@app.post("/api/swarm/reconcile", response_model=ReconcileResult)
async def reconcile(req: ReconcileRequest):
    checked = 0
    recycled = 0

    targets = list(agents.values())
    if req.scope == "role" and req.target:
        targets = [a for a in targets if a["role"] == req.target]
    elif req.scope == "agent" and req.target:
        targets = [a for a in targets if a["agent_id"] == req.target]

    for agent in targets:
        checked += 1
        if agent["task_count"] == 0 and (time.time() - agent["spawned_at"]) > 300:
            agent["status"] = "recycled"
            recycled += 1

    score = _qedo_score()
    gate = "OPTIMAL" if score >= 30.0 else ("STABLE" if score >= 15.0 else "DEGRADED")

    result = {
        "reconcile_id": str(uuid.uuid4()),
        "agents_checked": checked,
        "agents_recycled": recycled,
        "qedo_score": score,
        "gate": gate,
        "timestamp": time.time(),
    }
    reconciliation_log.append(result)

    return ReconcileResult(**result)


@app.get("/api/swarm/status", response_model=SwarmStatus)
async def swarm_status():
    role_counts = {}
    for role in ROLES:
        role_counts[role] = _role_count(role)

    return SwarmStatus(
        total_agents=len(agents),
        max_agents=MAX_AGENTS,
        ultra_mode=ultra_mode,
        roles=role_counts,
        total_assignments=len(assignments),
        total_reconciliations=len(reconciliation_log),
        uptime=round(time.time() - START_TIME, 2),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
