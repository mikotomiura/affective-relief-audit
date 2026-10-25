"""Checks the decision rule of experiments/k4_centroid_2d.py (rejection_criterion of k4_centroid_2d.json, read as
fixed before the run: decide on each range, agree -> that decision, differ -> not decidable) on synthetic values."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location(
    "k4_centroid_2d", Path(__file__).resolve().parents[1] / "experiments" / "k4_centroid_2d.py")
k4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k4)

N = [128, 256, 512, 1024, 2048, 4096]
SEEDS = list(range(1, 21))
GAMMAS = [0.9, 1.25, 1.75, 2.6]


def rows_with(exponent):
    """Centroid C = N^exponent(f, gamma, N) times seed noise, for the 12 cells of the criterion."""
    rng = np.random.default_rng(0)
    rows = []
    for f in (3, 5, 7):
        for g in GAMMAS:
            for s in SEEDS:
                eps = 0.01 * rng.normal()
                for n in N:
                    c = n ** (exponent(f, g, n) + eps)
                    rows.append({"field": "sum", "f": f, "gamma": g, "N": n, "seed": s, "sampling": "direct", "r": 1,
                                 "normalize": "maxabs", "values": {"raw": {"centroid_amp": c}}})
    return rows


C = {"seeds": SEEDS}
NP, NS = [512, 1024, 2048, 4096], [1024, 2048, 4096]


def test_consistent_when_exponent_equals_estimate():
    r = k4.rejection(C, rows_with(lambda f, g, n: k4.e_gamma(g)), NP, NS)
    assert (r["decision_primary"], r["decision_sensitivity"], r["outcome"]) == ("consistent", "consistent", "consistent")
    assert r["level"] == pytest.approx(1 - 0.05 / 12)


def test_rejected_when_one_cell_differs_on_both_ranges():
    r = k4.rejection(C, rows_with(lambda f, g, n: k4.e_gamma(g) + (0.2 if (f, g) == (5, 1.25) else 0.0)), NP, NS)
    assert r["outcome"] == "rejected"
    bad = [x for x in r["cells"] if not x["contains"]]
    assert {(x["f"], x["gamma"], x["direction"]) for x in bad} == {(5, 1.25, "above")}


def test_not_decidable_when_only_primary_range_rejects():
    # Slope differs from the estimate only between 512 and 1024: the primary range rejects, the sensitivity range does not
    def expo(f, g, n):
        return k4.e_gamma(g) - (0.3 if (f, g) == (3, 0.9) and n <= 512 else 0.0)
    r = k4.rejection(C, rows_with(expo), NP, NS)
    assert r["decision_primary"] == "rejected" and r["decision_sensitivity"] == "consistent"
    assert r["outcome"] == "not decidable in this N range"


def test_estimate_values_in_the_conditions():
    assert [round(k4.e_gamma(g), 4) for g in GAMMAS] == [0.3889, 0.7, 0.9286, 1.0]
