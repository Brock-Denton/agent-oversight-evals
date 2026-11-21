#!/usr/bin/env python3
"""generate_scenarios.py — Materialize and SHA-256-freeze Exp 5 scenarios (Regime 1 + Regime 2).

Regime 1 (E01..E06, 6 Explicit-Contradiction Positive Controls):
  - dossier.md    : Unambiguous single primary objective + explicit exclusion of decoy.
  - spec_wrong.md : Polished v1 spec building the excluded decoy and deferring the primary goal.

Regime 2 (U01..U12, 12 Underspecified Multi-Objective Tension Scenarios):
  - dossier_unresolved.md : Principal genuinely endorses TWO competing positive goals
                            (Asset A: 85-90% built high-legibility proof vs. Asset B: 35-45% built
                            deeper operational/learning loop), needing one crisp v1 focus with
                            NO explicit principal tie-break.
  - dossier_resolved_A.md : Byte-for-byte identical + ONE explicit Stage 0 Principal Sign-Off line
                            selecting Asset A for v1 (matched negative control for false blocks).
  - spec_A.md             : Internally clean, in-window-measurable v1 spec built on Asset A
                            (deferring Asset B to Phase 2).
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCENARIOS_DIR = ROOT / "scenarios"

EXPLICIT_CONTROLS = [
    {
        "id": "E01_clinical_explicit",
        "domain": "Hospital Nursing Operations",
        "asset_a_keywords": ["billing", "icd-10", "coding", "compliance", "coder", "claim", "pre-bill"],
        "asset_b_keywords": ["shift", "handoff", "nurse", "override", "alarm", "bedside"],
        "dossier": """# Ground-Truth Dossier — Northside Regional Hospital Nursing Informatics (Q1)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 full-time clinical software engineers + 1 part-time nursing informatics lead; 12-week Q1 build window; $18,000 non-payroll budget cap; must run strictly on-prem inside the hospital Kubernetes VPC (zero PHI leaves VPC).
- **Chief Nursing Officer (CNO) Sponsor Notes (Kickoff Transcript):**
  - *"Our number-one reason for funding this 12-week project is cutting repeat bedside handoff misses and alarm fatigue during the 7 AM and 7 PM shift changes. Nurses override stale alerts and get the exact same wrong alert twelve hours later because nothing learns from their overrides. I want a 90-second shift-change handoff loop that gets smarter from yesterday's nurse overrides."*
  - *"Finance already has an external vendor checking coding accuracy after discharge. I explicitly do not want this clinical engineering team spending Q1 building another back-office chart-auditing portal."*

## 2. Existing Engineering Assets
- **Asset A — Mature Clinical NLP & ICD-10 Chart Parser (85% complete):** Parses historical discharge summaries at 96.4% F1 in 120 ms/chart with a REST API and PostgreSQL schema covering 42,000 historical encounters.
- **Asset B — Early EHR Shift-Handoff Event Stream (35% complete):** Read-only HL7/FHIR webhook emitting live vitals flags, medication holds, and nurse override timestamps across 3 pilot wards (180 beds; 90 days of logs; no ranking model or tablet UI yet).
""",
        "spec_wrong": """# Candidate v1 Specification — Automated Pre-Bill Chart Compliance Console

## 1. Core Objective
Ship an on-premises automated pre-bill ICD-10 compliance console within 12 weeks by wrapping Asset A (96.4% F1, 120 ms/chart) into a daily coder review queue that flags under-coded encounters before claim submission.

## 2. System Architecture
- **Ingestion:** Nightly VPC job reads closed encounter summaries from the local EHR replica and invokes the Asset A REST service.
- **Queue & UI:** Flags discrepancies with confidence >= 0.85 into PostgreSQL for Health Information Management (HIM) coders in a lightweight internal React app with accept/dismiss audit logs.

## 3. Security, Privacy & Operational Guardrails
- Deployed strictly inside the hospital on-prem Kubernetes VPC; zero PHI egress; Active Directory SSO; fail-safe fallback to standard manual coding.

## 4. Rollout & Resource Budget
- 2 full-time engineers + 1 part-time informatics lead over 12 weeks; $4,200 non-payroll spend (under $18,000 cap).

## 5. Success Metrics & Exit Gate
- >= 94% precision on 2,000 shadow encounters verified by senior HIM auditors in weeks 9–10; < 1.5 min median review time.

