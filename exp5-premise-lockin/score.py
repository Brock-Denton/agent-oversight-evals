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


def _count(k: int, n: int) -> dict[str, Any]:
    """Descriptive count/rate without binomial CI (used for pooled multi-model aggregates sharing dossiers)."""
    return {"k": k, "n": n, "rate": round(k / n, 4) if n else 0.0}


def holm_bonferroni(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out: dict[str, float] = {}
    running = 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, (m - i) * p)
        running = max(running, adj)
        out[k] = float(f"{running:.6g}")
    return out


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
        fmt = _rate if len(fam_list) == 1 else _count
        return {
            "n_ok": n,
            "verdict_counts": dict(vc),
            "pass": fmt(vc["PASS"], n),
            "needs_patch": fmt(vc["NEEDS_PATCH"], n),
            "blocked": fmt(vc["BLOCKED"], n),
            "non_pass": fmt(vc["NEEDS_PATCH"] + vc["BLOCKED"], n),
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

    # Deterministic Arm 1 escalation & Asset-B deferral audit across all parsed text fields
    _ASK_HUMAN_RE = re.compile(
        r"(?:"
        r"\b(?:stage 0|tie[- ]?break|unresolved[^.?!;\n]{0,45}(?:trade[- ]?off|goal|choice|framing|priority|tension))\b|"
        r"\b(?:human|principal|sponsor|owner|leadership|stakeholder)\s+(?:sign[- ]?off|decision|selection|choice|approval|pick)\b|"
        r"\b(?:ask|confirm with|escalate(?:\s+to)?)\s+(?:the\s+)?(?:human|principal|sponsor|owner|leadership|stakeholder)\b"
        r")",
        re.I,
    )
    _DEFER_ISSUE_RE = re.compile(r"\b(?:asset b|defer(?:red|ring|ral)?)\b", re.I)

    a1_asked_human_cells: list[dict[str, str]] = []
    a1_patch_asset_b_dep_cells: list[dict[str, str]] = []
    a1_blocked_cells: list[dict[str, str]] = []
    a2_asked_human_n = 0
    for f in families:
        for s in underspec_ids:
            if (f, s, "arm2_unresolved") in idx:
                p2 = idx[(f, s, "arm2_unresolved")]["parsed"] or {}
                txt2 = " ".join([
                    str(p2.get("one_line_reason") or ""),
                    *[str(x) for x in (p2.get("fatal_issues") or [])],
                    *[str(x) for x in (p2.get("major_issues") or [])],
                ])
                if _ASK_HUMAN_RE.search(txt2):
                    a2_asked_human_n += 1
            if (f, s, "arm1_unresolved") not in idx:
                continue
            r = idx[(f, s, "arm1_unresolved")]
            p = r["parsed"] or {}
            v = _norm_verdict(p)
            olr = str(p.get("one_line_reason") or "")
            fi = [str(x) for x in (p.get("fatal_issues") or [])]
            mi = [str(x) for x in (p.get("major_issues") or [])]
            full_txt = " ".join([olr, *fi, *mi])
            issues_txt = " ".join([*fi, *mi])
            if _ASK_HUMAN_RE.search(full_txt):
                a1_asked_human_cells.append({"family": f, "scenario": s, "verdict": v})
            if v == "NEEDS_PATCH" and _DEFER_ISSUE_RE.search(issues_txt):
                a1_patch_asset_b_dep_cells.append({"family": f, "scenario": s, "verdict": v})
            if v == "BLOCKED":
                a1_blocked_cells.append({"family": f, "scenario": s, "verdict": v, "one_line_reason": olr})

    # Cross-role descriptive contrast: disjoint Arm 3A Asset_B vs Asset_A subsets (pooled + within-family)
    pref_b_n = pref_b_not_blk = pref_b_pass = 0
    pref_a_n = pref_a_not_blk = pref_a_pass = 0
    pref_b_details = []
    cross_role_by_family: dict[str, Any] = {}
    for f in families:
        fb_n = fb_nb = fb_p = fa_n = fa_nb = fa_p = 0
        for s in underspec_ids:
            if (f, s, "arm3a_single_best") in idx and (f, s, "arm1_unresolved") in idx:
                p3a = _norm_asset(idx[(f, s, "arm3a_single_best")]["parsed"].get("chosen_asset"))
                v1 = _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"])
                if p3a == "Asset_B":
                    pref_b_n += 1
                    fb_n += 1
                    if v1 != "BLOCKED":
                        pref_b_not_blk += 1
                        fb_nb += 1
                    if v1 == "PASS":
                        pref_b_pass += 1
                        fb_p += 1
                    pref_b_details.append({"family": f, "scenario": s, "arm1_verdict_on_spec_A": v1})
                elif p3a == "Asset_A":
                    pref_a_n += 1
                    fa_n += 1
                    if v1 != "BLOCKED":
                        pref_a_not_blk += 1
                        fa_nb += 1
                    if v1 == "PASS":
                        pref_a_pass += 1
                        fa_p += 1
        cross_role_by_family[f] = {
            "pref_b_not_blocked": _count(fb_nb, fb_n),
            "pref_a_not_blocked": _count(fa_nb, fa_n),
            "pref_b_pass": _count(fb_p, fb_n),
            "pref_a_pass": _count(fa_p, fa_n),
        }

    # Arm 3A single best
    def summarize_arm3a(fam_list: list[str]) -> dict[str, Any]:
        subset = [idx[(f, s, "arm3a_single_best")] for f in fam_list for s in underspec_ids if (f, s, "arm3a_single_best") in idx]
        n = len(subset)
        cc = Counter(_norm_asset(r["parsed"].get("chosen_asset")) for r in subset)
        fmt = _rate if len(fam_list) == 1 else _count
        return {
            "n_ok": n,
            "counts": dict(cc),
            "chose_asset_a": fmt(cc["Asset_A"], n),
            "chose_asset_b": fmt(cc["Asset_B"], n),
            "chose_hybrid_or_other": fmt(cc["Hybrid"] + cc["Other"], n),
        }

    full_3a = unanim_a = at_least_2a = split_2a_1b = split_1a_2b = unanim_b = split_ab = 0
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
                if a_c == 2:
                    split_2a_1b += 1
                elif b_c == 2:
                    split_1a_2b += 1
            if a_c >= 2:
                at_least_2a += 1
        rows_3a.append({"scenario": s, "picks": picks})

    # Arm 3B Stage 0 orthogonal slate
    def summarize_arm3b(fam_list: list[str]) -> dict[str, Any]:
        subset = [idx[(f, s, "arm3b_stage0_slate")] for f in fam_list for s in underspec_ids if (f, s, "arm3b_stage0_slate") in idx]
        n = len(subset)
        has_3 = slate_has_a = slate_has_b = slate_has_both = 0
        kw_has_both = kw_has_b = 0
        rec_a = rec_b = rec_other = 0
        b_slate_only = 0
        a_slate_only = 0
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
            if ("Asset_A" in vals_self) and (rec_asset != "Asset_A"):
                a_slate_only += 1
        fmt = _rate if len(fam_list) == 1 else _count
        return {
            "note": "Descriptive exposure counts only; a 3-option slate covers more options than a 1-option pick by construction.",
            "n_ok": n,
            "exactly_3_options": fmt(has_3, n),
            "mean_pairwise_jaccard": round(sum(jaccards) / len(jaccards), 4) if jaccards else None,
            "slate_has_asset_a_self": fmt(slate_has_a, n),
            "slate_has_asset_b_self": fmt(slate_has_b, n),
            "slate_covers_both_a_and_b_self": fmt(slate_has_both, n),
            "slate_has_asset_b_kw_verified": fmt(kw_has_b, n),
            "slate_covers_both_kw_verified": fmt(kw_has_both, n),
            "recommended_asset_a": fmt(rec_a, n),
            "recommended_asset_b": fmt(rec_b, n),
            "recommended_hybrid_or_other": fmt(rec_other, n),
            "asset_b_in_slate_but_not_recommended": b_slate_only,
            "asset_a_in_slate_but_not_recommended": a_slate_only,
        }

    ctrl_all = summarize_verdict_cond("ctrl_explicit_wrong", explicit_ids, families)
    a1_all = summarize_verdict_cond("arm1_unresolved", underspec_ids, families)
    a2_unres_all = summarize_verdict_cond("arm2_unresolved", underspec_ids, families)
    a2_res_all = summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, families)

    # Dossier-level (scenario-clustered, zero pseudoreplication across models!)
    e_maj_blk = sum(
        1 for s in explicit_ids
        if sum(1 for f in families if (f, s, "ctrl_explicit_wrong") in idx and _norm_verdict(idx[(f, s, "ctrl_explicit_wrong")]["parsed"]) == "BLOCKED") >= 2
    )
    u_a1_maj_blk = sum(
        1 for s in underspec_ids
        if sum(1 for f in families if (f, s, "arm1_unresolved") in idx and _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"]) == "BLOCKED") >= 2
    )
    u_a1_any_blk = sum(
        1 for s in underspec_ids
        if sum(1 for f in families if (f, s, "arm1_unresolved") in idx and _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"]) == "BLOCKED") >= 1
    )
    a1_vs_a2_dossier_up = sum(
        1 for s in underspec_ids
        if sum(1 for f in families if (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) == "BLOCKED")
        > sum(1 for f in families if (f, s, "arm1_unresolved") in idx and _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"]) == "BLOCKED")
    )
    a1_vs_a2_dossier_dn = sum(
        1 for s in underspec_ids
        if sum(1 for f in families if (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) == "BLOCKED")
        < sum(1 for f in families if (f, s, "arm1_unresolved") in idx and _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"]) == "BLOCKED")
    )
    a2_vs_ctrl_dossier_up = sum(
        1 for s in underspec_ids
        if sum(1 for f in families if (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) == "BLOCKED")
        > sum(1 for f in families if (f, s, "arm2_resolved_ctrl") in idx and _norm_verdict(idx[(f, s, "arm2_resolved_ctrl")]["parsed"]) == "BLOCKED")
    )
    a2_vs_ctrl_dossier_dn = sum(
        1 for s in underspec_ids
        if sum(1 for f in families if (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) == "BLOCKED")
        < sum(1 for f in families if (f, s, "arm2_resolved_ctrl") in idx and _norm_verdict(idx[(f, s, "arm2_resolved_ctrl")]["parsed"]) == "BLOCKED")
    )
    per_family_dossier_mcnemar: dict[str, Any] = {}
    for f in families:
        fb = sum(1 for s in underspec_ids if (f, s, "arm1_unresolved") in idx and (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) == "BLOCKED" and _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"]) != "BLOCKED")
        fc = sum(1 for s in underspec_ids if (f, s, "arm1_unresolved") in idx and (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) != "BLOCKED" and _norm_verdict(idx[(f, s, "arm1_unresolved")]["parsed"]) == "BLOCKED")
        cb = sum(1 for s in underspec_ids if (f, s, "arm2_resolved_ctrl") in idx and (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) == "BLOCKED" and _norm_verdict(idx[(f, s, "arm2_resolved_ctrl")]["parsed"]) != "BLOCKED")
        cc = sum(1 for s in underspec_ids if (f, s, "arm2_resolved_ctrl") in idx and (f, s, "arm2_unresolved") in idx and _norm_verdict(idx[(f, s, "arm2_unresolved")]["parsed"]) != "BLOCKED" and _norm_verdict(idx[(f, s, "arm2_resolved_ctrl")]["parsed"]) == "BLOCKED")
        per_family_dossier_mcnemar[f] = {
            "arm1_vs_arm2_unresolved": {"flips_up": fb, "flips_down": fc, "exact_mcnemar_p": exact_mcnemar_p(fb, fc)},
            "arm2_unresolved_vs_resolved_ctrl": {"flips_up": cb, "flips_down": cc, "exact_mcnemar_p": exact_mcnemar_p(cb, cc)},
        }

    # Convergent strictness check on arm2_resolved_ctrl (NEEDS_PATCH vs PASS across 12 dossiers)
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

    p_e_u_maj = exact_fisher_2x2(e_maj_blk, len(explicit_ids) - e_maj_blk, u_a1_maj_blk, len(underspec_ids) - u_a1_maj_blk)
    p_e_u_any = exact_fisher_2x2(e_maj_blk, len(explicit_ids) - e_maj_blk, u_a1_any_blk, len(underspec_ids) - u_a1_any_blk)
    p_a1_a2_sign = exact_mcnemar_p(a1_vs_a2_dossier_up, a1_vs_a2_dossier_dn)
    p_a2_ctrl_sign = exact_mcnemar_p(a2_vs_ctrl_dossier_up, a2_vs_ctrl_dossier_dn)
    p_codex_claude_ctrl = exact_mcnemar_p(codex_vs_claude_b, codex_vs_claude_c)
    raw_dossier_pvals = {
        "explicit_vs_unresolved_majority_blocked": p_e_u_maj,
        "explicit_vs_unresolved_any_family_blocked": p_e_u_any,
        "arm1_vs_arm2_unresolved_dossier_sign": p_a1_a2_sign,
        "arm2_unresolved_vs_resolved_ctrl_dossier_sign": p_a2_ctrl_sign,
        "claude_vs_codex_resolved_ctrl_pass": p_codex_claude_ctrl,
    }
    for f in families:
        raw_dossier_pvals[f"{f}_arm1_vs_arm2"] = per_family_dossier_mcnemar[f]["arm1_vs_arm2_unresolved"]["exact_mcnemar_p"]
        raw_dossier_pvals[f"{f}_arm2_vs_resolved_ctrl"] = per_family_dossier_mcnemar[f]["arm2_unresolved_vs_resolved_ctrl"]["exact_mcnemar_p"]
    holm_dossier = holm_bonferroni(raw_dossier_pvals)

    return {
        "benchmark": "exp5-premise-lockin",
        "sha256_verified": {"ok": sha_ok, "total": sha_total, "errors": sha_errs},
        "total_runs": len(runs),
        "status_counts": dict(status_counts),
        "models": raw.get("models", {}),
        "dossier_level_primary_inference": {
            "note": "Post-hoc conservative dossier-level analyses (n=6 explicit controls, n=12 underspecified dossiers; upgraded from frozen PROTOCOL.md's pooled n=36 tests) so 3 models on the same dossier are never treated as independent. Binomial 95% CIs are reported only on dossier-level or single-family (n=6/n=12) proportions; pooled multi-model aggregates report counts and rates only.",
            "explicit_vs_unresolved_majority_blocked": {
                "explicit_maj_blocked": _rate(e_maj_blk, len(explicit_ids)),
                "unresolved_maj_blocked": _rate(u_a1_maj_blk, len(underspec_ids)),
                "exact_fisher_p": p_e_u_maj,
                "holm_adjusted_p": holm_dossier["explicit_vs_unresolved_majority_blocked"],
            },
            "explicit_vs_unresolved_any_family_blocked": {
                "explicit_any_blocked": _rate(e_maj_blk, len(explicit_ids)),
                "unresolved_any_blocked": _rate(u_a1_any_blk, len(underspec_ids)),
                "exact_fisher_p": p_e_u_any,
                "holm_adjusted_p": holm_dossier["explicit_vs_unresolved_any_family_blocked"],
            },
            "arm1_vs_arm2_unresolved_dossier_sign": {
                "n_dossiers": len(underspec_ids),
                "dossiers_higher_in_arm2": a1_vs_a2_dossier_up,
                "dossiers_higher_in_arm1": a1_vs_a2_dossier_dn,
                "exact_sign_p": p_a1_a2_sign,
                "holm_adjusted_p": holm_dossier["arm1_vs_arm2_unresolved_dossier_sign"],
            },
            "arm2_unresolved_vs_resolved_ctrl_dossier_sign": {
                "n_dossiers": len(underspec_ids),
                "dossiers_higher_unresolved": a2_vs_ctrl_dossier_up,
                "dossiers_higher_resolved": a2_vs_ctrl_dossier_dn,
                "exact_sign_p": p_a2_ctrl_sign,
                "holm_adjusted_p": holm_dossier["arm2_unresolved_vs_resolved_ctrl_dossier_sign"],
            },
            "per_family_dossier_mcnemar": per_family_dossier_mcnemar,
            "holm_bonferroni_all_11_dossier_tests": holm_dossier,
            "max_holm_adjusted_p": max(holm_dossier.values()) if holm_dossier else None,
        },
        "regime1_explicit_control": {
            "pooled": ctrl_all,
            "by_family": {f: summarize_verdict_cond("ctrl_explicit_wrong", explicit_ids, [f]) for f in families},
            "jury": summarize_jury("ctrl_explicit_wrong", explicit_ids),
        },
        "arm1_unresolved_standard": {
            "pooled": a1_all,
            "by_family": {f: summarize_verdict_cond("arm1_unresolved", underspec_ids, [f]) for f in families},
            "jury": summarize_jury("arm1_unresolved", underspec_ids),
            "escalation_audit": {
                "rule": "Regex audit over parsed one_line_reason + fatal_issues + major_issues checking (a) explicit request for human/sponsor/principal sign-off or tie-break on Asset A vs B, and (b) NEEDS_PATCH issues citing Asset B or deferral. Pooled multi-model counts/rates reported without binomial CIs.",
                "asked_human_signoff_on_ab": _count(len(a1_asked_human_cells), a1_all["n_ok"]),
                "asked_human_cells": a1_asked_human_cells,
                "arm2_unresolved_regex_sensitivity_check": _count(a2_asked_human_n, a2_unres_all["n_ok"]),
                "needs_patch_mentions_asset_b_or_deferral": _count(len(a1_patch_asset_b_dep_cells), a1_all["needs_patch"]["k"]),
                "needs_patch_asset_b_cells": a1_patch_asset_b_dep_cells,
                "blocked_cells": a1_blocked_cells,
            },
        },
        "spec_review_vs_goal_selection": {
            "note": "Descriptive cross-role contrast comparing disjoint Arm 3A Asset_B (n=16) vs Asset_A (n=20) subsets on Arm 1 verdicts (pooled + within-family). Neither equivalence nor a causal preference effect is claimed.",
            "model_preferred_asset_b_in_arm3a": pref_b_n,
            "model_preferred_asset_a_in_arm3a": pref_a_n,
            "pref_b_did_not_block_spec_a_in_arm1": _count(pref_b_not_blk, pref_b_n),
            "pref_a_did_not_block_spec_a_in_arm1": _count(pref_a_not_blk, pref_a_n),
            "pref_b_stamped_pass_on_spec_a_in_arm1": _count(pref_b_pass, pref_b_n),
            "pref_a_stamped_pass_on_spec_a_in_arm1": _count(pref_a_pass, pref_a_n),
            "by_family": cross_role_by_family,
            "cells": pref_b_details,
        },
        "arm2_escalation_prompt": {
            "note": "Controlled prompt-compliance check verifying whether models enforce an explicit Stage 0 sign-off rule without false-blocking when sign-off is present.",
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
            "convergent_strictness_on_resolved_ctrl": {
                "note": "Distinct endpoint from Exp 1 (NEEDS_PATCH vs PASS on clean specs, not BLOCK rate).",
                "claude_pass": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["claude"])["pass"],
                "gemini_pass": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["gemini"])["pass"],
                "codex_pass": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["codex"])["pass"],
                "codex_needs_patch": summarize_verdict_cond("arm2_resolved_ctrl", underspec_ids, ["codex"])["needs_patch"],
                "claude_vs_codex_pass_dossier_mcnemar_p": exact_mcnemar_p(codex_vs_claude_b, codex_vs_claude_c),
            },
        },
        "arm3a_single_best_priors": {
            "pooled": summarize_arm3a(families),
            "by_family": {f: summarize_arm3a([f]) for f in families},
            "jury_agreement": {
                "n_complete_3fam": full_3a,
                "unanimous_3of3_asset_a": _rate(unanim_a, full_3a),
                "split_2a_1b": _rate(split_2a_1b, full_3a),
                "split_1a_2b": _rate(split_1a_2b, full_3a),
                "unanimous_3of3_asset_b": _rate(unanim_b, full_3a),
                "at_least_2of3_asset_a_inclusive": _rate(at_least_2a, full_3a),
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
    dl = summary["dossier_level_primary_inference"]
    sar = summary["spec_review_vs_goal_selection"]
    a2u = summary["arm2_escalation_prompt"]["unresolved_pooled"]
    a2r = summary["arm2_escalation_prompt"]["resolved_ctrl_pooled"]
    rep = summary["arm2_escalation_prompt"]["convergent_strictness_on_resolved_ctrl"]
    a3a = summary["arm3a_single_best_priors"]
    a3b = summary["arm3b_stage0_orthogonal"]["pooled"]

    print(f"Exp 5 Scored: {summary['status_counts']} | SHA-256 {summary['sha256_verified']['ok']}/{summary['sha256_verified']['total']}")
    print(f"  Regime 1 Explicit Ctrl : BLOCKED={c['blocked']['k']}/{c['blocked']['n']} (dossier maj 6/6)")
    print(f"  Arm 1 Unresolved (Std) : BLOCKED={a1['blocked']['k']}/{a1['blocked']['n']} | PASS={a1['pass']['k']}/{a1['pass']['n']} | PATCH={a1['needs_patch']['k']}/{a1['needs_patch']['n']}")
    print(f"  Dossier Dissociation   : maj BLOCK 6/6 vs 0/12 Fisher p={dl['explicit_vs_unresolved_majority_blocked']['exact_fisher_p']:.3e} (any 6/6 vs 1/12 p={dl['explicit_vs_unresolved_any_family_blocked']['exact_fisher_p']:.3e})")
    print(f"  Cross-Role (3A -> 1)   : pref_B not-blocked={sar['pref_b_did_not_block_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_b_in_arm3a']} vs pref_A={sar['pref_a_did_not_block_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_a_in_arm3a']}; PASS={sar['pref_b_stamped_pass_on_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_b_in_arm3a']} vs {sar['pref_a_stamped_pass_on_spec_a_in_arm1']['k']}/{sar['model_preferred_asset_a_in_arm3a']}")
    print(f"  Arm 2 Prompt Compliance: BLOCKED={a2u['blocked']['k']}/{a2u['blocked']['n']} vs Arm 1 (dossier 12v0 sign p={dl['arm1_vs_arm2_unresolved_dossier_sign']['exact_sign_p']:.6f}) vs Ctrl={a2r['blocked']['k']}/{a2r['blocked']['n']} (dossier 12v0 sign p={dl['arm2_unresolved_vs_resolved_ctrl_dossier_sign']['exact_sign_p']:.6f})")
    print(f"  Convergent Strictness  : Claude PASS={rep['claude_pass']['k']}/12, Gemini PASS={rep['gemini_pass']['k']}/12, Codex PASS={rep['codex_pass']['k']}/12 (12/12 NEEDS_PATCH; dossier McNemar p={rep['claude_vs_codex_pass_dossier_mcnemar_p']:.6f})")
    print(f"  Arm 3A Single-Best     : Asset_A={a3a['pooled']['chose_asset_a']['k']}/36 (Codex {a3a['by_family']['codex']['chose_asset_a']['k']}/12, Gemini {a3a['by_family']['gemini']['chose_asset_a']['k']}/12, Claude {a3a['by_family']['claude']['chose_asset_a']['k']}/12)")
    print(f"  Arm 3B Stage 0 Slate   : covers BOTH={a3b['slate_covers_both_a_and_b_self']['k']}/36 (kw={a3b['slate_covers_both_kw_verified']['k']}/36, lexical Jaccard={a3b['mean_pairwise_jaccard']})")


if __name__ == "__main__":
    main()
