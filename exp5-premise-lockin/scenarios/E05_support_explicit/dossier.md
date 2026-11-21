# Ground-Truth Dossier — CloudSync B2B Support Engineering (Q1)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 full-stack engineers; 8-week build; $10,000 cap; strict customer PII scrubbing required.
- **Head of Customer Experience Notes (Product Brief):**
  - *"Our agents already hold 94% CSAT. Our real nightmare is answering the same 25 product bugs and stale doc traps 300 times a month because tier-2 findings die in closed Zendesk threads. For v1, I want a closed loop turning recurring tier-2 escalations into verified Jira bug drafts and help-doc patch PRs."*
  - *"We already coach agent tone in weekly 1-on-1s; explicitly do not spend v1 building an automated agent-QA tone scorecard."*

## 2. Existing Engineering Assets
- **Asset A — Mature Zendesk Sentiment & Agent-Tone Scorer (90% complete):** Scores 100% of closed replies for empathy and predicted CSAT (0.89 AUC) into BigQuery.
- **Asset B — Tier-2 Escalation Threads & Docs Repo (40% complete):** ~180 weekly tier-2 escalation logs plus Git-hosted Markdown help center and Jira API access.