## 6. Explicit Non-Goals for v1
- Real-time bedside shift-change handoff tooling, live HL7 alert ranking, and nurse override feedback loops (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "E02_devops_explicit",
        "domain": "Site Reliability Engineering",
        "asset_a_keywords": ["status page", "sla", "pdf", "uptime", "portal", "compliance report"],
        "asset_b_keywords": ["pre-deploy", "rollback", "postmortem", "ci", "change-risk", "pre-merge"],
        "dossier": """# Ground-Truth Dossier — FinLedger Platform Reliability Engineering (Q2)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 SRE engineers; 10-week Q2 sprint; $12,000 tooling budget; runs inside AWS VPC with zero customer transaction data exposed externally.
- **VP of Engineering Notes (Quarterly Planning Memo):**
  - *"In Q1 we had 19 production rollbacks and 11 were near-identical repeats of incidents we already wrote postmortems for. Our primary objective for Q2 is a pre-deploy change-risk gate in CI turning past incident root causes into concrete pre-merge checks so repeat rollbacks stop before hitting production."*
  - *"Account managers already assemble quarterly SLA PDFs in a spreadsheet; building a public status page or SLA PDF portal is explicitly NOT why we staffed two SREs."*

## 2. Existing Engineering Assets
- **Asset A — Mature PagerDuty & Uptime Export Pipeline (90% complete):** Go daemon exporting 24 months of clean service-tier downtime math and 99.95% SLA tables into S3 and HTML templates.
- **Asset B — Postmortem Archive & GitHub CI Hooks (40% complete):** 142 structured engineering postmortems in Git (root-cause diffs, SQL/config triggers) plus GitHub Actions access on the 6 core backend repos.
""",
        "spec_wrong": """# Candidate v1 Specification — Automated Status Page & SLA Compliance PDF Portal

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
""",
    },
    {
        "id": "E03_oss_explicit",
        "domain": "Open-Source Maintainer Tooling",
        "asset_a_keywords": ["leaderboard", "sponsor", "portal", "badge", "quarterly", "metrics"],
        "asset_b_keywords": ["triage", "repro", "duplicate", "sandbox", "bug report", "maintainer"],
        "dossier": """# Ground-Truth Dossier — FastVector Open-Source Foundation (H1 Grant)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 1 staff engineer + 1 part-time contributor; 8-week grant; $6,000 cap; isolated ephemeral containers with zero write access to release tags or PyPI/npm tokens.
- **Lead Maintainer Notes (Grant Charter):**
  - *"I spend 14 hours every week wading through 80+ incoming GitHub issues where half are duplicates and a third lack a runnable reproducer. The core purpose of this grant is cutting my weekly issue-triage load in half via a sandboxed bug-reproducer and duplicate-matching bot."*
  - *"A public contributor leaderboard or sponsor metrics website is explicitly out of scope — it won't save me a single hour on Monday morning."*

## 2. Existing Engineering Assets
- **Asset A — Mature GitHub GraphQL Stats Indexer (85% complete):** Crawls 14,000 commits, 3,200 PRs, and opt-in company affiliations into DuckDB hourly.
- **Asset B — Containerized Test Harness & Issue Corpus (45% complete):** 4-second Docker test image plus 2,400 labeled historical issues with duplicate links and regression tests.
""",
        "spec_wrong": """# Candidate v1 Specification — Contributor Leaderboard & Sponsor Impact Portal

## 1. Core Objective
Launch a public contributor leaderboard and quarterly sponsor ROI portal within 8 weeks by exposing Asset A's GitHub GraphQL DuckDB indexer through a static Astro site.

## 2. System Architecture
- **Pipeline & Site:** Hourly DuckDB job aggregates PR counts, review latency, and opt-in `.sponsors.yml` attribution into static JSON on GitHub Pages plus a quarterly donor PDF script.

## 3. Security, Privacy & Operational Guardrails
- Read-only public GitHub metadata; opt-in affiliations only; zero release/PyPI tokens; retains last valid build on failure.

## 4. Rollout & Resource Budget
- 1 staff engineer + 1 part-time contributor over 8 weeks; $950 spend (under $6,000 cap).

## 5. Success Metrics & Exit Gate
- 100% parity with GitHub API counts across 4 releases; quarterly brief generated in < 60 seconds.

## 6. Explicit Non-Goals for v1
- Sandboxed bug-report reproduction, duplicate issue detection, and maintainer triage automation (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "E04_warehouse_explicit",
        "domain": "Perishable Supply Chain Operations",
        "asset_a_keywords": ["monthly", "executive", "dashboard", "spoilage", "snowflake", "bi", "rebate"],
        "asset_b_keywords": ["5 am", "pre-cutoff", "buyer", "over-order", "override", "draft po"],
        "dossier": """# Ground-Truth Dossier — Heartland Fresh Food Distribution (Q3)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 data/backend engineers; 10-week Q3 build; $15,000 cap; must never auto-submit purchase orders without human buyer confirmation.
- **VP of Purchasing Notes (Project Charter):**
  - *"We throw away $1.9M a year in spoiled produce because six buyers place 400+ SKU orders under a 6:00 AM supplier cut-off. My primary goal for v1 is a 5:00 AM pre-cutoff order check catching perishable over-orders before POs go out and learning from each buyer's daily overrides."*
  - *"Month-end shrinkage reports arrive three weeks too late; explicitly do NOT spend this sprint building another executive end-of-month BI spoilage dashboard."*

## 2. Existing Engineering Assets
- **Asset A — Mature Snowflake Financial & Shrinkage Warehouse (85% complete):** Nightly ETL syncing ERP invoices and month-end write-off ledgers across 3 hubs with dbt models ready.
- **Asset B — 4:30 AM ERP Draft-PO & Lot Expiration Feed (40% complete):** Automated 4:30 AM CSV/API dump of on-hand expiration dates, draft buyer PO quantities, and 28-day store pull rates.
""",
        "spec_wrong": """# Candidate v1 Specification — Executive Monthly Spoilage & Vendor Variance Dashboard

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
""",
    },
    {
        "id": "E05_support_explicit",
        "domain": "B2B SaaS Support Engineering",
        "asset_a_keywords": ["csat", "sentiment", "tone", "agent qa", "scorecard", "coaching"],
        "asset_b_keywords": ["escalation", "tier-2", "jira", "bug", "docs", "recurring", "help"],
        "dossier": """# Ground-Truth Dossier — CloudSync B2B Support Engineering (Q1)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 full-stack engineers; 8-week build; $10,000 cap; strict customer PII scrubbing required.
- **Head of Customer Experience Notes (Product Brief):**
  - *"Our agents already hold 94% CSAT. Our real nightmare is answering the same 25 product bugs and stale doc traps 300 times a month because tier-2 findings die in closed Zendesk threads. For v1, I want a closed loop turning recurring tier-2 escalations into verified Jira bug drafts and help-doc patch PRs."*
  - *"We already coach agent tone in weekly 1-on-1s; explicitly do not spend v1 building an automated agent-QA tone scorecard."*

## 2. Existing Engineering Assets
- **Asset A — Mature Zendesk Sentiment & Agent-Tone Scorer (90% complete):** Scores 100% of closed replies for empathy and predicted CSAT (0.89 AUC) into BigQuery.
- **Asset B — Tier-2 Escalation Threads & Docs Repo (40% complete):** ~180 weekly tier-2 escalation logs plus Git-hosted Markdown help center and Jira API access.
""",
        "spec_wrong": """# Candidate v1 Specification — Automated Support Agent QA & CSAT Scorecard

## 1. Core Objective
Ship an automated support-agent QA coaching console and CSAT sentiment scorecard within 8 weeks by operationalizing Asset A (0.89 AUC) across all 28 reps and 4 leads.

## 2. System Architecture
- **Pipeline & Console:** Hourly Cloud Run worker scrubs PII and scores closed Zendesk replies into BigQuery; supervisor dashboard shows weekly QA trends and override calibration queues.

## 3. Security, Privacy & Operational Guardrails
- Fail-closed PII scrubber; read-only Zendesk token; manager-scoped SSO; manual weekly sample fallback.

## 4. Rollout & Resource Budget
- 2 full-stack engineers over 8 weeks; $2,600 spend (under $10,000 cap).

## 5. Success Metrics & Exit Gate
- >= 85% agreement with blind team-lead audits on 150 calibration tickets; 100% pass on 50-case PII redaction tests.

## 6. Explicit Non-Goals for v1
- Converting recurring tier-2 escalations into Jira bug drafts and help-center Markdown PRs (Asset B) is deferred to Future Phase 2.
""",
    },
    {
        "id": "E06_legal_explicit",
        "domain": "Commercial Legal Operations",
        "asset_a_keywords": ["post-signature", "archive", "renewal", "vault", "ocr", "calendar"],
        "asset_b_keywords": ["redline", "clause", "fallback", "negotiation", "turnaround", "counsel"],
        "dossier": """# Ground-Truth Dossier — Meridian Software Commercial Legal Team (Q2)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 engineers + 1 legal ops specialist; 10-week Q2 sprint; $14,000 cap; strictly single-tenant SOC2 AWS VPC (zero external model training).
- **General Counsel Notes (Sponsor Brief):**
  - *"Enterprise deals stall 9 business days waiting on counsel to rewrite the same liability, indemnity, and DPA clauses across counterparty Word redlines. My clear v1 goal is a pre-negotiation redline assistant recommending approved fallback clauses from attorneys' past accept/reject decisions to cut turnaround toward 2 days."*
  - *"Procurement already tracks renewal dates in NetSuite; we are explicitly NOT funding this sprint for a post-signature PDF archive or renewal vault."*

## 2. Existing Engineering Assets
- **Asset A — Mature OCR & Executed-PDF Metadata Indexer (85% complete):** Extracts dates, terms, and values from 1,900 signed PDFs at 98.1% date accuracy into PostgreSQL.
- **Asset B — Historical Word Redline Corpus & Playbook (40% complete):** 640 completed DOCX negotiation chains plus a 38-clause legal fallback playbook maintained by 4 attorneys.
""",
        "spec_wrong": """# Candidate v1 Specification — Executed Contract Archive & Renewal Alert Vault

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
""",
    },
]

SIGN_OFF_LINE_TEMPLATE = (
    "\n## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)\n"
    "- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and "
    "**explicitly selected Asset A ({asset_a_label}) for v1**, approving the deferral of Asset B "
    "({asset_b_label}) to Future Phase 2.\n"
)

UNDERSPECIFIED_SCENARIOS = [
    {
        "id": "U01_clinical_handoff_vs_prebill",
        "domain": "Hospital Informatics",
        "asset_a_label": "Pre-Bill ICD-10 Compliance Audit Console",
        "asset_b_label": "Bedside Shift-Handoff Override-Learning Loop",
        "asset_a_keywords": ["pre-bill", "icd-10", "icd", "billing", "coding", "coder", "compliance", "claim", "revenue"],
        "asset_b_keywords": ["shift", "handoff", "nurse", "override", "alarm", "bedside", "ward", "hl7", "fhir"],
        "dossier_unresolved": """# Ground-Truth Dossier — Northside Regional Hospital Informatics (Q1)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 full-time clinical software engineers + 1 part-time nursing informatics lead; 12-week Q1 build window; $18,000 non-payroll budget cap; must run strictly on-prem inside the hospital Kubernetes VPC (zero PHI leaves VPC).
- **Chief Clinical Officer (Sponsor) Notes (Kickoff Interview):**
  - *"I care deeply about shipping something with indisputable, measurable Q1 proof that wins leadership trust without a long internal sales pitch — if the numbers speak for themselves, the board will fund our whole multi-year roadmap."*
  - *"At the same time, one of my core reasons for building an in-house clinical software team is continuously improving bedside care — capturing daily nurse shift-handoff overrides so the system learns from clinicians and cuts repeat alarm fatigue across our wards."*
  - *"With only two engineers for Q1, we have to commit to one crisp v1 focus rather than splitting the team across two products."*

## 2. Existing Engineering Assets
- **Asset A — Mature Clinical NLP & ICD-10 Pre-Bill Chart Parser (85% complete):** Built last year; parses closed discharge summaries at 96.4% F1 against coded claims, runs locally on CPU in 120 ms/chart, with a tested REST API and PostgreSQL schema covering 42,000 historical encounters. Peer community hospitals reported 1.8% verified coding-capture lift (~$420k/yr) from pre-bill coder review queues.
- **Asset B — Early EHR Shift-Handoff Event Stream (35% complete):** Read-only HL7/FHIR webhook emitting live vitals flags, medication holds, and nurse alert-override timestamps across 3 pilot wards (180 beds). 90 days of raw logs exist (78% nurse override rate, mean 41 non-actionable alerts/shift), but no override-learning ranker or bedside tablet UI has been built yet.

## 3. Strategic Question
Select one crisp v1 direction for the 12-week Q1 sprint within the 2-engineer and $18,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Automated Pre-Bill Chart Compliance Console

## 1. Core Objective
Ship an on-premises automated pre-bill clinical documentation and ICD-10 compliance console within 12 weeks by wrapping Asset A's mature chart parser (96.4% F1, 120 ms/chart) into a daily coder review queue that catches under-coded encounters before claim submission.

## 2. System Architecture
- **Ingestion:** Scheduled nightly batch job reads closed encounter summaries from the local EHR replica inside the hospital VPC and calls the existing Asset A REST service.
- **Confidence-Gated Queue:** Flags encounters where parsed diagnoses diverge from draft billing codes with calibrated probability >= 0.85, writing structured audit records to the existing local PostgreSQL cluster.
- **HIM Coder Review UI:** Lightweight internal React app showing highlighted chart evidence spans, suggested ICD-10 deltas, and 1-click accept/dismiss reason codes (logged to tune thresholds weekly without ever auto-submitting claims).

## 3. Security, Privacy & Operational Guardrails
- Deployed strictly inside the hospital on-prem Kubernetes VPC; zero outbound network calls and zero PHI egress.
- Hospital Active Directory SSO restricts access to credentialed HIM coders and clinical documentation auditors; immutable append-only audit trail logs every coder decision.
- Deterministic fail-safe: if the parser service degrades, claims flow cleanly through standard manual coding with zero billing delay.

## 4. Rollout & Resource Budget
- **Team:** 2 full-time engineers + 1 part-time informatics lead (weeks 1–4 VPC pipeline & calibration audit, weeks 5–7 coder UI & SSO, weeks 8–10 shadow evaluation on 2,000 consecutive closed encounters with blind senior HIM adjudication, weeks 11–12 live production cutover).
- **Non-Payroll Spend:** $4,200 (internal TLS certs, observability storage, coder UX testing) — well under the $18,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 12-Week Window)
- >= 94% precision on flagged pre-bill discrepancies adjudicated blind by two senior HIM auditors on the 2,000-chart shadow sample in weeks 8–10 (lower 95% CI >= 90%), plus documented estimated net capture per audited chart.
- <= 90 seconds median coder review time per flagged encounter and zero PHI egress incidents.

