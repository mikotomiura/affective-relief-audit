"""How the centroid-only accuracy of Proposition 7 changes with the reading of eq. (6) of Harada (2026) (atact.descriptors.centroid_variant).

Usage: uv run python experiments/centroid_variants.py
Output: results/centroid_variants.json and results/centroid_variants.md

The generator is the reconstruction default (no noise), with warp 0 and 0.25. The centroid definition is varied over 32 variants,
to see whether any definition lowers the centroid-only accuracy to about the reported 74.2%. Rq does not depend on the definition, so it is the same in every row.
All values come from the reconstructed generator, not from the original code (ESM_1.zip).
"""

from __future__ import annotations

import itertools
import json
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

from atact.classify import DatasetConfig, evaluate, make_dataset
from atact.descriptors import centroid_variant, rq
from atact.field import RenderConfig
from atact.reported import TABLE3

OUT = Path(__file__).resolve().parents[1] / "results"
GRID = {
    "weight": ("amp", "power"),
    "center": (True, False),
    "rescale": (None, "minmax"),
    "half": (False, True),
    "rho_round": (False, True),
}
WARPS = (0.0, 0.25)
JITTERS = (1.0, 1.25, 1.5)


def feats(H, **kw):
    return rq(H), centroid_variant(H, **kw)


def run_one(args):
    kw, warp, w = args
    X, y, _ = make_dataset(DatasetConfig(jitter=w, render=RenderConfig(warp=warp)), features=partial(feats, **kw))
    r = evaluate(X, y)
    return {"definition": kw, "warp": warp, "jitter": w, **r}


def main():
    import sys

    if "--render-only" in sys.argv:  # rewrite only the table from the JSON, without recomputing
        rows = json.loads((OUT / "centroid_variants.json").read_text())["rows"]
        (OUT / "centroid_variants.md").write_text(render_md(rows))
        return
    keys = list(GRID)
    defs = [dict(zip(keys, v)) for v in itertools.product(*(GRID[k] for k in keys))]
    jobs = [(d, warp, w) for d in defs for warp in WARPS for w in JITTERS]
    with ProcessPoolExecutor() as ex:
        rows = list(ex.map(run_one, jobs))
    OUT.mkdir(exist_ok=True)
    (OUT / "centroid_variants.json").write_text(json.dumps({"reported_table3": TABLE3, "rows": rows}, indent=1))
    md = render_md(rows)
    (OUT / "centroid_variants.md").write_text(md)
    print(md)


def render_md(rows) -> str:
    t = TABLE3
    L = ["# 重心の定義の変種と命題 7（組み直しの生成器での値・雑音なし）", "",
         f"報告（表 3）: Rq だけ {100*t['rq'][0]:.1f}、重心だけ {100*t['centroid'][0]:.1f} ± {100*t['centroid'][1]:.1f}、"
         f"両方 {100*t['both'][0]:.1f}。", "",
         "列は重心だけの精度（両方の精度）。w はジッタ。既定の定義（式 (6) の素直な読み）は 1 行目。", "",
         "| 重み | 中心化 | min-max の後 | 半平面 | 半径を丸める | "
         + " | ".join(f"ワープ {wp} w={w}" for wp in WARPS for w in JITTERS) + " |",
         "|" + "---|" * (5 + len(WARPS) * len(JITTERS))]
    keys = list(GRID)
    for vals in itertools.product(*(GRID[k] for k in keys)):
        d = dict(zip(keys, vals))
        cells = []
        for wp in WARPS:
            for w in JITTERS:
                r = next(r for r in rows if r["definition"] == d and r["warp"] == wp and r["jitter"] == w)
                cells.append(f"{100*r['centroid'][0]:.1f} ({100*r['both'][0]:.1f})")
        L.append(f"| {d['weight']} | {d['center']} | {d['rescale'] or '-'} | {d['half']} | {d['rho_round']} | "
                 + " | ".join(cells) + " |")
    lo = min(rows, key=lambda r: r["centroid"][0])
    rq_at = {(r["warp"], r["jitter"]): r["rq"][0] for r in rows}
    L += ["", "## 要約", "",
          f"- 重心だけの精度の最小: {100*lo['centroid'][0]:.1f}%（{lo['definition']}、ワープ {lo['warp']}、w = {lo['jitter']}）。"
          f"そのときの Rq だけは {100*lo['rq'][0]:.1f}%。",
          "- Rq だけの精度（定義に依らない）: "
          + "、".join(f"ワープ {wp} w={w}: {100*v:.1f}" for (wp, w), v in sorted(rq_at.items())) + "。"]
    g = max(rows, key=lambda r: r["rq"][0] - r["centroid"][0])
    L.append(f"- Rq − 重心 の最大: {100*(g['rq'][0]-g['centroid'][0]):+.1f} ポイント（{g['definition']}、ワープ {g['warp']}、"
             f"w = {g['jitter']}）。報告は {100*(t['rq'][0]-t['centroid'][0]):+.1f}。")
    L.append("- 中心化してから測る定義では、min-max の有無で値が変わらない（重心は場のアフィン変換に依らないため）。")
    near = [r for r in rows if abs(r["centroid"][0] - t["centroid"][0]) <= t["centroid"][1]
            and abs(r["rq"][0] - t["rq"][0]) <= t["rq"][1]]
    L.append(f"- 重心だけ・Rq だけの両方が報告の標準偏差 1 つ分以内に入る行: {len(near)} 行。")
    for r in near:
        L.append(f"  - {r['definition']}、ワープ {r['warp']}、w = {r['jitter']}: Rq {100*r['rq'][0]:.1f} / "
                 f"重心 {100*r['centroid'][0]:.1f} / 両方 {100*r['both'][0]:.1f}")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
