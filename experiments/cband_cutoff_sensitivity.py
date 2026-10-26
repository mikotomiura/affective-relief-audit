"""Sensitivity of the K5 accuracies of C_band to the band limit K (supplement only).

Usage:  uv run python experiments/cband_cutoff_sensitivity.py
Conditions: experiments/conditions/cband_cutoff_sensitivity.json (version 1, committed before this script was run)
Base: experiments/k5_classification.py and its conditions (version 1); the surfaces, folds, classifiers and bootstrap
are those of the K5 experiment, imported from that script.

The power spectrum of each surface is computed once per grid and processing, and C_band is evaluated from it for every
K. At K = 32 the accuracies must equal the stored K5 accuracies (the control); otherwise nothing is written.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import k5_classification as k5  # noqa: E402
from atact.descriptors import _radial_frequency_cached  # noqa: E402
from atact.field import procedural_field_separable  # noqa: E402
from atact.spectral import windowed  # noqa: E402
from atact.transform import t_gamma  # noqa: E402

COND = ROOT / "experiments" / "conditions" / "cband_cutoff_sensitivity.json"
STORED = ROOT / "results" / "k5_classification.json"
OUT = ROOT / "results"
NAME = "cband_cutoff_sensitivity"
N_PAIRS = 480
TOL = 1e-12


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def head_commit() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def band_centroids(X: np.ndarray, Ks: list[float]) -> list[float]:
    """C_band of X (already mean-removed or windowed) for each K, from one DFT; as in descriptors.spectral_centroids."""
    n = X.shape[0]
    pw = np.abs(np.fft.fft2(X - X.mean())) ** 2
    rho = _radial_frequency_cached(n)
    out = []
    for K in Ks:
        keep = (rho <= K) & (rho > 0)
        out.append(float((rho[keep] * pw[keep]).sum() / pw[keep].sum()))
    return out


def surface_job(job: tuple) -> tuple:
    """job = (cond, w, g, seed, Ns, Ks) -> array (N, processing, K)."""
    cond, w, g, seed, Ns, Ks = job
    p = k5.surface_params(cond, g, seed, w)
    arr = np.empty((len(Ns), len(k5.PROCS), len(Ks)))
    for a, n in enumerate(Ns):
        H = p["s"] * t_gamma(procedural_field_separable(p["f"], n, seed), p["gamma"])
        for b, proc in enumerate(k5.PROCS):
            X = H - H.mean() if proc == "raw" else windowed(H)
            arr[a, b] = band_centroids(X, Ks)
    return cond, w, g, seed, arr


def classify(x: np.ndarray) -> dict:
    """Accuracy of the svm and the threshold on one descriptor; samples ordered pair by pair."""
    X = x.reshape(-1, 1)
    y, folds, B = k5.labels(N_PAIRS), k5.make_folds(N_PAIRS), k5.boot_indices(N_PAIRS, k5.N_BOOT)
    out = {}
    for clf in ("svm", "threshold"):
        r = k5.interval_summary(k5.cv_correct(X, y, folds, clf), B)
        out[clf] = {"acc": r["acc"], "ci95": r["ci95"]}
    return out


def main() -> None:
    c = json.loads(COND.read_text())
    start = head_commit()
    Ks, Ns, conds, ws = c["band_limits_K"], c["grids_N"], c["conditions"], c["jitter_w"]
    if 32 not in Ks:
        raise SystemExit("K = 32 is needed for the control")
    bases = k5.SEEDS["experiment"]
    jobs = [(cond, w, g, k5.pair_seeds(cond, i, bases)[g], Ns, Ks)
            for cond in conds for w in ws for i in range(N_PAIRS) for g in (0, 1)]
    vals = {}
    with ProcessPoolExecutor(max_workers=k5.WORKERS) as ex:
        for cond, w, g, seed, arr in ex.map(surface_job, jobs, chunksize=40):
            vals[(cond, w, g, seed)] = arr
    stored = json.loads(STORED.read_text())["rows"]
    rows, mismatches = [], []
    for cond in conds:
        for w in ws:
            seeds = [k5.pair_seeds(cond, i, bases) for i in range(N_PAIRS)]
            A = np.stack([np.stack([vals[(cond, w, 0, s0)], vals[(cond, w, 1, s1)]]) for s0, s1 in seeds])
            for a, n in enumerate(Ns):
                for b, proc in enumerate(k5.PROCS):
                    for k, K in enumerate(Ks):
                        r = classify(A[:, :, a, b, k].reshape(-1))
                        row = {"condition": cond, "w": w, "N": n, "processing": proc, "K": K, **r}
                        rows.append(row)
                        if K == 32:
                            ref = stored[f"{cond}_w{w}|{n}|{proc}|H|centroid_band_power"]
                            for clf in ("svm", "threshold"):
                                if abs(ref[clf]["acc"] - r[clf]["acc"]) > TOL:
                                    mismatches.append((cond, w, n, proc, clf, ref[clf]["acc"], r[clf]["acc"]))
    if mismatches:
        raise SystemExit(f"control failed in {len(mismatches)} rows, nothing written: {mismatches[:5]}")
    if head_commit() != start:
        raise SystemExit("HEAD changed during the run; nothing written")
    meta = {"name": NAME, "conditions": str(COND.relative_to(ROOT)), "conditions_sha256": sha256(COND),
            "script_sha256": sha256(Path(__file__)), "k5_script_sha256": sha256(ROOT / "experiments" / "k5_classification.py"),
            "stored_k5_sha256": sha256(STORED), "uv_lock_sha256": sha256(ROOT / "uv.lock"), "commit": start,
            "finished": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "control": f"K = 32 equals the stored K5 accuracies in all {len(rows) // len(Ks) * 2} classifier rows"}
    out_json, out_md = OUT / f"{NAME}.json", OUT / f"{NAME}.md"
    for p in (out_json, out_md):
        if p.exists():
            raise SystemExit(f"{p} exists; not overwritten")
    out_json.write_text(json.dumps({"meta": meta, "rows": rows}, indent=1))
    lines = [f"# C_band and the band limit K (supplement only)", "",
             f"Conditions {meta['conditions']} (version {c['version']}, SHA-256 {meta['conditions_sha256']}); commit {start}.",
             "Generated by experiments/cband_cutoff_sensitivity.py; not edited by hand.", "", meta["control"] + ".", "",
             "| condition | w | N | proc | clf | " + " | ".join(f"K={K}" for K in Ks) + " | max abs diff from K=32 |",
             "|---|---|---|---|---|" + "---|" * (len(Ks) + 1)]
    for cond in conds:
        for w in ws:
            for n in Ns:
                for proc in k5.PROCS:
                    sel = {r["K"]: r for r in rows if (r["condition"], r["w"], r["N"], r["processing"]) == (cond, w, n, proc)}
                    for clf in ("svm", "threshold"):
                        accs = [sel[K][clf]["acc"] for K in Ks]
                        cells = [f"{sel[K][clf]['acc']:.3f} [{sel[K][clf]['ci95'][0]:.3f}, {sel[K][clf]['ci95'][1]:.3f}]" for K in Ks]
                        d = max(abs(a - sel[32][clf]["acc"]) for a in accs)
                        lines.append(f"| {cond} | {w} | {n} | {proc} | {clf} | " + " | ".join(cells) + f" | {d:.3f} |")
    lines += ["", "## i_A: accuracy at least 0.99 for every K", ""]
    for n in Ns:
        for proc in k5.PROCS:
            for w in ws:
                for clf in ("svm", "threshold"):
                    ok = all(r[clf]["acc"] >= 0.99 for r in rows
                             if (r["condition"], r["w"], r["N"], r["processing"]) == ("i_A", w, n, proc))
                    lines.append(f"- N = {n}, {proc}, w = {w}, {clf}: {'yes' if ok else 'no'}")
    out_md.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
