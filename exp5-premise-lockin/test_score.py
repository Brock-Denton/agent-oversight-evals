#!/usr/bin/env python3
"""Unit tests for exp5-premise-lockin score.py & run_exp5.py parsers."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import run_exp5  # noqa: E402
import score  # noqa: E402


class TestExp5Scoring(unittest.TestCase):
    def test_sha256_manifest_passes(self) -> None:
        ok, total, errs = score.verify_sha256_manifest(ROOT, "scenarios.sha256")
        self.assertEqual(errs, [])
        self.assertEqual(ok, total)
        self.assertEqual(total, 50)

    def test_extract_last_json_object_prefers_last_valid_match(self) -> None:
        text = (
            'Intro prose with fake {"verdict": "PASS"} earlier.\n'
            'Final JSON:\n'
            '{"verdict": "BLOCKED", "fatal_issues": ["Unresolved Stage 0 trade-off"], '
            '"major_issues": [], "one_line_reason": "Needs human pick."}\n'
        )
        obj = run_exp5.extract_last_json_object(text, ("verdict",))
        self.assertIsNotNone(obj)
        assert obj is not None
        self.assertEqual(obj["verdict"], "BLOCKED")

    def test_exact_stats_sanity(self) -> None:
        self.assertEqual(score.exact_mcnemar_p(0, 0), 1.0)
        self.assertAlmostEqual(score.exact_mcnemar_p(5, 0), 0.0625, places=4)
        self.assertLess(score.exact_fisher_2x2(18, 0, 1, 35), 1e-10)
        lo, hi = score.clopper_pearson_ci(0, 12)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.2646, places=3)

    def test_orthogonality_jaccard(self) -> None:
        identical = [
            {"id": "A", "title": "Pre-bill ICD audit", "core_mechanism": "Parse discharge summaries for coders"},
            {"id": "B", "title": "Pre-bill ICD audit console", "core_mechanism": "Parse discharge summaries for coders"},
        ]
        distinct = [
            {"id": "A", "title": "Pre-bill ICD audit", "core_mechanism": "Nightly billing coder review queue"},
            {"id": "B", "title": "Bedside nurse handoff", "core_mechanism": "Live HL7 override alert ranker"},
            {"id": "C", "title": "Offline alarm governance", "core_mechanism": "Weekly threshold calibration report"},
        ]
        self.assertGreater(score.framing_orthogonality_jaccard(identical), 0.7)
        self.assertLess(score.framing_orthogonality_jaccard(distinct), 0.2)

    def test_end_to_end_synthetic_scoring(self) -> None:
        manifest = json.loads((ROOT / "scenarios_manifest.json").read_text(encoding="utf-8"))
        runs = []
        fams = ["claude", "codex", "gemini"]
        for s in manifest["explicit_controls"]:
            for f in fams:
                runs.append({
                    "family": f, "model_id": f, "scenario": s["id"], "condition": "ctrl_explicit_wrong",
                    "status": "OK",
                    "parsed": {"verdict": "BLOCKED", "fatal_issues": ["Explicitly excluded"], "major_issues": [], "one_line_reason": "Wrong goal"},
                })
        for s in manifest["underspecified_scenarios"]:
            for f in fams:
                runs.append({
                    "family": f, "model_id": f, "scenario": s["id"], "condition": "arm1_unresolved",
                    "status": "OK",
                    "parsed": {"verdict": "PASS", "fatal_issues": [], "major_issues": [], "one_line_reason": "Clean spec"},
                })
                runs.append({
                    "family": f, "model_id": f, "scenario": s["id"], "condition": "arm2_unresolved",
                    "status": "OK",
                    "parsed": {"verdict": "BLOCKED", "fatal_issues": ["Unresolved Stage 0 trade-off"], "major_issues": [], "one_line_reason": "Needs sign-off"},
                })
                runs.append({
                    "family": f, "model_id": f, "scenario": s["id"], "condition": "arm2_resolved_ctrl",
                    "status": "OK",
                    "parsed": {"verdict": "PASS", "fatal_issues": [], "major_issues": [], "one_line_reason": "Signed off"},
                })
                runs.append({
                    "family": f, "model_id": f, "scenario": s["id"], "condition": "arm3a_single_best",
                    "status": "OK",
                    "parsed": {"chosen_asset": "Asset_B" if f == "claude" else "Asset_A", "title": s["asset_a_label"], "one_line_reason": "Test"},
                })
                runs.append({
                    "family": f, "model_id": f, "scenario": s["id"], "condition": "arm3b_stage0_slate",
                    "status": "OK",
                    "parsed": {
                        "framings": [
                            {"id": "A", "title": s["asset_a_label"], "primary_asset": "Asset_A", "core_mechanism": " ".join(s["asset_a_keywords"][:3]), "deferred": "B"},
                            {"id": "B", "title": s["asset_b_label"], "primary_asset": "Asset_B", "core_mechanism": " ".join(s["asset_b_keywords"][:3]), "deferred": "A"},
                            {"id": "C", "title": "Thin Diagnostic Pilot", "primary_asset": "Hybrid", "core_mechanism": "Read-only baseline telemetry audit", "deferred": "Full build"},
                        ],
                        "recommended": "A",
                        "rationale": "Asset A is 85% ready",
                    },
                })
        with tempfile.TemporaryDirectory() as td:
            rp = Path(td) / "runs.json"
            rp.write_text(json.dumps({"models": {"claude": "c", "codex": "o", "gemini": "g"}, "runs": runs}), encoding="utf-8")
            out = score.score_results(rp, None, ROOT)
            self.assertEqual(out["regime1_explicit_control"]["pooled"]["blocked"]["k"], 18)
            self.assertEqual(out["arm1_unresolved_standard"]["pooled"]["pass"]["k"], 36)
            self.assertNotIn("ci95", out["arm1_unresolved_standard"]["pooled"]["pass"])
            self.assertIn("ci95", out["arm1_unresolved_standard"]["by_family"]["claude"]["pass"])
            self.assertEqual(out["arm1_unresolved_standard"]["escalation_audit"]["asked_human_signoff_on_ab"]["k"], 0)
            self.assertEqual(out["spec_review_vs_goal_selection"]["model_preferred_asset_b_in_arm3a"], 12)
            self.assertEqual(out["spec_review_vs_goal_selection"]["pref_b_stamped_pass_on_spec_a_in_arm1"]["k"], 12)
            self.assertEqual(out["spec_review_vs_goal_selection"]["pref_a_did_not_block_spec_a_in_arm1"]["k"], 24)
            self.assertAlmostEqual(out["dossier_level_primary_inference"]["arm1_vs_arm2_unresolved_dossier_sign"]["exact_sign_p"], 0.000488, places=5)
            self.assertLessEqual(out["dossier_level_primary_inference"]["arm1_vs_arm2_unresolved_dossier_sign"]["holm_adjusted_p"], 0.01)
            self.assertEqual(out["arm2_escalation_prompt"]["discrimination"]["balanced_accuracy_block"], 1.0)
            self.assertEqual(out["arm3b_stage0_orthogonal"]["pooled"]["slate_covers_both_a_and_b_self"]["k"], 36)


if __name__ == "__main__":
    unittest.main()
