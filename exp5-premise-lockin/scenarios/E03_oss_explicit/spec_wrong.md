# Candidate v1 Specification — Contributor Leaderboard & Sponsor Impact Portal

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
