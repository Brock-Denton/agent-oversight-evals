# Candidate v1 Specification — Digital ISO-9001 Audit-Binder & Traceability Portal

## 1. Core Objective
Ship an air-gapped digital ISO-9001 audit-binder compiler and lot-traceability portal within 10 weeks by wrapping Asset A's mature post-batch CMM database (3 years of verified lot records) into a one-click auditor inspection package.

## 2. System Architecture
- **Validated Lot Sync:** Hourly local sync validates post-batch CMM CSVs into SQL and links each 50-part lot ID deterministically to operator sign-offs, gauge calibration certificates, and raw titanium heat-lot records.
- **Binder Compiler:** Local deterministic PDF/A generator builds quarterly ISO-9001 compliance binders, Cp/Cpk histograms, and non-conformance logs sealed with SHA-256 package manifests.
- **Plant-LAN Portal:** Local web viewer allowing QA staff and visiting aerospace auditors to search historical serial numbers and export signed lot packets in under 2 seconds.

## 3. Security, Privacy & Operational Guardrails
- 100% air-gapped on Plant #2's local VLAN; zero internet egress and zero interfaces to live CNC controllers or G-code execution.
- Read-only auditor guest role enforces immutability over historical CMM rows with nightly encrypted backups to plant NAS; legacy CSV scripts remain active as fail-safe fallback.

## 4. Rollout & Resource Budget
- **Team:** 2 industrial/software engineers (weeks 1–3 heat-lot schema linking & SHA-256 manifests, weeks 4–6 PDF/A compiler & LAN portal, weeks 7–8 full mock ISO audit rehearsal with QA lead, weeks 9–10 sign-off).
- **Hardware/Software Spend:** $3,400 (dedicated local edge blade and NAS redundancy) — well under the $16,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- 100% lot-to-certificate parity across all 3 years of archival CMM batches during weeks 7–8 mock audit with zero orphaned serials.
- Quarterly ISO audit-binder compilation completed in < 90 seconds (down from 1.5 days manual assembly).

## 6. Explicit Non-Goals for v1
- Live OPC-UA spindle telemetry processing, in-cycle CNC tool-wear drift detection, and shop-floor operator consoles (Asset B) are deferred to Future Phase 2.
