"""表面の記述子。原稿の式 (5) Rq と式 (6) スペクトルの重心。"""

from __future__ import annotations

import numpy as np


def rq(H: np.ndarray) -> float:
    """式 (5): 中心化した場の二乗平均平方根。"""
    return float(np.sqrt(np.mean((H - H.mean()) ** 2)))


def radial_frequency(n: int) -> np.ndarray:
    """2 次元 DFT の各係数の半径方向の周波数（領域あたりの周期数）。"""
    k = np.fft.fftfreq(n) * n
    kx, ky = np.meshgrid(k, k)
    return np.hypot(kx, ky)


def centroid(H: np.ndarray) -> float:
    """式 (6): 振幅で重みを付けた半径方向の周波数の重心（DC は中心化で 0）。"""
    Hc = H - H.mean()
    mag = np.abs(np.fft.fft2(Hc))
    rho = radial_frequency(H.shape[0])
    return float((rho * mag).sum() / mag.sum())


def centroid_power(H: np.ndarray, cutoff: float | None = None) -> float:
    """代わりの指標: パワーで重み付けし、必要なら半径 cutoff で打ち切る。"""
    Hc = H - H.mean()
    pw = np.abs(np.fft.fft2(Hc)) ** 2
    rho = radial_frequency(H.shape[0])
    if cutoff is not None:
        pw = np.where(rho <= cutoff, pw, 0.0)
    return float((rho * pw).sum() / pw.sum())


def max_gradient(H: np.ndarray) -> float:
    """格子の間隔を 1/n とした最大の勾配の大きさ。"""
    n = H.shape[0]
    gy, gx = np.gradient(H, 1.0 / n)
    return float(np.hypot(gx, gy).max())
