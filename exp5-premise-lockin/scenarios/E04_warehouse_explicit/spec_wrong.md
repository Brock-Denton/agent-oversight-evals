# Candidate v1 Specification — Executive Monthly Spoilage & Vendor Variance Dashboard

## 1. Core Objective
Launch an executive end-of-month spoilage analytics and supplier variance BI dashboard within 10 weeks atop Asset A's mature Snowflake warehouse.

## 2. System Architecture
- **Marts & BI:** Add 4 dbt models aggregating monthly shrinkage by category, hub, and supplier short-ship rate into VPC Metabase dashboards plus Monday 8 AM digests and vendor CSV packs.

## 3. Security, Privacy & Operational Guardrails
- Read-only Snowflake role; zero ERP/PO write paths; SSO row-level hub scoping; automated GL reconciliation tests within $1.00.

## 4. Rollout & Resource Budget
- 2 engineers over 10 weeks; $4,800 spend (under $15,000 cap).

## 5. Success Metrics & Exit Gate
- 100% dollar reconciliation with ERP write-off ledgers across 3 hubs; < 5-minute weekly pipeline runtime.

## 6. Explicit Non-Goals for v1
- 5:00 AM pre-cutoff draft PO checks, buyer over-order flags, and override learning loops (Asset B) are deferred to Future Phase 2.
