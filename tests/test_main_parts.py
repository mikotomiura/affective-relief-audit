"""Tests of the components added for the main computations (K4 in two dimensions, the paired edge-and-grid comparison
and validation 3). Names refer to clauses of experiments/spec/generator-and-descriptors.md where one applies."""

from __future__ import annotations

import numpy as np
import pytest

from atact.descriptors import (
    centroid,
    centroid_1d,
    centroid_power,
    spectral_centroids,
    spectral_centroids_1d,
    windowed_1d,
)
from atact.field import (
    RenderConfig,
    procedural_field,
    procedural_field_separable,
    sine_1d,
    tone_amplitude_for_rms_slope,
    tone_surface,
)
from atact.measured import central_crop, largest_pow2, unit_factor
from atact.spectral import centroid_band, decimate_fourier, windowed
from atact.stats import (
    bonferroni_level,
    flips_relative,
    flips_seeded,
    kendall_tau,
    local_slopes,
    log_corrected_fit,
    slopes_per_seed,
    t_interval,
)
from atact.transform import t_gamma


@pytest.mark.parametrize("f,octaves,norm,x0,y0", [(5.5, 4, "maxabs", 0.0, 0.0), (3.0, 1, "maxabs", 0.0, 0.0),
                                                  (6.3, 4, "ampsum", 0.13, 0.29), (5.0, 4, "none", 0.77, 0.53)])
def test_s1_separable_generator_equals_procedural_field_exactly(f, octaves, norm, x0, y0):
    a = procedural_field_separable(f, 96, 7, octaves, x0, y0, norm)
    b = procedural_field(f, RenderConfig(n=96, octaves=octaves, normalize=norm, x0=x0, y0=y0), 7)
    np.testing.assert_array_equal(a, b)


def test_s1_3_separable_generator_draws_phi_then_psi():
    # The x factor takes the first draw: swapping x and y must change the field for non-symmetric phases
    a = procedural_field_separable(5.0, 32, 3, 1, normalize="none")
    rng = np.random.default_rng(3)
    phi, psi = rng.uniform(0, 2 * np.pi, 2)
    x = np.arange(32) / 32
    np.testing.assert_allclose(a, np.outer(np.sin(2 * np.pi * 5 * x + psi), np.sin(2 * np.pi * 5 * x + phi)), atol=1e-14)


def test_oned_field_phase_from_seed():
    rng = np.random.default_rng(11)
    phi = rng.uniform(0, 2 * np.pi)
    x = np.arange(64) / 64
    np.testing.assert_array_equal(sine_1d(3.5, 64, 11), np.sin(2 * np.pi * 3.5 * x + phi))


def test_s2_3_s2_4_spectral_centroids_agree_with_single_descriptors():
    H = t_gamma(procedural_field_separable(5.5, 128, 2), 1.75)
    c = spectral_centroids(H, 32.0)
    assert c["centroid_amp"] == pytest.approx(centroid(H), rel=1e-12)
    assert c["centroid_power"] == pytest.approx(centroid_power(H), rel=1e-12)
    assert c["centroid_band_power"] == pytest.approx(centroid_band(H, 32.0, "power"), rel=1e-12)
    X = windowed(H)
    assert spectral_centroids(X, 32.0)["centroid_amp"] == pytest.approx(centroid(X), rel=1e-12)
    with pytest.raises(ValueError):
        spectral_centroids(H, 65.0)


def test_s2_7_one_dimensional_centroids():
    z = t_gamma(sine_1d(5.5, 256, 4), 2.6)
    c = spectral_centroids_1d(z, 32.0)
    assert c["centroid_amp"] == pytest.approx(centroid_1d(z), rel=1e-12)
    x = np.arange(256) / 256
    tone = np.cos(2 * np.pi * 9 * x) + 0.5 * np.cos(2 * np.pi * 40 * x)
    c = spectral_centroids_1d(tone, 32.0)
    assert c["centroid_band_power"] == pytest.approx(9.0)
    assert spectral_centroids_1d(tone, 9.0)["centroid_band_power"] == pytest.approx(9.0)  # the band includes K
    assert c["centroid_power"] == pytest.approx((9 + 40 * 0.25) / 1.25)
    w = windowed_1d(tone)
    assert abs(w.mean()) < 1e-12 and w[0] == pytest.approx(0.0, abs=1e-12)


def test_s3_1_one_dimensional_window_matches_two_dimensional_row():
    # The 2-D window is the outer product of the 1-D window with itself
    from atact.descriptors import hann_1d
    from atact.spectral import hann2d

    np.testing.assert_allclose(hann2d(64), np.outer(hann_1d(64), hann_1d(64)), atol=1e-15)


def test_s4_decimation_from_fine_grid_agrees_with_direct_for_bandlimited():
    # gamma = 1, integer f, highest frequency 3 * 8 = 24 < 32: generating at 4N and decimating equals direct sampling
    fine = procedural_field_separable(3.0, 256, 5, normalize="ampsum")
    np.testing.assert_allclose(decimate_fourier(fine, 64), procedural_field_separable(3.0, 64, 5, normalize="ampsum"),
                               atol=1e-12)


