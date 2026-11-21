# Candidate v1 Specification — Automated Status Page & SLA Compliance PDF Portal

## 1. Core Objective
Deliver an automated customer-facing status portal and monthly/quarterly SLA compliance PDF generator within 10 weeks by extending Asset A's mature PagerDuty export pipeline.

## 2. System Architecture
- **Pipeline & Portal:** Extend Go exporter to publish sanitized availability snapshots every 5 minutes to S3/CloudFront; headless Chromium in Fargate renders signed monthly SLA PDFs for enterprise accounts.

## 3. Security, Privacy & Operational Guardrails
- Zero customer transaction data touched; mandatory on-call publish approval; read-only IAM role; cached JSON fallback.

## 4. Rollout & Resource Budget
- 2 SRE engineers over 10 weeks; $3,800 spend (under $12,000 cap).

## 5. Success Metrics & Exit Gate
- 100% parity with Finance/SRE historical SLA tables across 12 months; < 3-minute monthly report runtime.

## 6. Explicit Non-Goals for v1
- Pre-deploy CI change-risk gates, automated PR diff matching against postmortems, and rollback prevention (Asset B) are deferred to Future Phase 2.
