"""Supplementary exploration of K4 (b): the centroid of the sum field up to N = 16384, extrapolations of the local
slopes and an estimate of the leading terms compared with the shell spectrum.

Usage:  uv run python experiments/k4_supplement.py            (compute, then write the results)
        uv run python experiments/k4_supplement.py --report   (rewrite the results from results/k4_supplement.json)
        uv run python experiments/k4_supplement.py --smoke DIR (small grids and seeds outside the conditions)
Conditions: experiments/conditions/k4_supplement.json (fixed and committed before this script was run)
Specification: experiments/spec/generator-and-descriptors.md
Output: results/k4_supplement.json (all values and the derived summaries) and results/k4_supplement.md

Exploratory: designed after the results of K4 had been seen. Where the conditions leave a choice open, the choice is
stated in INTERPRETATION below and in the results; it was fixed in this script before the computation was run.
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
import scipy.fft as sfft
from scipy.optimize import least_squares

from atact.field import _UNIT
from atact.stats import bonferroni_level, local_slopes, slopes_per_seed, t_interval
from atact.transform import t_gamma

ROOT = Path(__file__).resolve().parents[1]
COND = ROOT / "experiments" / "conditions" / "k4_supplement.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
K4_RESULTS = ROOT / "results" / "k4_centroid_2d.json"
K4_RESULTS_SHA256 = "257173c1b375595146a4f23a746fb8e2d8537a6df6426eeb1c82b40d37f6872a"  # commit cb369b4
SCRIPT = Path(__file__).resolve()
OUT = ROOT / "results"
NAME = "k4_supplement"
OCTAVES = 4
SHELLS_PER_OCTAVE = 8      # implementation.shell_spectrum: edges rho = 2^(j/8)
TOL_IMPL = 1e-9            # implementation.check
TOL_SHELL = 0.05           # P-S4
LEVEL = bonferroni_level(12)
BLOCK = 512                # rows (and half as many columns) per block of the low-memory DFT
WORKERS = {"xl": 3, "l": 6, "s": 8}  # N = 16384 about 2.5 GB per process, N = 8192 about 1 GB (timing run)
E_BOUND = 1e-6             # E1: a fitted c within this of 0 or 1.5 counts as ending at a bound

INTERPRETATION = [
    "Ranges are taken from the end of grids_N: the extrapolations use the last six N (512-16384) and, for the "
    "sensitivity range, the last five (1024-16384); the slopes of approach 1 use the last four (2048-16384) and the "
    "last three (4096-16384). With the grids of the conditions these are the ranges named there.",
    "Local slopes are per seed (atact.stats.local_slopes) and are placed at the geometric mean of the two grids. "
    "'Mean local slope' is the mean over the 20 seeds.",
    "E1 is fitted as ln C_N = ln(a + b (N/N_max)^c), N_max the largest N of the range, which is the same model with b "
    "rescaled; scipy.optimize.least_squares (trust-region reflective) with bounds a >= -(1 - 1e-9) min C_N, b >= 0 and "
    f"0 <= c <= 1.5, started from a = 0, c = the last local slope of the range clipped to [0.01, 1.49] and b = C at "
    f"N_max. A fit counts as failed if the optimiser reports no success or if c ends within {E_BOUND} of 0 or 1.5.",
    "Shell spectrum: rho = |k| in cycles per domain for every bin with rho >= 1; the shell index is "
    f"floor({SHELLS_PER_OCTAVE} log2 rho); each bin enters with its weight of the half-plane sum (2 or 1), so that a "
    "shell holds the sum over the full plane. The density divides the shell sum of |H^_k| / N^2 by the width of the "
    "shell (the last shell cut at the largest rho of the grid, unless that would give it zero width; the last shell "
    "never enters the band of the shell exponent). The shell exponent is the least-squares slope of ln density on the "
    "logarithm of the geometric centre of the shell.",
    "Rate of approach: the deficit is e(gamma) - s_j for the five local slopes of the extrapolation range; 'their seed "
    "means decrease with N' is strict for each consecutive pair.",
    "The implementation check is made after all N <= 4096 have been computed and before any larger N is computed; "
    "if it fails, the run stops there.",
    "E1 failure cases beyond those on c: the growing term changes the model over the range by less than 1e-6 max C_N "
    "(b (1 - (N_min/N_max)^c) < 1e-6 max C_N; this includes b at its lower bound 0, where c is not identified), "
    "a ends within 1e-9 min C_N "
    "of its lower bound, or the fitted model value is not finite and positive at every N. Inside the optimiser a "
    "non-positive model value is evaluated as 1e-300 (a large residual); such a fit is then failed by the last rule.",
    "E3 uses the exact delta(gamma) (7/18, 3/10, 1/14, 3/26); the condition file also lists them rounded to four "
    "places.",
    "Shells are half-open, [2^(j/8), 2^((j+1)/8)); a bin is assigned by floor(8 log2 rho) in floating point, so a bin "
    "with rho exactly on an edge (for example rho = 512) goes to the shell that starts there.",
    "The rate of approach is given an interval only if at least 2 seeds have all five deficits positive. The "
    "difference between the two grids in the shell table is the seed mean at the larger N minus that at the smaller "
    "N, without an interval.",
    "Standard errors by N and per-seed values (local slopes, fits, deficit signs) are in the JSON file; the Markdown "
    "file shows the seed means and the intervals.",
]


def load_conditions() -> dict:
    return json.loads(COND.read_text())


def e_gamma(g: float) -> float:
    return min(1.0, 1.5 - 1.0 / g)


def delta_gamma(g: float) -> float:
    """approach_3_estimate: the order of the leading correction of the local slope."""
    a = 1.0 / g
    return min(1.5 - a, a - 0.5) if a > 0.5 else 0.5 - a


# --- computation ----------------------------------------------------------------------------------------------------


def octave_vectors(f: float, n: int, seed: int, octaves: int = OCTAVES):
    """Draws and vectors of procedural_field_separable (same order): (amplitude, y-vector, x-vector) per octave."""
    rng = np.random.default_rng(seed)
    x = np.arange(n) / n
    out = []
    for o in range(octaves):
        fo, a = f * 2**o, 0.5**o
        px, py = rng.uniform(0, 2 * np.pi, 2)
        w = _UNIT["cycles"] * fo
        out.append((a, np.sin(w * x + py), np.sin(w * x + px)))
    return out


def _field_rows(vecs, i0: int, i1: int) -> np.ndarray:
    F = np.zeros((i1 - i0, len(vecs[0][2])))
    for a, vy, vx in vecs:
        F += a * np.outer(vy[i0:i1], vx)
    return F


def shell_index(rho: np.ndarray) -> np.ndarray:
    return np.floor(SHELLS_PER_OCTAVE * np.log2(rho)).astype(np.int64)


def shell_edges(n: int) -> np.ndarray:
    """Edges 2^(j/8) of the logarithmic shells, up to the shell of the largest rho of the grid, whose upper edge is
    cut at that rho (left uncut if the cut would give the shell zero width)."""
    rmax = np.hypot(np.float64(n // 2), np.float64(n // 2))  # the same arithmetic as the bin (N/2, N/2)
    nsh = int(shell_index(np.array([rmax]))[0]) + 1
    e = 2.0 ** (np.arange(nsh + 1) / SHELLS_PER_OCTAVE)
    if rmax > e[-2]:
        e[-1] = min(e[-1], rmax)
    return e


def lean_centroid(f: float, n: int, seed: int, g: float, block: int = BLOCK) -> dict:
    """implementation.rule: centroid_amp of S2.3 for T_gamma of the four-octave sum field, and the shell sums."""
    vecs = octave_vectors(f, n, seed)
    block = min(block, n)
    mx = 0.0
    for i0 in range(0, n, block):
        mx = max(mx, float(np.abs(_field_rows(vecs, i0, min(n, i0 + block))).max()))
    half = np.empty((n, n // 2 + 1), dtype=np.complex128)
    for i0 in range(0, n, block):
        i1 = min(n, i0 + block)
        half[i0:i1] = sfft.rfft(t_gamma(_field_rows(vecs, i0, i1) / mx, g), axis=1)
    kx = np.arange(n // 2 + 1, dtype=float)
    ky = np.abs(np.fft.fftfreq(n) * n)
    wcol = np.full(n // 2 + 1, 2.0)
    wcol[0] = wcol[-1] = 1.0
    edges = shell_edges(n)
    shells = np.zeros(len(edges) - 1)
    num = den = 0.0
    cb = max(1, block // 2)
    for j0 in range(0, n // 2 + 1, cb):
        j1 = min(n // 2 + 1, j0 + cb)
        mag = np.abs(sfft.fft(half[:, j0:j1], axis=0, overwrite_x=True))
        if j0 == 0:
            mag[0, 0] = 0.0
        rho = np.hypot(ky[:, None], kx[None, j0:j1])
        wm = mag * wcol[None, j0:j1]
        num += float((rho * wm).sum())
        den += float(wm.sum())
        keep = rho >= 1.0
        b = np.bincount(shell_index(rho[keep]), weights=wm[keep], minlength=len(shells))
        if len(b) != len(shells):
            raise RuntimeError("a bin lies outside the shells")
        shells += b
    density = shells / n**2 / np.diff(edges)
    return {"centroid_amp": num / den, "shell_density": density.tolist()}


def jobs_from(c: dict) -> list[tuple]:
    return [(f, g, n, s) for f in c["f"] for g in c["gamma"] for n in c["grids_N"] for s in c["seeds"]]


def run_job(job: tuple) -> dict:
    """finite_values: a centroid that is not finite and positive, or a shell density that is not finite, stops the run."""
    f, g, n, s = job
    v = lean_centroid(f, n, s, g)
    if not (np.isfinite(v["centroid_amp"]) and v["centroid_amp"] > 0 and np.isfinite(v["shell_density"]).all()):
        raise RuntimeError(f"non-finite value for job {job}")
    return {"f": f, "gamma": g, "N": n, "seed": s, **v}


def memory_class(job: tuple) -> str:
    n = job[2]
    return "xl" if n >= 16384 else ("l" if n >= 8192 else "s")


def _key(r) -> tuple:
    return (r["f"], r["gamma"], r["N"], r["seed"])


def run_identity(c: dict) -> dict:
    """What the rows of a run depend on (resume rule of the conditions): compared on resume."""
    import scipy

    return {"conditions_sha256": sha(COND), "spec_sha256": sha(SPEC), "k4_results_sha256": sha(K4_RESULTS),
            "script_sha256": sha(SCRIPT), "numpy": np.__version__, "scipy": scipy.__version__,
            "python": sys.version.split()[0], "block": BLOCK, "grids_N": c["grids_N"], "seeds": c["seeds"]}


def read_partial(partial: Path, identity: dict, jobs: list[tuple]) -> tuple[dict, str | None]:
    """Rows of an interrupted run and its start time. Refuses a partial file written by another version or containing
    a row that is not a job of this run; a last line cut off by an interruption is dropped with a warning."""
    if not partial.exists():
        return {}, None
    lines = partial.read_text().splitlines()
    if not lines:
        return {}, None
    head = json.loads(lines[0])
    if head.get("identity") != identity:
        raise SystemExit(f"{partial} was written by another version of the conditions, script or libraries; "
                         "refusing to resume (move it away to start again)")
    wanted = set(jobs)
    done = {}
    for i, line in enumerate(lines[1:], 2):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            if i == len(lines):
                print(f"warning: dropping a cut-off last line of {partial}", flush=True)
                continue
            raise
        if _key(r) not in wanted:
            raise SystemExit(f"{partial} contains a row that is not a job of this run: {_key(r)}")
        done[_key(r)] = r
    return done, head["started"]


def compute(c: dict, partial: Path, check_against: dict | None, identity: dict, started: str) -> tuple[list[dict], str]:
    """Runs the jobs class by class (small N first), appending each result to `partial` so that an interrupted run
    resumes. After the small class, the implementation check is made (if `check_against` is given). Returns the rows
    and the start time of the first attempt."""
    jobs = jobs_from(c)
    done, first_start = read_partial(partial, identity, jobs)
    if first_start is None:
        partial.write_text(json.dumps({"identity": identity, "started": started}) + "\n")
        first_start = started
    else:
        print(f"resuming: {len(done)} jobs already done (first started {first_start})", flush=True)
        if partial.read_text()[-1:] != "\n":
            partial.write_text("\n".join(partial.read_text().splitlines()[:-1]) + "\n")
    with partial.open("a") as fh:
        for cls in ("s", "l", "xl"):
            part = [j for j in jobs if memory_class(j) == cls and j not in done]
            part.sort(key=lambda j: -j[2])
            t0 = time.time()
            if part:
                with ProcessPoolExecutor(max_workers=WORKERS[cls]) as ex:
                    futs = [ex.submit(run_job, j) for j in part]
                    for i, fu in enumerate(as_completed(futs), 1):
                        r = fu.result()
                        done[_key(r)] = r
                        fh.write(json.dumps(r) + "\n")
                        fh.flush()
                        el = time.time() - t0
                        if i % max(1, len(part) // 20) == 0 or i == len(part):
                            print(f"[{cls}] {i}/{len(part)} jobs, {el:.0f} s, about {el / i * (len(part) - i):.0f} s "
                                  "left", flush=True)
            if cls == "s" and check_against is not None:
                chk = implementation_check(list(done.values()), check_against)
                print(f"implementation check: max relative difference {chk['max_rel_diff']:.2e} over "
                      f"{chk['n_compared']} values", flush=True)
                if not chk["passed"]:
                    raise SystemExit("implementation check failed; larger N not computed")
    return [done[j] for j in jobs], first_start


def k4_reference(c: dict) -> dict:
    """centroid_amp (raw) of the 12 cells stored by K4, keyed like _key."""
    if sha(K4_RESULTS) != K4_RESULTS_SHA256:
        raise SystemExit("results/k4_centroid_2d.json is not the file of commit cb369b4")
    rows = json.loads(K4_RESULTS.read_text())["rows"]
    ref = {}
    for r in rows:
        if (r["field"] == "sum" and r["sampling"] == "direct" and r["r"] == 1 and r["normalize"] == "maxabs"
                and r["f"] in c["f"] and r["gamma"] in c["gamma"]):
            ref[(r["f"], r["gamma"], r["N"], r["seed"])] = r["values"]["raw"]["centroid_amp"]
    return ref


def implementation_check(rows: list[dict], ref: dict) -> dict:
    """implementation.check: every value with N <= 4096 against the K4 value of the same cell, seed and N."""
    diffs = []
    missing = 0
    for r in rows:
        if r["N"] > 4096:
            continue
        k = _key(r)
        if k not in ref:
            missing += 1
            continue
        v, w = float(r["centroid_amp"]), float(ref[k])
        ok = np.isfinite(v) and np.isfinite(w) and v > 0 and w > 0
        diffs.append(abs(v / w - 1) if ok else float("inf"))
    expected = len([k for k in ref if k[2] <= 4096])
    d = np.asarray(diffs, dtype=float)
    worst = float(d.max()) if d.size and np.isfinite(d).all() else float("inf")
    return {"n_compared": len(diffs), "n_expected": expected, "missing": missing, "max_rel_diff": worst,
            "passed": bool(d.size) and missing == 0 and len(diffs) == expected and bool(np.isfinite(d).all())
            and worst <= TOL_IMPL}


# --- analysis -------------------------------------------------------------------------------------------------------


def series(rows, f, g, Ns, seeds) -> np.ndarray:
    idx = {(r["seed"], r["N"]): r for r in rows if r["f"] == f and r["gamma"] == g}
    return np.array([[idx[(s, n)]["centroid_amp"] for n in Ns] for s in seeds])


def fit_e1(N, C) -> dict:
    """approach_2 E1 for one seed: ln C = ln(a + b (N/N_max)^c)."""
    N = np.asarray(N, dtype=float)
    C = np.asarray(C, dtype=float)
    x = N / N[-1]
    ls = np.diff(np.log(C)) / np.diff(np.log(N))
    c0 = float(np.clip(ls[-1], 0.01, 1.49))
    lo = [-(1 - 1e-9) * C.min(), 0.0, 0.0]
    hi = [np.inf, np.inf, 1.5]
    x0 = [0.0, float(C[-1]), c0]

    def res(p):
        v = p[0] + p[1] * x ** p[2]
        return np.log(np.maximum(v, 1e-300)) - np.log(C)

    r = least_squares(res, x0, bounds=(lo, hi), method="trf", x_scale="jac", max_nfev=20000)
    a, b, c = (float(v) for v in r.x)
    model = a + b * x**c
    reasons = []
    if not r.success:
        reasons.append("no convergence")
    if c <= E_BOUND or c >= 1.5 - E_BOUND:
        reasons.append("c at a bound")
    if not b * (1 - x[0] ** c) >= 1e-6 * C.max():
        reasons.append("growing term not identified")
    if a <= lo[0] + 1e-9 * C.min():
        reasons.append("a at its bound")
    if not (np.isfinite(model).all() and (model > 0).all() and np.isfinite(r.x).all()):
        reasons.append("model not finite and positive")
    return {"a": a, "b": b, "c": c, "failed": bool(reasons), "reasons": reasons, "cost": float(r.cost)}


def fit_linear_intercept(u, s) -> float:
    """Intercept of the least-squares line s = s_inf + d u."""
    A = np.column_stack([np.ones_like(u), u])
    coef, *_ = np.linalg.lstsq(A, s, rcond=None)
    return float(coef[0])


def outcome(t: dict, e: float) -> str:
    if not (np.isfinite(t["lo"]) and np.isfinite(t["hi"])):
        return "not determined"
    return "contains e(gamma)" if t["lo"] <= e <= t["hi"] else ("below" if t["hi"] < e else "above")


def extrapolations(N, C, g) -> dict:
    """E1, E2 and E3 on one range (N and C of shape (seeds, len(N)))."""
    e = e_gamma(g)
    ls = local_slopes(N, C)
    Nm = np.sqrt(np.asarray(N[:-1], dtype=float) * np.asarray(N[1:], dtype=float))
    out = {}
    fits = [fit_e1(N, row) for row in C]
    ok = [x["c"] for x in fits if not x["failed"]]
    nf = len(fits) - len(ok)
    if nf > 2 or len(ok) < 2:
        out["E1"] = {"n_failed": nf, "outcome": "not determined", "fits": fits}
    else:
        t = t_interval(ok, LEVEL)
        out["E1"] = {**t, "n_failed": nf, "outcome": outcome(t, e), "fits": fits}
    for name, u in (("E2", 1.0 / np.log(Nm)), ("E3", Nm ** (-delta_gamma(g)))):
        vals = [fit_linear_intercept(u, row) for row in ls]
        t = t_interval(vals, LEVEL)
        out[name] = {**t, "n_failed": 0, "outcome": outcome(t, e), "values": vals}
    return out


def shell_exponent(rows, f, g, n, seeds, band) -> dict | None:
    """approach_3 compared quantity 1: slope of ln density on ln centre over the shells inside band = [lo, hi)."""
    sub = {r["seed"]: r for r in rows if r["f"] == f and r["gamma"] == g and r["N"] == n}
    if not sub:
        return None
    edges = shell_edges(n)
    js = [j for j in range(len(edges) - 1) if edges[j] >= band[0] - 1e-9 and edges[j + 1] <= band[1] + 1e-9]
    lc = np.log(np.sqrt(edges[js] * edges[[j + 1 for j in js]]))
    sl = []
    for s in seeds:
        y = np.log(np.asarray(sub[s]["shell_density"])[js])
        xc = lc - lc.mean()
        sl.append(float((y - y.mean()) @ xc / (xc @ xc)))
    return {**t_interval(sl, LEVEL), "n_shells": len(js), "per_seed": sl}


def rate_of_approach(N, C, g) -> dict:
    """approach_3 compared quantity 2."""
    e = e_gamma(g)
    ls = local_slopes(N, C)
    Nm = np.sqrt(np.asarray(N[:-1], dtype=float) * np.asarray(N[1:], dtype=float))
    d = e - ls
    pos = (d > 0).all(axis=1)
    rates = []
    for row in d[pos]:
        x = np.log(Nm)
        y = np.log(row)
        xc = x - x.mean()
        rates.append(float((y - y.mean()) @ xc / (xc @ xc)))
    mean_d = d.mean(axis=0)
    out = {"n_positive_seeds": int(pos.sum()), "deficit_mean": mean_d.tolist(),
           "deficit_signs": [[int(np.sign(v)) for v in row] for row in d],
           "mean_decreasing": bool((np.diff(mean_d) < 0).all()), "target": -delta_gamma(g)}
    if len(rates) >= 2:
        out["rate"] = t_interval(rates, 0.95)
    return out


def analyse(c: dict, rows: list[dict], check: dict | None) -> dict:
    seeds = c["seeds"]
    Nall = c["grids_N"]
    band = c.get("_shell_band", [512, 2048])
    S = {"implementation_check": check, "cells": []}
    for f in c["f"]:
        for g in c["gamma"]:
            C = series(rows, f, g, Nall, seeds)
            ls = local_slopes(Nall, C)
            cell = {"f": f, "gamma": g, "e": e_gamma(g), "delta": delta_gamma(g), "target_shell": -(1 / g + 0.5),
                    "N": Nall, "mean_by_N": C.mean(axis=0).tolist(),
                    "se_by_N": (C.std(axis=0, ddof=1) / np.sqrt(len(seeds))).tolist(),
                    "local_mean": ls.mean(axis=0).tolist(),
                    "local_se": (ls.std(axis=0, ddof=1) / np.sqrt(len(seeds))).tolist(), "slopes": {}}
            for k in (4, 3):
                Nr = Nall[-k:]
                t = t_interval(slopes_per_seed(Nr, C[:, -k:]), LEVEL)
                cell["slopes"][f"{Nr[0]}-{Nr[-1]}"] = {**t, "outcome": outcome(t, e_gamma(g))}
            cell["extrapolation"] = {}
            for k in (6, 5):
                Nr = Nall[-k:]
                cell["extrapolation"][f"{Nr[0]}-{Nr[-1]}"] = extrapolations(Nr, C[:, -k:], g)
            cell["shell"] = {str(n): shell_exponent(rows, f, g, n, seeds, band) for n in Nall[-2:]}
            cell["rate"] = rate_of_approach(Nall[-6:], C[:, -6:], g)
            S["cells"].append(cell)
    S["predictions"] = predictions(c, S)
    return S


def predictions(c, S) -> dict:
    P = {}
    nmax = str(c["grids_N"][-1])
    items = []
    for x in S["cells"]:
        ls = x["local_mean"]
        items.append({"f": x["f"], "gamma": x["gamma"], "local_last_three": ls[-3:],
                      "holds": bool(ls[-2] > ls[-3] and ls[-1] > ls[-2])})
    P["P-S1"] = {"items": items}
    items = []
    k3 = f"{c['grids_N'][-3]}-{c['grids_N'][-1]}"
    for x in S["cells"]:
        t = x["slopes"][k3]
        items.append({"f": x["f"], "gamma": x["gamma"], "e": x["e"], "slope": t["mean"], "lo": t["lo"], "hi": t["hi"],
                      "holds": bool(t["hi"] < x["e"])})
    P["P-S2"] = {"items": items}
    items = []
    for x in S["cells"]:
        for rng, ex in x["extrapolation"].items():
            for form in ("E1", "E2", "E3"):
                v = ex[form]
                items.append({"f": x["f"], "gamma": x["gamma"], "range": rng, "form": form, "e": x["e"],
                              "value": v.get("mean"), "lo": v.get("lo"), "hi": v.get("hi"),
                              "n_failed": v["n_failed"], "outcome": v["outcome"], "holds": None})
    P["P-S3"] = {"items": items, "note": "No direction predicted; outcomes are reported."}
    items = []
    for x in S["cells"]:
        t = x["shell"][nmax]
        tg = x["target_shell"]
        items.append({"f": x["f"], "gamma": x["gamma"], "target": tg, "exponent": t["mean"], "lo": t["lo"],
                      "hi": t["hi"], "width": t["hi"] - t["lo"], "holds": bool(t["lo"] <= tg + TOL_SHELL and t["hi"] >= tg - TOL_SHELL)})
    P["P-S4"] = {"items": items}
    items = []
    n_seeds = len(c["seeds"])
    for x in S["cells"]:
        r = x["rate"]
        rt = r.get("rate")
        ok = (r["n_positive_seeds"] == n_seeds and r["mean_decreasing"] and rt is not None
              and rt["lo"] <= r["target"] <= rt["hi"])
        items.append({"f": x["f"], "gamma": x["gamma"], "target": r["target"], "n_positive_seeds": r["n_positive_seeds"],
                      "mean_decreasing": r["mean_decreasing"], "rate": rt["mean"] if rt else None,
                      "lo": rt["lo"] if rt else None, "hi": rt["hi"] if rt else None, "holds": bool(ok)})
    P["P-S5"] = {"items": items}
    return P


# --- report ---------------------------------------------------------------------------------------------------------


def fmt(x, p=3):
    return "-" if x is None else f"{x:.{p}f}"


def write_report(c: dict, meta: dict, S: dict) -> str:
    Nall = c["grids_N"]
    L = ["# K4 supplement: the centroid of the sum field up to N = 16384, extrapolations and an estimate", "",
         f"Conditions: `experiments/conditions/k4_supplement.json` (SHA-256 `{meta['conditions_sha256']}`). "
         f"Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `{meta['spec_sha256']}`). "
         f"Reference values of the implementation check: `results/k4_centroid_2d.json` (SHA-256 "
         f"`{meta['k4_results_sha256']}`). numpy {meta['numpy']}, scipy {meta['scipy']}, Python {meta['python']}. "
         f"Script SHA-256 `{meta['script_sha256']}`, repository commit `{meta['git_commit']}`"
         f"{' (with uncommitted changes to the files read)' if meta['git_dirty'] else ''}. "
         f"Run started {meta['started']}{' (resumed)' if meta['resumed'] else ''} and finished {meta['finished']} "
         f"({meta['platform']}).", "",
         "Exploratory: designed after the results of K4 had been seen; not blind; not evidence for the claims of the "
         "main text. Nothing here is a proof, and the extrapolated values are not limits.", "",
         "## Reading of the conditions fixed before the run", ""]
    L += [f"- {s}" for s in INTERPRETATION]
    ch = S["implementation_check"]
    L += ["", "## Implementation check", ""]
    if ch is None:
        L += ["Not made (smoke run).", ""]
    else:
        L += [f"{ch['n_compared']} of {ch['n_expected']} values (N 128-4096) compared with K4; largest relative "
              f"difference {ch['max_rel_diff']:.2e}; {'passed' if ch['passed'] else 'FAILED'} (tolerance {TOL_IMPL}).",
              ""]
    L += ["## Approach 1: local slopes and slopes over the larger ranges", "",
          f"Local slopes: seed means between consecutive N ({Nall[0]}-{Nall[1]}, ..., {Nall[-2]}-{Nall[-1]}). Slopes: "
          f"simultaneous intervals at level {LEVEL:.5f}.", "",
          "| f | gamma | e(gamma) | local slopes | slope, interval, outcome | slope, interval, outcome |",
          "|---|---|---|---|---|---|"]
    for x in S["cells"]:
        sl = [f"{k}: {fmt(v['mean'], 4)} [{fmt(v['lo'], 4)}, {fmt(v['hi'], 4)}] {v['outcome']}"
              for k, v in x["slopes"].items()]
        L.append(f"| {x['f']} | {x['gamma']} | {fmt(x['e'], 4)} | {', '.join(fmt(v) for v in x['local_mean'])} | "
                 f"{sl[0]} | {sl[1]} |")
    L += ["", "## Approach 2: extrapolated exponents", "",
          f"Mean over seeds and simultaneous interval (level {LEVEL:.5f}); E1 over the seeds whose fit did not fail.", "",
          "| f | gamma | e(gamma) | range | form | value | interval | failed seeds | outcome |",
          "|---|---|---|---|---|---|---|---|---|"]
    for i in S["predictions"]["P-S3"]["items"]:
        iv = "-" if i["lo"] is None else f"[{fmt(i['lo'], 4)}, {fmt(i['hi'], 4)}]"
        L.append(f"| {i['f']} | {i['gamma']} | {fmt(i['e'], 4)} | {i['range']} | {i['form']} | {fmt(i['value'], 4)} | "
                 f"{iv} | {i['n_failed']} | {i['outcome']} |")
    L += ["", "## Approach 3: shell spectrum and rate of approach", "",
          "Shell exponent: slope of ln(shell density) on ln rho over the shells in the band of the conditions, mean and "
          f"simultaneous interval (level {LEVEL:.5f}), at the two largest N; target -(1/gamma + 1/2).", "",
          "| f | gamma | target | " + " | ".join(f"N = {n}" for n in Nall[-2:]) + " | difference |",
          "|---|---|---|" + "---|" * 3]
    for x in S["cells"]:
        a, b = (x["shell"][str(n)] for n in Nall[-2:])
        L.append(f"| {x['f']} | {x['gamma']} | {fmt(x['target_shell'], 4)} | "
                 f"{fmt(a['mean'], 4)} [{fmt(a['lo'], 4)}, {fmt(a['hi'], 4)}] | "
                 f"{fmt(b['mean'], 4)} [{fmt(b['lo'], 4)}, {fmt(b['hi'], 4)}] | {b['mean'] - a['mean']:+.4f} |")
    L += ["", f"Rate of approach over the local slopes of N {Nall[-6]}-{Nall[-1]}: deficit e(gamma) - s_j (seed means), "
          "number of seeds with all five deficits positive, fitted slope of ln deficit on ln N_j (95% interval over "
          "those seeds) and the target -delta(gamma).", "",
          "| f | gamma | deficits | positive seeds | means decrease | rate | interval | target |",
          "|---|---|---|---|---|---|---|---|"]
    for x in S["cells"]:
        r = x["rate"]
        rt = r.get("rate")
        L.append(f"| {x['f']} | {x['gamma']} | {', '.join(f'{v:+.4f}' for v in r['deficit_mean'])} | "
                 f"{r['n_positive_seeds']} | {'yes' if r['mean_decreasing'] else 'no'} | "
                 f"{fmt(rt['mean'] if rt else None, 4)} | "
                 f"{'-' if not rt else '[' + fmt(rt['lo'], 4) + ', ' + fmt(rt['hi'], 4) + ']'} | {fmt(r['target'], 4)} |")
    L += ["", "## Predictions", ""]
    for key, p in S["predictions"].items():
        text = [x for x in c["predictions"] if x.startswith(key + " ")][0]
        if key == "P-S3":
            L += [f"### {key}: outcomes reported (no direction predicted)", "", f"Prediction: {text}", "",
                  "See the table of approach 2.", ""]
            continue
        L += [f"### {key}: {sum(i['holds'] for i in p['items'])} of {len(p['items'])} items hold", "",
              f"Prediction: {text}", ""]
        keys = list(dict.fromkeys(k for i in p["items"] for k in i if k != "holds"))
        L += ["| " + " | ".join(keys) + " | holds |", "|" + "---|" * (len(keys) + 1)]
        for i in p["items"]:
            cells = []
            for k in keys:
                v = i.get(k, "-")
                cells.append(", ".join(fmt(u) for u in v) if isinstance(v, list)
                             else (fmt(v) if isinstance(v, float) else str(v)))
            L.append("| " + " | ".join(cells) + f" | {'yes' if i['holds'] else 'no'} |")
        L.append("")
    L += ["## Seed means of the centroid by N", "",
          f"| f | gamma | N {Nall[0]} ... {Nall[-1]} (mean; standard error of the last) |", "|---|---|---|"]
    for x in S["cells"]:
        L.append(f"| {x['f']} | {x['gamma']} | {', '.join(fmt(v, 2) for v in x['mean_by_N'])} "
                 f"({x['se_by_N'][-1]:.2g}) |")
    return "\n".join(L) + "\n"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_state() -> dict:
    """Commit of the repository and whether the files the computation reads differ from it."""
    import subprocess

    def run(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()

    paths = ["experiments/k4_supplement.py", "experiments/conditions", "experiments/spec", "src", "pyproject.toml",
             "uv.lock"]
    return {"git_commit": run("rev-parse", "HEAD"), "git_dirty": bool(run("status", "--porcelain", "--", *paths))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="rewrite the results from the saved values")
    ap.add_argument("--smoke", metavar="DIR", help="run the whole pipeline on small grids and seeds outside the "
                    "conditions (101-103), writing to DIR; for testing the script only")
    args = ap.parse_args()
    c = load_conditions()
    out = OUT
    ref = None
    if args.smoke:
        c = dict(c, grids_N=[32, 64, 128, 256, 512, 1024], seeds=[101, 102, 103], _shell_band=[32, 128])
        out = Path(args.smoke)
    else:
        ref = k4_reference(c)
    out.mkdir(exist_ok=True)
    js = out / f"{NAME}.json"
    partial = out / f"{NAME}.partial.jsonl"
    if args.report:
        saved = json.loads(js.read_text())
        meta, rows, check = saved["meta"], saved["rows"], saved["summary"]["implementation_check"]
    else:
        identity = run_identity(c)
        now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        rows, started = compute(c, partial, ref, identity, now)
        meta = {**{k: v for k, v in identity.items() if k not in ("grids_N", "seeds")}, **git_state(),
                "platform": f"{platform.system()} {platform.machine()}, {os.cpu_count()} logical CPUs",
                "started": started, "resumed": started != now,
                "finished": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        check = implementation_check(rows, ref) if ref is not None else None
    for k, p in (("conditions_sha256", COND), ("spec_sha256", SPEC), ("k4_results_sha256", K4_RESULTS),
                 ("script_sha256", SCRIPT)):
        if meta[k] != sha(p):
            raise SystemExit(f"{p.name} changed since the values were computed")
    S = analyse(c, rows, check)
    js.write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION, "summary": S, "rows": rows}))
    (out / f"{NAME}.md").write_text(write_report(c, meta, S))
    if partial.exists() and not args.report:
        partial.unlink()
    print("written", js)


if __name__ == "__main__":
    main()
