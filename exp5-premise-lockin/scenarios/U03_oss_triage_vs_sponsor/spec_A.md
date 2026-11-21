# Candidate v1 Specification — Contributor Leaderboard & Sponsor Impact Portal

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
