# Candidate v1 Specification — Sponsor Enrollment-Velocity Forecast Portal

## 1. Core Objective
Launch a 21 CFR Part 11-validated sponsor-facing enrollment-velocity forecast portal and site-recruitment benchmark dashboard within 12 weeks by wrapping Asset A's mature screening pipeline and Monte Carlo accrual engine across all 22 Phase-II sites.

## 2. System Architecture
- **Validated Accrual Pipeline:** Weekly ETL inside BioNova's GxP VPC ingests de-identified site screening, screen-failure codes, and randomization counts from Asset A into versioned PostgreSQL tables and runs deterministic-seed Monte Carlo LPI confidence forecasts.
- **Sponsor & Partner Dashboard:** Role-scoped web portal showing actual-vs-planned enrollment curves, site activation rankings, and screen-failure breakdowns across all 22 sites.
- **Immutable Board Packs:** One-click PDF/slide summary exporter stamping every weekly snapshot with version metadata, random seed, and SHA-256 hash.

## 3. Security, Privacy & Operational Guardrails
- Strictly de-identified site-level aggregates only; zero patient PHI or subject IDs ever enter the portal.
- Full 21 CFR Part 11 versioned snapshots, RBAC, and immutable audit logs inside BioNova's validated GxP VPC; zero write connectivity to live EDC; delayed site feeds render last certified snapshot with explicit freshness stamps.

## 4. Rollout & Resource Budget
- **Team:** 2 clinical data engineers + 1 regulatory QA lead (weeks 1–4 ETL validation & biostats parity, weeks 5–7 portal UI & immutable packs, weeks 8–10 formal IQ/OQ validation testing, weeks 11–12 sponsor onboarding).
- **Validation/Infra Spend:** $6,200 (GxP VPC hosting, IQ/OQ tooling, compliance docs) — well under the $20,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 12-Week Window)
- 100% numeric reconciliation against biostats' reference Friday workbook across all 22 sites and 12 historical weeks during weeks 8–10 validation.
- 100% IQ/OQ test pass rate, < 2-second portal load time, and zero unauthorized data-access findings.

## 6. Explicit Non-Goals for v1
- Real-time EDC eCRF protocol-deviation pre-checks, pre-dosing eligibility/lab-window validation, and site coordinator warning modals (Asset B) are deferred to Future Phase 2.
