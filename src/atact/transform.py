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
