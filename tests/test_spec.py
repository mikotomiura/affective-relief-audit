"""Checks, clause by clause, that the code agrees with the specification experiments/spec/generator-and-descriptors.md (the English version is authoritative).

Test names such as s1_2 refer to clause numbers of the specification.
"""

from __future__ import annotations

import numpy as np
import pytest

from atact.descriptors import centroid, centroid_power, radial_frequency, rq
from atact.field import RenderConfig, height, procedural_field
from atact.mapping import params
from atact.spectral import (
    centroid_band,
    decimate_fourier,
    decimate_normals,
    hann2d,
    periodic_component,
    remove_plane,
    subsample,
    windowed,
    windowed_normals,
)
from atact.transform import t_gamma


def _explicit(f, n, seed, octaves=4, x0=0.0, y0=0.0):
    """S1.1-S1.3 written out literally as in the specification."""
    rng = np.random.default_rng(seed)
    x = x0 + np.arange(n) / n
    y = y0 + np.arange(n) / n
    X, Y = np.meshgrid(x, y)  # [j, i]; rows run along y
    F = np.zeros((n, n))
    for o in range(octaves):
        phi, psi = rng.uniform(0, 2 * np.pi, 2)
        fo = f * 2**o
        F += 2.0**-o * np.sin(2 * np.pi * fo * X + phi) * np.sin(2 * np.pi * fo * Y + psi)
    return F


@pytest.mark.parametrize("f,seed", [(5.5, 7), (3.0, 1), (6.3, 42)])
def test_s1_2_s1_3_field_matches_formula(f, seed):
    F = procedural_field(f, RenderConfig(n=64, normalize="none"), seed)
    np.testing.assert_allclose(F, _explicit(f, 64, seed), atol=1e-12)


def test_s1_1_window_shift_is_same_infinite_field():
    cfg = RenderConfig(n=64, normalize="none", x0=0.3, y0=0.7)
    np.testing.assert_allclose(procedural_field(5.5, cfg, 3), _explicit(5.5, 64, 3, x0=0.3, y0=0.7), atol=1e-12)
    # For integer f, a window shifted by N/4 pixels coincides with a cyclic shift of the array
    a = procedural_field(5.0, RenderConfig(n=64, normalize="none"), 3)
    b = procedural_field(5.0, RenderConfig(n=64, normalize="none", x0=0.25), 3)
    np.testing.assert_allclose(b, np.roll(a, -16, axis=1), atol=1e-12)


def test_s1_4_normalisations():
    raw = procedural_field(5.5, RenderConfig(n=64, normalize="none"), 2)
    mx = procedural_field(5.5, RenderConfig(n=64, normalize="maxabs"), 2)
    am = procedural_field(5.5, RenderConfig(n=64, normalize="ampsum"), 2)
    assert np.abs(mx).max() == pytest.approx(1.0)
    np.testing.assert_allclose(am, raw / 1.875, atol=1e-12)
    # The centroid is independent of normalisation by homogeneity of T_gamma
    for g in (0.9, 1.75):
        assert centroid(t_gamma(mx, g)) == pytest.approx(centroid(t_gamma(am, g)), rel=1e-9)


def test_s1_4_ampsum_same_surface_across_grids():
    a = procedural_field(5.5, RenderConfig(n=128, normalize="ampsum"), 4)
    b = procedural_field(5.5, RenderConfig(n=256, normalize="ampsum"), 4)
    np.testing.assert_allclose(a, b[::2, ::2], atol=1e-12)


@pytest.mark.parametrize("f,periodic", [(5.0, True), (3.0, True), (5.5, False), (6.3, False)])
def test_s1_6_periodic_iff_integer_f(f, periodic):
    left = procedural_field(f, RenderConfig(n=64, normalize="none"), 9)[:, 0]
    right = procedural_field(f, RenderConfig(n=64, normalize="none", x0=1.0), 9)[:, 0]
    assert np.allclose(left, right, atol=1e-9) == periodic


def test_s2_1_rule():
    f, s, g = params(0.2, -0.4)
    p, q = 0.3, 0.4
    assert (f, s, g) == pytest.approx((3 + 4 * p, 0.06 + 0.24 * q, 0.9 + 1.7 * (0.65 * p + 0.35 * q)))


