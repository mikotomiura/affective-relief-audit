"""原稿の図 3（source/media/image3.png）から 3 枚の高さを取り戻し、形の指紋を測る。

図 3 の作り（2026-10-24 に画像から確かめた）:
  - 6000 x 2160 の画像に 3 枚が並ぶ。各枚は太さ約 7 px の黒い枠の内側の 1872 x 1872。
  - 各枚は 1 辺 256 個のブロックを最近傍で拡大したもの。描いた格子は 256 x 256（表 2 の 128 ではない）。
  - 色は gist_earth（256 色）に soft-light の陰影をかけたもの（matplotlib の LightSource.shade の
    blend_mode="soft" と同じ式）。soft-light は明るさ I について線形なので、各点で
    「色地図の番号 c と明るさ I」を最小二乗で当てると、色の誤差は 1/255 未満に収まる。
  - c / 255 が min-max した高さ（256 段に量子化）になる。

指紋（generator の出力にも同じ関数をかけて比べる）:
  cycles_x, cycles_y  各軸の主な周期数（領域あたり）。行（列）ごとに正弦を最小二乗で当てた説明率の和が
                      最大になる周波数。整数でない周期数（Calm の約 1.5）も測れる
  harmonic3           3 次と 1 次の振幅の比。正弦なら 0、矩形波なら 1/3
  speckle             4 近傍のラプラシアンの絶対値の中央値（面の中のざらつき。縁には引きずられない）
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIG3 = ROOT / "source" / "media" / "image3.png"

# 各枚の内側の左上 (x0, y0) と 1 辺の長さ。枠は列 (87, 1974)・(2057, 3944)・(4027, 5914)、行 (137, 2024)
PANELS = {"calm": (95, 145), "anger": (2065, 145), "complex": (4035, 145)}
SIDE = 1872


def _lut(name: str = "gist_earth", n: int = 256) -> np.ndarray:
    import matplotlib

    return np.asarray(matplotlib.colormaps[name].resampled(n)(np.arange(n))[:, :3])


def load_image(path: Path = FIG3) -> np.ndarray:
    from PIL import Image

    return np.asarray(Image.open(path).convert("RGB")).astype(float) / 255


def block_grid(P: np.ndarray, n: int = 256) -> np.ndarray:
    """最近傍で拡大した枚から、ブロックの中心の色を拾って元の格子に戻す。

    隣と色が変わる列（行）を境目とみなす。図 3 では内側に 255 本の境目があり、最初と最後の
    ブロックは枠に半分ほど隠れている。色が平らに続く模様では境目を数えられないので、
    数が n と合わなければ止める。
    """
    def centers(axis):
        changed = (np.abs(np.diff(P, axis=axis)).sum(-1) > 0).mean(1 - axis)
        e = np.r_[0, np.where(changed > 0.5)[0] + 1, P.shape[1 - axis]]
        if len(e) - 1 != n:
            raise ValueError(f"ブロックが {len(e) - 1} 個（{n} 個のはず）")
        return (e[:-1] + e[1:]) // 2

    return P[np.ix_(centers(0), centers(1))]


def soft_light_inverse(G: np.ndarray, lut: np.ndarray | None = None):
    """色 G (h, w, 3) を、soft-light 合成 out = L^2 + I (2L - 2L^2) の (c, I) に戻す。

    返り値は (c: 色地図の番号, I: 明るさ, err: 色の誤差 (0-1 の RGB の距離))。
    """
    L = _lut() if lut is None else lut
    a, b = L**2, 2 * L - 2 * L**2
    flat = G.reshape(-1, 3)
    c = np.empty(len(flat), int)
    I = np.empty(len(flat))
    err = np.empty(len(flat))
    bb = np.maximum((b**2).sum(-1), 1e-12)
    for s in range(0, len(flat), 8192):
        r = flat[s : s + 8192, None, :] - a[None]
        i = np.clip((r * b[None]).sum(-1) / bb[None], 0, 1)
        e = np.sqrt(((r - i[..., None] * b[None]) ** 2).sum(-1))
        k = e.argmin(1)
        idx = np.arange(len(k))
        c[s : s + 8192], I[s : s + 8192], err[s : s + 8192] = k, i[idx, k], e[idx, k]
    sh = G.shape[:2]
    return c.reshape(sh), I.reshape(sh), err.reshape(sh)


def panels(path: Path = FIG3) -> dict:
    """3 枚の {name: {"height": [0,1] の 256 x 256, "shade": I, "err": 色の誤差}}。"""
    im = load_image(path)
    out = {}
    for name, (x0, y0) in PANELS.items():
        G = block_grid(im[y0 : y0 + SIDE, x0 : x0 + SIDE])
        c, I, err = soft_light_inverse(G)
        out[name] = {"height": c / 255.0, "shade": I, "err": err}
    return out


# ---------------------------------------------------------------- 指紋


def _sine_power(rows: np.ndarray, freqs: np.ndarray) -> np.ndarray:
    """各周波数で、行ごとに a sin + b cos + c を当てたときの説明された分散の合計。"""
    n = rows.shape[1]
    x = np.arange(n) / n
    R = rows - rows.mean(1, keepdims=True)
    out = np.empty(len(freqs))
    for j, f in enumerate(freqs):
        B = np.column_stack([np.sin(2 * np.pi * f * x), np.cos(2 * np.pi * f * x), np.ones(n)])
        coef, *_ = np.linalg.lstsq(B, R.T, rcond=None)
        out[j] = ((B @ coef) ** 2).sum()
    return out / (R**2).sum()


def dominant_cycles(H: np.ndarray, axis: int = 1, fmax: float = 20.0, step: float = 0.05) -> float:
    """axis=1 は横（x）方向、axis=0 は縦（y）方向の、領域あたりの主な周期数。"""
    rows = H if axis == 1 else H.T
    freqs = np.arange(0.5, fmax + step / 2, step)
    return float(freqs[_sine_power(rows, freqs).argmax()])


def harmonic3(H: np.ndarray, f: float, axis: int = 1) -> float:
    """周期数 f の 3 次と 1 次の振幅の比（行ごとに当て、振幅を足し合わせる）。"""
    rows = H if axis == 1 else H.T
    n = rows.shape[1]
    x = np.arange(n) / n
    R = rows - rows.mean(1, keepdims=True)
    B = np.column_stack([np.sin(2 * np.pi * k * f * x) for k in (1, 3)]
                        + [np.cos(2 * np.pi * k * f * x) for k in (1, 3)] + [np.ones(n)])
    coef, *_ = np.linalg.lstsq(B, R.T, rcond=None)
    a1 = np.hypot(coef[0], coef[2]).sum()
    a3 = np.hypot(coef[1], coef[3]).sum()
    return float(a3 / a1)


def speckle(H: np.ndarray) -> float:
    """細かい斑点の強さ: 4 近傍のラプラシアンの絶対値の中央値（min-max した高さで）。

    中央値をとるので、矩形波の縁（面積が小さい）には引きずられず、面の中のざらつきを見る。
    純音や滑らかな場では 256 段の量子化の大きさ（約 0.004）に近くなる。
    """
    lap = 4 * H - np.roll(H, 1, 0) - np.roll(H, -1, 0) - np.roll(H, 1, 1) - np.roll(H, -1, 1)
    return float(np.median(np.abs(lap[1:-1, 1:-1])))


def fingerprint(H: np.ndarray) -> dict:
    """min-max した高さの指紋。H は正方形（図 3 は 256 x 256）。"""
    H = (H - H.min()) / (H.max() - H.min())
    cx = dominant_cycles(H, 1)
    cy = dominant_cycles(H, 0)
    return {
        "cycles_x": cx,
        "cycles_y": cy,
        "harmonic3": 0.5 * (harmonic3(H, cx, 1) + harmonic3(H, cy, 0)),
        "speckle": speckle(H),
    }


def distance(fp: dict, ref: dict) -> float:
    """指紋どうしの距離。周期数と斑点は対数の差、高調波の比はそのままの差（3 倍して重みをそろえる）。"""
    d = abs(np.log(fp["cycles_x"] / ref["cycles_x"])) + abs(np.log(fp["cycles_y"] / ref["cycles_y"]))
    d += 3 * abs(fp["harmonic3"] - ref["harmonic3"])
    # 斑点は 256 段の量子化の大きさ（約 0.004）より下を区別しない
    d += abs(np.log(max(fp["speckle"], 0.004) / max(ref["speckle"], 0.004)))
    return float(d)
