"""
PyraClaw NVIDIA API Service — Sovereign GPU Inference Gateway
Connects to NVIDIA NIM (build.nvidia.com) for Nemotron + Vision models.
Routes inference through QDP-sealed evidence pipeline.

Endpoints:
  /health          — Service health + model availability
  /api/models      — List available NVIDIA models
  /api/chat        — Chat completion (Nemotron)
  /api/vision      — Vision analysis (Nemotron Vision)
  /api/embeddings  — Text embeddings (NV-Embed)
  /api/verify-key  — Validate NVIDIA API key without storing

DD7 International GmbH | Patent: PCT/EP2025/080977
ORCID: 0009-0003-9584-1741 | MINTED_GREEN | SURGICAL
"""

import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

app = FastAPI(
    title="PyraClaw NVIDIA API Gateway",
    version="1.0.0",
    description="Sovereign GPU inference via NVIDIA NIM",
)

START_TIME = time.time()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_NEMOTRON_MODEL = os.getenv(
    "NVIDIA_NEMOTRON_DEFAULT_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1"
)
NVIDIA_VISION_MODEL = os.getenv(
    "NVIDIA_NEMOTRON_VISION_MODEL", "nvidia/llama-3.2-nv-vision-90b"
)
NVIDIA_EMBED_MODEL = os.getenv(
    "NVIDIA_EMBED_MODEL", "nvidia/nv-embedqa-e5-v5"
)

# QDP seal for evidence
def qdp_seal(data: str) -> Dict[str, str]:
    raw = data.encode("utf-8")
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sha512": hashlib.sha512(raw).hexdigest()[:32],
        "sha3_256": hashlib.sha3_256(raw).hexdigest(),
        "sha3_512": hashlib.sha3_512(raw).hexdigest()[:32],
    }


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }


def _check_key():
    if not NVIDIA_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="NVIDIA API key not configured. Run: bash scripts/configure.sh",
        )


# ── Request/Response Models ─────────────────────────────────
class ChatMessage(BaseModel):
    role: str = "user"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=4096)
    stream: bool = False


class VisionRequest(BaseModel):
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    prompt: str = "Describe this image in detail."
    model: Optional[str] = None
    max_tokens: int = Field(default=1024, ge=1, le=4096)


class EmbeddingRequest(BaseModel):
    input: List[str]
    model: Optional[str] = None


# ── Health ───────────────────────────────────────────────────
@app.get("/health")
async def health():
    key_status = "configured" if NVIDIA_API_KEY else "missing"
    return {
        "status": "healthy",
        "service": "nvidia-api",
        "version": "1.0.0",
        "nvidia_key": key_status,
        "base_url": NVIDIA_BASE_URL,
        "default_model": NVIDIA_NEMOTRON_MODEL,
        "vision_model": NVIDIA_VISION_MODEL,
        "uptime": round(time.time() - START_TIME, 2),
    }


# ── List Models ──────────────────────────────────────────────
@app.get("/api/models")
async def list_models():
    _check_key()
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{NVIDIA_BASE_URL}/models", headers=_headers())
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()


# ── Chat Completion ──────────────────────────────────────────
@app.post("/api/chat")
async def chat(req: ChatRequest):
    _check_key()
    model = req.model or NVIDIA_NEMOTRON_MODEL
    payload = {
        "model": model,
        "messages": [m.model_dump() for m in req.messages],
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            headers=_headers(),
            json=payload,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        result = resp.json()

    # QDP-seal the response for evidence
    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    seal = qdp_seal(content)

    return {
        "model": model,
        "response": content,
        "usage": result.get("usage", {}),
        "seal": seal,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Vision ───────────────────────────────────────────────────
@app.post("/api/vision")
async def vision(req: VisionRequest):
    _check_key()
    model = req.model or NVIDIA_VISION_MODEL

    # Build the vision message
    content_parts = [{"type": "text", "text": req.prompt}]
    if req.image_url:
        content_parts.append({
            "type": "image_url",
            "image_url": {"url": req.image_url},
        })
    elif req.image_base64:
        content_parts.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{req.image_base64}"},
        })
    else:
        raise HTTPException(status_code=400, detail="Provide image_url or image_base64")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content_parts}],
        "max_tokens": req.max_tokens,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            headers=_headers(),
            json=payload,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        result = resp.json()

    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    seal = qdp_seal(content)

    return {
        "model": model,
        "analysis": content,
        "usage": result.get("usage", {}),
        "seal": seal,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Embeddings ───────────────────────────────────────────────
@app.post("/api/embeddings")
async def embeddings(req: EmbeddingRequest):
    _check_key()
    model = req.model or NVIDIA_EMBED_MODEL
    payload = {
        "model": model,
        "input": req.input,
        "input_type": "query",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{NVIDIA_BASE_URL}/embeddings",
            headers=_headers(),
            json=payload,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        result = resp.json()

    return {
        "model": model,
        "embeddings": result.get("data", []),
        "usage": result.get("usage", {}),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── Verify Key ───────────────────────────────────────────────
@app.post("/api/verify-key")
async def verify_key(request: Request):
    """Test an NVIDIA API key without storing it."""
    body = await request.json()
    key = body.get("key", "")
    if not key:
        raise HTTPException(status_code=400, detail="Provide 'key' in request body")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{NVIDIA_BASE_URL}/models", headers=headers)

    if resp.status_code == 200:
        models = resp.json()
        model_count = len(models.get("data", []))
        return {"valid": True, "models_available": model_count}
    elif resp.status_code == 401:
        return {"valid": False, "error": "Unauthorized — invalid key"}
    else:
        return {"valid": False, "error": f"HTTP {resp.status_code}"}
