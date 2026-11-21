# Candidate v1 Specification — Public 311 Transparency Map & District Scorecard

## 1. Core Objective
Launch an accessible citizen-facing 311 transparency map and council-district response-time scorecard within 10 weeks by extending Asset A's mature PostGIS tile server and quarterly open-data exporter.

## 2. System Architecture
- **Sanitized Spatial ETL:** Nightly job reads open and closed 311 tickets from a read-only replica, strips caller names and phone numbers, snaps exact addresses to 100-meter street-block centroids, and refreshes PostGIS vector tiles plus district SLA aggregates.
- **Public Web Portal:** WCAG 2.1 AA responsive web map displaying repair heatmaps, category filters, median days-to-close trends, and one-click CSV/JSON open-data downloads.
- **Council Briefings:** Automated monthly district summary packs formatted cleanly for City Council packets.

## 3. Security, Privacy & Operational Guardrails
- Automated PII anonymization tests verify zero resident contact info or exact house numbers enter tiles or CSV exports before CDN publication.
- Strictly read-only replica access (zero write paths to crew dispatch tables; zero new crew tablets required); CDN caching protects internal servers from traffic spikes.

## 4. Rollout & Resource Budget
- **Team:** 2 civic engineers (weeks 1–3 PII block-snapping ETL & PostGIS views, weeks 4–6 accessible map UI & council exports, weeks 7–8 WCAG 2.1 AA audit & numeric reconciliation, weeks 9–10 public launch).
- **Infra Spend:** $3,500 (CDN tile hosting and accessibility audit) — well under the $14,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 10-Week Window)
- 100% pass on PII anonymization suite and WCAG 2.1 AA audit in weeks 7–8, with 100% numeric parity against official quarterly 311 totals.
- < 1.5-second p95 mobile map load time under simulated council-meeting traffic spike.

## 6. Explicit Non-Goals for v1
- Incoming duplicate 311 ticket merging, corridor-based crew route batching, and field dispatch workflow integration (Asset B) are deferred to Future Phase 2.
