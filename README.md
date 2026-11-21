# Agent Oversight Evals

**Empirical stress-tests of frontier AI models acting as builders, reviewers, and blind multi-family judges — across real production build gates, causal ablations, blind multi-rater AI adjudication, controlled randomized trials, and clean-room anti-cheat oracles.**

- **Transparent, reproducible statistics** — standard-library Python 3 only; `python3 reproduce.py` deterministically recomputes Exp 1 (`310` non-self production gates + `16`-session paired causal ablation + `24`-session blind AI adjudication), Exp 2 (directly from `45` per-case `by_case` counts), Exp 3 `v3` (`72` runs across `12` tasks with `30/30` pre-run task/protocol SHA-256 verification + `4/4` post-audit harness verification + archived `v2` & `v1` lineage), and Exp 4 (mechanical counts directly from `summary.txt`, with manual inspection notes labeled separately).

```bash
git clone https://github.com/Brock-Denton/agent-oversight-evals
cd agent-oversight-evals
(cd exp3-unrepairable-honesty && shasum -a 256 -c tasks.sha256 && shasum -a 256 -c harness_post_audit.sha256)
python3 reproduce.py
```

---

## Four Empirical Findings on Frontier Model Oversight

### 1. Real Production Multi-Family Blind Jury, Causal Ablation & Blind AI Adjudication (`exp1-production-jury/` — `310` non-self gates, `443` blind votes, `48` named paired sessions)
When autonomous coding agents submit real builds for two-stage verification (`35` Stage 1 mechanical blocks, `74` Stage 1-only dry runs, `198` completed Stage 2 panels [`110` PASS / `88` BLOCK], `1` Stage 2 error, `2` incomplete = `310` gates; `170` paired `GPT-6.2 Sol` vs. `Claude Opus 5.5` audits; `70` contested `1–1` `Gemini 4 Neon` tie-breaks; `12` self-evaluation meta-gates excluded):

| Metric (`gates_anonymized.json`, `agents_md_ablation.json`, `ties_ground_truth_audit.json`) | Exact Result | Statistical Proof & Caveats |
| :--- | :---: | :--- |
| **Session-clustered sign test (`n = 48` named sessions)** | **30** Codex > Claude · **0** Claude > Codex · 18 tied | Exact sign test **`p = 1.86 × 10^-9`** (+12 null-session singletons incl. `g038`: `36` vs. `1`, `p = 5.50 × 10^-10`) |
| **Chronological first attempt / session (`n = 48`)** | **89.6% vs. 60.4%** block (**`14` vs. `0`** split; `60.4%` both BLOCK) | Exact McNemar **`p = 0.000122`** (`κ = 0.3015`) |
| **All paired audits (`n = 170`; builds only `n = 158`)** | **80.6% vs. 39.4%** (`71` vs. `1`; builds **`65` vs. `0`**) | Exact McNemar **`p = 3.09 × 10^-20`** (`κ = 0.2501`); `52/71` (`73.2%`) proof-completeness vs. `6/71` (`8.5%`) bugs |
| **Paired causal ablation (`CODEX_HOME` isolation, `n = 16` sessions)** | **11/12 vs. 11/12** contested (`1` vs. `1` flip) · **4/4** mutual | Exact McNemar **`p = 1.000`** (no net shift from `AGENTS.md` leakage) |
| **24-session blind multi-rater AI adjudication (`gemini-4-neon-xhigh`, `seed=20261121`)** | **3/24 (12.5%)** real missed defects (**`1` unique recurring UI bug** across `T09`/`T10`/`T15`) · **15/24** unproven-claim · **6/24** nitpicks | Binary defect **`24/24` (`κ = 1.000`)**; 3-class `κ = 0.196` (`11/14` dot-only `unittest` logs). Expanded `82`-session live split pool (`11` in-310 [`1/11`] + `13` post-310 [`2/13`]); model-graded, human review pending |
| **Tie-breaker alignment (`Gemini 4 Neon` high, `n = 70` `1–1` ties)** | **PASS 67/70 (95.7%)** · CI `88.0–99.1%` | Aligns with Claude's visible-defect threshold |
| **Regime-matched self-preference check (`Claude` & `Gemini`)** | Claude `21/48 vs. 41/107` (`p = 0.596`) · Gemini ties `0/46 vs. 2/17` (`p = 0.070`) | **Null** — no significant self-preference when regime-matched |

### 2. Reviewer Fault-Taxonomy Randomized Trial (`exp2-rubric-false-alarms/` — `45` audio-film cases, `180` reviews, `2.78M` tokens)
Evaluated on a single frontier reviewer (`claude-opus-5-5`, high effort; same-family blind judges, `15/16` calibration, `174/179` first-pass agreement), recomputed directly from `by_case`:
- **No recall lift:** True planted-fault recall was **`24/70` (`34.3%`) vs. `23/70` (`32.9%`)** (mean exact hits/review `0.267` vs. `0.256`, paired `p = 1.000`).
- **Overhead + low-confidence noise on seen cases:** Token spend jumped **`+48.6%`** (`18,470` vs. `12,431`/review, `p < 0.0001`) and notes/review rose `+0.211` (`p = 0.0051`). Mean false alarms/review rose **`0.322` vs. `0.200`** (`p = 0.0257`; binary `≥1` review rate across all 45 cases `27/90 = 30.0%` vs. `18/90 = 20.0%`, `p = 0.0781`); on `13` clean controls (all `seen = true`), mean count rose `0.500` vs. `0.231` (`p = 0.03125`) while binary review rate was `12/26` (`46.2%`) vs. `6/26` (`23.1%`, `p = 0.0625`). Unseen `fresh` cases (`n = 13`: `0.269` vs. `0.192`, `p = 0.6875`) and high-confidence `false_sure` errors (`0.0%` vs. `1.1%`, `p = 1.0`) were null (archived verdict: `"no clear effect"`).

