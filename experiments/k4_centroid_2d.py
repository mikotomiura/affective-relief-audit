"""K4 (b)-(d): growth of the amplitude-weighted frequency centroid with the grid size N.

Usage:  uv run python experiments/k4_centroid_2d.py            (compute, then write the results)
        uv run python experiments/k4_centroid_2d.py --report   (rewrite the results from results/k4_centroid_2d.json)
Conditions: experiments/conditions/k4_centroid_2d.json (fixed and committed before this script was run)
Specification: experiments/spec/generator-and-descriptors.md
Output: results/k4_centroid_2d.json (all values and the derived summaries) and results/k4_centroid_2d.md

Every computed cell is listed in the conditions file. Where the conditions leave a choice open, the choice is stated
in INTERPRETATION below and in the results; it was fixed in this script before the computation was run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from atact.descriptors import spectral_centroids, spectral_centroids_1d, windowed_1d
from atact.field import procedural_field_separable, sine_1d
from atact.spectral import decimate_fourier, windowed
from atact.stats import bonferroni_level, local_slopes, log_corrected_fit, slopes_per_seed, t_interval
from atact.transform import t_gamma

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "k4_centroid_2d.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
OUT = ROOT / "results"
NAME = "k4_centroid_2d"
K_BAND = 32.0  # descriptors: centroid_band_power with K = 32 cycles per domain
DESCRIPTORS = ("centroid_amp", "centroid_power", "centroid_band_power")
PROCESSINGS = ("raw", "hann")
TOL_SLOPE = 0.05  # operational tolerance for "close to" / "tends to" in the predictions (see INTERPRETATION)
TOL_FLAT = 1e-9   # relative range across N regarded as "does not depend on N" (rounding)
SENSITIVITY_N = [1024, 2048, 4096]  # rejection_criterion.sensitivity: "N in {1024, 2048, 4096}"

INTERPRETATION = [
    "Decision rule of the rejection criterion: the decision ('rejected' if at least one adjusted interval excludes "
    "e(gamma), 'consistent' if all contain it) is made separately on the primary range (N 512-4096) and on the "
    "sensitivity range (N 1024-4096). If the two agree, that is the outcome; if they differ, the outcome is 'not "
    "decidable in this N range'. The decision on the primary range alone is reported beside it. (The condition file "
    "states the 'rejected' rule on the primary range and the 'not decidable' rule for differing decisions; the two "
    "overlap when only the primary range rejects. This reading was fixed before the computation.)",
    "oned: the height is T_gamma of the sine (no normalisation; the centroid is scale-invariant). 'hann' for oned is "
    "the one-dimensional window w(i) = sin^2(pi i/N) (the analogue of S3.1), and centroid_power and "
    "centroid_band_power for oned use |k| in place of rho (the analogue of S2.4). Only the raw centroid_amp of oned "
    "enters a prediction (P-K4-1).",
    "Aliasing subset: the fine array is H = T_gamma(F) on the grid of side rN with the same seed and window (F with "
    "maxabs normalisation over the fine grid; the centroid does not depend on the normalisation constant), reduced "
    "to side N by decimate_fourier; both processings and all three descriptors are computed on the reduced array.",
    "Operational criteria for the predictions (the condition file states directions; the thresholds below were "
    f"fixed in this script before the computation): 'close to' an exponent means within {TOL_SLOPE} of it; 'the "
    f"local slope tends to 0' means that the magnitude of the mean local slope between the two largest N is below "
    f"{TOL_SLOPE} and below its magnitude between the two smallest N; 'does not depend on N' means that the "
    f"relative range over N of every seed is at most {TOL_FLAT}. Slopes are those of the primary range (N 512-4096) "
    "with 95% t intervals over seeds unless stated otherwise.",
]


def load_conditions() -> dict:
    return json.loads(COND.read_text())


def jobs_from(c: dict) -> list[tuple]:
    """All cells of the condition file. A job is (field, f, gamma, N, seed, sampling, r, normalize)."""
    fs = c["f_integer"] + c["f_noninteger"]
    jobs = []
    for field in ("sum", "product1", "oned"):
        for f in fs:
            for g in c["gamma"]:
                for n in c["grids_N"]:
                    for seed in c["seeds"]:
                        jobs.append((field, f, g, n, seed, "direct", 1, "maxabs"))
    # normalisation_check: sum, f in {5, 5.5}, gamma in {0.9, 1.75}, seeds 1-5, every N, ampsum
    for f in (5, 5.5):
        for g in (0.9, 1.75):
            for n in c["grids_N"]:
                for seed in c["seeds"][:5]:
                    jobs.append(("sum", f, g, n, seed, "direct", 1, "ampsum"))
    # aliasing subset: sum, f in {5, 5.5}, all gamma, seeds 1-10; r = 2 for every N, r = 4 for N <= 2048
    for f in (5, 5.5):
        for g in c["gamma"]:
            for n in c["grids_N"]:
                for seed in c["seeds"][:10]:
                    jobs.append(("sum", f, g, n, seed, "decimate", 2, "maxabs"))
                    if n <= 2048:
                        jobs.append(("sum", f, g, n, seed, "decimate", 4, "maxabs"))
    return jobs


def run_job(job: tuple) -> dict:
    field, f, g, n, seed, sampling, r, norm = job
    if field == "oned":
        z = t_gamma(sine_1d(f, n, seed), g)
        vals = {"raw": spectral_centroids_1d(z, K_BAND), "hann": spectral_centroids_1d(windowed_1d(z), K_BAND)}
    else:
        octaves = 4 if field == "sum" else 1
        m = n * r
        H = t_gamma(procedural_field_separable(f, m, seed, octaves, normalize=norm), g)
        if sampling == "decimate":
            H = decimate_fourier(H, n)
        raw = spectral_centroids(H, K_BAND)
        H = windowed(H)
        vals = {"raw": raw, "hann": spectral_centroids(H, K_BAND)}
    return {"field": field, "f": f, "gamma": g, "N": n, "seed": seed, "sampling": sampling, "r": r,
            "normalize": norm, "values": vals}


def memory_class(job: tuple) -> str:
    """Fine side M = rN: M = 8192 needs about 4 GB per process, M = 4096 about 1.5 GB (measured on a test seed)."""
    field, _, _, n, _, _, r, _ = job
    m = n * r if field != "oned" else 0
    return "xl" if m >= 8192 else ("l" if m >= 4096 else "s")


WORKERS = {"xl": 2, "l": 5, "s": 8}


def compute(c: dict) -> list[dict]:
    jobs = jobs_from(c)
    rows = []
    for cls in ("xl", "l", "s"):
        part = [j for j in jobs if memory_class(j) == cls]
        part.sort(key=lambda j: -j[3] * j[6])
        t0 = time.time()
        with ProcessPoolExecutor(max_workers=WORKERS[cls]) as ex:
            rows += list(ex.map(run_job, part, chunksize=1 if cls != "s" else 8))
        print(f"[{cls}] {len(part)} jobs in {time.time() - t0:.0f} s", flush=True)
    return rows


# --- analysis -------------------------------------------------------------------------------------------------------


def series(rows, field, f, g, proc, desc, Ns, seeds, sampling="direct", r=1, norm="maxabs") -> np.ndarray:
    """Array (seeds, N) of one descriptor."""
    idx = {(x["seed"], x["N"]): x for x in rows
           if x["field"] == field and x["f"] == f and x["gamma"] == g and x["sampling"] == sampling
           and x["r"] == r and x["normalize"] == norm}
    return np.array([[idx[(s, n)]["values"][proc][desc] for n in Ns] for s in seeds])


def slope_summary(N, C, level=0.95) -> dict:
    sl = slopes_per_seed(N, C)
    out = t_interval(sl, level)
    ls = local_slopes(N, C)
    out["local_mean"] = ls.mean(axis=0).tolist()
    out["local_se"] = (ls.std(axis=0, ddof=1) / np.sqrt(ls.shape[0])).tolist()
    return out


def e_gamma(g: float) -> float:
    return min(1.0, 1.5 - 1.0 / g)


def analyse(c: dict, rows: list[dict]) -> dict:
    seeds = c["seeds"]
    Nall = c["grids_N"]
    Np = c["slope_ranges"]["primary"]
    Ns = c.get("_sensitivity_N", SENSITIVITY_N)
    fs = c["f_integer"] + c["f_noninteger"]
    S = {"cells": []}
    # slopes for every direct cell
    for field in ("sum", "product1", "oned"):
        for f in fs:
            for g in c["gamma"]:
                for proc in PROCESSINGS:
                    for desc in DESCRIPTORS:
                        C = series(rows, field, f, g, proc, desc, Nall, seeds)
                        ip = [Nall.index(n) for n in Np]
                        cell = {"field": field, "f": f, "gamma": g, "processing": proc, "descriptor": desc,
                                "mean_by_N": C.mean(axis=0).tolist(),
                                "se_by_N": (C.std(axis=0, ddof=1) / np.sqrt(len(seeds))).tolist(),
                                "rel_range_max": float(((C.max(axis=1) - C.min(axis=1)) / C.mean(axis=1)).max()),
                                "slope_primary": slope_summary(Np, C[:, ip]),
                                "slope_descriptive": slope_summary(Nall, C)}
                        if field != "oned" and proc == "raw" and desc == "centroid_amp":
                            i0 = Nall.index(256)
                            fit = log_corrected_fit(Nall[i0:], C[:, i0:])
                            cell["log_corrected"] = {"b": t_interval(fit[:, 1]), "c": t_interval(fit[:, 2])}
                        S["cells"].append(cell)
    S["rejection"] = rejection(c, rows, Np, Ns)
    S["normalisation_check"] = normalisation_check(c, rows)
    S["aliasing"] = aliasing(c, rows)
    S["c_lnN_over_N"] = c_lnN_over_N(c, rows)
    S["predictions"] = predictions(c, S)
    return S


def find(S, **kw) -> dict:
    hits = [x for x in S["cells"] if all(x[k] == v for k, v in kw.items())]
    assert len(hits) == 1, kw
    return hits[0]


def rejection(c, rows, Np, Ns, sampling="direct", r=1, fs=(3, 5, 7), seeds=None) -> dict:
    seeds = seeds or c["seeds"]
    gammas = [0.9, 1.25, 1.75, 2.6]
    m = len(fs) * len(gammas)
    level = bonferroni_level(12)
    out = {"level": level, "m": m, "cells": []}
    dec = {}
    for rng_name, Nr in (("primary", Np), ("sensitivity", Ns)):
        excl = []
        for f in fs:
            for g in gammas:
                C = series(rows, "sum", f, g, "raw", "centroid_amp", Nr, seeds, sampling, r)
                t = t_interval(slopes_per_seed(Nr, C), level)
                e = e_gamma(g)
                inside = t["lo"] <= e <= t["hi"]
                direction = None if inside else ("above" if t["lo"] > e else "below")
                out["cells"].append({"range": rng_name, "f": f, "gamma": g, "e": e, **t, "contains": inside,
                                     "direction": direction})
                excl.append(not inside)
        dec[rng_name] = "rejected" if any(excl) else "consistent"
    out["decision_primary"] = dec["primary"]
    out["decision_sensitivity"] = dec["sensitivity"]
    out["outcome"] = dec["primary"] if dec["primary"] == dec["sensitivity"] else "not decidable in this N range"
    return out


def normalisation_check(c, rows) -> dict:
    worst = 0.0
    for f in (5, 5.5):
        for g in (0.9, 1.75):
            for proc in PROCESSINGS:
                for desc in DESCRIPTORS:
                    a = series(rows, "sum", f, g, proc, desc, c["grids_N"], c["seeds"][:5])
                    b = series(rows, "sum", f, g, proc, desc, c["grids_N"], c["seeds"][:5], norm="ampsum")
                    worst = max(worst, float(np.abs(a / b - 1).max()))
    return {"max_rel_diff": worst, "agree_to_rounding": worst <= 1e-9}


def aliasing(c, rows) -> dict:
    seeds = c["seeds"][:10]
    out = {"paired": [], "r2_vs_r4": [], "secondary_rejection": None}
    for f in (5, 5.5):
        for g in c["gamma"]:
            for proc in PROCESSINGS:
                for desc in DESCRIPTORS:
                    d = series(rows, "sum", f, g, proc, desc, c["grids_N"], seeds)
                    r2 = series(rows, "sum", f, g, proc, desc, c["grids_N"], seeds, "decimate", 2)
                    diff = r2 - d
                    out["paired"].append({"f": f, "gamma": g, "processing": proc, "descriptor": desc,
                                          "mean_diff_by_N": diff.mean(axis=0).tolist(),
                                          "se_by_N": (diff.std(axis=0, ddof=1) / np.sqrt(len(seeds))).tolist(),
                                          "rel_mean_diff_by_N": (diff.mean(axis=0) / d.mean(axis=0)).tolist()})
                    N4 = [n for n in c["grids_N"] if n <= 2048]
                    r2b = series(rows, "sum", f, g, proc, desc, N4, seeds, "decimate", 2)
                    r4 = series(rows, "sum", f, g, proc, desc, N4, seeds, "decimate", 4)
                    out["r2_vs_r4"].append({"f": f, "gamma": g, "processing": proc, "descriptor": desc, "N": N4,
                                            "rel_mean_diff_by_N": ((r4 - r2b).mean(axis=0) / r2b.mean(axis=0)).tolist()})
    Np = c["slope_ranges"]["primary"]
    Ns = c.get("_sensitivity_N", SENSITIVITY_N)
    out["secondary_rejection"] = rejection(c, rows, Np, Ns, "decimate", 2, fs=(5,), seeds=seeds)
    direct_f5 = rejection(c, rows, Np, Ns, "direct", 1, fs=(5,), seeds=seeds)
    out["direct_same_seeds_f5"] = direct_f5
    return out


def c_lnN_over_N(c, rows) -> list[dict]:
    out = []
    N = np.array(c["grids_N"], dtype=float)
    for field in ("sum", "product1", "oned"):
        for f in c["f_noninteger"]:
            C = series(rows, field, f, 1.0, "raw", "centroid_amp", c["grids_N"], c["seeds"])
            v = C * np.log(N) / N
            out.append({"field": field, "f": f, "mean_by_N": v.mean(axis=0).tolist()})
    return out


def _tends_to_zero(cell) -> bool:
    ls = cell["slope_descriptive"]["local_mean"]
    return abs(ls[-1]) < TOL_SLOPE and abs(ls[-1]) < abs(ls[0])


def predictions(c, S) -> dict:
    P = {}
    ints, nonints = c["f_integer"], c["f_noninteger"]
    # P-K4-1
    items = []
    for f in ints:
        for g in c["gamma"]:
            cell = find(S, field="oned", f=f, gamma=g, processing="raw", descriptor="centroid_amp")
            sp = cell["slope_primary"]
            if g > 1:
                target = 1 - 1 / g
                ok = (sp["lo"] <= target <= sp["hi"]) or abs(cell["slope_descriptive"]["local_mean"][-1] - target) < TOL_SLOPE
            elif g == 1:
                target = 0.0
                ok = cell["rel_range_max"] <= TOL_FLAT or sp["lo"] <= 0 <= sp["hi"]
            else:
                target = 0.0
                ok = _tends_to_zero(cell)
            items.append({"f": f, "gamma": g, "target": target, "slope": sp["mean"], "lo": sp["lo"], "hi": sp["hi"],
                          "local_last": cell["slope_descriptive"]["local_mean"][-1], "holds": bool(ok)})
    P["P-K4-1"] = {"items": items, "holds": all(i["holds"] for i in items)}
    # P-K4-2 (gamma != 1; the one-dimensional exponent is max(0, 1 - 1/gamma), compared also with the measured oned slope)
    items = []
    for f in ints:
        for g in c["gamma"]:
            if g == 1:
                continue
            sp = find(S, field="product1", f=f, gamma=g, processing="raw", descriptor="centroid_amp")["slope_primary"]
            so = find(S, field="oned", f=f, gamma=g, processing="raw", descriptor="centroid_amp")["slope_primary"]
            target = max(0.0, 1 - 1 / g)
            items.append({"f": f, "gamma": g, "target": target, "slope": sp["mean"], "lo": sp["lo"], "hi": sp["hi"],
                          "oned_slope": so["mean"], "holds": bool(abs(sp["mean"] - target) <= TOL_SLOPE)})
    P["P-K4-2"] = {"items": items, "holds": all(i["holds"] for i in items)}
    # P-K4-3
    items = []
    for f in ints:
        for g in c["gamma"]:
            if g == 1:
                continue
            sp = find(S, field="sum", f=f, gamma=g, processing="raw", descriptor="centroid_amp")["slope_primary"]
            so = find(S, field="oned", f=f, gamma=g, processing="raw", descriptor="centroid_amp")["slope_primary"]
            base = max(0.0, 1 - 1 / g)
            items.append({"f": f, "gamma": g, "oned_value": base, "oned_slope": so["mean"], "slope": sp["mean"],
                          "lo": sp["lo"], "hi": sp["hi"], "holds": bool(sp["lo"] > base and sp["lo"] > 0)})
    P["P-K4-3"] = {"items": items, "holds": all(i["holds"] for i in items),
                   "rejection_outcome": S["rejection"]["outcome"]}
    # P-K4-4
    items = []
    for field in ("sum", "product1"):
        for f in ints:
            cell = find(S, field=field, f=f, gamma=1.0, processing="raw", descriptor="centroid_amp")
            sp = cell["slope_descriptive"]
            items.append({"field": field, "f": f, "rel_range_max": cell["rel_range_max"], "slope": sp["mean"],
                          "lo": sp["lo"], "hi": sp["hi"],
                          "holds": bool(cell["rel_range_max"] <= TOL_FLAT and sp["lo"] <= 0 <= sp["hi"])})
    P["P-K4-4"] = {"items": items, "holds": all(i["holds"] for i in items),
                   "note": "Slopes over N 128-4096 (the band-limited case holds from N = 128)."}
    # P-K4-5
    items = []
    for field in ("sum", "product1"):
        for f in nonints:
            cell = find(S, field=field, f=f, gamma=1.0, processing="raw", descriptor="centroid_amp")
            ls = cell["slope_descriptive"]["local_mean"]
            sp = cell["slope_primary"]
            items.append({"field": field, "f": f, "slope": sp["mean"], "lo": sp["lo"], "hi": sp["hi"], "local": ls,
                          "holds": bool(sp["hi"] < 1 and ls[-1] > ls[0])})
    P["P-K4-5"] = {"items": items, "holds": all(i["holds"] for i in items)}
    # P-K4-6
    items = []
    for field in ("sum", "product1"):
        for g in c["gamma"]:
            hann_int = np.mean([find(S, field=field, f=f, gamma=g, processing="hann", descriptor="centroid_amp")
                                ["slope_primary"]["mean"] for f in ints])
            raw_int = np.mean([find(S, field=field, f=f, gamma=g, processing="raw", descriptor="centroid_amp")
                               ["slope_primary"]["mean"] for f in ints])
            for f in nonints:
                h = find(S, field=field, f=f, gamma=g, processing="hann", descriptor="centroid_amp")["slope_primary"]
                rw = find(S, field=field, f=f, gamma=g, processing="raw", descriptor="centroid_amp")["slope_primary"]
                closer = abs(h["mean"] - hann_int) < abs(rw["mean"] - raw_int) or abs(h["mean"] - hann_int) <= TOL_SLOPE
                items.append({"field": field, "f": f, "gamma": g, "hann_slope": h["mean"], "hann_int_slope": hann_int,
                              "raw_slope": rw["mean"], "raw_int_slope": raw_int,
                              "approaches": bool(closer), "smaller_than_raw": bool(h["hi"] < rw["lo"]),
                              "holds": bool(closer and h["hi"] < rw["lo"])})
    P["P-K4-6"] = {"items": items, "holds": all(i["holds"] for i in items),
                   "note": "'approaches': |hann slope (non-integer f) - mean hann slope (integer f)| is below the same "
                           f"distance for raw or below {TOL_SLOPE}; 'smaller than raw': the 95% intervals do not overlap."}
    # P-K4-7
    items = []
    for field in ("sum", "product1"):
        for g in c["gamma"]:
            for f in ints:
                cell = find(S, field=field, f=f, gamma=g, processing="raw", descriptor="centroid_power")
                items.append({"part": "power converges (integer f)", "field": field, "f": f, "gamma": g,
                              "local": cell["slope_descriptive"]["local_mean"], "holds": bool(_tends_to_zero(cell))})
            for f in nonints:
                cell = find(S, field=field, f=f, gamma=g, processing="raw", descriptor="centroid_power")
                m = np.array(cell["mean_by_N"])
                inc = np.diff(m) / np.diff(np.log(c["grids_N"]))
                ok = bool(np.all(inc > 0) and 0.5 <= inc[-1] / inc[0] <= 2)
                items.append({"part": "power ~ ln N (non-integer f)", "field": field, "f": f, "gamma": g,
                              "increments_per_lnN": inc.tolist(), "holds": ok})
        for f in ints:
            cell = find(S, field=field, f=f, gamma=1.0, processing="raw", descriptor="centroid_band_power")
            items.append({"part": "band power flat (gamma = 1, integer f)", "field": field, "f": f, "gamma": 1.0,
                          "rel_range_max": cell["rel_range_max"], "holds": bool(cell["rel_range_max"] <= TOL_FLAT)})
    P["P-K4-7"] = {"items": items, "holds": all(i["holds"] for i in items),
                   "note": "'grows roughly linearly in ln N': the increments of the seed mean per unit ln N are all "
                           "positive and the last is within a factor 2 of the first."}
    return P


# --- report ---------------------------------------------------------------------------------------------------------


def fmt(x, p=3):
    return f"{x:.{p}f}"


def write_report(c: dict, meta: dict, S: dict) -> str:
    L = ["# K4 in two dimensions: growth of the frequency centroid with the grid size", "",
         f"Conditions: `experiments/conditions/k4_centroid_2d.json` (SHA-256 `{meta['conditions_sha256']}`). "
         f"Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `{meta['spec_sha256']}`). "
         f"numpy {meta['numpy']}, scipy {meta['scipy']}, Python {meta['python']}. Run started {meta['started']} and "
         f"finished {meta['finished']} ({meta['platform']}).", "",
         "Nothing here is a proof. The intervals are over seeds and do not include the systematic bias of a finite "
         "N range; local slopes and the log-corrected fit are reported for that reason.", "",
         "## Reading of the conditions fixed before the run", ""]
    L += [f"- {s}" for s in INTERPRETATION]
    R = S["rejection"]
    L += ["", "## Rejection criterion (12 cells)", "",
          f"Simultaneous intervals: Bonferroni, level 1 - 0.05/12 = {R['level']:.5f}, t over {len(c['seeds'])} seeds.", "",
          f"- Decision on the primary range (N 512-4096): **{R['decision_primary']}**",
          f"- Decision on the sensitivity range (N 1024-4096): **{R['decision_sensitivity']}**",
          f"- Outcome: **{R['outcome']}**", "",
          "| range | f | gamma | e(gamma) | slope | adjusted interval | contains e | direction |",
          "|---|---|---|---|---|---|---|---|"]
    for x in R["cells"]:
        L.append(f"| {x['range']} | {x['f']} | {x['gamma']} | {fmt(x['e'], 4)} | {fmt(x['mean'], 4)} | "
                 f"[{fmt(x['lo'], 4)}, {fmt(x['hi'], 4)}] | {'yes' if x['contains'] else 'no'} | {x['direction'] or '-'} |")
    L += ["", "### Local slopes and log-corrected fit for the 12 cells (raw, centroid_amp, direct sampling)", "",
          "Local slopes are the means over seeds between consecutive N (128-256, ..., 2048-4096). The log-corrected fit "
          "is ln C = a + b ln N + c ln ln N over N 256-4096 (descriptive; mean and 95% interval over seeds).", "",
          "| f | gamma | local slopes | b | c |", "|---|---|---|---|---|"]
    for f in (3, 5, 7):
        for g in (0.9, 1.25, 1.75, 2.6):
            cell = find(S, field="sum", f=f, gamma=g, processing="raw", descriptor="centroid_amp")
            lc = cell["log_corrected"]
            L.append(f"| {f} | {g} | {', '.join(fmt(v) for v in cell['slope_descriptive']['local_mean'])} | "
                     f"{fmt(lc['b']['mean'])} [{fmt(lc['b']['lo'])}, {fmt(lc['b']['hi'])}] | "
                     f"{fmt(lc['c']['mean'])} [{fmt(lc['c']['lo'])}, {fmt(lc['c']['hi'])}] |")
    A = S["aliasing"]
    L += ["", "### Secondary analysis on the decimate_fourier version (f = 5, r = 2, seeds 1-10)", "",
          f"- decimate_fourier: primary {A['secondary_rejection']['decision_primary']}, sensitivity "
          f"{A['secondary_rejection']['decision_sensitivity']}, outcome {A['secondary_rejection']['outcome']}",
          f"- direct sampling, same cells and seeds: primary {A['direct_same_seeds_f5']['decision_primary']}, "
          f"sensitivity {A['direct_same_seeds_f5']['decision_sensitivity']}, outcome {A['direct_same_seeds_f5']['outcome']}",
          "", "| sampling | range | gamma | slope | adjusted interval | contains e |", "|---|---|---|---|---|---|"]
    for lab, rr in (("decimate r=2", A["secondary_rejection"]), ("direct", A["direct_same_seeds_f5"])):
        for x in rr["cells"]:
            L.append(f"| {lab} | {x['range']} | {x['gamma']} | {fmt(x['mean'], 4)} | [{fmt(x['lo'], 4)}, "
                     f"{fmt(x['hi'], 4)}] | {'yes' if x['contains'] else 'no'} |")
    L += ["", "## Predictions", ""]
    for key, p in S["predictions"].items():
        L += [f"### {key}: {sum(i['holds'] for i in p['items'])} of {len(p['items'])} items hold", ""]
        text = [x for x in c["predictions"] if x.startswith(key + " ")][0]
        L += [f"Prediction: {text}", ""]
        if "note" in p:
            L += [f"Criterion: {p['note']}", ""]
        if "rejection_outcome" in p:
            L += [f"Rejection criterion outcome: {p['rejection_outcome']}.", ""]
        keys = list(dict.fromkeys(k for i in p["items"] for k in i if k != "holds"))
        L += ["| " + " | ".join(keys) + " | holds |", "|" + "---|" * (len(keys) + 1)]
        for i in p["items"]:
            cells = []
            for k in keys:
                v = i.get(k, "-")
                cells.append(", ".join(fmt(u) for u in v) if isinstance(v, list) else (fmt(v) if isinstance(v, float) else str(v)))
            L.append("| " + " | ".join(cells) + f" | {'yes' if i['holds'] else 'no'} |")
        L.append("")
    NC = S["normalisation_check"]
    L += ["## Normalisation check (implementation control)", "",
          f"maxabs versus ampsum, sum field, f in {{5, 5.5}}, gamma in {{0.9, 1.75}}, seeds 1-5, every N, both "
          f"processings and all descriptors: largest relative difference {NC['max_rel_diff']:.2e} "
          f"({'agree to rounding' if NC['agree_to_rounding'] else 'DISAGREE: implementation error to be investigated'}).",
          "", "## Aliasing subset (sum, f in {5, 5.5}, seeds 1-10)", "",
          "Relative paired difference (decimate_fourier with r = 2 minus direct sampling, divided by the direct mean), "
          "raw processing, by N; and the residual of the reference (r = 4 minus r = 2, relative, N <= 2048).", "",
          "| f | gamma | descriptor | decimate - direct (relative), N 128 ... 4096 | r4 - r2 (relative), N 128 ... 2048 |",
          "|---|---|---|---|---|"]
    for x, y in zip(A["paired"], A["r2_vs_r4"]):
        if x["processing"] == "raw":
            L.append(f"| {x['f']} | {x['gamma']} | {x['descriptor']} | "
                     f"{', '.join(f'{v:+.2e}' for v in x['rel_mean_diff_by_N'])} | "
                     f"{', '.join(f'{v:+.2e}' for v in y['rel_mean_diff_by_N'])} |")
    L += ["", "## C ln N / N for gamma = 1 and non-integer f (check of P-K4-5)", "",
          "| field | f | N 128 ... 4096 |", "|---|---|---|"]
    for x in S["c_lnN_over_N"]:
        L.append(f"| {x['field']} | {x['f']} | {', '.join(fmt(v) for v in x['mean_by_N'])} |")
    L += ["", "## Slopes of every cell", "",
          "Primary range N 512-4096 (95% t interval over seeds) and descriptive range N 128-4096 (mean).", "",
          "| field | f | gamma | processing | descriptor | slope (primary) | interval | slope (128-4096) |",
          "|---|---|---|---|---|---|---|---|"]
    for x in S["cells"]:
        sp = x["slope_primary"]
        L.append(f"| {x['field']} | {x['f']} | {x['gamma']} | {x['processing']} | {x['descriptor']} | "
                 f"{fmt(sp['mean'], 4)} | [{fmt(sp['lo'], 4)}, {fmt(sp['hi'], 4)}] | "
                 f"{fmt(x['slope_descriptive']['mean'], 4)} |")
    L += ["", "## Seed means of the centroid by N", "",
          "| field | f | gamma | processing | descriptor | N 128 ... 4096 (mean; standard error of the last) |",
          "|---|---|---|---|---|---|"]
    for x in S["cells"]:
        L.append(f"| {x['field']} | {x['f']} | {x['gamma']} | {x['processing']} | {x['descriptor']} | "
                 f"{', '.join(fmt(v, 2) for v in x['mean_by_N'])} ({x['se_by_N'][-1]:.2g}) |")
    return "\n".join(L) + "\n"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="rewrite the results from the saved values")
    ap.add_argument("--smoke", metavar="DIR", help="run the whole pipeline on small grids and seeds outside the "
                    "conditions (101-103), writing to DIR; for testing the script only")
    args = ap.parse_args()
    c = load_conditions()
    out = OUT
    if args.smoke:
        c = dict(c, grids_N=[64, 128, 256, 512], seeds=[101, 102, 103], _sensitivity_N=[256, 512],
                 slope_ranges=dict(c["slope_ranges"], primary=[128, 256, 512]))
        out = Path(args.smoke)
    js = out / f"{NAME}.json"
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
    out.mkdir(exist_ok=True)
    js.write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION, "summary": S, "rows": rows}))
    (out / f"{NAME}.md").write_text(write_report(c, meta, S))
    print(f"outcome of the rejection criterion: {S['rejection']['outcome']}")


if __name__ == "__main__":
    main()
