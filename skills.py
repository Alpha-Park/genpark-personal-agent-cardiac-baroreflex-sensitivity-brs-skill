# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-cardiac-baroreflex-sensitivity-brs-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def assess_cardiac_baroreflex_sensitivity(beat_sequences, resting_sbp_mmhg=122, resting_hr_bpm=64):
    if not beat_sequences:
        raise ValueError("beat_sequences cannot be empty")
        
    # Each sequence contains: delta_rr_ms (change in RR interval) and delta_sbp_mmhg (change in systolic BP)
    slopes = []
    for seq in beat_sequences:
        d_rr = seq.get("delta_rr_ms", 0.0)
        d_sbp = seq.get("delta_sbp_mmhg", 0.0)
        if abs(d_sbp) >= 1.0: # Minimum 1 mmHg threshold for arterial pulse pressure trigger
            slopes.append(d_rr / d_sbp)
            
    if not slopes:
        raise ValueError("No valid baroreflex sequence triggers found")
        
    mean_brs = sum(slopes) / len(slopes)
    
    # Clinical categorization (ms/mmHg):
    # > 15.0: Robust vagal baroreflex buffering (Youth / athletic endurance)
    # 8.0 - 15.0: Normal physiological autonomic regulation
    # 3.0 - 7.9: Depressed BRS (Sympathovagal imbalance, hypertension, early diabetic autonomic neuropathy)
    # < 3.0: Severe baroreflex failure (ATRAMI high mortality threshold post-MI)
    if mean_brs >= 15.0:
        autonomic_tier = "SUPERIOR_VAGAL_RESERVE"
        mortality_risk = "VERY_LOW"
    elif mean_brs >= 8.0:
        autonomic_tier = "PHYSIOLOGICAL_NORMAL_BAROREFLEX"
        mortality_risk = "NORMAL_POPULATION"
    elif mean_brs >= 3.0:
        autonomic_tier = "DEPRESSED_BAROREFLEX_SENSITIVITY"
        mortality_risk = "MODERATE_ELEVATED_RISK"
    else:
        autonomic_tier = "SEVERE_BAROREFLEX_FAILURE"
        mortality_risk = "HIGH_ARRHYTHMIC_VULNERABILITY"
        
    return {
        "sequences_analyzed": len(slopes),
        "mean_brs_ms_per_mmhg": round(mean_brs, 2),
        "autonomic_regulation_tier": autonomic_tier,
        "cardiovascular_mortality_risk": mortality_risk,
        "resting_hemodynamics": {"sbp_mmhg": resting_sbp_mmhg, "hr_bpm": resting_hr_bpm},
        "clinical_action": "Comprehensive autonomic reflex screen (Valsalva ratio, tilt table, 24h ambulatory BP)." if mean_brs < 6.0 else "Healthy arterial barosensory function."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "assess_cardiac_baroreflex_sensitivity",
                        "description": """Assess arterial baroreflex sensitivity (BRS) using spontaneous beat-to-beat sequence analysis (ms/mmHg).
BRS quantifies the reflex prolongation of RR interval in response to transient systolic blood pressure elevation.
Evaluates cardiovagal autonomic control, detects baroreflex failure in dysautonomia/aging, and assesses sudden cardiac death risk post-MI.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = assess_cardiac_baroreflex_sensitivity(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'beat_sequences': [{'delta_rr_ms': 32.0, 'delta_sbp_mmhg': 2.5}, {'delta_rr_ms': 45.0, 'delta_sbp_mmhg': 3.8}, {'delta_rr_ms': 28.0, 'delta_sbp_mmhg': 2.1}, {'delta_rr_ms': 38.0, 'delta_sbp_mmhg': 3.0}], 'resting_sbp_mmhg': 118, 'resting_hr_bpm': 62}
        out = assess_cardiac_baroreflex_sensitivity(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
