"""K2 and K6: maximum gradient against N for T_gamma and T_{gamma,eps}, and the worked example tying eps to a printer.

Usage:  uv run python experiments/k2_gradient.py              (compute, then write the results; refuses to overwrite)
        uv run python experiments/k2_gradient.py --report     (rewrite the report from results/k2_gradient.json)
        uv run python experiments/k2_gradient.py --smoke DIR  (seeds outside the conditions; tests the script only)
Conditions: experiments/conditions/k2_gradient_and_figures.json (fixed and committed before this script was run)
Specification: experiments/spec/generator-and-descriptors.md
Output: results/k2_gradient.json and results/k2_gradient.md

Where the conditions leave a choice open, the choice is stated in INTERPRETATION below; it was fixed in this script
before the computation was run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from atact.field import procedural_field_separable
from atact.stats import local_slopes, slopes_per_seed, t_interval
from atact.transform import t_gamma, t_gamma_eps

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve()
COND = ROOT / "experiments" / "conditions" / "k2_gradient_and_figures.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
LIBS = [ROOT / "src" / "atact" / n for n in ("field.py", "transform.py", "stats.py")] + [ROOT / "uv.lock"]
OUT_JSON = ROOT / "results" / "k2_gradient.json"
OUT_MD = ROOT / "results" / "k2_gradient.md"

SLOPE_RANGE = (512, 1024, 2048, 4096)
RATIO_N = (128, 2048)  # ratio M_2048 / M_128
CHANGE_N = (1024, 4096)  # P-G5
OCTAVES = 4
AMPSUM = sum(0.5**o for o in range(OCTAVES))  # 1.875
TOL = 1e-12
WORKERS = 4  # each N = 4096 job holds about 1-1.5 GB

INTERPRETATION = [
    "The gradient of S2.6 is numpy.gradient(X, 1/N) for X = F, H and H_eps on the same F; its magnitude is "
    "hypot(d/dx, d/dy) and the maximum is over all grid points, edges included. edge_argmax is true when the grid "
    "point of the maximum lies in the first or last row or column.",
    "Primary normalisation ampsum (F = F_raw / 1.875); the secondary maxabs values (G and M only) use F_raw divided by "
    "its maximum absolute value over the same grid.",
    "G* is the largest G_4096 (ampsum) over the 20 seeds at the point 'high'. Each eps = e_min G* / (2 L) is computed "
    "once with its own (L, e_min); the main eps is used at every point, the sensitivity values at 'high' only.",
    "Ratios, slopes and changes are computed per seed and then summarised over seeds (mean, minimum, maximum; slopes "
    "also with the 95% t interval of S6.1). P-G5: |mean Meps_4096 / mean Meps_1024 - 1| < 0.05 and mean M_4096 / "
    "mean M_1024 > 2, on seed means.",
    "P-G4 and P-G6 are checked for every seed and N at the points with gamma > 1 and for every eps computed there. "
    "The shape error is max |T_{gamma,eps}(F) - T_gamma(F)| over the grid (that is max |H_eps - H| / s).",
    "Physical quantities use z = D H / (2 s_max): slope = D |grad H| / (2 s_max L), angle = atan(slope) in degrees, "
    "span = D (max H - min H) / (2 s_max). The band width at a seed is 2 eps L / G_4096 of that seed, in mm. The "
    "grid bound on the smoothed slope uses G*, the continuous bound uses G_bound = 2 pi f O / 1.875.",
]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_conditions() -> dict:
    return json.loads(COND.read_text())


def git_state() -> dict:
    def run(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()

    paths = ["experiments/k2_gradient.py", "experiments/conditions", "experiments/spec", "src", "pyproject.toml",
             "uv.lock"]
    return {"git_commit": run("rev-parse", "HEAD"), "git_dirty": bool(run("status", "--porcelain", "--", *paths))}


def identity() -> dict:
    import scipy

    return {"conditions_sha256": sha256(COND), "spec_sha256": sha256(SPEC), "script_sha256": sha256(SCRIPT),
            "library_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in LIBS},
            "numpy": np.__version__, "scipy": scipy.__version__, "python": sys.version.split()[0]}


def max_grad(X: np.ndarray) -> tuple[float, bool]:
    n = X.shape[0]
    gy, gx = np.gradient(X, 1.0 / n)
    m = np.hypot(gx, gy)
    j, i = np.unravel_index(int(np.argmax(m)), m.shape)
    return float(m[j, i]), bool(i in (0, n - 1) or j in (0, n - 1))


def sigma_eps(g: float, eps: float) -> float:
    """Largest slope of T_{gamma,eps} on [-1, 1] for gamma > 1 (at u = 0)."""
    return eps ** (1.0 / g - 1.0) * (1.0 + eps**2) ** ((1.0 - 1.0 / g) / 2.0)


def g_bound(f: float) -> float:
    return 2 * np.pi * f * OCTAVES / AMPSUM


def field(f: float, n: int, seed: int, norm: str) -> np.ndarray:
    return procedural_field_separable(f, n, seed, octaves=OCTAVES, normalize=norm)


def job_field_grad(args: tuple) -> tuple:
    f, n, seed = args
    return seed, max_grad(field(f, n, seed, "ampsum"))[0]


def job_all(args: tuple) -> tuple:
    name, f, s, g, n, seed, eps_list = args
    out = {"Meps": {}, "Meps_edge": {}, "shape_error": {}}
    for norm in ("maxabs", "ampsum"):
        F = field(f, n, seed, norm)
        T = t_gamma(F, g)
        G, _ = max_grad(F)
        M, edge = max_grad(s * T)
        if norm == "maxabs":
            out.update({"G_maxabs": G, "M_maxabs": M})
            continue
        out.update({"G": G, "M": M, "M_edge": edge, "span_H": float(s * (T.max() - T.min()))})
        for label, eps in eps_list:
            Te = t_gamma_eps(F, g, eps)
            out["Meps"][label], out["Meps_edge"][label] = max_grad(s * Te)
            out["shape_error"][label] = float(np.abs(Te - T).max())
    return (name, n, seed), out


def sens_label(x: dict) -> str:
    return f"L{x['L_mm']:g}_e{x['e_min_mm']:g}"


def eps_values(c: dict, G_star: float) -> dict:
    ex = c["eps_example"]
    eps = {"main": ex["e_min_mm"] * G_star / (2 * ex["L_mm"])}
    for x in ex["sensitivity_values"]:
        eps[sens_label(x)] = x["e_min_mm"] * G_star / (2 * x["L_mm"])
    return eps


def run(c: dict, seeds: list[int], Ns: list[int], workers: int) -> dict:
    hi = next(p for p in c["points"] if p["name"] == "high")
    nmax = max(Ns)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        g_hi = dict(pool.map(job_field_grad, [(hi["f"], nmax, sd) for sd in seeds]))
        G_star = max(g_hi.values())
        eps = eps_values(c, G_star)
        jobs = []
        for p in c["points"]:
            labels = list(eps) if p["name"] == "high" else ["main"]
            for n in Ns:
                for sd in seeds:
                    jobs.append((p["name"], p["f"], p["s"], p["gamma"], n, sd, [(k, eps[k]) for k in labels]))
        res = dict(pool.map(job_all, jobs, chunksize=1))
    return {"G_star": G_star, "G_Nmax_high": {str(k): v for k, v in g_hi.items()}, "eps": eps,
            "values": [{"point": k[0], "N": k[1], "seed": k[2], **v} for k, v in sorted(res.items())]}


def array(vals: list[dict], point: str, Ns, seeds, getter) -> np.ndarray:
    look = {(v["point"], v["N"], v["seed"]): v for v in vals}
    return np.array([[getter(look[(point, n, sd)]) for n in Ns] for sd in seeds], dtype=float)


def summ(v) -> dict:
    v = np.asarray(v, dtype=float)
    return {"mean": float(v.mean()), "min": float(v.min()), "max": float(v.max())}


def growth(Ns, X: np.ndarray, gamma: float) -> dict:
    Ns = list(Ns)
    if not set(SLOPE_RANGE) | set(RATIO_N) <= set(Ns):
        raise ValueError("the grids must contain RATIO_N and the slope range")
    r = X[:, Ns.index(RATIO_N[1])] / X[:, Ns.index(RATIO_N[0])]
    idx = [Ns.index(n) for n in SLOPE_RANGE]
    sl = slopes_per_seed(list(SLOPE_RANGE), X[:, idx])
    return {"ratio_2048_128": {**summ(r), "per_seed": r.tolist(), "reference_16^(1-1/gamma)": (RATIO_N[1] / RATIO_N[0]) ** (1 - 1 / gamma)},
            "slope_512_4096": {**t_interval(sl), "per_seed": sl.tolist(), "reference_1-1/gamma": 1 - 1 / gamma},
            "local_slopes_mean": local_slopes(Ns, X).mean(axis=0).tolist(),
            "seed_mean_by_N": X.mean(axis=0).tolist(), "seed_min_by_N": X.min(axis=0).tolist(),
            "seed_max_by_N": X.max(axis=0).tolist()}


def phys(x, d: dict) -> np.ndarray:
    """Physical slope D |grad H| / (2 s_max L) for an array of |grad H|."""
    return d["D_mm"] * np.asarray(x, dtype=float) / (2 * d["s_max"] * d["L_mm"])


def angle(slope) -> np.ndarray:
    return np.degrees(np.arctan(slope))


def analyse(c: dict, raw: dict, seeds, Ns) -> dict:
    vals, eps = raw["values"], raw["eps"]
    pts = {p["name"]: p for p in c["points"]}
    A: dict = {"eps": eps, "G_star": raw["G_star"], "points": {}}
    for name, p in pts.items():
        g, s = p["gamma"], p["s"]
        G = array(vals, name, Ns, seeds, lambda v: v["G"])
        M = array(vals, name, Ns, seeds, lambda v: v["M"])
        P = {"G": growth(Ns, G, g), "M": growth(Ns, M, g),
             "G_maxabs": growth(Ns, array(vals, name, Ns, seeds, lambda v: v["G_maxabs"]), g),
             "M_maxabs": growth(Ns, array(vals, name, Ns, seeds, lambda v: v["M_maxabs"]), g),
             "M_edge_count_by_N": array(vals, name, Ns, seeds, lambda v: v["M_edge"]).sum(axis=0).tolist(),
             "eps": {}}
        labels = list(eps) if name == "high" else ["main"]
        for lab in labels:
            Me = array(vals, name, Ns, seeds, lambda v: v["Meps"][lab])
            E = {"Meps": growth(Ns, Me, g),
                 "Meps_edge_count_by_N": array(vals, name, Ns, seeds,
                                               lambda v: v["Meps_edge"][lab]).sum(axis=0).tolist()}
            if g > 1:
                se = sigma_eps(g, eps[lab])
                ratio = Me / (s * se * G)
                err = array(vals, name, Ns, seeds, lambda v: v["shape_error"][lab])
                E.update({"sigma_eps": se, "Meps_over_bound_by_seed_N": ratio.tolist(),
                          "Meps_over_bound_max": float(ratio.max()),
                          "shape_error": {"max": float(err.max()), "bound_eps^(1/gamma)": eps[lab] ** (1 / g)}})
            P["eps"][lab] = E
        A["points"][name] = P
    A["example"] = example(c, raw, seeds, Ns)
    A["predictions"] = predictions(A, Ns)
    return A


def example(c: dict, raw: dict, seeds, Ns) -> dict:
    vals, eps = raw["values"], raw["eps"]
    hi = next(p for p in c["points"] if p["name"] == "high")
    ex = c["eps_example"]
    cases = [("main", ex["L_mm"], ex["e_min_mm"])] + [(sens_label(x), x["L_mm"], x["e_min_mm"])
                                                       for x in ex["sensitivity_values"]]
    G = array(vals, "high", Ns, seeds, lambda v: v["G"])
    M = array(vals, "high", Ns, seeds, lambda v: v["M"])
    span = array(vals, "high", Ns, seeds, lambda v: v["span_H"])
    scale = ex["D_mm"] / (2 * ex["s_max"])
    out = {}
    for lab, L, emin in cases:
        d = {"L_mm": L, "e_min_mm": emin, "D_mm": ex["D_mm"], "s_max": ex["s_max"]}
        e = eps[lab]
        se = sigma_eps(hi["gamma"], e)
        Me = array(vals, "high", Ns, seeds, lambda v: v["Meps"][lab])
        err = array(vals, "high", Ns, seeds, lambda v: v["shape_error"][lab])
        rows = []
        for j, n in enumerate(Ns):
            row = {"N": n, "grid_spacing_mm": L / n}
            for nm, X in (("T_gamma", M[:, j]), ("T_gamma_eps", Me[:, j]), ("field_sG", hi["s"] * G[:, j])):
                sl = phys(X, d)
                row[nm] = {"slope": summ(sl), "angle_deg": summ(angle(sl)), "slope_per_seed": sl.tolist()}
            rows.append(row)
        band = 2 * e * L / G[:, -1]
        b_grid = float(phys(hi["s"] * se * raw["G_star"], d))
        b_cont = float(phys(hi["s"] * se * g_bound(hi["f"]), d))
        out[lab] = {"L_mm": L, "e_min_mm": emin, "eps": e, "sigma_eps": se,
                    "band_width_mm": {**summ(band), "per_seed": band.tolist()},
                    "span_mm_at_Nmax": {**summ(scale * span[:, -1]), "per_seed": (scale * span[:, -1]).tolist()},
                    "rows": rows,
                    "smoothed_slope_bound_grid": {"slope": b_grid, "angle_deg": float(angle(b_grid))},
                    "smoothed_slope_bound_continuous": {"slope": b_cont, "angle_deg": float(angle(b_cont)),
                                                        "G_bound": g_bound(hi["f"])},
                    "shape_error_mm": {"max_at_Nmax": float(scale * hi["s"] * err[:, -1].max()),
                                       "bound": float(scale * hi["s"] * e ** (1 / hi["gamma"]))}}
    return out


def predictions(A: dict, Ns) -> dict:
    pts = A["points"]
    P: dict = {"P-G1": [], "P-G2": [], "P-G3": [], "P-G4": [], "P-G5": [], "P-G6": []}
    for name in ("mid", "high"):
        r = pts[name]["M"]["ratio_2048_128"]
        ref = r["reference_16^(1-1/gamma)"]
        P["P-G1"].append({"point": name, "min_ratio": r["min"], "mean_ratio": r["mean"], "reference": ref,
                          "holds": r["min"] > 1 and abs(r["mean"] / ref - 1) <= 0.20})
        sl = pts[name]["M"]["slope_512_4096"]
        P["P-G2"].append({"point": name, "mean": sl["mean"], "ci95": [sl["lo"], sl["hi"]],
                          "reference": sl["reference_1-1/gamma"],
                          "holds": abs(sl["mean"] - sl["reference_1-1/gamma"]) <= 0.05})
        for lab, E in pts[name]["eps"].items():
            mx = E["Meps_over_bound_max"]
            P["P-G4"].append({"point": name, "eps": lab, "largest_Meps_over_bound": mx, "holds": mx <= 1 + TOL})
            se = E["shape_error"]
            P["P-G6"].append({"point": name, "eps": lab, **se,
                              "holds": se["max"] <= se["bound_eps^(1/gamma)"] * (1 + TOL)})
    lo = pts["low"]["M"]
    P["P-G3"].append({"max_ratio": lo["ratio_2048_128"]["max"], "mean_slope": lo["slope_512_4096"]["mean"],
                      "holds": lo["ratio_2048_128"]["max"] < 1.5 and lo["slope_512_4096"]["mean"] < 0.05})
    i1, i4 = Ns.index(CHANGE_N[0]), Ns.index(CHANGE_N[1])
    m = pts["high"]["M"]["seed_mean_by_N"]
    gr = m[i4] / m[i1]
    for lab, E in pts["high"]["eps"].items():
        me = E["Meps"]["seed_mean_by_N"]
        ch = me[i4] / me[i1]
        P["P-G5"].append({"eps": lab, "Meps_4096_over_1024": ch, "M_4096_over_1024": gr,
                          "holds": abs(ch - 1) < 0.05 and gr > 2})
    for v in P.values():
        for it in v:
            it["holds"] = bool(it["holds"])
    return P


def fmt(x, d=4) -> str:
    return f"{x:.{d}f}"


def write_md(res: dict) -> str:
    m, A = res["meta"], res["analysis"]
    Ns = res["grids_N"]
    L = ["# K2: maximum gradient against N, and the eps example", "",
         f"Conditions: `experiments/conditions/k2_gradient_and_figures.json` (SHA-256 `{m['conditions_sha256']}`). "
         f"Specification SHA-256 `{m['spec_sha256']}`. Script SHA-256 `{m['script_sha256']}`. Commit "
         f"{m['git_commit'][:7]} (dirty: {m['git_dirty']}). numpy {m['numpy']}, scipy {m['scipy']}, Python "
         f"{m['python']}, {m['workers']} workers. Run started {m['started']} and finished {m['finished']} "
         f"({m['platform']}).{' SMOKE RUN: seeds outside the conditions.' if m.get('smoke') else ''}", "",
         "## Reading of the conditions fixed before the run", ""]
    L += [f"- {t}" for t in res["interpretation"]]
    L += ["", "## Predictions", ""]
    for k, items in A["predictions"].items():
        L += [f"### {k}: {sum(it['holds'] for it in items)} of {len(items)} items hold", ""]
        for it in items:
            L.append("- " + ", ".join(f"{a} = {fmt(b) if isinstance(b, float) else b}" for a, b in it.items()))
        L.append("")
    L += [f"## Growth with N (seed means over {len(res['seeds'])} seeds; ampsum unless marked)", ""]
    for name, P in A["points"].items():
        L += [f"### point {name}", "", "| quantity | " + " | ".join(f"N = {n}" for n in Ns) +
              " | ratio 2048/128 (mean, min-max) | slope 512-4096 (mean [95% CI]) |",
              "|---|" + "---|" * len(Ns) + "---|---|"]
        series = [("G", P["G"]), ("M", P["M"]), ("G (maxabs)", P["G_maxabs"]), ("M (maxabs)", P["M_maxabs"])]
        series += [(f"Meps ({lab})", E["Meps"]) for lab, E in P["eps"].items()]
        for q, g in series:
            r, sl = g["ratio_2048_128"], g["slope_512_4096"]
            L.append(f"| {q} | " + " | ".join(fmt(x, 3) for x in g["seed_mean_by_N"]) +
                     f" | {fmt(r['mean'], 3)} ({fmt(r['min'], 3)}-{fmt(r['max'], 3)}) | "
                     f"{fmt(sl['mean'])} [{fmt(sl['lo'])}, {fmt(sl['hi'])}] |")
        L += ["", "Local slopes of M (seed means): " + ", ".join(fmt(x) for x in P["M"]["local_slopes_mean"]),
              "Seeds whose maximum of M lies on the edge, by N: "
              + ", ".join(str(int(x)) for x in P["M_edge_count_by_N"]), ""]
    L += ["## Worked example (point 'high': f = 7, s = 0.30, gamma = 2.6; D = 1.2 mm)", ""]
    for lab, ex in A["example"].items():
        gb, cb = ex["smoothed_slope_bound_grid"], ex["smoothed_slope_bound_continuous"]
        L += [f"### {lab}: L = {ex['L_mm']:g} mm, e_min = {ex['e_min_mm']:g} mm", "",
              f"eps = {fmt(ex['eps'])}, sigma_eps = {fmt(ex['sigma_eps'])}, G* = {fmt(A['G_star'], 3)}. Band width "
              f"2 eps L / G_4096 over seeds: {fmt(ex['band_width_mm']['min'])}-{fmt(ex['band_width_mm']['max'])} mm. "
              f"Actual span of the relief at the largest N: {fmt(ex['span_mm_at_Nmax']['min'])}-"
              f"{fmt(ex['span_mm_at_Nmax']['max'])} mm. Bound on the slope of the smoothed relief: grid "
              f"{fmt(gb['slope'], 3)} ({fmt(gb['angle_deg'], 1)} deg), continuous {fmt(cb['slope'], 3)} "
              f"({fmt(cb['angle_deg'], 1)} deg). Shape error at the largest N: "
              f"{fmt(ex['shape_error_mm']['max_at_Nmax'])} mm (bound {fmt(ex['shape_error_mm']['bound'])} mm).", "",
              "| N | grid spacing (mm) | T_gamma: angle (deg), mean (min-max) | T_gamma_eps: angle | s F: angle |",
              "|---|---|---|---|---|"]
        for r in ex["rows"]:
            cells = [f"{fmt(r[k]['angle_deg']['mean'], 1)} ({fmt(r[k]['angle_deg']['min'], 1)}-"
                     f"{fmt(r[k]['angle_deg']['max'], 1)})" for k in ("T_gamma", "T_gamma_eps", "field_sG")]
            L.append(f"| {r['N']} | {fmt(r['grid_spacing_mm'], 4)} | " + " | ".join(cells) + " |")
        L.append("")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--smoke", type=Path)
    ap.add_argument("--workers", type=int, default=WORKERS)
    a = ap.parse_args()
    if a.report:
        res = json.loads(OUT_JSON.read_text())
        for k, p in (("conditions_sha256", COND), ("spec_sha256", SPEC), ("script_sha256", SCRIPT)):
            if res["meta"][k] != sha256(p):
                raise SystemExit(f"{p.name} changed since the values were computed")
        OUT_MD.write_text(write_md(res))
        return
    c = load_conditions()
    if a.smoke:
        seeds = [900001, 900002, 900003]
        a.smoke.mkdir(parents=True, exist_ok=True)
        out_json, out_md = a.smoke / "k2_gradient.json", a.smoke / "k2_gradient.md"
    else:
        seeds = c["seeds"]
        out_json, out_md = OUT_JSON, OUT_MD
        if out_json.exists():
            raise SystemExit(f"{out_json} exists; remove it to recompute")
    Ns = c["grids_N"]
    ident = identity()
    meta = {**ident, **git_state(), "workers": a.workers, "smoke": bool(a.smoke),
            "platform": f"{platform.system()} {platform.machine()}, {os.cpu_count()} logical CPUs",
            "started": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    raw = run(c, seeds, Ns, a.workers)
    meta["finished"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if identity() != ident:
        raise SystemExit("an input file changed during the run")
    res = {"meta": meta, "interpretation": INTERPRETATION, "seeds": seeds, "grids_N": Ns, "raw": raw,
           "analysis": analyse(c, raw, seeds, Ns)}
    out_json.write_text(json.dumps(res, indent=1) + "\n")
    out_md.write_text(write_md(res))
    print(f"written {out_json}")


if __name__ == "__main__":
    main()
