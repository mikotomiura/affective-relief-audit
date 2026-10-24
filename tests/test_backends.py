"""Tests of the generator back-end interface (atact.backends) and of the generator variants (the A1 variations).

1. Plumbing: with a fake adapter that merely wraps the reconstruction, the interface leaves results unchanged.
2. Conformance: the same contract is imposed on the reconstruction and on the original code (if an adapter exists).
   A failure of the original code is a finding of disagreement between eqs. (1)-(4) of Harada (2026) and its implementation.
3. Default pinned: adding variants does not change a single bit of the default generator output.
4. Per-variant properties: freq_unit, octave_form and noise each have their intended effect.
"""

import hashlib
import textwrap

import numpy as np
import pytest

from atact import backends
from atact.backends import AdapterBackend, ReconBackend, load_adapter
from atact.classify import DatasetConfig, make_dataset
from atact.descriptors import centroid, max_gradient, radial_frequency, rq
from atact.field import RenderConfig, height, minmax, procedural_field
from atact.mapping import params
from atact.transform import t_gamma

# Table 1 of Harada (2026)
TABLE1 = [
    ((1, -1), (3.0, 0.06, 0.9)),
    ((-1, -1), (3.0, 0.30, 1.495)),
    ((1, 1), (7.0, 0.06, 2.005)),
    ((-1, 1), (7.0, 0.30, 2.6)),
    ((0, 0), (5.0, 0.18, 1.75)),
]

FAKE_ADAPTER = textwrap.dedent(
    '''
    """Fake adapter that merely wraps the reconstruction (for testing the plumbing)."""
    from atact.field import RenderConfig, height as _height, procedural_field

    NAME = "fake"

    def height(V, A, seed=42):
        return _height(V, A, RenderConfig(), seed)

    def field(f, seed=42, n=128):
        return procedural_field(float(f), RenderConfig(n=n), seed)
    '''
)


@pytest.fixture
def fake(tmp_path):
    p = tmp_path / "fake_adapter.py"
    p.write_text(FAKE_ADAPTER)
    return load_adapter(p)


# ---------------------------------------------------------------- 1. Plumbing


def test_fake_adapter_matches_builtin_dataset(fake):
    cfg = DatasetConfig(per_class=6, jitter=0.5)
    X0, y0, va0 = make_dataset(cfg)
    X1, y1, va1 = make_dataset(cfg, backend=fake)
    assert np.array_equal(X0, X1)
    assert np.array_equal(y0, y1)
    assert np.array_equal(va0, va1)


def test_backend_is_actually_used(tmp_path):
    # A fake adapter identical to the reconstruction would pass the check above even if backend were ignored; check with a version whose height is doubled
    p = tmp_path / "double.py"
    p.write_text(FAKE_ADAPTER.replace("return _height(V, A, RenderConfig(), seed)",
                                      "return 2 * _height(V, A, RenderConfig(), seed)"))
    cfg = DatasetConfig(per_class=3)
    X0, _, _ = make_dataset(cfg)
    X2, _, _ = make_dataset(cfg, backend=load_adapter(p))
    assert np.allclose(X2[:, 0], 2 * X0[:, 0])  # Rq doubles
    assert np.allclose(X2[:, 1], X0[:, 1])      # the centroid is independent of the scale factor


def test_missing_optional_functions_are_none(fake):
    assert fake.NAME == "fake"
    assert fake.params(0, 0) is None
    assert fake.features(np.zeros((4, 4))) is None
    assert fake.dataset() is None
    assert fake.field(5.0).shape == (128, 128)
    assert fake.field(5.0, n=64).shape == (64, 64)


def test_adapter_without_height_is_rejected(tmp_path):
    p = tmp_path / "bad.py"
    p.write_text("NAME = 'bad'\n")
    with pytest.raises(AttributeError):
        load_adapter(p)


def test_features_hook_replaces_descriptors(fake):
    cfg = DatasetConfig(per_class=3)
    X, _, _ = make_dataset(cfg, backend=fake, features=lambda H: (1.0, 2.0))
    assert np.array_equal(X, np.tile([1.0, 2.0], (6, 1)))


