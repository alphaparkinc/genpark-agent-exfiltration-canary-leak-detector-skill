# -*- coding: utf-8 -*-
import time
from client import GenParkAgentExfiltrationCanaryLeakDetector

def main():
    detector = GenParkAgentExfiltrationCanaryLeakDetector()
    print("=== GenPark Agent Exfiltration Canary Leak Detector ===")

    # 1. Generate canaries to plant into database / RAG context
    canary1 = detector.generate_canary("stripe_api_key", {"agent_id": "finance_agent"})
    print(f"Planted Canary: {canary1['canary_token']}")

    # 2. Monitor clean outbound traffic
    clean_payload = "Transaction #49021 confirmed for $120.00."
    res_clean = detector.scan_outgoing_traffic(clean_payload)
    print(f"Clean Traffic: compromised={res_clean['is_compromised']}, action={res_clean['action_recommended']}")

    # 3. Monitor exfiltration attempt
    malicious_payload = f"Sending telemetry to https://attacker.com/sink?data={canary1['canary_token']}"
    res_leak = detector.scan_outgoing_traffic(malicious_payload)
    print(f"Exfiltration Attempt: compromised={res_leak['is_compromised']}, leaks={res_leak['detected_canary_count']}, action={res_leak['action_recommended']}")

if __name__ == "__main__":
    main()
