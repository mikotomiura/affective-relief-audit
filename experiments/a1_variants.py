"""A1（オクターブの形・周波数の単位）と雑音・ワープを振り、図 3 との近さと命題 7 の表を出す。

使い方: uv run python experiments/a1_variants.py [--quick]
出力: results/a1_variants.json と results/a1_variants.md

- 図 3 との近さ: 隅 (1,-1) を Calm、(-1,1) を Anger とみなし、256 x 256（図 3 の格子）で描いた高さの
  指紋（atact.fig3.fingerprint）と、図 3 から取り戻した高さの指紋との距離を足す。種は 42。
  図 3 の座標は本文に書かれていないので、隅とみなすこと自体が仮定である。Complex は座標の手がかりが無いので使わない。
- 命題 7: 128 x 128（表 2）で 120 枚を作り、表 3 と同じ 4 列を出す。
すべて組み直しの生成器での値で、元のコード（ESM_1.zip）の値ではない。
"""

from __future__ import annotations

import argparse
import itertools
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from pathlib import Path

import numpy as np

from atact import fig3
from atact.classify import DatasetConfig, evaluate, make_dataset
from atact.field import RenderConfig, height
from atact.reported import TABLE3

OUT = Path(__file__).resolve().parents[1] / "results"
CORNERS = {"calm": (1.0, -1.0), "anger": (-1.0, 1.0)}

GRID = {
    "freq_unit": ("cycles", "half"),
    "octave_form": ("product", "sum", "oriented"),
    "noise": (0.0, 0.1, 0.3),
    "warp": (0.0, 0.25),
}
JITTERS = (0.5, 1.0, 1.25, 1.5)


def variants(quick: bool):
    keys = list(GRID)
    for vals in itertools.product(*(GRID[k] for k in keys)):
        v = dict(zip(keys, vals))
        if quick and (v["octave_form"] == "oriented" or v["noise"] == 0.1):
            continue
        yield v


def fig3_distance(v: dict, ref: dict) -> dict:
    out = {}
    for name, va in CORNERS.items():
        H = height(*va, RenderConfig(n=256, **v), seed=42)
        fp = fig3.fingerprint(H)
        out[name] = {"fp": fp, "distance": fig3.distance(fp, ref[name])}
    out["total"] = sum(out[k]["distance"] for k in CORNERS)
    return out


def p7(v: dict, jitters) -> list:
    rows = []
    for w in jitters:
        X, y, _ = make_dataset(DatasetConfig(jitter=w, render=RenderConfig(**v)))
        r = evaluate(X, y)
        rows.append({"jitter": w, **r, "gap_rq_minus_centroid": r["rq"][0] - r["centroid"][0]})
    return rows


def run_one(args):
    v, ref, jitters = args
    return {"variant": v, "fig3": fig3_distance(v, ref), "p7": p7(v, jitters)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="oriented と noise=0.1 を外し、ジッタを 2 つにする")
    a = ap.parse_args()
    jitters = (1.0, 1.25) if a.quick else JITTERS
    panels = fig3.panels()
    ref = {k: fig3.fingerprint(panels[k]["height"]) for k in CORNERS}
    jobs = [(v, ref, jitters) for v in variants(a.quick)]
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(run_one, jobs))
    res.sort(key=lambda r: r["fig3"]["total"])
    OUT.mkdir(exist_ok=True)
    payload = {"reference_fig3": ref, "reported_table3": TABLE3, "default_render": asdict(RenderConfig()),
               "jitters": list(jitters), "results": res}
    (OUT / "a1_variants.json").write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    (OUT / "a1_variants.md").write_text(render_md(payload))
    print(render_md(payload))


def _pct(m):
    return f"{100 * m[0]:.1f}"


def render_md(p) -> str:
    ref = p["reference_fig3"]
    L = ["# A1 の変種: 図 3 との近さと命題 7（組み直しの生成器での値）", "",
         "図 3 から取り戻した高さの指紋（256 x 256）:", "",
         "| 枚 | 周期数 x | 周期数 y | 3 次/1 次 | 斑点 |", "|---|---|---|---|---|"]
    for k, fp in ref.items():
        L.append(f"| {k} | {fp['cycles_x']:.2f} | {fp['cycles_y']:.2f} | {fp['harmonic3']:.3f} | {fp['speckle']:.4f} |")
    t = p["reported_table3"]
    L += ["", f"報告（表 3）: Rq だけ {100*t['rq'][0]:.1f}、重心だけ {100*t['centroid'][0]:.1f}、"
          f"両方 {100*t['both'][0]:.1f}、並べ替え {100*t['permuted'][0]:.1f}。Rq − 重心 = "
          f"{100*(t['rq'][0]-t['centroid'][0]):.1f} ポイント", "",
          "図 3 に近い順。距離は Calm と Anger の和。命題 7 の列は「Rq だけ / 重心だけ / 両方（Rq − 重心）」で、ジッタ w ごと。", ""]
    js = p["jitters"]
    L.append("| 単位 | 形 | 雑音 | ワープ | 距離 | Calm 周期 | Anger 周期 | Anger 3次 | Anger 斑点 | "
             + " | ".join(f"w={w}" for w in js) + " |")
    L.append("|" + "---|" * (9 + len(js)))
    for r in p["results"]:
        v, f = r["variant"], r["fig3"]
        cells = []
        for row in r["p7"]:
            cells.append(f"{_pct(row['rq'])} / {_pct(row['centroid'])} / {_pct(row['both'])} "
                         f"({100*row['gap_rq_minus_centroid']:+.1f})")
        L.append(f"| {v['freq_unit']} | {v['octave_form']} | {v['noise']} | {v['warp']} | {f['total']:.2f} | "
                 f"{f['calm']['fp']['cycles_x']:.2f} | {f['anger']['fp']['cycles_x']:.2f} | "
                 f"{f['anger']['fp']['harmonic3']:.3f} | {f['anger']['fp']['speckle']:.4f} | " + " | ".join(cells) + " |")
    rows = [(r["variant"], row) for r in p["results"] for row in r["p7"]]
    L += ["", "## 要約", "", "雑音の強さごとの「Rq − 重心」の最大（全部の形・単位・ワープ・ジッタのうち）:", ""]
    for nz in sorted({v["noise"] for v, _ in rows}):
        g, v, row = max(((row["gap_rq_minus_centroid"], v, row) for v, row in rows if v["noise"] == nz),
                        key=lambda x: x[0])
        L.append(f"- 雑音 {nz}: {100*g:+.1f} ポイント（{v['freq_unit']} / {v['octave_form']} / ワープ {v['warp']} / "
                 f"w = {row['jitter']}）")

    def z(row):
        return float(np.sqrt(sum(((row[k][0] - t[k][0]) / t[k][1]) ** 2 for k in ("rq", "centroid", "both"))))

    L += ["", "報告に近い組（Rq だけ・重心だけ・両方の差を報告の標準偏差で割った大きさの二乗和の平方根）:", "",
          "| 単位 | 形 | 雑音 | ワープ | w | Rq だけ | 重心だけ | 両方 | 並べ替え | 75/25 | z |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for v, row in sorted(rows, key=lambda x: z(x[1]))[:8]:
        L.append(f"| {v['freq_unit']} | {v['octave_form']} | {v['noise']} | {v['warp']} | {row['jitter']} | "
                 f"{_pct(row['rq'])} | {_pct(row['centroid'])} | {_pct(row['both'])} | {_pct(row['permuted'])} | "
                 f"{100*row['holdout']:.1f} | {z(row):.2f} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
