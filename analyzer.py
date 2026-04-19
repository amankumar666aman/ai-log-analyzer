import re
from collections import Counter
from datetime import datetime

PATTERNS = [
    (r"\bERROR\b", "error", "high"),
    (r"\bCRITICAL\b", "critical", "critical"),
    (r"\bFATAL\b", "fatal", "critical"),
    (r"\bfailed\b", "failed", "medium"),
    (r"\btimeout\b", "timeout", "medium"),
    (r"\bwarning\b", "warning", "low"),
]

SEV = {"low": 1, "medium": 2, "high": 3, "critical": 4}

def analyze_logs(logs):
    found = []
    sev = Counter()
    pat = Counter()
    for e in logs:
        msg = e["message"].lower()
        hits = []
        for p, label, s in PATTERNS:
            if re.search(p, msg, re.IGNORECASE):
                hits.append({"label": label, "sev": s})
                sev[s] += 1
                pat[label] += 1
        if hits:
            top = max(hits, key=lambda x: SEV.get(x["sev"], 0))
            found.append({
                "log": e["message"],
                "time": e["timestamp"],
                "type": top["label"],
                "sev": top["sev"],
            })
    total = len(logs)
    score = max(0, 100 - (len(found) / max(total, 1)) * 100)
    return {
        "total": total,
        "anomalies": len(found),
        "score": round(score, 1),
        "breakdown": dict(sev),
        "items": found[:20]
    }
