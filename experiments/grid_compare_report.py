"""results/glcm_native_grid.json と results/tile_seam_grid.json から集計の表を書く。

使い方: uv run python experiments/grid_compare_report.py
出力: results/grid_compare.md
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def mse(v):
    v = np.asarray(v, float)
    return v.mean(), v.std(ddof=1) / np.sqrt(len(v))


def glcm_section():
    path = ROOT / "results" / "glcm_native_grid.json"
    if not path.exists():
        return ["## GLCM Score（HiMat の型）", "", "結果のファイルが無い。", ""]
    d = json.loads(path.read_text())
    rows = d["rows"]
    v = {(r["surface"], r["seed"], r["N"], r["method"]): r["glcm"] for r in rows}
    surfaces = list(dict.fromkeys(r["surface"] for r in rows))
    seeds = sorted({r["seed"] for r in rows})
    Ns = sorted({r["N"] for r in rows if r["method"] != "native"})
    methods = list(dict.fromkeys(r["method"] for r in rows if r["method"] != "native"))
    ref = lambda s, sd: v[(s, sd, 4096, "native")]
    L = ["## GLCM Score（HiMat の型）", "",
         f"条件の一覧の SHA-256: `{d['meta']['conditions_sha256'][:16]}`。値は Diffusion-4K の公開コードの写し（atact.gridcompare.glcm_score）で、4096 に拡大して描画した灰色の画像で測った。",
         "", "### 値（種 5 本の平均）。列は本来の格子 N、N = 4096 は拡大なし", ""]
    L += ["| 表面 | 拡大の方法 | " + " | ".join(f"N = {n}" for n in Ns) + " | N = 4096 |", "|---|---|" + "---|" * (len(Ns) + 1)]
    for s in surfaces:
        r4 = np.mean([ref(s, sd) for sd in seeds])
        for m in methods:
            L.append(f"| {s} | {m} | " + " | ".join(f"{np.mean([v[(s, sd, n, m)] for sd in seeds]):.3f}" for n in Ns) + f" | {r4:.3f} |")
    L += ["", "### N = 4096 との差（同じ種の対応のある差の平均、括弧は標準誤差）", ""]
    L += ["| 表面 | 拡大の方法 | " + " | ".join(f"N = {n}" for n in Ns) + " |", "|---|---|" + "---|" * len(Ns)]
    for s in surfaces:
        for m in methods:
            cells = []
            for n in Ns:
                a, e = mse([v[(s, sd, n, m)] - ref(s, sd) for sd in seeds])
                cells.append(f"{a:+.3f}（{e:.3f}）")
            L.append(f"| {s} | {m} | " + " | ".join(cells) + " |")
    L += ["", "### 順序: fine を N = 256 で作ったものと coarse を N = 4096 で作ったものの差（fine − coarse、種ごとの対応のある差）", ""]
    L += ["| 拡大の方法 | 平均（標準誤差） | 種ごとの符号 |", "|---|---|---|"]
    for m in methods:
        diffs = [v[("fine", sd, 256, m)] - ref("coarse", sd) for sd in seeds]
        a, e = mse(diffs)
        L.append(f"| {m} | {a:+.3f}（{e:.3f}） | {' '.join('+' if x > 0 else '−' for x in diffs)} |")
    a, e = mse([ref("fine", sd) - ref("coarse", sd) for sd in seeds])
    L += [f"| 参照: どちらも N = 4096 | {a:+.3f}（{e:.3f}） | |", ""]
    return L


def seam_section():
    d = json.loads((ROOT / "results" / "tile_seam_grid.json").read_text())
    g = defaultdict(dict)
    for r in d["rows"]:
        g[(r["kind"], r["f"], r["seed"], tuple(r["offset"]))][r["method"]] = r
    L = ["## 継ぎ目の指標（Gao ら 2026 の型）", "",
         f"条件の一覧の SHA-256: `{d['meta']['conditions_sha256'][:16]}`。1024 の法線の図を 512 に縮小（PIL の LANCZOS）したものと、中央の 512 を切り出したもの。指標は Gao らの公開コードの写し（RGB の 0〜255）。",
         "物差し: Gao ら 2026 の表 1 は Resize 29.80 / 59.99、Crop 26.10 / 52.82（border / grad）。", ""]
    for kind, lab in (("nonperiodic", "周期的でない場（種 5 × 切り出し 5）"), ("periodic", "周期的な場、陰性対照（種 5、切り出しの位置 (0, 0)）")):
        L += [f"### {lab}", "", "| f | 指標 | Resize | Crop | Resize − Crop（標準誤差） |", "|---|---|---|---|---|"]
        for f in sorted({k[1] for k in g if k[0] == kind}):
            ks = [k for k in g if k[0] == kind and k[1] == f]
            for m, ml in (("border_avg", "border"), ("grad_cont_avg", "grad")):
                R = [g[k]["resize"][m] for k in ks]
                C = [g[k]["crop"][m] for k in ks]
                a, e = mse(np.subtract(R, C))
                L.append(f"| {f} | {ml} | {np.mean(R):.2f} | {np.mean(C):.2f} | {a:+.2f}（{e:.2f}） |")
        L.append("")
    return L


def main():
    L = ["# 解像度をまたぐ比較の 2 つの型の再現（合成した表面）", "",
         "合成した表面での再現であり、HiMat と Gao らの比較の結論への影響は主張しない。", ""]
    L += glcm_section() + seam_section()
    (ROOT / "results" / "grid_compare.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
