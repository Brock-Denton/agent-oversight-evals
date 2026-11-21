# Ground-Truth Dossier — CloudSync B2B Support Engineering (Q1)

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

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Automated Support Agent QA & CSAT Scorecard) for v1**, approving the deferral of Asset B (Closed-Loop Tier-2 Escalation to Jira & Docs Pipeline) to Future Phase 2.
