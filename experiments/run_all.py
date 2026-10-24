"""Recompute the numbers for Propositions 3, 5, 6 and 7 and write JSON, tables and figures to results/.

Usage: uv run python experiments/run_all.py
Values come from the reconstructed generator, not from the original code (ESM_1.zip).
"""

from __future__ import annotations

import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sklearn

from atact.classify import DatasetConfig, evaluate, make_dataset
from atact.descriptors import centroid, max_gradient, rq
from atact.field import RenderConfig, height, procedural_field
from atact.mapping import params
from atact.transform import sigma2_single_sine, t_gamma

OUT = Path(__file__).resolve().parents[1] / "results"
FIG = OUT / "figs"


def p3_roughness():
    rows = []
    for g in (0.9, 1.0, 1.75, 2.6):
        rows.append({"gamma": g, "sigma2_closed": float(sigma2_single_sine(g))})
    corners = {}
    for name, va in {"pos_calm(+1,-1)": (1, -1), "neg_excited(-1,+1)": (-1, 1)}.items():
        H = height(*va)
        f, s, g = params(*va)
        corners[name] = {"f": float(f), "s": float(s), "gamma": float(g), "Rq": rq(H), "C": centroid(H)}
    return {"single_sine": rows, "corners_N128_seed42": corners}


def p5_centroid_vs_resolution():
    out = {}
    for N in (128, 256, 512, 1024):
        cfg = RenderConfig(n=N)
        c3 = centroid(t_gamma(procedural_field(3.0, cfg), 0.9))
        c7 = centroid(t_gamma(procedural_field(7.0, cfg), 2.6))
        out[N] = {"C_pos_calm": c3, "C_neg_excited": c7, "ratio": c7 / c3, "f_ratio": 7 / 3}
    return out


def p6_gradient_vs_resolution():
    out = {}
    for g in (0.9, 1.75, 2.6):
        vals = [max_gradient(t_gamma(procedural_field(5.0, RenderConfig(n=n)), g)) for n in (128, 512, 2048)]
        out[g] = {"N128": vals[0], "N512": vals[1], "N2048": vals[2], "growth": vals[2] / vals[0],
                  "theory_16^(1-1/g)": 16 ** max(0.0, 1 - 1 / g)}
    return out


def p7_classification():
    rows = []
    for warp in (0.0, 0.25):
        for w in (0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0):
            cfg = DatasetConfig(jitter=w, render=RenderConfig(warp=warp))
            X, y, _ = make_dataset(cfg)
            r = evaluate(X, y)
            rows.append({"warp": warp, "jitter": w, **{k: r[k] for k in r}})
    return rows


def fig_corners():
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.6))
    for ax, (va, warp) in zip(axes, [((1, -1), 0.0), ((-1, 1), 0.0), ((1, -1), 0.25), ((-1, 1), 0.25)]):
        H = height(*va, RenderConfig(warp=warp))
        ax.imshow(H, cmap="gray")
        ax.set_title(f"(V,A)={va} warp={warp}\nRq={rq(H):.3f} C={centroid(H):.1f}", fontsize=8)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(FIG / "corners.png", dpi=120)
    plt.close(fig)


def fig_classification(rows):
    fig, ax = plt.subplots(figsize=(5, 3.2))
    for warp, ls in ((0.0, "-"), (0.25, "--")):
        sub = [r for r in rows if r["warp"] == warp]
        w = [r["jitter"] for r in sub]
        for key, c in (("rq", "C0"), ("centroid", "C1"), ("both", "C2")):
            ax.plot(w, [r[key][0] for r in sub], ls, color=c, label=f"{key} warp={warp}")
    ax.axhline(0.921, color="k", lw=0.8, ls=":")
    ax.axhline(0.742, color="C1", lw=0.8, ls=":")
    ax.set_xlabel("jitter w (uniform, per coordinate)")
    ax.set_ylabel("5-fold x 20 accuracy")
    ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(FIG / "classification_vs_jitter.png", dpi=120)
    plt.close(fig)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    env = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
           "sklearn": sklearn.__version__, "matplotlib": matplotlib.__version__}
    res = {"env": env, "p3": p3_roughness(), "p5": p5_centroid_vs_resolution(),
           "p6": p6_gradient_vs_resolution()}
    rows = p7_classification()
    res["p7"] = rows
    (OUT / "results.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str))
    fig_corners()
    fig_classification(rows)
    lines = ["| warp | jitter | Rq だけ | 重心だけ | 両方 | 並べ替え | 75/25 |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        f = lambda m: f"{100*m[0]:.1f} ± {100*m[1]:.1f}"
        lines.append(f"| {r['warp']} | {r['jitter']} | {f(r['rq'])} | {f(r['centroid'])} | {f(r['both'])} | "
                     f"{f(r['permuted'])} | {100*r['holdout']:.1f} |")
    (OUT / "p7_table.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: res[k] for k in ("env", "p3", "p5", "p6")}, indent=1, default=str))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
