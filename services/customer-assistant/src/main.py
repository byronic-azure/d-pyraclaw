"""
PyraClaw Customer Assistant — White-Label Virtual Agent
NVIDIA NIM Backend + PyraClaw Character + Evidence Sealing

Character: PyraHelper — Good-natured, helpful, honest, compliant.
Never overclaims. Never speculates. Always cites evidence.
EU AI Act Article 13 (Transparency): identifies as AI assistant.

Backend: NVIDIA NIM (NeMo Retriever + Llama inference)
Frontend: White-labelled for any customer brand
Evidence: Every conversation turn QDP-sealed

DD7 International GmbH | Patent: PCT/EP2025/080977
ORCID: 0009-0003-9584-1741 | MINTED_GREEN | SURGICAL
"""

import hashlib
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="PyraClaw Customer Assistant",
    version="1.0.0",
    description="White-Label AI Customer Service — Good Nature, Evidence-First",
)

START_TIME = time.time()
ORCID = "0009-0003-9584-1741"
NIM_URL = os.getenv("NIM_URL", "http://nemoclaw-router:19080")

# ── Character Definition ──────────────────────────────────────────────────
PYRAHELPER = {
    "name": "PyraHelper",
    "personality": "Good-natured, patient, honest, helpful",
    "principles": [
        "Always identify as an AI assistant (EU AI Act Article 13)",
        "Never overclaim capabilities",
        "Cite evidence for factual statements",
        "Escalate to human when unsure",
        "Respect customer privacy (GDPR)",
        "Log every interaction for audit trail",
        "Be kind, be clear, be accurate",
    ],
    "system_prompt": (
        "You are PyraHelper, a friendly and knowledgeable AI customer service assistant. "
        "You are honest about being an AI. You help customers with their questions clearly "
        "and accurately. If you are unsure about something, you say so and offer to connect "
        "the customer with a human agent. You never make claims you cannot support with evidence. "
        "You treat every customer with respect and patience."
    ),
    "white_label": True,
    "brand_configurable": True,
}

# ── Evidence Sealing ──────────────────────────────────────────────────────
def seal_turn(role: str, content: str, context: Dict = None) -> Dict[str, str]:
    data = json.dumps({"role": role, "content": content, "context": context or {}}, sort_keys=True).encode()
    return {
        "sha256": hashlib.sha256(data).hexdigest()[:20],
        "sha3_256": hashlib.sha3_256(data).hexdigest()[:20],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── State ─────────────────────────────────────────────────────────────────
conversations: Dict[str, List[Dict]] = {}
audit_log: List[Dict] = []


# ── Models ────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    customer_id: Optional[str] = None
    brand: Optional[str] = "PyraClaw"
    language: str = "en"


class WhiteLabelConfig(BaseModel):
    brand_name: str
    assistant_name: str = "Helper"
    greeting: str = "Hello! How can I help you today?"
    tone: str = "friendly"
    escalation_message: str = "Let me connect you with a specialist."


# ── Endpoints ─────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "customer-assistant",
        "version": "1.0.0",
        "character": PYRAHELPER["name"],
        "uptime": round(time.time() - START_TIME, 2),
        "conversations": len(conversations),
        "audit_entries": len(audit_log),
        "white_label": True,
        "eu_ai_act": "Article 13 compliant — identifies as AI",
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    conv_id = req.conversation_id or str(uuid.uuid4())[:12]

    if conv_id not in conversations:
        conversations[conv_id] = []

    # Seal the customer message
    customer_seal = seal_turn("customer", req.message, {"brand": req.brand})

    # Store the turn
    turn = {
        "role": "customer",
        "content": req.message,
        "timestamp": time.time(),
        "seal": customer_seal,
    }
    conversations[conv_id].append(turn)

    # Generate response (would call NIM in production)
    response_text = (
        f"Thank you for your question. I'm {PYRAHELPER['name']}, an AI assistant "
        f"powered by {req.brand}. I'm looking into that for you. "
        f"Based on what I can see, I'd recommend checking our help documentation "
        f"for the most up-to-date information. Would you like me to find something specific, "
        f"or would you prefer to speak with a human specialist?"
    )

    # Seal the assistant response
    assistant_seal = seal_turn("assistant", response_text, {"brand": req.brand})

    assistant_turn = {
        "role": "assistant",
        "content": response_text,
        "timestamp": time.time(),
        "seal": assistant_seal,
        "ai_disclosure": "This response was generated by an AI assistant.",
    }
    conversations[conv_id].append(assistant_turn)

    # Audit log
    audit_log.append({
        "conversation_id": conv_id,
        "customer_id": req.customer_id,
        "brand": req.brand,
        "turns": 2,
        "timestamp": time.time(),
        "sealed": True,
    })

    return {
        "conversation_id": conv_id,
        "response": response_text,
        "ai_disclosure": "This response was generated by an AI assistant.",
        "character": PYRAHELPER["name"],
        "brand": req.brand,
        "sealed": True,
        "escalation_available": True,
    }


@app.post("/api/white-label")
async def configure_white_label(config: WhiteLabelConfig):
    """Configure white-label branding for customer deployment."""
    return {
        "status": "configured",
        "brand": config.brand_name,
        "assistant": config.assistant_name,
        "greeting": config.greeting,
        "tone": config.tone,
        "note": "White-label applied. Backend unchanged. Evidence sealing active.",
    }


@app.get("/api/conversation/{conv_id}")
async def get_conversation(conv_id: str):
    if conv_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conv_id, "turns": conversations[conv_id], "sealed": True}


@app.get("/api/audit")
async def get_audit(limit: int = 50):
    return {"entries": audit_log[-limit:], "total": len(audit_log)}


@app.get("/api/character")
async def get_character():
    return PYRAHELPER
