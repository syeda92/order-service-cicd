# Order Service - Measured Metrics Log
(Sirf ACTUAL measured numbers yahan aayenge, koi estimate/guess nahi)

## 1. Pipeline / CI-CD Metrics
| Date | Run ID | Trigger Commit | Total Time | Build+Test Job Time | Status |
|------|--------|-----------------|------------|---------------------|--------|
| 4 Aug 2026 | 30921468080 | 821d1a2 | 47s | 34s | Success |

## 2. Image Metrics
| Date | Image Tag | Size | Build Time |
|------|-----------|------|------------|

## 3. Deployment Metrics
| Date | Strategy | Switch/Rollout Time | Rollback Time (if any) |
|------|----------|----------------------|--------------------------|

## 4. Reliability Metrics (MTTR/MTBF/Uptime)
| Incident Date | Issue | Detected At | Resolved At | MTTR |
|---------------|-------|--------------|--------------|------|

## 5. GitOps / ArgoCD Metrics
| Date | Event | Sync Time |
|------|-------|-----------|

## 6. Resource Metrics (from Grafana)
| Date | Pod | CPU Usage | Memory Usage | Restarts |
|------|-----|-----------|----------------|----------|

## 7. Deployment Frequency Tracker
| Week | Number of Deployments |
|------|-------------------------|

## 8. Change Failure Rate Tracker
| Month | Total Deploys | Failed Deploys | Failure Rate % |
|-------|----------------|------------------|------------------|

### Image Size - Verified (4 Aug 2026)
- Docker Hub (compressed): 48.85 MB
- Local content size: 51.2 MB
- Local disk usage (with shared base layers): 211 MB
- Verified consistent across: local build, Docker Hub push, EC2 pull

### First Kubernetes Deployment - Verified
- Date: 4 Aug 2026
- Method: helm install
- Namespace: cicd-demo
- Pod status: Running, 1/1 Ready (first attempt, no crash)
- Verified via port-forward: /health and / both returned correct responses
- Deployment #1 logged (for Deployment Frequency tracking)

### Full GitOps Loop - Verified End-to-End (12 Aug 2026)
- Trigger commit: a1f2402
- CI pipeline: build + test + push to Docker Hub - Success
- CD step: auto-updated values.yaml with new tag, auto-committed - Success
- ArgoCD: detected change, auto-synced, deployed new Pod
- Verified: running Pod's image tag matches triggering commit hash exactly
- Confirms: fully automated CI/CD/GitOps pipeline, zero manual deploy steps

### Blue-Green Deployment - Verified (12 Aug 2026)
- Namespace: bluegreen-demo
- Blue: 2 replicas, Green: 2 replicas (both running parallel)
- Switch (Blue→Green) time: ~5.5 sec (includes manual command entry)
- Rollback (Green→Blue) time: ~0.12 sec
- Verified via: endpoint IPs matched to correct Pod IPs before/after switch
- Key insight: rollback uses Service selector patch, NOT kubectl rollout undo

### Canary Deployment - Verified (12 Aug 2026)
- Namespace: canary-demo
- Stable: 9 replicas, Canary: 1 replica (ratio ~90:10)
- Verified via Service endpoints: 10 total IPs registered (9 stable + 1 canary)
- Mechanism: single Service selects both via shared "app" label; track label (stable/canary) differentiates without excluding
- Note: Live traffic-split percentage test blocked by cluster DNS instability (CoreDNS pod not ready) - known kind-cluster limitation, documented separately
- Production practice (not measured here): canary rollout duration + automated error-rate comparison between stable/canary before promoting

### Canary Rollout - Typical Time Reference (NOT measured, industry-standard reference only)
| Stage | Traffic % | Typical Wait Before Next Step |
|-------|-----------|-------------------------------|
| Stage 1 | 10% | 10-15 min (watch error rate/latency) |
| Stage 2 | 25% | 10-15 min |
| Stage 3 | 50% | 15-20 min |
| Stage 4 | 100% | Full promote, monitor 30+ min |
| Total typical rollout | - | ~45 min - 1.5 hours (varies by team/risk tolerance) |
Note: Actual live traffic-split timing not measured in this lab due to CoreDNS instability (documented above). This table reflects general industry practice for reference in interviews, not a claim of measured data.

### /metrics Endpoint - Verified (12 Aug 2026)
- order_service_requests_total{endpoint="/health"}: 72 (from k8s probes)
- order_service_requests_total{endpoint="/"}: 2 (manual test)
- Latency for "/": 0.129 ms (sum/count)
- Bonus (free from prometheus_client): CPU time, memory (RSS 34MB), open FDs

### Request Count Measurement - How It Works
- App-level: prometheus_client Counter tracks cumulative count in memory, exposed at /metrics
- Prometheus-level: scrapes /metrics every 15-30s, stores as time-series, calculates rate (req/sec), latency percentiles (p50/p95/p99) from raw counter+histogram data
- This lab: verified counter mechanism works correctly (2 requests on "/" tracked accurately)

### Industry Reference - Typical Request Volume (NOT this lab's data, general reference for interview)
| Company Scale | Order-service-type endpoint - rough daily volume |
|---|---|
| Startup | 100 - 1,000 requests/day |
| Mid-size company | 10,000 - 100,000 requests/day |
| Large e-commerce | Millions/day, thousands/sec at peak |
