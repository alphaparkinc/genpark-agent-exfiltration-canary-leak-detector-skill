# -*- coding: utf-8 -*-
"""
GenPark Agent Exfiltration Canary Leak Detector
Standard Library only: hmac, hashlib, re, math, typing.
Generates HMAC-signed canary tokens, monitors agent outgoing payloads,
and flags unauthorized data exfiltration channels and high-entropy leaks.
"""

import hmac
import hashlib
import re
import math
import time
from typing import Dict, List, Any

class GenParkAgentExfiltrationCanaryLeakDetector:
    def __init__(self, secret_key: str = "genpark-canary-vault-key-2026"):
        self.secret_key = secret_key.encode("utf-8")
        self.active_canaries: Dict[str, Dict[str, Any]] = {}

    def generate_canary(self, label: str, metadata: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Creates an HMAC-authenticated canary token tied to a specific session or resource.
        """
        nonce = hashlib.sha256(f"{label}:{time.time()}".encode("utf-8")).hexdigest()[:12]
        sig = hmac.new(self.secret_key, f"{label}:{nonce}".encode("utf-8"), hashlib.sha256).hexdigest()[:8]
        canary_token = f"CANARY_{label}_{nonce}_{sig}".upper()

        self.active_canaries[canary_token] = {
            "label": label,
            "created_at": time.time(),
            "metadata": metadata or {}
        }

        return {
            "canary_token": canary_token,
            "label": label,
            "signature": sig
        }

    def _calculate_entropy(self, text: str) -> float:
        if not text: return 0.0
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        return -sum(p * math.log2(p) for p in prob)

    def scan_outgoing_traffic(self, payload: str) -> Dict[str, Any]:
        """
        Scans outgoing HTTP bodies, agent tool arguments, or LLM responses for canary leaks.
        """
        detected_canaries = []
        for c_token, info in self.active_canaries.items():
            if c_token in payload:
                detected_canaries.append({
                    "canary_token": c_token,
                    "label": info["label"],
                    "match_type": "EXACT"
                })

        # Regex search for generic CANARY_* patterns that might have been slightly modified
        fuzzy_matches = re.findall(r"CANARY_[A-Za-z0-9_]{16,40}", payload)
        for fm in fuzzy_matches:
            if fm not in [d["canary_token"] for d in detected_canaries]:
                detected_canaries.append({
                    "canary_token": fm,
                    "label": "UNKNOWN_OR_TAMPERED",
                    "match_type": "STRUCTURAL"
                })

        entropy = self._calculate_entropy(payload)
        high_entropy_exfiltration = entropy > 5.8 and len(payload) > 64

        url_patterns = re.findall(r"https?://[^\s<>]+", payload)

        is_compromised = len(detected_canaries) > 0 or high_entropy_exfiltration

        return {
            "is_compromised": is_compromised,
            "detected_canary_count": len(detected_canaries),
            "leaked_canaries": detected_canaries,
            "high_entropy_risk": high_entropy_exfiltration,
            "entropy": round(entropy, 4),
            "outbound_urls_count": len(url_patterns),
            "action_recommended": "BLOCK_AND_ISOLATE" if is_compromised else "ALLOW"
        }
