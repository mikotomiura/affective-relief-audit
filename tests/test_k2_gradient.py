"""Checks of experiments/k2_gradient.py."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import k2_gradient as k  # noqa: E402

from atact.descriptors import max_gradient
from atact.field import RenderConfig, procedural_field, procedural_field_separable
from atact.mapping import params
from atact.transform import t_gamma, t_gamma_eps

SMALL_N = [8, 16, 32, 64, 128]
SEEDS = [900001, 900002, 900003]  # outside the conditions


@pytest.fixture
def small(monkeypatch):
    monkeypatch.setattr(k, "SLOPE_RANGE", (16, 32, 64, 128))
    monkeypatch.setattr(k, "RATIO_N", (8, 128))
    monkeypatch.setattr(k, "CHANGE_N", (32, 128))
    c = k.load_conditions()
    raw = k.run(c, SEEDS, SMALL_N, workers=1)
    return c, raw, k.analyse(c, raw, SEEDS, SMALL_N)


def test_points_follow_the_rule():
    for p in k.load_conditions()["points"]:
        assert params(p["V"], p["A"]) == pytest.approx((p["f"], p["s"], p["gamma"]))


def test_max_grad_is_s2_6_and_edge_flag():
    F = procedural_field(5.0, RenderConfig(n=64), seed=3)
    assert k.max_grad(F)[0] == max_gradient(F)
    assert np.array_equal(procedural_field_separable(5.0, 64, 3), F)
    X = np.zeros((8, 8))
    X[0, 3] = 1.0
    assert k.max_grad(X)[1] is True
    X = np.zeros((8, 8))
    X[4, 4] = 1.0
    assert k.max_grad(X)[1] is False


def test_ampsum_field_and_bound():
    F = k.field(7.0, 256, 5, "ampsum")
    assert np.array_equal(F, procedural_field_separable(7.0, 256, 5, normalize="none") / 1.875)
    assert k.max_grad(F)[0] <= k.g_bound(7.0)
    assert k.g_bound(7.0) == pytest.approx(2 * np.pi * 7 * 4 / 1.875)


@pytest.mark.parametrize("g", [1.25, 1.75, 2.6])
@pytest.mark.parametrize("eps", [0.01, 0.1, 0.5])
def test_sigma_eps_is_the_largest_slope(g, eps):
    u = np.linspace(-1, 1, 400001)
    d = np.gradient(t_gamma_eps(u, g, eps), u)
    assert d.max() == pytest.approx(k.sigma_eps(g, eps), rel=1e-6)
    assert abs(u[np.argmax(d)]) < 1e-4


@pytest.mark.parametrize("g", [1.25, 2.6])
@pytest.mark.parametrize("eps", [0.01, 0.2, 0.5])
def test_shape_error_bound_p_g6(g, eps):
    u = np.linspace(-1, 1, 200001)
    assert np.abs(t_gamma_eps(u, g, eps) - t_gamma(u, g)).max() <= eps ** (1 / g)


def test_discrete_bound_p_g4_on_an_artificial_array():
    """Sign changes at the edge and inside, steep and flat parts: |grad_h T(F)| <= sigma |grad_h F| pointwise."""
    rng = np.random.default_rng(0)
    F = np.clip(rng.normal(0, 0.4, (40, 40)), -1, 1)
    F[0, :] = np.linspace(-1, 1, 40)
    g, eps = 2.6, 0.1
    gy, gx = np.gradient(F, 1 / 40)
    hy, hx = np.gradient(t_gamma_eps(F, g, eps), 1 / 40)
    assert np.all(np.hypot(hx, hy) <= k.sigma_eps(g, eps) * np.hypot(gx, gy) * (1 + k.TOL) + 1e-300)


def test_growth_on_a_power_law():
    Ns = [128, 256, 512, 1024, 2048, 4096]
    b = 0.6
    X = np.array([[c * n**b for n in Ns] for c in (1.0, 2.0, 3.0)])
    gr = k.growth(Ns, X, 2.5)
    assert gr["ratio_2048_128"]["mean"] == pytest.approx(16**b)
    assert gr["slope_512_4096"]["mean"] == pytest.approx(b)
    assert gr["local_slopes_mean"] == pytest.approx([b] * 5)
    assert gr["ratio_2048_128"]["reference_16^(1-1/gamma)"] == pytest.approx(16**0.6)
    X2 = X.copy()
    X2[:, 1] *= 10  # N = 256 is outside the slope range and the ratio
    g2 = k.growth(Ns, X2, 2.5)
    assert g2["slope_512_4096"]["mean"] == pytest.approx(b)
    assert g2["ratio_2048_128"]["mean"] == pytest.approx(16**b)
    with pytest.raises(ValueError):
        k.growth(Ns[:-1], X[:, :-1], 2.5)


def test_eps_values_use_their_own_dimensions():
    c = k.load_conditions()
    eps = k.eps_values(c, 100.0)
    ex = c["eps_example"]
    assert eps["main"] == pytest.approx(ex["e_min_mm"] * 100 / (2 * ex["L_mm"]))
    for x in ex["sensitivity_values"]:
        assert eps[k.sens_label(x)] == pytest.approx(x["e_min_mm"] * 100 / (2 * x["L_mm"]))
    assert len(eps) == 3


def test_run_and_example_by_hand(small):
    c, raw, A = small
    ex = c["eps_example"]
    G_hi = {sd: k.max_grad(k.field(7.0, 128, sd, "ampsum"))[0] for sd in SEEDS}
    assert raw["G_star"] == max(G_hi.values())
    assert {v["point"] for v in raw["values"]} == {"low", "mid", "high"}
    for v in raw["values"]:
        assert set(v["Meps"]) == ({"main", "L50_e0.05", "L100_e0.4"} if v["point"] == "high" else {"main"})
    # one value recomputed by hand: point high, seed 2, N = 64, sensitivity (100 mm, 0.4 mm)
    v = next(v for v in raw["values"] if (v["point"], v["N"], v["seed"]) == ("high", 64, 900002))
    F = k.field(7.0, 64, 900002, "ampsum")
    e = 0.4 * raw["G_star"] / (2 * 100)
    assert v["Meps"]["L100_e0.4"] == pytest.approx(k.max_grad(0.3 * t_gamma_eps(F, 2.6, e))[0], rel=1e-14)
    assert v["shape_error"]["L100_e0.4"] == pytest.approx(np.abs(t_gamma_eps(F, 2.6, e) - t_gamma(F, 2.6)).max())
    Fm = k.field(7.0, 64, 900002, "maxabs")
    assert v["M_maxabs"] == pytest.approx(k.max_grad(0.3 * t_gamma(Fm, 2.6))[0], rel=1e-14)
    # the worked example by hand
    E = A["example"]["L100_e0.4"]
    j, i = SMALL_N.index(64), SEEDS.index(900002)
    assert E["rows"][j]["T_gamma_eps"]["slope_per_seed"][i] == pytest.approx(1.2 * v["Meps"]["L100_e0.4"] / 60)
    assert E["band_width_mm"]["per_seed"][i] == pytest.approx(2 * e * 100 / G_hi[900002])
    T128 = t_gamma(k.field(7.0, 128, 900002, "ampsum"), 2.6)
    assert E["span_mm_at_Nmax"]["per_seed"][i] == pytest.approx(2.0 * 0.3 * (T128.max() - T128.min()))
    errs = [w["shape_error"]["L100_e0.4"] for w in raw["values"] if w["point"] == "high" and w["N"] == 128]
    assert E["shape_error_mm"]["max_at_Nmax"] == pytest.approx(2.0 * 0.3 * max(errs))
    se = k.sigma_eps(2.6, e)
    assert E["sigma_eps"] == pytest.approx(se)
    assert E["smoothed_slope_bound_grid"]["slope"] == pytest.approx(1.2 * 0.3 * se * raw["G_star"] / 60)
    assert E["smoothed_slope_bound_continuous"]["slope"] == pytest.approx(1.2 * 0.3 * se * k.g_bound(7.0) / 60)
    assert E["rows"][j]["grid_spacing_mm"] == pytest.approx(100 / 64)
    # the main example uses the main eps and L = 50 mm
    M = A["example"]["main"]
    assert M["eps"] == pytest.approx(ex["e_min_mm"] * raw["G_star"] / (2 * ex["L_mm"]))
    assert M["rows"][j]["T_gamma"]["slope_per_seed"][i] == pytest.approx(1.2 * v["M"] / (0.6 * 50))
    # P-G4 holds on real fields for every eps; item counts
    assert all(it["holds"] for it in A["predictions"]["P-G4"])
    assert len(A["predictions"]["P-G4"]) == 4 and len(A["predictions"]["P-G5"]) == 3


def _judge(A0, path, value, Ns=SMALL_N):
    A = copy.deepcopy(A0)
    d = A
    for p in path[:-1]:
        d = d[p]
    d[path[-1]] = value
    return k.predictions(A, Ns)


def test_prediction_boundaries(small):
    _, _, A0 = small
    ref = A0["points"]["high"]["M"]["ratio_2048_128"]["reference_16^(1-1/gamma)"]
    path = ["points", "high", "M", "ratio_2048_128"]
    for mn, mean, ok in ((1.01, ref * 1.19, True), (1.01, ref * 1.21, False), (0.99, ref, False)):
        r = _judge(A0, path, {"min": mn, "mean": mean, "max": 9, "reference_16^(1-1/gamma)": ref})
        assert r["P-G1"][1]["holds"] is ok
    sref = 1 - 1 / 2.6
    for val, ok in ((sref + 0.049, True), (sref - 0.051, False)):
        r = _judge(A0, ["points", "high", "M", "slope_512_4096"],
                   {"mean": val, "lo": 0, "hi": 1, "reference_1-1/gamma": sref})
        assert r["P-G2"][1]["holds"] is ok
    for mx, sl, ok in ((1.49, 0.049, True), (1.51, 0.0, False), (1.0, 0.051, False)):
        lo = copy.deepcopy(A0["points"]["low"]["M"])
        lo["ratio_2048_128"]["max"], lo["slope_512_4096"]["mean"] = mx, sl
        lo["ratio_2048_128"]["mean"] = 1.0
        assert _judge(A0, ["points", "low", "M"], lo)["P-G3"][0]["holds"] is ok
    assert not _judge(A0, ["points", "mid", "eps", "main", "Meps_over_bound_max"], 1 + 1e-9)["P-G4"][0]["holds"]
    assert _judge(A0, ["points", "mid", "eps", "main", "Meps_over_bound_max"], 1.0)["P-G4"][0]["holds"]
    b = A0["points"]["mid"]["eps"]["main"]["shape_error"]["bound_eps^(1/gamma)"]
    assert not _judge(A0, ["points", "mid", "eps", "main", "shape_error", "max"], b * (1 + 1e-9))["P-G6"][0]["holds"]
    i4 = SMALL_N.index(128)
    for me4, m4, ok in ((1.049, 2.01, True), (0.949, 2.01, False), (1.051, 2.01, False), (1.0, 1.99, False)):
        A = copy.deepcopy(A0)
        me, m = [1.0] * len(SMALL_N), [1.0] * len(SMALL_N)
        me[i4], m[i4] = me4, m4
        for E in A["points"]["high"]["eps"].values():
            E["Meps"]["seed_mean_by_N"] = list(me)
        A["points"]["high"]["M"]["seed_mean_by_N"] = m
        assert all(it["holds"] is ok for it in k.predictions(A, SMALL_N)["P-G5"])
