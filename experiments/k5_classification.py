"""K5: what the accuracy of classifying generated surfaces establishes (Table 1).

Usage:  uv run python experiments/k5_classification.py --power          (choose per_class_n; results/k5_power.*)
        uv run python experiments/k5_classification.py --large-sample   (predicted levels; results/k5_large_sample.*)
        uv run python experiments/k5_classification.py --frame          (Table 1 frame with the three prediction columns)
        uv run python experiments/k5_classification.py                  (the experiment; results/k5_classification.*)
        uv run python experiments/k5_classification.py --report        (rewrite the results from the saved values)
        uv run python experiments/k5_classification.py --smoke DIR      (all stages on small numbers, written to DIR)
Conditions: experiments/conditions/k5_classification.json (version 1, fixed and committed before this script was run)
Predicted direction and order: experiments/conditions/k5_table1_predictions.json (committed before any computation)
Specification: experiments/spec/generator-and-descriptors.md

The stages are run in the order power, large-sample, frame, experiment. The frame (the predicted direction, order and
large-sample level of every row) is committed before the experiment is run. Where the conditions leave a choice open,
the choice is stated in INTERPRETATION below and in the results; it was fixed in this script before the computation
was run.
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
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

from atact.descriptors import rq, spectral_centroids
from atact.field import minmax, procedural_field_separable
from atact.mapping import params
from atact.spectral import windowed
from atact.transform import t_gamma

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "k5_classification.json"
PRED = ROOT / "experiments" / "conditions" / "k5_table1_predictions.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
OUT = ROOT / "results"
NAME = "k5_classification"
K_BAND = 32.0
DESC = ("sq", "centroid_amp", "centroid_band_power")
PROCS = ("raw", "hann")
REPRS = ("H", "minmax")
NULL = ("iii_null", "check_same_seed")
CENTRES = {"i_V": ((-0.5, 0.0), (0.5, 0.0)), "i_A": ((0.0, -0.5), (0.0, 0.5)),
           "ii_s": ((1.0, -1.0), (-1.0, 1.0)), "ii_s_gamma": ((1.0, -1.0), (-1.0, 1.0)),
           "corners": ((1.0, -1.0), (-1.0, 1.0))}
S_FIXED, GAMMA_FIXED = 0.18, 1.0
N_FOLDS, N_BOOT, N_PERM = 5, 2000, 999
WORKERS = 8

# Seed bases (decision recorded before any computation). Pair i of the experiment uses base0 + i for group 0 and,
# for iii_null only, base1 + i for group 1 (conditions file: 1000 + i and 50000 + i). The other stages use ranges
# that do not overlap the experiment or each other.
SEEDS = {
    "experiment": (1000, 50000),
    "power_a": lambda r: (100000 + 1000 * r, 300000 + 1000 * r),   # iii_null, run r = 0..199
    "power_b": lambda r: (500000 + 1000 * r, None),                # corners, run r = 0..49
    "large_A": (2000000, 4000000),
    "large_B": (3000000, 5000000),
    "mechanism": (1000, None),
}
SMOKE_SEEDS = {
    "experiment": (900000, 950000),
    "power_a": lambda r: (901000 + 1000 * r, 905000 + 1000 * r),
    "power_b": lambda r: (908000 + 1000 * r, None),
    "large_A": (910000, 912000),
    "large_B": (911000, 913000),
    "mechanism": (900000, None),
}

INTERPRETATION = [
    "Groups: group 0 is the first centre listed for the condition and group 1 the second (i_V: V = -0.5 / 0.5; i_A: "
    "A = -0.5 / 0.5; ii_s, ii_s_gamma and corners: (1, -1) / (-1, 1)). iii_null and check_same_seed use the (f, s, "
    "gamma) of corner (1, -1) for both groups.",
    "Jitter (decision recorded before any computation): the surface of group g with seed s draws u = "
    "default_rng([s, g]).uniform(-1, 1, 2) and its jitter is w u. i_V adds w u[0] to V only and i_A adds w u[1] to A "
    "only; ii_s, ii_s_gamma and corners add both and clip to [-1, 1]. The same u is used for the three values of w and "
    "for every condition, N, processing and representation, so these differ only in the quantity named.",
    "Surface: F by S1.1-S1.4 (maxabs, four octaves, no warp; atact.field.procedural_field_separable), H = s T_gamma(F) "
    "(S2.2). Representation H uses H; minmax uses (H - min H) / (max H - min H). Processing raw computes the "
    "descriptors on the representation minus its mean; hann on the windowed array of S3.1. sq is S2.5, centroid_amp "
    "S2.3, centroid_band_power S2.4 with power weighting and 0 < rho <= 32.",
    "Cross-validation: pair i is relabelled perm[i] with perm = default_rng(0).permutation(n), and sklearn GroupKFold "
    "with five splits forms the folds from these labels. Both surfaces of a pair are always in the same fold. The fold "
    "assignment depends only on the pair indices, so it is the same under every label permutation.",
    "svm: StandardScaler and SVC(kernel='linear', C=1) fitted on the training folds. threshold: on the training folds, "
    "the cut between two adjacent distinct values (or below or above all values) and the direction that maximise "
    "training accuracy; ties are broken by the first maximum in the order (direction 'greater is group 1' before "
    "'smaller is group 1', smaller cut first). Accuracy is the fraction of the 2n surfaces predicted correctly out of "
    "fold.",
    "Bootstrap: the pairs are resampled with replacement (indices from default_rng(1), the same 2000 replicates for "
    "every row with the same n); the out-of-fold predictions are kept fixed and the accuracy of each replicate is the "
    "fraction of correct predictions among the resampled pairs. Percentile intervals use numpy.percentile (linear). "
    "TOST: 'at chance' if the 90% interval of accuracy - 0.5 lies strictly inside (-0.05, 0.05).",
    "Permutation: 999 replicates; in each, the labels of each pair are swapped with probability 1/2 (draws from "
    "default_rng(2)), and the whole pipeline (fold assignment, standardisation, classifier fit, threshold choice) is "
    "run again. p = (1 + number of permuted accuracies >= observed) / 1000.",
    "tost_chance and perm_p are given for each classifier (svm for every descriptor set, threshold for the "
    "single-descriptor sets).",
    "Power (decisions recorded before any computation): (a) run r of iii_null uses seeds 100000 + 1000 r + i (group 0) "
    "and 300000 + 1000 r + i (group 1), r = 0..199; for a candidate n the first n pairs are used. Equivalence must be "
    "declared in at least 80% of runs in every column of iii_null (both N, processings, representations, descriptor "
    "sets and classifiers). (b) run r of corners (w = 0.5, N = 128, raw, H, svm, {sq, centroid_amp}) uses seed 500000 "
    "+ 1000 r + i for both groups, r = 0..49; the mean half-width of the 95% interval must be at most 0.05. If no "
    "candidate satisfies both, the largest candidate (480) is used and this is stated in the results.",
    "Large-sample level (decision recorded before any computation): set A uses seeds 2000000 + j and set B 3000000 + j "
    "for both groups (iii_null group 1: 4000000 + j and 5000000 + j), j = 0..4999. One descriptor: the best threshold "
    "on set A, with its accuracy on set A (the level) and, beside it, on set B. Two descriptors: the svm of the "
    "experiment trained on set A and evaluated on set B. For iii_null the in-sample threshold accuracy exceeds 0.5 "
    "by selection, which is reported and not corrected.",
    "Mechanism check: descriptors of i_V and i_A at the jitter-free centres for seeds 1000-1099, by group "
    "(mean, standard deviation, minimum and maximum).",
    "Clipping: for ii_s, ii_s_gamma and corners, the fraction of surfaces with at least one coordinate clipped to the "
    "boundary is reported for each w.",
    "P-K5-4 and P-K5-5 compare accuracies for exact equality. Descriptor values that agree only to rounding (relative "
    "1e-13) can still give a different svm accuracy: the weight of the soft-margin SVM is unique but its intercept "
    "need not be, and a rounding-level change of which support vectors lie on the margin moves the intercept chosen "
    "by the solver (in a smoke run, one fold had the same weight and intercepts -0.104 and -0.035, with 24 and 25 "
    "support vectors; a solver tolerance of 1e-12 instead of 1e-3 gave the same accuracies). The accuracies of every "
    "unequal cell are listed beside the count. This was noticed in a smoke run before the experiment and the "
    "criterion was not changed.",
    "Smoke runs (--smoke) use seeds from 900000 upwards with 20 pairs, fewer replicates and fewer runs; they test the "
    "script only and their values are not used for any decision.",
]


# --- surfaces -------------------------------------------------------------------------------------------------------


def jitter_u(seed: int, g: int) -> np.ndarray:
    return np.random.default_rng([seed, g]).uniform(-1.0, 1.0, 2)


def surface_params(cond: str, g: int, seed: int, w: float | None) -> dict:
    """(V, A) and (f, s, gamma) of the surface of group g with the given seed under condition cond and jitter w."""
    if cond in NULL:
        V, A, clipped = 1.0, -1.0, False
    else:
        (V0, A0), u = CENTRES[cond][g], jitter_u(seed, g)
        if cond == "i_V":
            V, A = V0 + w * u[0], A0
        elif cond == "i_A":
            V, A = V0, A0 + w * u[1]
        else:
            V, A = V0 + w * u[0], A0 + w * u[1]
        clipped = bool(abs(V) > 1 or abs(A) > 1)
        V, A = float(np.clip(V, -1, 1)), float(np.clip(A, -1, 1))
    f, s, gm = (float(x) for x in params(V, A))
    if cond in ("ii_s", "ii_s_gamma"):
        s = S_FIXED
    if cond == "ii_s_gamma":
        gm = GAMMA_FIXED
    return {"V": V, "A": A, "f": f, "s": s, "gamma": gm, "clipped": clipped}


def pair_seeds(cond: str, i: int, bases: tuple) -> tuple[int, int]:
    s0 = bases[0] + i
    return s0, (bases[1] + i if cond == "iii_null" else s0)


def descriptor_block(f: float, s: float, gamma: float, seed: int, n: int) -> np.ndarray:
    """Array (representation, processing, descriptor) of one surface at grid n."""
    H = s * t_gamma(procedural_field_separable(f, n, seed), gamma)
    out = np.empty((len(REPRS), len(PROCS), len(DESC)))
    for a, rep in enumerate(REPRS):
        E = H if rep == "H" else minmax(H)
        for b, proc in enumerate(PROCS):
            X = E - E.mean() if proc == "raw" else windowed(E)
            c = spectral_centroids(X, K_BAND)
            out[a, b] = (rq(X), c["centroid_amp"], c["centroid_band_power"])
    return out


def gen_job(job: tuple) -> tuple:
    """job = (key, cond, w, g, seeds, Ns) -> (key, params list, array (len(seeds), len(Ns), repr, proc, desc))."""
    key, cond, w, g, seeds, Ns = job
    ps = [surface_params(cond, g, sd, w) for sd in seeds]
    arr = np.array([[descriptor_block(p["f"], p["s"], p["gamma"], sd, n) for n in Ns] for p, sd in zip(ps, seeds)])
    return key, ps, arr


def generate(specs: list[tuple], Ns, chunk: int = 40, label: str = "") -> dict:
    """specs: (key, cond, w, n_pairs, bases). Returns key -> {'params': [g0 list, g1 list], 'X': array
    (pair, group, N, repr, proc, desc)}."""
    jobs = []
    for key, cond, w, npairs, bases in specs:
        for g in (0, 1):
            seeds = [pair_seeds(cond, i, bases)[g] for i in range(npairs)]
            for k in range(0, npairs, chunk):
                jobs.append(((key, g, k), cond, w, g, seeds[k:k + chunk], tuple(Ns)))
    parts, t0 = {}, time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(gen_job, j) for j in jobs]
        for d, fu in enumerate(as_completed(futs), 1):
            (key, g, k), ps, arr = fu.result()
            parts[(key, g, k)] = (ps, arr)
            if d % max(1, len(jobs) // 20) == 0 or d == len(jobs):
                el = time.time() - t0
                print(f"[gen {label}] {d}/{len(jobs)} chunks, {el:.0f} s, about {el / d * (len(jobs) - d):.0f} s left",
                      flush=True)
    out = {}
    for key, cond, w, npairs, bases in specs:
        P, X = [], []
        for g in (0, 1):
            ks = sorted(k for (kk, gg, k) in parts if kk == key and gg == g)
            P.append([p for k in ks for p in parts[(key, g, k)][0]])
            X.append(np.concatenate([parts[(key, g, k)][1] for k in ks]))
        out[key] = {"params": P, "X": np.stack(X, axis=1)}
    return out


# --- classification -------------------------------------------------------------------------------------------------


def make_folds(n_pairs: int) -> list[tuple[np.ndarray, np.ndarray]]:
    from sklearn.model_selection import GroupKFold

    perm = np.random.default_rng(0).permutation(n_pairs)
    groups = np.repeat(perm, 2)
    idx = np.arange(2 * n_pairs)
    return [(tr, te) for tr, te in GroupKFold(n_splits=N_FOLDS).split(idx, idx % 2, groups)]


def fit_threshold(x: np.ndarray, y: np.ndarray) -> tuple[float, bool]:
    """Cut and direction maximising training accuracy. Returns (t, up): up means x > t is group 1."""
    o = np.argsort(x, kind="mergesort")
    xs, ys = x[o], y[o]
    m = len(xs)
    ones_left = np.concatenate([[0], np.cumsum(ys)])
    zeros_left = np.arange(m + 1) - ones_left
    acc_up = zeros_left + (ones_left[-1] - ones_left)
    acc_down = ones_left + (zeros_left[-1] - zeros_left)
    valid = np.ones(m + 1, dtype=bool)
    valid[1:m] = xs[1:] > xs[:-1]
    au, ad = np.where(valid, acc_up, -1), np.where(valid, acc_down, -1)
    up = au.max() >= ad.max()
    k = int(np.argmax(au if up else ad))
    t = -np.inf if k == 0 else (np.inf if k == m else (xs[k - 1] + xs[k]) / 2)
    return float(t), bool(up)


def predict_threshold(x: np.ndarray, t: float, up: bool) -> np.ndarray:
    return (x > t).astype(int) if up else (x < t).astype(int)


def svm_model():
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC

    return make_pipeline(StandardScaler(), SVC(kernel="linear", C=1.0))


def cv_correct(X: np.ndarray, y: np.ndarray, folds, clf: str) -> np.ndarray:
    """Out-of-fold correctness of each sample (samples ordered pair by pair: pair i is rows 2i and 2i + 1)."""
    pred = np.empty_like(y)
    for tr, te in folds:
        if clf == "svm":
            pred[te] = svm_model().fit(X[tr], y[tr]).predict(X[te])
        else:
            t, up = fit_threshold(X[tr, 0], y[tr])
            pred[te] = predict_threshold(X[te, 0], t, up)
    return pred == y


def boot_indices(n_pairs: int, n_boot: int) -> np.ndarray:
    return np.random.default_rng(1).integers(0, n_pairs, (n_boot, n_pairs))


def interval_summary(correct: np.ndarray, B: np.ndarray) -> dict:
    counts = correct.reshape(-1, 2).sum(axis=1)
    n = len(counts)
    acc = float(counts.sum() / (2 * n))
    accb = counts[B].sum(axis=1) / (2 * n)
    lo95, hi95, lo90, hi90 = np.percentile(accb, [2.5, 97.5, 5, 95])
    tost = bool(lo90 - 0.5 > -0.05 and hi90 - 0.5 < 0.05)
    return {"acc": acc, "ci95": [float(lo95), float(hi95)], "ci90": [float(lo90), float(hi90)], "tost_chance": tost}


def labels(n_pairs: int) -> np.ndarray:
    return np.tile([0, 1], n_pairs)


def features(Xc: np.ndarray, ni: int, rep: str, proc: str, dset) -> np.ndarray:
    """Feature matrix (2n, d) from the generated array of one cell (pair, group, N, repr, proc, desc)."""
    cols = [DESC.index(d) for d in dset]
    F = Xc[:, :, ni, REPRS.index(rep), PROCS.index(proc)][:, :, cols]
    return F.reshape(-1, len(cols))


def classify_row(job: tuple) -> tuple:
    """job = (row key, X (2n, d), n_boot, n_perm). Full analysis of one row of Table 1."""
    key, X, n_boot, n_perm = job
    n = X.shape[0] // 2
    y, folds, B = labels(n), make_folds(n), boot_indices(n, n_boot)
    swaps = np.random.default_rng(2).integers(0, 2, (n_perm, n)).astype(bool)
    out = {}
    for clf in (("svm", "threshold") if X.shape[1] == 1 else ("svm",)):
        corr = cv_correct(X, y, folds, clf)
        r = interval_summary(corr, B)
        perm_acc = np.empty(n_perm)
        for p in range(n_perm):
            yp = y.reshape(n, 2).copy()
            yp[swaps[p]] = yp[swaps[p]][:, ::-1]
            perm_acc[p] = cv_correct(X, yp.ravel(), folds, clf).mean()
        r["perm_p"] = float((1 + np.sum(perm_acc >= r["acc"] - 1e-12)) / (n_perm + 1))
        r["perm_mean"] = float(perm_acc.mean())
        out[clf] = r
    return key, out


# --- table frame ----------------------------------------------------------------------------------------------------


def combos(c: dict) -> list[tuple[str, float | None]]:
    return [(cd["name"], None) if cd["name"] in NULL else (cd["name"], w)
            for cd in c["conditions"] for w in ([None] if cd["name"] in NULL else c["jitter_w"])]


def ckey(cond: str, w) -> str:
    return cond if w is None else f"{cond}_w{w}"


def table_rows(c: dict) -> list[dict]:
    return [{"condition": cond, "w": w, "N": n, "processing": proc, "representation": rep,
             "descriptor_set": list(ds)}
            for cond, w in combos(c) for n in c["grids_N"] for proc in PROCS for rep in REPRS
            for ds in c["descriptor_sets"]]


def rkey(r: dict) -> str:
    return f"{ckey(r['condition'], r['w'])}|{r['N']}|{r['processing']}|{r['representation']}|" + "+".join(
        r["descriptor_set"])


def set_name(ds) -> str:
    return {("sq",): "S", ("centroid_amp",): "C", ("centroid_band_power",): "B",
            ("sq", "centroid_amp"): "SC"}[tuple(ds)]


def row_predictions(r: dict) -> tuple[list[str], list[str]]:
    """predicted_direction and predicted_order of one row, from the criteria of k5_table1_predictions.json."""
    cond, sn, rep, proc, n = r["condition"], set_name(r["descriptor_set"]), r["representation"], r["processing"], r["N"]
    d, o = [], []
    if cond == "check_same_seed":
        d.append("exactly 0.5 (P-K5-3)")
    elif cond == "iii_null":
        d.append("at chance by the TOST (P-K5-3)")
    elif cond == "ii_s_gamma" and sn == "S":
        d.append("no direction relative to chance (P-K5-9)")
    else:
        d.append("above chance (P-K5-12)")
    if rep == "minmax" and sn == "S" and cond in ("ii_s", "ii_s_gamma", "corners"):
        d.append("<= the same row on H (P-K5-1)")
    if rep == "minmax" and sn == "S" and cond == "i_V":
        d.append("<= the same row on H (P-K5-6)")
    if rep == "minmax" and sn in ("C", "B"):
        d.append("= the same row on H (P-K5-4)")
    if cond in ("ii_s", "corners") and (rep == "minmax" or sn in ("C", "B")):
        other = "corners" if cond == "ii_s" else "ii_s"
        d.append(f"= the same row of {other} (P-K5-5)")
    if cond == "i_A" and sn == "C" and proc == "raw":
        d.append("N = 512 >= N = 128 (P-K5-2)")
    if cond == "i_A" and ((sn == "B" and proc == "raw") or (sn == "C" and proc == "hann")):
        d.append("change between N = 128 and 512 smaller than for raw C (P-K5-2)")
    if cond == "i_V" and sn == "C" and proc == "raw":
        d.append("N = 512 >= N = 128 (P-K5-11)")
    if cond not in NULL:
        if sn == "SC":
            o.append(">= max(S, C) of the same cell (P-K5-7)")
        o.append("non-increasing in w (P-K5-8)")
        if cond == "ii_s_gamma" and sn == "S" and proc == "raw" and rep == "H":
            o.append("< S of i_V, i_A, ii_s and corners in the same column (P-K5-9)")
        if cond in ("i_A", "ii_s", "ii_s_gamma") or (cond == "corners" and rep == "minmax"):
            if sn in ("C", "B"):
                o.append(">= S of the same cell (P-K5-10)")
            if sn == "S":
                o.append("<= C and B of the same cell (P-K5-10)")
        if cond == "i_V" and rep == "H":
            if sn == "S":
                o.append(">= C of the same cell (P-K5-10)")
            if sn == "C":
                o.append("<= S of the same cell (P-K5-10)")
    return d or ["none"], o or ["none"]


# --- stages ---------------------------------------------------------------------------------------------------------


def meta_base() -> dict:
    import scipy
    import sklearn

    return {"conditions_sha256": sha(COND), "spec_sha256": sha(SPEC), "predictions_sha256": sha(PRED),
            "script_sha256": sha(Path(__file__)), "numpy": np.__version__, "scipy": scipy.__version__,
            "sklearn": sklearn.__version__, "python": sys.version.split()[0],
            "platform": f"{platform.system()} {platform.machine()}, {os.cpu_count()} logical CPUs",
            "started": now()}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def power_columns(c: dict) -> list[tuple]:
    return [(n, proc, rep, tuple(ds), clf) for n in c["grids_N"] for proc in PROCS for rep in REPRS
            for ds in c["descriptor_sets"] for clf in (("svm", "threshold") if len(ds) == 1 else ("svm",))]


def power_run_job(job: tuple) -> tuple:
    """job = (stage, r, X (pair, group, N, repr, proc, desc), Ns, columns, candidates, n_boot)."""
    stage, r, X, Ns, cols, cands, n_boot = job
    out = {}
    for npairs in cands:
        y, folds, B = labels(npairs), make_folds(npairs), boot_indices(npairs, n_boot)
        res = {}
        for (n, proc, rep, ds, clf) in cols:
            F = features(X[:npairs], Ns.index(n), rep, proc, ds)
            s = interval_summary(cv_correct(F, y, folds, clf), B)
            res["|".join([str(n), proc, rep, "+".join(ds), clf])] = (s["acc"], s["ci95"], s["tost_chance"])
        out[npairs] = res
    return stage, r, out


def stage_power(c: dict, seeds: dict, runs_a: int, runs_b: int, cands: list[int], n_boot: int) -> dict:
    nmax = max(cands)
    cols_a = power_columns(c)
    cols_b = [(128, "raw", "H", ("sq", "centroid_amp"), "svm")]
    specs = [(f"a{r}", "iii_null", None, nmax, seeds["power_a"](r)) for r in range(runs_a)]
    specs += [(f"b{r}", "corners", 0.5, nmax, seeds["power_b"](r)) for r in range(runs_b)]
    data_a = generate(specs[:runs_a], c["grids_N"], label="power a")
    data_b = generate(specs[runs_a:], [128], label="power b")
    jobs = [("a", r, data_a[f"a{r}"]["X"], list(c["grids_N"]), cols_a, cands, n_boot) for r in range(runs_a)]
    jobs += [("b", r, data_b[f"b{r}"]["X"], [128], cols_b, cands, n_boot) for r in range(runs_b)]
    res, t0 = {"a": {}, "b": {}}, time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(power_run_job, j) for j in jobs]
        for d, fu in enumerate(as_completed(futs), 1):
            stage, r, out = fu.result()
            res[stage][r] = out
            if d % max(1, len(jobs) // 20) == 0 or d == len(jobs):
                el = time.time() - t0
                print(f"[power] {d}/{len(jobs)} runs, {el:.0f} s, about {el / d * (len(jobs) - d):.0f} s left",
                      flush=True)
    summary = {"candidates": cands, "runs_a": runs_a, "runs_b": runs_b, "a": {}, "b": {}}
    for npairs in cands:
        keys = list(res["a"][0][npairs])
        rate = {k: float(np.mean([res["a"][r][npairs][k][2] for r in range(runs_a)])) for k in keys}
        mean_acc = {k: float(np.mean([res["a"][r][npairs][k][0] for r in range(runs_a)])) for k in keys}
        summary["a"][str(npairs)] = {"equivalence_rate": rate, "mean_accuracy": mean_acc,
                                     "min_rate": min(rate.values()), "min_rate_column": min(rate, key=rate.get),
                                     "holds": bool(min(rate.values()) >= 0.8)}
        hw = [(res["b"][r][npairs][k][1][1] - res["b"][r][npairs][k][1][0]) / 2
              for r in range(runs_b) for k in res["b"][r][npairs]]
        summary["b"][str(npairs)] = {"mean_half_width": float(np.mean(hw)), "holds": bool(np.mean(hw) <= 0.05)}
    ok = [n for n in cands if summary["a"][str(n)]["holds"] and summary["b"][str(n)]["holds"]]
    summary["per_class_n"] = min(ok) if ok else max(cands)
    summary["satisfied"] = bool(ok)
    return summary


def stage_large(c: dict, seeds: dict, n_large: int) -> dict:
    specs = []
    for cond, w in combos(c):
        for tag in ("A", "B"):
            specs.append((f"{ckey(cond, w)}|{tag}", cond, w, n_large, seeds[f"large_{tag}"]))
    data = generate(specs, c["grids_N"], chunk=100, label="large")
    jobs = []
    for cond, w in combos(c):
        k = ckey(cond, w)
        for ni, n in enumerate(c["grids_N"]):
            for proc in PROCS:
                for rep in REPRS:
                    for ds in c["descriptor_sets"]:
                        FA = features(data[f"{k}|A"]["X"], ni, rep, proc, ds)
                        FB = features(data[f"{k}|B"]["X"], ni, rep, proc, ds)
                        jobs.append((f"{k}|{n}|{proc}|{rep}|" + "+".join(ds), FA, FB))
    levels, t0 = {}, time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(level_job, j) for j in jobs]
        for d, fu in enumerate(as_completed(futs), 1):
            key, v = fu.result()
            levels[key] = v
            if d % max(1, len(jobs) // 20) == 0 or d == len(jobs):
                el = time.time() - t0
                print(f"[large] {d}/{len(jobs)} levels, {el:.0f} s, about {el / d * (len(jobs) - d):.0f} s left",
                      flush=True)
    moments = {}
    for cond, w in combos(c):
        k = ckey(cond, w)
        X = data[f"{k}|A"]["X"]  # pair, group, N, repr, proc, desc
        moments[k] = {"mean": X.mean(axis=0).tolist(), "sd": X.std(axis=0, ddof=1).tolist()}
    return {"n_per_group": n_large, "levels": levels, "moments_set_A": moments,
            "moments_axes": ["group", "N", "representation", "processing", "descriptor"]}


def level_job(job: tuple) -> tuple:
    key, FA, FB = job
    y = labels(FA.shape[0] // 2)
    if FA.shape[1] == 1:
        t, up = fit_threshold(FA[:, 0], y)
        v = {"method": "best threshold on set A",
             "level": float((predict_threshold(FA[:, 0], t, up) == y).mean()),
             "heldout_set_B": float((predict_threshold(FB[:, 0], t, up) == y).mean())}
    else:
        m = svm_model().fit(FA, y)
        v = {"method": "svm trained on set A, evaluated on set B", "level": float(m.score(FB, y)),
             "train_set_A": float(m.score(FA, y))}
    return key, v


def stage_frame(c: dict, large: dict) -> list[dict]:
    rows = []
    for r in table_rows(c):
        d, o = row_predictions(r)
        lv = large["levels"][rkey(r)]
        rows.append(dict(r, predicted_direction=d, predicted_order=o, predicted_level_large_sample=lv["level"],
                         predicted_level_detail=lv))
    return rows


def stage_experiment(c: dict, seeds: dict, npairs: int, n_boot: int, n_perm: int, partial: Path) -> dict:
    specs = [(ckey(cond, w), cond, w, npairs, seeds["experiment"]) for cond, w in combos(c)]
    data = generate(specs, c["grids_N"], label="experiment")
    mech_specs = [(f"{cond}_centre", cond, 0.0, 100, seeds["mechanism"]) for cond in ("i_V", "i_A")]
    mech = generate(mech_specs, c["grids_N"], label="mechanism")
    done = {}
    if partial.exists():
        saved = json.loads(partial.read_text())
        if saved.get("fingerprint") == fingerprint(npairs, n_boot, n_perm):
            done = saved["rows"]
            print(f"[experiment] resuming: {len(done)} rows already done", flush=True)
    rows = table_rows(c)
    jobs = []
    for r in rows:
        k = rkey(r)
        if k in done:
            continue
        X = features(data[ckey(r["condition"], r["w"])]["X"], c["grids_N"].index(r["N"]), r["representation"],
                     r["processing"], r["descriptor_set"])
        jobs.append((k, X, n_boot, n_perm))
    jobs.sort(key=lambda j: -j[1].shape[1])  # two-descriptor rows (svm only, slowest per fit) first
    t0, last = time.time(), time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(classify_row, j) for j in jobs]
        for d, fu in enumerate(as_completed(futs), 1):
            k, v = fu.result()
            done[k] = v
            if time.time() - last > 60 or d == len(jobs):
                partial.parent.mkdir(parents=True, exist_ok=True)
                partial.write_text(json.dumps({"fingerprint": fingerprint(npairs, n_boot, n_perm), "rows": done}))
                last = time.time()
                el = time.time() - t0
                print(f"[experiment] {len(done)}/{len(rows)} rows, {el:.0f} s, about "
                      f"{el / d * (len(jobs) - d):.0f} s left", flush=True)
    return {"rows": done, "data": data, "mech": mech}


def fingerprint(npairs, n_boot, n_perm) -> str:
    return f"{sha(COND)}|{sha(SPEC)}|{sha(PRED)}|{sha(Path(__file__))}|{npairs}|{n_boot}|{n_perm}"


# --- analysis -------------------------------------------------------------------------------------------------------


def unpack_data(saved: dict) -> dict:
    return {k: {"params": v["params"], "X": np.array(v["X"])} for k, v in saved.items()}


def pack_data(data: dict) -> dict:
    return {k: {"params": v["params"], "X": v["X"].tolist()} for k, v in data.items()}


def analyse(c: dict, frame: list[dict], res: dict, data: dict, mech: dict) -> dict:
    table = []
    for fr in frame:
        k = rkey(fr)
        v = res[k]
        row = {kk: fr[kk] for kk in ("condition", "w", "N", "processing", "representation", "descriptor_set",
                                     "predicted_direction", "predicted_order", "predicted_level_large_sample")}
        row.update({"estimate_finite_svm": v["svm"]["acc"], "ci95_svm": v["svm"]["ci95"],
                    "estimate_finite_threshold": v.get("threshold", {}).get("acc"),
                    "ci95_threshold": v.get("threshold", {}).get("ci95"),
                    "tost_chance": {clf: v[clf]["tost_chance"] for clf in v},
                    "perm_p": {clf: v[clf]["perm_p"] for clf in v},
                    "ci90": {clf: v[clf]["ci90"] for clf in v}})
        table.append(row)
    S = {"table1": table, "predictions": predictions(c, table, data), "mechanism": mechanism(c, mech),
         "clipping": clipping(c, data)}
    return S


def lookup(table: list[dict]) -> dict:
    return {(r["condition"], r["w"], r["N"], r["processing"], r["representation"], set_name(r["descriptor_set"])): r
            for r in table}


def acc(r: dict, clf: str):
    return r["estimate_finite_svm"] if clf == "svm" else r["estimate_finite_threshold"]


def max_rel_diff(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b) / np.maximum(np.abs(a), np.abs(b))))


def predictions(c: dict, table: list[dict], data: dict) -> dict:
    T = lookup(table)
    Ns, ws = c["grids_N"], c["jitter_w"]
    nonnull = [x for x in CENTRES]
    P = {}
    # P-K5-1
    items = []
    for clf in ("svm", "threshold"):
        bad = [(cd, w, n, p) for cd in ("ii_s", "ii_s_gamma", "corners") for w in ws for n in Ns for p in PROCS
               if acc(T[(cd, w, n, p, "minmax", "S")], clf) > acc(T[(cd, w, n, p, "H", "S")], clf)]
        items.append({"part": f"S on minmax <= S on H ({clf})", "cells": 3 * len(ws) * len(Ns) * len(PROCS),
                      "violations": len(bad), "violating": [list(map(str, b)) for b in bad], "holds": not bad})
    P["P-K5-1"] = items
    # P-K5-2
    items = []
    for clf in ("svm", "threshold"):
        bad = [(w, rep) for w in ws for rep in REPRS
               if acc(T[("i_A", w, 512, "raw", rep, "C")], clf) < acc(T[("i_A", w, 128, "raw", rep, "C")], clf)]
        items.append({"part": f"i_A raw C: N 512 >= N 128 ({clf})", "cells": len(ws) * len(REPRS),
                      "violations": len(bad), "violating": [list(map(str, b)) for b in bad], "holds": not bad})
    for clf in ("svm", "threshold"):
        for proc, sn in (("raw", "B"), ("hann", "C")):
            bad = []
            for w in ws:
                for rep in REPRS:
                    base = abs(acc(T[("i_A", w, 512, "raw", rep, "C")], clf) - acc(T[("i_A", w, 128, "raw", rep, "C")], clf))
                    dd = abs(acc(T[("i_A", w, 512, proc, rep, sn)], clf) - acc(T[("i_A", w, 128, proc, rep, sn)], clf))
                    if not dd < base:
                        bad.append((w, rep, dd, base))
            items.append({"part": f"i_A: |change with N| of {proc} {sn} < that of raw C ({clf})",
                          "cells": len(ws) * len(REPRS), "violations": len(bad),
                          "violating": [list(map(str, b)) for b in bad], "holds": not bad})
    P["P-K5-2"] = items
    # P-K5-3
    rows_null = [r for r in table if r["condition"] == "iii_null"]
    not_eq = [rkey(r) + "|" + clf for r in rows_null for clf, t in r["tost_chance"].items() if not t]
    rows_same = [r for r in table if r["condition"] == "check_same_seed"]
    not_half = [rkey(r) + "|" + clf for r in rows_same for clf in r["tost_chance"]
                if acc(r, clf) != 0.5]
    P["P-K5-3"] = [{"part": "iii_null at chance by the TOST in every column",
                    "columns": sum(len(r["tost_chance"]) for r in rows_null), "violations": len(not_eq),
                    "violating": not_eq, "holds": not not_eq},
                   {"part": "check_same_seed accuracy exactly 0.5", "columns": sum(len(r["tost_chance"]) for r in rows_same),
                    "violations": len(not_half), "violating": not_half, "holds": not not_half}]
    # P-K5-4
    rel = 0.0
    for k, v in data.items():
        X = v["X"]
        for di in (1, 2):
            rel = max(rel, max_rel_diff(X[..., 0, :, di], X[..., 1, :, di]))
    neq = [rkey(r) + "|" + clf + f" (minmax {acc(r, clf):.5f}, H {acc(h, clf):.5f})"
           for r in table if set_name(r["descriptor_set"]) in ("C", "B") and r["representation"] == "minmax"
           for h in [T[(r["condition"], r["w"], r["N"], r["processing"], "H", set_name(r["descriptor_set"]))]]
           for clf in ("svm", "threshold") if acc(r, clf) != acc(h, clf)]
    P["P-K5-4"] = [{"part": "centroids on minmax equal those on H (largest relative difference)", "value": rel,
                    "holds": rel < 1e-9},
                   {"part": "accuracies of C and B equal on minmax and H", "unequal_cells": len(neq),
                    "violating": neq, "holds": not neq}]
    # P-K5-5
    rel_m = rel_h = 0.0
    for w in ws:
        a, b = data[ckey("ii_s", w)]["X"], data[ckey("corners", w)]["X"]
        rel_m = max(rel_m, max_rel_diff(a[..., 1, :, :], b[..., 1, :, :]))
        rel_h = max(rel_h, max_rel_diff(a[..., 0, :, 1:], b[..., 0, :, 1:]))
    neq = []
    for w in ws:
        for n in Ns:
            for p in PROCS:
                for rep in REPRS:
                    for sn in ("S", "C", "B", "SC"):
                        if rep == "H" and sn in ("S", "SC"):
                            continue
                        for clf in (("svm", "threshold") if sn != "SC" else ("svm",)):
                            if acc(T[("ii_s", w, n, p, rep, sn)], clf) != acc(T[("corners", w, n, p, rep, sn)], clf):
                                neq.append(f"{w}|{n}|{p}|{rep}|{sn}|{clf} (ii_s "
                                           f"{acc(T[('ii_s', w, n, p, rep, sn)], clf):.5f}, corners "
                                           f"{acc(T[('corners', w, n, p, rep, sn)], clf):.5f})")
    P["P-K5-5"] = [{"part": "ii_s and corners: descriptors on minmax equal (largest relative difference)",
                    "value": rel_m, "holds": rel_m < 1e-9},
                   {"part": "ii_s and corners: centroids on H equal (largest relative difference)", "value": rel_h,
                    "holds": rel_h < 1e-9},
                   {"part": "ii_s and corners: accuracies equal in the predicted rows", "unequal_cells": len(neq),
                    "violating": neq, "holds": not neq}]
    # P-K5-6
    viol, tot = 0, 0
    for w in ws:
        X = data[ckey("i_V", w)]["X"]  # pair, group, N, repr, proc, desc
        d = X[:, 0, :, 0, 0, 0] - X[:, 1, :, 0, 0, 0]
        viol += int(np.sum(d <= 0))
        tot += d.size
    items = [{"part": "i_V raw H: sq of group 0 > sq of group 1 in every pair (all N and w)", "pairs": tot,
              "violations": viol, "holds": viol == 0}]
    for clf in ("svm", "threshold"):
        bad = [(w, n, p) for w in ws for n in Ns for p in PROCS
               if acc(T[("i_V", w, n, p, "minmax", "S")], clf) > acc(T[("i_V", w, n, p, "H", "S")], clf)]
        items.append({"part": f"i_V: S on minmax <= S on H ({clf})", "cells": len(ws) * len(Ns) * len(PROCS),
                      "violations": len(bad), "violating": [list(map(str, b)) for b in bad], "holds": not bad})
    P["P-K5-6"] = items
    # P-K5-7
    bad = []
    cells = [(cd, w, n, p, rep) for cd in nonnull for w in ws for n in Ns for p in PROCS for rep in REPRS]
    for cl in cells:
        sc, s_, c_ = (T[cl + (x,)]["estimate_finite_svm"] for x in ("SC", "S", "C"))
        if sc < max(s_, c_):
            bad.append("|".join(map(str, cl)) + f" SC {sc:.4f} < {max(s_, c_):.4f}")
    P["P-K5-7"] = [{"part": "svm: SC >= max(S, C)", "cells": len(cells), "violations": len(bad), "violating": bad,
                    "holds": not bad}]
    # P-K5-8
    bad, tot = [], 0
    for cd in nonnull:
        for n in Ns:
            for p in PROCS:
                for rep in REPRS:
                    for sn in ("S", "C", "B", "SC"):
                        a = [T[(cd, w, n, p, rep, sn)]["estimate_finite_svm"] for w in ws]
                        tot += 1
                        if not all(a[i] >= a[i + 1] for i in range(len(a) - 1)):
                            bad.append(f"{cd}|{n}|{p}|{rep}|{sn}: " + ", ".join(f"{x:.4f}" for x in a))
    P["P-K5-8"] = [{"part": "svm accuracy non-increasing in w", "columns": tot, "violations": len(bad),
                    "violating": bad, "holds": not bad}]
    # P-K5-9
    bad = []
    for w in ws:
        for n in Ns:
            a = T[("ii_s_gamma", w, n, "raw", "H", "S")]["estimate_finite_svm"]
            others = {cd: T[(cd, w, n, "raw", "H", "S")]["estimate_finite_svm"] for cd in ("i_V", "i_A", "ii_s", "corners")}
            if not all(a < v for v in others.values()):
                bad.append(f"{w}|{n}: {a:.4f} vs " + ", ".join(f"{k} {v:.4f}" for k, v in others.items()))
    P["P-K5-9"] = [{"part": "raw H: S of ii_s_gamma lower than S of the other non-null conditions",
                    "columns": len(ws) * len(Ns), "violations": len(bad), "violating": bad, "holds": not bad}]
    # P-K5-10
    bad, tot = [], 0
    for cd in ("i_A", "ii_s", "ii_s_gamma", "corners"):
        for rep in (REPRS if cd != "corners" else ("minmax",)):
            for w in ws:
                for n in Ns:
                    for p in PROCS:
                        g = lambda sn: T[(cd, w, n, p, rep, sn)]["estimate_finite_svm"]
                        tot += 1
                        if not (g("C") >= g("S") and g("B") >= g("S")):
                            bad.append(f"{cd}|{rep}|{w}|{n}|{p}: S {g('S'):.4f} C {g('C'):.4f} B {g('B'):.4f}")
    for w in ws:
        for n in Ns:
            for p in PROCS:
                g = lambda sn: T[("i_V", w, n, p, "H", sn)]["estimate_finite_svm"]
                tot += 1
                if not g("S") >= g("C"):
                    bad.append(f"i_V|H|{w}|{n}|{p}: S {g('S'):.4f} C {g('C'):.4f}")
    P["P-K5-10"] = [{"part": "order of single descriptors (svm)", "cells": tot, "violations": len(bad),
                     "violating": bad, "holds": not bad}]
    # P-K5-11
    items = []
    for clf in ("svm", "threshold"):
        bad = [(w, rep) for w in ws for rep in REPRS
               if acc(T[("i_V", w, 512, "raw", rep, "C")], clf) < acc(T[("i_V", w, 128, "raw", rep, "C")], clf)]
        items.append({"part": f"i_V raw C: N 512 >= N 128 ({clf})", "cells": len(ws) * len(REPRS),
                      "violations": len(bad), "violating": [list(map(str, b)) for b in bad], "holds": not bad})
    P["P-K5-11"] = items
    # P-K5-12
    rows12 = [r for r in table if r["condition"] in nonnull
              and not (r["condition"] == "ii_s_gamma" and set_name(r["descriptor_set"]) == "S")]
    bad = [rkey(r) for r in rows12 if not r["ci95_svm"][0] > 0.5]
    P["P-K5-12"] = [{"part": "95% interval of the svm accuracy above 0.5", "rows": len(rows12),
                     "violations": len(bad), "violating": bad, "holds": not bad}]
    return P


def mechanism(c: dict, mech: dict) -> dict:
    out = {}
    for k, v in mech.items():
        X = v["X"]  # pair, group, N, repr, proc, desc
        out[k] = {"params": [v["params"][0][0], v["params"][1][0]],
                  "mean": X.mean(axis=0).tolist(), "sd": X.std(axis=0, ddof=1).tolist(),
                  "min": X.min(axis=0).tolist(), "max": X.max(axis=0).tolist()}
    return out


def clipping(c: dict, data: dict) -> dict:
    out = {}
    for cond, w in combos(c):
        if cond in ("ii_s", "ii_s_gamma", "corners"):
            ps = data[ckey(cond, w)]["params"]
            out[ckey(cond, w)] = [float(np.mean([p["clipped"] for p in ps[g]])) for g in (0, 1)]
    return out


# --- reports --------------------------------------------------------------------------------------------------------


def fmt(x) -> str:
    if x is None:
        return "-"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return f"{x:.4g}"
    if isinstance(x, list):
        return "[" + ", ".join(fmt(v) for v in x) + "]"
    if isinstance(x, dict):
        return "; ".join(f"{k} {fmt(v)}" for k, v in x.items())
    return str(x)


def header(title: str, meta: dict) -> list[str]:
    return [f"# {title}", "",
            f"Conditions: `experiments/conditions/k5_classification.json` (SHA-256 `{meta['conditions_sha256']}`). "
            f"Predictions: `experiments/conditions/k5_table1_predictions.json` (SHA-256 `{meta['predictions_sha256']}`). "
            f"Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `{meta['spec_sha256']}`). "
            f"Script SHA-256 `{meta['script_sha256']}`. numpy {meta['numpy']}, scipy {meta['scipy']}, scikit-learn "
            f"{meta['sklearn']}, Python {meta['python']}. Run started {meta['started']} and finished "
            f"{meta.get('finished', '-')} ({meta['platform']}).", "",
            "## Reading of the conditions fixed before the run", ""] + [f"- {s}" for s in INTERPRETATION] + [""]


def report_power(meta: dict, S: dict) -> str:
    L = header("K5: choice of the number of pairs (TOST power)", meta)
    L += [f"Chosen per_class_n: **{S['per_class_n']}**" + ("" if S["satisfied"] else
          " (no candidate satisfied both requirements; the largest candidate is used)"), "",
          f"(a) iii_null, {S['runs_a']} runs: smallest equivalence rate over the columns, and its complement (the "
          "observed false non-equivalence rate). (b) corners, w = 0.5, N = 128, raw, H, svm, {sq, centroid_amp}, "
          f"{S['runs_b']} runs: mean half-width of the 95% interval.", "",
          "| n | (a) min rate | column with min rate | false non-equivalence | (a) holds | (b) mean half-width | (b) holds |",
          "|---|---|---|---|---|---|---|"]
    for n in S["candidates"]:
        a, b = S["a"][str(n)], S["b"][str(n)]
        L.append(f"| {n} | {a['min_rate']:.3f} | {a['min_rate_column']} | {1 - a['min_rate']:.3f} | {fmt(a['holds'])} | "
                 f"{b['mean_half_width']:.4f} | {fmt(b['holds'])} |")
    L += ["", "Equivalence rate by column, for each n:", "", "| column | " + " | ".join(str(n) for n in S["candidates"]) + " |",
          "|---|" + "---|" * len(S["candidates"])]
    for k in S["a"][str(S["candidates"][0])]["equivalence_rate"]:
        L.append(f"| {k} | " + " | ".join(f"{S['a'][str(n)]['equivalence_rate'][k]:.3f}" for n in S["candidates"]) + " |")
    return "\n".join(L) + "\n"


def report_large(meta: dict, S: dict) -> str:
    L = header("K5: predicted levels from large-sample simulation", meta)
    L += [f"{S['n_per_group']} surfaces per group in each of two sets.", "",
          "| row | method | level | other set |", "|---|---|---|---|"]
    for k, v in S["levels"].items():
        other = v.get("heldout_set_B", v.get("train_set_A"))
        L.append(f"| {k} | {v['method']} | {v['level']:.4f} | {other:.4f} |")
    return "\n".join(L) + "\n"


def report_frame(meta: dict, rows: list[dict]) -> str:
    L = header("K5: Table 1 frame (predictions entered before the experiment)", meta)
    L += ["| condition | w | N | processing | representation | set | predicted direction | predicted order | "
          "predicted level |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['condition']} | {fmt(r['w'])} | {r['N']} | {r['processing']} | {r['representation']} | "
                 f"{set_name(r['descriptor_set'])} | {'; '.join(r['predicted_direction'])} | "
                 f"{'; '.join(r['predicted_order'])} | {r['predicted_level_large_sample']:.4f} |")
    return "\n".join(L) + "\n"


def report_experiment(c: dict, meta: dict, S: dict, pred_text: dict) -> str:
    L = header("K5: Table 1", meta)
    L += [f"per_class_n = {meta['per_class_n']} (results/k5_power.json). Frame: results/k5_table1_frame.json "
          f"(SHA-256 `{meta['frame_sha256']}`). Set names: S = [sq], C = [centroid_amp], B = [centroid_band_power], "
          "SC = [sq, centroid_amp].", "", "## Predictions", ""]
    for key, items in S["predictions"].items():
        L += [f"### {key}: {sum(i['holds'] for i in items)} of {len(items)} items hold", "",
              f"Criterion: {pred_text[key]}", "", "| part | counts | holds |", "|---|---|---|"]
        for i in items:
            counts = "; ".join(f"{k} {fmt(v)}" for k, v in i.items() if k not in ("part", "holds", "violating"))
            L.append(f"| {i['part']} | {counts} | {fmt(i['holds'])} |")
        viol = [v for i in items for v in i.get("violating", [])]
        if viol:
            L += ["", "Violating cells: " + "; ".join(map(str, viol[:60])) + (" ..." if len(viol) > 60 else "")]
        L.append("")
    L += ["## Table 1", "",
          "| condition | w | N | proc | repr | set | level (large sample) | svm | 95% CI svm | threshold | 95% CI threshold "
          "| at chance (TOST) | perm p |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["table1"]:
        L.append(f"| {r['condition']} | {fmt(r['w'])} | {r['N']} | {r['processing']} | {r['representation']} | "
                 f"{set_name(r['descriptor_set'])} | {r['predicted_level_large_sample']:.4f} | "
                 f"{r['estimate_finite_svm']:.4f} | {fmt(r['ci95_svm'])} | {fmt(r['estimate_finite_threshold'])} | "
                 f"{fmt(r['ci95_threshold'])} | {fmt(r['tost_chance'])} | {fmt(r['perm_p'])} |")
    L += ["", "## Mechanism check (jitter-free centres, seeds 1000-1099)", "",
          "| condition | group | N | repr | proc | descriptor | mean | sd | min | max |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in S["mechanism"].items():
        for g in (0, 1):
            for ni, n in enumerate(c["grids_N"]):
                for a, rep in enumerate(REPRS):
                    for b, proc in enumerate(PROCS):
                        for di, dn in enumerate(DESC):
                            L.append(f"| {k} | {g} | {n} | {rep} | {proc} | {dn} | {v['mean'][g][ni][a][b][di]:.5g} | "
                                     f"{v['sd'][g][ni][a][b][di]:.3g} | {v['min'][g][ni][a][b][di]:.5g} | "
                                     f"{v['max'][g][ni][a][b][di]:.5g} |")
    L += ["", "## Clipping at the corners (fraction of surfaces with a clipped coordinate, group 0 / group 1)", "",
          "| condition | fractions |", "|---|---|"]
    for k, v in S["clipping"].items():
        L.append(f"| {k} | {fmt(v)} |")
    return "\n".join(L) + "\n"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--power", action="store_true", help="choose per_class_n (tost.power)")
    g.add_argument("--large-sample", action="store_true", help="large-sample levels")
    g.add_argument("--frame", action="store_true", help="write the Table 1 frame from the predictions and levels")
    g.add_argument("--report", action="store_true", help="rewrite the experiment results from the saved values")
    ap.add_argument("--smoke", metavar="DIR", help="run every stage on small numbers outside the conditions' seeds, "
                    "writing to DIR; for testing the script only")
    args = ap.parse_args()
    c = json.loads(COND.read_text())
    pred = json.loads(PRED.read_text())
    pred_text = {p["id"]: p["criterion"] for p in pred["predictions"]}
    if args.smoke:
        out, seeds = Path(args.smoke), SMOKE_SEEDS
        cfg = {"runs_a": 3, "runs_b": 2, "cands": [10, 20], "n_boot": 200, "n_large": 200, "n_perm": 19}
    else:
        out, seeds = OUT, SEEDS
        cfg = {"runs_a": 200, "runs_b": 50, "cands": c_cands(c), "n_boot": N_BOOT, "n_large": 5000, "n_perm": N_PERM}
    out.mkdir(parents=True, exist_ok=True)
    stages = (["power", "large", "frame", "experiment"] if args.smoke and not (args.power or args.large_sample
              or args.frame or args.report) else
              ["power"] if args.power else ["large"] if args.large_sample else ["frame"] if args.frame else
              ["report"] if args.report else ["experiment"])
    for stage in stages:
        run_stage(stage, c, pred_text, out, seeds, cfg)
    print("done")


def c_cands(c: dict) -> list[int]:
    """Candidates of pairs.per_class_n in the conditions file (stated there in words)."""
    assert "candidates 60, 120, 240, 480" in c["pairs"]["per_class_n"]
    return [60, 120, 240, 480]


def run_stage(stage: str, c: dict, pred_text: dict, out: Path, seeds: dict, cfg: dict):
    if stage == "power":
        meta = meta_base()
        S = stage_power(c, seeds, cfg["runs_a"], cfg["runs_b"], cfg["cands"], cfg["n_boot"])
        meta["finished"] = now()
        (out / "k5_power.json").write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION, "summary": S}))
        (out / "k5_power.md").write_text(report_power(meta, S))
    elif stage == "large":
        meta = meta_base()
        S = stage_large(c, seeds, cfg["n_large"])
        meta["finished"] = now()
        (out / "k5_large_sample.json").write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION,
                                                              "summary": S}))
        (out / "k5_large_sample.md").write_text(report_large(meta, S))
    elif stage == "frame":
        large = json.loads((out / "k5_large_sample.json").read_text())
        check_meta(large["meta"])
        meta = meta_base()
        meta["large_sample_sha256"] = sha(out / "k5_large_sample.json")
        rows = stage_frame(c, large["summary"])
        meta["finished"] = now()
        (out / "k5_table1_frame.json").write_text(json.dumps({"meta": meta, "rows": rows}))
        (out / "k5_table1_frame.md").write_text(report_frame(meta, rows))
    elif stage in ("experiment", "report"):
        js = out / f"{NAME}.json"
        if stage == "report":
            saved = json.loads(js.read_text())
            meta, res = saved["meta"], saved["rows"]
            data, mech = unpack_data(saved["data"]), unpack_data(saved["mechanism_data"])
            frame = json.loads((out / "k5_table1_frame.json").read_text())["rows"]
        else:
            power = json.loads((out / "k5_power.json").read_text())
            framef = json.loads((out / "k5_table1_frame.json").read_text())
            check_meta(power["meta"])
            check_meta(framef["meta"])
            frame = framef["rows"]
            meta = meta_base()
            meta["per_class_n"] = power["summary"]["per_class_n"]
            meta["frame_sha256"] = sha(out / "k5_table1_frame.json")
            meta["power_sha256"] = sha(out / "k5_power.json")
            r = stage_experiment(c, seeds, meta["per_class_n"], cfg["n_boot"], cfg["n_perm"], out / "partial" / f"{NAME}.json")
            res, data, mech = r["rows"], r["data"], r["mech"]
            meta["finished"] = now()
        check_meta(meta)
        if meta["frame_sha256"] != sha(out / "k5_table1_frame.json"):
            raise SystemExit("the Table 1 frame changed since the experiment was run")
        S = analyse(c, frame, res, data, mech)
        js.write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION, "summary": S, "rows": res,
                                  "data": pack_data(data), "mechanism_data": pack_data(mech)}))
        (out / f"{NAME}.md").write_text(report_experiment(c, meta, S, pred_text))


def check_meta(meta: dict):
    if (meta["conditions_sha256"] != sha(COND) or meta["spec_sha256"] != sha(SPEC)
            or meta["predictions_sha256"] != sha(PRED)):
        raise SystemExit("conditions, specification or predictions changed since the values were computed")


if __name__ == "__main__":
    main()
