"""Surface descriptors: Rq, eq. (5), and the spectral centroid, eq. (6), of Harada (2026)."""

from __future__ import annotations

import numpy as np


def rq(H: np.ndarray) -> float:
    """Eq. (5): root mean square of the centred field."""
    return float(np.sqrt(np.mean((H - H.mean()) ** 2)))


def radial_frequency(n: int) -> np.ndarray:
    """Radial frequency of each coefficient of the 2-D DFT (cycles per domain)."""
    k = np.fft.fftfreq(n) * n
    kx, ky = np.meshgrid(k, k)
    return np.hypot(kx, ky)


def centroid(H: np.ndarray) -> float:
    """Eq. (6): amplitude-weighted centroid of the radial frequency (DC is 0 after centring)."""
    Hc = H - H.mean()
    mag = np.abs(np.fft.fft2(Hc))
    rho = radial_frequency(H.shape[0])
    return float((rho * mag).sum() / mag.sum())


def centroid_power(H: np.ndarray, cutoff: float | None = None) -> float:
    """Alternative measure: power-weighted, optionally truncated at radius cutoff."""
    Hc = H - H.mean()
    pw = np.abs(np.fft.fft2(Hc)) ** 2
    rho = radial_frequency(H.shape[0])
    if cutoff is not None:
        pw = np.where(rho <= cutoff, pw, 0.0)
    return float((rho * pw).sum() / pw.sum())


def centroid_variant(
    H: np.ndarray,
    weight: str = "amp",
    center: bool = True,
    rescale: str | None = None,
    half: bool = False,
    rho_round: bool = False,
) -> float:
    """Measure under alternative readings of eq. (6). The default gives the same value as centroid().

    weight   "amp": weight by |H^| (eq. (6)) / "power": weight by |H^|^2
    center   if False the mean is not subtracted (the DC coefficient enters the weights; its rho is 0)
    rescale  "minmax" measures on the field stretched to [0, 1] (a reading contrary to "no normalisation" in Section 3.4)
    half     if True use only the half-plane of rfft2 (an implementation that does not count the conjugate overlap)
    rho_round if True round the radius to an integer (an implementation that aggregates over concentric rings)
    """
    X = H.astype(float)
    if rescale == "minmax":
        X = (X - X.min()) / (X.max() - X.min())
    elif rescale is not None:
        raise ValueError(rescale)
    if center:
        X = X - X.mean()
    n = X.shape[0]
    if half:
        mag = np.abs(np.fft.rfft2(X))
        kx = np.fft.rfftfreq(n) * n
        ky = np.fft.fftfreq(n) * n
        KX, KY = np.meshgrid(kx, ky)
        rho = np.hypot(KX, KY)
    else:
        mag = np.abs(np.fft.fft2(X))
        rho = radial_frequency(n)
    if rho_round:
        rho = np.round(rho)
    w = mag**2 if weight == "power" else mag
    if weight not in ("amp", "power"):
        raise ValueError(weight)
    return float((rho * w).sum() / w.sum())


def max_gradient(H: np.ndarray) -> float:
    """Maximum gradient magnitude, with grid spacing 1/n."""
    n = H.shape[0]
    gy, gx = np.gradient(H, 1.0 / n)
    return float(np.hypot(gx, gy).max())


def centroid_1d(z: np.ndarray) -> float:
    """One-dimensional version of eq. (6) (eq. (1) of Appendix A): amplitude-weighted frequency centroid."""
    zc = z - z.mean()
    mag = np.abs(np.fft.fft(zc))
    k = np.abs(np.fft.fftfreq(len(z)) * len(z))
    return float((k * mag).sum() / mag.sum())
