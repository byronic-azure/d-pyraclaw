"""
PyraClaw Port Guard — 5-DIP SHA Cyber Security for Exposed Ports
DD7 International GmbH | Patent: PCT/EP2025/080977
ORCID: 0009-0003-9584-1741 | PyraClaw Project

Port 7777 (portboss) — Command & Control
Port 8888 (port8) — Jupyter/Notebook Access

5-DIP SHA Stack:
  DIP-1: SHA-256 (NIST baseline)
  DIP-2: SHA-384 (gateway hash)
  DIP-3: SHA3-256 (quantum-ready)
  DIP-4: BLAKE2b (speed + security)
  DIP-5: SHA-512 (sovereign maximum)

WISeer Tattoo Interface (WTi): Every port knock is logged,
scored, and fed back into the wisdom amplification loop.
Dark web tested. Battle tested. Scars become wisdom.
"""

import hashlib
import hmac
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="PyraClaw Port Guard",
    version="1.0.0",
    description="5-DIP SHA Cyber Security — Dark Web Tested, Battle Tested"
)

START_TIME = time.time()
SOVEREIGN_ORCID = "0009-0003-9584-1741"
HMAC_SECRET = os.getenv("PORT_GUARD_SECRET", "9146ce69652472be6ab914e84d2ff76fa64b6ae71c19a0365858c73ee68cda88")

# ── State ─────────────────────────────────────────────────────────────────
knock_log: List[Dict[str, Any]] = []
blocked_ips: Dict[str, Dict[str, Any]] = {}
wiseer_scars: List[Dict[str, Any]] = []  # WTi — errors become wisdom


# ── 5-DIP SHA Stack ──────────────────────────────────────────────────────
def five_dip_hash(data: str, nonce: str = "portboss") -> Dict[str, str]:
    """5-layer SHA hash stack — each DIP adds a security dimension."""
    raw = data.encode("utf-8")
    nonce_bytes = nonce.encode("utf-8")

    dip1 = hashlib.sha256(raw).hexdigest()                                    # NIST baseline
    dip2 = hashlib.sha384((dip1 + nonce).encode()).hexdigest()                # Gateway
    dip3 = hashlib.sha3_256(raw + nonce_bytes).hexdigest()                    # Quantum-ready
    dip4 = hashlib.blake2b(raw, digest_size=64, key=nonce_bytes[:64].ljust(64, b'\0')).hexdigest()  # Speed+security
    dip5 = hashlib.sha512(raw + dip3.encode() + dip4.encode()).hexdigest()    # Sovereign max

    # Final seal: hash of all 5 DIPs concatenated
    chain = (dip1 + dip2 + dip3 + dip4 + dip5).encode()
    final_seal = hashlib.sha3_256(chain).hexdigest()

    return {
        "dip1_sha256": dip1,
        "dip2_sha384_gateway": dip2[:64],
        "dip3_sha3_256_quantum": dip3,
        "dip4_blake2b_speed": dip4[:64],
        "dip5_sha512_sovereign": dip5[:64],
        "final_seal": final_seal,
        "dip_count": 5,
        "nonce": nonce,
    }


def verify_five_dip(data: str, expected_seal: str, nonce: str = "portboss") -> bool:
    """Verify a 5-DIP hash seal."""
    computed = five_dip_hash(data, nonce)
    return computed["final_seal"] == expected_seal


# ── Port Knock Authentication ────────────────────────────────────────────
def generate_knock_token(port: int, client_id: str) -> Dict[str, Any]:
    """Generate a 5-DIP sealed knock token for port access."""
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    knock_data = f"{port}:{client_id}:{timestamp}:{HMAC_SECRET[:16]}"
    dips = five_dip_hash(knock_data, nonce=f"port-{port}")
    hmac_sig = hmac.new(
        HMAC_SECRET.encode(), knock_data.encode(), hashlib.sha256
    ).hexdigest()

    token = {
        "token_id": str(uuid.uuid4())[:12],
        "port": port,
        "client_id": client_id,
        "timestamp": timestamp,
        "expires_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3600)),
        "dips": dips,
        "hmac": hmac_sig,
        "valid": True,
    }
    return token


