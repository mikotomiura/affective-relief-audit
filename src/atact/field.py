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
    # A1 の変種（既定は A1 そのもの。図 3 に近づける版を試すために足した）
    freq_unit: str = "cycles"   # "cycles": f は領域あたりの周期数 / "half": 半周期の数（sin(pi f x)）
    octave_form: str = "product"  # "product" / "sum": 縦横の和 / "oriented": 向きが乱数の平面波
    noise: float = 0.0      # 正なら、正規化の前に F へ振幅 noise の一様な白色雑音を足す


_UNIT = {"cycles": 2 * np.pi, "half": np.pi}


def _octave(x, y, fo, px, py, cfg: RenderConfig = RenderConfig(), theta: float = 0.0):
    # A1: 各オクターブは sin(2 pi fo x + px) sin(2 pi fo y + py)、位相は一様乱数
    w = _UNIT[cfg.freq_unit] * fo
    if cfg.octave_form == "product":
        return np.sin(w * x + px) * np.sin(w * y + py)
    if cfg.octave_form == "sum":
        return 0.5 * (np.sin(w * x + px) + np.sin(w * y + py))
    if cfg.octave_form == "oriented":
        return np.sin(w * (x * np.cos(theta) + y * np.sin(theta)) + px)
    raise ValueError(cfg.octave_form)


def _draw(rng, cfg: RenderConfig):
    """1 段ぶんの乱数。既定の形では位相 2 つだけを引き、元の乱数の並びを変えない。"""
    ph = rng.uniform(0, 2 * np.pi, 2)
    theta = rng.uniform(0, np.pi) if cfg.octave_form == "oriented" else 0.0
    return ph, theta


def procedural_field(f: float, cfg: RenderConfig = RenderConfig(), seed: int = 42) -> np.ndarray:
    """周波数を倍・振幅を半分にしながら octaves 段を重ねた場 F。"""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0 : cfg.n, 0 : cfg.n] / cfg.n
    if cfg.warp:
        # A3: 基本周波数の 1 段の場で座標をずらす。ずれの大きさは warp / f（基本周期の割合）
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
