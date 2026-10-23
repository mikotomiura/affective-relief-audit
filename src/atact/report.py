"""報告値（atact.reported）と、こちらで出した値を並べる。

compare_reported・decompose・arrival_check の 3 本が使う。ここで扱う「こちらの値」は、
組み直しの生成器での値か、元のコードを通した値のどちらかで、表の見出しにどちらかを必ず書く。
"""

from __future__ import annotations

from .classify import DatasetConfig, evaluate, make_dataset
from .reported import HOLDOUT, TABLE3

COLUMNS = (("rq", "Rq だけ"), ("centroid", "重心だけ"), ("both", "両方"), ("permuted", "並べ替え"))


def run(backend=None, features=None, jitter: float = 1.25, seed: int = 0) -> dict:
    """生成器と記述子を選んで 120 枚を作り、表 3 と同じ評価をする。"""
    X, y, _ = make_dataset(DatasetConfig(jitter=jitter), backend=backend, features=features)
    return evaluate(X, y, seed=seed)


def compare(res: dict) -> list[dict]:
    """表 3 の 4 列と 75/25 について、差と「報告の標準偏差で割った大きさ」を返す。"""
    rows = []
    for key, label in COLUMNS:
        m, sd = res[key]
        rm, rsd = TABLE3[key]
        rows.append({"key": key, "label": label, "ours": m, "ours_sd": sd, "reported": rm, "reported_sd": rsd,
                     "diff": m - rm, "z": (m - rm) / rsd})
    n = HOLDOUT["n_test"]
    rows.append({"key": "holdout", "label": "75/25（30 枚中の正解数）", "ours": res["holdout"],
                 "ours_correct": round(res["holdout"] * n), "reported": HOLDOUT["accuracy"],
                 "reported_correct": HOLDOUT["n_correct"], "diff": res["holdout"] - HOLDOUT["accuracy"]})
    return rows


def table_md(rows: list[dict], title: str) -> str:
    L = [f"### {title}", "", "| 項目 | 報告 | こちら | 差 | 差 / 報告の SD |", "|---|---|---|---|---|"]
    for r in rows:
        if r["key"] == "holdout":
            L.append(f"| {r['label']} | {r['reported_correct']} / 30 | {r['ours_correct']} / 30 | "
                     f"{r['ours_correct'] - r['reported_correct']:+d} 枚 | - |")
        else:
            L.append(f"| {r['label']} | {100*r['reported']:.1f} ± {100*r['reported_sd']:.1f} | "
                     f"{100*r['ours']:.1f} ± {100*r['ours_sd']:.1f} | {100*r['diff']:+.1f} | {r['z']:+.2f} |")
    return "\n".join(L) + "\n"
