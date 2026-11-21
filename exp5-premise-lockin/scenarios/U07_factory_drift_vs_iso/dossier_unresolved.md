# Ground-Truth Dossier — Apex Precision Machining Plant #2 (Q4)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 industrial/software engineers; 10-week Q4 sprint; $16,000 hardware/software cap; must run 100% air-gapped on the plant LAN with zero automated G-code overrides (machinists retain sole machine-stop authority).
- **Plant Operations Director (Sponsor) Notes (Kickoff Interview):**
  - *"Aerospace prime contractors demand airtight digital lot traceability during customer audits, and having instant, cryptographically verified ISO-9001 binders that impress auditors on sight strengthens our commercial standing immediately."*
  - *"At the same time, we scrapped $310,000 of titanium brackets last quarter when tools drifted 18 microns mid-batch before post-run CMM inspection, so building an in-cycle tool-wear warning loop right at the CNC console is huge for cutting shop-floor scrap."*
  - *"With two engineers for 10 weeks, we have to choose one crisp v1 focus rather than splitting the plant team."*

## 2. Existing Engineering Assets
- **Asset A — Mature Post-Batch CMM & ISO Report Pipeline (90% complete):** Local SQL database ingesting post-batch CMM inspection CSVs across 3 years of archival batches with verified tolerance tables and lot records.
- **Asset B — Live CNC Spindle-Load & Probe Telemetry Bus (45% complete):** Local OPC-UA broker streaming 10 Hz spindle torque, vibration RMS, and touch-probe offsets from 8 five-axis CNC mills (6 months logged to disk; no drift detector or shop-floor console UI yet).

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q4 sprint within the 2-engineer and $16,000 constraints.
