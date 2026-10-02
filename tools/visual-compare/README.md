# visual-compare

Deterministic visual fidelity comparison CLI. Compares an **approved reference**
against an **implementation screenshot** and emits a fidelity score (0.00–100.00),
PASS/FAIL vs a threshold, per-metric scores, machine-readable JSON, and diff images.

No network. No AI inference. No randomness. No telemetry. No secrets.

## Install location

```
~/.kiro/tools/visual-compare/      # source + dedicated uv venv (.venv)
  visual_compare.py
  pyproject.toml
  README.md
  tests/
~/.local/bin/visual-compare        # shim -> runs the tool in its own venv
```

The tool runs entirely inside `~/.kiro/tools/visual-compare/.venv` (created with
`uv`), so it never pollutes system Python.

## Usage

```
visual-compare \
  --reference approved-mockup.png \
  --actual implementation.png \
  --threshold 92 \
  --output-dir ./visual-comparison
```

| Flag | Required | Default | Meaning |
|------|----------|---------|---------|
| `--reference PATH` | yes | — | approved reference image |
| `--actual PATH` | yes | — | implementation screenshot |
| `--threshold FLOAT` | no | `92.0` | pass if `fidelity_score >= threshold` |
| `--output-dir PATH` | no | `./visual-comparison` | where outputs are written |
| `--json` | no | off | print JSON result to **stdout** |
| `--quiet` | no | off | suppress the human-readable report |

With `--json`, JSON goes to stdout and the human report (unless `--quiet`) goes to
stderr, so stdout stays clean for machine parsing.

## Metrics & score

| Metric | How | Normalization |
|--------|-----|---------------|
| `ssim` | `skimage.metrics.structural_similarity` per-channel, `data_range=255` | ×100 |
| `pixel_similarity` | `1 - mean(|refRGB - actRGB|)/255` | ×100 |
| `edge_similarity` | Sobel edge magnitude (scipy.ndimage) on fixed-luma grayscale, `1 - mean(|edgeRef - edgeAct|)` | ×100 |

**Fixed weighted score (not runtime-configurable):**

```
fidelity_score = ssim*0.50 + pixel_similarity*0.30 + edge_similarity*0.20
```

Scores are computed at full float precision and **reported** rounded to 2 decimals.
PASS when `fidelity_score >= threshold`.

## Dimensions: no silent resizing

Images are compared at identical dimensions. If dimensions differ, the tool does
**not** resize. Instead it sets `dimensions_match=false`, reports both sizes, writes
an `error`, and **fails the gate** (exit 1). Capture the mockup and the Playwright
screenshot at the same canonical viewport.

## Output

```
<output-dir>/
  comparison.json      # machine-readable result (schema below)
  diff.png             # absolute RGB difference
  diff-amplified.png   # contrast-stretched difference magnitude (grayscale, white=max)
```

### comparison.json

```json
{
  "reference": "approved-mockup.png",
  "actual": "implementation.png",
  "reference_dimensions": [1280, 800],
  "actual_dimensions": [1280, 800],
  "dimensions_match": true,
  "weights": {"ssim": 0.5, "pixel_similarity": 0.3, "edge_similarity": 0.2},
  "threshold": 92.0,
  "metrics": {"ssim": 99.45, "pixel_similarity": 98.95, "edge_similarity": 99.87},
  "fidelity_score": 99.39,
  "passed": true
}
```

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | comparison completed **and** passed threshold |
| `1` | comparison completed **but** failed threshold (incl. dimension mismatch) |
| `2` | invalid input / processing failure (missing/corrupt/oversized image, bad args) |

A fidelity FAIL is a successful comparison (exit 1), not a crash.

## Safety

- Source images are never modified.
- Corrupt/unreadable files are refused cleanly (exit 2).
- Alpha channels are flattened deterministically over white before comparison.
- Decompression-bomb guard: max 50,000,000 px and 20,000 px/side.
- Only `comparison.json`, `diff.png`, `diff-amplified.png` are written, into `--output-dir`.

## Dependencies (pinned)

`numpy==2.1.3`, `pillow==11.0.0`, `scikit-image==0.24.0`, `scipy==1.14.1`
(+ `pytest==8.3.3` for tests). Python >= 3.12.

> OpenCV was intentionally **not** used — it wasn't present and scipy's Sobel is a
> smaller, deterministic dependency that fully covers the edge metric.

## Tests

```
~/.kiro/tools/visual-compare/.venv/bin/python -m pytest tests/ -v
```

Covers: identical (~100), changed rectangle, shifted component, slight color change,
dimension mismatch (hard fail), corrupt file (error), alpha flattening, run-to-run
determinism, and CLI exit codes 0/1/2.
