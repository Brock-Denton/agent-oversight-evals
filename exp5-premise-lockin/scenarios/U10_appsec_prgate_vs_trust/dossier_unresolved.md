# Ground-Truth Dossier — PayRail Application Security Team (Q2)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 AppSec engineers; 8-week Q2 sprint; $10,000 tooling cap; must run inside PayRail's private CI/GitHub Enterprise boundary with zero source code leaving the corporate network.
- **Security Leadership (Sponsor) Notes (Sprint Charter):**
  - *"Enterprise fintech prospects scrutinize our security posture every sales cycle, and turning our clean DefectDojo metrics into an audited CISO benchmark and external Trust Center badge pack gives verifiable proof without burning AppSec hours on repetitive questionnaires."*
  - *"At the same time, our PR SAST scanners fire 620 alerts a month at an 81% false-positive rate — developers ignore the noise, which let two real IDOR bugs slip last month — so filtering noise from developer dismissals and verifying inline fixes on PRs would genuinely raise code security."*
  - *"With two AppSec engineers for 8 weeks, we have to choose one crisp v1 deliverable."*

## 2. Existing Engineering Assets
- **Asset A — Mature Multi-Scanner SAST Aggregator & DefectDojo Metrics Store (90% complete):** Nightly pipeline consolidating Semgrep, CodeQL, and dependency counts across 48 microservices into clean vulnerability-density and MTTR tables.
- **Asset B — GitHub Enterprise PR Webhook & Developer Dismissal Logs (45% complete):** 7,800 historical PR findings with AppSec triage labels (`true_positive`, `false_positive_sanitizer`, `false_positive_test_only`) and CI runner access on 10 payment APIs; no suppression engine or test-verified patch bot exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 8-week Q2 sprint within the 2-engineer and $10,000 constraints.
