"""感情の座標 (V, A) から形のつまみ (f, s, gamma) への写像。原稿の式 (1)-(3)。"""

from __future__ import annotations

import numpy as np

# 式 (1)-(3) の係数
F0, F1 = 3.0, 4.0
S0, S1 = 0.06, 0.24
G0, G1 = 0.9, 1.7
WP, WQ = 0.65, 0.35


def pq(V, A):
    """p = (A+1)/2, q = (1-V)/2。V, A は [-1, 1] に切る（表 2）。"""
    V = np.clip(V, -1.0, 1.0)
    A = np.clip(A, -1.0, 1.0)
    return (A + 1.0) / 2.0, (1.0 - V) / 2.0


def params(V, A):
    """(V, A) -> (f, s, gamma)。"""
    p, q = pq(V, A)
    f = F0 + F1 * p
    s = S0 + S1 * q
    g = G0 + G1 * (WP * p + WQ * q)
    return f, s, g


def jacobian():
    """列は d/dV と d/dA。行は (f, s, gamma)。写像はアフィンなので定数。"""
    dV = np.array([0.0, -S1 / 2.0, -G1 * WQ / 2.0])
    dA = np.array([F1 / 2.0, 0.0, G1 * WP / 2.0])
    return np.column_stack([dV, dA])


def gamma_from_fs(f, s):
    """命題 1: 像は平面 gamma = G0 + a (f - F0) + b (s - S0) の上にある。"""
    a = G1 * WP / F1
    b = G1 * WQ / S1
    return G0 + a * (f - F0) + b * (s - S0)
