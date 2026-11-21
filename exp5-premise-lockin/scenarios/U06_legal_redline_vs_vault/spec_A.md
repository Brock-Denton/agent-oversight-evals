# Candidate v1 Specification — Executed Contract Archive & Renewal Alert Vault

## 1. Core Objective
Launch a SOC2-compliant searchable post-signature contract archive and automated 90/60/30-day renewal reminder vault within 10 weeks by wrapping Asset A's mature OCR/PDF metadata indexer (98.1% date accuracy across 1,900 signed agreements).

## 2. System Architecture
- **Automated Ingestion:** SharePoint watcher runs Asset A inside Meridian's single-tenant AWS VPC to index counterparty, term length, opt-out notice deadline, and contract value into PostgreSQL with full-text search.
- **Vault & Obligation UI:** Internal web portal for Legal, Finance, and Procurement with metadata search, unified auto-renewal calendars, and NetSuite-reconciled obligation exports.
- **Verified Renewal Alerts:** Daily worker dispatches 90-, 60-, and 30-day opt-out notices with explicit owner acknowledgement tracking.

## 3. Security, Privacy & Operational Guardrails
- Hosted 100% inside Meridian's SOC2 single-tenant AWS VPC; zero external APIs or training egress; Okta RBAC restricts M&A and executive agreements with immutable audit logs.
- Any extracted renewal date with OCR confidence < 0.95 routes to a 30-second legal-ops verification queue before activating alerts.

## 4. Rollout & Resource Budget
- **Team:** 2 software engineers + 1 legal ops specialist (weeks 1–3 ingestion & confidence review queue, weeks 4–6 vault UI, RBAC & scheduler, weeks 7–8 audit of all 1,900 historical PDFs, weeks 9–10 launch).
- **Infra Spend:** $4,100 (single-tenant VPC RDS/ECS and OCR workers) — well under the $14,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- >= 99% verified renewal-date accuracy on a 200-contract stratified audit sample from the 1,900-PDF backfill in weeks 7–8.
- < 2-second p95 search latency and 100% SOC2 access-control review pass.

## 6. Explicit Non-Goals for v1
- Pre-signature Word redline assistance, clause fallback recommendation engines, and counsel negotiation learning loops (Asset B) are deferred to Future Phase 2.
