"""Figures of the text example of Section 6, redrawn from the stored results (version 2 of the conditions).

Usage:  uv run python experiments/text_path_figures.py           (check the stored results, redraw, write the figures;
                                                                  refuses to overwrite)
Conditions: experiments/conditions/text_path_example.json, item 'figures_v2'
Input:  results/text_path_example.json (checked against the SHA-256 of the conditions; no value is recomputed)
Output: results/figs/fig5_text_path_B.pdf (main), results/figs/figS_text_path_AB.pdf and
        results/figs/figS_text_path_AB_nofunction.pdf (supplement), results/text_path_figures.json (the checks, the label
        boxes and the plotted grey levels). The PDFs are not byte-reproducible (usetex font subsets).

The tiles are generated again from (f, s, gamma), the seed and eps of the stored results with the tile() of the run
(experiments/text_path_example.py), after checking that the run script, the library and numpy/scipy are those recorded
in the stored results. Every readout stored for the grid of the figure is compared with the regenerated one. All
figures are drawn into a temporary directory and moved into results/ only when every check has passed.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text_path_example as run_  # noqa: E402

ROOT = run_.ROOT
OUT_ROOT = ROOT  # where the outputs go (tests point it to a temporary directory)
SCRIPT = Path(__file__).resolve()
SOURCE = run_.OUT_JSON
OUT_JSON_REL = "results/text_path_figures.json"
TOL = 1e-12
TEXT_COLOUR = {"A": "k", "B": "#d95f02"}
PATH_STYLE = {"main": dict(marker="o", ls="-"), "function_words_removed": dict(marker="s", ls="--")}
LABEL_DIST_PT = 7.0
POINT_FREE_PT = 3.0

INTERPRETATION = [
    "The stored results are read only after their SHA-256 has been compared with 'figures_v2.source_sha256' of the "
    "conditions. The run script, the library files and the versions of numpy and scipy must equal those recorded in "
    "the stored results. The tiles use the grid 'figures_v2.grid_N' (checked against the first grid of the results), "
    "and every readout stored for that grid is compared with the regenerated one to within 1e-12 (booleans exactly) "
    "before any figure is drawn. These readouts do not fix the image pixel by pixel; the identity of the images rests "
    "on the identity of the code and the inputs.",
    "Panel (a) shows the window [-w, w]^2 of the (V, A) plane, w from the conditions; the script stops before "
    "drawing if a shown point of any figure lies outside its window. An inset shows the whole square [-1, 1]^2 with "
    "the window as a rectangle; the centre (0, 0) is marked with a cross in both.",
    "Labels: coincident points of one text share one label ('(no term)' only when all of them are unmatched; a mix "
    "stops the script). After the layout is drawn, each label is placed 7 pt from its point in the first of eight "
    "directions (ordered by their angle to the direction away from the mean of the distinct shown points) in which "
    "it stays inside panel (a) and overlaps no earlier label, the legend, the inset, a point or the centre cross "
    "(3 pt around each). The layout is drawn again and every condition is checked on the final boxes; the script "
    "stops if one fails.",
    "All figures are drawn into a temporary directory; they and the JSON are moved into results/ only after every "
    "figure has been drawn. The script refuses to start if any of its outputs exists.",
]


def conditions() -> dict:
    c = run_.load_conditions()
    if c["version"] < 2 or "figures_v2" not in c:
        raise SystemExit("the conditions have no 'figures_v2' (version 2)")
    return c


def source_sha256(c: dict) -> str:
    return c["figures_v2"]["source_sha256"]


def load_source(c: dict, path: Path) -> dict:
    if run_.sha256(path) != source_sha256(c):
        raise SystemExit(f"{path} differs from the results named in the conditions")
    return json.loads(path.read_text())


def check_code(res: dict) -> dict:
    """The run script, the library and numpy/scipy must be those that produced the stored results."""
    import scipy

    m = res["meta"]
    now = {"script_sha256": run_.sha256(run_.SCRIPT),
           "library_sha256": {str(p.relative_to(ROOT)): run_.sha256(p) for p in run_.LIBS},
           "numpy": np.__version__, "scipy": scipy.__version__}
    for k, v in now.items():
        if m[k] != v:
            raise SystemExit(f"{k} differs from the one recorded in the stored results")
    return now


def compare(stored, new, where: str, worst: list) -> None:
    """Every stored readout against the regenerated one: numbers to within TOL, booleans exactly."""
    if isinstance(stored, dict):
        if set(stored) != set(new):
            raise SystemExit(f"the readouts of {where} differ in their keys")
        for k in stored:
            compare(stored[k], new[k], f"{where}/{k}", worst)
    elif isinstance(stored, bool) or isinstance(new, bool):
        if stored is not new:
            raise SystemExit(f"{where} differs from the stored value")
    else:
        dev = abs(float(new) - float(stored))
        worst[0] = max(worst[0], dev)
        if not dev <= TOL:
            raise SystemExit(f"{where} differs from the stored value by {dev}")


def redraw_tiles(res: dict, n: int) -> tuple[dict, dict]:
    """Tiles at grid n from the stored (f, s, gamma), checked against every readout stored for that grid."""
    a = res["analysis"]
    if n != a["grids_N"][0]:
        raise SystemExit(f"N = {n} is not the first grid of the stored results")
    images, worst = {}, [0.0]
    for name, t in a["texts"].items():
        for v in run_.VARIANTS:
            for i, r in enumerate(t["variants"][v]):
                p = {"f": r["f"], "s": r["s"], "gamma": r["gamma"]}
                x = run_.tile(p, n, a["seed"], a["eps"], a["dimensions"])
                compare(r["grids"][str(n)], {k: val for k, val in x.items() if k != "z"}, f"{name}{i + 1} {v}",
                        worst)
                images[(name, v, i)] = x["z"]
    return images, {"N": n, "max_abs_dev": worst[0]}


def label_groups(rows: list[dict], name: str) -> list[tuple[tuple[float, float], str]]:
    groups: dict[tuple[float, float], list[int]] = {}
    for i, r in enumerate(rows):
        groups.setdefault((r["V"], r["A"]), []).append(i)
    out = []
    for xy, idx in groups.items():
        flags = {rows[i]["unmatched"] for i in idx}
        if len(flags) > 1:
            raise SystemExit(f"matched and unmatched sentences of text {name} coincide at {xy}")
        out.append((xy, ",".join(f"{name}{i + 1}" for i in idx) + (" (no term)" if flags == {True} else "")))
    return out


def directions(x: float, y: float, centre: np.ndarray) -> list[tuple[float, float]]:
    """Eight unit directions, ordered by their angle to the direction away from the centre (upwards at the centre)."""
    d = np.array([x, y]) - centre
    a0 = float(np.arctan2(d[1], d[0])) if np.hypot(*d) > 1e-9 else np.pi / 2
    angles = [k * np.pi / 4 for k in range(8)]
    angles.sort(key=lambda a: (abs((a - a0 + np.pi) % (2 * np.pi) - np.pi), a))
    return [(float(np.cos(a)), float(np.sin(a))) for a in angles]


def alignment(ux: float, uy: float) -> tuple[str, str]:
    return ("left" if ux > 1e-9 else ("right" if ux < -1e-9 else "center"),
            "bottom" if uy > 1e-9 else ("top" if uy < -1e-9 else "center"))


def free_of(b, inside, others: list, points: list, half: float) -> bool:
    return (b.x0 >= inside.x0 and b.x1 <= inside.x1 and b.y0 >= inside.y0 and b.y1 <= inside.y1
            and not any(b.overlaps(o) for o in others)
            and not any(b.x0 < px + half and b.x1 > px - half and b.y0 < py + half and b.y1 > py - half
                        for px, py in points))


def place_labels(ax, fig, labels: list[tuple[str, tuple[float, float], str]], colours: dict,
                 obstacles: list) -> list:
    """Place each label in the first of eight directions in which its box stays inside the axes and overlaps no
    label placed before, no obstacle (legend, inset), no plotted point and not the centre. Stops if none fits.
    The layout must have been drawn (aspect applied) before this is called."""
    r = fig.canvas.get_renderer()
    pts = [ax.transData.transform(xy) for _, xy, _ in labels] + [ax.transData.transform((0.0, 0.0))]
    half = POINT_FREE_PT * fig.dpi / 72
    inside = ax.get_window_extent(r)
    centre = np.mean(np.array(sorted({xy for _, xy, _ in labels})), axis=0)
    boxes, texts = list(obstacles), []
    for name, (x, y), lab in labels:
        for ux, uy in directions(x, y, centre):
            ha, va = alignment(ux, uy)
            t = ax.annotate(lab, (x, y), xytext=(LABEL_DIST_PT * ux, LABEL_DIST_PT * uy),
                            textcoords="offset points", fontsize=7, ha=ha, va=va, color=colours[name])
            b = t.get_window_extent(r)
            if free_of(b, inside, boxes, pts, half):
                boxes.append(b)
                texts.append((t, lab, x, y, (ux, uy)))
                break
            t.remove()
        else:
            raise SystemExit(f"no place for the label {lab!r}")
    return texts


def final_label_check(ax, fig, texts: list, obstacles_of) -> list[dict]:
    """Draw the finished layout again and check every label box on it."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inside = ax.get_window_extent(r)
    half = POINT_FREE_PT * fig.dpi / 72
    pts = [ax.transData.transform((x, y)) for _, _, x, y, _ in texts] + [ax.transData.transform((0.0, 0.0))]
    boxes = [t.get_window_extent(r) for t, *_ in texts]
    obstacles = obstacles_of(r)
    out = []
    for j, ((t, lab, x, y, d), b) in enumerate(zip(texts, boxes)):
        if not free_of(b, inside, obstacles + boxes[:j] + boxes[j + 1:], pts, half):
            raise SystemExit(f"the label {lab!r} overlaps or leaves panel (a) in the final layout")
        out.append({"label": lab, "V": x, "A": y, "direction": list(d), "box_px": box(b)})
    return {"labels": out, "obstacles_px": [box(o) for o in obstacles],
            "points_px": [[float(px), float(py)] for px, py in pts], "point_free_px": float(half),
            "panel_px": box(inside)}


