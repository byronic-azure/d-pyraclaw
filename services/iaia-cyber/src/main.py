"""
iAiA 2 Cyber Specialist — PyraClaw Sovereign Security Agent
Claude API (Opus 4.6) Powered | White / Grey / Black Hat Modes
DD7 International GmbH | Patent: PCT/EP2025/080977 | US 19/541,276
ORCID: 0009-0003-9584-1741 | MINTED_GREEN | SURGICAL

Architecture:
  - Claude Opus 4.6 with adaptive thinking + @beta_tool security tools
  - QDP 4-layer sealing on all outputs (SHA-256/SHA-512/SHA3-256/SHA3-512)
  - RSFS 8-dimension scoring with security-specific thresholds
  - EU AI Act compliant (Article 13 transparency, Article 14 oversight)
  - 3-phase coherence model: Software (69%) → FPGA (85%) → 3nm ASIC (97%)

COMPLEXITY, DECIPHERED. REALITY, REDEFINED.
"""

import hashlib
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

import anthropic
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from prompts import PHASE_COHERENCE, get_prompt
from tools import ALL_TOOLS, TOOLS_BY_HAT

# ── App ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="iAiA 2 Cyber Specialist",
    version="2.0.0",
    description="PyraClaw Sovereign Security Agent — Claude API Powered",
)

# ── Constants ────────────────────────────────────────────────────────────
SERVICE_NAME = "iaia-cyber"
SERVICE_VERSION = "2.0.0"
PORT = 8012
START_TIME = time.time()
PATENT = "PCT/EP2025/080977"
ORCID = "0009-0003-9584-1741"
SUPER_HASH = "9146ce69652472be6ab914e84d2ff76fa64b6ae71c19a0365858c73ee68cda88"
SOVEREIGN_ORCID = "0009-0001-9561-5483"
MODEL = "claude-opus-4-6"

# ── Config from environment ──────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
IAIA_AUTH_TOKEN = os.getenv("IAIA_AUTH_TOKEN", "")
IAIA_HAT_MODE = os.getenv("IAIA_HAT_MODE", "white")
IAIA_PHASE = int(os.getenv("IAIA_PHASE", "1"))

# ── State ────────────────────────────────────────────────────────────────
current_hat_mode: str = IAIA_HAT_MODE
current_phase: int = IAIA_PHASE
audit_log: List[Dict] = []
analysis_cache: Dict[str, Dict] = {}


# ── QDP 4-Layer Sealing ──────────────────────────────────────────────────
def qdp_seal(data: str) -> Dict[str, str]:
    """Quad-Dimensional Proof: SHA-256 + SHA-512 + SHA3-256 + SHA3-512."""
    raw = data.encode("utf-8")
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sha512": hashlib.sha512(raw).hexdigest()[:32],
        "sha3_256": hashlib.sha3_256(raw).hexdigest(),
        "sha3_512": hashlib.sha3_512(raw).hexdigest()[:32],
        "qdp_version": "1.0.0",
        "sealed_by": SERVICE_NAME,
    }


# ── RSFS Security Scoring ───────────────────────────────────────────────
PHI_TARGET = 0.77
KAPPA = 0.618
C_CRIT = 52.79
C_OPT = 78.42