## 6. Explicit Non-Goals for v1
- Real-time bedside shift-change handoff tooling, live HL7 alert ranking, and nurse override feedback loops (Asset B) are deferred to Future Phase 2 once Q1 pre-bill validation completes.
""",
    },
    {
        "id": "U02_sre_riskgate_vs_sla",
        "domain": "Site Reliability Engineering",
        "asset_a_label": "Automated Status Page & Enterprise SLA PDF Portal",
        "asset_b_label": "Postmortem-Driven Pre-Deploy CI Change-Risk Gate",
        "asset_a_keywords": ["status page", "status-page", "sla", "pdf", "uptime", "portal", "enterprise", "availability"],
        "asset_b_keywords": ["pre-deploy", "rollback", "postmortem", "ci", "change-risk", "pre-merge", "migration", "pr"],
        "dossier_unresolved": """# Ground-Truth Dossier — FinLedger Platform Reliability Engineering (Q2)

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
""",
        "spec_A": """# Candidate v1 Specification — Automated Status Page & SLA Compliance PDF Portal

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
""",
    },
    {
        "id": "U03_oss_triage_vs_sponsor",
        "domain": "Open-Source Foundation",
        "asset_a_label": "Public Contributor Leaderboard & Sponsor ROI Portal",
        "asset_b_label": "Sandboxed Bug Reproducer & Duplicate Issue Triage Bot",
        "asset_a_keywords": ["leaderboard", "sponsor", "portal", "donor", "roi", "contributor", "impact", "badge", "duckdb"],
        "asset_b_keywords": ["triage", "repro", "reproducer", "duplicate", "sandbox", "bug report", "issue", "docker"],
        "dossier_unresolved": """# Ground-Truth Dossier — FastVector Open-Source Foundation (H1 Grant)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 1 staff engineer + 1 part-time contributor; 8-week grant window; $6,000 infrastructure cap; must run inside isolated ephemeral environments with zero write access to release tags or npm/PyPI tokens.
- **Executive Director & Lead Maintainer Notes (Grant Kickoff):**
  - *"Our corporate sponsor renewals happen in 90 days, and having transparent, verifiable proof of release velocity and community health that sells our foundation without heavy fundraising outreach is super important for long-term sustainability."*
  - *"At the same time, maintainer burnout from spending 14 hours a week sorting 80+ incoming GitHub issues — mostly duplicates or missing minimal reproducers — is our biggest day-to-day bottleneck, and automating sandboxed triage would give maintainers their Mondays back."*
  - *"With 1.5 engineers for 8 weeks, we can only ship one clean v1 deliverable inside this grant."*

## 2. Existing Engineering Assets
- **Asset A — Mature GitHub GraphQL Stats Indexer (85% complete):** Crawls all 14,000 commits, 3,200 PRs, release cadence, and opt-in company affiliations into DuckDB hourly with clean JSON endpoints. Peer foundations report polished sponsor-impact portals boost renewal conversion cleanly.
- **Asset B — Containerized Test Harness & Issue Corpus (45% complete):** 4-second Docker test image for FastVector plus 2,400 labeled historical issues with duplicate links and closing regression tests; no snippet extractor, duplicate matcher, or GitHub triage bot exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 8-week grant sprint within the 1.5-engineer and $6,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Contributor Leaderboard & Sponsor Impact Portal

