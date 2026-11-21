# Candidate v1 Specification — Advisory Essay Originality & Stylometry Review Panel

## 1. Core Objective
Launch a FERPA-compliant, evidence-first essay originality and stylometry review panel across Oakridge high schools within 9 weeks by calibrating and deploying Asset A's mature similarity microservice inside the submission workflow.

## 2. System Architecture
- **Calibrated Scoring Worker:** On submission, a district-VPC worker runs Asset A (<300 ms) to compute exact web-corpus n-gram overlaps and stylometric drift relative to the student's prior in-class baseline drafts, storing structured metrics in district PostgreSQL.
- **Evidence-First Teacher Panel:** Presents advisory tiers (*Standard*, *Review Recommended*, *High Match*) alongside exact matched text spans and draft edit-time history so teachers inspect concrete evidence rather than opaque scores.
- **Fairness & Appeal Log:** Teachers log confirmed vs. false-positive dispositions stratified by grade level and ELL cohort to monitor calibration continuously.

## 3. Security, Privacy & Operational Guardrails
- 100% FERPA-compliant inside district-owned cloud VPC; zero student essays leave district control or touch external training endpoints.
- Explicit policy guardrail prohibits auto-grading penalties; student identifiers are masked in calibration exports; worker timeout degrades cleanly to normal unblocked submission.

## 4. Rollout & Resource Budget
- **Team:** 2 engineers + 1 curriculum specialist (weeks 1–3 VPC hardening & ELL threshold calibration on the 8,000-essay archive, weeks 4–6 teacher review panel, weeks 7–8 pilot with 6 teachers, week 9 district launch).
- **Infra Spend:** $2,800 (district VPC compute and encrypted backups) — well under the $9,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 9-Week Window)
- < 2% false-flag rate on known human-written ELL and native essays across the 8,000-essay benchmark archive in weeks 1–3 and 6-teacher pilot in weeks 7–8.
- < 1-second scoring turnaround and 100% FERPA data-residency audit pass.

## 6. Explicit Non-Goals for v1
- Interactive mid-draft student revision coaching, targeted structural prompts, and draft-to-draft teacher diff tracking (Asset B) are deferred to Future Phase 2.
