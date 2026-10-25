"""Parts of experiments/v3_reduction_supplement.py: the two band-limits, the mirror reduction and the decomposition."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

from atact.spectral import decimate_fourier

spec = importlib.util.spec_from_file_location(
    "v3_reduction_supplement", Path(__file__).resolve().parents[1] / "experiments" / "v3_reduction_supplement.py")
sup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sup)


def test_periodic_bandlimit_sampled_equals_decimate_fourier():
    Z = np.random.default_rng(1).normal(size=(64, 64))
    for n in (32, 16):
        r = 64 // n
        assert np.allclose(sup.bandlimit_periodic(Z, n)[::r, ::r], decimate_fourier(Z, n), atol=1e-12)


def test_mirror_bandlimit_keeps_even_tones_inside_the_band_and_removes_those_outside():
    P, n = 64, 16
    x = (np.arange(P) + 0.5) / P
    inside = np.outer(np.cos(np.pi * 12 * x), np.cos(np.pi * 3 * x))  # 12 and 3 cycles per 2P: inside [-n, n)
    outside = np.outer(np.cos(np.pi * 20 * x), np.ones(P))  # 20 cycles per 2P: outside
    assert np.allclose(sup.bandlimit_mirror(inside, n), inside, atol=1e-12)
    assert np.allclose(sup.bandlimit_mirror(outside, n), 0, atol=1e-12)


def test_mirror_bandlimit_has_no_boundary_ringing_on_a_ramp():
    P, n = 128, 32
    Z = np.tile(np.linspace(0.0, 1.0, P), (P, 1))  # non-periodic: a jump of 1 at the periodic boundary
    err_mirror = np.abs(sup.bandlimit_mirror(Z, n) - Z).max()
    err_periodic = np.abs(sup.bandlimit_periodic(Z, n) - Z).max()
    assert err_periodic > 0.3
    assert err_mirror < 0.05


def test_reduce_full_level_is_identity_and_mirror_level_matches_its_bandlimit():
    Z = np.random.default_rng(2).normal(size=(32, 32))
    for m in sup.REDUCTIONS:
        assert sup.reduce(Z, 32, m) is Z
    assert np.allclose(sup.reduce(Z, 8, "mirror"), sup.bandlimit_mirror(Z, 8)[::4, ::4])
    assert np.array_equal(sup.reduce(Z, 8, "subsample"), Z[::4, ::4])


def test_decomposition_terms_sum_to_total_and_s3_is_the_reduced_value():
    # a red-spectrum field on P = 256, so that the high-pass widths of the phys and px cutoffs differ by several bins
    rng = np.random.default_rng(3)
    P, n = 256, 64
    k = np.fft.fftfreq(P) * P
    amp = 1.0 / (1.0 + np.hypot(k[None, :], k[:, None])) ** 2
    Z = np.real(np.fft.ifft2(amp * np.exp(2j * np.pi * rng.random((P, P))))) * 1e-1
    L = 1.0
    for band, method in ((sup.bandlimit_periodic, "decimate_fourier"), (sup.bandlimit_mirror, "mirror")):
        d = sup.decomposition(Z, L, n, band)
        assert np.isclose(d["content"] + d["sampling"] + d["differences"], d["total"])
        assert abs(d["sampling"]) < 1e-3  # nearly linear normals of a band-limited height: sampling is exact
        direct = sup.descriptors(sup.reduce(Z, n, method), L, P)["hf_ratio_phys_float"]
        assert np.isclose(d["s"][3], direct, atol=1e-6)
