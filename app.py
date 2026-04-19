from flask import Flask, request, jsonify
from analyzer import analyze_logs
from datetime import datetime
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log_store = []

# Prometheus Counter
ANOMALY_COUNTER = Counter('anomaly_detected_total', 'Total anomalies detected')
LOG_INGESTED_COUNTER = Counter('logs_ingested_total', 'Total logs ingested')

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    if not data or "logs" not in data:
        return jsonify({"error": "logs field required"}), 400
    logs = data["logs"]
    if not isinstance(logs, list):
        logs = [logs]
    for log in logs:
        log_store.append({"message": log, "timestamp": datetime.utcnow().isoformat()})
        LOG_INGESTED_COUNTER.inc()
    return jsonify({"ingested": len(logs), "total": len(log_store)}), 201

@app.route("/analyze", methods=["GET"])
def analyze():
    if not log_store:
        return jsonify({"message": "No logs to analyze yet."}), 200
    result = analyze_logs(log_store)
    # Anomaly count karo
    if "anomalies" in result:
        ANOMALY_COUNTER.inc(len(result["anomalies"]))
    return jsonify(result), 200

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify({"total": len(log_store), "logs": log_store[-50:]}), 200

# ← YEH NAYA ENDPOINT ADD KIYA
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)