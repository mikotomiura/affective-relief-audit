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


# ---- 付録 A（advice/proofs/appendix-a.tex）の各主張 ----

from scipy.integrate import quad
from scipy.special import gamma as Gamma_fn
from scipy.special import zeta

from atact.descriptors import centroid_1d
from atact.transform import fourier_coeff_odd


def _sine(f, n, g, phase=0.0):
    # 零点に乗る標本は sin(pi) = 1.2e-16 になり、T_gamma が (1e-16)^(1/gamma) に増幅するので 0 にそろえる
    u = np.sin(2 * np.pi * f * np.arange(n) / n + phase)
    u[np.abs(u) < 1e-12] = 0.0
    return t_gamma(u, g)


def _c_gamma(g):
    a = 1 / g
    return 4 * Gamma_fn(1 + a) * np.cos(np.pi * a / 2) / np.pi


def _d_gamma(g, nmax=4_000_001):
    a = 1 / g
    n = np.arange(1, nmax, 2)
    return fourier_coeff_odd(n, g).sum() + _c_gamma(g) * nmax ** (-a) / (2 * a)


def _k_limit(g, f):
    """定理 A.6.1 (i) の極限の定数 K_gamma(f)。"""
    a = 1 / g
    phi = lambda t: zeta(1 + a, t) - zeta(1 + a, 1 - t)  # sum_m sign(t+m)|t+m|^(-1-a)
    pts = [j / (2 * f) for j in range(1, f) if j / (2 * f) < 0.5]
    integral = quad(lambda t: abs(f * t - round(f * t)) * phi(t), 0, 0.5, points=pts or None, limit=500)[0]
    return _c_gamma(g) * integral / (2 * _d_gamma(g))


