"""Comparison design of HiMat (Wang et al., Eurographics 2026): outputs whose native grids differ are upsampled to 4096 and compared by GLCM Score.

Usage: uv run python experiments/glcm_native_grid.py
Conditions: experiments/conditions/glcm_native_grid.json (fixed and committed before the computation)
Output: results/glcm_native_grid.json (aggregated by experiments/grid_compare_report.py)

This is a reproduction on synthetic surfaces; no claim is made about its bearing on the conclusions of HiMat.
"""

from __future__ import annotations

import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from atact.gridcompare import (field_and_grad, glcm_score, height_scale, normals_from_grad,
                               shade_gray, upsample)

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "glcm_native_grid.json"
OUT = ROOT / "results"
RMS_SLOPE = 0.3


def run_one(job):
    s, seed, n, methods, render_n = job
    h0 = height_scale(s["f"], s["octaves"], RMS_SLOPE)
    _, fx, fy = field_and_grad(s["f"], s["octaves"], n, seed, max_freq=n / 4)
    grad = h0 * np.stack([fx, fy], axis=-1)
    out = []
    for m in (methods if n != render_n else ["native"]):
        g = upsample(grad, render_n, m) if n != render_n else grad
        gray = shade_gray(normals_from_grad(g[..., 0], g[..., 1]))
        out.append({"surface": s["name"], "seed": seed, "N": n, "method": m, "glcm": glcm_score(gray)})
    return out


def main():
    cond = json.loads(COND.read_text())
    methods = [u["name"] for u in cond["upsampling"]]
    jobs = [(s, seed, n, methods, cond["render_N"]) for s in cond["surfaces"]
            for seed in cond["seeds"] for n in cond["native_N"]]
    with ProcessPoolExecutor() as ex:
        rows = [r for part in ex.map(run_one, jobs) for r in part]
    OUT.mkdir(exist_ok=True)
    meta = {"conditions_sha256": hashlib.sha256(COND.read_bytes()).hexdigest(), "numpy": np.__version__}
    (OUT / "glcm_native_grid.json").write_text(json.dumps({"meta": meta, "rows": rows}))
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
