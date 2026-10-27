"""Graphical abstract for the journal (an illustration only; no number in the paper comes from it).

    uv run python tools/graphical_abstract.py

Output: docs/media/graphical-abstract.png, 525 pixels wide (the width the journal asks for). Three inputs of equal
arousal and different valence go through the rule; the reliefs are drawn on one height scale shared by all works
(top) and exported image by image with min-max scaling (bottom). The surfaces are those of tools/readme_media.py: the
field of the paper (atact.field.height) with one fixed seed.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from PIL import Image

from atact.mapping import params
from readme_media import INK, OUT, S_MAX, relief, surface

WIDTH_PX = 525
DPI = 100
POINTS = ((-0.8, 0.0), (0.0, 0.0), (0.8, 0.0))  # valence V, arousal A
COLOURS = ("#0969da", "#8250df", "#cf222e")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 8, "text.color": INK, "axes.labelcolor": INK,
                         "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK})
    fig = plt.figure(figsize=(WIDTH_PX / DPI, 4.1), facecolor="white")
    fig.text(0.5, 0.965, "A rule from affect to relief, and what a min–max export keeps", ha="center",
             fontsize=9.5, fontweight="bold")

    sq = fig.add_axes([0.10, 0.44, 0.22, 0.36])
    sq.set_xlim(-1, 1), sq.set_ylim(-1, 1), sq.set_aspect("equal")
    sq.set_xticks([-1, 0, 1]), sq.set_yticks([-1, 0, 1])
    sq.set_xlabel("valence V"), sq.set_ylabel("arousal A")
    sq.set_title("input", fontsize=8)
    for (V, A), c in zip(POINTS, COLOURS):
        sq.plot([V], [A], "o", color=c, ms=6)

    x0, w, gap = 0.37, 0.19, 0.015
    rows = ((0.47, "one height scale shared by all works"), (0.04, "min–max export of each image"))
    for k, ((V, A), c) in enumerate(zip(POINTS, COLOURS)):
        f, s, g = params(V, A)
        H = surface(V, A)
        for r, (y, label) in enumerate(rows):
            ax = fig.add_axes([x0 + k * (w + gap), y, w, 0.30])
            if r == 0:
                img = relief(H, -S_MAX, S_MAX, exag=0.35)
                ax.set_title(f"V = {V:+.1f}\ns = {s:.2f}", fontsize=7.5, color=c)
            else:
                img = relief(H, H.min(), H.max(), 0.35 * 2 * S_MAX / (H.max() - H.min()))
            ax.imshow(img, interpolation="bilinear")
            ax.set_xticks([]), ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_color(c), sp.set_linewidth(1.2)
            if k == 1:
                ax.text(0.5, 1.30 if r == 0 else 1.06, label, transform=ax.transAxes, ha="center", fontsize=7.5)
    fig.text(0.04, 0.20, "Valence alone sets\nthe amplitude s;\nthe export removes it.", fontsize=7.5, va="center")
    path = OUT / "graphical-abstract.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    with Image.open(path) as im:
        print(path.name, im.size, f"{path.stat().st_size / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
