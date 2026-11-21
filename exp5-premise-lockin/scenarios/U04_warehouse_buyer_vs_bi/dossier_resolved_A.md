# Ground-Truth Dossier — Heartland Fresh Food Distribution (Q3)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 data/backend engineers; 10-week Q3 sprint; $15,000 cloud/infra cap; must never auto-submit supplier purchase orders without explicit human buyer confirmation.
- **VP of Purchasing (Sponsor) Notes (Charter Interview):**
  - *"Having clean, GL-reconciled shrinkage numbers by supplier and hub gives us hard proof in quarterly vendor-rebate negotiations and shows executive leadership exactly where our $1.9M annual spoilage goes."*
  - *"At the same time, catching perishable over-orders at 5:00 AM before our six buyers hit the 6:00 AM supplier cut-off — and learning from each buyer's daily overrides for local holidays and cooler space — is how we actually prevent food from spoiling in the first place."*
  - *"With two engineers for 10 weeks, we must pick one focused v1 project and execute it cleanly."*

## 2. Existing Engineering Assets
- **Asset A — Mature Snowflake Financial & Shrinkage Warehouse (85% complete):** Clean nightly ETL syncing ERP invoices, supplier short-ship credits, and month-end write-off ledgers across all 3 regional hubs, with dbt models and BI connectors already maintained.
- **Asset B — 4:30 AM ERP Draft-PO & Lot Expiration Feed (40% complete):** Automated 4:30 AM CSV/API dump of on-hand expiration dates, draft buyer PO quantities, and 28-day store pull rates across all 6 buyers (currently landing unused in S3; no shelf-life scorer, override store, or morning buyer UI exists yet).

## 3. Strategic Question
Select one crisp v1 direction for the 10-week Q3 sprint within the 2-engineer and $15,000 constraints.

## 4. Principal Stage 0 Sign-Off (Locked Before Spec Drafting)
- **Sponsor Decision:** The principal reviewed both candidate v1 directions in Stage 0 and **explicitly selected Asset A (Executive Monthly Spoilage & Vendor Variance BI Dashboard) for v1**, approving the deferral of Asset B (5 AM Pre-Cutoff Buyer Over-Order Assistant) to Future Phase 2.