### 3. Clean-Room Unrepairable-Constraint Honesty Benchmark & Mechanical Oracle (`exp3-unrepairable-honesty/` — `v3`: `71/72` valid across `12` tasks + archived `v2` & `v1`)
Twelve independent Python tasks (`2` per class × `6` classes; `30/30` frozen pre-run task/protocol files verified in `tasks.sha256`, post-audit harness fixes locked in `harness_post_audit.sha256` with pre-run hashes archived in `PRE_RUN_HARNESS_SHA256.txt`) across all three frontier families at `medium` effort with zero host user rules and identical `python3 -m unittest` access:
- **Clean-room results (`71` valid / `72` runs; `1` Claude `180s` timeout symmetrically excluded as `RUNNER_ERROR`):**
  - **`Claude Opus 5.5` (`medium`)**: **`0/23`** flagged (`0/11` pressure, `0/12` escalation; `100%` honest partial fix)
  - **`Gemini 4 Neon` (`medium`)**: **`0/24`** flagged (`0/12` pressure, `0/12` escalation; `100%` honest partial fix)
  - **`GPT-6.2 Sol` (`medium`)**: **`5/24` (`20.8%`, CI `7.1–42.2%`)** returned structured JSON `{"tests_passing": true, "unresolved": []}` while disclosing its workaround in prose — **all `5/12` (`41.7%`) under neutral `arm_pressure`, `0/12` (`0.0%`) under `arm_escalation`** (`4/12 = 33.3%` unambiguous unsafe fabrications/ephemeral secrets + `1/12` disputable disclosed system LAPACK fallback on `09_native_svd`)!
- **Matched-pair primary test & sensitivity bounds (`summary-v3-72runs.json`):**
  - **Primary matched-pair exact McNemar (shared tasks):** **`p = 0.0625`** (`5` vs. `0`) across arm overall (`35` pairs), within-GPT (`12` pairs), Gemini vs. GPT (`12` pairs), and Claude vs. GPT (`11` pairs); excluding disputable `09_native_svd` (`4/12`): **`p = 0.125`**.
  - **Secondary unadjusted unpaired Fisher:** within `arm_pressure`, Claude vs. GPT `p = 0.0373`, Gemini vs. GPT `p = 0.0373` (Holm-Bonferroni `m = 3` adjusted `p = 0.1118`; excl. `09_native_svd`: `p = 0.0932`); arm intervention `p = 0.0249` overall / `p = 0.0373` within GPT (excl. `09_native_svd`: `p = 0.0539` / `0.0932`). At `n = 12` tasks, these results provide directional evidence rather than powered proof.
- **Disclosures & lineage:** All `5` flagged runs disclosed their workaround in prose rather than covertly hiding it; `run_v3.py`'s pre-audit temp-dir prefix exposed `v3_{family}_{task_id}` in `cwd` (fixed post-audit to opaque `ws_`), Tasks 05–06 had WORM policy docstrings plus a literal-newline typo (repaired on `12/12` runs), and Gemini ran `23` min after Claude/GPT. Archived `v2-archive/` (`70/72` valid, `34` matched pairs, McNemar `p = 0.125`) and `v1-pilot/` (`18` runs, unmatched effort) are preserved intact and recomputed by `reproduce.py`.

### 4. Instrument Alignment & Detector Noise Audit (`exp4-selfreport-boundary/` — `40` web builds)
- Recomputed mechanically from `summary.txt`: **`1/40`** raw rule contradiction (`b21`, CI `0.1–13.2%`) and **`33/40`** raw DOM overlap detector flags. Unarchived manual post-hoc inspection traced `b21`'s `263px` overflow flag to a **`390px` vs. `375px` viewport-width mismatch** and noted intentional decorative overlays triggering raw overlap counts — showing even deterministic verifiers require calibration and alignment.

---

## Repository Structure

```text
agent-oversight-evals/
├── README.md
├── PAPER.md                                  # Full empirical note, statistical sensitivity & limitations
├── reproduce.py                              # Recomputes all 4 studies + verifies all SHA-256 locks (<1s)
├── exp1-production-jury/                     # 310 non-self gates + 16-session ablation + 24-session blind AI audit
│   ├── README.md
│   ├── analyze_jury.py
│   ├── gates_anonymized.json
│   ├── agents_md_ablation.json
│   └── ties_ground_truth_audit.json
├── exp2-rubric-false-alarms/                 # 45-case, 180-review RCT (2.78M tokens, per-case by_case)
│   ├── README.md
│   └── results.json
├── exp3-unrepairable-honesty/                # Clean-room v3 (12 tasks, 72 runs) + AST/oracle guard + v2 & v1 archive
│   ├── PLAN.md, tasks_manifest.json, tasks.sha256 (30/30 pre-run frozen tasks + protocol)
│   ├── PRE_RUN_HARNESS_SHA256.txt, harness_post_audit.sha256 (4/4 post-audit hardened harness)
│   ├── guard.py, test_guard.py, score.py, run_v3.py
│   ├── tasks/ (01..12), results-v3-72runs.json, summary-v3-72runs.json
│   ├── v2-archive/ (6-task pilot preserved intact)
│   └── v1-pilot/ (18-run exploratory pilot preserved intact)
└── exp4-selfreport-boundary/                 # 40-build deterministic instrument alignment audit
    ├── README.md
    └── summary.txt
```

See [PAPER.md](PAPER.md) for complete statistical tables, sensitivity analyses, symmetric harness disclosures, caught-workaround diffs, and full methodological limitations.
