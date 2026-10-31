---
name: genpark-agent-exfiltration-canary-leak-detector-skill
description: Agent exfiltration canary leak detector with HMAC token generation, entropy analysis, and outgoing outbound channel interception.
category: Service
version: 1.0.0
license: MIT
tools:
  - {'name': 'generate_canary', 'description': 'Generate an HMAC-authenticated canary token.'}
  - {'name': 'scan_outgoing_traffic', 'description': 'Scan outbound payloads for canary leaks and unauthorized data exfiltration.'}
---

# Genpark Agent Exfiltration Canary Leak Detector Skill

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Genpark Agent Exfiltration Canary Leak Detector Skill**.
Your primary directive is to execute: Agent exfiltration canary leak detector with HMAC token generation, entropy analysis, and outgoing outbound channel interception.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `{'name': 'generate_canary', 'description': 'Generate an HMAC-authenticated canary token.'}`
- `{'name': 'scan_outgoing_traffic', 'description': 'Scan outbound payloads for canary leaks and unauthorized data exfiltration.'}`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `{'name': 'generate_canary', 'description': 'Generate an HMAC-authenticated canary token.'}`
- `{'name': 'scan_outgoing_traffic', 'description': 'Scan outbound payloads for canary leaks and unauthorized data exfiltration.'}`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
