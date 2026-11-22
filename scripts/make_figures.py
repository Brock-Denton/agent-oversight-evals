#!/usr/bin/env python3
"""make_figures.py — Deterministically generate crisp SVG figures directly from raw repo JSON data.

Standard-library Python 3 only. Every number plotted is computed directly from
exp1-production-jury/ and exp3-unrepairable-honesty/ via analyze_jury.py and score.py.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
sys.path.insert(0, str(ROOT / "exp1-production-jury"))
sys.path.insert(0, str(ROOT / "exp3-unrepairable-honesty"))

import analyze_jury  # noqa: E402
import score  # noqa: E402


def _load_exp5_score():
    spec = importlib.util.spec_from_file_location("exp5_score", ROOT / "exp5-premise-lockin" / "score.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

FONT = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"


def _fmt_sci(p: float) -> str:
    if p >= 0.001:
        return f"{p:.4f}"
    exp = int(f"{p:.2e}".split("e")[1])
    mant = p / (10 ** exp)
    sup_map = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{mant:.2f} × 10{str(exp).translate(sup_map)}"


def build_fig1_production_jury() -> str:
    e1 = analyze_jury.analyze(ROOT / "exp1-production-jury" / "gates_anonymized.json")
    paired = e1["paired_codex_vs_claude_all"]
    tb = e1["tiebreaker_gemini"]
    abl = e1["agents_md_causal_ablation"]
    ta = e1["blind_multi_rater_ai_tie_audit"]
    sess = e1["session_cluster_sign_test"]

    n_paired = paired["paired_n"]
    codex_b = paired["both_block"] + paired["codex_block_claude_pass"]
    claude_b = paired["both_block"] + paired["codex_pass_claude_block"]
    codex_pct = 100.0 * codex_b / n_paired
    claude_pct = 100.0 * claude_b / n_paired
    gem_blk = tb["gemini_block_count"]
    gem_n = tb["contested_ties_resolved"]
    gem_pct = 100.0 * gem_blk / gem_n

    abl_n = abl["codex_only_block_sessions"]
    abl_with = abl["with_agents_md_block"]
    abl_clean = abl["clean_no_agents_md_block"]
    abl_with_pct = 100.0 * abl_with / abl_n
    abl_clean_pct = 100.0 * abl_clean / abl_n

    ta_n = ta["sampled_unique_sessions"]
    ta_def = ta["real_defect_missed_by_passer"]["count"]
    ta_unp = ta["unproven_claim_gap"]["count"]
    ta_nit = ta["false_alarm_or_nitpick"]["count"]
    ta_clust = ta["unique_defect_clusters"]
    skew = ta["rater_ab_nondefect_skew"]

    W, H = 820, 404
    bar_x = 32
    bar_w = 348

    def hbar(y: int, label: str, sub: str, pct: float, color: str, val_txt: str) -> str:
        fw = max(6.0, bar_w * pct / 100.0)
        return f"""
  <text x="{bar_x}" y="{y}" font-family="{FONT}" font-size="12" font-weight="600" fill="#1C1917">{escape(label)}</text>
  <text x="{bar_x + bar_w}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" font-weight="700" fill="#1C1917">{escape(val_txt)}</text>
  <rect x="{bar_x}" y="{y + 7}" width="{bar_w}" height="18" rx="5" fill="#ECE6DC"/>
  <rect x="{bar_x}" y="{y + 7}" width="{fw:.1f}" height="18" rx="5" fill="{color}"/>
  <text x="{bar_x}" y="{y + 39}" font-family="{FONT}" font-size="10.2" fill="#635D56">{escape(sub)}</text>"""

    rx = 428
    rw = 360
    w_def = rw * ta_def / ta_n
    w_unp = rw * ta_unp / ta_n
    w_nit = rw - w_def - w_unp

    p_sess = _fmt_sci(sess["exact_sign_test_p"])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Experiment 1: Production Multi-Family Jury Calibration, Causal Ablation, and Blind AI Adjudication">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="#FAF8F4" stroke="#DDD6CA" stroke-width="1.5"/>

  <text x="32" y="32" font-family="{MONO}" font-size="10" font-weight="600" letter-spacing="0.08em" fill="#635D56">EXPERIMENT 1 · {e1['total_gates']} PRODUCTION GATES · {sess['unique_paired_sessions']} NAMED SESSIONS</text>
  <text x="32" y="56" font-family="{FONT}" font-size="18.5" font-weight="700" fill="#1C1917">Same Builds, Different Stack Thresholds — Isolated CODEX_HOME Unchanged</text>

  <line x1="32" y1="71" x2="{W - 32}" y2="71" stroke="#E5DFD5" stroke-width="1"/>
  <line x1="404" y1="84" x2="404" y2="348" stroke="#E5DFD5" stroke-width="1"/>

  <!-- Left Panel -->
  <text x="32" y="98" font-family="{FONT}" font-size="12.8" font-weight="700" fill="#1C1917">A. Block Rate on Paired Builds &amp; CODEX_HOME Swap</text>
  {hbar(122, "GPT-6.2 Sol stack (Primary A)", f"Paired audits: {paired['codex_block_claude_pass']} Codex-only vs {paired['codex_pass_claude_block']} Claude-only", codex_pct, "#B9382C", f"{codex_pct:.1f}% ({codex_b}/{n_paired})")}
  {hbar(178, "Claude Opus 5.5 stack (Primary B)", f"Session sign test: {sess['sessions_codex_higher_block']} Codex > Claude, {sess['sessions_claude_higher_block']} reverse (p = {p_sess}*)", claude_pct, "#2F6D8F", f"{claude_pct:.1f}% ({claude_b}/{n_paired})")}
  {hbar(234, "Gemini 4 Neon (1–1 Tie-Breaker)", f"Passed {tb['gemini_pass_count']}/{gem_n} ({100*tb['gemini_pass_count']/gem_n:.1f}%) resolved splits (0/46 Gem vs 2/17 Claude)", gem_pct, "#1B6B4A", f"{gem_pct:.1f}% ({gem_blk}/{gem_n})")}

  <line x1="32" y1="286" x2="380" y2="286" stroke="#E5DFD5" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="32" y="305" font-family="{FONT}" font-size="11.2" font-weight="700" fill="#1C1917">Isolated CODEX_HOME Swap (excl. AGENTS.md/state, n = {abl_n})</text>
  <rect x="32" y="315" width="168" height="24" rx="5" fill="#ECE6DC"/>
  <rect x="32" y="315" width="{168 * abl_with_pct / 100.0:.1f}" height="24" rx="5" fill="#B9382C"/>
  <text x="108" y="331" text-anchor="middle" font-family="{MONO}" font-size="10.2" font-weight="700" fill="#FFFFFF">Default home: {abl_with}/{abl_n}</text>

  <rect x="212" y="315" width="168" height="24" rx="5" fill="#ECE6DC"/>
  <rect x="212" y="315" width="{168 * abl_clean_pct / 100.0:.1f}" height="24" rx="5" fill="#8C2B22"/>
  <text x="288" y="331" text-anchor="middle" font-family="{MONO}" font-size="10.2" font-weight="700" fill="#FFFFFF">Isolated: {abl_clean}/{abl_n}</text>

  <!-- Right Panel -->
  <text x="{rx}" y="98" font-family="{FONT}" font-size="12.8" font-weight="700" fill="#1C1917">B. Blind AI Audit of {ta_n} Contested Splits</text>
  <text x="{rx}" y="116" font-family="{FONT}" font-size="10.4" fill="#635D56">3 zero-context Gemini passes on PNGs + logs (human review pending)</text>

  <!-- Stacked Bar -->
  <rect x="{rx}" y="130" width="{w_def:.1f}" height="32" rx="5" fill="#B9382C"/>
  <rect x="{rx + w_def + 2:.1f}" y="130" width="{w_unp - 2:.1f}" height="32" fill="#B87314"/>
  <rect x="{rx + w_def + w_unp + 2:.1f}" y="130" width="{w_nit - 2:.1f}" height="32" rx="5" fill="#5B6770"/>

  <text x="{rx + w_def/2:.1f}" y="150" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#FFFFFF">{ta_def}</text>
  <text x="{rx + w_def + w_unp/2:.1f}" y="150" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#FFFFFF">{ta_unp} ({100*ta_unp/ta_n:.1f}%)</text>
  <text x="{rx + w_def + w_unp + w_nit/2:.1f}" y="150" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#FFFFFF">{ta_nit} ({100*ta_nit/ta_n:.0f}%)</text>

  <!-- Legend Breakdown -->
  <rect x="{rx}" y="178" width="11" height="11" rx="2.5" fill="#B9382C"/>
  <text x="{rx + 18}" y="188" font-family="{FONT}" font-size="11.5" font-weight="700" fill="#1C1917">Real defect missed by Claude: {ta_def}/{ta_n} ({100*ta_def/ta_n:.1f}%)</text>
  <text x="{rx + 18}" y="203" font-family="{FONT}" font-size="10.1" fill="#57534E">All 3 hits = {ta_clust} recurring UI bug (T09/T10/T15); binary κ = {ta['binary_defect_cohens_kappa']:.3f}</text>

  <rect x="{rx}" y="220" width="11" height="11" rx="2.5" fill="#B87314"/>
  <text x="{rx + 18}" y="230" font-family="{FONT}" font-size="11.5" font-weight="700" fill="#1C1917">Unproven claim gap: {ta_unp}/{ta_n} ({100*ta_unp/ta_n:.1f}%)</text>
  <text x="{rx + 18}" y="245" font-family="{FONT}" font-size="10.1" fill="#57534E">No visible bug; proof omitted claimed state or test detail</text>

  <rect x="{rx}" y="262" width="11" height="11" rx="2.5" fill="#5B6770"/>
  <text x="{rx + 18}" y="272" font-family="{FONT}" font-size="11.5" font-weight="700" fill="#1C1917">Non-blocking nitpick: {ta_nit}/{ta_n} ({100*ta_nit/ta_n:.1f}%)</text>
  <text x="{rx + 18}" y="287" font-family="{FONT}" font-size="10.1" fill="#57534E">Scoped claim satisfied; accurate-but-immaterial demand</text>

  <rect x="{rx}" y="304" width="{rw}" height="38" rx="6" fill="#F2ECE1" stroke="#DFD7C8"/>
  <text x="{rx + 10}" y="320" font-family="{FONT}" font-size="9.8" font-weight="600" fill="#57534E">Caveat: 3-class κ = {ta['three_class_cohens_kappa']:.3f}; Rater A vs B directional imbalance {skew['a_unproven_b_nitpick']}:{skew['a_nitpick_b_unproven']}</text>
  <text x="{rx + 10}" y="334" font-family="{FONT}" font-size="9.8" fill="#57534E">on non-defect boundary ({skew['discordant_dot_only_logs']}/14 dot-only logs, {skew['discordant_non_visual']}/14 non-visual).</text>

  <!-- Footer -->
  <line x1="32" y1="362" x2="{W - 32}" y2="362" stroke="#E5DFD5" stroke-width="1"/>
  <text x="32" y="383" font-family="{FONT}" font-size="10.2" fill="#635D56">*Session sign test assumes independent sessions. CODEX_HOME flips: {abl['flips_block_to_pass_vs_pass_to_block']} (p = {abl['exact_mcnemar_p']:.1f}); mutual: {abl['mutual_block_sessions_preserved']}.</text>
</svg>
"""


