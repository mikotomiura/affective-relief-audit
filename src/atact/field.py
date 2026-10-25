"""Reconstruction of the procedural field F and the height field H.

The original code (ESM_1.zip) is not available. This is a reconstruction from the description in Section 3.2 and Table 2 of
Harada (2026); where the description does not determine the construction, an assumption fills the gap. The assumptions correspond
one to one with the table "reconstruction assumptions" in the README (referred to here as A1-A4).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .mapping import params
from .transform import t_gamma, t_gamma_eps


@dataclass(frozen=True)
class RenderConfig:
    n: int = 128            # Table 2: 128 x 128
    octaves: int = 4        # Table 2: 4 octaves
    warp: float = 0.0       # Table 2 gives 0.25, the text says "optional". Default: none (A3)
    normalize: str = "maxabs"  # A2: divide by max |F| so that F lies in [-1, 1]
    eps: float = 0.0        # 0 gives T_gamma, positive gives T_{gamma,eps}
    # Variants of A1 (the default is A1 itself; added to test versions closer to Fig. 3)
    freq_unit: str = "cycles"   # "cycles": f is cycles per domain / "half": number of half-periods (sin(pi f x))
    octave_form: str = "product"  # "product" / "sum": sum of the two directions / "oriented": plane wave with random direction
    noise: float = 0.0      # if positive, add uniform white noise of amplitude noise to F before normalisation
    # Window position (shift the domain to [x0, x0+1) x [y0, y0+1); the same seed gives another window of the same infinite field)
    x0: float = 0.0
    y0: float = 0.0


_UNIT = {"cycles": 2 * np.pi, "half": np.pi}


def _octave(x, y, fo, px, py, cfg: RenderConfig = RenderConfig(), theta: float = 0.0):
    # A1: each octave is sin(2 pi fo x + px) sin(2 pi fo y + py), with uniformly random phases
    w = _UNIT[cfg.freq_unit] * fo
    if cfg.octave_form == "product":
        return np.sin(w * x + px) * np.sin(w * y + py)
    if cfg.octave_form == "sum":
        return 0.5 * (np.sin(w * x + px) + np.sin(w * y + py))
    if cfg.octave_form == "oriented":
        return np.sin(w * (x * np.cos(theta) + y * np.sin(theta)) + px)
    raise ValueError(cfg.octave_form)


def _draw(rng, cfg: RenderConfig):
    """Random draws for one octave. The default form draws only the two phases, leaving the sequence of draws unchanged."""
    ph = rng.uniform(0, 2 * np.pi, 2)
    theta = rng.uniform(0, np.pi) if cfg.octave_form == "oriented" else 0.0
    return ph, theta


def procedural_field(f: float, cfg: RenderConfig = RenderConfig(), seed: int = 42) -> np.ndarray:
    """Field F with octaves layers, frequency doubling and amplitude halving at each layer."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0 : cfg.n, 0 : cfg.n] / cfg.n
    x, y = x + cfg.x0, y + cfg.y0
    if cfg.warp:
        # A3: displace the coordinates by a one-layer field at the base frequency; displacement magnitude is warp / f (fraction of the base period)
        (ph, th) = _draw(rng, cfg)
        wx = _octave(x, y, f, *ph, cfg, th)
        (ph, th) = _draw(rng, cfg)
        wy = _octave(x, y, f, *ph, cfg, th)
        x = x + cfg.warp / f * wx
        y = y + cfg.warp / f * wy
    F = np.zeros((cfg.n, cfg.n))
    for o in range(cfg.octaves):
        fo, a = f * 2**o, 0.5**o
        ph, th = _draw(rng, cfg)
        F += a * _octave(x, y, fo, *ph, cfg, th)
    if cfg.noise:
        F = F + cfg.noise * rng.uniform(-1, 1, F.shape)
    if cfg.normalize == "maxabs":
        F = F / np.abs(F).max()
    elif cfg.normalize == "ampsum":
        # Constant normalisation by the sum of amplitudes: the same surface for any window and grid (spec S1.4)
        F = F / sum(0.5**o for o in range(cfg.octaves))
    elif cfg.normalize != "none":
        raise ValueError(cfg.normalize)
    return F


