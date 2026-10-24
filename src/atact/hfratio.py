"""Copy of the "HF ratio" descriptor of the evaluation of Gao et al. (2026), and the procedure for building a normal map from a height field.

The copy is from the authors' public code (github.com/alex4727/Text2TactileGraphics, main, retrieved 2026-10-24):
`src/experiments/text2texture/05_evaluate_hf_ratio.py` and
`src/text2tactilegraphics/geometry/filtering.py`. The retrieved code was read and transcribed, not run.
The only difference is in input and output (uint8 arrays instead of PIL); the computational steps and constants are the same.
"""

from __future__ import annotations

import numpy as np

DEFAULT_FREQ_THRESHOLD = 120  # text2texture/config.py
_GAUSSIAN_FWHM = float(np.sqrt(2 * np.log(2)))


# --- copy of filtering.py --------------------------------------------------------


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
    """apply_high_pass_to_normal_map(method="per_channel"). Input and output are uint8 H x W x 3."""
    normal_rgb = rgb.astype(np.float32) / 255.0
    h, w = normal_rgb.shape[:2]
    normal = normal_rgb * 2.0 - 1.0
    hp = _highpass_filter_fft(normal, cutoff_ratio(h, w, freq_threshold))
    hp[..., 2] += 1.0
    hp = hp / (np.linalg.norm(hp, axis=-1, keepdims=True) + 1e-8)
    out = (hp + 1.0) / 2.0
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


# --- copy of 05_evaluate_hf_ratio.py ---------------------------------------------


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
    """compute_hf_ratio. rgb is a uint8 H x W x 3 normal map."""
    before = _signal_energy(rgb.astype(np.float32) / 255.0)
    if before <= 0:
        return 0.0
    filtered = high_pass_normal_rgb(rgb, freq_threshold)
    after = _signal_energy(filtered.astype(np.float32) / 255.0)
    return float(np.clip(after / before, 0.0, 1.0))


# --- From height field to normal map (from here on, the procedure of this work) --------------------------------


def normal_rgb_from_height(z: np.ndarray, side: float = 1.0) -> np.ndarray:
    """Build an OpenGL-convention normal map (uint8) from a height z (in the same length unit as the domain).

    Slopes are central differences (one-sided at the edge; no periodicity assumed). The pixel spacing is side / N, so
    for the same surface the normals are nearly the same on different grids.
    """
    n = z.shape[0]
    dzdy, dzdx = np.gradient(z, side / n)
    v = np.stack([-dzdx, dzdy, np.ones_like(z)], axis=-1)
    v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    return np.round((v + 1.0) / 2.0 * 255).astype(np.uint8)


def hann2d(n: int) -> np.ndarray:
    w = np.hanning(n)
    return np.outer(w, w)


def hf_ratio_float(normal: np.ndarray, freq_threshold: float = DEFAULT_FREQ_THRESHOLD) -> float:
    """Float variant of hf_ratio (S2.9): a control without uint8 rounding.

    `normal` is an H x W x 3 array of unit normals in [-1, 1]. The steps follow hf_ratio and
    high_pass_normal_rgb exactly, with the encoding (n + 1) / 2 kept in floating point, so only
    the rounding to uint8 of the input and of the filtered map is omitted.
    """
    rgb01 = ((normal.astype(np.float32) + 1.0) / 2.0).astype(np.float32)
    before = _signal_energy(rgb01)
    if before <= 0:
        return 0.0
    h, w = rgb01.shape[:2]
    hp = _highpass_filter_fft(rgb01 * 2.0 - 1.0, cutoff_ratio(h, w, freq_threshold))
    hp[..., 2] += 1.0
    hp = hp / (np.linalg.norm(hp, axis=-1, keepdims=True) + 1e-8)
    after = _signal_energy(np.clip((hp + 1.0) / 2.0, 0, 1))
    return float(np.clip(after / before, 0.0, 1.0))