def rsfs_score(findings: Dict) -> Dict:
    """8-dimension RSFS scoring tuned for security analysis."""
    issue_count = findings.get("total_issues", 0)
    has_critical = any(
        f.get("severity") == "CRITICAL"
        for f in findings.get("findings", findings.get("issues", []))
    )

    # Security-specific dimension scoring
    dims = {
        "correctness": max(0.5, 1.0 - issue_count * 0.02),
        "alignment": 0.90 if not has_critical else 0.60,
        "stability": max(0.6, 1.0 - issue_count * 0.015),
        "security_posture": max(0.3, 1.0 - issue_count * 0.05),
        "evidence_quality": 0.92,  # tool-generated evidence is high quality
        "compliance_gate": 0.88 if not has_critical else 0.50,
        "deploy_readiness": max(0.4, 1.0 - issue_count * 0.04),
        "ui_integrity": 0.85,
    }

    # Compute composite
    q = sum(dims.values()) / len(dims)
    n = sum(1 for v in dims.values() if v >= 0.6) / len(dims)
    t = 1.0  # no temporal decay for security scans
    c_score = PHI_TARGET * q * n * t * KAPPA * 100

    if c_score >= C_OPT:
        gate = "PASS"
    elif c_score >= C_CRIT:
        gate = "HOLD"
    else:
        gate = "FAIL"

    weakest = min(dims, key=dims.get)

    return {
        "dimensions": {k: round(v, 3) for k, v in dims.items()},
        "c_score": round(c_score, 2),
        "gate": gate,
        "weakest_dimension": weakest,
        "phi_target": PHI_TARGET,
        "kappa": KAPPA,
    }


# ── Audit Logger ─────────────────────────────────────────────────────────
def log_audit(action: str, hat_mode: str, details: Dict = None):
    entry = {
        "id": str(uuid.uuid4())[:12],
        "action": action,
        "hat_mode": hat_mode,
        "phase": current_phase,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "details": details or {},
    }
    audit_log.append(entry)
    # Keep audit log bounded
    if len(audit_log) > 10000:
        audit_log.pop(0)
    return entry


# ── Authorization Check ──────────────────────────────────────────────────
def check_auth(hat_mode: str, auth_token: Optional[str], sovereign_override: Optional[str]):
    """Verify authorization for restricted hat modes."""
    if hat_mode == "white":
        return  # no auth needed for defensive mode

    if hat_mode == "grey":
        if not auth_token or (IAIA_AUTH_TOKEN and auth_token != IAIA_AUTH_TOKEN):
            raise HTTPException(status_code=403, detail="Grey hat mode requires valid IAIA_AUTH_TOKEN")

    if hat_mode == "black":
        if not auth_token or (IAIA_AUTH_TOKEN and auth_token != IAIA_AUTH_TOKEN):
            raise HTTPException(status_code=403, detail="Black hat mode requires valid IAIA_AUTH_TOKEN")
        if not sovereign_override or sovereign_override != SOVEREIGN_ORCID:
            raise HTTPException(
                status_code=403,
                detail="Black hat mode requires X-Sovereign-Override header with sovereign ORCID"
            )


# ── Claude API Client ───────────────────────────────────────────────────
def _get_client() -> anthropic.Anthropic:
    if not ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY not configured. Run: bash scripts/configure.sh"
        )
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _run_analysis(prompt: str, hat_mode: str, user_content: str) -> Dict:
    """Run Claude Opus 4.6 with security tools via the beta tool runner."""
    client = _get_client()
    system_prompt = get_prompt(hat_mode, current_phase)
    tools = TOOLS_BY_HAT.get(hat_mode, TOOLS_BY_HAT["white"])

    messages = [{"role": "user", "content": user_content}]

    # Use the tool runner for automatic agentic loop
    collected_text = []
    tool_calls = []

    runner = client.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=16000,
        system=system_prompt,
        thinking={"type": "adaptive"},
        tools=tools,
        messages=messages,
    )

    for message in runner:
        for block in message.content:
            if block.type == "text":
                collected_text.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append({"tool": block.name, "input_summary": str(block.input)[:200]})

    response_text = "\n".join(collected_text)

    return {
        "response": response_text,
        "tool_calls": tool_calls,
        "model": MODEL,
        "hat_mode": hat_mode,
        "phase": current_phase,
    }


# ── Request Models ───────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    code: str = Field(..., description="Source code or configuration to analyze")
    language: str = Field(default="python", description="Programming language")
    context: Optional[str] = Field(default=None, description="Additional context for analysis")


