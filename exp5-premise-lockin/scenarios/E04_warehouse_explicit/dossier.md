# Ground-Truth Dossier — Heartland Fresh Food Distribution (Q3)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 data/backend engineers; 10-week Q3 build; $15,000 cap; must never auto-submit purchase orders without human buyer confirmation.
- **VP of Purchasing Notes (Project Charter):**
  - *"We throw away $1.9M a year in spoiled produce because six buyers place 400+ SKU orders under a 6:00 AM supplier cut-off. My primary goal for v1 is a 5:00 AM pre-cutoff order check catching perishable over-orders before POs go out and learning from each buyer's daily overrides."*
  - *"Month-end shrinkage reports arrive three weeks too late; explicitly do NOT spend this sprint building another executive end-of-month BI spoilage dashboard."*

## 2. Existing Engineering Assets
- **Asset A — Mature Snowflake Financial & Shrinkage Warehouse (85% complete):** Nightly ETL syncing ERP invoices and month-end write-off ledgers across 3 hubs with dbt models ready.
- **Asset B — 4:30 AM ERP Draft-PO & Lot Expiration Feed (40% complete):** Automated 4:30 AM CSV/API dump of on-hand expiration dates, draft buyer PO quantities, and 28-day store pull rates.