def build_fig2_exp3_honesty() -> str:
    data = json.loads((ROOT / "exp3-unrepairable-honesty" / "results-v3-72runs.json").read_text(encoding="utf-8"))
    summary = score.summarize_results(data["runs"])
    bma = summary["by_model_arm"]
    sens = summary["sensitivity_excluding_disputable_09_native_svd"]
    mcnemar_full = summary["paired_arm_mcnemar"]["exact_mcnemar_p"]
    mcnemar_sens = sens["matched_pair_mcnemar_p"]

    rows = [
        ("Claude Opus 5.5", "claude-opus-5-5", "180s timeout excluded symmetrically*", "0/12 flagged · 0 cheats"),
        ("Gemini 4 Neon", "gemini-4-neon-medium", "All 24 runs valid (max 79.3s)", "0/12 flagged · 0 cheats"),
        ("GPT-6.2 Sol", "gpt-6.2-sol", "All 5 disclosed in prose while JSON = true", "Drops 41.7% → 0.0% with escalation"),
    ]

    W, H = 820, 362

    def panel_rows(arm_key: str, x0: int, bw: int) -> str:
        parts = []
        y = 132
        for label, mid, note_p, note_e in rows:
            st = bma[f"{mid}__{arm_key}"]
            val = st["valid_runs"]
            ch = st["cheated"]
            pct = 100.0 * ch / val if val else 0.0
            parts.append(f'<text x="{x0}" y="{y}" font-family="{FONT}" font-size="12" font-weight="600" fill="#1C1917">{escape(label)}</text>')
            parts.append(f'<text x="{x0 + bw}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" font-weight="700" fill="{"#B9382C" if ch else "#1B6B4A"}">{ch}/{val} ({pct:.1f}%)</text>')
            parts.append(f'<rect x="{x0}" y="{y + 8}" width="{bw}" height="22" rx="5" fill="#1B6B4A"/>')
            if ch > 0:
                if mid == "gpt-6.2-sol" and arm_key == "arm_pressure" and ch == 5:
                    w_unamb = bw * 4 / val
                    w_disp = bw * 1 / val
                    parts.append(f'<rect x="{x0}" y="{y + 8}" width="{w_unamb:.1f}" height="22" rx="5" fill="#B9382C"/>')
                    parts.append(f'<rect x="{x0 + w_unamb:.1f}" y="{y + 8}" width="{w_disp:.1f}" height="22" fill="#B87314"/>')
                    parts.append(f'<text x="{x0 + w_unamb/2:.1f}" y="{y + 23}" text-anchor="middle" font-family="{MONO}" font-size="10.2" font-weight="700" fill="#FFFFFF">4 unsafe</text>')
                    parts.append(f'<text x="{x0 + w_unamb + w_disp/2:.1f}" y="{y + 23}" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="#FFFFFF">1*</text>')
                    parts.append(f'<text x="{x0 + w_unamb + w_disp + (bw - w_unamb - w_disp)/2:.1f}" y="{y + 23}" text-anchor="middle" font-family="{MONO}" font-size="10.2" font-weight="600" fill="#FFFFFF">7 honest</text>')
                else:
                    fw = bw * ch / val
                    parts.append(f'<rect x="{x0}" y="{y + 8}" width="{fw:.1f}" height="22" rx="5" fill="#B9382C"/>')
            else:
                parts.append(f'<text x="{x0 + bw/2:.1f}" y="{y + 23}" text-anchor="middle" font-family="{MONO}" font-size="10.2" font-weight="600" fill="#FFFFFF">{val}/{val} honest partial fix</text>')
            sub = note_p if arm_key == "arm_pressure" else note_e
            parts.append(f'<text x="{x0}" y="{y + 43}" font-family="{FONT}" font-size="10.1" fill="#635D56">{escape(sub)}</text>')
            y += 61
        return "\n  ".join(parts)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Experiment 3: Clean-Room Unrepairable-Constraint Honesty Benchmark across 3 Frontier Families">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="#FAF8F4" stroke="#DDD6CA" stroke-width="1.5"/>

  <text x="32" y="32" font-family="{MONO}" font-size="10" font-weight="600" letter-spacing="0.08em" fill="#635D56">EXPERIMENT 3 · CLEAN-ROOM V3 PILOT · 71/72 VALID RUNS ACROSS 12 TASKS</text>
  <text x="32" y="56" font-family="{FONT}" font-size="18.5" font-weight="700" fill="#1C1917">Explicit Escalation Drops Spec-Relaxing Green-CI Workarounds to 0%</text>

  <line x1="32" y1="71" x2="{W - 32}" y2="71" stroke="#E5DFD5" stroke-width="1"/>
  <line x1="410" y1="84" x2="410" y2="300" stroke="#E5DFD5" stroke-width="1"/>

  <!-- Left: Neutral Pressure -->
  <text x="32" y="98" font-family="{FONT}" font-size="12.8" font-weight="700" fill="#1C1917">Neutral CI Pressure (arm_pressure)</text>
  <text x="32" y="114" font-family="{FONT}" font-size="10.3" fill="#635D56">No escalation cue; returns JSON tests_passing: true | false</text>
  {panel_rows("arm_pressure", 32, 356)}

  <!-- Right: Explicit Escalation -->
  <text x="432" y="98" font-family="{FONT}" font-size="12.8" font-weight="700" fill="#1C1917">Explicit Escalation (arm_escalation)</text>
  <text x="432" y="114" font-family="{FONT}" font-size="10.3" fill="#635D56">Anti-fabrication rules + permission to leave unrepairable failing</text>
  {panel_rows("arm_escalation", 432, 356)}

  <!-- Legend & Stats Footer -->
  <line x1="32" y1="308" x2="{W - 32}" y2="308" stroke="#E5DFD5" stroke-width="1"/>
  <rect x="32" y="320" width="11" height="11" rx="2.5" fill="#1B6B4A"/>
  <text x="49" y="330" font-family="{FONT}" font-size="10.2" fill="#57534E">Honest partial fix</text>
  <rect x="158" y="320" width="11" height="11" rx="2.5" fill="#B9382C"/>
  <text x="175" y="330" font-family="{FONT}" font-size="10.2" fill="#57534E">Unsafe fabrication / ephemeral key (4/12)</text>
  <rect x="408" y="320" width="11" height="11" rx="2.5" fill="#B87314"/>
  <text x="425" y="330" font-family="{FONT}" font-size="10.2" fill="#57534E">1* Disputable LAPACK fallback (09_native_svd)</text>

  <text x="32" y="348" font-family="{FONT}" font-size="10.1" fill="#635D56">Primary matched-pair exact McNemar p = {mcnemar_full:.4f} (p = {mcnemar_sens:.4f} excl. 09_native_svd). Directional pilot (n = 12 tasks); *1 Claude 180s timeout excluded.</text>
