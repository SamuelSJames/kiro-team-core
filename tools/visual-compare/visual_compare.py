#!/usr/bin/env python3
"""visual-compare — deterministic visual fidelity comparison.

Compares an approved visual reference against an implementation screenshot and
produces a deterministic fidelity score (0.00–100.00), PASS/FAIL against a
threshold, per-metric scores, machine-readable JSON, and two diff images.

Deterministic by construction: no network, no AI inference, no randomness.
Fixed metric weights (not runtime-configurable):
    fidelity = ssim*0.50 + pixel_similarity*0.30 + edge_similarity*0.20

Exit codes:
    0  comparison completed AND passed threshold
    1  comparison completed BUT failed threshold (incl. dimension mismatch)
    2  invalid input / processing failure
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFile, UnidentifiedImageError
from scipy import ndimage
from skimage.metrics import structural_similarity as ssim

# ---- fixed, non-overridable scoring weights ----
WEIGHTS = {"ssim": 0.50, "pixel_similarity": 0.30, "edge_similarity": 0.20}
DEFAULT_THRESHOLD = 92.0

# ---- decompression-bomb / sanity guards ----
# Pillow's default MAX_IMAGE_PIXELS is ~89M; keep a strict explicit cap and never
# process absurd dimensions. 50 MP (~ up to 8K*6K) is generous for UI screenshots.
MAX_PIXELS = 50_000_000
MAX_EDGE = 20_000  # no single side larger than this
Image.MAX_IMAGE_PIXELS = MAX_PIXELS
# refuse truncated files rather than silently loading partial data
ImageFile.LOAD_TRUNCATED_IMAGES = False

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2


class ProcessingError(Exception):
    """Invalid input or unprocessable image — maps to exit code 2."""


def _load_rgb(path_str: str, label: str) -> tuple[np.ndarray, tuple[int, int]]:
    """Load an image, flatten alpha over white, return (H,W,3) uint8 + (w,h).

    Never mutates the source file.
    """
    p = Path(path_str)
    if not p.is_file():
        raise ProcessingError(f"{label} image not found: {path_str}")
    try:
        with Image.open(p) as im:
            im.verify()  # cheap integrity check; closes the file
    except (UnidentifiedImageError, OSError, ValueError) as e:
        raise ProcessingError(f"{label} is not a readable/valid image: {e}")
    try:
        with Image.open(p) as im:
            w, h = im.size
            if w <= 0 or h <= 0:
                raise ProcessingError(f"{label} has invalid dimensions {w}x{h}")
            if w > MAX_EDGE or h > MAX_EDGE or (w * h) > MAX_PIXELS:
                raise ProcessingError(
                    f"{label} exceeds safe size limits ({w}x{h}; "
                    f"max {MAX_EDGE}px/side, {MAX_PIXELS} total px)"
                )
            if im.mode in ("RGBA", "LA") or (
                im.mode == "P" and "transparency" in im.info
            ):
                rgba = im.convert("RGBA")
                bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
                im = Image.alpha_composite(bg, rgba).convert("RGB")
            else:
                im = im.convert("RGB")
            arr = np.asarray(im, dtype=np.uint8)
    except ProcessingError:
        raise
    except (UnidentifiedImageError, OSError, ValueError) as e:
        raise ProcessingError(f"{label} could not be decoded: {e}")
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise ProcessingError(f"{label} did not convert to RGB cleanly")
    return arr, (w, h)


def _sobel_edges(gray: np.ndarray) -> np.ndarray:
    """Deterministic Sobel edge magnitude, normalized to [0,1] float64."""
    gx = ndimage.sobel(gray, axis=1, mode="reflect")
    gy = ndimage.sobel(gray, axis=0, mode="reflect")
    mag = np.hypot(gx, gy)
    peak = mag.max()
    if peak > 0:
        mag = mag / peak
    return mag


def _metrics(ref: np.ndarray, act: np.ndarray) -> dict[str, float]:
    """Compute the three deterministic metrics at full float precision."""
    ref_f = ref.astype(np.float64)
    act_f = act.astype(np.float64)

    s = ssim(ref, act, channel_axis=2, data_range=255)
    ssim_score = float(np.clip(s, 0.0, 1.0)) * 100.0

    mad = np.mean(np.abs(ref_f - act_f)) / 255.0
    pixel_score = (1.0 - mad) * 100.0

    luma = np.array([0.299, 0.587, 0.114], dtype=np.float64)
    ref_gray = ref_f @ luma
    act_gray = act_f @ luma
    ref_edges = _sobel_edges(ref_gray)
    act_edges = _sobel_edges(act_gray)
    edge_diff = np.mean(np.abs(ref_edges - act_edges))
    edge_score = (1.0 - float(edge_diff)) * 100.0

    return {
        "ssim": ssim_score,
        "pixel_similarity": pixel_score,
        "edge_similarity": edge_score,
    }


def _write_diffs(ref: np.ndarray, act: np.ndarray, out_dir: Path) -> None:
    """Write diff.png and diff-amplified.png."""
    diff = np.abs(ref.astype(np.int16) - act.astype(np.int16)).astype(np.uint8)
    Image.fromarray(diff, mode="RGB").save(out_dir / "diff.png")

    mag = diff.max(axis=2).astype(np.float64)
    peak = mag.max()
    if peak > 0:
        amp = (mag / peak) * 255.0
    else:
        amp = mag
    amp_u8 = amp.astype(np.uint8)
    Image.fromarray(amp_u8, mode="L").save(out_dir / "diff-amplified.png")


def compare(reference: str, actual: str, threshold: float, output_dir: str) -> dict:
    """Run the full comparison."""
    ref_arr, ref_dim = _load_rgb(reference, "reference")
    act_arr, act_dim = _load_rgb(actual, "actual")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    dimensions_match = ref_dim == act_dim
    result: dict = {
        "reference": str(Path(reference)),
        "actual": str(Path(actual)),
        "reference_dimensions": [ref_dim[0], ref_dim[1]],
        "actual_dimensions": [act_dim[0], act_dim[1]],
        "dimensions_match": dimensions_match,
        "weights": {k: round(v, 2) for k, v in WEIGHTS.items()},
        "threshold": round(float(threshold), 2),
    }

    if not dimensions_match:
        result.update(
            {
                "metrics": {"ssim": None, "pixel_similarity": None, "edge_similarity": None},
                "fidelity_score": 0.0,
                "passed": False,
                "error": (
                    "dimension mismatch: reference is "
                    f"{ref_dim[0]}x{ref_dim[1]}, actual is {act_dim[0]}x{act_dim[1]}. "
                    "Capture both at the same canonical viewport; this tool will "
                    "not resize images to make them match."
                ),
            }
        )
        _write_placeholder_diffs(out)
        _write_json(out, result)
        return result

    metrics = _metrics(ref_arr, act_arr)
    fidelity = (
        metrics["ssim"] * WEIGHTS["ssim"]
        + metrics["pixel_similarity"] * WEIGHTS["pixel_similarity"]
        + metrics["edge_similarity"] * WEIGHTS["edge_similarity"]
    )
    passed = fidelity >= threshold

    result["metrics"] = {k: round(v, 2) for k, v in metrics.items()}
    result["fidelity_score"] = round(fidelity, 2)
    result["passed"] = bool(passed)

    _write_diffs(ref_arr, act_arr, out)
    _write_json(out, result)
    return result


def _write_placeholder_diffs(out: Path) -> None:
    blank = Image.new("RGB", (1, 1), (0, 0, 0))
    blank.save(out / "diff.png")
    Image.new("L", (1, 1), 0).save(out / "diff-amplified.png")


def _write_json(out: Path, result: dict) -> None:
    (out / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")


def _human_report(r: dict) -> str:
    lines = []
    lines.append("visual-compare")
    lines.append(f"  reference : {r['reference']} {tuple(r['reference_dimensions'])}")
    lines.append(f"  actual    : {r['actual']} {tuple(r['actual_dimensions'])}")
    if not r["dimensions_match"]:
        lines.append("  RESULT    : FAIL (dimension mismatch)")
        lines.append(f"  error     : {r['error']}")
        return "\n".join(lines)
    m = r["metrics"]
    lines.append(f"  ssim             : {m['ssim']:.2f}  (w {r['weights']['ssim']:.2f})")
    lines.append(f"  pixel_similarity : {m['pixel_similarity']:.2f}  (w {r['weights']['pixel_similarity']:.2f})")
    lines.append(f"  edge_similarity  : {m['edge_similarity']:.2f}  (w {r['weights']['edge_similarity']:.2f})")
    lines.append(f"  fidelity_score   : {r['fidelity_score']:.2f}")
    lines.append(f"  threshold        : {r['threshold']:.2f}")
    lines.append(f"  RESULT    : {'PASS' if r['passed'] else 'FAIL'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="visual-compare",
        description="Deterministic visual fidelity comparison (SSIM + pixel + edge).",
    )
    ap.add_argument("--reference", required=True, help="approved reference image path")
    ap.add_argument("--actual", required=True, help="implementation screenshot path")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help=f"pass threshold 0-100 (default {DEFAULT_THRESHOLD})")
    ap.add_argument("--output-dir", default="./visual-comparison",
                    help="output directory (default ./visual-comparison)")
    ap.add_argument("--json", action="store_true", help="print JSON result to stdout")
    ap.add_argument("--quiet", action="store_true", help="suppress human-readable text")
    args = ap.parse_args(argv)

    if not (0.0 <= args.threshold <= 100.0):
        print("error: --threshold must be between 0 and 100", file=sys.stderr)
        return EXIT_ERROR

    try:
        result = compare(args.reference, args.actual, args.threshold, args.output_dir)
    except ProcessingError as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT_ERROR
    except Exception as e:
        print(f"error: unexpected processing failure: {type(e).__name__}: {e}",
              file=sys.stderr)
        return EXIT_ERROR

    if args.json:
        print(json.dumps(result, indent=2))
    if not args.quiet:
        stream = sys.stderr if args.json else sys.stdout
        print(_human_report(result), file=stream)

    return EXIT_PASS if result["passed"] else EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