def box(b) -> list[float]:
    return [float(b.x0), float(b.y0), float(b.x1), float(b.y1)]


def check_windows(res: dict, figs: list[dict]) -> None:
    for s in figs:
        for name in s["texts"]:
            for i, r in enumerate(res["analysis"]["texts"][name]["variants"][s["variant"]]):
                if max(abs(r["V"]), abs(r["A"])) > s["window"]:
                    raise SystemExit(f"{name}{i + 1} ({s['variant']}) lies outside the window {s['window']}")


def figure(res: dict, images: dict, variant: str, texts: list[str], w: float, path: Path) -> dict:
    import matplotlib

    matplotlib.use("agg")  # the agg canvas measures the labels; savefig still writes a PDF
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    plt.rcParams.update({
        "text.usetex": True, "font.family": "serif", "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
        "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
        "lines.linewidth": 1.0, "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "pdf.fonttype": 42,
        "savefig.dpi": 600,  # images (tiles) at 600 dpi in the PDF, not resampled to 100 dpi
    })
    a = res["analysis"]
    D = a["dimensions"]["D"]
    rows_of = {name: a["texts"][name]["variants"][variant] for name in texts}
    check_windows(res, [{"variant": variant, "texts": texts, "window": w}])
    cols: list[tuple[str, int] | None] = []
    for j, name in enumerate(texts):
        if j:
            cols.append(None)
        cols += [(name, i) for i in range(len(rows_of[name]))]
    widths = [3.0, 0.5] + [0.25 if c is None else 1.0 for c in cols]
    fig = plt.figure(figsize=(1.9 + 0.62 * len(cols), 2.3))
    gs = fig.add_gridspec(3, len(widths), width_ratios=widths, wspace=0.08, hspace=0.08)
    ax = fig.add_subplot(gs[:, 0])
    labels = [(name, xy, lab) for name in texts for xy, lab in label_groups(rows_of[name], name)]
    ax.plot([0], [0], marker="+", ms=6, color="0.5", mew=0.6, ls="none")
    for name in texts:
        rows = rows_of[name]
        V, A = [r["V"] for r in rows], [r["A"] for r in rows]
        ax.plot(V, A, lw=0.7, ms=3, color=TEXT_COLOUR[name], label=f"text {name}", **PATH_STYLE[variant])
        un = [i for i, r in enumerate(rows) if r["unmatched"]]
        if un:
            ax.plot([V[i] for i in un], [A[i] for i in un], ls="none", marker="o", ms=7, mfc="none",
                    mec=TEXT_COLOUR[name], mew=0.7)
    ax.set(xlabel="$V$", ylabel="$A$", xlim=(-w, w), ylim=(-w, w), aspect="equal",
           xticks=[-w, 0, w], yticks=[-w, 0, w], title=r"(a) path of the sentences")
    leg = ax.legend(loc="upper left", frameon=False, handlelength=1.6)
    ins = ax.inset_axes([0.70, 0.70, 0.28, 0.28])
    ins.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], color="k", lw=0.4)
    ins.add_patch(Rectangle((-w, -w), 2 * w, 2 * w, fill=False, lw=0.4, ec="0.4"))
    ins.plot([0], [0], marker="+", ms=3, color="0.5", mew=0.4, ls="none")
    ins.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), aspect="equal", xticks=[], yticks=[])
    for sp in ins.spines.values():
        sp.set_visible(False)
    names = {"common": "common", "minmax": "min--max", "common_eps": r"common, $T_{\gamma,\varepsilon}$"}
    plotted = []
    for k, e in enumerate(run_.EXPORTS):
        for m, col in enumerate(cols):
            if col is None:
                continue
            name, i = col
            t = fig.add_subplot(gs[k, m + 2])
            z = images[(name, variant, i)][e]
            grey = z / D if e == "minmax" else z / D + 0.5
            t.imshow(grey, cmap="gray", vmin=0, vmax=1, interpolation="nearest", origin="lower")
            t.set_xticks([])
            t.set_yticks([])
            for sp in t.spines.values():
                sp.set_linewidth(0.3)
            if k == 0:
                t.set_title(f"{name}{i + 1}", pad=2)
            if m == 0:
                t.set_ylabel(names[e], fontsize=6)
            plotted.append({"export": e, "text": name, "sentence": i + 1, "grey_min": float(grey.min()),
                            "grey_max": float(grey.max())})
    x0 = fig.axes[-len(plotted)].get_position().x0
    x1 = fig.axes[-1].get_position().x1
    fig.text((x0 + x1) / 2, 0.99, rf"(b) one tile per sentence, $N = {a['grids_N'][0]}$", ha="center", va="bottom")
    fig.canvas.draw()  # apply the equal aspect before measuring
    r = fig.canvas.get_renderer()
    texts_ = place_labels(ax, fig, labels, TEXT_COLOUR, [leg.get_window_extent(r), ins.get_window_extent(r)])
    placed = final_label_check(ax, fig, texts_, lambda r_: [leg.get_window_extent(r_), ins.get_window_extent(r_)])
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, metadata={"CreationDate": None, "Creator": "experiments/text_path_figures.py",
                                "Producer": None})
    plt.close(fig)
    return {"variant": variant, "texts": texts, "window": w, **placed, "grey": plotted}


