"""Logo and animations for the README (illustrations only; no number in the paper comes from them).

    uv run python tools/readme_media.py

Output: docs/media/logo-light.png and logo-dark.png, docs/media/rule.gif (the input point moves over the square of valence and arousal and the
relief follows the rule), docs/media/export.gif (the same reliefs on one common height scale and under a per-image
min-max export). Every surface uses the field of the paper (atact.field.height) with one fixed seed, so a frame differs
from the next only through the parameters (f, s, gamma).
"""

from __future__ import annotations

import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LightSource  # noqa: E402
from PIL import Image  # noqa: E402

from atact.field import RenderConfig, height  # noqa: E402
from atact.mapping import S0, S1, params  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "media"
SEED = 7
N = 160
S_MAX = S0 + S1  # 0.30, the largest amplitude of the rule
CMAP = plt.get_cmap("gist_earth")
LIGHT = LightSource(azdeg=315, altdeg=40)
INK = "#57606a"  # mid grey, legible on light and dark backgrounds
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK})


def relief(H: np.ndarray, lo: float, hi: float, exag: float) -> np.ndarray:
    """Shaded colour image of a height map; lo and hi fix the colour scale (common scale) or follow H (min-max)."""
    z = (H - lo) / (hi - lo)
    return LIGHT.shade(z, cmap=CMAP, vert_exag=exag, dx=1.0 / N, dy=1.0 / N, blend_mode="soft", vmin=0.0, vmax=1.0)


def surface(V: float, A: float) -> np.ndarray:
    return height(V, A, RenderConfig(n=N), seed=SEED)


def fig_to_image(fig) -> Image.Image:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, transparent=False, facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def save_gif(frames: list[Image.Image], path: Path, ms: int) -> None:
    pal = frames[len(frames) // 2].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    q[0].save(path, save_all=True, append_images=q[1:], duration=ms, loop=0, optimize=True, disposal=1)


def logo() -> None:
    """Two versions for light and dark page backgrounds (the README picks one with prefers-color-scheme)."""
    H = surface(0.4, -0.6)
    img = relief(H, -S_MAX, S_MAX, exag=0.35)
    for name, ink in (("logo-light.png", "#57606a"), ("logo-dark.png", "#c9d1d9")):
        fig = plt.figure(figsize=(9.0, 2.0), facecolor="none")
        ax = fig.add_axes([0.0, 0.0, 2.0 / 9.0, 1.0])
        ax.imshow(img, interpolation="bilinear")
        ax.set_axis_off()
        fig.text(0.255, 0.60, "affective-relief-audit", fontsize=28, fontweight="bold", va="center", color=ink)
        fig.text(0.255, 0.30, "a generative rule from affect to tactile relief, read as mathematics", fontsize=12.5,
                 va="center", color=ink)
        fig.savefig(OUT / name, dpi=120, transparent=True)
        plt.close(fig)


def path_points(k: int) -> list[tuple[float, float]]:
    t = np.linspace(0.0, 2.0 * np.pi, k, endpoint=False)
    return [(0.85 * np.cos(a), 0.85 * np.sin(a)) for a in t]


def rule_gif() -> None:
    frames = []
    pts = path_points(60)
    trail = np.array(pts + pts[:1])  # closed loop
    for V, A in pts:
        f, s, g = params(V, A)
        H = surface(V, A)
        fig = plt.figure(figsize=(6.4, 3.0), facecolor="white")
        a = fig.add_axes([0.11, 0.17, 0.31, 0.70])
        a.plot(trail[:, 0], trail[:, 1], color="#d0d7de", lw=1.0)
        a.plot([V], [A], "o", color="#cf222e", ms=8)
        a.set_xlim(-1, 1), a.set_ylim(-1, 1), a.set_aspect("equal")
        a.set_xticks([-1, 0, 1]), a.set_yticks([-1, 0, 1])
        a.set_xlabel("valence V"), a.set_ylabel("arousal A")
        a.set_title("input", fontsize=10)
        b = fig.add_axes([0.52, 0.05, 0.40, 0.85])
        b.imshow(relief(H, -S_MAX, S_MAX, exag=0.35), interpolation="bilinear")
        b.set_axis_off()
        b.set_title(f"relief   f = {f:.2f}   s = {s:.2f}   γ = {g:.2f}", fontsize=10)
        frames.append(fig_to_image(fig))
    save_gif(frames, OUT / "rule.gif", ms=90)


def export_gif() -> None:
    frames = []
    Vs = np.concatenate([np.linspace(-1, 1, 30), np.linspace(1, -1, 30)])
    row = N // 3
    x = np.arange(N) / N
    for V in Vs:
        f, s, g = params(V, 0.0)
        H = surface(float(V), 0.0)
        mm = (H - H.min()) / (H.max() - H.min())
        common = (H + S_MAX) / (2 * S_MAX)
        fig = plt.figure(figsize=(6.4, 3.4), facecolor="white")
        for i, (img, prof, title) in enumerate(
            ((relief(H, -S_MAX, S_MAX, 0.35), common, "one common height scale"),
             (relief(H, H.min(), H.max(), 0.35 * 2 * S_MAX / (H.max() - H.min())), mm, "per-image min–max"))):
            ax = fig.add_axes([0.05 + 0.5 * i, 0.30, 0.40, 0.58])
            ax.imshow(img, interpolation="bilinear")
            ax.axhline(row, color="white", lw=1.0, ls="--")
            ax.set_axis_off()
            ax.set_title(title, fontsize=10)
            p = fig.add_axes([0.05 + 0.5 * i, 0.08, 0.40, 0.18])
            p.plot(x, prof[row], color="#cf222e", lw=1.0)
            p.set_ylim(0, 1), p.set_xlim(0, 1)
            p.set_xticks([]), p.set_yticks([0, 1]), p.set_yticklabels(["0", "D"])
        fig.text(0.5, 0.95, f"V = {V:+.2f} (A = 0)   amplitude s = {s:.2f}", ha="center", fontsize=10)
        frames.append(fig_to_image(fig))
    save_gif(frames, OUT / "export.gif", ms=90)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    logo()
    rule_gif()
    export_gif()
    for f in ("logo-light.png", "logo-dark.png", "rule.gif", "export.gif"):
        print(f, f"{(OUT / f).stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
