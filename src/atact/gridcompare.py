"""解像度をまたぐ比較の 2 つの記述子の写しと、その比較を合成した表面で再現する部品。

- GLCM Score: Diffusion-4K（Zhang ら, CVPR 2025）の公開コード
  （github.com/zhang0jhon/diffusion-4k、main を 2026-10-24 に取得）の `eval.py` の `gray_proc` と `glcm`。
  HiMat（Wang ら, Eurographics 2026）がこの指標で 256・512・4K の生成物を比べている。
  論文の式は s = −(1/P)ΣH(g_p) と負号つきだが、コードは正のエントロピー
  （skimage の shannon_entropy を GLCM の配列にかけたもの）を返す。ここではコードに従う。
- 継ぎ目の指標: Gao ら 2026 の公開コード（github.com/alex4727/Text2TactileGraphics）の
  `src/experiments/tiling/02_evaluate_tileability.py` と、`01_generate_tiled.py` の縮小（PIL の LANCZOS）と中央の切り出し。

取得したコードは実行せず、読んで書き写した。違いは入出力（ファイルの代わりに配列）だけである。
"""

from __future__ import annotations

import numpy as np
from PIL import Image
from skimage.feature import graycomatrix
from skimage.measure import shannon_entropy

# --- Diffusion-4K の GLCM Score ------------------------------------------------

GLCM_DIST = [1, 2, 3, 4]
GLCM_ANGLES = [0, np.pi / 4, np.pi / 2, np.pi * 3 / 4]


def gray64(gray_u8: np.ndarray) -> np.ndarray:
    """gray_proc の後半（256 階調を 4 で割って 64 階調に落とす）。入力は既に灰色の uint8。"""
    return (gray_u8.astype(np.uint8) // 4).astype(np.uint8)


def glcm_entropy(patch64: np.ndarray) -> float:
    g = graycomatrix(patch64, GLCM_DIST, GLCM_ANGLES, levels=64, normed=True)
    return float(shannon_entropy(g))


def glcm_score(gray_u8: np.ndarray, patch: int = 64) -> float:
    """main のループ。画像を patch 画素の小片に割り、小片ごとの値を平均する。"""
    g = gray64(gray_u8)
    n = g.shape[0] // patch
    s = [glcm_entropy(g[i * patch:(i + 1) * patch, j * patch:(j + 1) * patch])
         for i in range(n) for j in range(n)]
    return float(np.mean(s))


# --- Gao ら 2026 の継ぎ目の指標 --------------------------------------------------


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


# --- 解析的な場（ここからは本研究の手順） ------------------------------------------


def field_and_grad(f: float, octaves: int, n: int, seed: int, x0: float = 0.0, y0: float = 0.0,
                   max_freq: float | None = None):
    """窓 [x0, x0+1) x [y0, y0+1) の上の場 F と、その解析的な勾配（領域の 1 辺を 1 とする単位）。

    各段 sin(2π f_o x + φ) sin(2π f_o y + ψ)、f_o = f 2^o、振幅 0.5^o。位相の引き方は atact.field と同じ。
    max_freq を与えると、f_o がそれを超える段を落とす（その格子の生成器が作れない細部を持たせない）。
    乱数は落とした段の分も引くので、残る段の位相は max_freq によらず同じになる。
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
    """整数の f の周期的な場で、傾きの大きさの RMS が rms_slope になる高さの倍率 H0（すべての段を含む）。

    各段の勾配の各成分の二乗平均は a^2 w^2 / 4、段どうしの交差項は平均 0。
    """
    s2 = sum((0.5**o) ** 2 * (2 * np.pi * f * 2**o) ** 2 / 2 for o in range(octaves))
    return rms_slope / np.sqrt(s2)


def normals_from_grad(zx: np.ndarray, zy: np.ndarray) -> np.ndarray:
    """OpenGL 規約の単位法線（H x W x 3、浮動小数）。atact.hfratio.normal_rgb_from_height と同じ向き。"""
    v = np.stack([-zx, zy, np.ones_like(zx)], axis=-1)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def to_rgb_u8(nrm: np.ndarray) -> np.ndarray:
    return np.round((nrm + 1.0) / 2.0 * 255).astype(np.uint8)


def upsample(img: np.ndarray, size: int, method: str) -> np.ndarray:
    """H x W x C の浮動小数の図を、成分ごとに size へ拡大する。

    method: "fourier"（周期的な場に対する帯域制限の補間。DFT の零詰め）、
    PIL の "nearest" / "bilinear" / "bicubic" / "lanczos"（浮動小数の画像で行う）。
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
    """平行光 1 つのランバートの陰影を、灰色の uint8 にする。"""
    return np.round(np.clip(nrm @ LIGHT, 0, 1) * 255).astype(np.uint8)