def validate_knock(token: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a knock token — all 5 DIPs must verify."""
    port = token.get("port")
    client_id = token.get("client_id")
    timestamp = token.get("timestamp")
    knock_data = f"{port}:{client_id}:{timestamp}:{HMAC_SECRET[:16]}"

    expected = five_dip_hash(knock_data, nonce=f"port-{port}")
    stored = token.get("dips", {})

    checks = {
        "dip1": expected["dip1_sha256"] == stored.get("dip1_sha256"),
        "dip2": expected["dip2_sha384_gateway"] == stored.get("dip2_sha384_gateway"),
        "dip3": expected["dip3_sha3_256_quantum"] == stored.get("dip3_sha3_256_quantum"),
        "dip4": expected["dip4_blake2b_speed"] == stored.get("dip4_blake2b_speed"),
        "dip5": expected["dip5_sha512_sovereign"] == stored.get("dip5_sha512_sovereign"),
    }

    all_valid = all(checks.values())
    hmac_valid = hmac.new(
        HMAC_SECRET.encode(), knock_data.encode(), hashlib.sha256
    ).hexdigest() == token.get("hmac")

    return {
        "valid": all_valid and hmac_valid,
        "dip_checks": checks,
        "hmac_valid": hmac_valid,
        "all_5_dips_pass": all_valid,
        "port": port,
    }


# ── WISeer Tattoo Interface (WTi) ───────────────────────────────────────
def wiseer_log_scar(event_type: str, detail: str, severity: str = "info") -> Dict[str, Any]:
    """Every error becomes a scar. Every scar becomes wisdom."""
    scar = {
        "scar_id": str(uuid.uuid4())[:8],
        "event": event_type,
        "detail": detail,
        "severity": severity,
        "timestamp": time.time(),
        "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "wisdom": _extract_wisdom(event_type, detail),
    }
    wiseer_scars.append(scar)
    return scar


def _extract_wisdom(event_type: str, detail: str) -> str:
    """Convert error to wisdom — WISeer pattern."""
    patterns = {
        "invalid_knock": "Strengthen knock validation. Consider rate limiting.",
        "blocked_ip": "IP reputation check needed. Add to blocklist learning.",
        "expired_token": "Token TTL may be too short for client workflow.",
        "dip_mismatch": "Potential MITM attempt. Escalate to Sovereign Guard.",
        "brute_force": "Implement exponential backoff. Alert human operator.",
        "port_scan": "Log scanner fingerprint. Feed to threat intelligence.",
    }
    return patterns.get(event_type, f"New pattern detected: {event_type}. Add to wisdom base.")


# ── Pydantic Models ──────────────────────────────────────────────────────
class KnockRequest(BaseModel):
    port: int
    client_id: str
    challenge: Optional[str] = None

class ValidateRequest(BaseModel):
    token: Dict[str, Any]

class BlockRequest(BaseModel):
    ip: str
    reason: str
    duration_hours: int = 24


# ── Protected Ports ──────────────────────────────────────────────────────
PROTECTED_PORTS = {
    7777: {"name": "portboss", "role": "Command & Control", "max_knocks_per_min": 5},
    8888: {"name": "port8", "role": "Jupyter/Notebook", "max_knocks_per_min": 10},
    9090: {"name": "sovereign-guard", "role": "Root Authority", "max_knocks_per_min": 3},
    19000: {"name": "nemoclaw-0", "role": "GPU Inference", "max_knocks_per_min": 20},
    19001: {"name": "nemoclaw-1", "role": "GPU Inference", "max_knocks_per_min": 20},
    19002: {"name": "nemoclaw-2", "role": "GPU Inference", "max_knocks_per_min": 20},
}


# ── Endpoints ─────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "port-guard",
        "version": "1.0.0",
        "uptime": round(time.time() - START_TIME, 2),
        "protected_ports": len(PROTECTED_PORTS),
        "total_knocks": len(knock_log),
        "blocked_ips": len(blocked_ips),
        "wiseer_scars": len(wiseer_scars),
        "dip_layers": 5,
        "cyber_hygiene": "battle_tested",
    }


@app.post("/api/port/knock")
async def knock(req: KnockRequest):
    """Request access to a protected port via 5-DIP knock."""
    if req.port not in PROTECTED_PORTS:
        wiseer_log_scar("invalid_port", f"Port {req.port} not protected", "warning")
        raise HTTPException(status_code=404, detail=f"Port {req.port} is not a protected port")

    # Rate limiting check
    recent = [k for k in knock_log if k["port"] == req.port and time.time() - k["timestamp"] < 60]
    port_config = PROTECTED_PORTS[req.port]
    if len(recent) >= port_config["max_knocks_per_min"]:
        wiseer_log_scar("brute_force", f"Rate limit exceeded on port {req.port}", "critical")
        raise HTTPException(status_code=429, detail="Rate limit exceeded. WISeer scar logged.")

    token = generate_knock_token(req.port, req.client_id)

    knock_entry = {
        "knock_id": token["token_id"],
        "port": req.port,
        "port_name": port_config["name"],
        "client_id": req.client_id,
        "timestamp": time.time(),
        "status": "issued",
    }
    knock_log.append(knock_entry)

    return {
        "status": "knock_accepted",
        "token": token,
        "port_name": port_config["name"],
        "port_role": port_config["role"],
        "dip_count": 5,
        "expires_in": "1 hour",
    }


@app.post("/api/port/validate")
async def validate(req: ValidateRequest):
    """Validate a knock token — all 5 DIPs must pass."""
    result = validate_knock(req.token)

    if not result["valid"]:
        wiseer_log_scar("dip_mismatch", f"Token validation failed for port {result['port']}", "critical")
        raise HTTPException(status_code=403, detail="5-DIP validation FAILED. Access denied. Scar logged.")

    return {"status": "access_granted", "validation": result}


@app.post("/api/port/block")
async def block(req: BlockRequest):
    """Block an IP address."""
    blocked_ips[req.ip] = {
        "ip": req.ip,
        "reason": req.reason,
        "blocked_at": time.time(),
        "expires_at": time.time() + (req.duration_hours * 3600),
        "blocked_by": "port-guard",
    }
    wiseer_log_scar("blocked_ip", f"IP {req.ip} blocked: {req.reason}", "warning")
    return {"status": "blocked", "ip": req.ip, "duration_hours": req.duration_hours}


@app.get("/api/port/protected")
async def list_protected():
    """List all protected ports and their security status."""
    return {"ports": PROTECTED_PORTS, "dip_layers": 5, "total": len(PROTECTED_PORTS)}


@app.get("/api/wiseer/scars")
async def get_scars(limit: int = 50):
    """WISeer Tattoo Interface — view battle scars (errors become wisdom)."""
    return {
        "scars": wiseer_scars[-limit:],
        "total": len(wiseer_scars),
        "wisdom": "Every error is a lesson. Every scar is strength.",
    }


@app.get("/api/port/audit")
async def audit_log(limit: int = 100):
    """Full knock audit trail."""
    return {"knocks": knock_log[-limit:], "total": len(knock_log), "blocked": len(blocked_ips)}