def height(V: float, A: float, cfg: RenderConfig = RenderConfig(), seed: int = 42) -> np.ndarray:
    """Eq. (4): H = s T_gamma(F). Descriptors are measured on the centred H (Section 3.4)."""
    f, s, g = params(V, A)
    F = procedural_field(float(f), cfg, seed)
    T = t_gamma_eps(F, g, cfg.eps) if cfg.eps > 0 else t_gamma(F, g)
    return s * T


def minmax(H: np.ndarray) -> np.ndarray:
    """Grey-level height image in [0, 1] for min-max export."""
    return (H - H.min()) / (H.max() - H.min())


def procedural_field_separable(
    f: float, n: int, seed: int, octaves: int = 4, x0: float = 0.0, y0: float = 0.0, normalize: str = "maxabs"
) -> np.ndarray:
    """S1.1-S1.4 for the canonical product form, computed octave by octave as outer products.

    Each octave sin(w x + phi) sin(w y + psi) is the outer product of two vectors, so the full array is never built
    from coordinate grids. The arithmetic is the same as in procedural_field (same draws, same order of operations),
    and the result agrees with procedural_field(f, RenderConfig(n=n, octaves=octaves, x0=x0, y0=y0,
    normalize=normalize), seed) element by element. It is used for large N, where the coordinate grids of
    procedural_field would dominate the memory.
    """
    rng = np.random.default_rng(seed)
    x = np.arange(n) / n + x0
    y = np.arange(n) / n + y0
    F = np.zeros((n, n))
    for o in range(octaves):
        fo, a = f * 2**o, 0.5**o
        px, py = rng.uniform(0, 2 * np.pi, 2)
        w = _UNIT["cycles"] * fo
        F += a * np.outer(np.sin(w * y + py), np.sin(w * x + px))
    if normalize == "maxabs":
        F /= np.abs(F).max()
    elif normalize == "ampsum":
        F /= sum(0.5**o for o in range(octaves))
    elif normalize != "none":
        raise ValueError(normalize)
    return F


def sine_1d(f: float, n: int, seed: int) -> np.ndarray:
    """One-dimensional sine sin(2 pi f x + phi) on x_i = i/n, with phi = default_rng(seed).uniform(0, 2 pi)
    (the 'oned' field of experiments/conditions/k4_centroid_2d.json)."""
    phi = np.random.default_rng(seed).uniform(0, 2 * np.pi)
    x = np.arange(n) / n
    return np.sin(2 * np.pi * f * x + phi)


def tone_surface(freqs, amps, n: int, x0: float = 0.0) -> np.ndarray:
    """Height made of tones along x only: z(x, y) = sum_m a_m sin(2 pi k_m (x + x0)), constant along y.

    Used for the flip_positive control of experiments/conditions/edge_grid_paired.json. The phases are zero; the crop
    offset x0 shifts all tones together.
    """
    x = np.arange(n) / n + x0
    row = sum(a * np.sin(2 * np.pi * k * x) for k, a in zip(freqs, amps))
    return np.tile(row, (n, 1))


def tone_amplitude_for_rms_slope(freqs, ratios, rms_slope: float) -> float:
    """Scale c such that the tones c * ratios at freqs (cycles per unit length) have the given RMS slope.

    Uses the continuous RMS slope of sum_m a_m sin(2 pi k_m x), sqrt(sum_m (2 pi k_m a_m)^2 / 2), so that the
    surface (and its amplitude) is the same at every grid.
    """
    s = np.sqrt(sum((2 * np.pi * k * r) ** 2 for k, r in zip(freqs, ratios)) / 2)
    return rms_slope / s
