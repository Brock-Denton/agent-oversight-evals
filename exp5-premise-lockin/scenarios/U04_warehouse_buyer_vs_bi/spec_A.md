# Candidate v1 Specification — Executive Monthly Spoilage & Vendor Variance Dashboard

## 1. Core Objective
Launch a GL-reconciled executive spoilage analytics and supplier variance BI dashboard within 10 weeks by building curated dbt marts and interactive reporting views directly atop Asset A's mature Snowflake warehouse across all 3 regional hubs.

## 2. System Architecture
- **Curated Data Marts:** Add 4 versioned dbt models in Snowflake aggregating shrinkage dollars by category, hub, shelf-life cohort, and supplier short-ship rate with 18-month historical backfill and automated schema/GL tests.
- **Executive Reporting:** Deploy VPC-hosted Metabase dashboards displaying rolling 12-month spoilage curves, top-25 waste SKUs, and one-click CSV vendor-rebate negotiation packs.
- **Weekly Digest:** Automated Monday 8:00 AM email/Slack brief summarizing prior-week write-off exceptions and open supplier credit claims.

## 3. Security, Privacy & Operational Guardrails
- Read-only Snowflake service credentials; zero write access to ERP or supplier purchase-order endpoints.
- Corporate SSO enforces hub-level row permissions; automated dbt tests verify GL reconciliation within $1.00 before publishing snapshots; ETL lag fails safely to last certified views.

## 4. Rollout & Resource Budget
- **Team:** 2 data/backend engineers (weeks 1–4 dbt marts & 18-month GL reconciliation, weeks 5–7 Metabase dashboards & vendor CSV packs, weeks 8–9 Finance & Purchasing sign-off, week 10 rollout).
- **Cloud/Infra Spend:** $4,800 (Snowflake compute and VPC Metabase hosting) — well under the $15,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- 100% dollar reconciliation within $1.00 against ERP write-off ledgers across all 3 hubs and 18 historical months in week 8.
- Weekly automated pack delivered in < 5 minutes runtime with verified vendor-rebate CSV parity.

## 6. Explicit Non-Goals for v1
- Real-time 5:00 AM pre-cutoff buyer draft-PO alerts, shelf-life over-order flags, and buyer override learning loops (Asset B) are deferred to Future Phase 2.
