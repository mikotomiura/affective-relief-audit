"""Paired comparison of edge and grid effects: for the same surface, only the crop position and the grid are varied.

Usage:  uv run python experiments/edge_grid_paired.py            (compute, then write the results)
        uv run python experiments/edge_grid_paired.py --report   (rewrite the results from results/edge_grid_paired.json)
Conditions: experiments/conditions/edge_grid_paired.json (fixed and committed before this script was run)
Specification: experiments/spec/generator-and-descriptors.md
Output: results/edge_grid_paired.json and results/edge_grid_paired.md

This design extends an earlier computation whose results had been seen (hf_ratio_edge.json; commits c2ee719 and
82efec2), so it is not blind to those results. Where the conditions leave a choice open, the choice is stated in
INTERPRETATION below and in the results; it was fixed in this script before the computation was run.
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
from itertools import combinations
from pathlib import Path

import numpy as np

from atact.descriptors import rq, spectral_centroids
from atact.field import procedural_field_separable, tone_amplitude_for_rms_slope, tone_surface
from atact.hfratio import hf_ratio, hf_ratio_float, normal_from_height, normal_rgb_from_height
from atact.mapping import params
from atact.spectral import (
    decimate_fourier,
    linear_hf_ratio,
    periodic_component,
    windowed,
    windowed_normals,
    windowed_normals_float,
)
from atact.stats import flips_seeded, kendall_tau
from atact.transform import t_gamma

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "edge_grid_paired.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
OUT = ROOT / "results"
NAME = "edge_grid_paired"
K_BAND = 32.0
Z_SCALE = 1 / 30  # hf_ratio.height_to_normals: z = H / 30 in units of L
N_REF = 1024      # phys cutoff: freq_threshold = 120 N / 1024
LEVELS = (-1.0, -0.5, 0.0, 0.5, 1.0)
FLIP_A = {"freqs": (2, 60), "ratios": (1.0, 0.316)}  # conditions version 3
FLIP_B = {"freqs": (8,), "ratios": (1.0,)}
FLIP_RMS_SLOPE = 0.01
HEIGHT_DESC = ("centroid_amp", "centroid_power", "centroid_band_power", "sq")
HF_CUTS = ("px", "phys")
HF_VARIANTS = ("uint8", "float", "linear_height")
PROCS = ("raw", "hann", "pplus")
FLIP_DETAIL = ("hf_px_raw_uint8", "hf_phys_raw_uint8", "centroid_amp_raw")  # keys whose flipped pairs are listed


def pack(rows: list[dict]) -> dict:
    """Columnar form of the rows for the results file (one list of values per descriptor)."""
    keys = sorted({k for r in rows for k in r["values"]})
    return {"index_fields": ["surface", "seed", "crop", "N", "sampling"],
            "index": [[r["surface"], r["seed"], r["crop"], r["N"], r["sampling"]] for r in rows],
            "values": {k: [r["values"].get(k) for r in rows] for k in keys}}


def unpack(t: dict) -> list[dict]:
    rows = []
    for i, (sf, seed, crop, n, sampling) in enumerate(t["index"]):
        vals = {k: v[i] for k, v in t["values"].items() if v[i] is not None}
        rows.append({"surface": sf, "seed": seed, "crop": crop, "N": n, "sampling": sampling, "values": vals})
    return rows

INTERPRETATION = [
    "Conditions version 3. The five points with A = 0.25 (f = 5.5) are surfaces like the rule points but are "
    "not among the 25 rule points used for C3, C4 and C5; they enter C1, C2, the aliasing subset and P-E2 to P-E5.",
    "flip_positive (version 3): surface a is z = c (sin(2 pi 2 x') + 0.316 sin(2 pi 60 x')) and surface b is "
    "z = c' sin(2 pi 8 x'), "
    "with x' = x + x0 (zero phases; the crop offset shifts the tones), constant along y, in units of L. The "
    "amplitudes c and c' give a continuous RMS slope of 0.01. The surfaces have no random element, so the ten seeds "
    "give identical values; their standard error is 0 and, by S6.2, any change of sign with a non-zero difference "
    "counts as a flip. Height descriptors of these surfaces are computed on z.",
    "Normal maps of the rule points and sine controls come from z = H/30 (S2.8 with side 1). The float variant uses "
    "the unit normals before the uint8 encoding; for 'hann' it applies the window of S3.1 to those normals and "
    "renormalises without rounding. The linear-height variant uses z itself: raw z, the windowed z of S3.1 for "
    "'hann', and the periodic component of S3.2 for 'pplus'.",
    "S6.2 order: the order of two surfaces at a level is the sign of the mean over seeds of sign(D_a - D_b); a flip "
    "also requires the mean paired difference to exceed twice its standard error over seeds at both levels.",
    "C3 is computed for each N and crop. The ratio (mean over seeds of C1) / C3 is reported for the C3 of each crop "
    "at the same N; the summary ratio uses the largest C3 over the crops (so that it is not inflated by a small C3). "
    "|C2| / C3 uses the C3 of the same crop at N = 2048, averaged over crops. C2 is the value at N = 2048 minus the "
    "value at N = 128 for each seed and crop; its mean and standard error are reported per crop (paired by seed), "
    "and the crop-averaged standard error is taken over the seed-level averages across crops (crops share seeds).",
    "C5: within each processing, the descriptors (the height descriptors computed under that processing, and the HF "
    "ratio in its two cutoffs and three variants under that processing) are ranked by the absolute standardised "
    "difference |d| between the corners (V, A) = (1, -1) and (-1, 1), d = (mean_a - mean_b) / sqrt((var_a + var_b)/2) "
    "over seeds; the signed d is reported. Whether the ranking changes is reported by counting distinct rankings.",
    "Operational criteria for the predictions (the condition file states directions; these were fixed in this script "
    "before the computation): P-E1 'below 1e-9 in relative terms' uses C1 and |C2| divided by the mean value; "
    "'decreases monotonically' uses the mean over seeds and crops at successive N; P-E2 holds at an N if, for each V, "
    "the mean C1 of the point (V, 0.25) exceeds that of the rule point (V, 0), and the mean C1 of sine_jump exceeds "
    "that of every rule point with A = 0; the prediction holds if this is so at every N; P-E3 holds if the mean C1 of "
    "at least one point with A = 0.25 exceeds C3 at N = 2048 for every crop (that is, the largest C3 over crops); "
    "P-E4 compares the mean C1 (absolute) of hann centroid_amp and of pplus centroid_amp with raw centroid_amp, and "
    "of centroid_band_power with raw centroid_power (the same weighting over the full band), for each of the five "
    "points with A = 0.25 at every N, and reports the comparison of C1 relative to the mean value beside it; P-E5 "
    "uses the 25 rule points, the five points with A = 0.25 and the two sine controls for the monotonicity and |C2| "
    "parts, and the flips of C4 (the 25 rule points, as defined in the conditions) for the flip parts, with uint8 raw "
    "for the HF ratio and flips counted over all pairs of grids within each crop; P-E6 compares the mean over seeds "
    "and crops of |decimated - direct| (absolute; the relative difference is reported beside it), noting that only "
    "the point (1, -1) has gamma <= 1; P-E7 requires a flip of the px linear ratio for every crop and no flip of the "
    "phys linear ratio for any crop.",
]


def surfaces() -> list[dict]:
    out = []
    for V in LEVELS:
        for A in LEVELS:
            f, s, g = params(V, A)
            out.append({"name": f"V{V:+.1f}_A{A:+.1f}", "kind": "rule", "V": V, "A": A, "f": float(f), "s": float(s),
                        "gamma": float(g), "octaves": 4})
    for V in LEVELS:  # surfaces_noninteger (version 2): A = 0.25, f = 5.5
        f, s, g = params(V, 0.25)
        out.append({"name": f"V{V:+.1f}_A+0.25", "kind": "nonint", "V": V, "A": 0.25, "f": float(f), "s": float(s),
                    "gamma": float(g), "octaves": 4})
    out.append({"name": "sine_periodic", "kind": "sine", "f": 5.0, "s": 0.18, "gamma": 1.0, "octaves": 1})
    out.append({"name": "sine_jump", "kind": "sine", "f": 5.5, "s": 0.18, "gamma": 1.0, "octaves": 1})
    for nm, spec in (("flip_a", FLIP_A), ("flip_b", FLIP_B)):
        c = tone_amplitude_for_rms_slope(spec["freqs"], spec["ratios"], FLIP_RMS_SLOPE)
        out.append({"name": nm, "kind": "flip", "freqs": spec["freqs"], "amps": [c * r for r in spec["ratios"]]})
    return out


def make_z(s: dict, n: int, seed: int, x0: float, y0: float) -> tuple[np.ndarray, np.ndarray]:
    """(H, z): the height H of S2.2 (ampsum) and the height z in units of L used for normal maps."""
    if s["kind"] == "flip":
        z = tone_surface(s["freqs"], s["amps"], n, x0)
        return z, z
    F = procedural_field_separable(s["f"], n, seed, s["octaves"], x0, y0, normalize="ampsum")
    H = s["s"] * t_gamma(F, s["gamma"])
    return H, H * Z_SCALE


def hf_values(z: np.ndarray, n: int, procs=PROCS) -> dict:
    thr = {"px": 120.0, "phys": 120.0 * n / N_REF}
    out = {}
    for proc in procs:
        zp = periodic_component(z) if proc == "pplus" else z
        rgb = normal_rgb_from_height(zp)
        v = normal_from_height(zp)
        zl = windowed(z) if proc == "hann" else zp
        if proc == "hann":
            rgb, v = windowed_normals(rgb), windowed_normals_float(v)
        for cut in HF_CUTS:
            out[f"hf_{cut}_{proc}_uint8"] = hf_ratio(rgb, thr[cut])
            out[f"hf_{cut}_{proc}_float"] = hf_ratio_float(v, thr[cut])
            out[f"hf_{cut}_{proc}_linear_height"] = linear_hf_ratio(zl, thr[cut])
    return out


def run_job(job: tuple) -> dict:
    s, seed, n, (x0, y0), sampling = job
    if sampling == "direct":
        H, z = make_z(s, n, seed, x0, y0)
    else:  # aliasing subset: generate at r = 4 and decimate
        Hf, _ = make_z(s, 4 * n, seed, x0, y0)
        H = decimate_fourier(Hf, n)
        z = H if s["kind"] == "flip" else H * Z_SCALE
    vals = {}
    procs = PROCS if sampling == "direct" else ("raw",)
    for proc in procs:
        X = windowed(H) if proc == "hann" else (periodic_component(H) if proc == "pplus" else H)
        c = spectral_centroids(X, K_BAND)
        vals[f"centroid_amp_{proc}"] = c["centroid_amp"]
        if sampling == "direct":
            vals[f"centroid_power_{proc}"] = c["centroid_power"]
            vals[f"sq_{proc}"] = rq(X)
            if proc == "raw":
                vals["centroid_band_power_raw"] = c["centroid_band_power"]
    vals.update(hf_values(z, n, procs))
    return {"surface": s["name"], "seed": seed, "N": n, "crop": [x0, y0], "sampling": sampling, "values": vals}


def jobs_from(c: dict) -> list[tuple]:
    jobs = []
    for s in surfaces():
        for seed in c["seeds"]:
            for off in c["crop_offsets"]:
                for n in c["grids_N"]:
                    jobs.append((s, seed, n, tuple(off), "direct"))
                for n in (128, 256, 512):
                    jobs.append((s, seed, n, tuple(off), "decimate"))
    return jobs


def compute(c: dict) -> list[dict]:
    jobs = sorted(jobs_from(c), key=lambda j: -j[2] * (16 if j[4] == "decimate" else 1))
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(run_job, jobs, chunksize=4))
    print(f"{len(jobs)} jobs in {time.time() - t0:.0f} s", flush=True)
    return rows


# --- analysis -------------------------------------------------------------------------------------------------------


class Table:
    """Values indexed by (surface, seed, crop index, N, sampling) -> dict of descriptor values."""

    def __init__(self, c, rows):
        self.c = c
        self.crops = [tuple(o) for o in c["crop_offsets"]]
        self.idx = {(r["surface"], r["seed"], self.crops.index(tuple(r["crop"])), r["N"], r["sampling"]): r["values"]
                    for r in rows}

    def arr(self, surface, key, N=None, sampling="direct") -> np.ndarray:
        """Array (seeds, crops, N) of one descriptor key."""
        Ns = self.c["grids_N"] if N is None else N
        return np.array([[[self.idx[(surface, s, k, n, sampling)][key] for n in Ns]
                          for k in range(len(self.crops))] for s in self.c["seeds"]])


def keys_of(rows) -> list[str]:
    return sorted(next(r for r in rows if r["sampling"] == "direct")["values"])


def analyse(c, rows) -> dict:
    T = Table(c, rows)
    names = [s["name"] for s in surfaces()]
    rule = [s for s in surfaces() if s["kind"] == "rule"]
    rule_names = [s["name"] for s in rule]
    keys = keys_of(rows)
    Ns = c["grids_N"]
    S = {"C1": {}, "C2": {}, "C3": {}, "ratios": {}}
    for key in keys:
        C3 = None
        for nm in names:
            X = T.arr(nm, key)  # seeds, crops, N
            c1 = X.max(axis=1) - X.min(axis=1)  # seeds, N
            mean = X.mean(axis=(0, 1))  # N
            c2 = X[:, :, -1] - X[:, :, 0]  # seeds, crops
            c2s = c2.mean(axis=1)  # seed-level averages across crops
            S["C1"].setdefault(key, {})[nm] = {"mean_by_N": c1.mean(0).tolist(),
                                              "se_by_N": (c1.std(0, ddof=1) / np.sqrt(c1.shape[0])).tolist(),
                                              "rel_by_N": (c1.mean(0) / np.abs(mean)).tolist(),
                                              "value_mean_by_N": mean.tolist()}
            S["C2"].setdefault(key, {})[nm] = {"mean": float(c2.mean()), "abs_mean": float(np.abs(c2).mean()),
                                              "se": float(c2s.std(ddof=1) / np.sqrt(len(c2s))),
                                              "mean_by_crop": c2.mean(axis=0).tolist(),
                                              "se_by_crop": (c2.std(axis=0, ddof=1) / np.sqrt(c2.shape[0])).tolist(),
                                              "rel_abs_mean": float(np.abs(c2).mean() / abs(mean[0]))}
        R = np.array([T.arr(nm, key).mean(axis=0) for nm in rule_names])  # points, crops, N
        C3 = R.max(axis=0) - R.min(axis=0)  # crops, N
        S["C3"][key] = {"by_crop_N": C3.tolist(), "max_over_crops_by_N": C3.max(axis=0).tolist()}
        S["ratios"][key] = {nm: {"C1_over_C3_by_N": (np.array(S["C1"][key][nm]["mean_by_N"]) / C3.max(axis=0)).tolist(),
                                 "C1_over_C3_by_crop_N": (np.array(S["C1"][key][nm]["mean_by_N"])[None, :] / C3).tolist(),
                                 "absC2_over_C3": float(np.mean(np.abs(np.array(S["C2"][key][nm]["mean_by_crop"]))
                                                                / C3[:, -1]))}
                            for nm in names}
    S["C4"] = c4(c, T, keys, rule_names)
    S["C5"] = c5(c, T, keys)
    S["aliasing"] = aliasing(c, T, names)
    S["predictions"] = predictions(c, S, T, rule)
    return S


def c4(c, T, keys, rule_names) -> dict:
    out = {}
    Ns = c["grids_N"]
    for key in keys:
        A = np.array([T.arr(nm, key) for nm in rule_names])  # points, seeds, crops, N
        M = A.mean(axis=1)  # points, crops, N
        grid_pairs, crop_pairs = [], []
        for k in range(len(T.crops)):
            for i, j in combinations(range(len(Ns)), 2):
                fl = flips_seeded(A[:, :, k, i], A[:, :, k, j], rule_names)
                gp = {"crop": k, "N": [Ns[i], Ns[j]], "tau": kendall_tau(M[:, k, i], M[:, k, j]), "flips": len(fl)}
                if key in FLIP_DETAIL:
                    gp["flip_pairs"] = [[d["a"], d["b"]] for d in fl]
                grid_pairs.append(gp)
        for n_i, n in enumerate(Ns):
            for k1, k2 in combinations(range(len(T.crops)), 2):
                fl = flips_seeded(A[:, :, k1, n_i], A[:, :, k2, n_i], rule_names)
                crop_pairs.append({"N": n, "crops": [k1, k2], "tau": kendall_tau(M[:, k1, n_i], M[:, k2, n_i]),
                                   "flips": len(fl)})
        out[key] = {"grid_pairs": grid_pairs, "crop_pairs": crop_pairs,
                    "total_grid_flips": sum(g["flips"] for g in grid_pairs),
                    "total_crop_flips": sum(g["flips"] for g in crop_pairs),
                    "min_tau_grid": min(g["tau"] for g in grid_pairs),
                    "min_tau_crop": min(g["tau"] for g in crop_pairs)}
    return out


def c5(c, T, keys) -> dict:
    a, b = "V+1.0_A-1.0", "V-1.0_A+1.0"
    out = {"cells": [], "distinct_rankings": {}}
    for proc in PROCS:
        ks = [k for k in keys if k.endswith(f"_{proc}") or f"_{proc}_" in k]
        for ni, n in enumerate(c["grids_N"]):
            for k in range(len(T.crops)):
                d = {}
                for key in ks:
                    xa, xb = T.arr(a, key)[:, k, ni], T.arr(b, key)[:, k, ni]
                    pooled = np.sqrt((xa.var(ddof=1) + xb.var(ddof=1)) / 2)
                    d[key] = float((xa.mean() - xb.mean()) / pooled) if pooled > 0 else float("inf")
                ranking = sorted(ks, key=lambda q: -abs(d[q]))
                out["cells"].append({"processing": proc, "N": n, "crop": k, "d": d, "ranking": ranking})
        rk = {tuple(x["ranking"]) for x in out["cells"] if x["processing"] == proc}
        out["distinct_rankings"][proc] = len(rk)
    top = {}
    for x in out["cells"]:
        top.setdefault(x["processing"], set()).add(x["ranking"][0])
    out["distinct_top"] = {p: sorted(v) for p, v in top.items()}
    return out


def aliasing(c, T, names) -> dict:
    Na = [128, 256, 512]
    out = {}
    for key in ["centroid_amp_raw"] + [f"hf_{cut}_raw_{v}" for cut in HF_CUTS for v in HF_VARIANTS]:
        out[key] = {}
        for nm in names:
            d = T.arr(nm, key, Na)
            m = T.arr(nm, key, Na, "decimate")
            rel = np.abs(m - d) / np.abs(d)
            out[key][nm] = {"rel_abs_diff_by_N": rel.mean(axis=(0, 1)).tolist(),
                            "abs_diff_by_N": np.abs(m - d).mean(axis=(0, 1)).tolist(),
                            "mean_diff_by_N": (m - d).mean(axis=(0, 1)).tolist()}
    return out


def predictions(c, S, T, rule) -> dict:
    P = {}
    Ns = c["grids_N"]
    nonint = [s["name"] for s in surfaces() if s["kind"] == "nonint"]
    integ = [s["name"] for s in rule if s["A"] == 0]
    # P-E1
    items = []
    for key in ("centroid_amp_raw", "centroid_power_raw", "sq_raw"):
        r1 = max(S["C1"][key]["sine_periodic"]["rel_by_N"])
        r2 = S["C2"][key]["sine_periodic"]["rel_abs_mean"]
        items.append({"part": f"{key}: crop range and grid change", "rel_C1_max": r1, "rel_absC2": r2,
                      "holds": bool(r1 < 1e-9 and r2 < 1e-9)})
    m = S["C1"]["hf_px_raw_uint8"]["sine_periodic"]["value_mean_by_N"]
    items.append({"part": "hf px decreases with N (uint8 raw)", "values": m, "holds": bool(np.all(np.diff(m) < 0))})
    a, b = S["C2"]["hf_px_raw_uint8"]["sine_periodic"]["abs_mean"], S["C2"]["hf_phys_raw_uint8"]["sine_periodic"]["abs_mean"]
    items.append({"part": "|C2| px > |C2| phys", "px": a, "phys": b, "holds": bool(a > b)})
    P["P-E1"] = items
    # P-E2
    items = []
    by_v0 = {s["V"]: s["name"] for s in rule if s["A"] == 0}
    by_v1 = {s["V"]: s["name"] for s in surfaces() if s["kind"] == "nonint"}
    c1 = lambda nm, ni: S["C1"]["centroid_amp_raw"][nm]["mean_by_N"][ni]
    for ni, n in enumerate(Ns):
        pairs = {V: (c1(by_v1[V], ni), c1(by_v0[V], ni)) for V in LEVELS}
        pair_ok = all(a > b for a, b in pairs.values())
        jump_ok = c1("sine_jump", ni) > max(c1(nm, ni) for nm in integ)
        items.append({"N": n, "C1_A0.25_by_V": [pairs[V][0] for V in LEVELS], "C1_A0_by_V": [pairs[V][1] for V in LEVELS],
                      "C1_sine_jump": c1("sine_jump", ni), "pairs_larger": sum(a > b for a, b in pairs.values()),
                      "holds": bool(pair_ok and jump_ok)})
    P["P-E2"] = items
    # P-E3 (N = 2048, the largest grid of the conditions)
    ni = len(Ns) - 1
    C3 = S["C3"]["centroid_amp_raw"]["max_over_crops_by_N"][ni]
    exceed = [nm for nm in nonint if S["C1"]["centroid_amp_raw"][nm]["mean_by_N"][ni] > C3]
    P["P-E3"] = [{"N": Ns[ni], "C3_max_over_crops": C3, "points_exceeding": exceed,
                  "largest_C1": max(S["C1"]["centroid_amp_raw"][nm]["mean_by_N"][ni] for nm in nonint),
                  "holds": bool(exceed)}]
    # P-E4
    items = []
    for treat, base in (("centroid_amp_hann", "centroid_amp_raw"), ("centroid_amp_pplus", "centroid_amp_raw"),
                        ("centroid_band_power_raw", "centroid_power_raw")):
        cnt = cnt_rel = tot = 0
        for nm in nonint:
            for ni in range(len(Ns)):
                tot += 1
                cnt += S["C1"][treat][nm]["mean_by_N"][ni] < S["C1"][base][nm]["mean_by_N"][ni]
                cnt_rel += S["C1"][treat][nm]["rel_by_N"][ni] < S["C1"][base][nm]["rel_by_N"][ni]
        items.append({"treatment": treat, "baseline": base, "cells_smaller": cnt, "cells_smaller_relative": cnt_rel,
                      "cells": tot, "holds": cnt == tot})
    P["P-E4"] = items
    # P-E5
    items = []
    targets = [s["name"] for s in rule] + nonint + ["sine_periodic", "sine_jump"]
    dec = [nm for nm in targets if np.all(np.diff(S["C1"]["hf_px_raw_uint8"][nm]["value_mean_by_N"]) < 0)]
    items.append({"part": "px decreases with N for every surface", "surfaces_decreasing": len(dec),
                  "surfaces": len(targets), "holds": len(dec) == len(targets)})
    smaller = [nm for nm in targets
               if S["C2"]["hf_phys_raw_uint8"][nm]["abs_mean"] < S["C2"]["hf_px_raw_uint8"][nm]["abs_mean"]]
    items.append({"part": "|C2| phys < |C2| px", "surfaces_smaller": len(smaller), "surfaces": len(targets),
                  "holds": len(smaller) == len(targets)})
    fpx, fph = S["C4"]["hf_px_raw_uint8"]["total_grid_flips"], S["C4"]["hf_phys_raw_uint8"]["total_grid_flips"]
    items.append({"part": "flips px >= 1", "flips_px": fpx, "holds": fpx >= 1})
    items.append({"part": "flips phys < px", "flips_px": fpx, "flips_phys": fph, "holds": fph < fpx})
    P["P-E5"] = items
    # P-E6
    items = []
    hi_g = [s["name"] for s in rule if s["gamma"] > 1]
    lo_g = [s["name"] for s in rule if s["gamma"] <= 1]
    for ni, n in enumerate([128, 256, 512]):
        al = S["aliasing"]["centroid_amp_raw"]
        a = float(np.mean([al[nm]["abs_diff_by_N"][ni] for nm in hi_g]))
        b = float(np.mean([al[nm]["abs_diff_by_N"][ni] for nm in lo_g]))
        ar = float(np.mean([al[nm]["rel_abs_diff_by_N"][ni] for nm in hi_g]))
        br = float(np.mean([al[nm]["rel_abs_diff_by_N"][ni] for nm in lo_g]))
        items.append({"N": n, "gamma_gt_1": a, "gamma_le_1": b, "relative_gt_1": ar, "relative_le_1": br,
                      "points_le_1": lo_g, "holds": bool(a > b)})
    P["P-E6"] = items
    # P-E7
    items = []
    seeds_ = c["seeds"]
    for key in ("hf_px_raw_linear_height", "hf_phys_raw_linear_height", "hf_px_raw_uint8", "hf_px_raw_float"):
        per_crop = []
        for k in range(len(T.crops)):
            A = np.array([T.arr("flip_a", key)[:, k, :], T.arr("flip_b", key)[:, k, :]])  # 2, seeds, N
            n_fl = sum(len(flips_seeded(A[:, :, i], A[:, :, j])) for i, j in combinations(range(len(Ns)), 2))
            per_crop.append(n_fl)
        order = np.sign(T.arr("flip_a", key).mean(axis=(0, 1)) - T.arr("flip_b", key).mean(axis=(0, 1))).tolist()
        if key == "hf_px_raw_linear_height":
            ok = all(x >= 1 for x in per_crop)
        elif key == "hf_phys_raw_linear_height":
            ok = all(x == 0 for x in per_crop)
        else:
            ok = any(x >= 1 for x in per_crop)
        items.append({"descriptor": key, "flips_per_crop": per_crop, "sign_a_minus_b_by_N": order, "holds": bool(ok)})
    P["P-E7"] = items
    return P


# --- report ---------------------------------------------------------------------------------------------------------


def g(x):
    if isinstance(x, float):
        return f"{x:.4g}"
    if isinstance(x, list):
        return ", ".join(g(v) for v in x)
    return str(x)


def write_report(c, meta, S) -> str:
    L = ["# Paired comparison of edge and grid effects", "",
         f"Conditions: `experiments/conditions/edge_grid_paired.json` (SHA-256 `{meta['conditions_sha256']}`). "
         f"Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `{meta['spec_sha256']}`). "
         f"numpy {meta['numpy']}, scipy {meta['scipy']}, Python {meta['python']}. Run started {meta['started']} and "
         f"finished {meta['finished']} ({meta['platform']}).", "",
         "This computation extends an earlier one whose results had been seen (hf_ratio_edge.json, commits c2ee719 "
         "and 82efec2); it is not blind to those results. Values after a window, the periodic-plus-smooth "
         "decomposition or band fixing are not regarded as true values. Reference scale from Table 1 of Gao et al. "
         "(2026): differences in HF ratio between the compared models of 0.009-0.103.", "",
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
    L += ["## C4: flips and Kendall's tau among the 25 rule points", "",
          "Totals over the five crops and the ten pairs of grids (grid flips), and over the five N and the ten pairs "
          "of crops (crop flips).", "",
          "| descriptor | grid flips | min tau over grid pairs | crop flips | min tau over crop pairs |",
          "|---|---|---|---|---|"]
    for key, v in S["C4"].items():
        L.append(f"| {key} | {v['total_grid_flips']} | {v['min_tau_grid']:.3f} | {v['total_crop_flips']} | "
                 f"{v['min_tau_crop']:.3f} |")
    L += ["", "## C5: ranking of descriptors by the separation of the corners (1, -1) and (-1, 1)", "",
          "| processing | distinct rankings over N and crops (of 25) | descriptors ranked first |", "|---|---|---|"]
    for p in PROCS:
        L.append(f"| {p} | {S['C5']['distinct_rankings'][p]} | {', '.join(S['C5']['distinct_top'][p])} |")
    L += ["", "Rankings at the default crop (0, 0):", "", "| processing | N | ranking (|d|, descending) |", "|---|---|---|"]
    for x in S["C5"]["cells"]:
        if x["crop"] == 0:
            L.append(f"| {x['processing']} | {x['N']} | " + ", ".join(f"{q} ({x['d'][q]:+.2f})" for q in x["ranking"]) + " |")
    L += ["", "## C1 and C3: crop range relative to the range over the rule (raw centroid_amp)", "",
          "| surface | mean C1, N 128 ... 2048 | C1 / C3 (largest C3 over crops), N 128 ... 2048 | |C2| / C3 |",
          "|---|---|---|---|"]
    for nm, v in S["C1"]["centroid_amp_raw"].items():
        r = S["ratios"]["centroid_amp_raw"][nm]
        L.append(f"| {nm} | {g(v['mean_by_N'])} | {g(r['C1_over_C3_by_N'])} | {r['absC2_over_C3']:.4g} |")
    L += ["", "C3 (largest over crops) by N for each descriptor:", "", "| descriptor | C3, N 128 ... 2048 |", "|---|---|"]
    for key, v in S["C3"].items():
        L.append(f"| {key} | {g(v['max_over_crops_by_N'])} |")
    L += ["", "## Ratios for every descriptor (mean over the 25 rule points)", "",
          "| descriptor | mean C1/C3 at N = 2048 | mean |C2|/C3 |", "|---|---|---|"]
    rule_names = [s["name"] for s in surfaces() if s["kind"] == "rule"]
    for key, v in S["ratios"].items():
        L.append(f"| {key} | {np.mean([v[nm]['C1_over_C3_by_N'][-1] for nm in rule_names]):.4g} | "
                 f"{np.mean([v[nm]['absC2_over_C3'] for nm in rule_names]):.4g} |")
    L += ["", "## Aliasing subset (r = 4, decimate_fourier versus direct sampling)", "",
          "Mean over seeds and crops of |decimated - direct| / direct, N = 128, 256, 512.", "",
          "| surface | centroid_amp_raw | hf_px_raw_uint8 | hf_phys_raw_uint8 |", "|---|---|---|---|"]
    for nm in S["aliasing"]["centroid_amp_raw"]:
        L.append(f"| {nm} | {g(S['aliasing']['centroid_amp_raw'][nm]['rel_abs_diff_by_N'])} | "
                 f"{g(S['aliasing']['hf_px_raw_uint8'][nm]['rel_abs_diff_by_N'])} | "
                 f"{g(S['aliasing']['hf_phys_raw_uint8'][nm]['rel_abs_diff_by_N'])} |")
    L += ["", "## Seed and crop means of every descriptor by N", "", "| descriptor | surface | N 128 ... 2048 |", "|---|---|---|"]
    for key, v in S["C1"].items():
        for nm, w in v.items():
            L.append(f"| {key} | {nm} | {g(w['value_mean_by_N'])} |")
    return "\n".join(L) + "\n"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="rewrite the results from the saved values")
    ap.add_argument("--smoke", metavar="DIR", help="run the whole pipeline on small grids and seeds outside the "
                    "conditions (101-103), writing to DIR; for testing the script only")
    args = ap.parse_args()
    c = json.loads(COND.read_text())
    out = OUT
    if args.smoke:
        c = dict(c, grids_N=[128, 256, 512], seeds=[101, 102, 103])
        out = Path(args.smoke)
    js = out / f"{NAME}.json"
    if args.report:
        saved = json.loads(js.read_text())
        meta, rows = saved["meta"], unpack(saved["rows"])
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
    js.write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION, "summary": S, "rows": pack(rows)}))
    (out / f"{NAME}.md").write_text(write_report(c, meta, S))
    print("done")


if __name__ == "__main__":
    main()