def _sandwich(g, f, n):
    k = np.arange(1, n // 2, 2)
    b, bn = fourier_coeff_odd(k, g), fourier_coeff_odd(n - k, g)
    w = np.abs((f * k + n // 2) % n - n // 2)  # ||f k||_N
    return (w * (b - bn)).sum() / b.sum(), (w * b).sum() / (b - bn).sum()


@pytest.mark.parametrize("g", [0.9, 1.75, 2.6])
def test_a4_bn_closed_form_matches_fft(g):
    m = 2**16
    z = np.fft.fft(_sine(1, m, g)) / m
    for n in (1, 3, 5):
        assert np.isclose(-2 * z[n].imag, fourier_coeff_odd(n, g), rtol=1e-8)
    for n in (51, 201):
        assert np.isclose(-2 * z[n].imag, fourier_coeff_odd(n, g), rtol=1e-5)
    assert np.allclose(z[2:200:2], 0, atol=1e-12)  # 偶数次は 0


@pytest.mark.parametrize("g", [0.9, 1.75, 2.6])
def test_a4_bn_decay_constant(g):
    n = 100_001
    assert np.isclose(fourier_coeff_odd(n, g) * n ** (1 + 1 / g) / _c_gamma(g), 1, atol=1e-4)


def test_a4_bn_sign_and_monotone():
    n = np.arange(1, 2001, 2)
    b = fourier_coeff_odd(n, 1.75)  # alpha < 1
    assert np.all(b > 0) and np.all(np.diff(b) < 0)
    b = fourier_coeff_odd(n, 0.9)  # 1 < alpha < 3
    assert b[0] > 0 and np.all(b[1:] < 0) and np.all(np.diff(np.abs(b[1:])) < 0)


def test_a4_exception_odd_alpha():
    # gamma = 1 は sin そのもの。gamma = 1/3 は sin^3 = (3 sin t - sin 3t)/4
    assert np.allclose(fourier_coeff_odd(np.arange(3, 101, 2), 1.0), 0, atol=1e-15)
    m = 4096
    z = np.fft.fft(_sine(1, m, 1 / 3)) / m
    assert np.allclose([-2 * z[1].imag, -2 * z[3].imag], [0.75, -0.25])
    assert np.allclose(z[5:100], 0, atol=1e-12)


@pytest.mark.parametrize("g", [1.75, 2.6])
def test_a5_alias_bounds(g):
    n = 256
    beta = (2j * np.fft.fft(_sine(1, n, g)) / n).real  # beta_k = 2i zhat(k) / N
    k = np.arange(1, n // 2, 2)
    b, bn = fourier_coeff_odd(k, g), fourier_coeff_odd(n - k, g)
    assert np.all(beta[k] <= b + 1e-12)
    assert np.all(beta[k] >= b - bn - 1e-12)
    assert np.allclose(beta[0 : n : 2], 0, atol=1e-12)


def test_a5_permutation():
    n, f = 128, 5
    z1 = np.abs(np.fft.fft(_sine(1, n, 1.75)))
    zf = np.abs(np.fft.fft(_sine(f, n, 1.75)))
    k = np.arange(n)
    assert np.allclose(zf[(f * k) % n], z1, atol=1e-9)


TABLE_P5 = {1.75: [10.36, 18.26, 32.69, 58.89], 2.6: [13.50, 29.71, 67.27, 154.69]}


@pytest.mark.parametrize("g", [1.75, 2.6])
def test_a6_sandwich_and_table(g):
    for n, ref in zip((128, 512, 2048, 8192), TABLE_P5[g]):
        c = centroid_1d(_sine(5, n, g))
        lo, hi = _sandwich(g, 5, n)
        assert lo <= c <= hi
        assert round(c, 2) == ref


@pytest.mark.parametrize("g,f", [(1.75, 5), (2.6, 7)])
def test_a6_limit_constant(g, f):
    n = 2**18
    a = 1 / g
    assert np.isclose(centroid_1d(_sine(f, n, g)) / n ** (1 - a), _k_limit(g, f), rtol=0.01)


def _cstar(g, nmax=2_000_001):
    """定理 A.6.1 (ii) の C*。sum n|b_n| は n^(-1/gamma) でしか収束しないので尾部を Hurwitz のゼータで足す。"""
    a = 1 / g
    n = np.arange(1, nmax, 2)
    b = np.abs(fourier_coeff_odd(n, g))
    c = abs(_c_gamma(g))
    j0 = (nmax - 1) // 2  # 次の奇数 nmax = 2 j0 + 1
    num = (n * b).sum() + c * 2 ** (-a) * zeta(a, j0 + 0.5)
    den = b.sum() + c * 2 ** (-1 - a) * zeta(1 + a, j0 + 0.5)
    return num / den


def test_a6_gamma_below_one_converges():
    g, f = 0.9, 5
    lim = f * _cstar(g)
    assert np.isclose(lim, f * _cstar(g, 4_000_001), rtol=1e-8)  # 打ち切りに依らない
    c = [centroid_1d(_sine(f, m, g)) for m in (2**13, 2**16, 2**20)]
    assert round(c[0], 2) == 7.21  # 命題 5 の表
    assert np.all(np.diff(c) > 0) and c[-1] < lim
    # 差は N^(1 - 1/gamma) で減る: N を 2^4 倍にすると 2^(4 * (1 - 1/0.9)) = 0.735 倍
    assert np.isclose((lim - c[2]) / (lim - c[1]), 2 ** (4 * (1 - 1 / g)), rtol=0.01)


def test_a6_even_f_reduces_by_gcd():
    g = 1.75
    a = 1 / g
    n = 2**20
    assert np.isclose(centroid_1d(_sine(2, n, g)) / n ** (1 - a), 2**a * _k_limit(g, 1), rtol=0.01)


@pytest.mark.parametrize("n", [128, 1000, 4096])
def test_a6_gamma_one_constant(n):
    assert np.isclose(centroid_1d(_sine(5, n, 1.0)), 5.0)


def test_a6_gamma_to_one_limit_is_f():
    assert np.isclose(_k_limit(1.01, 5), 5, rtol=0.05)


@pytest.mark.parametrize("g", [1.75, 2.6])
def test_a2_slope_bounds(g):
    a = 1 / g
    for n in (128, 1024, 8192):
        h = 1 / n
        for ph in np.linspace(0, 1, 7):
            z = _sine(1, n, g, ph)
            d = np.abs(np.roll(z, -1) - np.roll(z, 1)).max() / (2 * h)
            # |F'(x0)| = 2 pi、||F'|| = 2 pi
            assert (2 * np.pi / 4) ** a <= d * h ** (1 - a) <= (2 * np.pi) ** a + 1e-9


@pytest.mark.parametrize("g", [1.75, 2.6])
@pytest.mark.parametrize("eps", [0.01, 0.05, 0.2])
def test_a2_smoothed_transform(g, eps):
    a = 1 / g
    u = np.linspace(-1, 1, 400_001)
    y = t_gamma_eps(u, g, eps)
    assert np.all(np.diff(y) > 0)
    assert np.isclose(np.gradient(y, u).max(), eps ** (a - 1) * (1 + eps**2) ** ((1 - a) / 2), rtol=1e-3)
    assert np.abs(y - t_gamma(u, g)).max() <= eps**a
    assert np.all(np.abs(y) <= np.abs(t_gamma(u, g)) + 1e-15)


def test_a3_grid_sigma_monotone_in_gamma():
    s = [np.mean(_sine(5, 128, g) ** 2) for g in (0.9, 1.0, 1.75, 2.6)]
    assert np.all(np.diff(s) > 0)
    assert np.isclose(np.mean(_sine(5, 128, 1.75)), 0, atol=1e-12)  # 格子の上でも対称


KAPPA0 = np.pi * quad(lambda t: t / np.sin(np.pi * t) if t > 0 else 1 / np.pi, 0, 0.5)[0]


def test_a7_noninteger_f_n_over_log_n():
    catalan = sum((-1) ** k / (2 * k + 1) ** 2 for k in range(200_000))  # DLMF 25.11.40
    assert np.isclose(KAPPA0, 2 * catalan / np.pi, rtol=1e-9)  # 付録 A 系 A.7.1 の前の恒等式
    r = []
    for n in (2**12, 2**16, 2**20):
        z = np.sin(2 * np.pi * 5.3 * np.arange(n) / n)
        r.append(centroid_1d(z) * np.log(n) / n)
    assert np.all(np.diff(r) > 0) and r[-1] < KAPPA0


def test_a7_zero_jump_grows_like_log():
    # f = 5.5, phi = 0 は J = 0（端で値はつながり、傾きだけが跳ぶ）
    c = [centroid_1d(np.sin(2 * np.pi * 5.5 * np.arange(n) / n)) for n in (2**12, 2**16, 2**20)]
    assert np.all(np.diff(c) > 0) and c[-1] < 2 * c[0]


@pytest.mark.parametrize("g", [0.9, 0.5])
def test_a6_cstar_closed_form(g):
    # 注意 A.6.2: 1 < alpha < 3 で C* = 4 alpha / (3 alpha - 1)、D = Gamma(a/2) / (sqrt(pi) Gamma((a+1)/2))
    a = 1 / g
    assert np.isclose(_cstar(g), 4 * a / (3 * a - 1), rtol=1e-9)
    d_closed = Gamma_fn(a / 2) / (np.sqrt(np.pi) * Gamma_fn((a + 1) / 2))
    assert np.isclose(_d_gamma(g), d_closed, rtol=1e-7)
    assert np.isclose(fourier_coeff_odd(1, g) / d_closed, 2 * a / (a + 1))


def test_a6_even_f_limit_depends_on_gcd():
    # f = 6: d = gcd(f, N) ごとに極限が分かれる（d = 2 と d = 6、どちらも N/d は偶数）
    g = 1.75
    a = 1 / g
    for n, d in ((1048576, 2), (1048572, 6)):
        assert np.gcd(6, n) == d and (n // d) % 2 == 0
        assert np.isclose(centroid_1d(_sine(6, n, g)) / n ** (1 - a), d**a * _k_limit(g, 6 // d), rtol=0.01)
