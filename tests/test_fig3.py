"""Tests of the Fig. 3 fingerprint (atact.fig3).

1. Check by recomputation: from a known pattern rendered in the same way (gist_earth + soft-light shading + nearest-neighbour enlargement),
   the height and the fingerprint are recovered.
2. Actual figure: if source/media/image3.png exists, pin the 256 x 256 grid, the colour error and the three fingerprints.
   The preprint is outside git, so the tests are skipped if it is absent.
"""

import numpy as np
import pytest

from atact import fig3
from atact.fig3 import block_grid, dominant_cycles, fingerprint, harmonic3, soft_light_inverse, speckle

N = 256
Y, X = np.mgrid[0:N, 0:N] / N


def _shade(Z):
    import matplotlib
    from matplotlib.colors import LightSource

    return LightSource(azdeg=315, altdeg=45).shade(Z, cmap=matplotlib.colormaps["gist_earth"], blend_mode="soft")[..., :3]


def _mm(Z):
    return (Z - Z.min()) / (Z.max() - Z.min())


def _tone(f):
    return np.sin(2 * np.pi * f * X) * np.sin(2 * np.pi * f * Y)


def _square(f):
    return np.sign(np.sin(2 * np.pi * f * X + 0.3)) * np.sign(np.sin(2 * np.pi * f * Y + 0.3))


def _noisy(f, a=0.2):
    return _tone(f) + a * np.random.default_rng(0).uniform(-1, 1, (N, N))


# ---------------------------------------------------------------- 1. Check by recomputation


@pytest.mark.parametrize("Z", [_tone(1.5), _tone(6), _noisy(6)], ids=["tone1.5", "tone6", "noisy6"])
def test_soft_light_inverse_recovers_height(Z):
    c, I, err = soft_light_inverse(_shade(Z))
    assert err.max() < 1e-6
    assert np.abs(c / 255 - _mm(Z)).max() < 1 / 255 + 1e-9  # within the 256-level quantisation


def test_block_grid_roundtrip():
    G = _shade(_noisy(6))
    idx = (np.arange(1872) * N / 1872).astype(int)
    assert np.array_equal(block_grid(G[np.ix_(idx, idx)]), G)


def test_block_grid_refuses_flat_pattern():
    G = _shade(_square(6))
    idx = (np.arange(1872) * N / 1872).astype(int)
    with pytest.raises(ValueError):
        block_grid(G[np.ix_(idx, idx)])


@pytest.mark.parametrize("f", [1.5, 1.6, 6.0, 6.4])
def test_dominant_cycles_pure_tone(f):
    assert dominant_cycles(_tone(f), 1, step=0.01) == pytest.approx(f, abs=0.011)
    assert dominant_cycles(_tone(f), 0, step=0.01) == pytest.approx(f, abs=0.011)


def test_harmonic3_sine_vs_square():
    assert harmonic3(_tone(6), 6.0) < 0.01
    assert harmonic3(_square(6), 6.0) == pytest.approx(1 / 3, abs=0.01)


def test_speckle_separates_noise_from_edges():
    assert speckle(_mm(_tone(6))) < 0.02    # a smooth bend of 6 cycles gives 0.008
    assert speckle(_mm(_square(6))) < 0.004   # edges alone do not raise it
    assert speckle(_mm(_noisy(6))) > 0.05


def test_fingerprint_distance_zero_to_self():
    fp = fingerprint(_noisy(6))
    assert fig3.distance(fp, fp) == 0.0
    assert fig3.distance(fingerprint(_tone(1.5)), fp) > 1.0


# ---------------------------------------------------------------- 2. Actual figure

needs_fig = pytest.mark.skipif(not fig3.FIG3.exists(), reason="Fig. 3 of the preprint is not redistributed with the repository")


@pytest.fixture(scope="module")
def real():
    return fig3.panels()


@needs_fig
def test_real_grid_is_256_and_fits_soft_light(real):
    for name, d in real.items():
        assert d["height"].shape == (256, 256), name
        assert 255 * d["err"].max() < 2.0, name  # colour error below 2/255


# Values measured on 2026-10-24 (on the height recovered from Fig. 3)
REAL_FP = {
    "calm": {"cycles_x": 1.6, "cycles_y": 1.6, "harmonic3": (0.0, 0.03), "speckle": (0.0, 0.006)},
    "anger": {"cycles_x": 6.4, "cycles_y": 6.4, "harmonic3": (0.15, 0.25), "speckle": (0.1, 0.16)},
    "complex": {"cycles_x": 4.85, "cycles_y": 1.7, "harmonic3": (0.3, 0.5), "speckle": (0.0, 0.006)},
}


@needs_fig
@pytest.mark.parametrize("name", list(REAL_FP))
def test_real_fingerprint(real, name):
    fp = fingerprint(real[name]["height"])
    want = REAL_FP[name]
    assert fp["cycles_x"] == pytest.approx(want["cycles_x"], abs=0.051)
    assert fp["cycles_y"] == pytest.approx(want["cycles_y"], abs=0.051)
    lo, hi = want["harmonic3"]
    assert lo <= fp["harmonic3"] <= hi
    lo, hi = want["speckle"]
    assert lo <= fp["speckle"] <= hi
