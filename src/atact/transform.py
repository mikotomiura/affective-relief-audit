"""Height transform T_gamma (eq. (4) of Harada (2026)) and its smoothed version T_{gamma,eps}."""

from __future__ import annotations

import numpy as np
from scipy.special import gamma as Gamma


def t_gamma(u, g):
    """T_gamma(u) = sign(u) |u|^(1/gamma)."""
    u = np.asarray(u, dtype=float)
    return np.sign(u) * np.abs(u) ** (1.0 / g)


def t_gamma_eps(u, g, eps):
    """Version with the singularity at zero smoothed over width eps. Odd, and preserves +-1.

    For |u| >> eps it is close to T_gamma; the slope near 0 is bounded by about eps^(1/gamma - 1).
    """
    u = np.asarray(u, dtype=float)
    k = (1.0 / g - 1.0) / 2.0
    return u * (u**2 + eps**2) ** k / (1.0 + eps**2) ** k


def sigma2_single_sine(g):
    """Proposition 3: closed form of E|T_gamma(F)|^2 for F = sin(theta)."""
    return Gamma(1.0 / g + 0.5) / (np.sqrt(np.pi) * Gamma(1.0 / g + 1.0))


def fourier_coeff_odd(n, g):
    """Appendix A, Lemma A.4.1: coefficients b_n in T_gamma(sin theta) = sum b_n sin(n theta) (n odd, n > 1/gamma).

    Closed form obtained from the imaginary part of DLMF 5.12.6 and the reflection formula (DLMF 5.5.3).
    """
    from scipy.special import gammaln

    a = 1.0 / g
    n = np.asarray(n, dtype=float)
    sign = np.sign(Gamma((n - a) / 2.0))
    ratio = sign * np.exp(gammaln((n - a) / 2.0) - gammaln(1.0 + (n + a) / 2.0))
    return 2.0 ** (1.0 - a) * Gamma(a + 1.0) * np.cos(np.pi * a / 2.0) / np.pi * ratio
