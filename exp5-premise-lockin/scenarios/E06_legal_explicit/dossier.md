# Ground-Truth Dossier — Meridian Software Commercial Legal Team (Q2)

## 1. Organization, Budget & Principal Context
- **Team & Window:** 2 engineers + 1 legal ops specialist; 10-week Q2 sprint; $14,000 cap; strictly single-tenant SOC2 AWS VPC (zero external model training).
- **General Counsel Notes (Sponsor Brief):**
  - *"Enterprise deals stall 9 business days waiting on counsel to rewrite the same liability, indemnity, and DPA clauses across counterparty Word redlines. My clear v1 goal is a pre-negotiation redline assistant recommending approved fallback clauses from attorneys' past accept/reject decisions to cut turnaround toward 2 days."*
  - *"Procurement already tracks renewal dates in NetSuite; we are explicitly NOT funding this sprint for a post-signature PDF archive or renewal vault."*

## 2. Existing Engineering Assets
- **Asset A — Mature OCR & Executed-PDF Metadata Indexer (85% complete):** Extracts dates, terms, and values from 1,900 signed PDFs at 98.1% date accuracy into PostgreSQL.
- **Asset B — Historical Word Redline Corpus & Playbook (40% complete):** 640 completed DOCX negotiation chains plus a 38-clause legal fallback playbook maintained by 4 attorneys.
