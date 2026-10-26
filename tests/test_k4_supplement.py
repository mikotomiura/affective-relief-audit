"""Checks of experiments/k4_supplement.py: the low-memory centroid against the full DFT, the shell spectrum against a
brute-force binning, the extrapolation fits and the implementation check on synthetic values."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

from atact.descriptors import radial_frequency, spectral_centroids
from atact.field import procedural_field_separable
from atact.transform import t_gamma

spec = importlib.util.spec_from_file_location(
    "k4_supplement", Path(__file__).resolve().parents[1] / "experiments" / "k4_supplement.py")
ks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ks)


@pytest.mark.parametrize("f,g,n,seed,block", [(5, 0.9, 64, 3, 512), (3, 2.6, 128, 7, 48), (7, 1.25, 256, 11, 100),
                                              (5.5, 1.75, 128, 2, 30), (5, 1.0, 64, 1, 16)])
def test_lean_centroid_equals_full_dft(f, g, n, seed, block):
    H = t_gamma(procedural_field_separable(f, n, seed), g)
    ref = spectral_centroids(H, 16.0)["centroid_amp"]
    got = ks.lean_centroid(f, n, seed, g, block=block)["centroid_amp"]
    assert got == pytest.approx(ref, rel=1e-12)


@pytest.mark.parametrize("n,block,seed", [(64, 512, s) for s in range(1, 11)] + [(128, 40, 4)])
def test_shell_density_equals_brute_force(n, block, seed):
    f, g = 5, 0.9
    H = t_gamma(procedural_field_separable(f, n, seed), g)
    mag = np.abs(np.fft.fft2(H - H.mean())) / n**2
    rho = radial_frequency(n)
    keep = rho >= 1
    edges = ks.shell_edges(n)
    # independent binning: edges 2^(j/8) built here, bin j holds edges[j] <= rho < edges[j + 1]
    own = 2.0 ** (np.arange(len(edges) + 8) / 8)
    idx = np.searchsorted(own, rho[keep], side="right") - 1
    sums = np.bincount(idx, weights=mag[keep], minlength=len(edges) - 1)
    assert len(sums) == len(edges) - 1
    got = np.asarray(ks.lean_centroid(f, n, seed, g, block=block)["shell_density"])
    np.testing.assert_allclose(got * np.diff(edges), sums, rtol=1e-10, atol=1e-15)
    # every nonzero bin is in a shell: the shells hold the whole amplitude sum
    assert (got * np.diff(edges)).sum() == pytest.approx(mag[keep].sum(), rel=1e-12)


@pytest.mark.parametrize("n", [32, 64, 1024, 16384])
def test_shell_edges_cover_the_grid_with_positive_widths(n):
    e = ks.shell_edges(n)
    assert (np.diff(e) > 0).all()
    rmax = np.hypot(np.float64(n // 2), np.float64(n // 2))
    assert ks.shell_index(np.array([rmax]))[0] == len(e) - 2
    assert e[0] == 1.0


def test_band_of_the_conditions_has_16_shells():
    rows = []
    for s in (1, 2):
        rows.append({"f": 5, "gamma": 0.9, "N": 16384, "seed": s,
                     "shell_density": list(np.arange(1, len(ks.shell_edges(16384))) ** -1.5)})
    out = ks.shell_exponent(rows, 5, 0.9, 16384, [1, 2], [512, 2048])
    assert out["n_shells"] == 16


def test_shell_exponent_recovers_a_power_law():
    n = 1024
    e = ks.shell_edges(n)
    centre = np.sqrt(e[:-1] * e[1:])
    rows = [{"f": 3, "gamma": 1.25, "N": n, "seed": s, "shell_density": list((1 + 0.01 * s) * centre ** -1.3)}
            for s in (1, 2, 3)]
    out = ks.shell_exponent(rows, 3, 1.25, n, [1, 2, 3], [32, 128])
    assert out["mean"] == pytest.approx(-1.3, abs=1e-12)


def test_e_and_delta():
    assert [round(ks.e_gamma(g), 4) for g in (0.9, 1.25, 1.75, 2.6)] == [0.3889, 0.7, 0.9286, 1.0]
    assert [round(ks.delta_gamma(g), 4) for g in (0.9, 1.25, 1.75, 2.6)] == [0.3889, 0.3, 0.0714, 0.1154]


def test_conditions_agree_with_the_script():
    c = json.loads(ks.COND.read_text())
    assert c["grids_N"][-6:] == [512, 1024, 2048, 4096, 8192, 16384]
    assert c["f"] == [3, 5, 7] and c["gamma"] == [0.9, 1.25, 1.75, 2.6] and c["seeds"] == list(range(1, 21))
    e3 = [x for x in c["approach_2_extrapolation"]["forms"] if x["name"] == "E3"][0]["rule"]
    for g in c["gamma"]:
        assert str(round(ks.delta_gamma(g), 4)) in e3
    shell = c["approach_3_estimate"]["compared_quantities"][0]
    for g in c["gamma"]:
        assert str(round(-(1 / g + 0.5), 4)) in shell


N6 = [512, 1024, 2048, 4096, 8192, 16384]


def test_e1_recovers_the_exponent():
    N = np.array(N6, dtype=float)
    C = 30.0 + 0.8 * N**0.45
    r = ks.fit_e1(N6, C)
    assert not r["failed"] and r["c"] == pytest.approx(0.45, abs=1e-5)


def test_e1_counts_a_fit_at_the_bound_as_failed():
    N = np.array(N6, dtype=float)
    C = 5.0 * N**1.8  # exponent beyond the bound 1.5
    r = ks.fit_e1(N6, C)
    assert r["failed"] and "c at a bound" in r["reasons"]


def test_e2_and_e3_recover_the_intercept():
    N = np.array(N6, dtype=float)
    Nm = np.sqrt(N[:-1] * N[1:])
    rows2, rows3 = [], []
    for _ in range(4):
        s2 = 0.6 - 1.7 / np.log(Nm)
        s3 = 0.7 - 2.0 * Nm ** (-ks.delta_gamma(1.25))
        # integrate the local slopes back to C so that extrapolations() sees centroid series
        rows2.append(np.exp(np.concatenate([[0.0], np.cumsum(s2 * np.diff(np.log(N)))])))
        rows3.append(np.exp(np.concatenate([[0.0], np.cumsum(s3 * np.diff(np.log(N)))])))
    out2 = ks.extrapolations(N6, np.array(rows2) * np.array([[1.0], [1.1], [0.9], [1.2]]), 1.25)
    out3 = ks.extrapolations(N6, np.array(rows3) * np.array([[1.0], [1.1], [0.9], [1.2]]), 1.25)
    assert out2["E2"]["mean"] == pytest.approx(0.6, abs=1e-10)
    assert out3["E3"]["mean"] == pytest.approx(0.7, abs=1e-10)
    assert out3["E3"]["outcome"] in ("contains e(gamma)", "below", "above")


def test_rate_of_approach_recovers_delta():
    N = np.array(N6, dtype=float)
    Nm = np.sqrt(N[:-1] * N[1:])
    g = 0.9
    rows = []
    for k in (1.0, 1.3, 0.8):
        s = ks.e_gamma(g) - k * 3.0 * Nm ** (-ks.delta_gamma(g))
        rows.append(np.exp(np.concatenate([[0.0], np.cumsum(s * np.diff(np.log(N)))])))
    r = ks.rate_of_approach(N6, np.array(rows), g)
    assert r["n_positive_seeds"] == 3 and r["mean_decreasing"]
    assert r["rate"]["mean"] == pytest.approx(-ks.delta_gamma(g), abs=1e-10)


def _rows(vals):
    return [{"f": 5, "gamma": 0.9, "N": n, "seed": s, "centroid_amp": v} for (n, s), v in vals.items()]


def test_implementation_check_passes_and_fails():
    ref = {(5, 0.9, n, s): 10.0 + n / 1000 + s for n in (128, 4096) for s in (1, 2)}
    good = {(n, s): ref[(5, 0.9, n, s)] * (1 + 1e-12) for n in (128, 4096) for s in (1, 2)}
    assert ks.implementation_check(_rows(good) + _rows({(8192, 1): 99.0}), ref)["passed"]
    bad = dict(good)
    bad[(4096, 2)] *= 1 + 1e-8
    assert not ks.implementation_check(_rows(bad), ref)["passed"]
    short = {k: v for k, v in good.items() if k != (128, 1)}
    assert not ks.implementation_check(_rows(short), ref)["passed"]


def test_p_s1_logic():
    c = {"grids_N": [512, 1024, 2048, 4096], "predictions": []}
    cell = {"f": 5, "gamma": 0.9, "e": 0.3889, "local_mean": [0.1, 0.2, 0.3],
            "slopes": {"1024-4096": {"mean": 0.2, "lo": 0.1, "hi": 0.3}},
            "extrapolation": {}, "shell": {"4096": {"mean": -1.6, "lo": -1.7, "hi": -1.5}},
            "target_shell": -1.6111,
            "rate": {"n_positive_seeds": 0, "mean_decreasing": False, "target": -0.3889}}
    P = ks.predictions(dict(c, seeds=[1]), {"cells": [cell]})
    assert P["P-S1"]["items"][0]["holds"] and P["P-S2"]["items"][0]["holds"] and P["P-S4"]["items"][0]["holds"]
    cell["local_mean"] = [0.1, 0.3, 0.3]
    P = ks.predictions(dict(c, seeds=[1]), {"cells": [cell]})
    assert not P["P-S1"]["items"][0]["holds"]


# --- stop logic, resume and non-finite values -------------------------------------------------------------------


from concurrent.futures import ThreadPoolExecutor

TINY = {"f": [5], "gamma": [0.9], "grids_N": [2048, 4096, 8192], "seeds": [1, 2]}


def _fake_run_job(job):
    f, g, n, s = job
    return {"f": f, "gamma": g, "N": n, "seed": s, "centroid_amp": 10.0 + n / 1000 + s, "shell_density": [1.0]}


def _tiny_ref(scale=1.0):
    return {(5, 0.9, n, s): (10.0 + n / 1000 + s) * scale for n in (2048, 4096) for s in (1, 2)}


@pytest.fixture
def threaded(monkeypatch):
    monkeypatch.setattr(ks, "ProcessPoolExecutor", ThreadPoolExecutor)
    monkeypatch.setattr(ks, "run_job", _fake_run_job)


IDENT = {"version": "test"}


def test_compute_stops_before_large_n_when_the_check_fails(threaded, tmp_path):
    partial = tmp_path / "p.jsonl"
    with pytest.raises(SystemExit):
        ks.compute(TINY, partial, _tiny_ref(1 + 1e-6), IDENT, "t0")
    rows = [json.loads(x) for x in partial.read_text().splitlines()[1:]]
    assert len(rows) == 4 and max(r["N"] for r in rows) == 4096


def test_compute_runs_all_when_the_check_passes(threaded, tmp_path):
    rows, started = ks.compute(TINY, tmp_path / "p.jsonl", _tiny_ref(), IDENT, "t0")
    assert len(rows) == 6 and started == "t0"


def test_resume_refuses_another_identity_and_foreign_rows(threaded, tmp_path):
    partial = tmp_path / "p.jsonl"
    partial.write_text(json.dumps({"identity": {"version": "old"}, "started": "t-1"}) + "\n")
    with pytest.raises(SystemExit):
        ks.compute(TINY, partial, _tiny_ref(), IDENT, "t0")
    bad = dict(_fake_run_job((7, 0.9, 2048, 1)))
    partial.write_text(json.dumps({"identity": IDENT, "started": "t-1"}) + "\n" + json.dumps(bad) + "\n")
    with pytest.raises(SystemExit, match="not a job"):
        ks.compute(TINY, partial, _tiny_ref(), IDENT, "t0")


def test_resume_rechecks_and_drops_a_cut_last_line(threaded, tmp_path):
    partial = tmp_path / "p.jsonl"
    wrong = dict(_fake_run_job((5, 0.9, 2048, 1)), centroid_amp=999.0)
    partial.write_text(json.dumps({"identity": IDENT, "started": "t-1"}) + "\n" + json.dumps(wrong) + "\n")
    with pytest.raises(SystemExit):  # a wrong small-N row from the partial file is checked too
        ks.compute(TINY, partial, _tiny_ref(), IDENT, "t0")
    good = _fake_run_job((5, 0.9, 2048, 1))
    partial.write_text(json.dumps({"identity": IDENT, "started": "t-1"}) + "\n" + json.dumps(good) + "\n"
                       + '{"f": 5, "gam')
    rows, started = ks.compute(TINY, partial, _tiny_ref(), IDENT, "t0")
    assert len(rows) == 6 and started == "t-1"


def test_run_job_rejects_non_finite(monkeypatch):
    monkeypatch.setattr(ks, "lean_centroid", lambda f, n, s, g: {"centroid_amp": float("nan"), "shell_density": [1.0]})
    with pytest.raises(RuntimeError):
        ks.run_job((5, 0.9, 64, 1))


def test_implementation_check_fails_on_nan_anywhere():
    ref = {(5, 0.9, 128, s): 10.0 + s for s in (1, 2, 3)}
    rows = [{"f": 5, "gamma": 0.9, "N": 128, "seed": s, "centroid_amp": 10.0 + s} for s in (1, 2, 3)]
    rows[1]["centroid_amp"] = float("nan")
    assert not ks.implementation_check(rows, ref)["passed"]
    rows[1]["centroid_amp"] = 12.0
    assert ks.implementation_check(rows, ref)["passed"]
    ref[(5, 0.9, 128, 3)] = float("nan")
    assert not ks.implementation_check(rows, ref)["passed"]


def test_outcome_of_a_non_finite_interval():
    assert ks.outcome({"lo": float("nan"), "hi": float("nan")}, 0.5) == "not determined"
    assert ks.outcome({"lo": 0.1, "hi": 0.2}, 0.5) == "below"


def test_e1_constant_series_is_failed():
    r = ks.fit_e1(N6, np.full(6, 40.0))
    assert r["failed"]


def test_k4_reference_takes_the_maxabs_direct_rows():
    c = json.loads(ks.COND.read_text())
    ref = ks.k4_reference(c)
    assert len(ref) == 12 * 20 * 6
    rows = json.loads(ks.K4_RESULTS.read_text())["rows"]
    want = [r for r in rows if r["field"] == "sum" and r["f"] == 5 and r["gamma"] == 0.9 and r["N"] == 512
            and r["seed"] == 3 and r["sampling"] == "direct" and r["r"] == 1 and r["normalize"] == "maxabs"]
    assert len(want) == 1 and ref[(5, 0.9, 512, 3)] == want[0]["values"]["raw"]["centroid_amp"]


# --- prediction boundaries ----------------------------------------------------------------------------------------


def _cell(**kw):
    cell = {"f": 5, "gamma": 0.9, "e": 0.3889, "local_mean": [0.1, 0.2, 0.3],
            "slopes": {"1024-4096": {"mean": 0.2, "lo": 0.1, "hi": 0.3}}, "extrapolation": {},
            "shell": {"4096": {"mean": -1.6, "lo": -1.7, "hi": -1.5}}, "target_shell": -1.6111,
            "rate": {"n_positive_seeds": 1, "mean_decreasing": True, "target": -0.3889,
                     "rate": {"mean": -0.39, "lo": -0.5, "hi": -0.3}}}
    cell.update(kw)
    return cell


C4 = {"grids_N": [512, 1024, 2048, 4096], "predictions": [], "seeds": [1]}


def test_p_s4_uses_the_tolerance_band():
    # interval [-1.58, -1.57] does not contain -1.6111 but meets [-1.6611, -1.5611]
    P = ks.predictions(C4, {"cells": [_cell(shell={"4096": {"mean": -1.575, "lo": -1.58, "hi": -1.57}})]})
    assert P["P-S4"]["items"][0]["holds"]
    P = ks.predictions(C4, {"cells": [_cell(shell={"4096": {"mean": -1.5, "lo": -1.55, "hi": -1.45}})]})
    assert not P["P-S4"]["items"][0]["holds"]


def test_p_s5_holds_and_fails_at_each_condition():
    assert ks.predictions(C4, {"cells": [_cell()]})["P-S5"]["items"][0]["holds"]
    for change in ({"n_positive_seeds": 0}, {"mean_decreasing": False},
                   {"rate": {"mean": -0.2, "lo": -0.25, "hi": -0.15}}):
        r = dict(_cell()["rate"], **change)
        assert not ks.predictions(C4, {"cells": [_cell(rate=r)]})["P-S5"]["items"][0]["holds"]


def test_e1_not_determined_only_above_two_failures(monkeypatch):
    N = np.array(N6, dtype=float)
    C = np.array([30.0 + (0.8 + 0.01 * s) * N**0.45 for s in range(6)])
    real = ks.fit_e1
    for nf, expect in ((2, False), (3, True)):
        calls = {"i": 0}

        def fake(Nr, row, calls=calls, nf=nf):
            calls["i"] += 1
            out = real(Nr, row)
            return dict(out, failed=calls["i"] <= nf)

        monkeypatch.setattr(ks, "fit_e1", fake)
        out = ks.extrapolations(N6, C, 1.25)
        assert (out["E1"]["outcome"] == "not determined") is expect


def test_check_is_made_on_resume_when_every_small_n_is_done(threaded, tmp_path):
    partial = tmp_path / "p.jsonl"
    small = [_fake_run_job((5, 0.9, n, s)) for n in (2048, 4096) for s in (1, 2)]
    small[0]["centroid_amp"] = 999.0
    partial.write_text(json.dumps({"identity": IDENT, "started": "t-1"}) + "\n"
                       + "".join(json.dumps(r) + "\n" for r in small))
    with pytest.raises(SystemExit, match="implementation check"):
        ks.compute(TINY, partial, _tiny_ref(), IDENT, "t0")


def test_implementation_check_fails_on_a_row_without_reference():
    ref = {(5, 0.9, 128, 1): 11.0}
    rows = [{"f": 5, "gamma": 0.9, "N": 128, "seed": 1, "centroid_amp": 11.0},
            {"f": 5, "gamma": 0.9, "N": 128, "seed": 9, "centroid_amp": 3.0}]
    r = ks.implementation_check(rows, ref)
    assert r["missing"] == 1 and not r["passed"]


def test_k4_reference_refuses_another_file(monkeypatch):
    monkeypatch.setattr(ks, "K4_RESULTS_SHA256", "0" * 64)
    with pytest.raises(SystemExit):
        ks.k4_reference(json.loads(ks.COND.read_text()))
