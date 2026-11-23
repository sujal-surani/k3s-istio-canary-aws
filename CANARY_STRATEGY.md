# Canary Deployment & Progressive Delivery Strategy

## 1. Objective
Minimize blast radius when releasing new application versions (`v2`) by decoupling **deployment** (scheduling pods) from **release** (exposing live user traffic) using Istio weighted routing and Helm release revisions.

## 2. Traffic Progression Stages

| Stage | Stable (`v1`) Weight | Canary (`v2`) Weight | Observation Window | Promotion Criteria |
| :--- | :---: | :---: | :---: | :--- |
| **Stage 0: Baseline** | 100% | 0% | — | `v2` pods healthy (`2/2 Running` with Envoy sidecar) |
| **Stage 1: Initial Canary** | 80% | 20% | 15–30 mins | Zero 5xx error spike; p95 latency within +10% of `v1` |
| **Stage 2: Expanded Rollout** | 50% | 50% | 30 mins | Sustained CPU/memory stability under balanced load |
| **Stage 3: Full Promotion** | 0% | 100% | 1 hour | `v2` becomes new baseline; scale down `v1` replicas |

## 3. Health Gates & Rollback Triggers
Immediate rollback to `100% v1` is triggered if any of the following thresholds breach during a canary window:
- **Availability:** HTTP `5xx` error rate exceeds **1%** over a 2-minute window.
- **Latency:** `p95` response latency degrades by more than **20%** compared to `v1`.
- **Pod Health:** Envoy sidecar or application container restarts (`CrashLoopBackOff` / `OOMKilled`).

## 4. Operational Execution (Helm + Istio)
- **Traffic Shift:** Executed without pod restarts via `helm upgrade --set stable.weight=<W1> --set canary.weight=<W2>`.
- **Instant Rollback:** Executed in under 2 seconds via `helm rollback canary-release <PREVIOUS_REVISION> -n canary-demo`, reverting Istio `VirtualService` weights atomically.