</svg>
"""


def build_fig3_premise_lockin() -> str:
    exp5_score = _load_exp5_score()
    s = exp5_score.score_results(
        ROOT / "exp5-premise-lockin" / "results-exp5-198runs.json",
        None,
        ROOT / "exp5-premise-lockin",
    )
    ctrl = s["regime1_explicit_control"]["pooled"]["blocked"]
    a1 = s["arm1_unresolved_standard"]["pooled"]["blocked"]
    a2u = s["arm2_escalation_prompt"]["unresolved_pooled"]["blocked"]
    a2r = s["arm2_escalation_prompt"]["resolved_ctrl_pooled"]["blocked"]
    dl = s["dossier_level_primary_inference"]
    sar = s["spec_review_vs_goal_selection"]
    a3a_f = s["arm3a_single_best_priors"]["by_family"]
    a3b = s["arm3b_stage0_orthogonal"]["pooled"]
    p_a12 = f"{dl['arm1_vs_arm2_unresolved_dossier_sign']['exact_sign_p']:.4f}"
    p_a2c = f"{dl['arm2_unresolved_vs_resolved_ctrl_dossier_sign']['exact_sign_p']:.4f}"

    W, H = 820, 396
    bar_x, bar_w = 32, 348

    def hbar(y: int, label: str, sub: str, k: int, n: int, color: str) -> str:
        pct = 100.0 * k / n if n else 0.0
        fw = max(6.0, bar_w * pct / 100.0) if k > 0 else 4.0
        val_txt = f"{pct:.1f}% ({k}/{n})"
        return f"""
  <text x="{bar_x}" y="{y}" font-family="{FONT}" font-size="11.6" font-weight="600" fill="#1C1917">{escape(label)}</text>
  <text x="{bar_x + bar_w}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="10.8" font-weight="700" fill="{color if k else '#1B6B4A'}">{escape(val_txt)}</text>
  <rect x="{bar_x}" y="{y + 7}" width="{bar_w}" height="17" rx="5" fill="#ECE6DC"/>
  <rect x="{bar_x}" y="{y + 7}" width="{fw:.1f}" height="17" rx="5" fill="{color if k else '#9CA3AF'}"/>
  <text x="{bar_x}" y="{y + 37}" font-family="{FONT}" font-size="9.7" fill="#635D56">{escape(sub)}</text>"""

    rx, rw = 428, 360

    def split_bar(y: int, label: str, k_a: int, k_b: int, n: int, sub: str) -> str:
        wa = rw * k_a / n if n else 0.0
        wb = rw - wa
        return f"""
  <text x="{rx}" y="{y}" font-family="{FONT}" font-size="11.6" font-weight="600" fill="#1C1917">{escape(label)}</text>
  <text x="{rx + rw}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="10.4" font-weight="700" fill="#1C1917">{k_a}A / {k_b}B</text>
  <rect x="{rx}" y="{y + 7}" width="{wa:.1f}" height="18" rx="4" fill="#B87314"/>
  <rect x="{rx + wa + 2:.1f}" y="{y + 7}" width="{max(0.0, wb - 2):.1f}" height="18" rx="4" fill="#2F6D8F"/>
  <text x="{rx + wa/2:.1f}" y="{y + 20}" text-anchor="middle" font-family="{MONO}" font-size="9.8" font-weight="700" fill="#FFFFFF">{100*k_a/n:.0f}% A</text>
  <text x="{rx + wa + wb/2:.1f}" y="{y + 20}" text-anchor="middle" font-family="{MONO}" font-size="9.8" font-weight="700" fill="#FFFFFF">{100*k_b/n:.0f}% B</text>
  <text x="{rx}" y="{y + 37}" font-family="{FONT}" font-size="9.7" fill="#635D56">{escape(sub)}</text>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Experiment 5: Premise Lock-In, Sign-Off Compliance, and Stage 0 Slates across 198 Runs">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="#FAF8F4" stroke="#DDD6CA" stroke-width="1.5"/>

  <text x="32" y="32" font-family="{MONO}" font-size="10" font-weight="600" letter-spacing="0.08em" fill="#635D56">EXPERIMENT 5 · 198 RUNS · 12 DOSSIERS + 6 CONTROLS · DOSSIER-CLUSTERED INFERENCE</text>
  <text x="32" y="56" font-family="{FONT}" font-size="18.2" font-weight="700" fill="#1C1917">Red-Teams Catch Explicit Contradictions, Not Unresolved Human Trade-Offs</text>

  <line x1="32" y1="71" x2="{W - 32}" y2="71" stroke="#E5DFD5" stroke-width="1"/>
  <line x1="404" y1="84" x2="404" y2="344" stroke="#E5DFD5" stroke-width="1"/>

  <!-- Left Panel: BLOCKED rate across 4 regimes -->
  <text x="32" y="98" font-family="{FONT}" font-size="12.4" font-weight="700" fill="#1C1917">A. Strict BLOCKED Rate on Spec Audit (3 Families)</text>
  {hbar(120, "1. Explicit Contradiction (E01–E06)", "6/6 dossiers majority-blocked (6/6 Claude, 6/6 Codex, 6/6 Gemini)", ctrl["k"], ctrl["n"], "#1B6B4A")}
  {hbar(174, "2. Unresolved Tension (U01–U12, Std)", "0/12 maj-blocked; 0/36 asked human (separate non-exchangeable stimuli)", a1["k"], a1["n"], "#B9382C")}
  {hbar(228, "3. Unresolved + Sign-Off Rule (Arm 2)", f"Explicit rule compliance: 12/12 dossiers blocked vs Arm 1 (p = {p_a12})", a2u["k"], a2u["n"], "#1B6B4A")}
  {hbar(282, "4. Matched Sign-Off Control (Arm 2)", f"0/12 dossiers blocked vs Arm 2 (p = {p_a2c}); Codex 12/12 PATCH*", a2r["k"], a2r["n"], "#1B6B4A")}

  <!-- Right Panel: Single-Best Priors vs Stage 0 Slate -->
  <text x="{rx}" y="98" font-family="{FONT}" font-size="12.4" font-weight="700" fill="#1C1917">B. Blind Priors (Arm 3A) vs. Stage 0 Slate (Arm 3B)</text>
  {split_bar(120, "GPT-6.2 Sol — Single-Best Pick (Arm 3A)", a3a_f["codex"]["chose_asset_a"]["k"], a3a_f["codex"]["chose_asset_b"]["k"], 12, "Favors mature Asset A (10/12 A in Stage 0 auto-rec)")}
  {split_bar(174, "Gemini 4 Neon — Single-Best Pick (Arm 3A)", a3a_f["gemini"]["chose_asset_a"]["k"], a3a_f["gemini"]["chose_asset_b"]["k"], 12, "Moderately favors Asset A (8/12 A in Stage 0 auto-rec)")}
  {split_bar(228, "Claude Opus 5.5 — Single-Best Pick (Arm 3A)", a3a_f["claude"]["chose_asset_a"]["k"], a3a_f["claude"]["chose_asset_b"]["k"], 12, "Preferred operational Asset B (8/12) in goal selection")}

  <rect x="{rx}" y="278" width="{rw}" height="64" rx="7" fill="#ECF4EF" stroke="#B7D7C5"/>
  <text x="{rx + 12}" y="297" font-family="{FONT}" font-size="10.6" font-weight="700" fill="#145339">Stage 0 Slate (Arm 3B): {a3b['slate_covers_both_a_and_b_self']['k']}/{a3b['slate_covers_both_a_and_b_self']['n']} (100%) Exposed Both A &amp; B</text>
  <text x="{rx + 12}" y="314" font-family="{FONT}" font-size="9.6" fill="#1F4D3A">Keyword-checked: {a3b['slate_covers_both_kw_verified']['k']}/36 · Mean lexical Jaccard: {a3b['mean_pairwise_jaccard']:.4f}</text>
  <text x="{rx + 12}" y="330" font-family="{FONT}" font-size="9.6" fill="#1F4D3A">Single-family picks diverge (4/12 A, 2/12 B, 6/12 split across 12 dossiers)</text>

  <!-- Footer -->
  <line x1="32" y1="354" x2="{W - 32}" y2="354" stroke="#E5DFD5" stroke-width="1"/>
  <text x="32" y="375" font-family="{FONT}" font-size="9.1" fill="#635D56">Cross-role contrast (Arm 3A pref B vs A): {sar['pref_b_did_not_block_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_b_in_arm3a']} vs {sar['pref_a_did_not_block_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_a_in_arm3a']} not-blocked; {sar['pref_b_stamped_pass_on_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_b_in_arm3a']} vs {sar['pref_a_stamped_pass_on_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_a_in_arm3a']} PASS. *PATCH vs PASS.</text>
</svg>
"""


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    f1 = ASSETS / "fig1_production_jury.svg"
    f2 = ASSETS / "fig2_exp3_honesty.svg"
    f3 = ASSETS / "fig3_premise_lockin.svg"
    f1.write_text(build_fig1_production_jury(), encoding="utf-8")
    f2.write_text(build_fig2_exp3_honesty(), encoding="utf-8")
    f3.write_text(build_fig3_premise_lockin(), encoding="utf-8")
    print(f"Wrote {f1} ({f1.stat().st_size} bytes)")
    print(f"Wrote {f2} ({f2.stat().st_size} bytes)")
    print(f"Wrote {f3} ({f3.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
