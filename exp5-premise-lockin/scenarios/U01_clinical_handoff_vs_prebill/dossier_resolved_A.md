# Ground-Truth Dossier — Northside Regional Hospital Informatics (Q1)

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

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Pre-Bill ICD-10 Compliance Audit Console) for v1**, approving the deferral of Asset B (Bedside Shift-Handoff Override-Learning Loop) to Future Phase 2.
