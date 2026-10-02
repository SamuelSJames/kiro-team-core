"""Deterministic tests for visual-compare.

Fixtures are generated programmatically (no binary assets committed). Each test
asserts on the relationship between scores, not brittle absolute values, except
where the spec pins an expectation (identical ~100, dimension mismatch hard-fail,
corrupt file -> processing error). Also verifies run-to-run determinism.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import visual_compare as vc

W, H = 200, 150


def _save(arr: np.ndarray, path: Path) -> Path:
    Image.fromarray(arr.astype(np.uint8), mode="RGB").save(path)
    return path


def _base() -> np.ndarray:
    """A deterministic non-trivial scene: white bg, a filled rect, a line."""
    a = np.full((H, W, 3), 255, dtype=np.uint8)
    a[30:90, 40:120] = (40, 90, 200)      # blue rectangle
    a[100:105, 10:190] = (0, 0, 0)        # black horizontal line
    return a


def test_identical_approx_100(tmp_path: Path):
    img = _save(_base(), tmp_path / "ref.png")
    r = vc.compare(str(img), str(img), 92.0, str(tmp_path / "out"))
    assert r["dimensions_match"] is True
    assert r["fidelity_score"] >= 99.99
    assert r["passed"] is True
    assert r["metrics"]["ssim"] >= 99.99
    assert r["metrics"]["pixel_similarity"] >= 99.99
    assert r["metrics"]["edge_similarity"] >= 99.99
    # diff images exist
    assert (tmp_path / "out" / "diff.png").is_file()
    assert (tmp_path / "out" / "diff-amplified.png").is_file()
    assert (tmp_path / "out" / "comparison.json").is_file()


def test_changed_rectangle_below_identical(tmp_path: Path):
    ref = _save(_base(), tmp_path / "ref.png")
    b = _base()
    b[30:90, 40:120] = (200, 60, 40)  # recolor the rectangle (obvious change)
    act = _save(b, tmp_path / "act.png")
    r = vc.compare(str(ref), str(act), 92.0, str(tmp_path / "out"))
    assert r["fidelity_score"] < 100.0
    # a big block recolor should move the score meaningfully
    assert r["fidelity_score"] < 99.0


def test_shifted_component_lowers_structural_and_edge(tmp_path: Path):
    ref = _save(_base(), tmp_path / "ref.png")
    b = np.full((H, W, 3), 255, dtype=np.uint8)
    b[30:90, 70:150] = (40, 90, 200)   # same rect shifted right by 30px
    b[100:105, 10:190] = (0, 0, 0)
    act = _save(b, tmp_path / "act.png")
    r = vc.compare(str(ref), str(act), 92.0, str(tmp_path / "out"))
    ident = vc.compare(str(ref), str(ref), 92.0, str(tmp_path / "out2"))
    assert r["metrics"]["ssim"] < ident["metrics"]["ssim"]
    assert r["metrics"]["edge_similarity"] < ident["metrics"]["edge_similarity"]


def test_slight_color_change_measurable_pixel_diff(tmp_path: Path):
    ref = _save(_base(), tmp_path / "ref.png")
    b = _base().astype(np.int16)
    b[30:90, 40:120] += 12  # nudge the rectangle color slightly
    act = _save(np.clip(b, 0, 255).astype(np.uint8), tmp_path / "act.png")
    r = vc.compare(str(ref), str(act), 92.0, str(tmp_path / "out"))
    assert r["metrics"]["pixel_similarity"] < 100.0
    assert r["metrics"]["pixel_similarity"] > 95.0  # only a small nudge


def test_dimension_mismatch_hard_fail(tmp_path: Path):
    ref = _save(_base(), tmp_path / "ref.png")
    small = _save(_base()[:, :100], tmp_path / "act.png")  # 100x150
    r = vc.compare(str(ref), str(small), 92.0, str(tmp_path / "out"))
    assert r["dimensions_match"] is False
    assert r["passed"] is False
    assert r["fidelity_score"] == 0.0
    assert "dimension mismatch" in r["error"]
    assert r["reference_dimensions"] == [W, H]
    assert r["actual_dimensions"] == [100, H]


def test_corrupt_file_raises_processing_error(tmp_path: Path):
    bad = tmp_path / "bad.png"
    bad.write_bytes(b"\x89PNG\r\n\x1a\n not a real png at all")
    try:
        vc.compare(str(bad), str(bad), 92.0, str(tmp_path / "out"))
    except vc.ProcessingError:
        return
    raise AssertionError("expected ProcessingError for corrupt file")


def test_alpha_flattened_safely(tmp_path: Path):
    # RGBA with transparency must flatten over white, not crash
    rgba = np.zeros((H, W, 4), dtype=np.uint8)
    rgba[..., 3] = 0  # fully transparent
    p = tmp_path / "a.png"
    Image.fromarray(rgba, mode="RGBA").save(p)
    white = _save(np.full((H, W, 3), 255, dtype=np.uint8), tmp_path / "white.png")
    r = vc.compare(str(p), str(white), 92.0, str(tmp_path / "out"))
    # transparent-over-white == white, so near identical
    assert r["fidelity_score"] >= 99.0


def test_determinism_identical_runs(tmp_path: Path):
    ref = _save(_base(), tmp_path / "ref.png")
    b = _base()
    b[30:90, 40:120] = (200, 60, 40)
    act = _save(b, tmp_path / "act.png")
    r1 = vc.compare(str(ref), str(act), 92.0, str(tmp_path / "o1"))
    r2 = vc.compare(str(ref), str(act), 92.0, str(tmp_path / "o2"))
    assert r1["metrics"] == r2["metrics"]
    assert r1["fidelity_score"] == r2["fidelity_score"]


def test_cli_exit_codes(tmp_path: Path):
    """Exercise the real CLI entrypoint for exit codes 0/1/2."""
    ref = _save(_base(), tmp_path / "ref.png")
    b = _base()
    b[30:90, 40:120] = (200, 60, 40)
    act = _save(b, tmp_path / "act.png")

    def run(args):
        return subprocess.run(
            [sys.executable, str(Path(vc.__file__)), *args],
            capture_output=True, text=True,
        )

    # pass (identical, threshold 0) -> 0
    cp = run(["--reference", str(ref), "--actual", str(ref),
              "--threshold", "0", "--output-dir", str(tmp_path / "p"), "--json"])
    assert cp.returncode == 0
    assert json.loads(cp.stdout)["passed"] is True

    # fail threshold (changed, threshold 100) -> 1
    cp = run(["--reference", str(ref), "--actual", str(act),
              "--threshold", "100", "--output-dir", str(tmp_path / "f")])
    assert cp.returncode == 1

    # invalid input (missing file) -> 2
    cp = run(["--reference", str(tmp_path / "nope.png"), "--actual", str(ref),
              "--output-dir", str(tmp_path / "e")])
    assert cp.returncode == 2
