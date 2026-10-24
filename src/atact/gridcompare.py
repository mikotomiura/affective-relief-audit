"""Copies of two descriptors used in comparisons across resolutions, and components to reproduce that comparison on synthetic surfaces.

- GLCM Score: `gray_proc` and `glcm` of `eval.py` in the public code of Diffusion-4K (Zhang et al., CVPR 2025)
  (github.com/zhang0jhon/diffusion-4k, main, retrieved 2026-10-24).
  HiMat (Wang et al., Eurographics 2026) compares outputs at 256, 512 and 4K with this measure.
  The paper's formula carries a minus sign, s = -(1/P) sum H(g_p), but the code returns a positive entropy
  (skimage shannon_entropy applied to the GLCM array). The code is followed here.
- Seam measure: the public code of Gao et al. 2026 (github.com/alex4727/Text2TactileGraphics),
  `src/experiments/tiling/02_evaluate_tileability.py`, and the downscaling (PIL LANCZOS) and centre crop of `01_generate_tiled.py`.

The retrieved code was read and transcribed, not run. The only differences are in input and output (arrays instead of files).
"""

from __future__ import annotations

import numpy as np
from PIL import Image
from skimage.feature import graycomatrix
from skimage.measure import shannon_entropy

# --- GLCM Score of Diffusion-4K ------------------------------------------------

GLCM_DIST = [1, 2, 3, 4]
GLCM_ANGLES = [0, np.pi / 4, np.pi / 2, np.pi * 3 / 4]


def gray64(gray_u8: np.ndarray) -> np.ndarray:
    """Second half of gray_proc (reduce 256 grey levels to 64 by dividing by 4). The input is already grey uint8."""
    return (gray_u8.astype(np.uint8) // 4).astype(np.uint8)


def glcm_entropy(patch64: np.ndarray) -> float:
    g = graycomatrix(patch64, GLCM_DIST, GLCM_ANGLES, levels=64, normed=True)
    return float(shannon_entropy(g))


def glcm_score(gray_u8: np.ndarray, patch: int = 64) -> float:
    """Loop of main: split the image into patches of patch pixels and average the per-patch values."""
    g = gray64(gray_u8)
    n = g.shape[0] // patch
    s = [glcm_entropy(g[i * patch:(i + 1) * patch, j * patch:(j + 1) * patch])
         for i in range(n) for j in range(n)]
    return float(np.mean(s))


# --- Seam measure of Gao et al. 2026 --------------------------------------------------


def border_discontinuity(img: np.ndarray, direction: str) -> float:
    img = img.astype(np.float32)
    if direction == "x":
        e1, e2 = img[:, -1], img[:, 0]
    else:
        e1, e2 = img[-1, :], img[0, :]
    return float(np.mean(np.abs(e1 - e2)))


def gradient_continuity(img: np.ndarray, direction: str) -> float:
    img = img.astype(np.float32)
    if direction == "x":
        g_r, g_l, g_s = img[:, -1] - img[:, -2], img[:, 1] - img[:, 0], img[:, 0] - img[:, -1]
    else:
        g_r, g_l, g_s = img[-1, :] - img[-2, :], img[1, :] - img[0, :], img[0, :] - img[-1, :]
    return float(np.mean(np.abs(g_s - g_r) + np.abs(g_l - g_s)))


def seam_metrics(rgb_u8: np.ndarray) -> dict[str, float]:
    arr = rgb_u8.astype(np.float32)
    return {
        "border_avg": (border_discontinuity(arr, "x") + border_discontinuity(arr, "y")) / 2,
        "grad_cont_avg": (gradient_continuity(arr, "x") + gradient_continuity(arr, "y")) / 2,
    }


def resize_lanczos(rgb_u8: np.ndarray, size: int) -> np.ndarray:
    return np.asarray(Image.fromarray(rgb_u8).resize((size, size), Image.Resampling.LANCZOS))


def center_crop(rgb_u8: np.ndarray, size: int) -> np.ndarray:
    h, w = rgb_u8.shape[:2]
    t, l = (h - size) // 2, (w - size) // 2
    return rgb_u8[t:t + size, l:l + size]


# --- Analytic field (from here on, the procedure of this work) ------------------------------------------


def field_and_grad(f: float, octaves: int, n: int, seed: int, x0: float = 0.0, y0: float = 0.0,
                   max_freq: float | None = None):
    """Field F on the window [x0, x0+1) x [y0, y0+1) and its analytic gradient (unit: domain side = 1).

    Each layer is sin(2π f_o x + φ) sin(2π f_o y + ψ), f_o = f 2^o, amplitude 0.5^o. Phases are drawn as in atact.field.
    If max_freq is given, layers with f_o above it are dropped (so that no detail is present that the generator for that grid could not produce).
    The random draws include the dropped layers, so the phases of the remaining layers do not depend on max_freq.
    """
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:n, 0:n] / n
    x, y = x + x0, y + y0
    F, Fx, Fy = np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n))
    for o in range(octaves):
        fo, a = f * 2**o, 0.5**o
        px, py = rng.uniform(0, 2 * np.pi, 2)
        if max_freq is not None and fo > max_freq:
            continue
        w = 2 * np.pi * fo
        sx, sy = np.sin(w * x + px), np.sin(w * y + py)
        F += a * sx * sy
        Fx += a * w * np.cos(w * x + px) * sy
        Fy += a * w * sx * np.cos(w * y + py)
    return F, Fx, Fy


