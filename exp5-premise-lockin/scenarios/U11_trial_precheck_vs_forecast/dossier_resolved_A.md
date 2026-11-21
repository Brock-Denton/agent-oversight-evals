# Ground-Truth Dossier — BioNova Phase-II Oncology Trial Operations (Q3)

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

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Sponsor Enrollment-Velocity Forecast Portal) for v1**, approving the deferral of Asset B (Real-Time Site Protocol-Deviation Pre-Check) to Future Phase 2.
