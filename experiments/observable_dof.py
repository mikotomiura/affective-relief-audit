"""観測できる自由度: 入力から、高さ図・書き出しの高さ図・記述子までの写像の階数。

使い方: uv run python experiments/observable_dof.py
条件: experiments/conditions/observable_dof.json（計算の前に固定してコミットした）
出力: results/observable_dof.json と results/observable_dof.md
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from atact.descriptors import centroid, rq
from atact.field import RenderConfig, minmax, procedural_field
from atact.mapping import params
from atact.transform import t_gamma

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "observable_dof.json"
STEP = 1e-4
TOL = 1e-6
D_COEF = 0.3


def outputs(V, A, D, seed, cfg=RenderConfig()):
    f, s, g = params(V, A)
    g = g + D_COEF * D
    H = s * t_gamma(procedural_field(float(f), cfg, seed), g)
    M = minmax(H)
    return {"H": H.ravel(), "minmax": M.ravel(),
            "desc_H": np.array([rq(H), centroid(H)]), "desc_minmax": np.array([rq(M), centroid(M)])}


def jac(point, k, seed):
    cols = {name: [] for name in ("H", "minmax", "desc_H", "desc_minmax")}
    for i in range(k):
        e = np.zeros(3)
        e[i] = STEP
        hi, lo = outputs(*(np.array(point) + e), seed), outputs(*(np.array(point) - e), seed)
        for name in cols:
            cols[name].append((hi[name] - lo[name]) / (2 * STEP))
    return {name: np.column_stack(v) for name, v in cols.items()}


def main():
    c = json.loads(COND.read_text())
    rows = []
    for mp, k in (("two_inputs", 2), ("three_inputs", 3)):
        for pt in c["points"]:
            p = pt if k == 3 else [pt[0], pt[1], 0.0]
            for seed in c["seeds"]:
                for name, J in jac(p, k, seed).items():
                    sv = np.linalg.svd(J, compute_uv=False)
                    rel = sv / sv[0]
                    row = {"map": mp, "point": p, "seed": seed, "output": name,
                           "rank": int((rel > TOL).sum()), "rel_sv": rel.tolist()}
                    if mp == "three_inputs" and name == "minmax":
                        _, _, vt = np.linalg.svd(J)
                        row["null_dir"] = (vt[-1] / np.abs(vt[-1]).max()).tolist()
                    rows.append(row)
    meta = {"conditions_sha256": hashlib.sha256(COND.read_bytes()).hexdigest(), "numpy": np.__version__}
    (ROOT / "results" / "observable_dof.json").write_text(json.dumps({"meta": meta, "rows": rows}))
    L = ["# 観測できる自由度（入力から各段への写像の階数）", "",
         f"条件の一覧の SHA-256: `{meta['conditions_sha256'][:16]}`。点 4 つ × 種 3 つ。階数は、特異値を最大の特異値で割った値が {TOL} を超える数。", "",
         "| 写像 | 出力 | 階数（12 通りの最小〜最大） | 最小の相対特異値の範囲 |", "|---|---|---|---|"]
    for mp in ("two_inputs", "three_inputs"):
        for name in ("H", "minmax", "desc_H", "desc_minmax"):
            rs = [r for r in rows if r["map"] == mp and r["output"] == name]
            rk = [r["rank"] for r in rs]
            last = [r["rel_sv"][-1] for r in rs]
            L.append(f"| {mp} | {name} | {min(rk)}〜{max(rk)} | {min(last):.1e}〜{max(last):.1e} |")
    nd = [r["null_dir"] for r in rows if "null_dir" in r]
    L += ["", "3 入力の minmax の零の方向（(dV, dA, dD)、最大の成分で割った値）の例: "
          + ", ".join("(" + ", ".join(f"{x:+.3f}" for x in v) + ")" for v in nd[:3])]
    (ROOT / "results" / "observable_dof.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