def test_s2_2_height_is_s_tgamma_f():
    cfg = RenderConfig(n=64)
    f, s, g = params(-0.5, 0.5)
    H = height(-0.5, 0.5, cfg, seed=5)
    np.testing.assert_allclose(H, s * t_gamma(procedural_field(float(f), cfg, 5), g), atol=1e-12)


def test_s2_3_centroid_matches_formula():
    H = t_gamma(procedural_field(5.5, RenderConfig(n=64), 1), 1.75)
    Hc = H - H.mean()
    mag = np.abs(np.fft.fft2(Hc))
    k = np.fft.fftfreq(64) * 64
    assert k.min() == -32 and k.max() == 31  # each component lies in [-N/2, N/2)
    rho = np.hypot(*np.meshgrid(k, k))
    assert centroid(H) == pytest.approx((rho * mag).sum() / mag.sum(), rel=1e-12)
    # The centroid of a pure tone equals its frequency (cycles per domain)
    x = np.arange(64) / 64
    tone = np.tile(np.cos(2 * np.pi * 5 * x), (64, 1))
    assert centroid(tone) == pytest.approx(5.0)
    # The mean has no effect (DC is removed)
    assert centroid(H + 3.0) == pytest.approx(centroid(H), rel=1e-12)


def test_s2_4_band_fixed_is_grid_invariant_for_periodic_bandlimited():
    # Proposition 8, part 1: independent of the grid under (C1)-(C3). For f = 3 and 4 octaves the highest is 24 cycles
    vals = []
    for n in (128, 256, 512):
        F = procedural_field(3.0, RenderConfig(n=n, normalize="ampsum"), 2)
        vals.append([centroid_band(F, 40.0, w) for w in ("power", "amp")])
    np.testing.assert_allclose(vals[0], vals[1], rtol=1e-9)
    np.testing.assert_allclose(vals[0], vals[2], rtol=1e-9)


def test_s2_4_band_fixed_matches_power_centroid_when_band_covers_all():
    F = procedural_field(3.0, RenderConfig(n=128, octaves=2), 2)
    assert centroid_band(F, 64.0, "power") == pytest.approx(centroid_power(F), rel=1e-9)
    with pytest.raises(ValueError):
        centroid_band(F, 65.0)


def test_s2_5_sq():
    H = np.array([[1.0, 3.0], [1.0, 3.0]])
    assert rq(H) == pytest.approx(1.0)


def test_s3_1_window():
    W = hann2d(64)
    assert W[0].max() == 0 and W[:, 0].max() == 0
    assert W[32, 32] == pytest.approx(1.0)
    X = windowed(procedural_field(5.5, RenderConfig(n=64), 1))
    assert abs(X.mean()) < 1e-12
    flat = np.full((32, 32, 3), [128, 128, 255], dtype=np.uint8)
    np.testing.assert_array_equal(windowed_normals(flat), flat)


def test_s3_2_periodic_component():
    # For a periodic field, the difference between the two ends of the array is only a one-pixel difference, and s shrinks to 0 with N.
    # For a non-periodic field the edge discontinuity remains and s does not shrink
    smooth = lambda f, n: np.abs((Z := procedural_field(f, RenderConfig(n=n), 1)) - periodic_component(Z)).max()
    assert smooth(5.0, 1024) < smooth(5.0, 256) / 2  # only the shrinkage is checked (no rate is claimed)
    assert smooth(5.5, 1024) > 0.2
    F = procedural_field(5.0, RenderConfig(n=64), 1)
    # For a non-periodic field, the edge discontinuity of the periodic component is smaller than that of the original
    G = procedural_field(5.5, RenderConfig(n=64), 1)
    P = periodic_component(G)
    jump = lambda Z: np.abs(Z[:, 0] - Z[:, -1]).mean() + np.abs(Z[0] - Z[-1]).mean()
    assert jump(P) < 0.5 * jump(G)
    # The decomposition is linear: s(G + F) = s(G) + s(F)
    s_ = lambda Z: Z - periodic_component(Z)
    np.testing.assert_allclose(s_(G + F), s_(G) + s_(F), atol=1e-10)


