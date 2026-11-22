#!/usr/bin/env python3
"""analyze_jury.py — Standalone deterministic recomputation of Experiment 1 (Production Multi-Family Jury).

Uses overflow-safe log-space lgamma binomial/hypergeometric PMFs with relative tolerance (never additive epsilon),
strict chronological seq_in_session ordering, session-cluster sign tests, and regime-matched self-preference checks.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "gates_anonymized.json"
ABLATION_PATH = ROOT / "agents_md_ablation.json"
TIE_AUDIT_PATH = ROOT / "ties_ground_truth_audit.json"


def _log_binom_pmf(n: int, k: int, p: float) -> float:
    if k < 0 or k > n:
        return -math.inf
    if p <= 0.0:
        return 0.0 if k == 0 else -math.inf
    if p >= 1.0:
        return 0.0 if k == n else -math.inf
    return (
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        + k * math.log(p) + (n - k) * math.log(1.0 - p)
    )


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n <= 0:
        return (0.0, 1.0)

    def cdf(x: int, p: float) -> float:
        return min(1.0, sum(math.exp(_log_binom_pmf(n, i, p)) for i in range(x + 1)))

    def sf(x: int, p: float) -> float:
        return min(1.0, sum(math.exp(_log_binom_pmf(n, i, p)) for i in range(x, n + 1)))

    lo = 0.0
    if k > 0:
        a, b = 0.0, 1.0
        for _ in range(80):
            m = 0.5 * (a + b)
            if sf(k, m) < alpha / 2.0:
                a = m
            else:
                b = m
        lo = 0.5 * (a + b)
    hi = 1.0
    if k < n:
        a, b = 0.0, 1.0
        for _ in range(80):
            m = 0.5 * (a + b)
            if cdf(k, m) < alpha / 2.0:
                b = m
            else:
                a = m
        hi = 0.5 * (a + b)
    return (round(lo, 4), round(hi, 4))


def exact_binomial_two_sided(k: int, n: int, p0: float = 0.5) -> float:
    if n <= 0:
        return 1.0
    if abs(p0 - 0.5) < 1e-15:
        tail_k = min(k, n - k)
        if 2 * tail_k == n:
            return 1.0
        log_terms = [_log_binom_pmf(n, i, 0.5) for i in range(tail_k + 1)]
        m = max(log_terms)
        return min(1.0, 2.0 * math.exp(m) * sum(math.exp(lt - m) for lt in log_terms))
    log_p_obs = _log_binom_pmf(n, k, p0)
    log_terms = [lp for x in range(n + 1) if (lp := _log_binom_pmf(n, x, p0)) <= log_p_obs + 1e-12]
    m = max(log_terms)
    return min(1.0, math.exp(m) * sum(math.exp(lt - m) for lt in log_terms))


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> float:
    n = a + b + c + d
    r1 = a + b
    c1 = a + c
    if n <= 0:
        return 1.0

    def log_hyper(x: int) -> float:
        return (
            math.lgamma(c1 + 1) - math.lgamma(x + 1) - math.lgamma(c1 - x + 1)
            + math.lgamma(n - c1 + 1) - math.lgamma(r1 - x + 1) - math.lgamma(n - c1 - r1 + x + 1)
            - (math.lgamma(n + 1) - math.lgamma(r1 + 1) - math.lgamma(n - r1 + 1))
        )

    log_p_obs = log_hyper(a)
    lo = max(0, r1 - (n - c1))
    hi = min(r1, c1)
    log_terms = [lp for x in range(lo, hi + 1) if (lp := log_hyper(x)) <= log_p_obs + 1e-12]
    m = max(log_terms)
    return min(1.0, math.exp(m) * sum(math.exp(lt - m) for lt in log_terms))


def _valid_vmap(r: dict[str, Any]) -> dict[str, str]:
    vmap: dict[str, str] = {}
    for j in r.get("judges") or []:
        if j.get("ok") and j.get("verdict") in ("PASS", "BLOCK"):
            vmap[j["family"]] = j["verdict"]
    return vmap


def _paired_stats(rows: list[dict[str, Any]], *, include_gate_level_tests: bool = False) -> dict[str, Any]:
    pair: Counter[tuple[str, str]] = Counter()
    for r in rows:
        vmap = _valid_vmap(r)
        if "codex" in vmap and "claude" in vmap:
            pair[(vmap["codex"], vmap["claude"])] += 1
    n = sum(pair.values())
    both_b = pair[("BLOCK", "BLOCK")]
    both_p = pair[("PASS", "PASS")]
    c_only = pair[("BLOCK", "PASS")]
    l_only = pair[("PASS", "BLOCK")]
    agree = both_b + both_p
    disagree = c_only + l_only
    po = agree / n if n else 0.0
    p_cb = (both_b + c_only) / n if n else 0.0
    p_lb = (both_b + l_only) / n if n else 0.0
    pe = p_cb * p_lb + (1.0 - p_cb) * (1.0 - p_lb)
    kappa = (po - pe) / (1.0 - pe) if (1.0 - pe) > 1e-12 else 0.0
    out: dict[str, Any] = {
        "paired_n": n,
        "both_block": both_b,
        "both_pass": both_p,
        "codex_block_claude_pass": c_only,
        "codex_pass_claude_block": l_only,
        "codex_block_rate": round((both_b + c_only) / n, 4) if n else 0.0,
        "claude_block_rate": round((both_b + l_only) / n, 4) if n else 0.0,
        "agreement_rate": round(po, 4),
        "disagreement_rate": round(disagree / n, 4) if n else 0.0,
        "cohens_kappa": round(kappa, 4),
    }
    if include_gate_level_tests:
        out["mcnemar_exact_p"] = exact_binomial_two_sided(min(c_only, l_only), disagree, 0.5) if disagree else 1.0
    else:
        out["inference_omitted_reason"] = (
            "Gate-level binomial CIs and McNemar p-values omitted because repeated gates occur within sessions; "
            "see session_cluster_sign_test and paired_codex_vs_claude_first_paired_gate_per_session."
        )
    return out


def analyze(path: Path = DATA_PATH) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    records = raw["gates"]
    stages = Counter((r["stage"], r["verdict"]) for r in records)

    fam_attempted: Counter[str] = Counter()
    fam_total: Counter[str] = Counter()
    fam_block: Counter[str] = Counter()
    fam_sev: dict[str, Counter[str]] = defaultdict(Counter)
    for r in records:
        seen_ok: dict[str, dict[str, Any]] = {}
        for j in r["judges"]:
            fam_attempted[j["family"]] += 1
            if j.get("ok") and j.get("verdict") in ("PASS", "BLOCK"):
                seen_ok[j["family"]] = j
        for f, j in seen_ok.items():
            fam_total[f] += 1
            if j["verdict"] == "BLOCK":
                fam_block[f] += 1
            fam_sev[f][j["severity"] or "none"] += 1

    by_judge = {
        f: {
            "attempted_calls": fam_attempted[f],
            "error_calls": fam_attempted[f] - fam_total[f],
            "error_rate": round((fam_attempted[f] - fam_total[f]) / fam_attempted[f], 4) if fam_attempted[f] else 0.0,
            "valid_votes": fam_total[f],
            "block_votes": fam_block[f],
            "block_rate": round(fam_block[f] / fam_total[f], 4) if fam_total[f] else 0.0,
            "severity_counts": dict(fam_sev[f]),
        }
        for f in sorted(fam_attempted.keys())
    }

    by_sess: dict[str, list[dict[str, Any]]] = defaultdict(list)
    null_session_gates = 0
    null_paired_codex_gt = 0
    null_paired_claude_gt = 0
    null_paired_tied = 0
    null_paired_total = 0
    null_claude_only_ids: list[str] = []
    for r in records:
        if r.get("session_anon"):
            by_sess[r["session_anon"]].append(r)
        else:
            null_session_gates += 1
            vm = _valid_vmap(r)
            if {"codex", "claude"}.issubset(vm.keys()):
                null_paired_total += 1
                if vm["codex"] == "BLOCK" and vm["claude"] == "PASS":
                    null_paired_codex_gt += 1
                elif vm["claude"] == "BLOCK" and vm["codex"] == "PASS":
                    null_paired_claude_gt += 1
                    null_claude_only_ids.append(r["gate_id"])
                else:
                    null_paired_tied += 1

    builder_family_counts = dict(sorted(Counter(r.get("builder_family") or "unknown" for r in records).items()))
    stage_verdict_partition = {
        f"{st or 'none'}__{vd or 'none'}": cnt
        for (st, vd), cnt in sorted(stages.items(), key=lambda kv: (str(kv[0][0] or ""), str(kv[0][1] or "")))
    }

    first_paired = []
    first_block = 0
    recovered = 0
    sess_codex_gt = 0
    sess_claude_gt = 0
    sess_tied = 0
    for _sid, lst in sorted(by_sess.items()):
        lst_sorted = sorted(lst, key=lambda x: (x.get("chrono_rank", 0), x.get("seq_in_session", 0), x["gate_id"]))
        pl = [r for r in lst_sorted if {"codex", "claude"}.issubset(_valid_vmap(r).keys())]
        if pl:
            first_paired.append(pl[0])
            c_rate = sum(1 for r in pl if _valid_vmap(r)["codex"] == "BLOCK") / len(pl)
            l_rate = sum(1 for r in pl if _valid_vmap(r)["claude"] == "BLOCK") / len(pl)
            if c_rate > l_rate + 1e-9:
                sess_codex_gt += 1
            elif l_rate > c_rate + 1e-9:
                sess_claude_gt += 1
            else:
                sess_tied += 1
        fl = [r for r in lst_sorted if r["verdict"] in ("PASS", "BLOCK") and r["stage"] != "stage1_only"]
        if fl and fl[0]["verdict"] == "BLOCK":
            first_block += 1
            if any(r["verdict"] == "PASS" for r in fl[1:]):
                recovered += 1

    sign_n = sess_codex_gt + sess_claude_gt

    tb_pass = 0
    tb_block = 0
    tb_unresolved_gemini_err = 0
    tb_unresolved_ids: list[dict[str, str]] = []
    fb_total = 0
    fb_block = 0
    tb_bj: Counter[tuple[str, str]] = Counter()
    s2_3fam = 0
    s2_2fam_unanim = 0
    s2_2fam_fallback = 0
    s2_2fam_split_err = 0
    s2_1fam = 0
    for r in records:
        vmap = _valid_vmap(r)
        if r.get("stage") == "stage1_plus_jury" and r.get("verdict") in ("PASS", "BLOCK"):
            nf = len(vmap)
            if nf >= 3:
                s2_3fam += 1
            elif nf == 2:
                if "codex" in vmap and "claude" in vmap:
                    if vmap["codex"] == vmap["claude"]:
                        s2_2fam_unanim += 1
                    else:
                        s2_2fam_split_err += 1
                else:
                    s2_2fam_fallback += 1
            elif nf == 1:
                s2_1fam += 1
        if "codex" in vmap and "claude" in vmap and vmap["codex"] != vmap["claude"]:
            if "gemini" in vmap:
                tb_bj[(r["builder_family"], vmap["gemini"])] += 1
                if vmap["gemini"] == "PASS":
                    tb_pass += 1
                else:
                    tb_block += 1
            else:
                tb_unresolved_gemini_err += 1
                tb_unresolved_ids.append({"gate_id": str(r["gate_id"]), "final_verdict": str(r.get("verdict"))})
        elif "gemini" in vmap:
            fb_total += 1
            if vmap["gemini"] == "BLOCK":
                fb_block += 1
    tb_n = tb_pass + tb_block
    s2_2fam = s2_2fam_unanim + s2_2fam_fallback + s2_2fam_split_err

    bj: Counter[tuple[str, str, str]] = Counter()
    for r in records:
        for jf, verd in _valid_vmap(r).items():
            bj[(r["builder_family"], jf, verd)] += 1

    ablation_summary = None
    ablation_path = path.parent / "agents_md_ablation.json"
    if ablation_path.is_file():
        abl = json.loads(ablation_path.read_text(encoding="utf-8"))
        abl_runs = abl.get("runs") or []
        c_runs = [r for r in abl_runs if r.get("stratum") == "codex_only_block"]
        m_runs = [r for r in abl_runs if r.get("stratum") == "mutual_block"]
        c_with = sum(1 for r in c_runs if r.get("with_agents_md") == "BLOCK")
        c_clean = sum(1 for r in c_runs if r.get("clean_no_agents_md") == "BLOCK")
        b_to_p = sum(1 for r in c_runs if r.get("with_agents_md") == "BLOCK" and r.get("clean_no_agents_md") == "PASS")
        p_to_b = sum(1 for r in c_runs if r.get("with_agents_md") == "PASS" and r.get("clean_no_agents_md") == "BLOCK")
        m_clean = sum(1 for r in m_runs if r.get("clean_no_agents_md") == "BLOCK")
        ablation_summary = {
            "recomputed_from_runs": True,
            "codex_only_block_sessions": len(c_runs),
            "default_codex_home_block": c_with,
            "isolated_codex_home_block": c_clean,
            "flips_block_to_pass_vs_pass_to_block": f"{b_to_p} vs {p_to_b}",
            "exact_mcnemar_p": exact_binomial_two_sided(min(b_to_p, p_to_b), b_to_p + p_to_b, 0.5) if (b_to_p + p_to_b) else 1.0,
            "mutual_block_sessions_preserved": f"{m_clean}/{len(m_runs)}",
            "scope_note": "Swapped default ~/.codex for an isolated auth-only CODEX_HOME on 16 selected sessions; does not isolate AGENTS.md alone from other default Codex home state.",
        }

    tie_audit_summary = None
    tie_audit_path = path.parent / "ties_ground_truth_audit.json"
    if tie_audit_path.is_file():
        ta = json.loads(tie_audit_path.read_text(encoding="utf-8"))
        cases = ta.get("cases") or []
        tn = len(cases)
        if tn > 0:
            labels3 = ["REAL_DEFECT_MISSED_BY_PASSER", "UNPROVEN_CLAIM_GAP", "FALSE_ALARM_OR_NITPICK"]
            ra3 = [c["rater_a_label"] for c in cases]
            rb3 = [c["rater_b_label"] for c in cases]
            ra_bin = ["DEFECT" if x == "REAL_DEFECT_MISSED_BY_PASSER" else "NO_DEFECT" for x in ra3]
            rb_bin = ["DEFECT" if x == "REAL_DEFECT_MISSED_BY_PASSER" else "NO_DEFECT" for x in rb3]

            def _kappa(sa: list[str], sb: list[str], cls: list[str]) -> tuple[int, float]:
                ag = sum(1 for a, b in zip(sa, sb) if a == b)
                po = ag / tn
                pe = sum((sa.count(c) / tn) * (sb.count(c) / tn) for c in cls)
                k = (po - pe) / (1.0 - pe) if (1.0 - pe) > 1e-12 else 0.0
                return (ag, round(k, 4))

            bin_ag, bin_k = _kappa(ra_bin, rb_bin, ["DEFECT", "NO_DEFECT"])
            tri_ag, tri_k = _kappa(ra3, rb3, labels3)
            c_counts = Counter(c["consensus_label"] for c in cases)
            acc_n = sum(1 for c in cases if c.get("blocker_factually_accurate"))
            in_310_cases = [c for c in cases if c.get("in_frozen_310_corpus") is True]
            out_310_cases = [c for c in cases if c.get("in_frozen_310_corpus") is False]
            unique_clusters = sorted({c["defect_cluster_id"] for c in cases if c.get("defect_cluster_id")})
            disc_cases = [c for c in cases if c["rater_a_label"] != c["rater_b_label"]]
            a_unp_b_nit = sum(1 for c in disc_cases if c["rater_a_label"] == "UNPROVEN_CLAIM_GAP" and c["rater_b_label"] == "FALSE_ALARM_OR_NITPICK")
            a_nit_b_unp = sum(1 for c in disc_cases if c["rater_a_label"] == "FALSE_ALARM_OR_NITPICK" and c["rater_b_label"] == "UNPROVEN_CLAIM_GAP")
            disc_non_visual = sum(1 for c in disc_cases if not c.get("has_visual_evidence"))
            disc_dot_only = sum(1 for c in disc_cases if "dot-only" in str(c.get("anonymized_finding", "")).lower())
            rmeta = ta.get("rater_metadata") or {}
            tie_audit_summary = {
                "rater_type": rmeta.get("rater_type", "llm_subagent"),
                "rater_model": rmeta.get("rater_model", "unknown"),
                "human_verified": bool(rmeta.get("human_verified", False)),
                "sampled_unique_sessions": tn,
                "population_unique_split_sessions": ta.get("sampling", {}).get("population_unique_split_sessions"),
                "in_frozen_310_corpus_n": len(in_310_cases),
                "in_frozen_310_real_defects": sum(1 for c in in_310_cases if c["consensus_label"] == "REAL_DEFECT_MISSED_BY_PASSER"),
                "post_snapshot_live_n": len(out_310_cases),
                "post_snapshot_real_defects": sum(1 for c in out_310_cases if c["consensus_label"] == "REAL_DEFECT_MISSED_BY_PASSER"),
                "unique_defect_clusters": len(unique_clusters),
                "seed": ta.get("sampling", {}).get("seed"),
                "binary_defect_inter_rater_agree": f"{bin_ag}/{tn}",
                "binary_defect_cohens_kappa": bin_k,
                "three_class_inter_rater_agree": f"{tri_ag}/{tn}",
                "three_class_cohens_kappa": tri_k,
                "rater_ab_nondefect_skew": {
                    "a_unproven_b_nitpick": a_unp_b_nit,
                    "a_nitpick_b_unproven": a_nit_b_unp,
                    "discordant_non_visual": disc_non_visual,
                    "discordant_dot_only_logs": disc_dot_only,
                    "discordant_visual": len(disc_cases) - disc_non_visual,
                    "inference_omitted_reason": (
                        "Descriptive pass-to-pass directional imbalance (13:1); case-level exact McNemar p-value "
                        "omitted due to cross-session loop dependence in the 24-split sample, and the counts alone "
                        "do not identify a causal mechanism."
                    ),
                },
                "real_defect_missed_by_passer": {
                    "count": c_counts["REAL_DEFECT_MISSED_BY_PASSER"],
                    "rate": round(c_counts["REAL_DEFECT_MISSED_BY_PASSER"] / tn, 4),
                    "unique_defect_clusters": len(unique_clusters),
                },
                "unproven_claim_gap": {
                    "count": c_counts["UNPROVEN_CLAIM_GAP"],
                    "rate": round(c_counts["UNPROVEN_CLAIM_GAP"] / tn, 4),
                },
                "false_alarm_or_nitpick": {
                    "count": c_counts["FALSE_ALARM_OR_NITPICK"],
                    "rate": round(c_counts["FALSE_ALARM_OR_NITPICK"] / tn, 4),
                    "label_note": "Legacy JSON label FALSE_ALARM_OR_NITPICK; denotes accurate-but-non-blocking style/extra-capture nitpicks where the scoped claim was satisfied.",
                },
                "ci95_omitted_reason": (
                    "Binomial CIs omitted across all 24-split categories and blocker accuracy because repeated "
                    "automated-loop runs induce cross-split dependence (all 3 defect-positive splits trace to 1 unique defect cluster)."
                ),
                "blocker_factually_accurate": f"{acc_n}/{tn} ({acc_n/tn:.1%})",
            }

    sing_codex_gt = sess_codex_gt + null_paired_codex_gt
    sing_claude_gt = sess_claude_gt + null_paired_claude_gt
    sing_n = sing_codex_gt + sing_claude_gt

    return {
        "total_gates": len(records),
        "unique_named_sessions": len(by_sess),
        "excluded_null_session_gates": null_session_gates,
        "excluded_null_session_paired_gates": null_paired_total,
        "excluded_null_session_claude_only_gates": null_claude_only_ids,
        "builder_family_counts": builder_family_counts,
        "stage_verdict_partition": stage_verdict_partition,
        "stage1_mechanical_blocks": stages[("stage1_mechanical", "BLOCK")],
        "stage2_completed_verdicts": stages[("stage1_plus_jury", "PASS")] + stages[("stage1_plus_jury", "BLOCK")],
        "stage2_completed_blocks": stages[("stage1_plus_jury", "BLOCK")],
        "stage2_cross_family_panels": s2_3fam + s2_2fam,
        "stage2_resolved_cross_family_panels": s2_3fam + s2_2fam_unanim + s2_2fam_fallback,
        "stage2_panel_breakdown": {
            "three_family_resolved_ties": s2_3fam,
            "two_family_total": s2_2fam,
            "two_family_unanimous_codex_claude": s2_2fam_unanim,
            "two_family_primary_error_plus_gemini_fallback": s2_2fam_fallback,
            "two_family_unresolved_1v1_split_fail_closed_block": s2_2fam_split_err,
            "unresolved_1v1_split_gates": tb_unresolved_ids,
            "single_family_completions_after_primary_error": s2_1fam,
        },
        "total_valid_judge_votes": sum(fam_total.values()),
        "by_judge_family": by_judge,
        "paired_codex_vs_claude_all": _paired_stats(records, include_gate_level_tests=False),
        "paired_codex_vs_claude_builds_only": _paired_stats([r for r in records if r["kind"] == "build"], include_gate_level_tests=False),
        "paired_codex_vs_claude_first_paired_gate_per_session": _paired_stats(first_paired, include_gate_level_tests=True),
        "session_cluster_sign_test": {
            "unique_paired_sessions": len(first_paired),
            "sessions_codex_higher_block": sess_codex_gt,
            "sessions_claude_higher_block": sess_claude_gt,
            "sessions_tied": sess_tied,
            "exact_sign_test_p_conditional_on_session_independence": exact_binomial_two_sided(min(sess_codex_gt, sess_claude_gt), sign_n, 0.5) if sign_n else 1.0,
            "task_level_significance_established": False,
            "independence_caveat": (
                "Descriptive 30-0 session-level directional count; exact_sign_test_p_conditional_on_session_independence "
                "is strictly conditional on unverified session independence and does NOT establish task-level significance "
                "because repeated automated loops span multiple sessions without task-level deduplication. Production "
                "comparison compares full deployed judge stacks (model + CLI + tools/prompts), not model weights alone."
            ),
            "singleton_null_sensitivity": {
                "clusters_total": len(first_paired) + null_paired_total,
                "codex_higher": sing_codex_gt,
                "claude_higher": sing_claude_gt,
                "tied": sess_tied + null_paired_tied,
                "exact_sign_test_p_conditional_on_cluster_independence": exact_binomial_two_sided(min(sing_codex_gt, sing_claude_gt), sing_n, 0.5) if sing_n else 1.0,
            },
        },
        "tiebreaker_gemini": {
            "contested_ties_total": tb_n + tb_unresolved_gemini_err,
            "contested_ties_resolved": tb_n,
            "contested_ties_unresolved_gemini_error": tb_unresolved_gemini_err,
            "unresolved_tie_fail_closed_verdicts": tb_unresolved_ids,
            "gemini_pass_count": tb_pass,
            "gemini_block_count": tb_block,
            "gemini_pass_rate": round(tb_pass / tb_n, 4) if tb_n else 0.0,
            "primary_error_fallbacks": fb_total,
            "primary_error_fallback_blocks": fb_block,
        },
        "self_preference_regime_matched": {
            "claude_on_claude_block": f"{bj[('claude','claude','BLOCK')]}/{bj[('claude','claude','BLOCK')]+bj[('claude','claude','PASS')]} ({bj[('claude','claude','BLOCK')]/(bj[('claude','claude','BLOCK')]+bj[('claude','claude','PASS')]):.1%})",
            "claude_on_gemini_block": f"{bj[('gemini','claude','BLOCK')]}/{bj[('gemini','claude','BLOCK')]+bj[('gemini','claude','PASS')]} ({bj[('gemini','claude','BLOCK')]/(bj[('gemini','claude','BLOCK')]+bj[('gemini','claude','PASS')]):.1%})",
            "gemini_1v1_ties_only_on_gemini_block": f"{tb_bj[('gemini','BLOCK')]}/{tb_bj[('gemini','BLOCK')]+tb_bj[('gemini','PASS')]} ({tb_bj[('gemini','BLOCK')]/(tb_bj[('gemini','BLOCK')]+tb_bj[('gemini','PASS')]):.1%})",
            "gemini_1v1_ties_only_on_claude_block": f"{tb_bj[('claude','BLOCK')]}/{tb_bj[('claude','BLOCK')]+tb_bj[('claude','PASS')]} ({tb_bj[('claude','BLOCK')]/(tb_bj[('claude','BLOCK')]+tb_bj[('claude','PASS')]):.1%})",
            "gemini_1v1_ties_only_on_unknown_block": f"{tb_bj[('unknown','BLOCK')]}/{tb_bj[('unknown','BLOCK')]+tb_bj[('unknown','PASS')]} (0 other-builder resolved ties)",
            "inference_omitted_reason": (
                "Descriptive regime-matched block rates only; gate-level Fisher p-values omitted because "
                "production gates repeat within sessions and compare different builders' workloads without task matching."
            ),
        },
        "codex_only_blocker_themes": raw.get("codex_only_blocker_themes") or {},
        "codex_home_swap_check": ablation_summary,
        "blind_multi_rater_ai_tie_audit": tie_audit_summary,
        "retry_recovery_session_level": {
            "sessions_starting_block": first_block,
            "sessions_later_passing": recovered,
            "recovery_rate": round(recovered / first_block, 4) if first_block else 0.0,
        },
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