def test_adapter_path_from_env(tmp_path, monkeypatch):
    p = tmp_path / "a.py"
    p.write_text(FAKE_ADAPTER)
    monkeypatch.setenv("ATACT_ORIGINAL_ADAPTER", str(p))
    assert backends.adapter_path() == p
    assert "original" in backends.available()
    monkeypatch.setenv("ATACT_ORIGINAL_ADAPTER", str(tmp_path / "none.py"))
    assert backends.adapter_path() is None
    assert "original" not in backends.available()


# ---------------------------------------------------------------- 2. Conformance


def _conformance_backends():
    out = [pytest.param(ReconBackend(), id="recon"),
           pytest.param(ReconBackend(RenderConfig(warp=0.25)), id="recon_warp")]
    p = backends.adapter_path()
    if p is not None:
        out.append(pytest.param(p, id="original"))
    else:
        out.append(pytest.param(None, id="original", marks=pytest.mark.skip("アダプタが無い")))
    return out


@pytest.fixture(params=_conformance_backends())
def be(request):
    b = request.param
    return load_adapter(b) if not isinstance(b, ReconBackend) else b


def test_conf_shape_and_seed(be):
    H = be.height(0.0, 0.0, 42)
    assert H.shape == (128, 128)
    assert np.all(np.isfinite(H))
    assert np.array_equal(H, be.height(0.0, 0.0, 42))
    assert not np.array_equal(H, be.height(0.0, 0.0, 43))


@pytest.mark.parametrize("va,fsg", TABLE1)
def test_conf_params_table1(be, va, fsg):
    p = be.params(*va)
    if p is None:
        pytest.skip("params が無い")
    assert np.allclose(p, fsg)


def _field_or_skip(be, f, seed=42, n=None):
    F = be.field(f, seed) if n is None else be.field(f, seed, n)
    if F is None:
        pytest.skip("field が無い")
    return F


@pytest.mark.parametrize("va", [v for v, _ in TABLE1])
def test_conf_eq4_height_is_s_tgamma_f(be, va):
    # Eq. (4): H = s T_gamma(F); centring is allowed to be present or absent
    f, s, g = params(*va)
    F = _field_or_skip(be, f)
    assert np.abs(F).max() <= 1 + 1e-9  # A2: values lie in [-1, 1]
    H = be.height(*va, 42)
    want = s * t_gamma(F, g)
    assert np.allclose(H - H.mean(), want - want.mean(), atol=1e-9)


def test_conf_p3_rq_proportional_to_s(be):
    F = _field_or_skip(be, 5.0)
    for g in (0.9, 2.6):
        assert np.isclose(rq(0.30 * t_gamma(F, g)) / rq(0.06 * t_gamma(F, g)), 5.0)


def test_conf_p4_minmax_erases_s(be):
    F = _field_or_skip(be, 5.0)
    assert np.allclose(minmax(0.06 * t_gamma(F, 1.75)), minmax(0.30 * t_gamma(F, 1.75)), atol=1e-12)


def test_conf_p6_gradient_grows_with_grid(be):
    # A coarse grid does not resolve the highest octave (8 f); compare the two finer grids
    F1 = _field_or_skip(be, 5.0, n=1024)
    F2 = _field_or_skip(be, 5.0, n=2048)
    g = 2.6
    # For gamma > 1 the maximum gradient grows when the grid is doubled (theory: 2^(1-1/gamma) = 1.53)
    assert max_gradient(t_gamma(F2, g)) / max_gradient(t_gamma(F1, g)) > 1.3
    # For gamma = 1, F is smooth and the maximum gradient has converged
    assert max_gradient(F2) / max_gradient(F1) < 1.05


# ---------------------------------------------------------------- 3. Default pinned


def _digest(a):
    # Round to 10 digits before taking the SHA-256, so that last-digit floating-point jitter does not cause failures
    return hashlib.sha256(np.round(np.asarray(a, dtype=float), 10).tobytes()).hexdigest()[:16]


