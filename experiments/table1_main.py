"""Main-text version of Table 1 of K5, extracted from the stored results without any new computation.

Usage:  uv run python experiments/table1_main.py
Input:  results/k5_classification.json (commit 3f58861; its SHA-256 is checked below)
        experiments/conditions/k5_table1_predictions.json (the predictions, for their wording)
Output: results/table1_main.json, results/table1_main.md and results/table1_main.tex

The slice shown in the main text is fixed as N = 128, raw (no window) and w = 0.3; the null conditions (iii_null and
check_same_seed) have no w. Rows are the seven conditions, columns the four descriptor sets times the two
representations (H and min-max). Each cell gives the predicted direction and order (prediction numbers of
k5_table1_predictions.json), the large-sample level, and the finite-sample estimates of the svm and of the threshold
with their 95% pair-bootstrap intervals, copied from the row of the stored summary. The full table (544 rows) is in
results/k5_classification.md.

Whether a prediction holds in a cell is evaluated again here from the stored accuracies, with the criteria of
k5_table1_predictions.json restricted to the predictions that name this cell. Predictions that compare the cell with
rows outside the slice (other w or N) use those stored rows. No surface is generated and no classifier is fitted.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "results" / "k5_classification.json"
SRC_SHA256 = "a96c475bae36c43a71aa5b2bc9660cce530da628648afe6f8a7899c9f8cde653"  # commit 3f58861
PRED = ROOT / "experiments" / "conditions" / "k5_table1_predictions.json"
PRED_SHA256 = "6cf0f96992bd4acab004d03f66b0566c355f84f14eb8bf869709d9a33db7693b"
OUT = ROOT / "results"

N_MAIN, PROC_MAIN, W_MAIN = 128, "raw", 0.3
CONDITIONS = ["i_V", "i_A", "ii_s", "ii_s_gamma", "corners", "iii_null", "check_same_seed"]
NULL = ("iii_null", "check_same_seed")
SETS = ["S", "C", "B", "SC"]
SET_OF = {("sq",): "S", ("centroid_amp",): "C", ("centroid_band_power",): "B", ("sq", "centroid_amp"): "SC"}
REPS = ["H", "minmax"]
OTHER_W = (0.1, 0.5)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_rows() -> list[dict]:
    if sha256(SRC) != SRC_SHA256:
        raise SystemExit(f"{SRC} does not have the SHA-256 of commit 3f58861")
    if sha256(PRED) != PRED_SHA256:
        raise SystemExit(f"{PRED} does not have the SHA-256 recorded in INDEX.json")
    rows = json.loads(SRC.read_text())["summary"]["table1"]
    if len(rows) != 544:
        raise SystemExit(f"expected 544 rows, found {len(rows)}")
    return rows


def key(cond: str, w, n: int, proc: str, rep: str, sn: str) -> tuple:
    return (cond, w, n, proc, rep, sn)


def index(rows: list[dict]) -> dict:
    out = {}
    for r in rows:
        k = key(r["condition"], r["w"], r["N"], r["processing"], r["representation"], SET_OF[tuple(r["descriptor_set"])])
        if k in out:
            raise SystemExit(f"duplicate row {k}")
        out[k] = r
    return out


def main_w(cond: str):
    return None if cond in NULL else W_MAIN


def acc(r: dict, clf: str):
    return r["estimate_finite_svm"] if clf == "svm" else r["estimate_finite_threshold"]


def classifiers(sn: str) -> list[str]:
    return ["svm"] if sn == "SC" else ["svm", "threshold"]


def pid(text: str) -> str:
    """'above chance (svm; P-K5-12)' -> 'P-K5-12'."""
    i = text.rfind("P-K5-")
    if i < 0:
        raise ValueError(text)
    return text[i:].rstrip(")")


def evaluate(text: str, cell: tuple, ix: dict) -> bool | None:
    """Whether the prediction `text` of the row `cell` holds there, from the stored accuracies. None: no criterion."""
    cond, w, n, proc, rep, sn = cell
    r = ix[cell]
    p = pid(text)
    if p == "P-K5-12":
        return r["ci95_svm"][0] > 0.5
    if p == "P-K5-3" and text.startswith("exactly"):
        return all(acc(r, c) == 0.5 for c in classifiers(sn))
    if p == "P-K5-3":
        return all(r["tost_chance"][c] for c in classifiers(sn))
    if p == "P-K5-9" and text.startswith("no direction"):
        return None
    if p in ("P-K5-1", "P-K5-6"):  # <= the same row on H, both classifiers
        h = ix[key(cond, w, n, proc, "H", sn)]
        return all(acc(r, c) <= acc(h, c) for c in classifiers(sn))
    if p == "P-K5-4":  # = the same row on H
        h = ix[key(cond, w, n, proc, "H", sn)]
        return all(acc(r, c) == acc(h, c) for c in classifiers(sn))
    if p == "P-K5-5":
        other = "corners" if cond == "ii_s" else "ii_s"
        o = ix[key(other, w, n, proc, rep, sn)]
        return all(acc(r, c) == acc(o, c) for c in classifiers(sn))
    if p in ("P-K5-2", "P-K5-11") and text.startswith("N = 512"):
        big = ix[key(cond, w, 512, proc, rep, sn)]
        small = ix[key(cond, w, 128, proc, rep, sn)]
        return all(acc(big, c) >= acc(small, c) for c in classifiers(sn))
    if p == "P-K5-2":  # change between N = 128 and 512 smaller than for raw C
        ref_hi, ref_lo = ix[key(cond, w, 512, "raw", rep, "C")], ix[key(cond, w, 128, "raw", rep, "C")]
        hi, lo = ix[key(cond, w, 512, proc, rep, sn)], ix[key(cond, w, 128, proc, rep, sn)]
        return all(abs(acc(hi, c) - acc(lo, c)) < abs(acc(ref_hi, c) - acc(ref_lo, c)) for c in classifiers(sn))
    if p == "P-K5-7":
        s_, c_ = ix[key(cond, w, n, proc, rep, "S")], ix[key(cond, w, n, proc, rep, "C")]
        return acc(r, "svm") >= max(acc(s_, "svm"), acc(c_, "svm"))
    if p == "P-K5-8":
        a = [acc(ix[key(cond, ww, n, proc, rep, sn)], "svm") for ww in (0.1, 0.3, 0.5)]
        return a[0] >= a[1] >= a[2]
    if p == "P-K5-9":
        others = [acc(ix[key(c2, w, n, proc, rep, "S")], "svm") for c2 in ("i_V", "i_A", "ii_s", "corners")]
        return all(acc(r, "svm") < x for x in others)
    if p == "P-K5-10":
        g = {s2: acc(ix[key(cond, w, n, proc, rep, s2)], "svm") for s2 in ("S", "C", "B")}
        if text.startswith(">= S"):
            return g[sn] >= g["S"]
        if text.startswith("<= C and B"):
            return g["S"] <= g["C"] and g["S"] <= g["B"]
        if text.startswith(">= C"):
            return g["S"] >= g["C"]
        if text.startswith("<= S"):
            return g["C"] <= g["S"]
    raise ValueError(f"no criterion for {text!r}")


def build(rows: list[dict]) -> list[dict]:
    ix = index(rows)
    out = []
    for cond in CONDITIONS:
        for rep in REPS:
            for sn in SETS:
                cell = key(cond, main_w(cond), N_MAIN, PROC_MAIN, rep, sn)
                r = ix[cell]
                preds = []
                for text in r["predicted_direction"] + r["predicted_order"]:
                    if text == "none":
                        continue
                    preds.append({"text": text, "id": pid(text), "holds": evaluate(text, cell, ix)})
                out.append({
                    "condition": cond, "w": cell[1], "N": N_MAIN, "processing": PROC_MAIN, "representation": rep,
                    "descriptor_set": sn, "predictions": preds,
                    "level_large_sample": r["predicted_level_large_sample"],
                    "svm": r["estimate_finite_svm"], "ci95_svm": r["ci95_svm"],
                    "threshold": r["estimate_finite_threshold"], "ci95_threshold": r["ci95_threshold"],
                    "tost_chance": r["tost_chance"], "perm_p": r["perm_p"],
                })
    return out


def f3(x) -> str:
    return "-" if x is None else f"{x:.3f}"


def ci(c) -> str:
    return "-" if c is None else f"[{c[0]:.3f}, {c[1]:.3f}]"


def short_list(preds: list[dict]) -> str:
    """Prediction numbers in order of first appearance; '*' if the prediction fails in any of its parts here."""
    seen: dict[str, bool] = {}
    for p in preds:
        n = p["id"].replace("P-K5-", "")
        seen[n] = seen.get(n, False) or p["holds"] is False
    return ", ".join(n + ("*" if bad else "") for n, bad in seen.items())


def write_md(cells: list[dict], meta: dict) -> str:
    L = ["# Table 1, main-text version (K5)", "",
         f"Extracted from `results/k5_classification.json` (SHA-256 `{SRC_SHA256}`, commit 3f58861) by "
         f"`experiments/table1_main.py` (SHA-256 `{meta['script_sha256']}`). No new computation. "
         f"Slice: N = {N_MAIN}, processing {PROC_MAIN}, w = {W_MAIN} (the null conditions have no w). "
         "The full table of 544 rows is in `results/k5_classification.md`.", "",
         "Predictions are numbered as in `experiments/conditions/k5_table1_predictions.json`; an asterisk marks a "
         "prediction that does not hold in this cell (evaluated from the stored accuracies with the criterion of that "
         "prediction restricted to this cell). Level: large-sample level of the frame. Intervals: 95% pair bootstrap.",
         "", "| condition | repr | set | predictions | level | svm | 95% CI svm | threshold | 95% CI threshold |",
         "|---|---|---|---|---|---|---|---|---|"]
    for c in cells:
        pr = short_list(c["predictions"]) or "none"
        L.append(f"| {c['condition']} | {c['representation']} | {c['descriptor_set']} | {pr} | "
                 f"{f3(c['level_large_sample'])} | {f3(c['svm'])} | {ci(c['ci95_svm'])} | {f3(c['threshold'])} | "
                 f"{ci(c['ci95_threshold'])} |")
    L += ["", "## Predictions that do not hold in a cell of this slice", ""]
    bad = [(c, p) for c in cells for p in c["predictions"] if p["holds"] is False]
    if not bad:
        L.append("None.")
    for c, p in bad:
        L.append(f"- {c['condition']}, {c['representation']}, {c['descriptor_set']}: {p['text']}")
    L += ["", "## Wording of the predictions in this slice", ""]
    seen = {}
    for c in cells:
        for p in c["predictions"]:
            seen.setdefault(p["id"], set()).add(p["text"])
    for k in sorted(seen, key=lambda s: int(s.split("-")[-1])):
        for t in sorted(seen[k]):
            L.append(f"- {k}: {t}")
    return "\n".join(L) + "\n"


TEX_COND = {"i_V": r"(i) $V$", "i_A": r"(i) $A$", "ii_s": r"(ii) $s$", "ii_s_gamma": r"(ii) $s,\gamma$",
            "corners": "corners", "iii_null": "(iii) null", "check_same_seed": "same seed"}
TEX_SET = {"S": r"$S_q$", "C": r"$C$", "B": r"$C_{\mathrm{band}}$", "SC": r"$S_q{+}C$"}


def tex_cell(c: dict) -> str:
    pr = short_list(c["predictions"]).replace(" ", "") or "--"
    lines = [rf"\textit{{{pr}}}", rf"L {f3(c['level_large_sample'])}",
             rf"S {f3(c['svm'])} {ci(c['ci95_svm'])}"]
    if c["threshold"] is not None:
        lines.append(rf"T {f3(c['threshold'])} {ci(c['ci95_threshold'])}")
    return r"\makecell[l]{" + r"\\ ".join(lines) + "}"


def write_tex(cells: list[dict]) -> str:
    by = {(c["condition"], c["representation"], c["descriptor_set"]): c for c in cells}
    L = ["% Generated by experiments/table1_main.py from results/k5_classification.json (commit 3f58861).",
         "% Needs \\usepackage{booktabs,makecell}. Each cell: prediction numbers (* = does not hold here),",
         "% L = large-sample level, S = svm, T = threshold, with 95% pair-bootstrap intervals.",
         r"\begin{tabular}{l" + "l" * 8 + "}", r"\toprule",
         " & " + " & ".join(rf"\multicolumn{{4}}{{c}}{{{t}}}" for t in ("height $H$", "min--max export")) + r" \\",
         r"\cmidrule(lr){2-5}\cmidrule(lr){6-9}",
         "condition & " + " & ".join(TEX_SET[s] for _ in REPS for s in SETS) + r" \\", r"\midrule"]
    for cond in CONDITIONS:
        L.append(TEX_COND[cond] + " & " + " & ".join(tex_cell(by[(cond, rep, s)]) for rep in REPS for s in SETS)
                 + r" \\")
        L.append(r"\addlinespace")
    L[-1] = r"\bottomrule"
    L.append(r"\end{tabular}")
    return "\n".join(L) + "\n"


def main() -> None:
    rows = load_rows()
    cells = build(rows)
    meta = {"source": str(SRC.relative_to(ROOT)), "source_sha256": SRC_SHA256,
            "predictions": str(PRED.relative_to(ROOT)), "predictions_sha256": PRED_SHA256,
            "script_sha256": sha256(Path(__file__)),
            "slice": {"N": N_MAIN, "processing": PROC_MAIN, "w": W_MAIN, "w_null": None}}
    (OUT / "table1_main.json").write_text(json.dumps({"meta": meta, "cells": cells}, indent=1) + "\n")
    (OUT / "table1_main.md").write_text(write_md(cells, meta))
    (OUT / "table1_main.tex").write_text(write_tex(cells))
    print(f"{len(cells)} cells written")


if __name__ == "__main__":
    main()
