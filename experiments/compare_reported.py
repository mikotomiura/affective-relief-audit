"""Place the reported values (Table 3 of Harada 2026 and the 75/25 split) beside the values computed with the chosen generator.

Usage:
  uv run python experiments/compare_reported.py --backend recon --jitter 1.0 1.25 1.5
  uv run python experiments/compare_reported.py --backend original     # when an adapter is available
Output: results/compare_<backend>.md (changeable with --out)

Values for recon come from the reconstructed generator. The jitter w is not given in the preprint (Harada 2026; assumption A4), so several values are tabulated.
If the original code returns dataset() (the features of the original 120 surfaces), a table evaluating them with the classification procedure used here is also produced.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from atact import backends
from atact.classify import evaluate
from atact.report import compare, run, table_md

OUT = Path(__file__).resolve().parents[1] / "results"


def build(name: str, jitters, seed: int = 0) -> str:
    avail = backends.available()
    if name not in avail:
        raise SystemExit(f"{name} は使えない（使えるのは {sorted(avail)}）。元のコードはアダプタが要る")
    be = avail[name]
    kind = "組み直しの生成器での値" if name.startswith("recon") else "元のコードの生成器を通した値"
    L = [f"# 報告値との比較: {name}（{kind}）", "",
         "分類の手順はこちらの組み直し（標準化 + 線形 SVM、層化 5 分割 × 20 回、75/25 は 1 回）。", ""]
    for w in jitters:
        L.append(table_md(compare(run(backend=be, jitter=w, seed=seed)), f"ジッタ w = {w}"))
    ds = be.dataset()
    if ds is not None:
        X, y = (np.asarray(a) for a in ds)
        L.append(table_md(compare(evaluate(X, y, seed=seed)),
                          f"元のコードが作った {len(y)} 枚の特徴（ジッタは元のコードのまま）"))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default="recon")
    ap.add_argument("--jitter", type=float, nargs="+", default=[1.0, 1.25, 1.5])
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    md = build(a.backend, a.jitter)
    out = a.out or OUT / f"compare_{a.backend}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    print(md)


if __name__ == "__main__":
    main()
