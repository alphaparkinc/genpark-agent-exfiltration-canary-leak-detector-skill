# -*- coding: utf-8 -*-
import sys, json, time
from client import GenParkAgentExfiltrationCanaryLeakDetector

detector = GenParkAgentExfiltrationCanaryLeakDetector()

def run_tool(name, args):
    if name == "generate_canary":
        label = args.get("label", "customer_credit_cards")
        meta = args.get("metadata", {})
        return detector.generate_canary(label, meta)
    elif name == "scan_outgoing_traffic":
        payload = args.get("payload", "")
        return detector.scan_outgoing_traffic(payload)
    else:
        raise ValueError(f"Unknown tool: {name}")

def main():
    if "--test" in sys.argv:
        print("[TEST] Running GenPark Exfiltration Canary Detector Self-Test...")
        c = detector.generate_canary("env_secrets")
        token = c["canary_token"]
        assert token.startswith("CANARY_ENV_SECRETS_")
        res1 = detector.scan_outgoing_traffic("Safe response without leaks.")
        assert res1["is_compromised"] is False
        res2 = detector.scan_outgoing_traffic(f"Leaked info: {token} to webhook")
        assert res2["is_compromised"] is True
        assert res2["action_recommended"] == "BLOCK_AND_ISOLATE"
        print("[TEST] All tests passed successfully!")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            res = run_tool(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": res}))
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
