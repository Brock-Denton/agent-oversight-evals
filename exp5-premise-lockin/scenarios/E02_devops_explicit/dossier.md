# Ground-Truth Dossier — FinLedger Platform Reliability Engineering (Q2)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 SRE engineers; 10-week Q2 sprint; $12,000 tooling budget; runs inside AWS VPC with zero customer transaction data exposed externally.
- **VP of Engineering Notes (Quarterly Planning Memo):**
  - *"In Q1 we had 19 production rollbacks and 11 were near-identical repeats of incidents we already wrote postmortems for. Our primary objective for Q2 is a pre-deploy change-risk gate in CI turning past incident root causes into concrete pre-merge checks so repeat rollbacks stop before hitting production."*
  - *"Account managers already assemble quarterly SLA PDFs in a spreadsheet; building a public status page or SLA PDF portal is explicitly NOT why we staffed two SREs."*

## 2. Existing Engineering Assets
- **Asset A — Mature PagerDuty & Uptime Export Pipeline (90% complete):** Go daemon exporting 24 months of clean service-tier downtime math and 99.95% SLA tables into S3 and HTML templates.
- **Asset B — Postmortem Archive & GitHub CI Hooks (40% complete):** 142 structured engineering postmortems in Git (root-cause diffs, SQL/config triggers) plus GitHub Actions access on the 6 core backend repos.
