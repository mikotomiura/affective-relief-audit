"""報告値との食い違いが、生成器・記述子・分類の手順のどこから来るかを切り分ける。

使い方: uv run python experiments/decompose.py [--jitter 1.25] [--out results/decompose.md]

組:
  生成器   組み直し / 元のコード（アダプタの height）
  記述子   組み直し（式 (5)(6)） / 元のコード（アダプタの features）
  手順     組み直し（make_dataset のジッタと種 + 標準化 + 線形 SVM） / 元のコードの dataset()（元の 120 枚の特徴）
元のコードが無い組・アダプタに関数が無い組は「無し」と書く。今は組み直しの行だけが埋まる。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from atact import backends
from atact.classify import default_features, evaluate
from atact.report import COLUMNS, run
from atact.reported import HOLDOUT, TABLE3

OUT = Path(__file__).resolve().parents[1] / "results"


def _orig_features(orig):
    if orig is None:
        return None
    probe = orig.features(orig.height(0.0, 0.0, 42))
    return None if probe is None else (lambda H: tuple(orig.features(H)))


def cells(jitter: float, seed: int = 0):
    """(生成器, 記述子, 手順, 結果 or 無しの理由) の並び。"""
    recon = backends.ReconBackend()
    orig = backends.original()
    ofeat = _orig_features(orig)
    out = []
    for gname, gen in (("組み直し", recon), ("元", orig)):
        for fname, feat in (("組み直し", default_features), ("元", ofeat)):
            if gen is None:
                out.append((gname, fname, "組み直し", "元のコードが無い"))
            elif feat is None:
                out.append((gname, fname, "組み直し", "元のコードが無い" if orig is None else "アダプタに features が無い"))
            else:
                out.append((gname, fname, "組み直し", run(backend=gen, features=feat, jitter=jitter, seed=seed)))
    ds = None if orig is None else orig.dataset()
    if ds is None:
        out.append(("元", "元", "元の dataset()", "元のコードが無い" if orig is None else "アダプタに dataset が無い"))
    else:
        X, y = (np.asarray(a) for a in ds)
        out.append(("元", "元", "元の dataset()", evaluate(X, y, seed=seed)))
    return out


def render(cs, jitter: float) -> str:
    L = ["# 切り分け: 生成器 × 記述子 × 手順", "",
         f"手順が「組み直し」の行はジッタ w = {jitter}（A4。原稿に無い）。値は 20 回 × 5 分割の平均の精度（%）。", "",
         "| 生成器 | 記述子 | 手順 | " + " | ".join(lbl for _, lbl in COLUMNS) + " | 75/25 正解数 |",
         "|---|---|---|" + "---|" * (len(COLUMNS) + 1)]
    L.append("| 報告 | 報告 | 報告 | " + " | ".join(f"{100*TABLE3[k][0]:.1f}" for k, _ in COLUMNS)
             + f" | {HOLDOUT['n_correct']} / 30 |")
    for g, f, p, r in cs:
        if isinstance(r, str):
            L.append(f"| {g} | {f} | {p} | " + " | ".join("無し" for _ in COLUMNS) + f" | 無し（{r}） |")
        else:
            L.append(f"| {g} | {f} | {p} | " + " | ".join(f"{100*r[k][0]:.1f}" for k, _ in COLUMNS)
                     + f" | {round(30 * r['holdout'])} / 30 |")
    L += ["", "読み方: 行を 1 つずつ変えて、報告に近づく段がどこかを見る。生成器だけを元に替えて近づくなら、"
          "食い違いは生成器（A1〜A3）から来ている。"]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jitter", type=float, default=1.25)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    md = render(cells(a.jitter), a.jitter)
    out = a.out or OUT / "decompose.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    print(md)


if __name__ == "__main__":
    main()
