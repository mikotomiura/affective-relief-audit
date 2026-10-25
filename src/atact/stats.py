"""Statistics shared by the condition files (spec S6): growth exponents with intervals over seeds, local slopes,
the log-corrected fit, order flips between two grid levels, and Kendall's tau between rankings."""

from __future__ import annotations

from itertools import combinations

import numpy as np
from scipy import stats as _st


def slopes_per_seed(N, C) -> np.ndarray:
    """S6.1: for each seed (row of C), the least-squares slope of ln C on ln N. C has shape (seeds, len(N))."""
    x = np.log(np.asarray(N, dtype=float))
    y = np.log(np.asarray(C, dtype=float))
    xc = x - x.mean()
    return (y - y.mean(axis=1, keepdims=True)) @ xc / (xc @ xc)


def t_interval(values, level: float = 0.95) -> dict:
    """Mean and two-sided t interval over seeds (n - 1 degrees of freedom) at the given level (S6.1)."""
    v = np.asarray(values, dtype=float)
    n = len(v)
    m = float(v.mean())
    se = float(v.std(ddof=1) / np.sqrt(n))
    q = float(_st.t.ppf(1 - (1 - level) / 2, n - 1))
    return {"mean": m, "se": se, "lo": m - q * se, "hi": m + q * se, "level": level, "df": n - 1}


def bonferroni_level(m: int, alpha: float = 0.05) -> float:
    """S6.1: simultaneous level 1 - alpha/m for m cells."""
    return 1 - alpha / m


def local_slopes(N, C) -> np.ndarray:
    """Slope of ln C on ln N between consecutive N, per seed. Shape (seeds, len(N) - 1)."""
    x = np.log(np.asarray(N, dtype=float))
    y = np.log(np.asarray(C, dtype=float))
    return np.diff(y, axis=1) / np.diff(x)


def log_corrected_fit(N, C) -> np.ndarray:
    """Per seed, least squares of ln C = a + b ln N + c ln ln N. Returns an array of shape (seeds, 3) with (a, b, c)."""
    lnN = np.log(np.asarray(N, dtype=float))
    X = np.column_stack([np.ones_like(lnN), lnN, np.log(lnN)])
    coef, *_ = np.linalg.lstsq(X, np.log(np.asarray(C, dtype=float)).T, rcond=None)
    return coef.T


def flips_seeded(Xg, Xh, labels=None) -> list[dict]:
    """S6.2 with seeds. Xg and Xh have shape (surfaces, seeds): the descriptor at levels g and h, with the same
    seeds in the same columns. For each pair of surfaces (a, b), the order at a level is the sign of the mean over
    seeds of sign(D_a - D_b). A flip is a pair whose order differs between the two levels and whose mean difference
    exceeds twice its standard error (over seeds, paired by seed) at both levels.
    """
    Xg, Xh = np.asarray(Xg, dtype=float), np.asarray(Xh, dtype=float)
    n = Xg.shape[1]
    labels = list(range(Xg.shape[0])) if labels is None else labels
    out = []
    for a, b in combinations(range(Xg.shape[0]), 2):
        dg, dh = Xg[a] - Xg[b], Xh[a] - Xh[b]
        og, oh = np.sign(np.sign(dg).mean()), np.sign(np.sign(dh).mean())
        mg, mh = dg.mean(), dh.mean()
        sg = dg.std(ddof=1) / np.sqrt(n) if n > 1 else 0.0
        sh = dh.std(ddof=1) / np.sqrt(n) if n > 1 else 0.0
        if og * oh < 0 and abs(mg) > 2 * sg and abs(mh) > 2 * sh:
            out.append({"a": labels[a], "b": labels[b], "mean_g": float(mg), "se_g": float(sg),
                        "mean_h": float(mh), "se_h": float(sh)})
    return out


def flips_relative(xg, xh, threshold: float, labels=None, pairs=None) -> list[dict]:
    """S6.2 for measured data without seeds. xg and xh are the descriptor values (positive) of each surface at
    levels g and h. A flip is a pair whose sign of D_a - D_b differs between the levels and whose relative difference
    |D_a - D_b| / ((D_a + D_b) / 2) exceeds the threshold at both levels. `pairs` restricts the pairs considered.
    """
    xg, xh = np.asarray(xg, dtype=float), np.asarray(xh, dtype=float)
    labels = list(range(len(xg))) if labels is None else labels
    pairs = combinations(range(len(xg)), 2) if pairs is None else pairs
    rel = lambda u, v: abs(u - v) / ((u + v) / 2)
    out = []
    for a, b in pairs:
        if (np.sign(xg[a] - xg[b]) * np.sign(xh[a] - xh[b]) < 0
                and rel(xg[a], xg[b]) > threshold and rel(xh[a], xh[b]) > threshold):
            out.append({"a": labels[a], "b": labels[b], "g": [float(xg[a]), float(xg[b])],
                        "h": [float(xh[a]), float(xh[b])]})
    return out


def kendall_tau(u, v) -> float:
    """Kendall's tau (tau-b, scipy) between the orderings given by two vectors of values."""
    return float(_st.kendalltau(u, v).statistic)
