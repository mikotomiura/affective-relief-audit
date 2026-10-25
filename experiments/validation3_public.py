"""Validation 3: whether the change of descriptor values and orderings under a change of grid, seen on synthetic
surfaces, also occurs on publicly available measured surfaces (one measurement resampled on a fixed physical domain).

Usage:  uv run python experiments/validation3_public.py            (compute, then write the results)
        uv run python experiments/validation3_public.py --report   (rewrite the results from results/validation3_public.json)
Conditions: experiments/conditions/validation3_public.json (fixed and committed before this script was run)
Specification: experiments/spec/generator-and-descriptors.md (S5)
Data: external/topo-challenge-20261025/ (Surface-Topography Challenge, CC0) and
      external/hf-tactiledreamfusion-20261025/data/tactile_textures/ (TactileDreamFusion, MIT); not redistributed.
      The SHA-256 of every input file is checked against the conditions before any value is read.
Output: results/validation3_public.json and results/validation3_public.md

This is a test of robustness to resampling of one measurement, not of re-measurement with different instruments.
No claim is made about the conclusions of other studies.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

from atact.descriptors import rq, spectral_centroids
from atact.hfratio import hf_ratio, hf_ratio_float, normal_from_height, normal_rgb_from_height
from atact.measured import central_crop, largest_pow2, read_challenge, read_normal_png
from atact.spectral import decimate_fourier, decimate_normals, remove_plane, subsample, windowed
from atact.stats import flips_relative, kendall_tau

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "validation3_public.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
OUT = ROOT / "results"
NAME = "validation3_public"
CHALLENGE_DIR = ROOT / "external" / "topo-challenge-20261025"
TDF_DIR = ROOT / "external" / "hf-tactiledreamfusion-20261025" / "data" / "tactile_textures"
THRESHOLD = 0.05  # V2: relative-difference threshold fixed in the conditions
LEVELS = ("full", "half", "quarter")

INTERPRETATION = [
    "Challenge: heights are stored with dimensions (x, y) and are transposed to [y, x]. The pixel spacings along x "
    "and y (length attribute divided by the number of points) differ by at most 3.3e-4 in relative terms in the "
    "included measurements; the normal map uses their mean as the spacing of S2.8, and the side of the crop is "
    "L = P times that spacing. At the coarser levels the spacing is L/n.",
    "Challenge levels: the P x P crop after plane removal is level 'full'; 'half' and 'quarter' are made from it by "
    "decimate_fourier (primary) and by subsample (control). TDF levels are made from the normal map per component "
    "by decimate_normals (S5.4); the finest level is the input itself (patch with alpha dropped, central 1024 block of "
    "the tiled map) and is not re-encoded.",
    "TDF float variant: the decoded normals n = rgb/255 * 2 - 1 of each level, renormalised (no further rounding).",
    "centroid_band_power uses K = P/8. At the quarter level K equals n/2; the bin at -n/2 along an axis is kept by "
    "decimate_fourier and its partner at +n/2 is not, so the retained bins on the circle rho = n/2 are not exactly "
    "the same as at the finer levels (noted before the computation, in relation to P-V3).",
    "Operational criteria (fixed in this script before the computation): 'increases (decreases) when the grid is "
    "coarsened' means strictly monotone over full, half, quarter for the measurement; 'the change of hf_ratio_phys "
    "is smaller' compares |quarter - full| per measurement; 'fewer flips' compares the main counts (pairs from "
    "different containers, all three pairs of levels); P-V3 'up to rounding' means a relative range over the three "
    "levels of at most 1e-9.",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_inputs(c) -> tuple[list, list]:
    """Locate every input file and check its SHA-256 against the conditions. Stops on any mismatch."""
    ch, tdf = c["datasets"]
    mpaths, tpaths, bad = [], [], []
    for m in ch["measurements"]:
        hits = list(CHALLENGE_DIR.glob(f"*/{m['container']}/{m['file']}"))
        if len(hits) != 1 or sha(hits[0]) != m["sha256"]:
            bad.append(f"{m['container']}/{m['file']}")
        mpaths.append(hits[0] if hits else None)
    for f in tdf["files"]:
        p = TDF_DIR / f["file"]
        if not p.exists() or sha(p) != f["sha256"]:
            bad.append(f["file"])
        tpaths.append(p)
    if bad:
        raise SystemExit(f"input files missing or with a different SHA-256: {bad}")
    return mpaths, tpaths


def challenge_values(m: dict, path: Path) -> list[dict]:
    z, dx, dy = read_challenge(path)
    P = largest_pow2(min(z.shape))
    if P != m["P"]:
        raise SystemExit(f"P differs from the conditions for {m['file']}")
    spacing = (dx + dy) / 2
    L = P * spacing
    Z = remove_plane(central_crop(z, P))
    rows = []
    for method in ("decimate_fourier", "subsample"):
        for lev, n in zip(LEVELS, (P, P // 2, P // 4)):
            Zn = Z if n == P else (decimate_fourier(Z, n) if method == "decimate_fourier" else subsample(Z, n))
            if n == P and method == "subsample":
                continue  # the full level is the same array for both methods
            rgb = normal_rgb_from_height(Zn, L)
            v = normal_from_height(Zn, L)
            cen = spectral_centroids(Zn, P / 8)
            vals = {"hf_ratio_px": hf_ratio(rgb, 120.0), "hf_ratio_phys": hf_ratio(rgb, 120.0 * n / P),
                    "hf_ratio_px_float": hf_ratio_float(v, 120.0),
                    "centroid_amp": cen["centroid_amp"],
                    "centroid_amp_hann": spectral_centroids(windowed(Zn), P / 8)["centroid_amp"],
                    "centroid_band_power": cen["centroid_band_power"], "sq": rq(Zn)}
            rows.append({"dataset": "challenge", "id": f"{m['container']}/{m['file']}", "container": m["container"],
                         "surface": m["surface"], "level": lev, "n": n, "P": P, "method": method, "values": vals})
    for r in rows:
        if r["level"] == "full":
            r2 = dict(r, method="subsample")
            rows.append(r2)
            break
    return rows


def tdf_values(f: dict, path: Path) -> list[dict]:
    rgb = read_normal_png(path)
    kind = "patch" if f["file"].endswith("normal_patch.png") else "tiled"
    if kind == "tiled":
        rgb = central_crop(rgb, 1024)
    n0 = rgb.shape[0]
    rows = []
    for lev, n in zip(LEVELS, (n0, n0 // 2, n0 // 4)):
        r = rgb if n == n0 else decimate_normals(rgb, n)
        v = r.astype(float) / 255 * 2 - 1
        v = v / np.linalg.norm(v, axis=-1, keepdims=True)
        vals = {"hf_ratio_px": hf_ratio(r, 120.0), "hf_ratio_phys": hf_ratio(r, 120.0 * n / n0),
                "hf_ratio_px_float": hf_ratio_float(v, 120.0), "hf_ratio_phys_float": hf_ratio_float(v, 120.0 * n / n0)}
        rows.append({"dataset": "tdf", "id": f["file"], "container": f["file"].split("/")[0], "input": kind,
                     "level": lev, "n": n, "P": n0, "method": "decimate_fourier", "values": vals})
    return rows


def compute(c) -> list[dict]:
    mpaths, tpaths = check_inputs(c)
    ch, tdf = c["datasets"]
    rows = []
    for m, p in zip(ch["measurements"], mpaths):
        rows += challenge_values(m, p)
    for f, p in zip(tdf["files"], tpaths):
        rows += tdf_values(f, p)
    return rows


# --- analysis -------------------------------------------------------------------------------------------------------


def values_by(rows, dataset, method, desc, ids):
    idx = {(r["id"], r["level"]): r["values"][desc] for r in rows if r["dataset"] == dataset and r["method"] == method}
    return np.array([[idx[(i, lev)] for lev in LEVELS] for i in ids])  # measurements, levels


def flip_summary(X, ids, containers, pair_filter=None) -> dict:
    """V2: flips for every pair of levels, split into pairs from different containers (main) and from the same container."""
    n = len(ids)
    allpairs = [(a, b) for a, b in combinations(range(n), 2) if pair_filter is None or pair_filter(a, b)]
    diff = [(a, b) for a, b in allpairs if containers[a] != containers[b]]
    same = [(a, b) for a, b in allpairs if containers[a] == containers[b]]
    out = {"level_pairs": []}
    for i, j in combinations(range(len(LEVELS)), 2):
        fd = flips_relative(X[:, i], X[:, j], THRESHOLD, ids, diff)
        fs = flips_relative(X[:, i], X[:, j], THRESHOLD, ids, same)
        out["level_pairs"].append({"levels": [LEVELS[i], LEVELS[j]], "flips_main": len(fd), "flips_same_container": len(fs),
                                   "pairs_main": len(diff), "pairs_same_container": len(same),
                                   "tau": kendall_tau(X[:, i], X[:, j]), "examples": fd[:5]})
    out["flips_main"] = sum(x["flips_main"] for x in out["level_pairs"])
    out["flips_same_container"] = sum(x["flips_same_container"] for x in out["level_pairs"])
    return out


def analyse(c, rows) -> dict:
    ch, tdf = c["datasets"]
    S = {"challenge": {}, "tdf": {}}
    ids = [f"{m['container']}/{m['file']}" for m in ch["measurements"]]
    cont = [m["container"] for m in ch["measurements"]]
    surf = [m["surface"] for m in ch["measurements"]]
    descs = list(next(r for r in rows if r["dataset"] == "challenge")["values"])
    for method in ("decimate_fourier", "subsample"):
        for d in descs:
            X = values_by(rows, "challenge", method, d, ids)
            mixed = lambda a, b: surf[a] != surf[b]
            S["challenge"][f"{method}/{d}"] = {
                "values": X.tolist(),
                "V1_quarter_minus_full": (X[:, 2] - X[:, 0]).tolist(),
                "V2": flip_summary(X, ids, cont),
                "V3": flip_summary(X, ids, cont, mixed)}
    S["challenge"]["V4"] = {}
    for d in descs:
        a = values_by(rows, "challenge", "decimate_fourier", d, ids)
        b = values_by(rows, "challenge", "subsample", d, ids)
        S["challenge"]["V4"][d] = {"rel_diff_half": (np.abs(b[:, 1] - a[:, 1]) / np.abs(a[:, 1])).tolist(),
                                   "rel_diff_quarter": (np.abs(b[:, 2] - a[:, 2]) / np.abs(a[:, 2])).tolist()}
    tids = [f["file"] for f in tdf["files"]]
    tcont = [i.split("/")[0] for i in tids]
    for kind in ("patch", "tiled"):
        sel = [k for k, i in enumerate(tids) if (kind == "patch") == i.endswith("normal_patch.png")]
        for d in ("hf_ratio_px", "hf_ratio_phys", "hf_ratio_px_float", "hf_ratio_phys_float"):
            X = values_by(rows, "tdf", "decimate_fourier", d, [tids[k] for k in sel])
            S["tdf"][f"{kind}/{d}"] = {"ids": [tids[k] for k in sel], "values": X.tolist(),
                                       "V1_quarter_minus_full": (X[:, 2] - X[:, 0]).tolist(),
                                       "V2": flip_summary(X, [tids[k] for k in sel], [tcont[k] for k in sel])}
    S["predictions"] = predictions(S, ids)
    return S


def mono(X, inc=True):
    d = np.diff(np.asarray(X), axis=1)
    return (d > 0).all(axis=1) if inc else (d < 0).all(axis=1)


def predictions(S, ids) -> dict:
    C = S["challenge"]
    P = {}
    px = np.array(C["decimate_fourier/hf_ratio_px"]["values"])
    ph = np.array(C["decimate_fourier/hf_ratio_phys"]["values"])
    inc = mono(px)
    smaller = np.abs(ph[:, 2] - ph[:, 0]) < np.abs(px[:, 2] - px[:, 0])
    P["P-V1"] = [{"part": "hf_ratio_px increases when coarsened", "measurements": int(inc.sum()), "of": len(ids),
                  "not": [ids[k] for k in np.where(~inc)[0]], "holds": bool(inc.all())},
                 {"part": "|change| phys < |change| px", "measurements": int(smaller.sum()), "of": len(ids),
                  "holds": bool(smaller.all())}]
    fpx = C["decimate_fourier/hf_ratio_px"]["V2"]["flips_main"]
    fph = C["decimate_fourier/hf_ratio_phys"]["V2"]["flips_main"]
    P["P-V2"] = [{"part": "hf_ratio_px has at least one flip", "flips_px": fpx, "holds": fpx >= 1},
                 {"part": "hf_ratio_phys has fewer flips", "flips_px": fpx, "flips_phys": fph, "holds": fph < fpx}]
    bp = np.array(C["decimate_fourier/centroid_band_power"]["values"])
    rr = (bp.max(axis=1) - bp.min(axis=1)) / bp.mean(axis=1)
    rr_fh = np.abs(bp[:, 1] - bp[:, 0]) / bp[:, 0]
    P["P-V3"] = [{"part": "centroid_band_power grid-independent (three levels)", "max_rel_range": float(rr.max()),
                  "holds": bool(rr.max() <= 1e-9)},
                 {"part": "same, full and half only (K < n/2)", "max_rel_range": float(rr_fh.max()),
                  "holds": bool(rr_fh.max() <= 1e-9)}]
    ca = np.array(C["decimate_fourier/centroid_amp"]["values"])
    dec = mono(ca, inc=False)
    P["P-V4"] = [{"part": "centroid_amp decreases when coarsened", "measurements": int(dec.sum()), "of": len(ids),
                  "holds": bool(dec.all())},
                 {"part": "flips of centroid_amp (not predicted)", "flips_main": C["decimate_fourier/centroid_amp"]["V2"]["flips_main"],
                  "holds": True}]
    items = []
    for kind in ("patch", "tiled"):
        X = np.array(S["tdf"][f"{kind}/hf_ratio_px"]["values"])
        ok = mono(X)
        items.append({"part": f"tdf {kind}: hf_ratio_px increases when coarsened", "inputs": int(ok.sum()),
                      "of": len(X), "holds": bool(ok.all())})
        items.append({"part": f"tdf {kind}: flips of hf_ratio_px (not predicted)",
                      "flips_main": S["tdf"][f"{kind}/hf_ratio_px"]["V2"]["flips_main"], "holds": True})
    P["P-V5"] = items
    return P


# --- report ---------------------------------------------------------------------------------------------------------


def g(x):
    if isinstance(x, float):
        return f"{x:.4g}"
    if isinstance(x, list):
        return ", ".join(g(v) for v in x) if x else "-"
    return str(x)


def write_report(c, meta, S, rows) -> str:
    ch, tdf = c["datasets"]
    L = ["# Validation 3 on public measured data", "",
         f"Conditions: `experiments/conditions/validation3_public.json` (SHA-256 `{meta['conditions_sha256']}`). "
         f"Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `{meta['spec_sha256']}`). "
         f"numpy {meta['numpy']}, scipy {meta['scipy']}, Python {meta['python']}. Run started {meta['started']} and "
         f"finished {meta['finished']} ({meta['platform']}). The SHA-256 of all {len(ch['measurements'])} Challenge "
         f"files and {len(tdf['files'])} TactileDreamFusion files agreed with the conditions before any value was read.", "",
         "Interpretation: robustness to resampling of one measurement on a fixed physical domain, not re-measurement "
         "with different instruments. No claim is made about the conclusions of other studies. Data sources and "
         f"licences: {ch['source']}; {ch['license']} {tdf['source']}; {tdf['license']}", "",
         "## Reading of the conditions fixed before the run", ""]
    L += [f"- {s}" for s in INTERPRETATION]
    L += ["", "## Predictions", ""]
    for key, items in S["predictions"].items():
        text = [x for x in c["predictions"] if x.startswith(key + " ") or x.startswith(key + ":")][0]
        L += [f"### {key}: {sum(i['holds'] for i in items)} of {len(items)} items hold", "", f"Prediction: {text}", ""]
        cols = list(dict.fromkeys(k for i in items for k in i if k != "holds"))
        L += ["| " + " | ".join(cols) + " | holds |", "|" + "---|" * (len(cols) + 1)]
        for i in items:
            L.append("| " + " | ".join(g(i.get(k, "-")) for k in cols) + f" | {'yes' if i['holds'] else 'no'} |")
        L.append("")
    L += ["## V2 and V3: flips (Challenge)", "",
          "Main count: pairs from different containers; pairs from the same container are reported separately and not "
          f"counted as independent. Threshold: relative difference above {THRESHOLD} at both levels.", "",
          "| method / descriptor | flips (main) | flips (same container) | V3 flips rougher vs smoother (main) | "
          "tau full-half, full-quarter, half-quarter |", "|---|---|---|---|---|"]
    for k, v in S["challenge"].items():
        if k == "V4":
            continue
        L.append(f"| {k} | {v['V2']['flips_main']} | {v['V2']['flips_same_container']} | {v['V3']['flips_main']} | "
                 f"{', '.join(f'{x['tau']:.3f}' for x in v['V2']['level_pairs'])} |")
    L += ["", "## V2: flips (TactileDreamFusion)", "", "| input / descriptor | flips (main) | flips (same object) | tau |",
          "|---|---|---|---|"]
    for k, v in S["tdf"].items():
        L.append(f"| {k} | {v['V2']['flips_main']} | {v['V2']['flips_same_container']} | "
                 f"{', '.join(f'{x['tau']:.3f}' for x in v['V2']['level_pairs'])} |")
    L += ["", "## V1 and V4: values by level (Challenge)", "",
          "Values at full, half and quarter (decimate_fourier), and the relative difference of subsample from "
          "decimate_fourier at half and quarter (V4).", "",
          "| measurement | surface | P | hf_ratio_px | hf_ratio_phys | centroid_amp | centroid_band_power | V4 hf_ratio_px | V4 centroid_amp |",
          "|---|---|---|---|---|---|---|---|---|"]
    ids = [f"{m['container']}/{m['file']}" for m in ch["measurements"]]
    C = S["challenge"]
    for k, (i, m) in enumerate(zip(ids, ch["measurements"])):
        L.append(f"| {i} | {m['surface']} | {m['P']} | {g(C['decimate_fourier/hf_ratio_px']['values'][k])} | "
                 f"{g(C['decimate_fourier/hf_ratio_phys']['values'][k])} | {g(C['decimate_fourier/centroid_amp']['values'][k])} | "
                 f"{g(C['decimate_fourier/centroid_band_power']['values'][k])} | "
                 f"{g([C['V4']['hf_ratio_px']['rel_diff_half'][k], C['V4']['hf_ratio_px']['rel_diff_quarter'][k]])} | "
                 f"{g([C['V4']['centroid_amp']['rel_diff_half'][k], C['V4']['centroid_amp']['rel_diff_quarter'][k]])} |")
    L += ["", "## V1: values by level (TactileDreamFusion)", "", "| input | hf_ratio_px | hf_ratio_phys | hf_ratio_px_float |",
          "|---|---|---|---|"]
    for kind in ("patch", "tiled"):
        T = S["tdf"]
        for k, i in enumerate(T[f"{kind}/hf_ratio_px"]["ids"]):
            L.append(f"| {i} | {g(T[f'{kind}/hf_ratio_px']['values'][k])} | {g(T[f'{kind}/hf_ratio_phys']['values'][k])} | "
                     f"{g(T[f'{kind}/hf_ratio_px_float']['values'][k])} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="rewrite the results from the saved values")
    args = ap.parse_args()
    c = json.loads(COND.read_text())
    js = OUT / f"{NAME}.json"
    if args.report:
        saved = json.loads(js.read_text())
        meta, rows = saved["meta"], saved["rows"]
    else:
        import scipy

        meta = {"conditions_sha256": sha(COND), "spec_sha256": sha(SPEC), "numpy": np.__version__,
                "scipy": scipy.__version__, "python": sys.version.split()[0],
                "platform": f"{platform.system()} {platform.machine()}, {os.cpu_count()} logical CPUs",
                "started": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        rows = compute(c)
        meta["finished"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if meta["conditions_sha256"] != sha(COND) or meta["spec_sha256"] != sha(SPEC):
        raise SystemExit("conditions or specification changed since the values were computed")
    S = analyse(c, rows)
    OUT.mkdir(exist_ok=True)
    js.write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION, "summary": S, "rows": rows}))
    (OUT / f"{NAME}.md").write_text(write_report(c, meta, S, rows))
    print("done")


if __name__ == "__main__":
    main()
