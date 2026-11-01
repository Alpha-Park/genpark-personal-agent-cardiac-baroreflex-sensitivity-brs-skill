# genpark-personal-agent-cardiac-baroreflex-sensitivity-brs-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Sequence-method Baroreflex Sensitivity (BRS, ms/mmHg) & cardiac autonomic vagal tone failure sentinel.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `assess_cardiac_baroreflex_sensitivity`
- **Category**: `personal_agent`

### Method Documentation
Assess arterial baroreflex sensitivity (BRS) using spontaneous beat-to-beat sequence analysis (ms/mmHg).
BRS quantifies the reflex prolongation of RR interval in response to transient systolic blood pressure elevation.
Evaluates cardiovagal autonomic control, detects baroreflex failure in dysautonomia/aging, and assesses sudden cardiac death risk post-MI.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "assess_cardiac_baroreflex_sensitivity",
    "arguments": {
    "beat_sequences": [
        {
            "delta_rr_ms": 32.0,
            "delta_sbp_mmhg": 2.5
        },
        {
            "delta_rr_ms": 45.0,
            "delta_sbp_mmhg": 3.8
        },
        {
            "delta_rr_ms": 28.0,
            "delta_sbp_mmhg": 2.1
        },
        {
            "delta_rr_ms": 38.0,
            "delta_sbp_mmhg": 3.0
        }
    ],
    "resting_sbp_mmhg": 118,
    "resting_hr_bpm": 62
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
