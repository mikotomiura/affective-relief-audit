"""Recover the heights of the three panels of Fig. 3 of Harada (2026) (source/media/image3.png) and measure shape fingerprints.

Structure of Fig. 3 (checked on the image, 2026-10-24):
  - Three panels in a 6000 x 2160 image. Each panel is 1872 x 1872 inside a black frame about 7 px thick.
  - Each panel is a nearest-neighbour enlargement of blocks, 256 per side. The grid drawn is 256 x 256 (not the 128 of Table 2).
  - The colour is gist_earth (256 colours) with soft-light shading (the same formula as blend_mode="soft" of
    matplotlib LightSource.shade). Soft-light is linear in the intensity I, so fitting, at each point, the
    colour-map index c and the intensity I by least squares gives a colour error below 1/255.
  - c / 255 is the min-max height (quantised to 256 levels).

Fingerprints (the same functions are applied to the output of the generator for comparison):
  cycles_x, cycles_y  dominant number of cycles along each axis (per domain): the frequency maximising the summed variance explained by a least-squares sinusoid per row (column). Non-integer numbers
                      of cycles (about 1.5 for Calm) can also be measured
  harmonic3           ratio of the amplitudes of the 3rd and 1st harmonics: 0 for a sine, 1/3 for a square wave
  speckle             median of the absolute 4-neighbour Laplacian (roughness inside faces; not dominated by edges)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIG3 = ROOT / "source" / "media" / "image3.png"

# Top-left corner (x0, y0) and side length of the inside of each panel. Frames at columns (87, 1974), (2057, 3944), (4027, 5914), rows (137, 2024)
PANELS = {"calm": (95, 145), "anger": (2065, 145), "complex": (4035, 145)}
SIDE = 1872


def _lut(name: str = "gist_earth", n: int = 256) -> np.ndarray:
    import matplotlib

    return np.asarray(matplotlib.colormaps[name].resampled(n)(np.arange(n))[:, :3])


def load_image(path: Path = FIG3) -> np.ndarray:
    from PIL import Image

    return np.asarray(Image.open(path).convert("RGB")).astype(float) / 255


def block_grid(P: np.ndarray, n: int = 256) -> np.ndarray:
    """From a panel enlarged by nearest neighbour, take the colour at each block centre and return to the original grid.

    A column (row) where the colour differs from its neighbour is taken as a block boundary. In Fig. 3 there are 255 boundaries inside;
    the first and last blocks are about half hidden by the frame. For a pattern with flat runs of colour the boundaries cannot be counted,
    so the function stops if their number does not match n.
    """
    def centers(axis):
        changed = (np.abs(np.diff(P, axis=axis)).sum(-1) > 0).mean(1 - axis)
        e = np.r_[0, np.where(changed > 0.5)[0] + 1, P.shape[1 - axis]]
        if len(e) - 1 != n:
            raise ValueError(f"{len(e) - 1} blocks found ({n} expected)")
        return (e[:-1] + e[1:]) // 2

    return P[np.ix_(centers(0), centers(1))]


def soft_light_inverse(G: np.ndarray, lut: np.ndarray | None = None):
    """Invert the soft-light composite out = L^2 + I (2L - 2L^2) to (c, I) from the colour G (h, w, 3).

    Returns (c: colour-map index, I: intensity, err: colour error (RGB distance in 0-1)).
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
    """For the three panels, {name: {"height": [0,1] array of 256 x 256, "shade": I, "err": colour error}}."""
    im = load_image(path)
    out = {}
    for name, (x0, y0) in PANELS.items():
        G = block_grid(im[y0 : y0 + SIDE, x0 : x0 + SIDE])
        c, I, err = soft_light_inverse(G)
        out[name] = {"height": c / 255.0, "shade": I, "err": err}
    return out


# ---------------------------------------------------------------- fingerprints


def _sine_power(rows: np.ndarray, freqs: np.ndarray) -> np.ndarray:
    """Total explained variance when a sin + b cos + c is fitted row by row at each frequency."""
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
    """Dominant number of cycles per domain along axis=1 (horizontal, x) or axis=0 (vertical, y)."""
    rows = H if axis == 1 else H.T
    freqs = np.arange(0.5, fmax + step / 2, step)
    return float(freqs[_sine_power(rows, freqs).argmax()])


def harmonic3(H: np.ndarray, f: float, axis: int = 1) -> float:
    """Ratio of the 3rd to the 1st harmonic amplitude at f cycles (fitted row by row, amplitudes summed)."""
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
    """Strength of fine speckle: median of the absolute 4-neighbour Laplacian (on the min-max height).

    Because it is a median, it is not dominated by the edges of a square wave (small area) and measures roughness inside faces.
    For a pure tone or a smooth field it is close to the 256-level quantisation size (about 0.004).
    """
    lap = 4 * H - np.roll(H, 1, 0) - np.roll(H, -1, 0) - np.roll(H, 1, 1) - np.roll(H, -1, 1)
    return float(np.median(np.abs(lap[1:-1, 1:-1])))


def fingerprint(H: np.ndarray) -> dict:
    """Fingerprint of the min-max height. H is square (256 x 256 for Fig. 3)."""
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
    """Distance between fingerprints: log difference for cycles and speckle, plain difference for the harmonic ratio (times 3 to equalise weights)."""
    d = abs(np.log(fp["cycles_x"] / ref["cycles_x"])) + abs(np.log(fp["cycles_y"] / ref["cycles_y"]))
    d += 3 * abs(fp["harmonic3"] - ref["harmonic3"])
    # Speckle below the 256-level quantisation size (about 0.004) is not distinguished
    d += abs(np.log(max(fp["speckle"], 0.004) / max(ref["speckle"], 0.004)))
    return float(d)
