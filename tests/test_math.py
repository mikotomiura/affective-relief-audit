"""命題 1〜4・6 の性質と、原稿の表 1 の値を確かめる。"""

import numpy as np
import pytest

from atact.descriptors import centroid, max_gradient, rq
from atact.field import RenderConfig, height, minmax, procedural_field
from atact.mapping import gamma_from_fs, jacobian, params
from atact.transform import sigma2_single_sine, t_gamma, t_gamma_eps

# 原稿の表 1（式 (1)-(3) から導いた隅の値）
TABLE1 = [
    ((1, -1), (3.0, 0.06, 0.9)),
    ((-1, -1), (3.0, 0.30, 1.495)),
    ((1, 1), (7.0, 0.06, 2.005)),
    ((-1, 1), (7.0, 0.30, 2.6)),
    ((0, 0), (5.0, 0.18, 1.75)),
]


@pytest.mark.parametrize("va,fsg", TABLE1)
def test_table1(va, fsg):
    assert np.allclose(params(*va), fsg)


def test_p1_rank2_parallelogram():
    J = jacobian()
    assert np.linalg.matrix_rank(J) == 2
    assert np.isclose(J[:, 0] @ J[:, 1], -0.2975 * 0.5525)  # -0.1644。直交しない -> 長方形ではない
    rng = np.random.default_rng(1)
    V, A = rng.uniform(-1, 1, (2, 1000))
    f, s, g = params(V, A)
    assert np.allclose(g, gamma_from_fs(f, s))


def test_p1_plane_coefficients():
    # gamma = 0.9 + 0.27625 (f-3) + 2.479... (s-0.06)
    assert np.isclose(gamma_from_fs(4.0, 0.06), 0.9 + 0.27625)
    assert np.isclose(gamma_from_fs(3.0, 0.07), 0.9 + 0.01 * 1.7 * 0.35 / 0.24)


@pytest.mark.parametrize("g", [0.9, 1.0, 1.75, 2.6])
def test_p2_basic_properties(g):
    u = np.linspace(-1, 1, 2001)
    T = t_gamma(u, g)
    assert np.allclose(T, -t_gamma(-u, g))           # 奇関数
    assert np.all(np.diff(T) > 0)                     # 狭義単調
    assert np.allclose(t_gamma(np.array([-1, 0, 1.0]), g), [-1, 0, 1])
    inside = np.abs(u) <= 1
    if g > 1:
        assert np.all(np.abs(T[inside]) >= np.abs(u[inside]) - 1e-12)
    if g < 1:
        assert np.all(np.abs(T[inside]) <= np.abs(u[inside]) + 1e-12)


@pytest.mark.parametrize("g", [0.9, 1.0, 1.75, 2.6])
def test_p3_closed_form(g):
    th = np.linspace(0, 2 * np.pi, 400_001)[:-1]
    num = np.mean(np.abs(np.sin(th)) ** (2 / g))
    assert np.isclose(num, sigma2_single_sine(g), rtol=1e-6)


def test_p3_rq_linear_in_s():
    cfg = RenderConfig()
    F = procedural_field(5.0, cfg)
    for g in (0.9, 2.6):
        r1 = rq(0.06 * t_gamma(F, g))
        r2 = rq(0.30 * t_gamma(F, g))
        assert np.isclose(r2 / r1, 5.0)


def test_rq_is_root_mean_square():
    # 整数周期の正弦の RMS は 1/sqrt(2)（絶対値の平均なら 2/pi になり区別できる）
    x = np.arange(256) / 256
    H = np.tile(np.sin(2 * np.pi * 4 * x), (256, 1))
    assert np.isclose(rq(H), 1 / np.sqrt(2))


def test_centroid_of_pure_tone():
    # 単一の周波数 k の正弦は重心が k になる
    x = np.arange(128) / 128
    H = np.tile(np.sin(2 * np.pi * 6 * x), (128, 1))
    assert np.isclose(centroid(H), 6.0)


def test_p4_minmax_erases_s():
    F = procedural_field(5.0)
    a = minmax(0.06 * t_gamma(F, 1.75))
    b = minmax(0.30 * t_gamma(F, 1.75))
    assert np.allclose(a, b, atol=1e-12)


def test_field_deterministic_by_seed():
    assert np.array_equal(procedural_field(5.0, seed=7), procedural_field(5.0, seed=7))
    assert not np.array_equal(procedural_field(5.0, seed=7), procedural_field(5.0, seed=8))


def test_p6_smoothing_bounds_gradient():
    # gamma > 1 では格子を細かくすると最大勾配が増え、eps でならすと増え方が抑えられる
    g = 2.6
    raw = [max_gradient(t_gamma(procedural_field(5.0, RenderConfig(n=n)), g)) for n in (128, 1024)]
    sm = [
        max_gradient(t_gamma_eps(procedural_field(5.0, RenderConfig(n=n)), g, 0.05))
        for n in (128, 1024)
    ]
    assert raw[1] / raw[0] > 2.0
    assert sm[1] / sm[0] < raw[1] / raw[0]


def test_t_gamma_eps_limits():
    u = np.linspace(-1, 1, 101)
    assert np.allclose(t_gamma_eps(u, 2.0, 1e-9), t_gamma(u, 2.0), atol=1e-6)
    assert np.allclose(t_gamma_eps(np.array([-1.0, 1.0]), 2.6, 0.1), [-1, 1])


def test_height_uses_regime_parameters():
    H1 = height(1, -1)
    H2 = height(-1, 1)
    assert rq(H2) > 5 * rq(H1)
    assert centroid(H2) > centroid(H1)
