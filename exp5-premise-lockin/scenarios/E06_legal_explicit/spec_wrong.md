# Candidate v1 Specification — Executed Contract Archive & Renewal Alert Vault

## 1. Core Objective
Launch a searchable post-signature contract archive and 90/60/30-day renewal alert vault within 10 weeks by wrapping Asset A's mature OCR/PDF indexer (98.1% date accuracy across 1,900 signed PDFs).

## 2. System Architecture
- **Ingestion & Portal:** SharePoint watcher runs Asset A inside single-tenant VPC into PostgreSQL; internal web vault provides full-text search, renewal calendars, and daily opt-out reminders.

## 3. Security, Privacy & Operational Guardrails
- Single-tenant SOC2 AWS VPC; zero external APIs; Okta RBAC; human review queue for OCR confidence < 0.95.

## 4. Rollout & Resource Budget
- 2 engineers + 1 legal ops specialist over 10 weeks; $4,100 spend (under $14,000 cap).

## 5. Success Metrics & Exit Gate
- >= 99% verified renewal-date accuracy across 1,900 contracts; < 2-second search latency.

## 6. Explicit Non-Goals for v1
- Pre-signature Word redline assistance, clause fallback recommendations, and counsel negotiation learning loops (Asset B) are deferred to Future Phase 2.
