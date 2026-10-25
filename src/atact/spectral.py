"""Edge and grid treatments for descriptors (spec S3) and the decimation that separates aliasing (spec S4).

Window, periodic-plus-smooth decomposition and band fixing are procedures for comparing edge discontinuity and grid dependence;
the value after treatment is not taken as the true value (the window also changes the interior of the domain).
"""

from __future__ import annotations

import numpy as np

from .descriptors import radial_frequency


def hann2d(n: int) -> np.ndarray:
    """S3.1: outer product of periodic Hann windows, w(i) = sin^2(pi i / n). Zero at the DFT edge."""
    w = np.sin(np.pi * np.arange(n) / n) ** 2
    return np.outer(w, w)


def windowed(H: np.ndarray) -> np.ndarray:
    """S3.1: subtract the mean, apply the window, then subtract the mean again after windowing."""
    X = (H - H.mean()) * hann2d(H.shape[0])
    return X - X.mean()


def periodic_component(H: np.ndarray) -> np.ndarray:
    """S3.2: periodic component p (H = p + s) of the Moisan (2011) decomposition into periodic and smooth components.

    From the edge-difference image v, s is obtained by the inverse of the discrete Laplacian (s has mean 0).
    """
    u = H.astype(float)
    m, n = u.shape
    v = np.zeros_like(u)
    v[0, :] = u[-1, :] - u[0, :]
    v[-1, :] = u[0, :] - u[-1, :]
    v[:, 0] += u[:, -1] - u[:, 0]
    v[:, -1] += u[:, 0] - u[:, -1]
    q = np.arange(m).reshape(-1, 1)
    r = np.arange(n).reshape(1, -1)
    den = 2 * np.cos(2 * np.pi * q / m) + 2 * np.cos(2 * np.pi * r / n) - 4
    den[0, 0] = 1.0
    S = np.fft.fft2(v) / den
    S[0, 0] = 0.0
    return u - np.real(np.fft.ifft2(S))


def centroid_band(H: np.ndarray, kmax: float, weight: str = "power") -> float:
    """S2.4: centroid measured on the bins with radius at most kmax (cycles per domain, physical unit) only.

    kmax must not exceed N/2 (a precondition for the band not to depend on the grid).
    """
    n = H.shape[0]
    if kmax > n / 2:
        raise ValueError("kmax must be <= N/2")
    mag = np.abs(np.fft.fft2(H - H.mean()))
    w = mag**2 if weight == "power" else mag
    if weight not in ("amp", "power"):
        raise ValueError(weight)
    rho = radial_frequency(n)
    keep = (rho <= kmax) & (rho > 0)
    return float((rho[keep] * w[keep]).sum() / w[keep].sum())


def remove_plane(Z: np.ndarray) -> np.ndarray:
    """S5.2: subtract a least-squares plane (used after cropping a measured height)."""
    m, n = Z.shape
    y, x = np.mgrid[0:m, 0:n]
    A = np.column_stack([np.ones(Z.size), x.ravel(), y.ravel()])
    c, *_ = np.linalg.lstsq(A, Z.ravel(), rcond=None)
    return Z - (A @ c).reshape(m, n)


def decimate_fourier(Z: np.ndarray, n: int) -> np.ndarray:
    """S4: decimate to n x n after an ideal low-pass (keeping only bins whose components lie in [-n/2, n/2)).

    The result is the field built on the fine grid M = Z.shape[0], band-limited and sampled on the grid of n.
    M must be a multiple of n.
    """
    M = Z.shape[0]
    if M % n or Z.shape[1] != M:
        raise ValueError("Z must be square with side a multiple of n")
    Fz = np.fft.fft2(Z)
    idx = np.r_[0 : n // 2, M - n // 2 : M]
    small = Fz[np.ix_(idx, idx)] * (n / M) ** 2
    return np.real(np.fft.ifft2(small))


def subsample(Z: np.ndarray, n: int) -> np.ndarray:
    """S4: decimate by taking every other sample without low-pass (control that retains aliasing)."""
    step = Z.shape[0] // n
    return Z[::step, ::step]


def windowed_normals(rgb: np.ndarray) -> np.ndarray:
    """S3.1: multiply the deviation of each normal-map component from its mean by W, renormalise and return to uint8."""
    v = rgb[..., :3].astype(float) / 255 * 2 - 1
    m = v.reshape(-1, 3).mean(0)
    v = m + (v - m) * hann2d(v.shape[0])[..., None]
    v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    return np.round((v + 1) / 2 * 255).astype(np.uint8)


def decimate_normals(rgb: np.ndarray, n: int) -> np.ndarray:
    """S5.4: reduce each component of a normal map to n by decimate_fourier, renormalise and return to uint8."""
    v = rgb[..., :3].astype(float) / 255 * 2 - 1
    w = np.stack([decimate_fourier(v[..., c], n) for c in range(3)], axis=-1)
    w = w / np.linalg.norm(w, axis=-1, keepdims=True)
    return np.round((w + 1) / 2 * 255).astype(np.uint8)


def linear_hf_ratio(z: np.ndarray, freq_threshold: float) -> float:
    """S2.9, linear height variant: high-pass energy ratio of the height itself.

    Uses the Gaussian high-pass weight of the HF ratio (same cutoff rule) on the DFT of
    z - mean(z); the DC bin is excluded from both energies.
    """
    from .hfratio import _highpass_filter_fft, cutoff_ratio

    zc = (z - z.mean()).astype(np.float32)
    h, w = zc.shape
    hp = _highpass_filter_fft(zc, cutoff_ratio(h, w, freq_threshold))
    e = np.abs(np.fft.fft2(zc)) ** 2
    e[0, 0] = 0.0
    ehp = np.abs(np.fft.fft2(hp)) ** 2
    ehp[0, 0] = 0.0
    return float(ehp.sum() / e.sum())


def windowed_normals_float(v: np.ndarray) -> np.ndarray:
    """windowed_normals without the uint8 rounding of input and output (for the float variant of S2.9).

    `v` is an H x W x 3 array of unit normals in [-1, 1]; the result is renormalised unit normals.
    """
    m = v.reshape(-1, 3).mean(0)
    w = m + (v - m) * hann2d(v.shape[0])[..., None]
    return w / np.linalg.norm(w, axis=-1, keepdims=True)
