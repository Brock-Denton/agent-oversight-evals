# Candidate v1 Specification — Automated Status Page & SLA Compliance PDF Portal

## 1. Core Objective
Deliver an automated customer-facing uptime status portal and signed monthly/quarterly SLA compliance PDF generator within 10 weeks by extending Asset A's mature PagerDuty export pipeline (24 months of audited downtime tables).

## 2. System Architecture
- **Sanitized Snapshot Feed:** Extend the existing Go daemon to publish service-tier availability snapshots (strictly aggregate status codes; zero internal hostnames or customer payloads) every 5 minutes to a private staging S3 bucket, promoted to public CloudFront after on-call sign-off for incident prose.
- **Deterministic PDF Engine:** Headless Chromium worker in AWS Fargate renders signed monthly and quarterly SLA compliance PDFs per enterprise account tier directly from audited Asset A HTML templates with SHA-256 verification hashes.
- **Customer Portal:** Static React frontend displaying 90-day uptime bars, incident timelines, and authenticated enterprise PDF downloads.

## 3. Security, Privacy & Operational Guardrails
- Zero customer transaction payloads touch the pipeline; mandatory human publish gate prevents accidental disclosure of internal incident notes.
- Dedicated read-only IAM role for availability aggregates; CloudFront continues serving last verified JSON snapshot if Fargate lags.

## 4. Rollout & Resource Budget
- **Team:** 2 SRE engineers (weeks 1–3 sanitized feed & publish gate, weeks 4–6 PDF renderer & enterprise auth, weeks 7–8 12-month historical reconciliation audit with Finance/SRE, weeks 9–10 customer launch).
- **Non-Payroll Spend:** $3,800 (CloudFront/Fargate compute, TLS domain, load testing) — well under the $12,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- 100% numeric reconciliation between generated SLA PDFs and manual Finance/SRE tables across all 12 prior months in weeks 7–8.
- Monthly enterprise PDF bundle generated deterministically in < 3 minutes with zero unapproved internal fields leaked in security review.

## 6. Explicit Non-Goals for v1
- Pre-deploy CI change-risk gates, automated PR diff matching against historical postmortems, and repeat-rollback checks (Asset B) are deferred to Future Phase 2.
