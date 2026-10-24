"""Gao ら 2026 の継ぎ目の評価の型: 1024 の法線の図の縮小（Resize）と中央の切り出し（Crop）を比べる。

使い方: uv run python experiments/tile_seam_grid.py
条件: experiments/conditions/tile_seam_grid.json（計算の前に固定してコミットした）
出力: results/tile_seam_grid.json（集計は experiments/grid_compare_report.py）

合成した表面での再現であり、Gao らの結論への影響は主張しない。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from atact.gridcompare import (center_crop, field_and_grad, height_scale, normals_from_grad,
                               resize_lanczos, seam_metrics, to_rgb_u8)

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "tile_seam_grid.json"
OUT = ROOT / "results"
RMS_SLOPE = 0.3


def run(kind, fs, octaves, offsets, seeds, src, tgt):
    rows = []
    for f in fs:
        h0 = height_scale(f, octaves, RMS_SLOPE)
        for seed in seeds:
            for x0, y0 in offsets:
                _, fx, fy = field_and_grad(f, octaves, src, seed, x0, y0)
                rgb = to_rgb_u8(normals_from_grad(h0 * fx, h0 * fy))
                for name, img in (("resize", resize_lanczos(rgb, tgt)), ("crop", center_crop(rgb, tgt))):
                    rows.append({"kind": kind, "f": f, "seed": seed, "offset": [x0, y0], "method": name,
                                 **seam_metrics(img)})
    return rows


def main():
    c = json.loads(COND.read_text())
    np_ = c["surfaces_nonperiodic"]
    p_ = c["surfaces_periodic"]
    rows = run("nonperiodic", np_["f"], np_["octaves"], c["crop_offsets"], c["seeds"], c["source_N"], c["target_N"])
    rows += run("periodic", p_["f"], p_["octaves"], c["periodic_offsets"], c["seeds"], c["source_N"], c["target_N"])
    OUT.mkdir(exist_ok=True)
    meta = {"conditions_sha256": hashlib.sha256(COND.read_bytes()).hexdigest(), "numpy": np.__version__}
    (OUT / "tile_seam_grid.json").write_text(json.dumps({"meta": meta, "rows": rows}))
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
