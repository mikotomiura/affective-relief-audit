"""Checks of experiments/text_path_example.py on a small artificial lexicon (the real lexicon is not in the repo)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import text_path_example as t  # noqa: E402

from atact.lexicon import load_lexicon, sentence_point
from atact.mapping import params


@pytest.fixture
def lex(tmp_path):
    p = tmp_path / "lex.txt"
    p.write_text("term\tvalence\tarousal\tdominance\n"
                 "storm\t-0.6\t0.9\t0.2\n"
                 "calm\t0.8\t-0.9\t0.1\n"
                 "sea\t0.3\t0.1\t0.0\n"
                 "the\t0.1\t-0.2\t0.0\n"
                 "is\t0.0\t-0.1\t0.0\n"
                 "who\t-0.1\t0.0\t0.0\n"
                 "am\t0.05\t0.0\t0.0\n"
                 "calm sea\t0.9\t-1.0\t0.3\n"
                 "storm over\t-0.5\t0.8\t0.0\n"
                 "who am\t0.2\t0.2\t0.0\n")
    return load_lexicon(p)


@pytest.fixture
def cond():
    return t.load_conditions()


TEXTS = {"A": "Who am I? Who is the storm? Am I?", "B": "The calm sea. The storm is the sea."}


@pytest.fixture
def result(cond, lex, monkeypatch):
    c = json.loads(json.dumps(cond))
    c["surface"]["grids_N"] = [32, 64]
    return t.run(c, TEXTS, lex, 0.35, coverage=False)


def test_main_variant_is_the_lexicon_baseline(lex):
    for s in ("Who is the storm?", "The calm sea.", "Nothing here."):
        p, q = t.point(s, lex, None), sentence_point(s, lex)
        assert (p["V"], p["A"], p["Z"], p["matched"]) == (q.V, q.A, q.Z, q.matched)
        assert (p["f"], p["s"], p["gamma"]) == pytest.approx(tuple(float(x) for x in params(q.V, q.A)))


def test_function_words_are_dropped_and_z0_is_flagged(lex):
    sw = t.stop_words()
    p = t.point("Who is the storm?", lex, sw)
    assert p["matched"] == ["storm"] and p["Z"] == 1 and p["V"] == -0.6
    q = t.point("Who am I?", lex, sw)
    assert q["Z"] == 0 and q["unmatched"] and (q["V"], q["A"]) == (0.0, 0.0)
    # a multiword term is kept unless every token is a stop word
    assert t.point("The calm sea.", lex, sw)["matched"] == ["calm sea"]
    # one stop-word token is not enough to drop a multiword term; all stop-word tokens drop it
    assert t.point("A storm over.", lex, sw)["matched"] == ["storm over"]
    assert t.point("Who am I?", lex, None)["matched"] == ["who am"]
    assert t.point("Who am I?", lex, sw)["matched"] == []


def test_stop_word_list_is_the_one_of_the_conditions(cond):
    sw = t.stop_words()
    v = cond["variants"]["function_words_removed"]
    assert t.stop_words_sha256(sw) in v and f"{len(sw)} words" in v


def test_predictions_hold_on_the_test_texts(result):
    out, images = result
    p = out["predictions"]
    assert p["P-T1"]["holds"] and p["P-T2"]["holds"] and p["P-T3"]["holds"]
    assert p["P-T3"]["cases_checked"] > 0
    # text A without function words: 'Who am I?' and 'Am I?' are unmatched and must give the same tile
    assert p["P-T4"]["A"]["unmatched"] == [0, 2] and p["P-T4"]["A"]["holds"] is True
    assert p["P-T4"]["A"]["at_origin_with_params_of_(0,0)"] is True
    # the figure and P-T4 use the first grid
    assert images[("A", "main", 0)]["common"].shape == (32, 32)
    assert images[("A", "function_words_removed", 0, 64)]["common"].shape == (64, 64)
    assert p["P-T4"]["B"]["holds"] is None


def test_exports_by_hand(cond, lex):
    d = {"D": 1.2, "L": 50.0, "s_max": 0.30}
    p = t.point("The storm.", lex, None)
    r = t.tile(p, 32, 42, 0.35, d)
    from atact.field import procedural_field_separable
    from atact.transform import t_gamma

    H = p["s"] * t_gamma(procedural_field_separable(p["f"], 32, 42, normalize="ampsum"), p["gamma"])
    assert r["z"]["common"] == pytest.approx(1.2 * H / 0.6, abs=1e-15)
    assert r["span_mm"]["minmax"] == pytest.approx(1.2)
    gy, gx = np.gradient(r["z"]["common"], 50.0 / 32)  # mm per mm
    assert r["slope"]["common"] == pytest.approx(float(np.hypot(gx, gy).max()))
    gy, gx = np.gradient(r["z"]["minmax"], 50.0 / 32)
    assert r["slope"]["minmax"] == pytest.approx(float(np.hypot(gx, gy).max()))
    assert r["angle_deg"]["common"] == pytest.approx(np.degrees(np.arctan(r["slope"]["common"])))


def test_comparison_ratios(result):
    out, _ = result
    for v in t.VARIANTS:
        rs = [x for name in out["texts"] for x in out["comparison"][v][name]["common_span_ratio_to_largest"]]
        assert max(rs) == 1.0 and min(rs) > 0


def test_p_t1_detects_a_broken_minmax(result, cond, lex, monkeypatch):
    monkeypatch.setattr(t, "minmax", lambda X: (X - X.min()) / (X.max() - X.min()) * (1 + 1e-6 * (X > 0)))
    c = json.loads(json.dumps(cond))
    c["surface"]["grids_N"] = [32]
    out, _ = t.run(c, TEXTS, lex, 0.35, coverage=False)
    assert out["predictions"]["P-T1"]["holds"] is False


def test_p_t3_detects_a_wrong_eps_transform(cond, lex, monkeypatch):
    real = t.t_gamma_eps
    monkeypatch.setattr(t, "t_gamma_eps", lambda u, g, e: real(u, g, e / 10))
    c = json.loads(json.dumps(cond))
    c["surface"]["grids_N"] = [128]
    out, _ = t.run(c, TEXTS, lex, 0.35, coverage=False)
    assert out["predictions"]["P-T3"]["holds"] is False


def test_p_t4_detects_different_tiles(cond, lex, monkeypatch):
    real = t.point
    calls = {"n": 0}

    def shifted(s, lx, drop):
        p = real(s, lx, drop)
        if drop is not None and p["unmatched"]:
            calls["n"] += 1
            p["s"] += 0.01 * calls["n"]
        return p

    monkeypatch.setattr(t, "point", shifted)
    c = json.loads(json.dumps(cond))
    c["surface"]["grids_N"] = [32]
    out, _ = t.run(c, TEXTS, lex, 0.35, coverage=False)
    assert out["predictions"]["P-T4"]["A"]["holds"] is False


def test_check_inputs_refuses_a_wrong_lexicon(cond, tmp_path):
    p = tmp_path / "x.txt"
    p.write_text("term\tvalence\tarousal\tdominance\n")
    with pytest.raises(SystemExit):
        t.check_inputs(cond, p)


def test_eps_of_the_conditions_matches_k2(cond):
    if not t.K2.exists():
        pytest.skip("results/k2_gradient.json not present")
    eps = json.loads(t.K2.read_text())["analysis"]["eps"]["main"]
    assert f"eps = {eps!r}" in cond["exports"]["common_eps"]


def test_conditions_texts():
    c = t.load_conditions()
    assert c["texts"]["A"]["content"] == "Is this the place? Where am I? Who am I?"
    assert set(c["texts"]) >= {"A", "B"}


def test_exports_on_a_known_field(lex, monkeypatch):
    """Independent of the generator: a plane F(x, y) = x - 1/2 with the parameters of a hand-computed point."""
    n = 16
    x = np.arange(n) / n
    monkeypatch.setattr(t, "procedural_field_separable",
                        lambda f, n_, seed, octaves, normalize: np.tile(x - 0.5, (n_, 1)))
    p = {"f": 4.0, "s": 0.12, "gamma": 1.325}
    # (V, A) = (0.5, -0.5): f = 3 + 4 * 0.25, s = 0.06 + 0.24 * 0.25, gamma = 0.9 + 1.7 * (0.65 * 0.25 + 0.35 * 0.25)
    assert tuple(float(v) for v in params(0.5, -0.5)) == pytest.approx((4.0, 0.12, 1.325))
    d = {"D": 1.2, "L": 50.0, "s_max": 0.30}
    r = t.tile(p, n, 42, 0.35, d)
    u = x - 0.5
    T = np.sign(u) * np.abs(u) ** (1 / 1.325)
    Te = u * (u**2 + 0.35**2) ** ((1 / 1.325 - 1) / 2) / (1 + 0.35**2) ** ((1 / 1.325 - 1) / 2)
    assert r["z"]["common"][0] == pytest.approx(2.0 * 0.12 * T, abs=1e-15)
    assert r["z"]["common_eps"][0] == pytest.approx(2.0 * 0.12 * Te, abs=1e-15)
    assert r["z"]["minmax"][0] == pytest.approx(1.2 * (T - T.min()) / (T.max() - T.min()), abs=1e-15)
    assert r["span_mm"]["common"] == pytest.approx(2.0 * 0.12 * (T.max() - T.min()))
    # largest slope: central differences of the common heights, per mm
    dz = np.gradient(2.0 * 0.12 * T, 50.0 / n)
    assert r["slope"]["common"] == pytest.approx(float(np.abs(dz).max()))
    # the plane is constant along y, so the first maximum in row-major order lies in row 0 (an edge row)
    assert r["edge_argmax"]["common"] is True
    assert r["shape_change_mm"] == pytest.approx(float(np.abs(2.0 * 0.12 * (Te - T)).max()))


def test_coverage_is_checked_against_the_conditions(cond, lex):
    c = json.loads(json.dumps(cond))
    c["surface"]["grids_N"] = [16]
    with pytest.raises(SystemExit, match="coverage"):
        t.run(c, TEXTS, lex, 0.35, coverage=True)


def test_figure_grey_levels_in_range(result, tmp_path):
    out, images = result
    for v in t.VARIANTS:
        fig = t.figure(out, images, v, tmp_path / f"{v}.pdf")
        assert all(0.0 <= g["grey_min"] and g["grey_max"] <= 1.0 for g in fig["grey"])


def test_real_run_refuses_dirty_inputs(monkeypatch, tmp_path):
    monkeypatch.setattr(t, "OUT_JSON", tmp_path / "x.json")
    monkeypatch.setattr(t, "OUT_MD", tmp_path / "x.md")
    monkeypatch.setattr(t, "FIGS", tmp_path)

    def no_run(*a, **k):  # if the guard is broken, stop here instead of computing the real texts
        raise AssertionError("the run started")

    monkeypatch.setattr(t, "run", no_run)
    monkeypatch.setattr(t, "git_state", lambda: {"git_commit": "x", "git_dirty": True})
    monkeypatch.setattr(t, "check_inputs", lambda c, p: 0.35)
    monkeypatch.setattr(sys, "argv", ["text_path_example.py"])
    with pytest.raises(SystemExit, match="commit first"):
        t.main()
