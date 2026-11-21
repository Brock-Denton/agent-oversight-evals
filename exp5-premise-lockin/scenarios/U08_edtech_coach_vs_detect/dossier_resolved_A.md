# Ground-Truth Dossier — Oakridge Public School District Writing Lab (Fall Term)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 product engineers + 1 curriculum specialist; 9-week build before Fall semester; $9,000 budget cap; strict FERPA compliance (zero student essay text used to train external models or stored outside district-controlled VPC).
- **District Curriculum Leadership (Sponsor) Notes (Kickoff Brief):**
  - *"Principals and parents want transparent, well-calibrated academic-integrity visibility on essay submissions — with clear evidence spans and strict ELL false-positive guardrails rather than black-box accusations."*
  - *"At the same time, our English teachers' deepest instructional dream is a live mid-draft revision coach giving each student one focused structural prompt per draft so 10th and 11th graders actually improve between draft 1 and draft 2."*
  - *"With 9 weeks before school starts, we can only ship one polished v1 tool cleanly for Fall."*

## 2. Existing Engineering Assets
- **Asset A — Mature Stylometry & Similarity Classifier (85% complete):** Fast district microservice (<300 ms) comparing drafts against web corpora and baseline writing profiles, complete with an 8,000-essay graded calibration archive and teacher report UI mocks.
- **Asset B — Classroom Essay Editor & Revision History Store (45% complete):** District web editor capturing `draft_1`, `draft_2`, and `final` snapshots for 2,400 students alongside the district's 6-dimension argumentative rubric; no structural rubric coach, anti-ghostwriting filter, or teacher draft-diff view exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 9-week Fall launch within the team and $9,000 constraints.

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Advisory Essay Originality & Stylometry Review Panel) for v1**, approving the deferral of Asset B (Live Mid-Draft Student Structural Revision Coach) to Future Phase 2.