class ThreatModelRequest(BaseModel):
    system_description: str = Field(..., description="System architecture description")
    methodology: str = Field(default="STRIDE", description="STRIDE or DREAD")


class PentestRequest(BaseModel):
    scope: str = Field(..., description="Target scope and boundaries")
    target_type: str = Field(default="web_application", description="web_application, api, network, mobile, cloud, iot")
    rules_of_engagement: Optional[str] = Field(default=None, description="Custom rules of engagement")


class IncidentRequest(BaseModel):
    incident_type: str = Field(..., description="data_breach, ransomware, phishing, insider_threat, ddos, credential_compromise")
    severity: str = Field(default="high", description="critical, high, medium, low")
    context: Optional[str] = Field(default=None, description="Incident context and known details")


class ForensicsRequest(BaseModel):
    artifact_type: str = Field(..., description="access_log, auth_log, network_capture, file_metadata, email_header")
    data: str = Field(..., description="Raw artifact data")


class ReconRequest(BaseModel):
    target: str = Field(..., description="Domain or IP for passive reconnaissance")


class HatModeRequest(BaseModel):
    mode: str = Field(..., description="white, grey, or black")


class ReportRequest(BaseModel):
    analysis_id: str = Field(..., description="ID of a previous analysis to generate report for")
    format: str = Field(default="detailed", description="detailed or executive")


# ── Endpoints ────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    phase_info = PHASE_COHERENCE.get(current_phase, PHASE_COHERENCE[1])
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "identity": "iAiA 2 — PyraClaw Sovereign Cyber Specialist",
        "claude_api": "configured" if ANTHROPIC_API_KEY else "missing",
        "model": MODEL,
        "hat_mode": current_hat_mode,
        "phase": current_phase,
        "phase_name": phase_info["name"],
        "coherence_target": phase_info["coherence"],
        "uptime": round(time.time() - START_TIME, 2),
        "analyses": len(analysis_cache),
        "audit_entries": len(audit_log),
        "eu_ai_act": "Article 13 compliant — identifies as AI security analyst",
        "patent": PATENT,
    }


