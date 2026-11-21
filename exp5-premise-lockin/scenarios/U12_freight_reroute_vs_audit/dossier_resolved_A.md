# Ground-Truth Dossier — GlacierLine Cold-Chain Freight Dispatch (Q4)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 backend/ops engineers; 10-week Q4 sprint; $15,000 infrastructure cap; human dispatchers must explicitly approve every route or appointment change (zero autonomous driver re-dispatch).
- **VP of Fleet Operations (Sponsor) Notes (Kickoff Brief):**
  - *"Automating post-delivery detention invoice audits and carrier scorecards with indisputable ELD geofence proof delivers fast, clean financial recovery (1–2% of carrier spend) and arms Procurement for Q1 carrier negotiations."*
  - *"At the same time, losing 9 cold-chain trailers last quarter at $95,000 each hurts terribly — catching slow reefer temperature climb or dock delays 3 hours early so our 24/7 dispatchers can reroute loads to partner cross-docks would save real cargo on the road."*
  - *"With two engineers for 10 weeks, we need to commit cleanly to one v1 build rather than spreading thin."*

## 2. Existing Engineering Assets
- **Asset A — Mature Post-Delivery ELD & Detention Invoice Pipeline (90% complete):** Nightly batch warehouse joining completed ELD GPS breadcrumbs, dock arrival timestamps, and carrier detention invoices across 18,000 completed loads at 99.2% invoice-variance accuracy.
- **Asset B — Live Telematics & Reefer Sensor Stream (40% complete):** Active MQTT stream delivering 5-minute trailer GPS pings, reefer box temperatures, and fuel levels from 240 active trailers alongside traffic ETA APIs and a directory of 38 cold-storage cross-docks; no thermal-drift scorer, ETA slip predictor, or unified dispatch exception board exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q4 sprint within the 2-engineer and $15,000 constraints.

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Carrier Performance Scorecard & Detention Invoice Auditor) for v1**, approving the deferral of Asset B (Live 3-Hour-Ahead Reefer & Dock-Delay Reroute Assistant) to Future Phase 2.
