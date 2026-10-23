"""手続き的な場 F と高さの場 H の組み直し。

元のコード（ESM_1.zip）は手元に無い。原稿 3.2 節と表 2 の記述から組み直したもので、
記述が決めていないところは仮定で埋めた。仮定は README の「組み直しの仮定」の表と
1 対 1 に対応する（ここでは A1〜A4 の記号で示す）。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .mapping import params
from .transform import t_gamma, t_gamma_eps


@dataclass(frozen=True)
class RenderConfig:
    n: int = 128            # 表 2: 128 x 128
    octaves: int = 4        # 表 2: 4 オクターブ
    warp: float = 0.0       # 表 2 は 0.25、本文は "optional"。既定は無し（A3）
    normalize: str = "maxabs"  # A2: |F| の最大で割って [-1, 1] に入れる
    eps: float = 0.0        # 0 なら T_gamma、正なら T_{gamma,eps}


def _octave(x, y, fo, px, py):
    # A1: 各オクターブは sin(2 pi fo x + px) sin(2 pi fo y + py)、位相は一様乱数
    return np.sin(2 * np.pi * fo * x + px) * np.sin(2 * np.pi * fo * y + py)


def procedural_field(f: float, cfg: RenderConfig = RenderConfig(), seed: int = 42) -> np.ndarray:
    """周波数を倍・振幅を半分にしながら octaves 段を重ねた場 F。"""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0 : cfg.n, 0 : cfg.n] / cfg.n
    if cfg.warp:
        # A3: 基本周波数の 1 段の場で座標をずらす。ずれの大きさは warp / f（基本周期の割合）
        wx = _octave(x, y, f, *rng.uniform(0, 2 * np.pi, 2))
        wy = _octave(x, y, f, *rng.uniform(0, 2 * np.pi, 2))
        x = x + cfg.warp / f * wx
        y = y + cfg.warp / f * wy
    F = np.zeros((cfg.n, cfg.n))
    for o in range(cfg.octaves):
        fo, a = f * 2**o, 0.5**o
        F += a * _octave(x, y, fo, *rng.uniform(0, 2 * np.pi, 2))
    if cfg.normalize == "maxabs":
        F = F / np.abs(F).max()
    elif cfg.normalize != "none":
        raise ValueError(cfg.normalize)
    return F


def height(V: float, A: float, cfg: RenderConfig = RenderConfig(), seed: int = 42) -> np.ndarray:
    """式 (4): H = s T_gamma(F)。記述子は中心化した H で測る（3.4 節）。"""
    f, s, g = params(V, A)
    F = procedural_field(float(f), cfg, seed)
    T = t_gamma_eps(F, g, cfg.eps) if cfg.eps > 0 else t_gamma(F, g)
    return s * T


def minmax(H: np.ndarray) -> np.ndarray:
    """書き出し用の [0, 1] の灰色の高さ図。"""
    return (H - H.min()) / (H.max() - H.min())
