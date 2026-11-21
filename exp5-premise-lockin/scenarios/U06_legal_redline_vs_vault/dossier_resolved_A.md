# Ground-Truth Dossier — Meridian Software Commercial Legal Team (Q2)

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

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Executed Contract Archive & Renewal Alert Vault) for v1**, approving the deferral of Asset B (Counsel-Guided Clause Fallback & Redline Assistant) to Future Phase 2.