def height_scale(f: float, octaves: int, rms_slope: float) -> float:
    """Scale H0 of the height at which the RMS slope magnitude equals rms_slope, for a periodic field with integer f (all layers included).

    The mean square of each gradient component of a layer is a^2 w^2 / 4; cross terms between layers have mean 0.
    """
    s2 = sum((0.5**o) ** 2 * (2 * np.pi * f * 2**o) ** 2 / 2 for o in range(octaves))
    return rms_slope / np.sqrt(s2)


def normals_from_grad(zx: np.ndarray, zy: np.ndarray) -> np.ndarray:
    """Unit normals in the OpenGL convention (H x W x 3, floating point). Same orientation as atact.hfratio.normal_rgb_from_height."""
    v = np.stack([-zx, zy, np.ones_like(zx)], axis=-1)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def to_rgb_u8(nrm: np.ndarray) -> np.ndarray:
    return np.round((nrm + 1.0) / 2.0 * 255).astype(np.uint8)


def upsample(img: np.ndarray, size: int, method: str) -> np.ndarray:
    """Enlarge a floating-point H x W x C image to size, component by component.

    method: "fourier" (band-limited interpolation for periodic fields; DFT zero padding),
    or PIL "nearest" / "bilinear" / "bicubic" / "lanczos" (applied to floating-point images).
    """
    n = img.shape[0]
    if n == size:
        return img
    out = np.empty((size, size, img.shape[2]))
    for c in range(img.shape[2]):
        ch = img[..., c]
        if method == "fourier":
            S = np.fft.fftshift(np.fft.fft2(ch))
            P = np.zeros((size, size), complex)
            o = (size - n) // 2
            P[o:o + n, o:o + n] = S
            out[..., c] = np.real(np.fft.ifft2(np.fft.ifftshift(P))) * (size / n) ** 2
        else:
            rs = {"nearest": Image.Resampling.NEAREST, "bilinear": Image.Resampling.BILINEAR,
                  "bicubic": Image.Resampling.BICUBIC, "lanczos": Image.Resampling.LANCZOS}[method]
            out[..., c] = np.asarray(Image.fromarray(ch.astype(np.float32)).resize((size, size), rs))
    return out


LIGHT = np.array([1.0, 1.0, 2.0]) / np.sqrt(6.0)


def shade_gray(nrm: np.ndarray) -> np.ndarray:
    """Lambertian shading under a single parallel light, as grey uint8."""
    return np.round(np.clip(nrm @ LIGHT, 0, 1) * 255).astype(np.uint8)