# Values recorded on 2026-10-24 from the version before the A1 variants were added (6e0be23)
DEFAULT_DIGESTS = {
    ("F", 0.0, 3.0): "1fd0d1a09fe51785",
    ("F", 0.0, 7.0): "c29221a61df3bf1f",
    ("F", 0.25, 3.0): "364e4024bab82e68",
    ("F", 0.25, 7.0): "eb45d0cb6b0b1e22",
    ("H", (1, -1)): "3831f5a9f921d00a",
    ("H", (-1, 1)): "a57f64afe3dc4bd5",
}


@pytest.mark.parametrize("key", list(DEFAULT_DIGESTS))
def test_default_generator_unchanged(key):
    if key[0] == "F":
        a = procedural_field(key[2], RenderConfig(warp=key[1]), seed=42)
    else:
        a = height(*key[1])
    assert _digest(a) == DEFAULT_DIGESTS[key]


# ---------------------------------------------------------------- 4. Per-variant properties

ONE = dict(octaves=1, warp=0.0)


def test_freq_unit_half_halves_pure_tone():
    # With a single octave, no warp and gamma = 1, F is a pure tone; in half-period units the centroid is exactly half
    c = centroid(procedural_field(6.0, RenderConfig(**ONE)))
    h = centroid(procedural_field(6.0, RenderConfig(**ONE, freq_unit="half")))
    assert np.isclose(h / c, 0.5)


def test_octave_form_product_vs_sum_centroid():
    # The product sin(wx) sin(wy) has radius sqrt(2) f; the sum sin(wx) + sin(wy) has radius f
    p = centroid(procedural_field(6.0, RenderConfig(**ONE, octave_form="product")))
    s = centroid(procedural_field(6.0, RenderConfig(**ONE, octave_form="sum")))
    assert np.isclose(p, 6.0 * np.sqrt(2))
    assert np.isclose(s, 6.0)


def test_octave_form_rank():
    # As a matrix the product has rank 1; the sum and the plane wave with random orientation have rank 2
    def rank(form):
        return np.linalg.matrix_rank(procedural_field(5.0, RenderConfig(**ONE, octave_form=form)), tol=1e-8)

    assert rank("product") == 1
    assert rank("sum") == 2
    assert rank("oriented") == 2


def test_oriented_direction_depends_on_seed():
    a = procedural_field(5.0, RenderConfig(**ONE, octave_form="oriented"), seed=1)
    b = procedural_field(5.0, RenderConfig(**ONE, octave_form="oriented"), seed=2)
    # Not only the phase but the orientation changes: the location of the maximum of the 2-D spectrum differs
    pa = np.unravel_index(np.abs(np.fft.fft2(a)).argmax(), a.shape)
    pb = np.unravel_index(np.abs(np.fft.fft2(b)).argmax(), b.shape)
    assert pa != pb


def _high_fraction(F, cut=60):
    # Count only above the highest octave (8 f = 40 cycles for f = 5; product radius 56.6)
    pw = np.abs(np.fft.fft2(F - F.mean())) ** 2
    return pw[radial_frequency(F.shape[0]) > cut].sum() / pw.sum()


def test_noise_raises_high_frequency_share():
    base = _high_fraction(procedural_field(5.0, RenderConfig()))
    noisy = _high_fraction(procedural_field(5.0, RenderConfig(noise=0.3)))
    assert base < 1e-6
    assert noisy > 0.01


def test_noise_keeps_field_in_unit_range_and_deterministic():
    cfg = RenderConfig(noise=0.3)
    F = procedural_field(5.0, cfg, seed=3)
    assert np.isclose(np.abs(F).max(), 1.0)
    assert np.array_equal(F, procedural_field(5.0, cfg, seed=3))


@pytest.mark.parametrize("bad", [dict(freq_unit="x"), dict(octave_form="x")])
def test_unknown_variant_rejected(bad):
    with pytest.raises((KeyError, ValueError)):
        procedural_field(5.0, RenderConfig(**bad))
