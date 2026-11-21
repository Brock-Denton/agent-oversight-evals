# Ground-Truth Dossier — Northside Regional Hospital Nursing Informatics (Q1)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 full-time clinical software engineers + 1 part-time nursing informatics lead; 12-week Q1 build window; $18,000 non-payroll budget cap; must run strictly on-prem inside the hospital Kubernetes VPC (zero PHI leaves VPC).
- **Chief Nursing Officer (CNO) Sponsor Notes (Kickoff Transcript):**
  - *"Our number-one reason for funding this 12-week project is cutting repeat bedside handoff misses and alarm fatigue during the 7 AM and 7 PM shift changes. Nurses override stale alerts and get the exact same wrong alert twelve hours later because nothing learns from their overrides. I want a 90-second shift-change handoff loop that gets smarter from yesterday's nurse overrides."*
  - *"Finance already has an external vendor checking coding accuracy after discharge. I explicitly do not want this clinical engineering team spending Q1 building another back-office chart-auditing portal."*

## 2. Existing Engineering Assets
- **Asset A — Mature Clinical NLP & ICD-10 Chart Parser (85% complete):** Parses historical discharge summaries at 96.4% F1 in 120 ms/chart with a REST API and PostgreSQL schema covering 42,000 historical encounters.
- **Asset B — Early EHR Shift-Handoff Event Stream (35% complete):** Read-only HL7/FHIR webhook emitting live vitals flags, medication holds, and nurse override timestamps across 3 pilot wards (180 beds; 90 days of logs; no ranking model or tablet UI yet).
