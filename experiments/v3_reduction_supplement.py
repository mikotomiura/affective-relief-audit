"""Supplementary exploration of validation 3 (not a registered computation): the reduction method and the change of
hf_ratio_phys with coarsening on the Surface-Topography Challenge measurements.

Usage:  uv run python experiments/v3_reduction_supplement.py            (compute, then write the results)
        uv run python experiments/v3_reduction_supplement.py --report   (rewrite the results from the saved values)
Conditions: experiments/conditions/v3_reduction_supplement.json (exploratory; designed after the results of
            validation 3 had been seen; not blind; not used as evidence for the main claims)
Specification: experiments/spec/generator-and-descriptors.md
Data: as validation 3 (external/topo-challenge-20261025/, CC0; not redistributed). The SHA-256 of every input file is
      checked against experiments/conditions/validation3_public.json before any value is read.
Output: results/v3_reduction_supplement.json and results/v3_reduction_supplement.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from atact.descriptors import spectral_centroids  # noqa: E402
from atact.hfratio import hf_ratio, hf_ratio_float, normal_from_height, normal_rgb_from_height  # noqa: E402
from atact.measured import central_crop, largest_pow2, read_challenge  # noqa: E402
from atact.spectral import decimate_fourier, remove_plane, subsample  # noqa: E402
from validation3_public import LEVELS, check_inputs, flip_summary, mono, sha  # noqa: E402

COND = ROOT / "experiments" / "conditions" / "v3_reduction_supplement.json"
COND_V3 = ROOT / "experiments" / "conditions" / "validation3_public.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
OUT = ROOT / "results"
NAME = "v3_reduction_supplement"
REDUCTIONS = ("decimate_fourier", "mirror", "subsample")
DESCRIPTORS = ("hf_ratio_px", "hf_ratio_phys", "hf_ratio_phys_float", "centroid_amp", "centroid_band_power")
SMALL = 1e-3

INTERPRETATION = [
    "Exploratory: designed after the results of validation 3 had been seen; not blind; no predictions; for the "
    "supplement only.",
    "mirror: even extension of the P x P crop to 2P x 2P, ideal low-pass keeping the bins whose components lie in "
    "[-n, n) of that frame (the same physical band as [-n/2, n/2) on the P x P frame), sampled at every (P/n)-th pixel "
    "of the first quadrant. The full level is the crop itself for every reduction.",
    "Decomposition of the change of hf_ratio_phys_float from full to level n: content = s1 - s0 (heights band-limited "
    "to level n, normals on the grid P), sampling = s2 - s1 (the normals of s1 taken at every (P/n)-th pixel), "
    "differences = s3 - s2 (normals computed from the reduced heights on the grid n). For the subsample reduction "
    "there is no band-limit, so it is not decomposed.",
]


def bandlimit_periodic(Z: np.ndarray, n: int) -> np.ndarray:
    """The heights of decimate_fourier(Z, n) on the fine grid: bins outside [-n/2, n/2) per component removed."""
    M = Z.shape[0]
    keep = np.zeros(M, bool)
    keep[np.r_[0 : n // 2, M - n // 2 : M]] = True
    return np.real(np.fft.ifft2(np.fft.fft2(Z) * np.outer(keep, keep)))


def bandlimit_mirror(Z: np.ndarray, n: int) -> np.ndarray:
    """Even extension to 2P x 2P, keep the bins in [-n, n) per component, return the first P x P quadrant."""
    P = Z.shape[0]
    E = np.block([[Z, Z[:, ::-1]], [Z[::-1, :], Z[::-1, ::-1]]])
    keep = np.zeros(2 * P, bool)
    keep[np.r_[0:n, 2 * P - n : 2 * P]] = True
    return np.real(np.fft.ifft2(np.fft.fft2(E) * np.outer(keep, keep)))[:P, :P]


def reduce(Z: np.ndarray, n: int, method: str) -> np.ndarray:
    P = Z.shape[0]
    if n == P:
        return Z
    if method == "decimate_fourier":
        return decimate_fourier(Z, n)
    if method == "mirror":
        return np.ascontiguousarray(bandlimit_mirror(Z, n)[:: P // n, :: P // n])
    return subsample(Z, n)


def descriptors(Zn: np.ndarray, L: float, P: int) -> dict:
    n = Zn.shape[0]
    rgb = normal_rgb_from_height(Zn, L)
    cen = spectral_centroids(Zn, P / 8)
    return {"hf_ratio_px": hf_ratio(rgb, 120.0), "hf_ratio_phys": hf_ratio(rgb, 120.0 * n / P),
            "hf_ratio_phys_float": hf_ratio_float(normal_from_height(Zn, L), 120.0 * n / P),
            "centroid_amp": cen["centroid_amp"], "centroid_band_power": cen["centroid_band_power"]}


def decomposition(Z: np.ndarray, L: float, n: int, band) -> dict:
    """s0..s3 of the conditions for hf_ratio_phys_float and level n; `band` is bandlimit_periodic or bandlimit_mirror."""
    P = Z.shape[0]
    r = P // n
    Zb = band(Z, n)
    nb = normal_from_height(Zb, L)
    s0 = hf_ratio_float(normal_from_height(Z, L), 120.0)
    s1 = hf_ratio_float(nb, 120.0)
    s2 = hf_ratio_float(np.ascontiguousarray(nb[::r, ::r]), 120.0 * n / P)
    s3 = hf_ratio_float(normal_from_height(np.ascontiguousarray(Zb[::r, ::r]), L), 120.0 * n / P)
    return {"s": [s0, s1, s2, s3], "content": s1 - s0, "sampling": s2 - s1, "differences": s3 - s2, "total": s3 - s0}


def crop_stats(Z: np.ndarray, L: float) -> dict:
    P = Z.shape[0]
    k = np.fft.fftfreq(P, d=L / P) * 2 * np.pi
    F = np.fft.fft2(Z)
    gx = np.real(np.fft.ifft2(F * 1j * k[None, :]))
    gy = np.real(np.fft.ifft2(F * 1j * k[:, None]))
    jump = np.sqrt((np.mean((Z[0] - Z[-1]) ** 2) + np.mean((Z[:, 0] - Z[:, -1]) ** 2)) / 2) / Z.std()
    return {"rms_slope": float(np.sqrt((gx**2 + gy**2).mean())), "jump_rel": float(jump)}


def compute(cv3) -> list[dict]:
    mpaths, _ = check_inputs(cv3)
    rows = []
    for k, (m, p) in enumerate(zip(cv3["datasets"][0]["measurements"], mpaths)):
        z, dx, dy = read_challenge(p)
        P = largest_pow2(min(z.shape))
        if P != m["P"]:
            raise SystemExit(f"P differs from the conditions for {m['file']}")
        L = P * (dx + dy) / 2
        Z = remove_plane(central_crop(z, P))
        row = {"id": f"{m['container']}/{m['file']}", "container": m["container"], "surface": m["surface"], "P": P,
               **crop_stats(Z, L), "values": {}, "decomposition": {}}
        for method in REDUCTIONS:
            row["values"][method] = [descriptors(reduce(Z, n, method), L, P) for n in (P, P // 2, P // 4)]
        for name, band in (("decimate_fourier", bandlimit_periodic), ("mirror", bandlimit_mirror)):
            for lev, n in (("half", P // 2), ("quarter", P // 4)):
                row["decomposition"][f"{name}/{lev}"] = decomposition(Z, L, n, band)
                row["decomposition"][f"{name}/{lev}/small_slope"] = decomposition(Z * SMALL, L, n, band)
        rows.append(row)
        print(f"{k + 1}/{len(mpaths)} {row['id']}", flush=True)
    return rows


def analyse(rows) -> dict:
    ids = [r["id"] for r in rows]
    cont = [r["container"] for r in rows]
    surf = [r["surface"] for r in rows]
    mixed = lambda a, b: surf[a] != surf[b]  # noqa: E731
    S = {"by_reduction": {}, "decomposition": {}}
    for method in REDUCTIONS:
        for d in DESCRIPTORS:
            X = np.array([[r["values"][method][j][d] for j in range(3)] for r in rows])
            inc, dec = mono(X, True), mono(X, False)
            S["by_reduction"][f"{method}/{d}"] = {
                "values": X.tolist(), "increasing": int(inc.sum()), "decreasing": int(dec.sum()),
                "non_monotone": int(len(ids) - inc.sum() - dec.sum()),
                "abs_quarter_minus_full": np.abs(X[:, 2] - X[:, 0]).tolist(),
                "V2": flip_summary(X, ids, cont), "V3": flip_summary(X, ids, cont, mixed)}
    keys = list(rows[0]["decomposition"])
    for key in keys:
        T = {t: np.array([r["decomposition"][key][t] for r in rows]) for t in ("total", "content", "sampling", "differences")}
        S["decomposition"][key] = {t: {"mean_abs": float(np.abs(v).mean()), "mean": float(v.mean()),
                                       "positive": int((v > 0.005).sum()), "negative": int((v < -0.005).sum())}
                                   for t, v in T.items()}
    return S


def g(x) -> str:
    return f"{x:.4g}"


def write_report(meta, S, rows) -> str:
    L = ["# Supplementary exploration of validation 3: reduction methods", "",
         f"Conditions: `experiments/conditions/v3_reduction_supplement.json` (SHA-256 `{meta['conditions_sha256']}`). "
         f"Data and their check: `experiments/conditions/validation3_public.json` (SHA-256 `{meta['conditions_v3_sha256']}`). "
         f"Specification SHA-256 `{meta['spec_sha256']}`. numpy {meta['numpy']}, scipy {meta['scipy']}, Python {meta['python']}. "
         f"Run started {meta['started']} and finished {meta['finished']} ({meta['platform']}).", "",
         "**Status: exploratory.** Designed after the results of validation 3 had been seen; not blind; no predictions. "
         "Its results are for the supplement and are not used as evidence for the claims of the main text.", "",
         "## Reading of the conditions", ""]
    L += [f"- {x}" for x in INTERPRETATION]
    L += ["", "## Direction of the change with coarsening (38 measurements)", "",
          "| reduction | descriptor | increasing | decreasing | non-monotone | mean abs(quarter - full) | V2 flips (main) | V3 flips (main) |",
          "|---|---|---|---|---|---|---|---|"]
    for method in REDUCTIONS:
        for d in DESCRIPTORS:
            x = S["by_reduction"][f"{method}/{d}"]
            L.append(f"| {method} | {d} | {x['increasing']} | {x['decreasing']} | {x['non_monotone']} | "
                     f"{g(float(np.mean(x['abs_quarter_minus_full'])))} | {x['V2']['flips_main']} | {x['V3']['flips_main']} |")
    L += ["", "## Decomposition of the change of hf_ratio_phys_float (means over the 38 measurements)", "",
          "Mean of the absolute value, mean, and numbers of measurements with the term above 0.005 or below -0.005.", "",
          "| band-limit / level | term | mean abs | mean | > 0.005 | < -0.005 |", "|---|---|---|---|---|---|"]
    for key, T in S["decomposition"].items():
        for t in ("total", "content", "sampling", "differences"):
            x = T[t]
            L.append(f"| {key} | {t} | {g(x['mean_abs'])} | {x['mean']:+.4f} | {x['positive']} | {x['negative']} |")
    L += ["", "## Values by measurement (hf_ratio_phys; full, half, quarter)", "",
          "| measurement | surface | RMS slope | boundary jump / RMS height | decimate_fourier | mirror | subsample |",
          "|---|---|---|---|---|---|---|"]
    for k, r in enumerate(rows):
        cells = [", ".join(g(v) for v in S["by_reduction"][f"{m}/hf_ratio_phys"]["values"][k]) for m in REDUCTIONS]
        L.append(f"| {r['id']} | {r['surface']} | {g(r['rms_slope'])} | {g(r['jump_rel'])} | " + " | ".join(cells) + " |")
    L += ["", "## Decomposition by measurement (quarter; content, sampling, differences)", "",
          "| measurement | decimate_fourier | mirror | mirror, heights x 1e-3 |", "|---|---|---|---|"]
    for r in rows:
        cells = []
        for key in ("decimate_fourier/quarter", "mirror/quarter", "mirror/quarter/small_slope"):
            x = r["decomposition"][key]
            cells.append(f"{x['content']:+.3f}, {x['sampling']:+.3f}, {x['differences']:+.3f}")
        L.append(f"| {r['id']} | " + " | ".join(cells) + " |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="rewrite the results from the saved values")
    args = ap.parse_args()
    js = OUT / f"{NAME}.json"
    if args.report:
        saved = json.loads(js.read_text())
        meta, rows = saved["meta"], saved["rows"]
    else:
        import scipy

        meta = {"conditions_sha256": sha(COND), "conditions_v3_sha256": sha(COND_V3), "spec_sha256": sha(SPEC),
                "numpy": np.__version__, "scipy": scipy.__version__, "python": sys.version.split()[0],
                "platform": f"{platform.system()} {platform.machine()}, {os.cpu_count()} logical CPUs",
                "started": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        rows = compute(json.loads(COND_V3.read_text()))
        meta["finished"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if (meta["conditions_sha256"], meta["conditions_v3_sha256"], meta["spec_sha256"]) != (sha(COND), sha(COND_V3), sha(SPEC)):
        raise SystemExit("conditions or specification changed since the values were computed")
    S = analyse(rows)
    OUT.mkdir(exist_ok=True)
    js.write_text(json.dumps({"meta": meta, "interpretation": INTERPRETATION, "summary": S, "rows": rows}))
    (OUT / f"{NAME}.md").write_text(write_report(meta, S, rows))
    print("done")


if __name__ == "__main__":
    main()
