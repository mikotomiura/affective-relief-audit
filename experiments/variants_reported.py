"""Supplement: the accuracies reported in Harada (2026) against the reconstruction, for the variants fixed in
experiments/conditions/variants.json (version 1), and the check that a domain warp does not change Table 1 (K5).

Usage:
  uv run python experiments/variants_reported.py                # full run (refuses uncommitted inputs)
  uv run python experiments/variants_reported.py --smoke DIR    # a few variants and replicates, written to DIR
  uv run python experiments/variants_reported.py --report       # rewrite the Markdown from the JSON
Output: results/variants_reported.json and results/variants_reported.md

All values come from the reconstructed generator, not from the original code. Nothing here is evidence for the
claims of the main text; it is reported in the supplement.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import itertools
import json
import os
import platform
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import scipy
import sklearn

from atact.classify import REGIMES
from atact.descriptors import centroid_variant, rq
from atact.field import RenderConfig, height, procedural_field
from atact.spectral import windowed
from atact.transform import t_gamma

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import k5_classification as k5  # noqa: E402

COND = ROOT / "experiments" / "conditions" / "variants.json"
INDEX = ROOT / "experiments" / "conditions" / "INDEX.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
K5_JSON = ROOT / "results" / "k5_classification.json"
SCRIPT = Path(__file__).resolve()
LIBS = [ROOT / "src" / "atact" / f for f in
        ("__init__.py", "classify.py", "descriptors.py", "field.py", "mapping.py", "spectral.py", "transform.py")]
ENV = [ROOT / "pyproject.toml", ROOT / "uv.lock"]
K5_SCRIPT = ROOT / "experiments" / "k5_classification.py"
OUT_JSON = ROOT / "results" / "variants_reported.json"
OUT_MD = ROOT / "results" / "variants_reported.md"
OUT_PARTIAL = ROOT / "results" / "partial" / "variants_reported.variants.json"
WORKERS = 8

DEF_KEYS = ("weight", "center", "rescale", "half", "rho_round")
DEF_GRID = {"weight": ("amp", "power"), "center": (True, False), "rescale": (None, "minmax"),
            "half": (False, True), "rho_round": (False, True)}
DEFINITIONS = [dict(zip(DEF_KEYS, v)) for v in itertools.product(*(DEF_GRID[k] for k in DEF_KEYS))]
WINDOWS = ("raw", "hann")
PER_CLASS, BASE_SEED = 60, 42

INTERPRETATION = [
    "Dataset: for each (noise, jitter w, warp, N) and dataset replicate r (0-19), 60 surfaces per regime at the "
    "corners (1, -1) and (-1, 1), drawn as in atact.classify.make_dataset: rng = default_rng(r); for each surface "
    "V and A are the corner plus U(-w, w), clipped to [-1, 1]; the surface seed is 42 + index (0-119), the same in "
    "every replicate (assumption A5), so the replicates differ only in the jitter draws. The field is "
    "atact.field.procedural_field with RenderConfig(n=N, noise=noise, warp=warp), maxabs normalisation, four "
    "octaves, product form; with warp > 0 the two warp layers are drawn before the octave phases (A3).",
    "Descriptors: raw uses H; hann uses the windowed array of S3.1 (atact.spectral.windowed), and both descriptors "
    "are computed on that array: Sq = atact.descriptors.rq and the centroid = atact.descriptors.centroid_variant "
    "with one of the 32 definitions. 'center' and 'rescale' of a definition therefore act on the windowed array "
    "under hann (it is already centred, so center = False adds nothing there except through rescale). Sq does not "
    "depend on the centroid definition, so the Sq-only accuracy is computed once per (noise, w, window, warp, N).",
    "Cross-validation: RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=0) for every variant and "
    "replicate, a pipeline StandardScaler + SVC(kernel='linear', C=1) on the single descriptor; the accuracy of a "
    "replicate is the mean over the 100 test folds (as atact.classify.evaluate).",
    "Delta = accuracy - reported value, for sq_only (reported 0.916) and centroid_only (0.742). The point estimate is "
    "the mean of Delta over the 20 replicates; the 95% interval is the percentile interval of the 20 values "
    "(numpy.percentile, linear interpolation). The binomial width shown beside it is 1.96 sqrt(p (1 - p) / 120) at the "
    "reported p, for reference only.",
    "Reading rule (fixed in the conditions): a variant can explain a reported value if the interval of Delta for "
    "that column contains 0. Direction: whether the mean Sq-only accuracy exceeds the mean centroid-only accuracy.",
    "Warp check: every condition and jitter w of k5_classification.json at N = 128, processing raw, representation H, "
    "the four descriptor sets and both classifiers, with the 480 pairs and seeds of the K5 experiment (pair i: "
    "seed 1000 + i; iii_null group 1: 50000 + i) and the jitter streams of K5 (k5_classification.jitter_u). The "
    "field is procedural_field with warp 0.25. As an implementation control the same is computed with warp 0 by "
    "procedural_field and compared with the stored accuracies of K5 (results/k5_classification.json), which used "
    "procedural_field_separable; the two must agree exactly. The out-of-fold accuracy uses the folds and "
    "classifiers of K5; no bootstrap or permutation is run for the check.",
    "Warp and the draws: with warp > 0 the two warp layers consume the first draws of default_rng(seed), so the octave "
    "phases differ from those at warp 0 for the same seed. The difference between warp 0.25 and warp 0 therefore "
    "mixes the effect of the warp with a redraw of the surfaces. No interval is computed for it; the 95% pair-bootstrap "
    "interval stored by K5 for the warp-0 accuracy is shown beside it as a reference for the size of sampling "
    "variation.",
    "Implementation control: if any warp-0 accuracy differs from the stored K5 value, the run stops before writing the "
    "results (the variants are kept in results/partial/ for diagnosis). The warp check runs first, the variants second; "
    "the variants are written to results/partial/ as soon as they are finished.",
    "Counting: the Sq-only accuracy does not depend on the centroid definition, so each of the 72 combinations of "
    "(noise, w, warp, N, window) appears in 32 rows with the same Sq-only values. Counts for Sq only are given both "
    "as combinations (of 72) and as rows (of 2304).",
]


# --- identity -------------------------------------------------------------------------------------------------------


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def identity() -> dict:
    return {"conditions_sha256": sha256(COND), "index_sha256": sha256(INDEX), "spec_sha256": sha256(SPEC),
            "script_sha256": sha256(SCRIPT), "k5_script_sha256": sha256(K5_SCRIPT), "k5_results_sha256": sha256(K5_JSON),
            "library_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in LIBS},
            "environment_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in ENV}}


def git_state(strict: bool = True) -> dict:
    paths = [str(p.relative_to(ROOT)) for p in (COND, INDEX, SPEC, SCRIPT, K5_SCRIPT, K5_JSON, *LIBS, *ENV)]

    def run(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()

    if strict:  # the full run requires every input to be tracked
        for p in paths:
            try:
                run("ls-files", "--error-unmatch", p)
            except subprocess.CalledProcessError:
                raise SystemExit(f"{p} is not tracked; commit it first") from None
    return {"git_commit": run("rev-parse", "HEAD"), "git_dirty": bool(run("status", "--porcelain", "--", *paths))}


def load_conditions() -> dict:
    c = json.loads(COND.read_text())
    idx = json.loads(INDEX.read_text())["conditions"]["variants.json"]
    if idx["sha256"] != sha256(COND) or idx["version"] != c["version"]:
        raise SystemExit("variants.json does not match its entry in INDEX.json")
    v = c["variants"]
    if (v["noise"], v["jitter_w"], v["warp"], v["grids_N"]) != ([0.0, 0.1, 0.3], [1.0, 1.25, 1.5], [0.0, 0.25],
                                                                 [128, 256]):
        raise SystemExit("the variant grid differs from the one this script implements")
    if len(DEFINITIONS) != 32:
        raise SystemExit("expected 32 centroid definitions")
    return c


# --- variants -------------------------------------------------------------------------------------------------------


def def_name(d: dict) -> str:
    return (f"{d['weight']}|center={d['center']}|rescale={d['rescale'] or 'none'}|half={d['half']}"
            f"|round={d['rho_round']}")


def dataset_features(noise: float, w: float, warp: float, n: int, r: int) -> tuple[np.ndarray, np.ndarray]:
    """Features (120, 2 windows x (1 + 32)) and labels for one dataset replicate."""
    rng = np.random.default_rng(r)
    cfg = RenderConfig(n=n, noise=noise, warp=warp)
    rows, y, i = [], [], 0
    for label, (V0, A0) in REGIMES.items():
        for _ in range(PER_CLASS):
            V = float(np.clip(V0 + rng.uniform(-w, w), -1, 1))
            A = float(np.clip(A0 + rng.uniform(-w, w), -1, 1))
            H = height(V, A, cfg, seed=BASE_SEED + i)
            feats = []
            for win in WINDOWS:
                X = H if win == "raw" else windowed(H)
                feats.append(rq(X))
                feats.extend(centroid_variant(X, **d) for d in DEFINITIONS)
            rows.append(feats)
            y.append(label)
            i += 1
    return np.array(rows), np.array(y)


def cv_accuracy(x: np.ndarray, y: np.ndarray) -> float:
    from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score

    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=0)
    return float(cross_val_score(k5.svm_model(), x[:, None], y, cv=cv).mean())


def variant_job(job: tuple) -> tuple:
    noise, w, warp, n, r = job
    X, y = dataset_features(noise, w, warp, n, r)
    out = {}
    per = 1 + len(DEFINITIONS)
    for a, win in enumerate(WINDOWS):
        base = a * per
        out[(win, "sq")] = cv_accuracy(X[:, base], y)
        for j, d in enumerate(DEFINITIONS):
            out[(win, def_name(d))] = cv_accuracy(X[:, base + 1 + j], y)
    return job, out


def run_variants(c: dict, smoke: bool) -> dict:
    v = c["variants"]
    reps = range(2) if smoke else range(20)
    grid = [(nz, w, wp, n) for nz in v["noise"] for w in v["jitter_w"] for wp in v["warp"] for n in v["grids_N"]]
    if smoke:
        grid = [(0.0, 1.0, 0.0, 128), (0.3, 1.5, 0.25, 128)]
    jobs = [(*g, r) for g in grid for r in reps]
    res, t0 = {}, time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(variant_job, j) for j in jobs]
        for done, fu in enumerate(as_completed(futs), 1):
            job, out = fu.result()
            res[job] = out
            if done % max(1, len(jobs) // 40) == 0 or done == len(jobs):
                el = time.time() - t0
                print(f"[variants] {done}/{len(jobs)}, {el:.0f} s, about {el / done * (len(jobs) - done):.0f} s left",
                      flush=True)
    rep = c["reported"]
    rows = []
    for (nz, w, wp, n) in grid:
        for win in WINDOWS:
            sq = np.array([res[(nz, w, wp, n, r)][(win, "sq")] for r in reps])
            for d in DEFINITIONS:
                ce = np.array([res[(nz, w, wp, n, r)][(win, def_name(d))] for r in reps])
                row = {"noise": nz, "jitter_w": w, "warp": wp, "N": n, "window": win, "definition": d,
                       "sq_only_by_replicate": sq.tolist(), "centroid_only_by_replicate": ce.tolist()}
                for col, a, p in (("sq_only", sq, rep["sq_only"]), ("centroid_only", ce, rep["centroid_only"])):
                    dl = a - p
                    lo, hi = np.percentile(dl, [2.5, 97.5])
                    row[col] = {"mean": float(a.mean()), "delta": float(dl.mean()), "ci95": [float(lo), float(hi)],
                                "contains_0": bool(lo <= 0 <= hi)}
                row["direction_as_reported"] = bool(sq.mean() > ce.mean())
                rows.append(row)
    return {"rows": rows, "binomial_halfwidth_n120": {
        k: float(1.96 * np.sqrt(rep[k] * (1 - rep[k]) / 120)) for k in ("sq_only", "centroid_only")}}


# --- warp check (K5) ------------------------------------------------------------------------------------------------


def warp_descriptors(cond: str, w, g: int, seed: int, warp: float) -> list[float]:
    p = k5.surface_params(cond, g, seed, w)
    F = procedural_field(p["f"], RenderConfig(n=128, warp=warp), seed)
    H = p["s"] * t_gamma(F, p["gamma"])
    X = H - H.mean()
    cent = k5.spectral_centroids(X, k5.K_BAND)
    return [rq(X), cent["centroid_amp"], cent["centroid_band_power"]]


def warp_job(job: tuple) -> tuple:
    cond, w, warp, npairs = job
    bases = k5.SEEDS["experiment"]
    D = np.array([[warp_descriptors(cond, w, g, k5.pair_seeds(cond, i, bases)[g], warp) for g in (0, 1)]
                  for i in range(npairs)])                       # (pair, group, desc)
    y, folds = k5.labels(npairs), k5.make_folds(npairs)
    out = {}
    for ds in (("sq",), ("centroid_amp",), ("centroid_band_power",), ("sq", "centroid_amp")):
        cols = [k5.DESC.index(d) for d in ds]
        X = D[:, :, cols].reshape(-1, len(cols))
        for clf in (("svm", "threshold") if len(ds) == 1 else ("svm",)):
            out[(k5.set_name(ds), clf)] = float(k5.cv_correct(X, y, folds, clf).mean())
    return job, out


def run_warp(smoke: bool) -> dict:
    kc = json.loads(k5.COND.read_text())
    npairs = 20 if smoke else json.loads(K5_JSON.read_text())["meta"]["per_class_n"]
    combos = k5.combos(kc)
    if smoke:
        combos = combos[:2]
    jobs = [(cond, w, wp, npairs) for cond, w in combos for wp in (0.0, 0.25)]
    res = {}
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        for fu in as_completed([ex.submit(warp_job, j) for j in jobs]):
            job, out = fu.result()
            res[job] = out
    stored = json.loads(K5_JSON.read_text())["rows"]
    rows, mismatch = [], 0
    for cond, w in combos:
        for (sname, clf) in res[(cond, w, 0.0, npairs)]:
            ds = {"S": "sq", "C": "centroid_amp", "B": "centroid_band_power", "SC": "sq+centroid_amp"}[sname]
            key = f"{k5.ckey(cond, w)}|128|raw|H|{ds}"
            a0, a25 = res[(cond, w, 0.0, npairs)][(sname, clf)], res[(cond, w, 0.25, npairs)][(sname, clf)]
            k5acc = None if smoke else stored[key][clf]["acc"]
            k5ci = None if smoke else stored[key][clf]["ci95"]
            same = None if smoke else (a0 == k5acc)
            mismatch += 0 if (smoke or same) else 1
            rows.append({"condition": cond, "w": w, "set": sname, "classifier": clf, "warp0": a0, "warp025": a25,
                         "difference": a25 - a0, "k5_stored": k5acc, "k5_ci95": k5ci,
                         "warp0_equals_k5": same})
    return {"pairs": npairs, "rows": rows, "implementation_mismatches": mismatch}


# --- report ---------------------------------------------------------------------------------------------------------


def write_md(res: dict) -> str:
    m, rep = res["meta"], res["reported"]
    V = res["variants"]
    L = ["# The reported accuracies against the reconstruction, by variant (supplement)", "",
         f"Conditions: `experiments/conditions/variants.json` (SHA-256 `{m['conditions_sha256']}`). Specification "
         f"SHA-256 `{m['spec_sha256']}`. Script SHA-256 `{m['script_sha256']}`. Commit {m['git_commit'][:7]} (dirty: "
         f"{m['git_dirty']}). numpy {m['numpy']}, scipy {m['scipy']}, scikit-learn {m['sklearn']}, Python "
         f"{m['python']}. Run started {m['started']} and finished {m['finished']} ({m['platform']})."
         + (" SMOKE RUN: not for any decision." if m["smoke"] else ""), "",
         "All values come from the reconstructed generator, not from the original code. The list of variants was "
         "fixed after exploratory computations over overlapping grids had been seen (stated in the conditions). "
         "Nothing here is evidence for the claims of the main text.", "",
         "## Reading of the conditions fixed before the run", ""]
    L += [f"- {x}" for x in res["interpretation"]]
    rows = V["rows"]
    bw = V["binomial_halfwidth_n120"]
    L += ["", "## Summary", "",
          f"Reported: Sq only {rep['sq_only']}, centroid only {rep['centroid_only']}. Binomial half-width for n = 120 "
          f"(reference only): {bw['sq_only']:.3f} and {bw['centroid_only']:.3f}.", "",
          f"- Variants: {len(rows)}.",
          f"- Interval of Delta contains 0, Sq only: {_sq_combos(rows)} of 72 combinations of (noise, w, warp, N, "
          f"window) ({sum(r['sq_only']['contains_0'] for r in rows)} of {len(rows)} rows; Sq only does not depend on "
          f"the centroid definition).",
          f"- Interval of Delta contains 0, centroid only: {sum(r['centroid_only']['contains_0'] for r in rows)}.",
          f"- Both at once: {sum(r['sq_only']['contains_0'] and r['centroid_only']['contains_0'] for r in rows)}.",
          f"- Direction as reported (Sq only above centroid only): "
          f"{sum(r['direction_as_reported'] for r in rows)}.",
          f"- Both intervals contain 0 and the direction is as reported: "
          f"{sum(r['sq_only']['contains_0'] and r['centroid_only']['contains_0'] and r['direction_as_reported'] for r in rows)}.",
          "", "Range of the mean accuracy over all variants:", ""]
    for col in ("sq_only", "centroid_only"):
        a = [r[col]["mean"] for r in rows]
        L.append(f"- {col}: {min(a):.4f} to {max(a):.4f}")
    L += ["", "By factor (variants whose interval contains 0, out of the variants with that level; Sq only also as "
          "combinations of (noise, w, warp, N, window)):", "",
          "| factor | level | variants | Sq only (rows; combinations) | centroid only | both |", "|---|---|---|---|---|---|"]
    for fac in ("noise", "jitter_w", "warp", "N", "window"):
        for lev in sorted({r[fac] for r in rows}, key=str):
            sub = [r for r in rows if r[fac] == lev]
            L.append(f"| {fac} | {lev} | {len(sub)} | {sum(r['sq_only']['contains_0'] for r in sub)}; "
                     f"{_sq_combos(sub)} of {len(sub) // 32} | "
                     f"{sum(r['centroid_only']['contains_0'] for r in sub)} | "
                     f"{sum(r['sq_only']['contains_0'] and r['centroid_only']['contains_0'] for r in sub)} |")
    both = [r for r in rows if r["sq_only"]["contains_0"] and r["centroid_only"]["contains_0"]]
    L += ["", "## Variants whose intervals contain 0 in both columns", ""]
    L += _table(both) if both else ["None."]
    sq_combos = {_combo(r): r for r in rows if r["sq_only"]["contains_0"]}
    L += ["", "## Sq only: combinations whose interval contains 0", ""]
    if sq_combos:
        L += ["| noise | w | warp | N | window | Sq only (Delta [95%]) |", "|---|---|---|---|---|---|"]
        for r in sq_combos.values():
            s = r["sq_only"]
            L.append(f"| {r['noise']} | {r['jitter_w']} | {r['warp']} | {r['N']} | {r['window']} | {s['mean']:.4f} "
                     f"({s['delta']:+.4f} [{s['ci95'][0]:+.4f}, {s['ci95'][1]:+.4f}]) |")
    else:
        L.append("None.")
    ce = [r for r in rows if r["centroid_only"]["contains_0"]]
    L += ["", "## Centroid only: variants whose interval contains 0", ""]
    L += _table(ce) if ce else ["None."]
    L += ["", "## Sq only: variants closest to the reported value (20 smallest |Delta|)", ""]
    L += _table(sorted(rows, key=lambda r: abs(r["sq_only"]["delta"]))[:20])
    L += ["", "## Centroid only: variants closest to the reported value (20 smallest |Delta|)", ""]
    L += _table(sorted(rows, key=lambda r: abs(r["centroid_only"]["delta"]))[:20])
    W = res["warp_check"]
    L += ["", "## Warp check (K5, N = 128, raw, H)", "",
          f"Pairs per condition: {W['pairs']}. Implementation control (warp 0 here against the stored K5 accuracies): "
          f"{W['implementation_mismatches']} mismatches. The difference mixes the warp with a redraw of the surfaces "
          f"(Reading of the conditions); the K5 interval is a reference for sampling variation, not an interval of the "
          f"difference.", "",
          "| condition | w | set | classifier | warp 0 | warp 0.25 | difference | K5 stored [95% pair bootstrap] |",
          "|---|---|---|---|---|---|---|---|"]
    for r in W["rows"]:
        k = "-" if r["k5_stored"] is None else (f"{r['k5_stored']:.4f} [{r['k5_ci95'][0]:.4f}, "
                                                f"{r['k5_ci95'][1]:.4f}]")
        L.append(f"| {r['condition']} | {r['w']} | {r['set']} | {r['classifier']} | {r['warp0']:.4f} | "
                 f"{r['warp025']:.4f} | {r['difference']:+.4f} | {k} |")
    d = [abs(r["difference"]) for r in W["rows"]]
    L += ["", f"Largest absolute difference between warp 0.25 and warp 0: {max(d):.4f}.", ""]
    L += ["## Full list of variants", ""] + _table(rows)
    return "\n".join(L) + "\n"


def _combo(r: dict) -> tuple:
    return (r["noise"], r["jitter_w"], r["warp"], r["N"], r["window"])


def _sq_combos(rows) -> int:
    return len({_combo(r) for r in rows if r["sq_only"]["contains_0"]})


def _table(rows) -> list[str]:
    L = ["| noise | w | warp | N | window | definition | Sq only (Delta [95%]; binomial +-0.050) | 0 in | "
         "centroid only (Delta [95%]; binomial +-0.078) | 0 in | direction |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        s, c = r["sq_only"], r["centroid_only"]
        L.append(f"| {r['noise']} | {r['jitter_w']} | {r['warp']} | {r['N']} | {r['window']} | "
                 f"{def_name(r['definition'])} | {s['mean']:.4f} ({s['delta']:+.4f} [{s['ci95'][0]:+.4f}, "
                 f"{s['ci95'][1]:+.4f}]) | {'yes' if s['contains_0'] else 'no'} | {c['mean']:.4f} ({c['delta']:+.4f} "
                 f"[{c['ci95'][0]:+.4f}, {c['ci95'][1]:+.4f}]) | {'yes' if c['contains_0'] else 'no'} | "
                 f"{'yes' if r['direction_as_reported'] else 'no'} |")
    return L


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--smoke", type=Path)
    a = ap.parse_args()
    if a.report:
        res = json.loads(OUT_JSON.read_text())
        now = identity()
        for k in now:
            if res["meta"][k] != now[k]:
                raise SystemExit(f"{k} changed since the values were computed")
        OUT_MD.write_text(write_md(res))
        return
    c = load_conditions()
    if a.smoke:
        a.smoke.mkdir(parents=True, exist_ok=True)
        out_json, out_md = a.smoke / OUT_JSON.name, a.smoke / OUT_MD.name
    else:
        out_json, out_md = OUT_JSON, OUT_MD
        if out_json.exists() or out_md.exists():
            raise SystemExit("results exist; remove them to recompute")
        if git_state()["git_dirty"]:
            raise SystemExit("the conditions, the script or the library differ from the last commit; commit first")
    ident = identity()
    meta = {**ident, **git_state(strict=a.smoke is None), "smoke": bool(a.smoke), "numpy": np.__version__, "scipy": scipy.__version__,
            "sklearn": sklearn.__version__, "python": platform.python_version(),
            "platform": f"{platform.system()} {platform.machine()}",
            "started": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    warp = run_warp(a.smoke is not None)
    print(f"[warp] done, {warp['implementation_mismatches']} mismatches", flush=True)
    variants = run_variants(c, a.smoke is not None)
    partial = (a.smoke / OUT_PARTIAL.name) if a.smoke else OUT_PARTIAL
    partial.parent.mkdir(parents=True, exist_ok=True)
    tmp = partial.with_suffix(".tmp")
    tmp.write_text(json.dumps({"meta": meta, "variants": variants, "warp_check": warp}, indent=1) + "\n")
    os.replace(tmp, partial)
    meta["finished"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if identity() != ident:
        raise SystemExit("an input file changed during the run")
    if git_state(strict=False)["git_commit"] != meta["git_commit"]:
        raise SystemExit("HEAD changed during the run")
    if not a.smoke and warp["implementation_mismatches"]:
        raise SystemExit(f"implementation control failed: {warp['implementation_mismatches']} mismatches; "
                         f"results not written (variants kept in {partial})")
    res = {"meta": meta, "reported": c["reported"], "interpretation": INTERPRETATION, "variants": variants,
           "warp_check": warp}
    md = write_md(res)
    with open(out_json, "x") as fh:  # refuse to overwrite a result written by another run in the meantime
        fh.write(json.dumps(res, indent=1) + "\n")
    with open(out_md, "x") as fh:
        fh.write(md)
    print(f"wrote {out_json} and {out_md}")


if __name__ == "__main__":
    main()