def test_s4_decimate_matches_direct_sampling_for_bandlimited_periodic():
    # Proposition 8, part 5: for a periodic band-limited field, generating on a fine grid, band-limiting and decimating agrees with direct sampling
    fine = procedural_field(3.0, RenderConfig(n=256, normalize="ampsum", octaves=3), 6)
    coarse = procedural_field(3.0, RenderConfig(n=64, normalize="ampsum", octaves=3), 6)
    np.testing.assert_allclose(decimate_fourier(fine, 64), coarse, atol=1e-10)
    np.testing.assert_allclose(subsample(fine, 64), coarse, atol=1e-12)


def test_s4_decimate_removes_alias_that_subsample_keeps():
    # After T_gamma the field is not band-limited, so band-limited decimation differs from taking every other sample
    fine = t_gamma(procedural_field(5.0, RenderConfig(n=256, normalize="ampsum"), 6), 2.6)
    a = decimate_fourier(fine, 64)
    b = subsample(fine, 64)
    assert np.abs(a - b).max() > 1e-3
    # The band-limited version has no energy outside [-N/2, N/2) (it is unchanged when regenerated)
    np.testing.assert_allclose(decimate_fourier(a, 64), a, atol=1e-12)


def test_s5_2_remove_plane():
    y, x = np.mgrid[0:32, 0:32]
    Z = 0.5 + 0.1 * x - 0.3 * y
    np.testing.assert_allclose(remove_plane(Z), 0.0, atol=1e-10)
    rng = np.random.default_rng(0)
    R = rng.normal(size=(32, 32))
    np.testing.assert_allclose(remove_plane(Z + R), remove_plane(R), atol=1e-10)


def test_s5_4_decimate_normals_keeps_flat_and_shape():
    flat = np.full((240, 240, 4), [128, 128, 255, 255], dtype=np.uint8)
    out = decimate_normals(flat, 120)
    assert out.shape == (120, 120, 3)
    np.testing.assert_array_equal(out, flat[:120, :120, :3])


def test_radial_frequency_is_euclidean():
    r = radial_frequency(8)
    assert r[0, 0] == 0 and r[3, 4] == pytest.approx(5.0)


def test_s2_4_band_includes_its_edge():
    # The band is 0 < rho <= K (including bins exactly at K)
    x = np.arange(64) / 64
    tone = np.tile(np.cos(2 * np.pi * 5 * x), (64, 1)) + 0.5 * np.tile(np.cos(2 * np.pi * 9 * x), (64, 1))
    assert centroid_band(tone, 5.0, "power") == pytest.approx(5.0)
    assert centroid_band(tone, 9.0, "amp") == pytest.approx((5 * 1 + 9 * 0.5) / 1.5)


def test_s2_9_float_variant_matches_uint8_up_to_rounding():
    from atact.hfratio import hf_ratio, hf_ratio_float

    z = 0.01 * t_gamma(procedural_field(5.5, RenderConfig(n=256, normalize="ampsum"), 3), 1.75)
    dzdy, dzdx = np.gradient(z, 1 / 256)
    v = np.stack([-dzdx, dzdy, np.ones_like(z)], axis=-1)
    v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    rgb = np.round((v + 1) / 2 * 255).astype(np.uint8)
    a, b = hf_ratio(rgb, 120), hf_ratio_float(v, 120)
    assert b == pytest.approx(a, abs=0.02)  # differ only by uint8 rounding
    flat = np.zeros((32, 32, 3))
    flat[..., 2] = 1.0
    assert hf_ratio_float(flat) == 0.0


def test_s2_9_linear_variant_pixel_cutoff_decreases_with_grid():
    # Proposition 8, part 3: with a pixel-fixed cutoff the ratio does not increase with N;
    # with a physically fixed cutoff it is grid-independent for a periodic band-limited field
    from atact.spectral import linear_hf_ratio

    vals_px, vals_ph = [], []
    for n in (128, 256, 512):
        z = procedural_field(3.0, RenderConfig(n=n, normalize="ampsum", octaves=3), 2)
        vals_px.append(linear_hf_ratio(z, 120))
        vals_ph.append(linear_hf_ratio(z, 120 * n / 256))
    assert vals_px[0] > vals_px[1] > vals_px[2]
    np.testing.assert_allclose(vals_ph, vals_ph[0], rtol=1e-3)
