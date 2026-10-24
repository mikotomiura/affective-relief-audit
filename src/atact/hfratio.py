"""Gao ら（2026）の評価の記述子「HF ratio」の写しと、高さの場から法線の図を作る手順。

写しの出典は著者の公開コード（github.com/alex4727/Text2TactileGraphics、main を 2026-10-24 に取得）の
`src/experiments/text2texture/05_evaluate_hf_ratio.py` と
`src/text2tactilegraphics/geometry/filtering.py`。取得したコードは実行せず、読んで書き写した。
違いは入出力（PIL の代わりに uint8 の配列）だけで、計算の手順と定数は同じにしてある。
"""

from __future__ import annotations

import numpy as np

DEFAULT_FREQ_THRESHOLD = 120  # text2texture/config.py
_GAUSSIAN_FWHM = float(np.sqrt(2 * np.log(2)))


# --- filtering.py の写し --------------------------------------------------------


def _highpass_filter_fft(data: np.ndarray, cutoff_ratio: float) -> np.ndarray:
    h, w = data.shape[:2]
    cy, cx = h // 2, w // 2
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    cutoff = cutoff_ratio * np.sqrt(cx**2 + cy**2)
    hp = 1.0 - np.exp(-(dist**2) / (2 * cutoff**2))
    if data.ndim == 3:
        hp = hp[..., None]
    spec = np.fft.fftshift(np.fft.fft2(data, axes=(0, 1)), axes=(0, 1))
    out = np.fft.ifft2(np.fft.ifftshift(spec * hp, axes=(0, 1)), axes=(0, 1))
    return np.real(out).astype(np.float32)


def cutoff_ratio(h: int, w: int, freq_threshold: float) -> float:
    max_dist = np.sqrt((h / 2) ** 2 + (w / 2) ** 2)
    return float(np.clip(h / (freq_threshold * max_dist * _GAUSSIAN_FWHM), 0.001, 0.5))


def high_pass_normal_rgb(rgb: np.ndarray, freq_threshold: float) -> np.ndarray:
    """apply_high_pass_to_normal_map(method="per_channel")。入出力は uint8 の H x W x 3。"""
    normal_rgb = rgb.astype(np.float32) / 255.0
    h, w = normal_rgb.shape[:2]
    normal = normal_rgb * 2.0 - 1.0
    hp = _highpass_filter_fft(normal, cutoff_ratio(h, w, freq_threshold))
    hp[..., 2] += 1.0
    hp = hp / (np.linalg.norm(hp, axis=-1, keepdims=True) + 1e-8)
    out = (hp + 1.0) / 2.0
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


# --- 05_evaluate_hf_ratio.py の写し ---------------------------------------------


def _signal_energy(img01: np.ndarray) -> float:
    image = img01.astype(np.float32)
    if image.min() >= 0 and image.max() <= 1:
        image = image * 2.0 - 1.0
    total = 0.0
    for c in range(image.shape[2]):
        ch = image[:, :, c] - image[:, :, c].mean()
        e = np.abs(np.fft.fft2(ch)) ** 2
        e[0, 0] = 0.0
        total += float(np.sum(e))
    return total


def hf_ratio(rgb: np.ndarray, freq_threshold: float = DEFAULT_FREQ_THRESHOLD) -> float:
    """compute_hf_ratio。rgb は uint8 の H x W x 3 の法線の図。"""
    before = _signal_energy(rgb.astype(np.float32) / 255.0)
    if before <= 0:
        return 0.0
    filtered = high_pass_normal_rgb(rgb, freq_threshold)
    after = _signal_energy(filtered.astype(np.float32) / 255.0)
    return float(np.clip(after / before, 0.0, 1.0))


# --- 高さの場から法線の図へ（ここからは本研究の手順） --------------------------------


def normal_rgb_from_height(z: np.ndarray, side: float = 1.0) -> np.ndarray:
    """高さ z（領域と同じ長さの単位）から OpenGL 規約の法線の図（uint8）を作る。

    傾きは中心差分（端は片側差分。周期を仮定しない）。画素の間隔は side / N で、
    同じ表面なら格子を変えても法線はほぼ同じになる。
    """
    n = z.shape[0]
    dzdy, dzdx = np.gradient(z, side / n)
    v = np.stack([-dzdx, dzdy, np.ones_like(z)], axis=-1)
    v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    return np.round((v + 1.0) / 2.0 * 255).astype(np.uint8)


def hann2d(n: int) -> np.ndarray:
    w = np.hanning(n)
    return np.outer(w, w)
