"""Figures 1-4 of the main text, as vector PDF for the LaTeX draft.

Usage:  uv run python experiments/figures_main.py [--fig 1 2 3 4]
Output: results/figs/fig1_parameter_image.pdf, fig2_heights.pdf, fig3_transform_gradient.pdf,
        fig4_centroid_growth.pdf, and results/figs/figures_main.json (sources, their SHA-256 and the plotted numbers
        that are not in the sources).

The PDFs are not byte-reproducible: the usetex backend gives the embedded font subsets random name prefixes. The
plotted numbers are written to figures_main.json and are reproducible; compare those, not the PDF hashes.

Sources:
  Fig. 1: the rule (atact.mapping); no computation beyond the affine map.
  Fig. 2: the surfaces of 'figure2' in experiments/conditions/k2_gradient_and_figures.json (generated here).
  Fig. 3: (a) T_gamma and T_{gamma,eps} with the eps of results/k2_gradient.json; (b) the seed means of that file.
  Fig. 4: the seed means of results/k4_centroid_2d.json (commit cb369b4) and, for N 8192 and 16384 of the sum field,
          results/k4_supplement.json (commit cadd349; exploratory, marked in the figure).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402

from atact.field import procedural_field_separable  # noqa: E402
from atact.mapping import params  # noqa: E402
from atact.transform import t_gamma, t_gamma_eps  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "results" / "figs"
COND = ROOT / "experiments" / "conditions" / "k2_gradient_and_figures.json"
K2 = ROOT / "results" / "k2_gradient.json"
K4 = ROOT / "results" / "k4_centroid_2d.json"
K4_SHA256 = "257173c1b375595146a4f23a746fb8e2d8537a6df6426eeb1c82b40d37f6872a"  # commit cb369b4
K4S = ROOT / "results" / "k4_supplement.json"
K4S_SHA256 = "a515d550e8f47974b3d6f27454e9754bfb150cc490a97ce62060b535775044a0"  # commit cadd349

FULL, HALF = 6.3, 3.1  # inches
GRID5 = [-1.0, -0.5, 0.0, 0.5, 1.0]
GAMMA_COLOURS = {0.9: "#1b9e77", 1.0: "#7570b3", 1.25: "#666666", 1.75: "#d95f02", 2.6: "#e7298a"}

plt.rcParams.update({
    "text.usetex": True, "font.family": "serif", "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
    "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
    "lines.linewidth": 1.0, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    "savefig.dpi": 600,  # images (height maps) at 600 dpi in the PDF, not resampled to 100 dpi
    "pdf.fonttype": 42,
})
META = {"CreationDate": None, "Creator": "experiments/figures_main.py", "Producer": None}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(fig, name: str) -> Path:
    FIGS.mkdir(parents=True, exist_ok=True)
    p = FIGS / name
    fig.savefig(p, metadata=META)
    plt.close(fig)
    return p


# --- Fig. 1 -----------------------------------------------------------------------------------------------------------

def fig1() -> dict:
    V, A = np.meshgrid(GRID5, GRID5)
    f, s, g = params(V, A)
    fig = plt.figure(figsize=(FULL, 2.1))
    ax1 = fig.add_subplot(1, 3, 1)
    sc = ax1.scatter(V, A, c=V, cmap="viridis", s=14, vmin=-1, vmax=1, zorder=3)
    ax1.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], color="k", lw=0.6)
    ax1.set(xlabel="$V$", ylabel="$A$", xlim=(-1.25, 1.25), ylim=(-1.25, 1.25), aspect="equal",
            title=r"(a) input square $Q$")
    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    cv = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])
    cf, cs, cg = params(cv[:, 0], cv[:, 1])
    ax2.plot(cf, cs, cg, color="k", lw=0.6)
    ax2.scatter(f, s, g, c=V, cmap="viridis", s=8, vmin=-1, vmax=1, depthshade=False)
    ax2.set_xlabel("$f$", labelpad=-6)
    ax2.set_ylabel("$s$", labelpad=-6)
    ax2.set_zlabel(r"$\gamma$", labelpad=-7)
    ax2.tick_params(pad=-3)
    ax2.set_title(r"(b) image $\Phi(Q)$ in $(f,s,\gamma)$", pad=0)
    ax2.view_init(elev=22, azim=-58)
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.plot(cf, cg, color="k", lw=0.6)
    ax3.scatter(f, g, c=V, cmap="viridis", s=14, vmin=-1, vmax=1, zorder=3)
    ax3.set(xlabel="$f$", ylabel=r"$\gamma$", title=r"(c) what min--max keeps: $(f,\gamma)$")
    fig.subplots_adjust(wspace=0.45, right=0.9)
    cax = fig.add_axes([0.925, 0.2, 0.012, 0.6])
    cb = fig.colorbar(sc, cax=cax)
    cb.set_label("$V$")
    p = save(fig, "fig1_parameter_image.pdf")
    return {"file": str(p.relative_to(ROOT)), "corners_fsg": np.column_stack([cf, cs, cg])[:4].tolist()}


# --- Fig. 2 -----------------------------------------------------------------------------------------------------------

def fig2() -> dict:
    c = json.loads(COND.read_text())
    s_max = c["eps_example"]["s_max"]
    seed, n = 42, 128
    panels = []
    fig, axes = plt.subplots(5, 11, figsize=(FULL, 3.1), gridspec_kw={"width_ratios": [1] * 5 + [0.25] + [1] * 5})
    for ax in axes[:, 5]:
        ax.axis("off")
    for i, A in enumerate(GRID5[::-1]):          # rows: A from 1 (top) to -1
        for j, V in enumerate(GRID5):            # columns: V from -1 to 1
            f, s, g = (float(x) for x in params(V, A))
            H = s * t_gamma(procedural_field_separable(f, n, seed), g)
            common = (H + s_max) / (2 * s_max)
            mm = (H - H.min()) / (H.max() - H.min())
            for k, img in ((0, common), (6, mm)):
                ax = axes[i, j + k]
                ax.imshow(img, cmap="gray", vmin=0, vmax=1, interpolation="nearest", origin="lower")
                ax.set_xticks([])
                ax.set_yticks([])
                for sp in ax.spines.values():
                    sp.set_linewidth(0.3)
            panels.append({"V": V, "A": A, "f": f, "s": s, "gamma": g, "common_range": [float(common.min()),
                           float(common.max())]})
    for j, V in enumerate(GRID5):
        for k in (0, 6):
            axes[-1, j + k].set_xlabel(f"${V:g}$", labelpad=2)
    for i, A in enumerate(GRID5[::-1]):
        axes[i, 0].set_ylabel(f"${A:g}$", rotation=0, labelpad=4, ha="right", va="center")
    fig.text(0.29, 0.005, "$V$", ha="center")
    fig.text(0.72, 0.005, "$V$", ha="center")
    fig.text(0.0, 0.5, "$A$", va="center")
    fig.text(0.29, 0.99, r"(a) common scale, grey $=(H+s_{\max})/(2s_{\max})$", ha="center", va="top")
    fig.text(0.72, 0.99, r"(b) min--max export of each panel", ha="center", va="top")
    fig.subplots_adjust(wspace=0.06, hspace=0.06, top=0.93, bottom=0.07, left=0.06, right=0.99)
    p = save(fig, "fig2_heights.pdf")
    return {"file": str(p.relative_to(ROOT)), "seed": seed, "N": n, "panels": panels}


# --- Fig. 3 -----------------------------------------------------------------------------------------------------------

def fig3() -> dict:
    res = json.loads(K2.read_text())
    if res["meta"].get("smoke"):
        raise SystemExit("results/k2_gradient.json is a smoke run")
    eps = res["analysis"]["eps"]["main"]
    Ns = res["grids_N"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL, 2.3))
    u = np.linspace(-1, 1, 2001)
    for g in (0.9, 1.75, 2.6):
        col = GAMMA_COLOURS[g]
        a.plot(u, t_gamma(u, g), color=col, label=rf"$\gamma={g:g}$")
        if g > 1:
            a.plot(u, t_gamma_eps(u, g, eps), color=col, ls="--")
    a.plot([], [], color="k", ls="--", label=rf"$T_{{\gamma,\varepsilon}}$, $\varepsilon={eps:.3f}$")
    a.set(xlabel="$u$", ylabel="$T(u)$", xlim=(-1, 1), ylim=(-1.05, 1.05), title=r"(a) $T_\gamma$ and $T_{\gamma,\varepsilon}$")
    a.legend(frameon=False, loc="upper left")
    pts = {p["name"]: p for p in json.loads(COND.read_text())["points"]}
    out = {"eps": eps, "series": {}}
    for name in ("low", "mid", "high"):
        P = res["analysis"]["points"][name]
        g = pts[name]["gamma"]
        col = GAMMA_COLOURS[g]
        b.loglog(Ns, P["M"]["seed_mean_by_N"], color=col, marker="o", ms=2.5, label=rf"$\gamma={g:g}$, $f={pts[name]['f']:g}$")
        out["series"][name] = {"M": P["M"]["seed_mean_by_N"]}
        if g > 1:
            b.loglog(Ns, P["eps"]["main"]["Meps"]["seed_mean_by_N"], color=col, ls="--", marker="o", ms=2.5, mfc="white")
            out["series"][name]["Meps"] = P["eps"]["main"]["Meps"]["seed_mean_by_N"]
            m0 = P["M"]["seed_mean_by_N"][0]
            b.loglog(Ns, [0.6 * m0 * (n / Ns[0]) ** (1 - 1 / g) for n in Ns], color=col, lw=0.6, ls=":")
    b.plot([], [], color="k", ls="--", mfc="white", marker="o", ms=2.5, label=r"$T_{\gamma,\varepsilon}$")
    b.plot([], [], color="k", ls=":", lw=0.5, label=r"slope $1-1/\gamma$ (offset)")
    b.set(xlabel="$N$", ylabel=r"$\max|\nabla H|$ (seed mean)", title="(b) maximum gradient against $N$")
    b.set_xticks([128, 512, 2048], ["128", "512", "2048"])
    b.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    b.legend(frameon=False, loc="upper left", fontsize=6)
    fig.subplots_adjust(wspace=0.3)
    p = save(fig, "fig3_transform_gradient.pdf")
    return {"file": str(p.relative_to(ROOT)), **out}


# --- Fig. 4 -----------------------------------------------------------------------------------------------------------

def fig4() -> dict:
    if sha256(K4) != K4_SHA256 or sha256(K4S) != K4S_SHA256:
        raise SystemExit("K4 results do not have the recorded SHA-256")
    cells = json.loads(K4.read_text())["summary"]["cells"]
    look = {(c["field"], c["f"], c["gamma"]): c for c in cells
            if c["processing"] == "raw" and c["descriptor"] == "centroid_amp" and c["sampling"] == "direct"}
    sup = {}
    for r in json.loads(K4S.read_text())["rows"]:
        sup.setdefault((r["f"], r["gamma"], r["N"]), []).append(r["centroid_amp"])
    gammas = (0.9, 1.0, 1.75, 2.6)
    titles = {"oned": "(a) one-dimensional sine", "product1": "(b) single-octave product", "sum": "(c) four-octave sum"}
    fig, axes = plt.subplots(1, 3, figsize=(FULL, 2.3), sharey=True)
    out = {}
    for ax, field in zip(axes, ("oned", "product1", "sum")):
        for g in gammas:
            col = GAMMA_COLOURS[g]
            for f, ls in ((5, "-"), (5.5, "--")):
                c = look[(field, f, g)]
                ax.loglog(c["N"], c["mean_by_N"], color=col, ls=ls, marker="o", ms=2, mfc="white" if f == 5.5 else col)
                out[f"{field}|f={f}|gamma={g}"] = c["mean_by_N"]
            if field == "sum" and g != 1.0:
                Nx = [4096, 8192, 16384]
                ys = [look[(field, 5, g)]["mean_by_N"][-1]] + [float(np.mean(sup[(5, g, n)])) for n in Nx[1:]]
                if any(len(sup[(5, g, n)]) != 20 for n in Nx[1:]):
                    raise SystemExit("supplement does not have 20 seeds")
                ax.loglog(Nx, ys, color=col, ls=":", marker="s", ms=2, mfc="white")
                out[f"sum|f=5|gamma={g}|supplement"] = dict(zip(map(str, Nx[1:]), ys[1:]))
        ax.set(xlabel="$N$", title=titles[field])
        ticks = [128, 512, 2048] + ([8192] if field == "sum" else [])
        ax.set_xticks(ticks, [str(t) for t in ticks])
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axes[0].set_ylabel("amplitude-weighted centroid $C$ (cycles per domain)")
    for g in gammas:
        axes[0].plot([], [], color=GAMMA_COLOURS[g], label=rf"$\gamma={g:g}$")
    axes[0].plot([], [], color="k", ls="-", label="$f=5$")
    axes[0].plot([], [], color="k", ls="--", label="$f=5.5$")
    axes[2].plot([], [], color="k", ls=":", marker="s", ms=2, mfc="white", label="$N>4096$, exploratory")
    axes[0].legend(frameon=False, loc="upper left", fontsize=6)
    axes[2].legend(frameon=False, loc="upper left", fontsize=6)
    fig.subplots_adjust(wspace=0.08)
    p = save(fig, "fig4_centroid_growth.pdf")
    return {"file": str(p.relative_to(ROOT)), "series": out}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fig", type=int, nargs="*", default=[1, 2, 3, 4])
    a = ap.parse_args()
    man_p = FIGS / "figures_main.json"
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    srcs = {1: [], 2: [COND], 3: [COND, K2], 4: [K4, K4S]}
    for k in a.fig:
        info = {1: fig1, 2: fig2, 3: fig3, 4: fig4}[k]()
        info["sources"] = {str(p.relative_to(ROOT)): sha256(p) for p in srcs[k]}
        info["script_sha256"] = sha256(Path(__file__))
        info["pdf_sha256"] = sha256(ROOT / info["file"])
        man[f"fig{k}"] = info
        print(f"fig{k}: {info['file']}")
    man_p.write_text(json.dumps(man, indent=1) + "\n")


if __name__ == "__main__":
    main()
