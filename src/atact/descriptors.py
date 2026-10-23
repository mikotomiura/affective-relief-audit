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


def centroid_variant(
    H: np.ndarray,
    weight: str = "amp",
    center: bool = True,
    rescale: str | None = None,
    half: bool = False,
    rho_round: bool = False,
) -> float:
    """式 (6) の読み方の違いを切り替えて測る。既定は centroid() と同じ値になる。

    weight   "amp": |H^| で重み（式 (6)） / "power": |H^|^2 で重み
    center   False なら平均を引かない（DC の係数が重みに入る。DC の rho は 0）
    rescale  "minmax" なら [0, 1] に伸ばした後の場で測る（3.4 節の「正規化しない」に反する読み）
    half     True なら rfft2 の半平面だけで測る（共役の重なりを数えない実装）
    rho_round True なら半径を整数に丸める（同心の輪で集計する実装）
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
    """格子の間隔を 1/n とした最大の勾配の大きさ。"""
    n = H.shape[0]
    gy, gx = np.gradient(H, 1.0 / n)
    return float(np.hypot(gx, gy).max())
