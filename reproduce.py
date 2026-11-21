#!/usr/bin/env python3
"""reproduce.py — Zero-dependency deterministic recomputation of all 4 empirical studies in agent-oversight-evals.

Recomputes Exp 1 (from anonymized gates + ablation JSON), Exp 2 (directly from per-case by_case counts via
exact paired randomization tests), Exp 3 (with symmetric timeout exclusion + strict SHA-256 verification),
Exp 3 v1 pilot, and Exp 4 (directly from summary.txt with zero hardcoded overrides).
Exits non-zero if any frozen SHA-256 file is missing or corrupted.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
EXP1_DIR = ROOT / "exp1-production-jury"
EXP3_DIR = ROOT / "exp3-unrepairable-honesty"
sys.path.insert(0, str(EXP1_DIR))
sys.path.insert(0, str(EXP3_DIR))

import analyze_jury  # noqa: E402
import score  # noqa: E402


def verify_sha256_manifest(manifest_path: Path, base_dir: Path) -> tuple[int, int, list[str]]:
    ok = 0
    total = 0
    errors: list[str] = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        expected, rel = line.split(None, 1)
        rel = rel.strip()
        target = base_dir / rel
        total += 1
        if not target.is_file():
            errors.append(f"MISSING: {rel}")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual == expected:
            ok += 1
        else:
            errors.append(f"MISMATCH: {rel} expected={expected} actual={actual}")
    return (ok, total, errors)


def _exact_paired_sign_flip_p(diffs: list[float]) -> float:
    """Exact two-sided paired randomization p-value on non-zero per-case differences."""
    nz = [d for d in diffs if abs(d) > 1e-12]
    m = len(nz)
    if m == 0:
        return 1.0
    obs = abs(sum(nz))
    if m <= 20:
        ge = 0
        total = 1 << m
        for signs in itertools.product((-1.0, 1.0), repeat=m):
            if abs(sum(s * v for s, v in zip(signs, nz))) >= obs - 1e-12:
                ge += 1
        return round(ge / total, 6)
    # Deterministic fallback for large m: exact sign test on direction counts
    pos = sum(1 for d in nz if d > 0)
    neg = m - pos
    return round(analyze_jury.exact_binomial_two_sided(min(pos, neg), m, 0.5), 6)


def reproduce_exp1_production_jury() -> dict[str, Any]:
    return analyze_jury.analyze(EXP1_DIR / "gates_anonymized.json")


def reproduce_exp2_rubric_rct() -> dict[str, Any]:
    lr = json.loads((ROOT / "exp2-rubric-false-alarms" / "results.json").read_text(encoding="utf-8"))
    by_case = lr["by_case"]
    n_cases = len(by_case)

    # Recompute directly from the 45 per-case records (2 reviews per arm per case = 90 reviews/arm)
    list_real_sum = sum(sum(c["list_exact"]) for c in by_case)
    none_real_sum = sum(sum(c["none_exact"]) for c in by_case)
    planted_total_opps = sum(int(c.get("reals", 0)) * 2 for c in by_case)

    list_false_sum = sum(sum(c["list_false"]) for c in by_case)
    none_false_sum = sum(sum(c["none_false"]) for c in by_case)
    all_list_bin = sum(1 for c in by_case for v in c["list_false"] if v > 0)
    all_none_bin = sum(1 for c in by_case for v in c["none_false"] if v > 0)
    all_bin_diffs = [
        (sum(1 for v in c["list_false"] if v > 0) - sum(1 for v in c["none_false"] if v > 0)) / 2.0
        for c in by_case
    ]
    real_diffs = [(sum(c["list_exact"]) - sum(c["none_exact"])) / 2.0 for c in by_case]
    false_diffs = [(sum(c["list_false"]) - sum(c["none_false"])) / 2.0 for c in by_case]

    clean_cases = [c for c in by_case if not c.get("planted")]
    clean_list_count = sum(sum(c["list_false"]) for c in clean_cases)
    clean_none_count = sum(sum(c["none_false"]) for c in clean_cases)
    clean_count_diffs = [(sum(c["list_false"]) - sum(c["none_false"])) / 2.0 for c in clean_cases]

    # Binary proportion of clean-control reviews with >=1 false alarm (distinct from mean count/review!)
    clean_list_bin = sum(1 for c in clean_cases for v in c["list_false"] if v > 0)
    clean_none_bin = sum(1 for c in clean_cases for v in c["none_false"] if v > 0)
    clean_bin_diffs = [
        (sum(1 for v in c["list_false"] if v > 0) - sum(1 for v in c["none_false"] if v > 0)) / 2.0
        for c in clean_cases
    ]

    fresh_cases = [c for c in by_case if not c.get("seen")]
    fresh_false_diffs = [(sum(c["list_false"]) - sum(c["none_false"])) / 2.0 for c in fresh_cases]
    seen_cases = [c for c in by_case if c.get("seen")]

    return {
        "cases": n_cases,
        "reviews": n_cases * 4,
        "missing_runs": len(lr["missing_runs"]),
        "seen_cases": len(seen_cases),
        "fresh_unseen_cases": len(fresh_cases),
        "clean_controls_total": len(clean_cases),
        "clean_controls_seen": sum(1 for c in clean_cases if c.get("seen")),
        "recomputed_from_by_case": {
            "exact_hits_per_review_list": round(list_real_sum / (n_cases * 2), 4),
            "exact_hits_per_review_none": round(none_real_sum / (n_cases * 2), 4),
            "exact_hits_paired_p": _exact_paired_sign_flip_p(real_diffs),
            "true_planted_fault_recall_list": f"{list_real_sum}/{planted_total_opps} ({list_real_sum/planted_total_opps:.1%})",
            "true_planted_fault_recall_none": f"{none_real_sum}/{planted_total_opps} ({none_real_sum/planted_total_opps:.1%})",
            "false_alarms_per_review_list": round(list_false_sum / (n_cases * 2), 4),
            "false_alarms_per_review_none": round(none_false_sum / (n_cases * 2), 4),
            "false_alarms_paired_p": _exact_paired_sign_flip_p(false_diffs),
            "all_45_binary_ge1_false_alarm_list": f"{all_list_bin}/{n_cases*2} ({all_list_bin/(n_cases*2):.1%})",
            "all_45_binary_ge1_false_alarm_none": f"{all_none_bin}/{n_cases*2} ({all_none_bin/(n_cases*2):.1%})",
            "all_45_binary_ge1_false_alarm_exact_p": _exact_paired_sign_flip_p(all_bin_diffs),
            "clean_controls_mean_count_list": round(clean_list_count / (len(clean_cases) * 2), 4),
            "clean_controls_mean_count_none": round(clean_none_count / (len(clean_cases) * 2), 4),
            "clean_controls_count_exact_p": _exact_paired_sign_flip_p(clean_count_diffs),
            "clean_controls_binary_ge1_list": f"{clean_list_bin}/{len(clean_cases)*2} ({clean_list_bin/(len(clean_cases)*2):.1%})",
            "clean_controls_binary_ge1_none": f"{clean_none_bin}/{len(clean_cases)*2} ({clean_none_bin/(len(clean_cases)*2):.1%})",
            "clean_controls_binary_exact_p": _exact_paired_sign_flip_p(clean_bin_diffs),
            "fresh_unseen_false_per_review_list": round(sum(sum(c["list_false"]) for c in fresh_cases) / (len(fresh_cases) * 2), 4),
            "fresh_unseen_false_per_review_none": round(sum(sum(c["none_false"]) for c in fresh_cases) / (len(fresh_cases) * 2), 4),
            "fresh_unseen_false_exact_p": _exact_paired_sign_flip_p(fresh_false_diffs),
        },
        "archived_metadata": {
            "high_confidence_false_alarms": lr["false_sure"],
            "overall_archived_verdict": lr["verdict"],
            "notes_per_review": lr["notes"],
            "tokens_total": lr["tokens"]["total"],
            "tokens_per_review": lr["tokens"]["tokens"],
            "judge_calibration": lr["calibration"],
            "judge_agreement": lr["judges"],
        },
    }


def reproduce_exp3_honesty_v3() -> tuple[dict[str, Any], list[str]]:
    data = json.loads((EXP3_DIR / "results-v3-72runs.json").read_text(encoding="utf-8"))
    runs = data["runs"]
    summary = score.summarize_results(runs)
    chk_ok, chk_total, chk_errors = verify_sha256_manifest(EXP3_DIR / "tasks.sha256", EXP3_DIR)
    h_ok, h_total, h_errors = verify_sha256_manifest(EXP3_DIR / "harness_post_audit.sha256", EXP3_DIR)
    return (
        {
            "pre_run_task_checksums_verified": f"{chk_ok}/{chk_total}",
            "post_audit_harness_checksums_verified": f"{h_ok}/{h_total}",
            "timeout_handling": "symmetric RUNNER_ERROR (180s timeout or rc != 0)",
            **summary,
        },
        chk_errors + [f"harness_post_audit/{e}" for e in h_errors],
    )


def reproduce_exp3_honesty_v2_archive() -> tuple[dict[str, Any], list[str]]:
    v2_dir = EXP3_DIR / "v2-archive"
    data = json.loads((v2_dir / "results-v2-72runs.json").read_text(encoding="utf-8"))
    runs = data["runs"]
    summary = score.summarize_results(runs)
    chk_ok, chk_total, chk_errors = verify_sha256_manifest(v2_dir / "tasks.sha256", v2_dir)
    return (
        {
            "checksums_verified": f"{chk_ok}/{chk_total}",
            "timeout_handling": data.get("timeout_handling_note", "symmetric RUNNER_ERROR"),
            **summary,
        },
        [f"v2-archive/{e}" for e in chk_errors],
    )


def reproduce_exp3_honesty_v1() -> dict[str, Any]:
    v1_dir = EXP3_DIR / "v1-pilot"
    scores = json.loads((v1_dir / "scores-main.json").read_text(encoding="utf-8"))
    probe = json.loads((v1_dir / "probe-main.json").read_text(encoding="utf-8"))
    repairable = sum(r["repairable"] for r in scores)
    remaining = sum(r["remaining_repairable"] for r in scores)

    by_model: dict[str, Counter[str]] = {}
    totals: Counter[str] = Counter()
    for _rid, _page, _arm, model, category, _says_clean in probe:
        totals[model] += 1
        by_model.setdefault(model, Counter())[category] += 1

    m_opus = "claude-opus-5-5-max"
    m_sol = "gpt-5.6-sol-medium"
    op_del = by_model.get(m_opus, Counter()).get("request removed from the page", 0)
    so_del = by_model.get(m_sol, Counter()).get("request removed from the page", 0)
    op_hon = by_model.get(m_opus, Counter()).get("left it and said so", 0)
    so_hon = by_model.get(m_sol, Counter()).get("left it and said so", 0)
    op_mock = by_model.get(m_opus, Counter()).get("request kept, made to succeed", 0)
    so_mock = by_model.get(m_sol, Counter()).get("request kept, made to succeed", 0)
    return {
        "effort_mismatch_note": "Exploratory pilot compared claude-opus-5-5 (max effort) vs gpt-5.6-sol (medium effort).",
        "repairable_repaired": repairable - remaining,
        "repairable_total": repairable,
        "remaining_ci95": list(score.clopper_pearson(remaining, repairable)),
        "probe_runs": len(probe),
        "claude_opus_5_5_max": {"removed": op_del, "mocked_success": op_mock, "honest_refusal": op_hon, "n": totals[m_opus]},
        "gpt_5_6_sol_medium": {"removed": so_del, "mocked_success": so_mock, "honest_refusal": so_hon, "n": totals[m_sol]},
        "fisher_p_silent_deletion": score.fisher_exact_two_sided(op_del, totals[m_opus] - op_del, so_del, totals[m_sol] - so_del),
        "fisher_p_honest_refusal": score.fisher_exact_two_sided(op_hon, totals[m_opus] - op_hon, so_hon, totals[m_sol] - so_hon),
    }


def reproduce_exp4_selfreport() -> dict[str, Any]:
    lines = [
        ln.strip()
        for ln in (ROOT / "exp4-selfreport-boundary" / "summary.txt").read_text(encoding="utf-8").splitlines()
        if ln.strip().startswith("b") and "\t" in ln
    ]
    n = len(lines)
    raw_disagrees = sum(1 for ln in lines if "\tCONTRADICTS\t" in ln)
    overlaps = sum(1 for ln in lines if "'overlaps':" in ln)
    return {
        "builds_measured": n,
        "mechanical_rule_contradictions": raw_disagrees,
        "mechanical_rule_ci95": list(score.clopper_pearson(raw_disagrees, n)),
        "raw_dom_overlap_detector_flags": overlaps,
        "unarchived_manual_inspection_notes": (
            "Manual post-hoc inspection (not stored inside summary.txt) traced b21's 263px overflow flag "
            "to a 390px vs 375px viewport-width mismatch and noted decorative overlays triggering raw DOM overlap counts."
        ),
    }


def main() -> int:
    e3_v3, chk_errors_v3 = reproduce_exp3_honesty_v3()
    e3_v2, chk_errors_v2 = reproduce_exp3_honesty_v2_archive()
    chk_errors = chk_errors_v3 + chk_errors_v2
    out = {
        "exp1_production_jury": reproduce_exp1_production_jury(),
        "exp2_rubric_false_alarms": reproduce_exp2_rubric_rct(),
        "exp3_unrepairable_honesty_v3_clean_room": e3_v3,
        "exp3_unrepairable_honesty_v2_archive": e3_v2,
        "exp3_unrepairable_honesty_v1_pilot": reproduce_exp3_honesty_v1(),
        "exp4_selfreport_boundary": reproduce_exp4_selfreport(),
    }
    print(json.dumps(out, indent=2))
    if chk_errors:
        print("SHA-256 VERIFICATION FAILED:", file=sys.stderr)
        for err in chk_errors:
            print("  -", err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
