#!/usr/bin/env python3
"""score.py — Zero-dependency deterministic scorer & exact statistical engine for Exp 5 (198 runs).

100% mechanical JSON-verdict scoring (zero subjective regex escalation heuristics):
  1. Goal-vs-Framing Dissociation: ctrl_explicit_wrong vs arm1_unresolved (exact Fisher)
  2. Spec-Anchoring Reversal: models that picked Asset_B in Arm 3A yet did not BLOCK spec_A in Arm 1
  3. Escalation Prompt Efficacy & Specificity: arm1_unresolved vs arm2_unresolved vs arm2_resolved_ctrl
     (exact paired McNemar + balanced accuracy + cross-benchmark Exp 1 calibration replication)
  4. Single-Best Family Prior Divergence (Arm 3A) vs Stage 0 Orthogonal Slate Coverage (Arm 3B)
     (self-labeled AND keyword-verified Asset_A/Asset_B coverage, pairwise Jaccard orthogonality,
      and exact paired McNemar comparing human-selectable coverage vs model auto-pick)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DEFAULT_RESULTS = ROOT / "results-exp5-198runs.json"
DEFAULT_SUMMARY = ROOT / "summary-exp5-198runs.json"

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "over", "under", "your",
    "their", "only", "using", "across", "within", "before", "after", "build", "system",
    "tool", "platform", "service", "data", "workflow", "users", "team", "without", "more",
    "than", "each", "every", "single", "core", "will", "have", "asset", "option", "direction",
}


def verify_sha256_manifest(base_dir: Path = ROOT, manifest_name: str = "scenarios.sha256") -> tuple[int, int, list[str]]:
    manifest = base_dir / manifest_name
    ok = 0
    total = 0
    errors: list[str] = []
    if not manifest.is_file():
        return 0, 0, [f"MISSING: {manifest_name}"]
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        expected, rel = line.split(None, 1)
        target = base_dir / rel.strip()
        total += 1
        if not target.is_file():
            errors.append(f"MISSING: {rel}")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual == expected:
            ok += 1
        else:
            errors.append(f"MISMATCH: {rel}")
    return ok, total, errors


def _binom_cdf_upper(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * (p ** i) * ((1.0 - p) ** (n - i)) for i in range(k, n + 1))


def _binom_cdf_lower(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * (p ** i) * ((1.0 - p) ** (n - i)) for i in range(0, k + 1))


def clopper_pearson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n <= 0:
        return (0.0, 1.0)
    if k == 0:
        lo = 0.0
    else:
        a, b = 0.0, 1.0
        for _ in range(60):
            m = 0.5 * (a + b)
            if _binom_cdf_upper(k, n, m) > alpha / 2.0:
                b = m
            else:
                a = m
        lo = 0.5 * (a + b)
    if k == n:
        hi = 1.0
    else:
        a, b = 0.0, 1.0
        for _ in range(60):
            m = 0.5 * (a + b)
            if _binom_cdf_lower(k, n, m) > alpha / 2.0:
                a = m
            else:
                b = m
        hi = 0.5 * (a + b)
    return (round(lo, 4), round(hi, 4))


def exact_mcnemar_p(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2.0 * sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    p = min(1.0, p)
    return float(f"{p:.6g}")


def exact_fisher_2x2(a: int, b: int, c: int, d: int) -> float:
    r1, r2 = a + b, c + d
    c1, c2 = a + c, b + d
    n = r1 + r2
    if n == 0:
        return 1.0

    def hyper(x: int) -> float:
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / math.comb(n, c1)

    p_obs = hyper(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    p_sum = sum(hyper(x) for x in range(lo, hi + 1) if hyper(x) <= p_obs + 1e-15)
    p_sum = min(1.0, p_sum)
    return float(f"{p_sum:.6g}")


def _rate(k: int, n: int) -> dict[str, Any]:
    lo, hi = clopper_pearson_ci(k, n)
    return {"k": k, "n": n, "rate": round(k / n, 4) if n else 0.0, "ci95": [lo, hi]}


def _norm_verdict(parsed: dict[str, Any] | None) -> str:
    if not isinstance(parsed, dict):
        return "INVALID"
    v = str(parsed.get("verdict") or "").strip().upper()
    return v if v in ("PASS", "NEEDS_PATCH", "BLOCKED") else "INVALID"


def _norm_asset(raw_val: Any) -> str:
    s = str(raw_val or "").strip().lower().replace("-", "_").replace(" ", "_")
    if s in ("asset_a", "a"):
        return "Asset_A"
    if s in ("asset_b", "b"):
        return "Asset_B"
    if "hybrid" in s or "both" in s:
        return "Hybrid"
    return "Other"


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]{3,}", text.lower()) if t not in STOPWORDS}


def framing_orthogonality_jaccard(framings: list[dict[str, Any]]) -> float:
    if not isinstance(framings, list) or len(framings) < 2:
        return 1.0
    sets = [
        _tokenize(f"{f.get('title', '')} {f.get('core_mechanism', '')}")
        for f in framings
        if isinstance(f, dict)
    ]
    if len(sets) < 2:
        return 1.0
    sims = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            u = sets[i] | sets[j]
            sims.append(len(sets[i] & sets[j]) / len(u) if u else 1.0)
    return round(sum(sims) / len(sims), 4)


def verify_option_asset_by_keywords(opt: dict[str, Any], sc_meta: dict[str, Any]) -> str:
    txt = f"{opt.get('title', '')} {opt.get('core_mechanism', '')}".lower()
    a_hits = sum(1 for kw in sc_meta.get("asset_a_keywords", []) if kw.lower() in txt)
    b_hits = sum(1 for kw in sc_meta.get("asset_b_keywords", []) if kw.lower() in txt)
    if a_hits >= 1 and a_hits > b_hits:
        return "Asset_A"
    if b_hits >= 1 and b_hits > a_hits:
        return "Asset_B"
    if a_hits >= 1 and b_hits >= 1:
        return "Hybrid"
    return "Other"


def score_results(
    results_path: Path = DEFAULT_RESULTS,
    _unused_blind_path: Path | None = None,
    base_dir: Path = ROOT,
) -> dict[str, Any]:
    sha_ok, sha_total, sha_errs = verify_sha256_manifest(base_dir, "scenarios.sha256")
    manifest = json.loads((base_dir / "scenarios_manifest.json").read_text(encoding="utf-8"))
    sc_meta = {s["id"]: s for s in manifest["explicit_controls"] + manifest["underspecified_scenarios"]}
    explicit_ids = [s["id"] for s in manifest["explicit_controls"]]
    underspec_ids = [s["id"] for s in manifest["underspecified_scenarios"]]

    raw = json.loads(results_path.read_text(encoding="utf-8"))
    runs = raw.get("runs", [])
    status_counts = Counter(r.get("status") for r in runs)
    ok_runs = [r for r in runs if r.get("status") == "OK"]
    families = sorted({r["family"] for r in runs})

    idx: dict[tuple[str, str, str], dict[str, Any]] = {}
    for r in ok_runs:
        idx[(r["family"], r["scenario"], r["condition"])] = r

    def summarize_verdict_cond(cond: str, sc_ids: list[str], fam_list: list[str]) -> dict[str, Any]:
        subset = [idx[(f, s, cond)] for f in fam_list for s in sc_ids if (f, s, cond) in idx]
        n = len(subset)
        vc = Counter(_norm_verdict(r["parsed"]) for r in subset)
        return {
            "n_ok": n,
            "verdict_counts": dict(vc),
            "pass": _rate(vc["PASS"], n),
            "needs_patch": _rate(vc["NEEDS_PATCH"], n),
            "blocked": _rate(vc["BLOCKED"], n),
            "non_pass": _rate(vc["NEEDS_PATCH"] + vc["BLOCKED"], n),
        }

    def summarize_jury(cond: str, sc_ids: list[str]) -> dict[str, Any]:
        full = 0
        unanim_pass = maj_pass = unanim_blk = maj_blk = zero_blk = 0
        rows = []
        for s in sc_ids:
            rs = [idx[(f, s, cond)] for f in families if (f, s, cond) in idx]
            vs = [_norm_verdict(r["parsed"]) for r in rs]
            if len(rs) == 3:
                full += 1
                p_c = sum(1 for v in vs if v == "PASS")
                b_c = sum(1 for v in vs if v == "BLOCKED")
                if p_c == 3:
                    unanim_pass += 1
                if p_c >= 2:
                    maj_pass += 1
                if b_c == 3:
                    unanim_blk += 1
                if b_c >= 2:
                    maj_blk += 1
                if b_c == 0:
                    zero_blk += 1
            rows.append({
                "scenario": s,
                "verdicts": {r["family"]: _norm_verdict(r["parsed"]) for r in rs},
            })
        return {
            "n_complete_3fam": full,
            "unanimous_3of3_pass": _rate(unanim_pass, full),
            "majority_2of3_pass": _rate(maj_pass, full),
            "unanimous_3of3_blocked": _rate(unanim_blk, full),
            "majority_2of3_blocked": _rate(maj_blk, full),
            "zero_of_3_blocked": _rate(zero_blk, full),
            "per_scenario": rows,
        }

    def paired_mcnemar(c1: str, c2: str, pred) -> dict[str, Any]:
        n_p = b = c = both_yes = both_no = 0
        for f in families:
            for s in underspec_ids:
                if (f, s, c1) not in idx or (f, s, c2) not in idx:
                    continue
                n_p += 1
                y1 = bool(pred(idx[(f, s, c1)]))
                y2 = bool(pred(idx[(f, s, c2)]))
                if y1 and y2:
                    both_yes += 1
                elif not y1 and not y2:
                    both_no += 1
                elif not y1 and y2:
                    b += 1
                else:
                    c += 1
        return {
            "n_pairs": n_p,
            "both_yes": both_yes,
            "c1_no_c2_yes": b,
            "c1_yes_c2_no": c,
            "both_no": both_no,
            "mcnemar_exact_p": exact_mcnemar_p(b, c),
        }

    # Spec-anchoring reversal: when model itself chose Asset_B in Arm 3A, how did it judge spec_A in Arm 1?
    pref_b_n = pref_b_not_blk = pref_b_pass = 0
    pref_b_details = []
    for f in families:
        for s in underspec_ids:
            if (f, s, "arm3a_single_best") in idx and (f, s, "arm1_unresolved") in idx:
                p3a = _norm_asset(idx[(f, s, "arm3a_single_best")]["parsed"].get("chosen_asset"))
                v1 = _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"])
                if p3a == "Asset_B":
                    pref_b_n += 1
                    if v1 != "BLOCKED":
                        pref_b_not_blk += 1
                    if v1 == "PASS":
                        pref_b_pass += 1
                    pref_b_details.append({"family": f, "scenario": s, "arm1_verdict_on_spec_A": v1})

    # Arm 3A single best
    def summarize_arm3a(fam_list: list[str]) -> dict[str, Any]:
        subset = [idx[(f, s, "arm3a_single_best")] for f in fam_list for s in underspec_ids if (f, s, "arm3a_single_best") in idx]
        n = len(subset)
        cc = Counter(_norm_asset(r["parsed"].get("chosen_asset")) for r in subset)
        return {
            "n_ok": n,
            "counts": dict(cc),
            "chose_asset_a": _rate(cc["Asset_A"], n),
            "chose_asset_b": _rate(cc["Asset_B"], n),
            "chose_hybrid_or_other": _rate(cc["Hybrid"] + cc["Other"], n),
        }

    full_3a = unanim_a = maj_a = unanim_b = split_ab = 0
    rows_3a = []
    for s in underspec_ids:
        rs = [idx[(f, s, "arm3a_single_best")] for f in families if (f, s, "arm3a_single_best") in idx]
        picks = {r["family"]: _norm_asset(r["parsed"].get("chosen_asset")) for r in rs}
        if len(rs) == 3:
            full_3a += 1
            a_c = sum(1 for v in picks.values() if v == "Asset_A")
            b_c = sum(1 for v in picks.values() if v == "Asset_B")
            if a_c == 3:
                unanim_a += 1
            elif b_c == 3:
                unanim_b += 1
            else:
                split_ab += 1
            if a_c >= 2:
                maj_a += 1
        rows_3a.append({"scenario": s, "picks": picks})

    # Arm 3B Stage 0 orthogonal slate
    def summarize_arm3b(fam_list: list[str]) -> dict[str, Any]:
        subset = [idx[(f, s, "arm3b_stage0_slate")] for f in fam_list for s in underspec_ids if (f, s, "arm3b_stage0_slate") in idx]
        n = len(subset)
        has_3 = slate_has_a = slate_has_b = slate_has_both = 0
        kw_has_both = kw_has_b = 0
        rec_a = rec_b = rec_other = 0
        b_slate_only = b_rec_only = 0
        a_slate_only = a_rec_only = 0
        jaccards: list[float] = []
        for r in subset:
            p = r["parsed"] or {}
            fr = p.get("framings") if isinstance(p.get("framings"), list) else []
            if len(fr) == 3:
                has_3 += 1
            jaccards.append(framing_orthogonality_jaccard(fr))
            meta = sc_meta[r["scenario"]]
            self_by_id: dict[str, str] = {}
            kw_by_id: dict[str, str] = {}
            for opt in fr:
                if isinstance(opt, dict):
                    oid = str(opt.get("id") or "").strip().upper()
                    self_by_id[oid] = _norm_asset(opt.get("primary_asset"))
                    kw_by_id[oid] = verify_option_asset_by_keywords(opt, meta)
            vals_self = set(self_by_id.values())
            vals_kw = set(kw_by_id.values())
            if "Asset_A" in vals_self:
                slate_has_a += 1
            if "Asset_B" in vals_self:
                slate_has_b += 1
            if "Asset_A" in vals_self and "Asset_B" in vals_self:
                slate_has_both += 1
            if "Asset_B" in vals_kw:
                kw_has_b += 1
            if "Asset_A" in vals_kw and "Asset_B" in vals_kw:
                kw_has_both += 1
            rec_id = str(p.get("recommended") or "").strip().upper()
            rec_asset = self_by_id.get(rec_id, "Other")
            if rec_asset == "Asset_A":
                rec_a += 1
            elif rec_asset == "Asset_B":
                rec_b += 1
            else:
                rec_other += 1
            if ("Asset_B" in vals_self) and (rec_asset != "Asset_B"):
                b_slate_only += 1
            elif ("Asset_B" not in vals_self) and (rec_asset == "Asset_B"):
                b_rec_only += 1
            if ("Asset_A" in vals_self) and (rec_asset != "Asset_A"):
                a_slate_only += 1
            elif ("Asset_A" not in vals_self) and (rec_asset == "Asset_A"):
                a_rec_only += 1
        return {
            "n_ok": n,
            "exactly_3_options": _rate(has_3, n),
            "mean_pairwise_jaccard": round(sum(jaccards) / len(jaccards), 4) if jaccards else None,
            "slate_has_asset_a_self": _rate(slate_has_a, n),
            "slate_has_asset_b_self": _rate(slate_has_b, n),
            "slate_covers_both_a_and_b_self": _rate(slate_has_both, n),
            "slate_has_asset_b_kw_verified": _rate(kw_has_b, n),
            "slate_covers_both_kw_verified": _rate(kw_has_both, n),
            "recommended_asset_a": _rate(rec_a, n),
            "recommended_asset_b": _rate(rec_b, n),
            "recommended_hybrid_or_other": _rate(rec_other, n),
            "asset_b_human_pick_lift_mcnemar_p": exact_mcnemar_p(b_slate_only, b_rec_only),
            "asset_b_in_slate_but_not_autopicked": b_slate_only,
            "asset_a_human_pick_lift_mcnemar_p": exact_mcnemar_p(a_slate_only, a_rec_only),
            "asset_a_in_slate_but_not_autopicked": a_slate_only,
        }

    ctrl_all = summarize_verdict_cond("ctrl_explicit_wrong", explicit_ids, families)
    a1_all = summarize_verdict_cond("arm1_unresolved", underspec_ids, families)
    a2_unres_all = summarize_verdict_cond("arm2_unresolved", underspec_ids, families)
    a2_res_all = summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, families)

    dissociation_blocked_p = exact_fisher_2x2(
        ctrl_all["blocked"]["k"],
        ctrl_all["blocked"]["n"] - ctrl_all["blocked"]["k"],
        a1_all["blocked"]["k"],
        a1_all["blocked"]["n"] - a1_all["blocked"]["k"],
    )

    # Cross-benchmark Exp 1 replication on arm2_resolved_ctrl: Codex PASS vs Claude/Gemini PASS
    codex_vs_claude_b = codex_vs_claude_c = 0
    for s in underspec_ids:
        if ("codex", s, "arm2_resolved_ctrl") in idx and ("claude", s, "arm2_resolved_ctrl") in idx:
            cp = _norm_verdict(idx[("codex", s, "arm2_resolved_ctrl")]["parsed"]) == "PASS"
            lp = _norm_verdict(idx[("claude", s, "arm2_resolved_ctrl")]["parsed"]) == "PASS"
            if (not cp) and lp:
                codex_vs_claude_b += 1
            elif cp and (not lp):
                codex_vs_claude_c += 1

    tpr_blk = a2_unres_all["blocked"]["rate"]
    fpr_blk = a2_res_all["blocked"]["rate"]

    return {
        "benchmark": "exp5-premise-lockin",
        "sha256_verified": {"ok": sha_ok, "total": sha_total, "errors": sha_errs},
        "total_runs": len(runs),
        "status_counts": dict(status_counts),
        "models": raw.get("models", {}),
        "regime1_explicit_control": {
            "pooled": ctrl_all,
            "by_family": {f: summarize_verdict_cond("ctrl_explicit_wrong", explicit_ids, [f]) for f in families},
            "jury": summarize_jury("ctrl_explicit_wrong", explicit_ids),
        },
        "arm1_unresolved_standard": {
            "pooled": a1_all,
            "by_family": {f: summarize_verdict_cond("arm1_unresolved", underspec_ids, [f]) for f in families},
            "jury": summarize_jury("arm1_unresolved", underspec_ids),
        },
        "goal_vs_framing_dissociation": {
            "ctrl_explicit_blocked": ctrl_all["blocked"],
            "arm1_unresolved_blocked": a1_all["blocked"],
            "fisher_blocked_p": dissociation_blocked_p,
        },
        "spec_anchoring_reversal": {
            "model_preferred_asset_b_in_arm3a": pref_b_n,
            "did_not_block_spec_a_in_arm1": _rate(pref_b_not_blk, pref_b_n),
            "stamped_pass_on_spec_a_in_arm1": _rate(pref_b_pass, pref_b_n),
            "cells": pref_b_details,
        },
        "arm2_escalation_prompt": {
            "unresolved_pooled": a2_unres_all,
            "unresolved_by_family": {f: summarize_verdict_cond("arm2_unresolved", underspec_ids, [f]) for f in families},
            "unresolved_jury": summarize_jury("arm2_unresolved", underspec_ids),
            "resolved_ctrl_pooled": a2_res_all,
            "resolved_ctrl_by_family": {f: summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, [f]) for f in families},
            "resolved_ctrl_jury": summarize_jury("arm2_resolved_ctrl", underspec_ids),
            "discrimination": {
                "block_gap_unresolved_minus_resolved": round(tpr_blk - fpr_blk, 4),
                "balanced_accuracy_block": round(0.5 * (tpr_blk + (1.0 - fpr_blk)), 4),
            },
            "paired_arm1_vs_arm2_unresolved": {
                "blocked": paired_mcnemar("arm1_unresolved", "arm2_unresolved", lambda r: _norm_verdict(r["parsed"]) == "BLOCKED"),
            },
            "paired_arm2_unresolved_vs_resolved_ctrl": {
                "blocked": paired_mcnemar("arm2_resolved_ctrl", "arm2_unresolved", lambda r: _norm_verdict(r["parsed"]) == "BLOCKED"),
                "pass": paired_mcnemar("arm2_unresolved", "arm2_resolved_ctrl", lambda r: _norm_verdict(r["parsed"]) == "PASS"),
            },
            "exp1_calibration_replication_on_resolved_ctrl": {
                "claude_pass": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["claude"])["pass"],
                "gemini_pass": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["gemini"])["pass"],
                "codex_pass": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["codex"])["pass"],
                "codex_needs_patch": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["codex"])["needs_patch"],
                "claude_vs_codex_pass_mcnemar_p": exact_mcnemar_p(codex_vs_claude_b, codex_vs_claude_c),
            },
        },
        "arm3a_single_best_priors": {
            "pooled": summarize_arm3a(families),
            "by_family": {f: summarize_arm3a([f]) for f in families},
            "jury_agreement": {
                "n_complete_3fam": full_3a,
                "unanimous_3of3_asset_a": _rate(unanim_a, full_3a),
                "majority_2of3_asset_a": _rate(maj_a, full_3a),
                "unanimous_3of3_asset_b": _rate(unanim_b, full_3a),
                "split_across_families": _rate(split_ab, full_3a),
                "per_scenario": rows_3a,
            },
        },
        "arm3b_stage0_orthogonal": {
            "pooled": summarize_arm3b(families),
            "by_family": {f: summarize_arm3b([f]) for f in families},
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Score Exp 5 198-run Premise Lock-In benchmark.")
    ap.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    ap.add_argument("--out", type=Path, default=DEFAULT_SUMMARY)
    args = ap.parse_args()

    summary = score_results(args.results, None, ROOT)
    if summary["sha256_verified"]["errors"]:
        print("SHA-256 VERIFICATION FAILED:", summary["sha256_verified"]["errors"], file=sys.stderr)
        sys.exit(1)
    args.out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    c = summary["regime1_explicit_control"]["pooled"]
    a1 = summary["arm1_unresolved_standard"]["pooled"]
    d = summary["goal_vs_framing_dissociation"]
    sar = summary["spec_anchoring_reversal"]
    a2u = summary["arm2_escalation_prompt"]["unresolved_pooled"]
    a2r = summary["arm2_escalation_prompt"]["resolved_ctrl_pooled"]
    p12 = summary["arm2_escalation_prompt"]["paired_arm1_vs_arm2_unresolved"]["blocked"]
    p2c = summary["arm2_escalation_prompt"]["paired_arm2_unresolved_vs_resolved_ctrl"]["blocked"]
    rep = summary["arm2_escalation_prompt"]["exp1_calibration_replication_on_resolved_ctrl"]
    a3a = summary["arm3a_single_best_priors"]
    a3b = summary["arm3b_stage0_orthogonal"]["pooled"]

    print(f"Exp 5 Scored: {summary['status_counts']} | SHA-256 {summary['sha256_verified']['ok']}/{summary['sha256_verified']['total']}")
    print(f"  Regime 1 Explicit Ctrl : BLOCKED={c['blocked']['k']}/{c['blocked']['n']} ({c['blocked']['rate']:.1%})")
    print(f"  Arm 1 Unresolved (Std) : BLOCKED={a1['blocked']['k']}/{a1['blocked']['n']} ({a1['blocked']['rate']:.1%}) | PASS={a1['pass']['k']}/{a1['pass']['n']} | PATCH={a1['needs_patch']['k']}/{a1['needs_patch']['n']}")
    print(f"  Dissociation Fisher p  : {d['fisher_blocked_p']:.3e}")
    print(f"  Spec-Anchoring Reversal: {sar['did_not_block_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_b_in_arm3a']} ({sar['did_not_block_spec_a_in_arm1']['rate']:.1%}) did not BLOCK spec_A; {sar['stamped_pass_on_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_b_in_arm3a']} ({sar['stamped_pass_on_spec_a_in_arm1']['rate']:.1%}) stamped PASS")
    print(f"  Arm 2 Unresolved (Esc) : BLOCKED={a2u['blocked']['k']}/{a2u['blocked']['n']} ({a2u['blocked']['rate']:.1%}) vs Arm 1 McNemar p={p12['mcnemar_exact_p']:.3e}")
    print(f"  Arm 2 Resolved Control : BLOCKED={a2r['blocked']['k']}/{a2r['blocked']['n']} ({a2r['blocked']['rate']:.1%}) vs Unresolved McNemar p={p2c['mcnemar_exact_p']:.3e}")
    print(f"  Exp 1 Replication (A2R): Claude PASS={rep['claude_pass']['k']}/12, Gemini PASS={rep['gemini_pass']['k']}/12, Codex PASS={rep['codex_pass']['k']}/12 (12/12 NEEDS_PATCH; McNemar p={rep['claude_vs_codex_pass_mcnemar_p']:.6f})")
    print(f"  Arm 3A Single-Best     : Asset_A={a3a['pooled']['chose_asset_a']['k']}/36 (Codex {a3a['by_family']['codex']['chose_asset_a']['k']}/12, Gemini {a3a['by_family']['gemini']['chose_asset_a']['k']}/12, Claude {a3a['by_family']['claude']['chose_asset_a']['k']}/12)")
    print(f"  Arm 3B Stage 0 Slate   : covers BOTH={a3b['slate_covers_both_a_and_b_self']['k']}/36 (kw={a3b['slate_covers_both_kw_verified']['k']}/36, Jaccard={a3b['mean_pairwise_jaccard']}) | auto-rec B={a3b['recommended_asset_b']['k']}/36 (lift p={a3b['asset_b_human_pick_lift_mcnemar_p']:.3e}) | auto-rec A={a3b['recommended_asset_a']['k']}/36 (lift p={a3b['asset_a_human_pick_lift_mcnemar_p']:.3e})")


if __name__ == "__main__":
    main()
