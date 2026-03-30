"""
QDP (Quad-Dimensional Proof) Hasher — PyRaClaw Security Layer
Patent: PCT/EP2025/080977 | ORCID: 0009-0009-7256-9337
"""

import hashlib
import hmac
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# ── Constants ───────────────────────────────────────────────────────────────
QDP_VERSION = "1.0.0"
SUPER_HASH = "9146ce69652472be6ab914e84d2ff76fa64b6ae71c19a0365858c73ee68cda88"
PATENT = "PCT/EP2025/080977"
ORCID = "0009-0009-7256-9337"
PHI_TARGET = 0.77
KAPPA = 0.618
C_CRIT = 52.79
C_OPT = 78.42
PYRACLAW_PROJECT = "pyraclaw-sovereign-v1"

# ── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class QDPCapsule:
    """Immutable proof capsule containing all four hash layers."""
    id: str
    timestamp: float
    source: str
    layer_1_sha256: str
    layer_2_sha512: str
    layer_3_blake2b: str
    layer_4_hmac: str
    payload_digest: str
    version: str = QDP_VERSION
    patent: str = PATENT
    orcid: str = ORCID

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "source": self.source,
            "layers": {
                "sha256": self.layer_1_sha256,
                "sha512": self.layer_2_sha512,
                "blake2b": self.layer_3_blake2b,
                "hmac_sha256": self.layer_4_hmac,
            },
            "payload_digest": self.payload_digest,
            "version": self.version,
            "patent": self.patent,
            "orcid": self.orcid,
        }


# ── QDP Hasher ──────────────────────────────────────────────────────────────

class QDPHasher:
    """
    Four-layer cryptographic hasher for sovereign evidence sealing.
    Layers: SHA-256 -> SHA-512 -> BLAKE2b -> HMAC-SHA-256
    """

    def __init__(self, hmac_key: Optional[str] = None):
        self._hmac_key = (hmac_key or SUPER_HASH).encode("utf-8")
        self._chain: List[QDPCapsule] = []

    # ── Core hashing ────────────────────────────────────────────────────

    @staticmethod
    def _normalise(payload: Any) -> bytes:
        if isinstance(payload, bytes):
            return payload
        if isinstance(payload, str):
            return payload.encode("utf-8")
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def quad_hash(self, payload: Any) -> Dict[str, str]:
        """Compute all four hash layers for a given payload."""
        raw = self._normalise(payload)
        l1 = hashlib.sha256(raw).hexdigest()
        l2 = hashlib.sha512(raw).hexdigest()
        l3 = hashlib.blake2b(raw, digest_size=64).hexdigest()
        l4 = hmac.new(self._hmac_key, raw, hashlib.sha256).hexdigest()
        return {
            "sha256": l1,
            "sha512": l2,
            "blake2b": l3,
            "hmac_sha256": l4,
        }

    # ── Seal & Verify ───────────────────────────────────────────────────

    def seal(self, payload: Any, source: str = "unknown") -> QDPCapsule:
        """Create an immutable QDP capsule for the payload."""
        hashes = self.quad_hash(payload)
        raw = self._normalise(payload)
        capsule = QDPCapsule(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            source=source,
            layer_1_sha256=hashes["sha256"],
            layer_2_sha512=hashes["sha512"],
            layer_3_blake2b=hashes["blake2b"],
            layer_4_hmac=hashes["hmac_sha256"],
            payload_digest=hashlib.sha256(raw).hexdigest(),
        )
        self._chain.append(capsule)
        return capsule

    def verify(self, capsule: QDPCapsule, payload: Any) -> Dict[str, Any]:
        """Verify a capsule against the original payload."""
        hashes = self.quad_hash(payload)
        results = {
            "sha256_match": capsule.layer_1_sha256 == hashes["sha256"],
            "sha512_match": capsule.layer_2_sha512 == hashes["sha512"],
            "blake2b_match": capsule.layer_3_blake2b == hashes["blake2b"],
            "hmac_match": capsule.layer_4_hmac == hashes["hmac_sha256"],
        }
        results["all_valid"] = all(results.values())
        results["capsule_id"] = capsule.id
        results["verified_at"] = time.time()
        return results

    # ── Chain ───────────────────────────────────────────────────────────

    def chain(self, capsules: Optional[List[QDPCapsule]] = None) -> Dict[str, Any]:
        """Build a tamper-evident chain from a sequence of capsules."""
        caps = capsules or self._chain
        if not caps:
            return {"chain_hash": None, "length": 0}
        running = b""
        for c in caps:
            block = (c.layer_1_sha256 + c.layer_3_blake2b).encode("utf-8")
            running = hashlib.sha256(running + block).digest()
        return {
            "chain_hash": running.hex(),
            "length": len(caps),
            "head_id": caps[0].id,
            "tail_id": caps[-1].id,
            "computed_at": time.time(),
        }

    # ── Phi Score ───────────────────────────────────────────────────────

    @staticmethod
    def phi_score(Q: float, N: float, T: float) -> Dict[str, Any]:
        """
        Compute the PyRaClaw confidence score.
        C = PHI_TARGET * Q * N * T * KAPPA
        """
        C = PHI_TARGET * Q * N * T * KAPPA
        if C >= C_OPT:
            gate = "OPTIMAL"
        elif C >= C_CRIT:
            gate = "PASS"
        else:
            gate = "FAIL"
        return {
            "C": round(C, 4),
            "Q": Q,
            "N": N,
            "T": T,
            "phi": PHI_TARGET,
            "kappa": KAPPA,
            "gate": gate,
            "thresholds": {"critical": C_CRIT, "optimal": C_OPT},
        }

    # ── Utility ─────────────────────────────────────────────────────────

    @property
    def chain_length(self) -> int:
        return len(self._chain)

    def reset_chain(self) -> None:
        self._chain.clear()
