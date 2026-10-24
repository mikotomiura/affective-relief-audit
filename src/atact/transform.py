"""高さの変換 T_gamma（式 (4)）と、なめらかにした T_{gamma,eps}。"""

from __future__ import annotations

import numpy as np
from scipy.special import gamma as Gamma


def t_gamma(u, g):
    """T_gamma(u) = sign(u) |u|^(1/gamma)。"""
    u = np.asarray(u, dtype=float)
    return np.sign(u) * np.abs(u) ** (1.0 / g)


def t_gamma_eps(u, g, eps):
    """零点の特異性を幅 eps でならした版。奇関数で +-1 を保つ。

    |u| >> eps では T_gamma に近く、0 の近くの傾きは eps^(1/gamma - 1) 程度に抑えられる。
    """
    u = np.asarray(u, dtype=float)
    k = (1.0 / g - 1.0) / 2.0
    return u * (u**2 + eps**2) ** k / (1.0 + eps**2) ** k


def sigma2_single_sine(g):
    """命題 3: F = sin(theta) のとき E|T_gamma(F)|^2 の閉じた形。"""
    return Gamma(1.0 / g + 0.5) / (np.sqrt(np.pi) * Gamma(1.0 / g + 1.0))


def fourier_coeff_odd(n, g):
    """付録 A 補題 A.4.1: T_gamma(sin theta) = sum b_n sin(n theta) の係数 b_n（n は奇数、n > 1/gamma）。

    DLMF 5.12.6 の虚部と反転公式（DLMF 5.5.3）から得た閉じた形。
    """
    from scipy.special import gammaln

    a = 1.0 / g
    n = np.asarray(n, dtype=float)
    sign = np.sign(Gamma((n - a) / 2.0))
    ratio = sign * np.exp(gammaln((n - a) / 2.0) - gammaln(1.0 + (n + a) / 2.0))
    return 2.0 ** (1.0 - a) * Gamma(a + 1.0) * np.cos(np.pi * a / 2.0) / np.pi * ratio
