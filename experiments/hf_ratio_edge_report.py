"""results/hf_ratio_edge.json から集計の表を書く（条件の一覧の readouts の順）。

使い方: uv run python experiments/hf_ratio_edge_report.py
出力: results/hf_ratio_edge.md
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GAO_SPAN = (0.009, 0.103)  # Gao ら 2026 表 1 の比較されたモデルの間の差（最小と最大）


def load():
    d = json.loads((ROOT / "results" / "hf_ratio_edge.json").read_text())
    return d["meta"], d["rows"]


def table(rows, cut, proc):
    g = defaultdict(list)
    for r in rows:
        if r["cutoff"] == cut and r["processing"] == proc:
            g[(r["surface"], r["N"])].append(r["hf_ratio"])
    return g


def spread(rows, cut, proc):
    """同じ表面・種・格子での、切り出しによる最大と最小の差。"""
    g = defaultdict(list)
    for r in rows:
        if r["cutoff"] == cut and r["processing"] == proc:
            g[(r["surface"], r["seed"], r["N"])].append(r["hf_ratio"])
    s = defaultdict(list)
    for (surf, _seed, n), v in g.items():
        s[(surf, n)].append(max(v) - min(v))
    return s


def main():
    meta, rows = load()
    surfaces = list(dict.fromkeys(r["surface"] for r in rows))
    Ns = sorted({r["N"] for r in rows})
    L = ["# HF ratio の端と格子への感度（合成した表面）", "",
         f"条件の一覧の SHA-256: `{meta['conditions_sha256'][:16]}`。numpy {meta['numpy']}。",
         "値は Gao ら 2026 の公開コードの写し（atact.hfratio）で測った。合成した表面での感度であり、Gao らの比較の結論への影響は主張しない。",
         f"物差し: Gao ら 2026 の表 1 で比較されたモデルの間の HF ratio の差は {GAO_SPAN[0]}〜{GAO_SPAN[1]}。", ""]
    for cut in ("px120", "phys"):
        for proc in ("raw", "hann"):
            t = table(rows, cut, proc)
            L += [f"## 平均（種 5 × 切り出し 5）: cutoff = {cut}, processing = {proc}", "",
                  "| 表面 | " + " | ".join(f"N = {n}" for n in Ns) + " |", "|---|" + "---|" * len(Ns)]
            for s in surfaces:
                L.append(f"| {s} | " + " | ".join(f"{np.mean(t[(s, n)]):.3f}" for n in Ns) + " |")
            L.append("")
    for proc in ("raw", "hann"):
        sp = spread(rows, "px120", proc)
        L += [f"## 切り出しによる幅（同じ表面・同じ種・同じ格子の最大 − 最小。種 5 本の平均と最大）: px120, {proc}", "",
              "| 表面 | " + " | ".join(f"N = {n}" for n in Ns) + " |", "|---|" + "---|" * len(Ns)]
        for s in surfaces:
            L.append(f"| {s} | " + " | ".join(f"{np.mean(sp[(s, n)]):.3f}（{np.max(sp[(s, n)]):.3f}）" for n in Ns) + " |")
        L.append("")
    t = table(rows, "px120", "raw")
    L += ["## 端の跳びの有無による差と、規則のつまみ（γ）による差: px120, raw", "",
          "| 比べるもの | " + " | ".join(f"N = {n}" for n in Ns) + " |", "|---|" + "---|" * len(Ns)]
    pairs = [("端の跳び: oct4 f5.5 − f5（γ = 1）", "oct4_f5.5_g1", "oct4_f5_g1"),
             ("端の跳び: oct4 f5.5 − f5（γ = 1.75）", "oct4_f5.5_g1.75", "oct4_f5_g1.75"),
             ("端の跳び: sine f5.5 − f5", "sine_f5.5", "sine_f5"),
             ("つまみ: γ 1.75 − 1（f = 5、端の跳びなし）", "oct4_f5_g1.75", "oct4_f5_g1")]
    for lab, a, b in pairs:
        L.append(f"| {lab} | " + " | ".join(f"{np.mean(t[(a, n)]) - np.mean(t[(b, n)]):+.3f}" for n in Ns) + " |")
    L.append("")
    (ROOT / "results" / "hf_ratio_edge.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
