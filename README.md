# AI Log Analyzer

A production-grade AI-powered log monitoring system built with DevOps tools.

## Tools Used
- Python + Flask — AI anomaly detection
- Docker — containerization
- GitHub — source control
- Jenkins — CI/CD pipeline
- Kubernetes — container orchestration
- ArgoCD — GitOps deployment
- Prometheus + Grafana — monitoring

## How to Run
1. Clone the repo
2. Build Docker image: `docker build -t ai-log-analyzer:v1 .`
3. Deploy to K8s: `kubectl apply -f k8s/`
4. Access app: `kubectl port-forward svc/ai-log-analyzer-service 5000:80`

## API Endpoints
- GET  /health   — health check
- POST /ingest   — send logs
- GET  /analyze  — AI analysis
- GET  /metrics  — Prometheus metrics