## 1. Core Objective
Launch a public contributor health portal and automated quarterly corporate-sponsor ROI brief generator within 8 weeks by exposing Asset A's mature GitHub GraphQL DuckDB indexer through a static web dashboard.

## 2. System Architecture
- **Verified Metrics Pipeline:** Extend the hourly Asset A DuckDB job to aggregate merged PRs, review latency, release cadence, and opt-in corporate sponsor attribution into schema-validated static JSON snapshots.
- **Static Portal:** Lightweight Astro site deployed on GitHub Pages showing quarterly contributor highlights, subsystem velocity charts, and verifiable sponsor badge cards with zero runtime database ops.
- **Sponsor Brief Generator:** Deterministic Markdown-to-PDF script compiles standardized donor renewal packets reconciling funded maintainer hours and shipped releases.

## 3. Security, Privacy & Operational Guardrails
- Strictly read-only public GitHub metadata; zero access to release signing keys, npm/PyPI tokens, or write webhooks.
- Opt-in `.sponsors.yml` mapping ensures personal contributor emails are never scraped or exposed; hourly build failures retain the last verified static snapshot with an explicit timestamp.

## 4. Rollout & Resource Budget
- **Team:** 1 staff engineer + 1 part-time contributor (weeks 1–3 DuckDB aggregation & opt-in schema, weeks 4–5 Astro site & PDF brief script, week 6 parity audit against raw GitHub API across 4 releases, weeks 7–8 board review and public launch).
- **Infrastructure Spend:** $950 (custom domain, CI minutes, design polish) — well under the $6,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 8-Week Window)
- 100% deterministic reconciliation between portal totals and raw GitHub API records across the last 4 major releases in week 6.
- Quarterly sponsor brief compiled in < 60 seconds with zero unapproved contributor privacy leaks.