def specs(c: dict) -> list[dict]:
    f = c["figures_v2"]
    return [f["main"]] + f["supplement"]


def outputs(c: dict) -> list[str]:
    """Published paths (relative to OUT_ROOT) of all outputs: the figures, then the JSON."""
    out = [s["file"] for s in specs(c)] + [OUT_JSON_REL]
    if len(set(out)) != len(out):
        raise SystemExit("two outputs share a path")
    return out


def git_state() -> dict:
    """As in the run, with this script and the stored results added; a failing git stops the script."""
    def git(*a):
        try:
            return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as e:
            raise SystemExit(f"git {' '.join(a)} failed: {e}") from e

    git("ls-files", "--error-unmatch", "experiments/text_path_figures.py", "experiments/text_path_example.py",
        "experiments/conditions/text_path_example.json", "results/text_path_example.json")
    paths = ["experiments/text_path_figures.py", "experiments/text_path_example.py", "experiments/conditions",
             "experiments/spec", "src", "pyproject.toml", "uv.lock", "results/text_path_example.json"]
    return {"git_commit": git("rev-parse", "HEAD"),
            "git_dirty": bool(git("status", "--porcelain", "--", *paths))}


def main() -> None:
    c = conditions()
    rel = outputs(c)
    for p in rel:
        if (OUT_ROOT / p).exists() or (OUT_ROOT / p).is_symlink():
            raise SystemExit(f"{OUT_ROOT / p} exists; remove it to redraw")
    git = git_state()
    if git["git_dirty"]:
        raise SystemExit("the conditions, the scripts or the library differ from the last commit; commit first")
    res = load_source(c, SOURCE)
    code = check_code(res)
    figs = specs(c)
    check_windows(res, figs)
    images, check = redraw_tiles(res, c["figures_v2"]["grid_N"])
    (OUT_ROOT / "results").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=OUT_ROOT / "results") as tmp:
        drawn = []
        for s in figs:
            d = figure(res, images, s["variant"], s["texts"], s["window"], Path(tmp) / Path(s["file"]).name)
            drawn.append({"file": s["file"], **d})
        out = {"meta": {"conditions_sha256": run_.sha256(run_.COND), "script_sha256": run_.sha256(SCRIPT),
                        "run_script_sha256": code["script_sha256"], "library_sha256": code["library_sha256"],
                        "numpy": code["numpy"], "scipy": code["scipy"], "python": sys.version.split()[0], **git,
                        "source": str(SOURCE.relative_to(ROOT)), "source_sha256": source_sha256(c),
                        "finished": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")},
               "interpretation": INTERPRETATION, "check": check, "figures": drawn}
        Path(tmp, "out.json").write_text(json.dumps(out, indent=1) + "\n")
        for s, d in zip(figs, drawn):
            (OUT_ROOT / s["file"]).parent.mkdir(parents=True, exist_ok=True)
            os.replace(Path(tmp) / Path(s["file"]).name, OUT_ROOT / s["file"])
        os.replace(Path(tmp, "out.json"), OUT_ROOT / OUT_JSON_REL)
    print(f"written {OUT_ROOT / OUT_JSON_REL}")


if __name__ == "__main__":
    main()
