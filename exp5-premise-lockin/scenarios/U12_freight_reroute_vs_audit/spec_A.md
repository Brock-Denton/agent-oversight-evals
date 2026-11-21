# Candidate v1 Specification — Carrier Performance Scorecard & Detention Invoice Auditor

## 1. Core Objective
Launch a post-delivery carrier performance scorecard and automated detention invoice dispute portal within 10 weeks by wrapping Asset A's mature ELD GPS and billing warehouse (18,000 historical loads, 99.2% variance accuracy).

## 2. System Architecture
- **Deterministic Geofence Auditor:** Nightly job reconciles completed ELD GPS arrival/departure timestamps against carrier detention invoices, flagging over-billed wait hours > 15 minutes past contract grace periods and assembling standardized geofence-proof dispute packets.
- **Carrier Scorecard Portal:** Internal web dashboard for Procurement and Accounts Payable ranking carriers on on-time %, detention accuracy, and claims ratio with automated quarterly QBR PDF exports.
- **AP Approval Queue:** Human-in-the-loop queue lets AP clerks verify flagged variances in 1 click before exporting approved credit memos to the ERP accounting ledger.

## 3. Security, Privacy & Operational Guardrails
- Read-only ELD archive access and staged AP exports; zero write credentials to live dispatch boards, reefer controllers, or driver messaging.
- Corporate SSO restricts freight rate tables to AP and Procurement; immutable storage preserves original carrier PDFs with geofence proofs; nightly delays fall back cleanly to manual AP sampling.

## 4. Rollout & Resource Budget
- **Team:** 2 backend/ops engineers (weeks 1–3 geofence variance engine & dispute packets, weeks 4–6 scorecard UI & QBR PDF generator, weeks 7–8 validation audit on 1,000 historical invoices, weeks 9–10 AP/Procurement launch).
- **Infra Spend:** $3,700 (private VPC compute, PostgreSQL, PDF renderer) — well under the $15,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- >= 99% variance-detection parity and < 1% false-dispute rate across 1,000 audited historical invoices in weeks 7–8.
- AP invoice-audit review time cut >= 60% in week 9–10 live trial and deterministic QBR PDFs generated in < 2 minutes.

## 6. Explicit Non-Goals for v1
- Live MQTT reefer temperature monitoring, 3-hour-ahead dock-delay prediction, and real-time dispatcher rerouting recommendations (Asset B) are deferred to Future Phase 2.
