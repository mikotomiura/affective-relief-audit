"""Checks of the parts of experiments/k5_classification.py (conditions version 1)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location(
    "k5_classification", Path(__file__).resolve().parents[1] / "experiments" / "k5_classification.py")
k5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k5)
COND = json.loads(k5.COND.read_text())


def test_conditions_parameters():
    for w in (0.1, 0.3, 0.5):
        for g in (0, 1):
            for sd in (1000, 1001, 1479):
                p = k5.surface_params("i_V", g, sd, w)
                assert p["f"] == 5.0 and p["A"] == 0.0 and (p["V"] < 0) == (g == 0)
                p = k5.surface_params("i_A", g, sd, w)
                assert p["V"] == 0.0 and p["s"] == pytest.approx(0.18) and (p["A"] < 0) == (g == 0)
                assert p["f"] != int(p["f"])
                p = k5.surface_params("ii_s", g, sd, w)
                q = k5.surface_params("corners", g, sd, w)
                assert p["s"] == 0.18 and (p["f"], p["gamma"], p["V"], p["A"]) == (q["f"], q["gamma"], q["V"], q["A"])
                r = k5.surface_params("ii_s_gamma", g, sd, w)
                assert r["gamma"] == 1.0 and r["s"] == 0.18 and r["f"] == q["f"]
    a, b = k5.surface_params("iii_null", 0, 1000, None), k5.surface_params("iii_null", 1, 50000, None)
    assert (a["f"], a["s"], a["gamma"]) == (b["f"], b["s"], b["gamma"]) == (3.0, pytest.approx(0.06), 0.9)


def test_corner_groups_and_clipping():
    p0 = [k5.surface_params("corners", 0, 1000 + i, 0.5) for i in range(200)]
    p1 = [k5.surface_params("corners", 1, 1000 + i, 0.5) for i in range(200)]
    assert all(p["V"] <= 1 and p["A"] >= -1 and p["V"] >= 0.5 for p in p0)
    assert all(p["V"] >= -1 and p["A"] <= 1 for p in p1)
    frac = np.mean([p["clipped"] for p in p0])
    assert 0.6 < frac < 0.9  # P(at least one of two coordinates clipped) = 3/4


def test_jitter_is_shared_across_w_and_conditions_but_not_groups():
    u0, u1 = k5.jitter_u(1007, 0), k5.jitter_u(1007, 1)
    assert not np.allclose(u0, u1)
    for w in (0.1, 0.3):
        assert k5.surface_params("i_V", 0, 1007, w)["V"] == pytest.approx(-0.5 + w * u0[0])
        assert k5.surface_params("i_A", 1, 1007, w)["A"] == pytest.approx(0.5 + w * u1[1])


def test_pair_seeds():
    b = k5.SEEDS["experiment"]
    assert k5.pair_seeds("iii_null", 7, b) == (1007, 50007)
    assert k5.pair_seeds("check_same_seed", 7, b) == (1007, 1007)
    assert k5.pair_seeds("corners", 7, b) == (1007, 1007)


def test_seed_ranges_do_not_overlap():
    n, ranges = 480, []
    e = k5.SEEDS["experiment"]
    ranges += [(e[0], e[0] + n), (e[1], e[1] + n)]
    for r in range(200):
        a0, a1 = k5.SEEDS["power_a"](r)
        ranges += [(a0, a0 + n), (a1, a1 + n)]
    for r in range(50):
        ranges.append((k5.SEEDS["power_b"](r)[0], k5.SEEDS["power_b"](r)[0] + n))
    for t in ("large_A", "large_B"):
        ranges += [(x, x + 5000) for x in k5.SEEDS[t]]
    ranges.append((900000, 920000))  # smoke
    ranges.sort()
    assert all(ranges[i][1] <= ranges[i + 1][0] for i in range(len(ranges) - 1))


def test_folds_keep_pairs_together_and_are_balanced():
    for n in (20, 60, 480):
        folds = k5.make_folds(n)
        assert len(folds) == 5
        te = np.concatenate([t for _, t in folds])
        assert sorted(te) == list(range(2 * n))
        for tr, t in folds:
            assert set(t // 2).isdisjoint(set(tr // 2))
            assert len(t) == 2 * n // 5


def test_threshold_fit():
    x = np.array([0.1, 0.2, 0.3, 1.1, 1.2, 1.3])
    y = np.array([0, 0, 0, 1, 1, 1])
    t, up = k5.fit_threshold(x, y)
    assert up and 0.3 < t < 1.1
    assert (k5.predict_threshold(x, t, up) == y).all()
    t, up = k5.fit_threshold(x, 1 - y)
    assert not up and (k5.predict_threshold(x, t, up) == 1 - y).all()
    rng = np.random.default_rng(5)
    for _ in range(50):
        x, y = rng.normal(size=30), rng.integers(0, 2, 30)
        t, up = k5.fit_threshold(x, y)
        best = max(max(((x > c) == y).mean(), ((x < c) == y).mean())
                   for c in np.concatenate([[-np.inf, np.inf], (np.sort(x)[1:] + np.sort(x)[:-1]) / 2]))
        assert (k5.predict_threshold(x, t, up) == y).mean() == pytest.approx(best)


def test_identical_pairs_give_exactly_one_half():
    rng = np.random.default_rng(3)
    n = 40
    f = rng.normal(size=(n, 2))
    X = np.repeat(f, 2, axis=0)  # both surfaces of a pair identical
    key, out = k5.classify_row(("x", X, 200, 19))
    assert out["svm"]["acc"] == 0.5
    key, out = k5.classify_row(("x", X[:, :1], 200, 19))
    assert out["svm"]["acc"] == 0.5 and out["threshold"]["acc"] == 0.5


def test_separable_rows_and_permutation_p():
    rng = np.random.default_rng(4)
    n = 40
    X = np.empty((2 * n, 1))
    X[0::2, 0] = rng.normal(0, 0.1, n)
    X[1::2, 0] = rng.normal(5, 0.1, n)
    key, out = k5.classify_row(("x", X, 200, 19))
    for clf in ("svm", "threshold"):
        assert out[clf]["acc"] == 1.0 and out[clf]["perm_p"] == pytest.approx(1 / 20)
        assert out[clf]["ci95"] == [1.0, 1.0] and not out[clf]["tost_chance"]


def test_tost_on_exact_half():
    n = 480
    correct = np.tile([True, False], n)
    s = k5.interval_summary(correct, k5.boot_indices(n, 2000))
    assert s["acc"] == 0.5 and s["ci90"] == [0.5, 0.5] and s["tost_chance"]
    # one wrong per pair half the time and both right otherwise: accuracy 0.75, not at chance
    correct = np.concatenate([[True, True] if i % 2 else [True, False] for i in range(n)])
    s = k5.interval_summary(correct, k5.boot_indices(n, 2000))
    assert s["acc"] == 0.75 and not s["tost_chance"]


def test_tost_uses_the_90_percent_interval():
    rng = np.random.default_rng(9)
    n = 480
    counts = rng.choice([0, 1, 2], size=n, p=[0.25, 0.5, 0.25])
    correct = np.concatenate([[c >= 1, c >= 2] for c in counts])
    B = k5.boot_indices(n, 2000)
    s = k5.interval_summary(correct, B)
    accb = correct.reshape(-1, 2).sum(1)[B].sum(1) / (2 * n)
    lo, hi = np.percentile(accb, [5, 95])
    assert s["ci90"] == [pytest.approx(lo), pytest.approx(hi)]
    assert s["tost_chance"] == bool(lo - 0.5 > -0.05 and hi - 0.5 < 0.05)


def test_descriptor_block_proposition_4():
    blk = k5.descriptor_block(5.5, 0.18, 1.7, 1234, 128)
    H, M = blk[0], blk[1]  # representation H and minmax
    np.testing.assert_allclose(M[:, 1:], H[:, 1:], rtol=1e-11)
    ratio = H[:, 0] / M[:, 0]
    assert ratio[0] == pytest.approx(ratio[1])  # sq scales by the same range under both processings
    blk2 = k5.descriptor_block(5.5, 0.30, 1.7, 1234, 128)
    np.testing.assert_allclose(blk2[1], M, rtol=1e-11)  # minmax removes s


def test_descriptor_block_matches_library():
    from atact.descriptors import centroid, rq
    from atact.field import RenderConfig, minmax, procedural_field
    from atact.spectral import centroid_band, windowed
    from atact.transform import t_gamma

    H = 0.24 * t_gamma(procedural_field(5.0, RenderConfig(n=128), seed=1001), 1.9)
    blk = k5.descriptor_block(5.0, 0.24, 1.9, 1001, 128)
    assert blk[0, 0, 0] == pytest.approx(rq(H), rel=1e-12)
    assert blk[0, 0, 1] == pytest.approx(centroid(H), rel=1e-12)
    assert blk[0, 0, 2] == pytest.approx(centroid_band(H, 32.0, "power"), rel=1e-12)
    W = windowed(minmax(H))
    assert blk[1, 1, 0] == pytest.approx(rq(W), rel=1e-12)
    assert blk[1, 1, 1] == pytest.approx(centroid(W), rel=1e-12)


def test_table_rows_and_row_predictions():
    rows = k5.table_rows(COND)
    assert len(rows) == (5 * 3 + 2) * 2 * 2 * 2 * 4
    assert len({k5.rkey(r) for r in rows}) == len(rows)
    for r in rows:
        d, o = k5.row_predictions(r)
        assert d and o
    r = {"condition": "check_same_seed", "w": None, "N": 128, "processing": "raw", "representation": "H",
         "descriptor_set": ["sq"]}
    assert k5.row_predictions(r) == (["exactly 0.5 (P-K5-3)"], ["none"])
    r = dict(r, condition="corners", w=0.3, representation="minmax")
    d, o = k5.row_predictions(r)
    assert "<= the same row on H (P-K5-1)" in d and "= the same row of ii_s (P-K5-5)" in d
    assert "<= C and B of the same cell (P-K5-10)" in o


def test_predictions_file_ids_match_script():
    pred = json.loads(k5.PRED.read_text())
    ids = [p["id"] for p in pred["predictions"]]
    assert ids == [f"P-K5-{i}" for i in range(1, 13)]
    assert pred["conditions"]["sha256"] == k5.sha(k5.COND)
