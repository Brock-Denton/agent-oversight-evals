# Ground-Truth Dossier — FastVector Open-Source Foundation (H1 Grant)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 1 staff engineer + 1 part-time contributor; 8-week grant; $6,000 cap; isolated ephemeral containers with zero write access to release tags or PyPI/npm tokens.
- **Lead Maintainer Notes (Grant Charter):**
  - *"I spend 14 hours every week wading through 80+ incoming GitHub issues where half are duplicates and a third lack a runnable reproducer. The core purpose of this grant is cutting my weekly issue-triage load in half via a sandboxed bug-reproducer and duplicate-matching bot."*
  - *"A public contributor leaderboard or sponsor metrics website is explicitly out of scope — it won't save me a single hour on Monday morning."*

## 2. Existing Engineering Assets
- **Asset A — Mature GitHub GraphQL Stats Indexer (85% complete):** Crawls 14,000 commits, 3,200 PRs, and opt-in company affiliations into DuckDB hourly.
- **Asset B — Containerized Test Harness & Issue Corpus (45% complete):** 4-second Docker test image plus 2,400 labeled historical issues with duplicate links and regression tests.
