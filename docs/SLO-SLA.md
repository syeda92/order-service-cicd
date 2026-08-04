# Order Service - SLO/SLA Definition

## SLI (Service Level Indicators) - kya measure karenge
- Availability: successful requests / total requests
- Latency: p95 response time
- Deployment success rate: successful deploys / total deploys

## SLO (Service Level Objectives) - internal target
- Availability: 99.5% (monthly)
- Latency: p95 < 300ms
- MTTR (Mean Time To Recovery): < 15 minutes
- Deployment frequency target: on-demand (multiple/day capable)

## SLA (Service Level Agreement) - external commitment
- Uptime commitment: 99% monthly (buffer rakha SLO se loose)
- Support response: P1 issue - 30 min ack

## Error Budget
- 99.5% SLO = 0.5% monthly error budget = ~3.6 hours downtime/month allowed
