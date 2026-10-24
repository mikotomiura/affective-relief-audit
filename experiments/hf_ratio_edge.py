"""Gao ら（2026）の HF ratio が、同じ表面の切り出し位置（端の跳び）と格子でどれだけ動くか。

使い方: uv run python experiments/hf_ratio_edge.py
条件: experiments/conditions/hf_ratio_edge.json（計算の前に固定してコミットした）
出力: results/hf_ratio_edge.json と results/hf_ratio_edge.md

合成した表面での感度の確認であり、Gao らの比較（表 1）の結論への影響は主張しない。
"""

from __future__ import annotations

import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from atact.field import RenderConfig, _draw
from atact.hfratio import hann2d, hf_ratio, normal_rgb_from_height
from atact.transform import t_gamma

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "hf_ratio_edge.json"
OUT = ROOT / "results"
H0 = 0.01


def field(f: float, octaves: int, n: int, seed: int, x0: float, y0: float) -> np.ndarray:
    """窓 [x0, x0+1) x [y0, y0+1) の上の場。位相の引き方は atact.field.procedural_field と同じ。"""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:n, 0:n] / n
    x, y = x + x0, y + y0
    F = np.zeros((n, n))
    cfg = RenderConfig()
    for o in range(octaves):
        fo, a = f * 2**o, 0.5**o
        (px, py), _ = _draw(rng, cfg)
        F += a * np.sin(2 * np.pi * fo * x + px) * np.sin(2 * np.pi * fo * y + py)
    return F / sum(0.5**o for o in range(octaves))


def windowed(rgb: np.ndarray) -> np.ndarray:
    v = rgb.astype(float) / 255 * 2 - 1
    m = v.reshape(-1, 3).mean(0)
    v = m + (v - m) * hann2d(v.shape[0])[..., None]
    v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    return np.round((v + 1) / 2 * 255).astype(np.uint8)


def run_one(job):
    s, seed, n, (x0, y0) = job
    z = H0 * t_gamma(field(s["f"], s["octaves"], n, seed, x0, y0), s["gamma"])
    rgb = normal_rgb_from_height(z)
    rgbw = windowed(rgb)
    out = []
    for cut, thr in (("px120", 120.0), ("phys", 120.0 * n / 1024)):
        for proc, img in (("raw", rgb), ("hann", rgbw)):
            out.append({"surface": s["name"], "seed": seed, "N": n, "offset": [x0, y0],
                        "cutoff": cut, "processing": proc, "hf_ratio": hf_ratio(img, thr)})
    return out


def main():
    cond = json.loads(COND.read_text())
    jobs = [(s, seed, n, tuple(off)) for s in cond["surfaces"] for seed in cond["seeds"]
            for n in cond["grids_N"] for off in cond["crop_offsets"]]
    with ProcessPoolExecutor() as ex:
        rows = [r for part in ex.map(run_one, jobs, chunksize=4) for r in part]
    OUT.mkdir(exist_ok=True)
    meta = {"conditions_sha256": hashlib.sha256(COND.read_bytes()).hexdigest(), "numpy": np.__version__}
    (OUT / "hf_ratio_edge.json").write_text(json.dumps({"meta": meta, "rows": rows}))
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
