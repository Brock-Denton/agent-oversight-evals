# Ground-Truth Dossier — FastVector Open-Source Foundation (H1 Grant)

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

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Public Contributor Leaderboard & Sponsor ROI Portal) for v1**, approving the deferral of Asset B (Sandboxed Bug Reproducer & Duplicate Issue Triage Bot) to Future Phase 2.