def test_s6_1_slopes_and_interval():
    N = np.array([128, 256, 512, 1024])
    C = np.vstack([3.0 * N**0.7, 2.0 * N**0.5])
    np.testing.assert_allclose(slopes_per_seed(N, C), [0.7, 0.5])
    np.testing.assert_allclose(local_slopes(N, C), [[0.7] * 3, [0.5] * 3])
    t = t_interval([0.7, 0.5, 0.6], 0.95)
    assert t["mean"] == pytest.approx(0.6)
    # t quantile with 2 degrees of freedom at 97.5% is 4.302653
    assert t["hi"] - t["mean"] == pytest.approx(4.302653 * 0.1 / np.sqrt(3), rel=1e-6)
    assert bonferroni_level(12) == pytest.approx(1 - 0.05 / 12)
    wide = t_interval([0.7, 0.5, 0.6], bonferroni_level(12))
    assert wide["hi"] > t["hi"]


def test_log_corrected_fit_recovers_coefficients():
    N = np.array([256, 512, 1024, 2048, 4096], dtype=float)
    C = np.exp(0.3 + 1.0 * np.log(N) - 1.0 * np.log(np.log(N)))[None, :]
    np.testing.assert_allclose(log_corrected_fit(N, C)[0], [0.3, 1.0, -1.0], atol=1e-9)


def test_s6_2_flip_with_seeds():
    rng = np.random.default_rng(0)
    noise = 0.01 * rng.normal(size=(3, 10))
    Xg = np.array([[1.0], [2.0], [3.0]]) + noise
    Xh = np.array([[2.0], [1.0], [3.0]]) + noise
    f = flips_seeded(Xg, Xh, labels=["a", "b", "c"])
    assert [(d["a"], d["b"]) for d in f] == [("a", "b")]
    # A sign change within noise is not a flip
    Xh2 = np.array([[2.0], [2.0 + 1e-4], [3.0]]) + noise
    assert flips_seeded(Xg, Xh2) == []
    # Deterministic surfaces (standard error 0): any change of sign with a non-zero difference is a flip
    assert len(flips_seeded(np.array([[1.0, 1.0], [2.0, 2.0]]), np.array([[2.0, 2.0], [1.0, 1.0]]))) == 1


def test_s6_2_flip_relative_threshold():
    xg, xh = np.array([1.0, 1.2]), np.array([1.2, 1.0])
    assert len(flips_relative(xg, xh, 0.05)) == 1
    assert flips_relative(np.array([1.0, 1.04]), np.array([1.04, 1.0]), 0.05) == []
    assert flips_relative(xg, xh, 0.05, pairs=[]) == []
    # The threshold must be exceeded at both levels
    assert flips_relative(np.array([1.0, 1.2]), np.array([1.03, 1.0]), 0.05) == []
    assert flips_relative(np.array([1.0, 1.03]), np.array([1.2, 1.0]), 0.05) == []


def test_kendall_tau():
    assert kendall_tau([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert kendall_tau([1, 2, 3, 4], [40, 30, 20, 10]) == pytest.approx(-1.0)


def test_flip_positive_tones_have_requested_rms_slope():
    freqs, ratios = (6, 96), (1.0, 0.15)
    c = tone_amplitude_for_rms_slope(freqs, ratios, 0.01)
    x = np.arange(4096) / 4096
    gx = sum(c * r * 2 * np.pi * k * np.cos(2 * np.pi * k * x) for k, r in zip(freqs, ratios))  # exact derivative
    assert np.sqrt(np.mean(gx**2)) == pytest.approx(0.01, rel=1e-12)
    z = tone_surface(freqs, [c * r for r in ratios], 4096)
    np.testing.assert_allclose(z[0], sum(c * r * np.sin(2 * np.pi * k * x) for k, r in zip(freqs, ratios)), atol=1e-15)
    # The crop offset shifts all tones together (periodic, integer frequencies)
    np.testing.assert_allclose(tone_surface(freqs, [1, 1], 64, x0=0.125), np.roll(tone_surface(freqs, [1, 1], 64), -8, axis=1),
                               atol=1e-12)


def test_s5_1_units():
    assert unit_factor(b"m") == 1.0 and unit_factor("nm") == 1e-9 and unit_factor(b"pm") == 1e-12
    with pytest.raises(ValueError):
        unit_factor("inch")


def test_s5_2_crop_size_and_position():
    assert largest_pow2(768) == 512 and largest_pow2(1232) == 1024 and largest_pow2(512) == 512
    a = np.arange(10 * 7).reshape(10, 7)
    np.testing.assert_array_equal(central_crop(a, 4), a[3:7, 1:5])


def test_s2_8_float_normals_encode_to_the_uint8_map():
    from atact.hfratio import normal_from_height, normal_rgb_from_height

    z = 0.01 * t_gamma(procedural_field_separable(5.5, 128, 3, normalize="ampsum"), 1.75)
    v = normal_from_height(z)
    np.testing.assert_array_equal(np.round((v + 1.0) / 2.0 * 255).astype(np.uint8), normal_rgb_from_height(z))
    np.testing.assert_allclose(np.linalg.norm(v, axis=-1), 1.0, atol=1e-12)


def test_s3_1_float_windowed_normals_match_uint8_up_to_rounding():
    from atact.hfratio import normal_from_height, normal_rgb_from_height
    from atact.spectral import windowed_normals, windowed_normals_float

    z = 0.01 * t_gamma(procedural_field_separable(5.5, 128, 3, normalize="ampsum"), 1.75)
    a = windowed_normals(normal_rgb_from_height(z)).astype(float) / 255 * 2 - 1
    b = windowed_normals_float(normal_from_height(z))
    assert np.abs(a - b).max() < 3 / 255
    flat = np.zeros((16, 16, 3))
    flat[..., 2] = 1.0
    np.testing.assert_array_equal(windowed_normals_float(flat), flat)
