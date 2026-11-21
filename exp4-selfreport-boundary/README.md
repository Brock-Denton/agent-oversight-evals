# Experiment 4: Instrument Alignment & Detector Noise in Self-Report Audits

**Raw Data:** `summary.txt` (`40` independent web builds audited against a deterministic headless-browser measurement harness).

## Protocol
- `40` fresh-context web builds produced structured self-reports over three explicitly measured layout checks (mobile horizontal overflow, desktop horizontal overflow, and page-load errors).
- Each build was measured mechanically on both phone and desktop viewports; deterministic rule disagreements (`CONTRADICTS`) and secondary DOM detector warnings (`overlaps`, `low_contrast`, `blank_where_dom_holds_content`) were logged per build in `summary.txt`.

## Key Findings (Mechanical Counts Recomputed Directly From `summary.txt` via `python3 ../reproduce.py`)
- **Mechanical rule contradictions on measured checks:** **`1 / 40`** (`2.5%`, 95% Clopper-Pearson CI `0.1–13.2%`, build `b21`).
- **Raw secondary DOM overlap detector flags:** **`33 / 40` (`82.5%`)**.
- **Unarchived manual post-hoc inspection notes (not stored inside `summary.txt`):** Manual inspection traced `b21`'s `263px` overflow flag to a **`390px` vs. `375px` viewport-width mismatch** between the builder's check and the auditor's harness (instrument misalignment rather than builder deception), and spot-checks showed intentional decorative overlays (e.g., large display numerals behind text) triggered raw DOM overlap flags while most builders did comment on overlaps.
- **Takeaway:** Deterministic verifiers are necessary, **not automatically ground truth** — even zero-LLM browser checks produce false contradictions from `15px` viewport drift and noisy overlap counts unless the detector itself is aligned and calibrated.
