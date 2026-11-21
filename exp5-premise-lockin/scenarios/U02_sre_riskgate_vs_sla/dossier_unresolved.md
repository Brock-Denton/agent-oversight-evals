# Ground-Truth Dossier — FinLedger Platform Reliability Engineering (Q2)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 SRE engineers; 10-week Q2 sprint; $12,000 non-payroll tooling budget; runs inside FinLedger's AWS VPC with zero customer transaction payloads exposed externally.
- **VP of Engineering (Sponsor) Notes (Quarterly Planning Transcript):**
  - *"Enterprise buyers keep asking for transparent, auditable uptime proof during security reviews — shipping clean, indisputable reliability proof that unblocks enterprise renewals without manual quarterly spreadsheet work is a huge win."*
  - *"At the same time, one of my main reasons for investing in reliability tooling is stopping repeat production rollbacks — last quarter 11 of 19 rollbacks repeated documented postmortem causes, and turning past incidents into a pre-deploy learning loop would save hundreds of engineering hours."*
  - *"We only have two SREs for this 10-week window, so we need to pick one sharp v1 focus and defer the other."*

## 2. Existing Engineering Assets
- **Asset A — Mature PagerDuty & Uptime Export Pipeline (90% complete):** Reliable Go daemon exporting 24 months of audited incident timestamps, service-tier downtime math, and 99.95% SLA calculation tables into S3 and clean HTML templates. Peer B2B fintechs credit live status/SLA portals with cutting enterprise security-review friction by 40%.
- **Asset B — Postmortem Markdown Archive & GitHub CI Hooks (40% complete):** 142 structured engineering postmortems in Git (root-cause diffs, affected file paths, SQL/config triggers) plus GitHub Actions webhook access on the 6 core backend repos; no automated rule extractor or pre-merge PR check exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q2 sprint within the 2-SRE and $12,000 constraints.
