# Ground-Truth Dossier — Metro Public Works 311 Modernization (FY26)

## 1. Organization, Constraints & Principal Context
- **Team & Window:** 2 civic software engineers; 10-week sprint; $14,000 budget cap; must integrate cleanly with existing city systems without buying new cellular tablets for crews.
- **Public Works & City Modernization Notes (Charter Briefing):**
  - *"City Council and residents keep demanding transparent, easy-to-verify proof of where repair dollars go — shipping an accessible neighborhood 311 map and district response-time scorecard builds public trust quickly."*
  - *"At the same time, field asphalt and lighting crews lose ~27% of dispatches to duplicate reports of the same pothole or dark streetlight, so deduplicating work orders and batching daily routes by corridor would let crews fix far more streets per shift."*
  - *"With two engineers for 10 weeks, we have to select one clear v1 deliverable."*

## 2. Existing Engineering Assets
- **Asset A — Mature Public GIS Tile Server & Open-Data Exporter (90% complete):** Fast municipal PostGIS/Mapbox tile pipeline already serving neighborhood polygons and quarterly 311 resolution-time stats cleanly to browsers.
- **Asset B — Raw 311 Work-Order Feed & Crew Dispatch Logs (40% complete):** Hourly incoming 311 tickets (lat/lon, free-text address, category) plus 18 months of completed crew logs showing ~27% manually marked duplicate; no spatial deduplicator, dispatcher merge queue, or corridor route batcher exists yet.

## 3. Strategic Question
Select one crisp v1 direction for the 10-week sprint within the 2-engineer and $14,000 constraints.