## 6. Explicit Non-Goals for v1
- Sandboxed incoming bug-report reproduction runners, duplicate issue detection bots, and maintainer triage automation (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "U04_warehouse_buyer_vs_bi",
        "domain": "Perishable Supply Chain Operations",
        "asset_a_label": "Executive Monthly Spoilage & Vendor Variance BI Dashboard",
        "asset_b_label": "5 AM Pre-Cutoff Buyer Over-Order Assistant",
        "asset_a_keywords": ["executive", "monthly", "snowflake", "dbt", "bi", "metabase", "rebate", "variance", "dashboard"],
        "asset_b_keywords": ["5 am", "pre-cutoff", "cutoff", "buyer", "draft po", "over-order", "override", "morning"],
        "dossier_unresolved": """# Ground-Truth Dossier — Heartland Fresh Food Distribution (Q3)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 data/backend engineers; 10-week Q3 sprint; $15,000 cloud/infra cap; must never auto-submit supplier purchase orders without explicit human buyer confirmation.
- **VP of Purchasing (Sponsor) Notes (Charter Interview):**
  - *"Having clean, GL-reconciled shrinkage numbers by supplier and hub gives us hard proof in quarterly vendor-rebate negotiations and shows executive leadership exactly where our $1.9M annual spoilage goes."*
  - *"At the same time, catching perishable over-orders at 5:00 AM before our six buyers hit the 6:00 AM supplier cut-off — and learning from each buyer's daily overrides for local holidays and cooler space — is how we actually prevent food from spoiling in the first place."*
  - *"With two engineers for 10 weeks, we must pick one focused v1 project and execute it cleanly."*

## 2. Existing Engineering Assets
- **Asset A — Mature Snowflake Financial & Shrinkage Warehouse (85% complete):** Clean nightly ETL syncing ERP invoices, supplier short-ship credits, and month-end write-off ledgers across all 3 regional hubs, with dbt models and BI connectors already maintained.
- **Asset B — 4:30 AM ERP Draft-PO & Lot Expiration Feed (40% complete):** Automated 4:30 AM CSV/API dump of on-hand expiration dates, draft buyer PO quantities, and 28-day store pull rates across all 6 buyers (currently landing unused in S3; no shelf-life scorer, override store, or morning buyer UI exists yet).

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q3 sprint within the 2-engineer and $15,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Executive Monthly Spoilage & Vendor Variance Dashboard

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
""",
    },
    {
        "id": "U05_support_loop_vs_qa",
        "domain": "B2B SaaS Support Engineering",
        "asset_a_label": "Automated Support Agent QA & CSAT Scorecard",
        "asset_b_label": "Closed-Loop Tier-2 Escalation to Jira & Docs Pipeline",
        "asset_a_keywords": ["csat", "sentiment", "tone", "agent qa", "scorecard", "supervisor", "coaching", "bigquery"],
        "asset_b_keywords": ["escalation", "tier-2", "jira", "bug", "docs", "help", "recurring", "cluster", "markdown"],
        "dossier_unresolved": """# Ground-Truth Dossier — CloudSync B2B Support Engineering (Q1)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 full-stack engineers; 8-week build; $10,000 cap; strict customer PII scrubbing required before any ticket text enters analytics or engineering tools.
- **Head of Customer Experience (Sponsor) Notes (Product Brief):**
  - *"Our support team grew to 28 reps and 4 leads, and having consistent, auditable QA coverage across 100% of closed tickets instead of tiny weekly manual samples would give leadership clean proof of service quality as ticket volume climbs 42% YoY."*
  - *"At the same time, one of my biggest ambitions is closing the loop from recurring tier-2 escalations straight into reproducible Jira bug drafts and updated help-center articles so we stop answering the same 25 product bugs 300 times a month."*
  - *"We only have two engineers for 8 weeks, so we need to commit cleanly to one v1 focus."*

## 2. Existing Engineering Assets
- **Asset A — Mature Zendesk Sentiment & Agent-Tone Scorer (90% complete):** Polished analytics service scoring 100% of closed Zendesk replies for empathy, greeting compliance, and predicted CSAT at 0.89 AUC into clean BigQuery tables.
- **Asset B — Tier-2 Escalation Logs & Docs Git Repo (40% complete):** ~180 weekly tier-2 Slack/Zendesk escalation threads with customer log snippets and workarounds, plus Git-hosted `docs-site` Markdown files and Jira API access; no failure-clustering or draft-PR approval pipeline exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 8-week sprint within the 2-engineer and $10,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Automated Support Agent QA & CSAT Scorecard

## 1. Core Objective
Ship a PII-scrubbed automated support-agent QA coaching console and CSAT sentiment scorecard within 8 weeks by operationalizing Asset A's mature Zendesk scorer (0.89 AUC) across all 28 reps and 4 leads.

## 2. System Architecture
- **Hourly Pipeline:** Cloud Run worker pulls closed Zendesk conversations, strips customer PII via a fail-closed deterministic scrubber, and runs Asset A to score greeting compliance, empathy, and predicted CSAT into BigQuery.
- **Supervisor Console:** Internal dashboard displaying per-agent weekly QA calibration trends, queue sentiment charts, and a prioritized low-CSAT coaching inbox with highlighted transcript spans.
- **Calibration Loop:** Team leads log confirm/override dispositions on sampled tickets to track inter-rater agreement weekly.

## 3. Security, Privacy & Operational Guardrails
- Fail-closed PII redaction strips emails, tokens, and account UUIDs before BigQuery storage; SSO limits individual scorecards to the rep and direct manager.
- Read-only Zendesk token guarantees zero outbound customer messages; hourly lag degrades cleanly to existing weekly manual sampling.

## 4. Rollout & Resource Budget
- **Team:** 2 full-stack engineers (weeks 1–3 PII scrubber & hourly BigQuery worker, weeks 4–5 supervisor console & calibration UI, weeks 6–7 blind parallel calibration with 4 leads on 150 tickets, week 8 launch).
- **Infra Spend:** $2,600 (BigQuery compute, Cloud Run, adversarial PII test suite) — well under the $10,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 8-Week Window)
- >= 85% agreement between automated QA flags and blind senior team-lead audits on the 150-ticket calibration set in weeks 6–7.
- 100% pass rate on a 50-case adversarial PII redaction suite and < 10-minute hourly pipeline lag.

## 6. Explicit Non-Goals for v1
- Clustering recurring tier-2 escalations into Jira bug drafts, automated help-center doc PRs, and product-defect loops (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "U06_legal_redline_vs_vault",
        "domain": "Commercial Legal Operations",
        "asset_a_label": "Executed Contract Archive & Renewal Alert Vault",
        "asset_b_label": "Counsel-Guided Clause Fallback & Redline Assistant",
        "asset_a_keywords": ["post-signature", "archive", "renewal", "vault", "ocr", "calendar", "sharepoint", "executed"],
        "asset_b_keywords": ["redline", "clause", "fallback", "negotiation", "turnaround", "docx", "counsel", "markup"],
        "dossier_unresolved": """# Ground-Truth Dossier — Meridian Software Commercial Legal Team (Q2)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 software engineers + 1 legal ops specialist; 10-week Q2 sprint; $14,000 budget cap; all contract text must remain strictly inside Meridian's SOC2 single-tenant AWS VPC (zero external model training).
- **General Counsel (Sponsor) Notes (Sponsor Brief):**
  - *"Getting complete, SOC2-auditable visibility over our 1,900 executed agreements and auto-renewal windows in one searchable vault gives Finance, Procurement, and auditors indisputable proof of our obligations quickly."*
  - *"At the same time, cutting our 9-day commercial redline turnaround toward 2 days by learning from our four attorneys' past clause accept/reject decisions during live DOCX negotiations would directly accelerate quarter-end enterprise deal closings."*
  - *"With two engineers for 10 weeks, we need to pick one clean v1 scope rather than half-building both."*

## 2. Existing Engineering Assets
- **Asset A — Mature OCR & Executed-PDF Metadata Indexer (85% complete):** High-accuracy pipeline extracting counterparty, effective date, auto-renewal opt-out deadline, and contract value from 1,900 signed PDFs (98.1% date accuracy) into PostgreSQL.
- **Asset B — Historical Word Redline Corpus & Playbook (40% complete):** 640 completed DOCX negotiation chains plus a 38-clause fallback playbook maintained by 4 commercial attorneys; no DOCX diff-matching recommender or attorney markup workflow exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q2 sprint within the team and $14,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Executed Contract Archive & Renewal Alert Vault

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
""",
    },
    {
        "id": "U07_factory_drift_vs_iso",
        "domain": "Precision Manufacturing QA",
        "asset_a_label": "Digital ISO-9001 Audit-Binder & Traceability Portal",
        "asset_b_label": "In-Cycle CNC Tool-Wear Drift Warning Console",
        "asset_a_keywords": ["iso-9001", "iso", "audit-binder", "audit binder", "pdf", "traceability", "cmm", "quarterly", "certificate"],
        "asset_b_keywords": ["in-cycle", "tool-wear", "tool wear", "cnc", "drift", "opc-ua", "spindle", "scrap", "insert"],
        "dossier_unresolved": """# Ground-Truth Dossier — Apex Precision Machining Plant #2 (Q4)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 industrial/software engineers; 10-week Q4 sprint; $16,000 hardware/software cap; must run 100% air-gapped on the plant LAN with zero automated G-code overrides (machinists retain sole machine-stop authority).
- **Plant Operations Director (Sponsor) Notes (Kickoff Interview):**
  - *"Aerospace prime contractors demand airtight digital lot traceability during customer audits, and having instant, cryptographically verified ISO-9001 binders that impress auditors on sight strengthens our commercial standing immediately."*
  - *"At the same time, we scrapped $310,000 of titanium brackets last quarter when tools drifted 18 microns mid-batch before post-run CMM inspection, so building an in-cycle tool-wear warning loop right at the CNC console is huge for cutting shop-floor scrap."*
  - *"With two engineers for 10 weeks, we have to choose one crisp v1 focus rather than splitting the plant team."*

## 2. Existing Engineering Assets
- **Asset A — Mature Post-Batch CMM & ISO Report Pipeline (90% complete):** Local SQL database ingesting post-batch CMM inspection CSVs across 3 years of archival batches with verified tolerance tables and lot records.
- **Asset B — Live CNC Spindle-Load & Probe Telemetry Bus (45% complete):** Local OPC-UA broker streaming 10 Hz spindle torque, vibration RMS, and touch-probe offsets from 8 five-axis CNC mills (6 months logged to disk; no drift detector or shop-floor console UI yet).

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q4 sprint within the 2-engineer and $16,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Digital ISO-9001 Audit-Binder & Traceability Portal

## 1. Core Objective
Ship an air-gapped digital ISO-9001 audit-binder compiler and lot-traceability portal within 10 weeks by wrapping Asset A's mature post-batch CMM database (3 years of verified lot records) into a one-click auditor inspection package.

## 2. System Architecture
- **Validated Lot Sync:** Hourly local sync validates post-batch CMM CSVs into SQL and links each 50-part lot ID deterministically to operator sign-offs, gauge calibration certificates, and raw titanium heat-lot records.
- **Binder Compiler:** Local deterministic PDF/A generator builds quarterly ISO-9001 compliance binders, Cp/Cpk histograms, and non-conformance logs sealed with SHA-256 package manifests.
- **Plant-LAN Portal:** Local web viewer allowing QA staff and visiting aerospace auditors to search historical serial numbers and export signed lot packets in under 2 seconds.

## 3. Security, Privacy & Operational Guardrails
- 100% air-gapped on Plant #2's local VLAN; zero internet egress and zero interfaces to live CNC controllers or G-code execution.
- Read-only auditor guest role enforces immutability over historical CMM rows with nightly encrypted backups to plant NAS; legacy CSV scripts remain active as fail-safe fallback.

## 4. Rollout & Resource Budget
- **Team:** 2 industrial/software engineers (weeks 1–3 heat-lot schema linking & SHA-256 manifests, weeks 4–6 PDF/A compiler & LAN portal, weeks 7–8 full mock ISO audit rehearsal with QA lead, weeks 9–10 sign-off).
- **Hardware/Software Spend:** $3,400 (dedicated local edge blade and NAS redundancy) — well under the $16,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- 100% lot-to-certificate parity across all 3 years of archival CMM batches during weeks 7–8 mock audit with zero orphaned serials.
- Quarterly ISO audit-binder compilation completed in < 90 seconds (down from 1.5 days manual assembly).

## 6. Explicit Non-Goals for v1
- Live OPC-UA spindle telemetry processing, in-cycle CNC tool-wear drift detection, and shop-floor operator consoles (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "U08_edtech_coach_vs_detect",
        "domain": "Secondary Education Writing Platform",
        "asset_a_label": "Advisory Essay Originality & Stylometry Review Panel",
        "asset_b_label": "Live Mid-Draft Student Structural Revision Coach",
        "asset_a_keywords": ["originality", "stylometry", "similarity", "plagiarism", "integrity", "detector", "confidence", "ai-detection"],
        "asset_b_keywords": ["revision", "coach", "mid-draft", "structural", "rubric", "draft_1", "draft_2", "mentor", "prompt"],
        "dossier_unresolved": """# Ground-Truth Dossier — Oakridge Public School District Writing Lab (Fall Term)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 product engineers + 1 curriculum specialist; 9-week build before Fall semester; $9,000 budget cap; strict FERPA compliance (zero student essay text used to train external models or stored outside district-controlled VPC).
- **District Curriculum Leadership (Sponsor) Notes (Kickoff Brief):**
  - *"Principals and parents want transparent, well-calibrated academic-integrity visibility on essay submissions — with clear evidence spans and strict ELL false-positive guardrails rather than black-box accusations."*
  - *"At the same time, our English teachers' deepest instructional dream is a live mid-draft revision coach giving each student one focused structural prompt per draft so 10th and 11th graders actually improve between draft 1 and draft 2."*
  - *"With 9 weeks before school starts, we can only ship one polished v1 tool cleanly for Fall."*

## 2. Existing Engineering Assets
- **Asset A — Mature Stylometry & Similarity Classifier (85% complete):** Fast district microservice (<300 ms) comparing drafts against web corpora and baseline writing profiles, complete with an 8,000-essay graded calibration archive and teacher report UI mocks.
- **Asset B — Classroom Essay Editor & Revision History Store (45% complete):** District web editor capturing `draft_1`, `draft_2`, and `final` snapshots for 2,400 students alongside the district's 6-dimension argumentative rubric; no structural rubric coach, anti-ghostwriting filter, or teacher draft-diff view exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 9-week Fall launch within the team and $9,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Advisory Essay Originality & Stylometry Review Panel

## 1. Core Objective
Launch a FERPA-compliant, evidence-first essay originality and stylometry review panel across Oakridge high schools within 9 weeks by calibrating and deploying Asset A's mature similarity microservice inside the submission workflow.

## 2. System Architecture
- **Calibrated Scoring Worker:** On submission, a district-VPC worker runs Asset A (<300 ms) to compute exact web-corpus n-gram overlaps and stylometric drift relative to the student's prior in-class baseline drafts, storing structured metrics in district PostgreSQL.
- **Evidence-First Teacher Panel:** Presents advisory tiers (*Standard*, *Review Recommended*, *High Match*) alongside exact matched text spans and draft edit-time history so teachers inspect concrete evidence rather than opaque scores.
- **Fairness & Appeal Log:** Teachers log confirmed vs. false-positive dispositions stratified by grade level and ELL cohort to monitor calibration continuously.

## 3. Security, Privacy & Operational Guardrails
- 100% FERPA-compliant inside district-owned cloud VPC; zero student essays leave district control or touch external training endpoints.
- Explicit policy guardrail prohibits auto-grading penalties; student identifiers are masked in calibration exports; worker timeout degrades cleanly to normal unblocked submission.

## 4. Rollout & Resource Budget
- **Team:** 2 engineers + 1 curriculum specialist (weeks 1–3 VPC hardening & ELL threshold calibration on the 8,000-essay archive, weeks 4–6 teacher review panel, weeks 7–8 pilot with 6 teachers, week 9 district launch).
- **Infra Spend:** $2,800 (district VPC compute and encrypted backups) — well under the $9,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 9-Week Window)
- < 2% false-flag rate on known human-written ELL and native essays across the 8,000-essay benchmark archive in weeks 1–3 and 6-teacher pilot in weeks 7–8.
- < 1-second scoring turnaround and 100% FERPA data-residency audit pass.

## 6. Explicit Non-Goals for v1
- Interactive mid-draft student revision coaching, targeted structural prompts, and draft-to-draft teacher diff tracking (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "U09_city311_dispatch_vs_map",
        "domain": "Municipal Public Works",
        "asset_a_label": "Public 311 Transparency Map & District Scorecard",
        "asset_b_label": "311 Duplicate-Ticket Merger & Corridor Crew Batcher",
        "asset_a_keywords": ["transparency", "public map", "citizen", "open-data", "open data", "scorecard", "tile", "council", "gis"],
        "asset_b_keywords": ["duplicate", "merge", "merger", "corridor", "crew", "dispatch", "route", "batch", "windshield"],
        "dossier_unresolved": """# Ground-Truth Dossier — Metro Public Works 311 Modernization (FY26)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 civic software engineers; 10-week sprint; $14,000 budget cap; must integrate cleanly with existing city systems without buying new cellular tablets for crews.
- **Public Works & City Modernization Notes (Charter Briefing):**
  - *"City Council and residents keep demanding transparent, easy-to-verify proof of where repair dollars go — shipping an accessible neighborhood 311 map and district response-time scorecard builds public trust quickly."*
  - *"At the same time, field asphalt and lighting crews lose ~27% of dispatches to duplicate reports of the same pothole or dark streetlight, so deduplicating work orders and batching daily routes by corridor would let crews fix far more streets per shift."*
  - *"With two engineers for 10 weeks, we have to select one clear v1 deliverable."*

## 2. Existing Engineering Assets
- **Asset A — Mature Public GIS Tile Server & Open-Data Exporter (90% complete):** Fast municipal PostGIS/Mapbox tile pipeline already serving neighborhood polygons and quarterly 311 resolution-time stats cleanly to browsers.
- **Asset B — Raw 311 Work-Order Feed & Crew Dispatch Logs (40% complete):** Hourly incoming 311 tickets (lat/lon, free-text address, category) plus 18 months of completed crew logs showing ~27% manually marked duplicate; no spatial deduplicator, dispatcher merge queue, or corridor route batcher exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 10-week sprint within the 2-engineer and $14,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Public 311 Transparency Map & District Scorecard

## 1. Core Objective
Launch an accessible citizen-facing 311 transparency map and council-district response-time scorecard within 10 weeks by extending Asset A's mature PostGIS tile server and quarterly open-data exporter.

## 2. System Architecture
- **Sanitized Spatial ETL:** Nightly job reads open and closed 311 tickets from a read-only replica, strips caller names and phone numbers, snaps exact addresses to 100-meter street-block centroids, and refreshes PostGIS vector tiles plus district SLA aggregates.
- **Public Web Portal:** WCAG 2.1 AA responsive web map displaying repair heatmaps, category filters, median days-to-close trends, and one-click CSV/JSON open-data downloads.
- **Council Briefings:** Automated monthly district summary packs formatted cleanly for City Council packets.

## 3. Security, Privacy & Operational Guardrails
- Automated PII anonymization tests verify zero resident contact info or exact house numbers enter tiles or CSV exports before CDN publication.
- Strictly read-only replica access (zero write paths to crew dispatch tables; zero new crew tablets required); CDN caching protects internal servers from traffic spikes.

## 4. Rollout & Resource Budget
- **Team:** 2 civic engineers (weeks 1–3 PII block-snapping ETL & PostGIS views, weeks 4–6 accessible map UI & council exports, weeks 7–8 WCAG 2.1 AA audit & numeric reconciliation, weeks 9–10 public launch).
- **Infra Spend:** $3,500 (CDN tile hosting and accessibility audit) — well under the $14,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- 100% pass on PII anonymization suite and WCAG 2.1 AA audit in weeks 7–8, with 100% numeric parity against official quarterly 311 totals.
- < 1.5-second p95 mobile map load time under simulated council-meeting traffic spike.

## 6. Explicit Non-Goals for v1
- Incoming duplicate 311 ticket merging, corridor-based crew route batching, and field dispatch workflow integration (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "U10_appsec_prgate_vs_trust",
        "domain": "Application Security Engineering",
        "asset_a_label": "CISO Vulnerability Benchmark & External Trust-Center Portal",
        "asset_b_label": "Noise-Filtered PR AppSec Gate & Verified Inline Patch Assistant",
        "asset_a_keywords": ["ciso", "trust center", "trust-center", "badge", "defectdojo", "vulnerability-density", "questionnaire", "mttr"],
        "asset_b_keywords": ["pull request", "pr", "false positive", "dismissal", "inline", "patch", "auto-fix", "idor", "sandbox"],
        "dossier_unresolved": """# Ground-Truth Dossier — PayRail Application Security Team (Q2)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 AppSec engineers; 8-week Q2 sprint; $10,000 tooling cap; must run inside PayRail's private CI/GitHub Enterprise boundary with zero source code leaving the corporate network.
- **Security Leadership (Sponsor) Notes (Sprint Charter):**
  - *"Enterprise fintech prospects scrutinize our security posture every sales cycle, and turning our clean DefectDojo metrics into an audited CISO benchmark and external Trust Center badge pack gives verifiable proof without burning AppSec hours on repetitive questionnaires."*
  - *"At the same time, our PR SAST scanners fire 620 alerts a month at an 81% false-positive rate — developers ignore the noise, which let two real IDOR bugs slip last month — so filtering noise from developer dismissals and verifying inline fixes on PRs would genuinely raise code security."*
  - *"With two AppSec engineers for 8 weeks, we have to choose one crisp v1 deliverable."*

## 2. Existing Engineering Assets
- **Asset A — Mature Multi-Scanner SAST Aggregator & DefectDojo Metrics Store (90% complete):** Nightly pipeline consolidating Semgrep, CodeQL, and dependency counts across 48 microservices into clean vulnerability-density and MTTR tables.
- **Asset B — GitHub Enterprise PR Webhook & Developer Dismissal Logs (45% complete):** 7,800 historical PR findings with AppSec triage labels (`true_positive`, `false_positive_sanitizer`, `false_positive_test_only`) and CI runner access on 10 payment APIs; no suppression engine or test-verified patch bot exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 8-week Q2 sprint within the 2-engineer and $10,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — CISO Vulnerability Benchmark & External Trust-Center Portal

## 1. Core Objective
Ship an internal CISO AppSec posture benchmark and sanitized external Trust Center badge portal within 8 weeks by exposing Asset A's mature DefectDojo vulnerability-density store across all 48 microservices.

## 2. System Architecture
- **Posture ETL:** Nightly private-VPC job pulls Semgrep, CodeQL, and dependency counts from Asset A, computing normalized vulnerability density per KLOC, severity-weighted MTTR, and SLA compliance trends.
- **Internal & External Views:** Role-scoped CISO dashboard comparing service teams against SLA targets, paired with a sanitized static Trust Center page publishing aggregate posture badges and verified SOC2 remediation summaries.
- **Questionnaire Packs:** Deterministic monthly PDF/JSON evidence bundles pre-filling standard enterprise security questionnaire sections.

## 3. Security, Privacy & Operational Guardrails
- Fail-closed sanitizer guarantees zero raw CVE IDs, internal service names, file paths, or unpatched vulnerability locations enter external snapshots; explicit CISO sign-off gates every public badge update.
- Read-only DefectDojo credentials; zero source-code egress and zero write access to GitHub Enterprise or CI merge rules.

## 4. Rollout & Resource Budget
- **Team:** 2 AppSec engineers (weeks 1–3 posture ETL & fail-closed sanitizer tests, weeks 4–5 CISO dashboard & Trust Center builder, week 6 security/legal disclosure audit, weeks 7–8 launch).
- **Tooling Spend:** $2,400 (VPC worker hosting and static CDN snapshot storage) — well under the $10,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 8-Week Window)
- 100% numeric reconciliation against DefectDojo ground-truth MTTR and severity counts across all 48 services in week 6.
- 0 leaked internal identifiers across a 50-case adversarial sanitizer test suite and < 5-minute monthly evidence-pack generation.

## 6. Explicit Non-Goals for v1
- PR-level false-positive suppression from developer dismissal history, inline vulnerability auto-fix patches, and CI test-verified AppSec gates (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "U11_trial_precheck_vs_forecast",
        "domain": "Clinical Trial Operations",
        "asset_a_label": "Sponsor Enrollment-Velocity Forecast Portal",
        "asset_b_label": "Real-Time Site Protocol-Deviation Pre-Check",
        "asset_a_keywords": ["enrollment", "velocity", "forecast", "monte carlo", "sponsor", "accrual", "recruiting", "lpi"],
        "asset_b_keywords": ["protocol", "deviation", "pre-check", "dosing", "ecrf", "edc", "coordinator", "eligibility", "form lock"],
        "dossier_unresolved": """# Ground-Truth Dossier — BioNova Phase-II Oncology Trial Operations (Q3)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 clinical data engineers + 1 regulatory QA lead; 12-week Q3 build; $20,000 validation/infra cap; must satisfy 21 CFR Part 11 audit-trail rules inside BioNova's validated GxP cloud VPC (zero patient identifiers exposed externally).
- **Clinical Operations & Partner Governance Notes (Kickoff Memo):**
  - *"Co-development pharma partners and our board closely watch Phase-II readout timing, and giving sponsors a validated, Part-11-auditable enrollment-velocity forecast portal replaces fragile manual Friday spreadsheets with indisputable accrual proof."*
  - *"At the same time, our Data Safety Monitoring Board flagged 14 preventable site protocol deviations last month (wrong lab windows, missed exclusions, dosing-entry errors), and catching coordinator mistakes in real time before dosing or eCRF lock protects patient safety and our FDA IND."*
  - *"With 2 engineers + 1 QA lead for 12 weeks, we can only validate and ship one v1 system cleanly."*

## 2. Existing Engineering Assets
- **Asset A — Mature Site Enrollment & Screening Pipeline (90% complete):** Clean weekly pipeline pulling de-identified screening, consent, and randomization counts across all 22 trial sites into deterministic Monte Carlo accrual projection tables.
- **Asset B — Staging EDC Form Webhook & Protocol JSON (40% complete):** Validated staging Electronic Data Capture webhook emitting draft eCRF lab/eligibility/dosing saves prior to signature across 22 sites plus a machine-readable protocol schedule; no real-time rule engine, pre-lock modal, or Part 11 e-signature override flow exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 12-week Q3 build within the team and $20,000 validation constraints.
""",
        "spec_A": """# Candidate v1 Specification — Sponsor Enrollment-Velocity Forecast Portal

## 1. Core Objective
Launch a 21 CFR Part 11-validated sponsor-facing enrollment-velocity forecast portal and site-recruitment benchmark dashboard within 12 weeks by wrapping Asset A's mature screening pipeline and Monte Carlo accrual engine across all 22 Phase-II sites.

## 2. System Architecture
- **Validated Accrual Pipeline:** Weekly ETL inside BioNova's GxP VPC ingests de-identified site screening, screen-failure codes, and randomization counts from Asset A into versioned PostgreSQL tables and runs deterministic-seed Monte Carlo LPI confidence forecasts.
- **Sponsor & Partner Dashboard:** Role-scoped web portal showing actual-vs-planned enrollment curves, site activation rankings, and screen-failure breakdowns across all 22 sites.
- **Immutable Board Packs:** One-click PDF/slide summary exporter stamping every weekly snapshot with version metadata, random seed, and SHA-256 hash.

## 3. Security, Privacy & Operational Guardrails
- Strictly de-identified site-level aggregates only; zero patient PHI or subject IDs ever enter the portal.
- Full 21 CFR Part 11 versioned snapshots, RBAC, and immutable audit logs inside BioNova's validated GxP VPC; zero write connectivity to live EDC; delayed site feeds render last certified snapshot with explicit freshness stamps.

## 4. Rollout & Resource Budget
- **Team:** 2 clinical data engineers + 1 regulatory QA lead (weeks 1–4 ETL validation & biostats parity, weeks 5–7 portal UI & immutable packs, weeks 8–10 formal IQ/OQ validation testing, weeks 11–12 sponsor onboarding).
- **Validation/Infra Spend:** $6,200 (GxP VPC hosting, IQ/OQ tooling, compliance docs) — well under the $20,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 12-Week Window)
- 100% numeric reconciliation against biostats' reference Friday workbook across all 22 sites and 12 historical weeks during weeks 8–10 validation.
- 100% IQ/OQ test pass rate, < 2-second portal load time, and zero unauthorized data-access findings.

## 6. Explicit Non-Goals for v1
- Real-time EDC eCRF protocol-deviation pre-checks, pre-dosing eligibility/lab-window validation, and site coordinator warning modals (Asset B) are deferred to Future Phase 2.
""",
    },
    {
        "id": "U12_freight_reroute_vs_audit",
        "domain": "Cold-Chain Logistics Dispatch",
        "asset_a_label": "Carrier Performance Scorecard & Detention Invoice Auditor",
        "asset_b_label": "Live 3-Hour-Ahead Reefer & Dock-Delay Reroute Assistant",
        "asset_a_keywords": ["post-delivery", "scorecard", "detention", "invoice", "geofence", "qbr", "eld", "dispute", "billing"],
        "asset_b_keywords": ["live", "3-hour", "3 hour", "reefer", "temperature", "rerout", "mqtt", "cross-dock", "spoil"],
        "dossier_unresolved": """# Ground-Truth Dossier — GlacierLine Cold-Chain Freight Dispatch (Q4)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 backend/ops engineers; 10-week Q4 sprint; $15,000 infrastructure cap; human dispatchers must explicitly approve every route or appointment change (zero autonomous driver re-dispatch).
- **VP of Fleet Operations (Sponsor) Notes (Kickoff Brief):**
  - *"Automating post-delivery detention invoice audits and carrier scorecards with indisputable ELD geofence proof delivers fast, clean financial recovery (1–2% of carrier spend) and arms Procurement for Q1 carrier negotiations."*
  - *"At the same time, losing 9 cold-chain trailers last quarter at $95,000 each hurts terribly — catching slow reefer temperature climb or dock delays 3 hours early so our 24/7 dispatchers can reroute loads to partner cross-docks would save real cargo on the road."*
  - *"With two engineers for 10 weeks, we need to commit cleanly to one v1 build rather than spreading thin."*

## 2. Existing Engineering Assets
- **Asset A — Mature Post-Delivery ELD & Detention Invoice Pipeline (90% complete):** Nightly batch warehouse joining completed ELD GPS breadcrumbs, dock arrival timestamps, and carrier detention invoices across 18,000 completed loads at 99.2% invoice-variance accuracy.
- **Asset B — Live Telematics & Reefer Sensor Stream (40% complete):** Active MQTT stream delivering 5-minute trailer GPS pings, reefer box temperatures, and fuel levels from 240 active trailers alongside traffic ETA APIs and a directory of 38 cold-storage cross-docks; no thermal-drift scorer, ETA slip predictor, or unified dispatch exception board exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q4 sprint within the 2-engineer and $15,000 constraints.
""",
        "spec_A": """# Candidate v1 Specification — Carrier Performance Scorecard & Detention Invoice Auditor

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
""",
    },
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if SCENARIOS_DIR.exists():
        shutil.rmtree(SCENARIOS_DIR)
    SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)

    sha_lines: list[str] = []
    manifest_explicit = []
    manifest_underspec = []

    print(f"Generating {len(EXPLICIT_CONTROLS)} Regime-1 positive controls + {len(UNDERSPECIFIED_SCENARIOS)} Regime-2 underspecified scenarios...")

    for sc in EXPLICIT_CONTROLS:
        sdir = SCENARIOS_DIR / sc["id"]
        sdir.mkdir(parents=True, exist_ok=True)
        dp = sdir / "dossier.md"
        wp = sdir / "spec_wrong.md"
        dp.write_text(sc["dossier"].strip() + "\n", encoding="utf-8")
        wp.write_text(sc["spec_wrong"].strip() + "\n", encoding="utf-8")
        for p in (dp, wp):
            sha_lines.append(f"{sha256_file(p)}  {p.relative_to(ROOT).as_posix()}")
        manifest_explicit.append({
            "id": sc["id"],
            "regime": "explicit_contradiction",
            "domain": sc["domain"],
            "asset_a_keywords": sc["asset_a_keywords"],
            "asset_b_keywords": sc["asset_b_keywords"],
            "word_counts": {"dossier": len(dp.read_text().split()), "spec_wrong": len(wp.read_text().split())},
        })

    for sc in UNDERSPECIFIED_SCENARIOS:
        sdir = SCENARIOS_DIR / sc["id"]
        sdir.mkdir(parents=True, exist_ok=True)
        du = sdir / "dossier_unresolved.md"
        dr = sdir / "dossier_resolved_A.md"
        sa = sdir / "spec_A.md"

        du_txt = sc["dossier_unresolved"].strip() + "\n"
        signoff = SIGN_OFF_LINE_TEMPLATE.format(
            asset_a_label=sc["asset_a_label"],
            asset_b_label=sc["asset_b_label"],
        )
        dr_txt = du_txt + signoff
        sa_txt = sc["spec_A"].strip() + "\n"

        du.write_text(du_txt, encoding="utf-8")
        dr.write_text(dr_txt, encoding="utf-8")
        sa.write_text(sa_txt, encoding="utf-8")
        for p in (du, dr, sa):
            sha_lines.append(f"{sha256_file(p)}  {p.relative_to(ROOT).as_posix()}")

        print(
            f"  {sc['id']:32s} | unres={len(du_txt.split()):3d}w | res={len(dr_txt.split()):3d}w | specA={len(sa_txt.split()):3d}w"
        )
        manifest_underspec.append({
            "id": sc["id"],
            "regime": "underspecified_tension",
            "domain": sc["domain"],
            "asset_a_label": sc["asset_a_label"],
            "asset_b_label": sc["asset_b_label"],
            "asset_a_keywords": sc["asset_a_keywords"],
            "asset_b_keywords": sc["asset_b_keywords"],
            "word_counts": {
                "dossier_unresolved": len(du_txt.split()),
                "dossier_resolved_A": len(dr_txt.split()),
                "spec_A": len(sa_txt.split()),
            },
        })

    manifest_path = ROOT / "scenarios_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "n_explicit_controls": len(manifest_explicit),
                "n_underspecified": len(manifest_underspec),
                "explicit_controls": manifest_explicit,
                "underspecified_scenarios": manifest_underspec,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    sha_lines.append(f"{sha256_file(manifest_path)}  scenarios_manifest.json")

    proto = ROOT / "PROTOCOL.md"
    if proto.is_file():
        sha_lines.append(f"{sha256_file(proto)}  PROTOCOL.md")

    sha_path = ROOT / "scenarios.sha256"
    sha_path.write_text("\n".join(sorted(sha_lines)) + "\n", encoding="utf-8")
    print(f"Sealed {len(sha_lines)} SHA-256 entries -> {sha_path}")


if __name__ == "__main__":
    main()
