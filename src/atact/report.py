"""Place the reported values (atact.reported) beside the values computed here.

Used by compare_reported, decompose and arrival_check. The "computed" values are either those of the
reconstructed generator or those obtained through the original code; the table heading must state which.
"""

from __future__ import annotations

from .classify import DatasetConfig, evaluate, make_dataset
from .reported import HOLDOUT, TABLE3

COLUMNS = (("rq", "Rq だけ"), ("centroid", "重心だけ"), ("both", "両方"), ("permuted", "並べ替え"))


def run(backend=None, features=None, jitter: float = 1.25, seed: int = 0) -> dict:
    """Build 120 surfaces with the chosen generator and descriptors and evaluate as in Table 3."""
    X, y, _ = make_dataset(DatasetConfig(jitter=jitter), backend=backend, features=features)
    return evaluate(X, y, seed=seed)


def compare(res: dict) -> list[dict]:
    """For the four columns of Table 3 and for 75/25, return the difference and its size in units of the reported standard deviation."""
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