@app.post("/api/analyze")
async def analyze(
    req: AnalyzeRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Analyze code or configuration for security vulnerabilities using Claude with tools."""
    check_auth(current_hat_mode, x_auth_token, x_sovereign_override)

    user_content = (
        f"Analyze the following {req.language} code for security vulnerabilities. "
        f"Use the available security tools to scan for OWASP Top 10, cryptographic weaknesses, "
        f"and any other security issues. Provide severity ratings and remediation.\n\n"
        f"```{req.language}\n{req.code}\n```"
    )
    if req.context:
        user_content += f"\n\nAdditional context: {req.context}"

    result = _run_analysis("analyze", current_hat_mode, user_content)

    # Seal and score
    seal = qdp_seal(result["response"])
    score = rsfs_score({"total_issues": len(result["tool_calls"]), "findings": []})

    analysis_id = str(uuid.uuid4())[:12]
    entry = {
        "id": analysis_id,
        "type": "code_analysis",
        **result,
        "seal": seal,
        "rsfs": score,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    analysis_cache[analysis_id] = entry
    log_audit("analyze", current_hat_mode, {"analysis_id": analysis_id, "language": req.language})

    return entry


@app.post("/api/threat-model")
async def threat_model_endpoint(
    req: ThreatModelRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Generate STRIDE/DREAD threat model using Claude with tools."""
    check_auth(current_hat_mode, x_auth_token, x_sovereign_override)

    user_content = (
        f"Perform a {req.methodology} threat model analysis on this system:\n\n"
        f"{req.system_description}\n\n"
        f"Use the threat_model tool and provide a comprehensive analysis with "
        f"risk ratings and mitigation recommendations."
    )

    result = _run_analysis("threat-model", current_hat_mode, user_content)
    seal = qdp_seal(result["response"])
    score = rsfs_score({"total_issues": 0, "findings": []})

    analysis_id = str(uuid.uuid4())[:12]
    entry = {
        "id": analysis_id,
        "type": "threat_model",
        **result,
        "methodology": req.methodology,
        "seal": seal,
        "rsfs": score,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    analysis_cache[analysis_id] = entry
    log_audit("threat-model", current_hat_mode, {"analysis_id": analysis_id, "methodology": req.methodology})

    return entry


@app.post("/api/pentest")
async def pentest_endpoint(
    req: PentestRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Generate authorized penetration testing plan. Black hat mode requires sovereign override."""
    check_auth(current_hat_mode, x_auth_token, x_sovereign_override)

    user_content = (
        f"Generate a penetration testing plan for the following scope:\n\n"
        f"Scope: {req.scope}\n"
        f"Target type: {req.target_type}\n"
    )
    if req.rules_of_engagement:
        user_content += f"Rules of engagement: {req.rules_of_engagement}\n"
    user_content += (
        "\nUse the pentest_plan tool and provide a comprehensive methodology, "
        "timeline, and deliverables list."
    )

    result = _run_analysis("pentest", current_hat_mode, user_content)
    seal = qdp_seal(result["response"])

    analysis_id = str(uuid.uuid4())[:12]
    entry = {
        "id": analysis_id,
        "type": "pentest_plan",
        **result,
        "seal": seal,
        "authorization_verified": True,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    analysis_cache[analysis_id] = entry
    log_audit("pentest", current_hat_mode, {"analysis_id": analysis_id, "target_type": req.target_type})

    return entry


@app.post("/api/incident")
async def incident_endpoint(
    req: IncidentRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Generate incident response playbook."""
    check_auth(current_hat_mode, x_auth_token, x_sovereign_override)

    user_content = (
        f"Generate an incident response playbook for:\n\n"
        f"Incident type: {req.incident_type}\n"
        f"Severity: {req.severity}\n"
    )
    if req.context:
        user_content += f"Context: {req.context}\n"
    user_content += "\nUse the incident_response tool and provide a comprehensive IR plan."

    result = _run_analysis("incident", current_hat_mode, user_content)
    seal = qdp_seal(result["response"])

    analysis_id = str(uuid.uuid4())[:12]
    entry = {
        "id": analysis_id,
        "type": "incident_response",
        **result,
        "seal": seal,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    analysis_cache[analysis_id] = entry
    log_audit("incident", current_hat_mode, {"analysis_id": analysis_id, "incident_type": req.incident_type})

    return entry


@app.post("/api/forensics")
async def forensics_endpoint(
    req: ForensicsRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Analyze digital forensic artifacts."""
    check_auth(current_hat_mode, x_auth_token, x_sovereign_override)

    user_content = (
        f"Analyze the following forensic artifact:\n\n"
        f"Artifact type: {req.artifact_type}\n"
        f"Data:\n```\n{req.data[:5000]}\n```\n\n"
        f"Use the forensics_analyze tool. Identify indicators of compromise, "
        f"timeline reconstruction, and chain of custody evidence."
    )

    result = _run_analysis("forensics", current_hat_mode, user_content)
    seal = qdp_seal(result["response"])

    analysis_id = str(uuid.uuid4())[:12]
    entry = {
        "id": analysis_id,
        "type": "forensics",
        **result,
        "artifact_hash": hashlib.sha256(req.data.encode()).hexdigest()[:16],
        "seal": seal,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    analysis_cache[analysis_id] = entry
    log_audit("forensics", current_hat_mode, {"analysis_id": analysis_id, "artifact_type": req.artifact_type})

    return entry


@app.post("/api/recon")
async def recon_endpoint(
    req: ReconRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Passive network reconnaissance. Requires grey or black hat mode."""
    if current_hat_mode == "white":
        raise HTTPException(status_code=403, detail="Reconnaissance requires grey or black hat mode")
    check_auth(current_hat_mode, x_auth_token, x_sovereign_override)

    user_content = (
        f"Perform passive reconnaissance on: {req.target}\n\n"
        f"Use the network_recon tool. Enumerate DNS records, subdomains, "
        f"certificate transparency logs, and any publicly available information. "
        f"Passive only — no active scanning."
    )

    result = _run_analysis("recon", current_hat_mode, user_content)
    seal = qdp_seal(result["response"])

    analysis_id = str(uuid.uuid4())[:12]
    entry = {
        "id": analysis_id,
        "type": "reconnaissance",
        **result,
        "target": req.target,
        "seal": seal,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    analysis_cache[analysis_id] = entry
    log_audit("recon", current_hat_mode, {"analysis_id": analysis_id, "target": req.target})

    return entry


@app.get("/api/hat-mode")
async def get_hat_mode():
    """Get current operational hat mode and phase."""
    phase_info = PHASE_COHERENCE.get(current_phase, PHASE_COHERENCE[1])
    return {
        "hat_mode": current_hat_mode,
        "phase": current_phase,
        "phase_name": phase_info["name"],
        "coherence_target": phase_info["coherence"],
        "tools_available": len(TOOLS_BY_HAT.get(current_hat_mode, [])),
        "authorization": {
            "white": "open",
            "grey": "requires X-Auth-Token",
            "black": "requires X-Auth-Token + X-Sovereign-Override (ORCID)",
        },
    }


@app.post("/api/hat-mode")
async def set_hat_mode(
    req: HatModeRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Switch operational hat mode. Grey/black require authorization."""
    global current_hat_mode
    if req.mode not in ("white", "grey", "black"):
        raise HTTPException(status_code=400, detail="Mode must be white, grey, or black")

    check_auth(req.mode, x_auth_token, x_sovereign_override)
    prev_mode = current_hat_mode
    current_hat_mode = req.mode
    log_audit("hat-mode-change", req.mode, {"previous": prev_mode, "new": req.mode})

    return {
        "status": "mode_changed",
        "previous": prev_mode,
        "current": current_hat_mode,
        "tools_available": len(TOOLS_BY_HAT.get(current_hat_mode, [])),
    }


@app.post("/api/report")
async def generate_report(
    req: ReportRequest,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token"),
    x_sovereign_override: Optional[str] = Header(None, alias="X-Sovereign-Override"),
):
    """Generate a QDP-sealed security report from a previous analysis."""
    check_auth(current_hat_mode, x_auth_token, x_sovereign_override)

    analysis = analysis_cache.get(req.analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analysis {req.analysis_id} not found")

    report_content = json.dumps(analysis, default=str, indent=2)
    seal = qdp_seal(report_content)

    report = {
        "report_id": str(uuid.uuid4())[:12],
        "analysis_id": req.analysis_id,
        "format": req.format,
        "generated_by": f"iAiA 2 v{SERVICE_VERSION}",
        "hat_mode": analysis.get("hat_mode", current_hat_mode),
        "phase": current_phase,
        "content": analysis.get("response", ""),
        "tool_calls": analysis.get("tool_calls", []),
        "rsfs": analysis.get("rsfs", {}),
        "seal": seal,
        "attestation": {
            "patent": PATENT,
            "orcid": ORCID,
            "project": "pyraclaw-sovereign-v1",
            "eu_ai_act": "This report was generated by an AI security analyst (Article 13)",
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    log_audit("report", current_hat_mode, {"report_id": report["report_id"], "analysis_id": req.analysis_id})

    return report


@app.get("/api/audit")
async def get_audit(limit: int = 100):
    """Retrieve security audit log entries."""
    return {
        "entries": audit_log[-limit:],
        "total": len(audit_log),
        "hat_mode": current_hat_mode,
        "phase": current_phase,
    }
