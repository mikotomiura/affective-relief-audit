"""Text example of Section 6: the paths of two texts through the lexicon, the rule and three exports.

Usage:  uv run python experiments/text_path_example.py              (compute, then write the results; refuses to
                                                                     overwrite)
        uv run python experiments/text_path_example.py --report     (rewrite the report from the stored results)
        uv run python experiments/text_path_example.py --smoke DIR  (a test text outside the conditions; tests the
                                                                     script only)
Conditions: experiments/conditions/text_path_example.json (fixed and committed before this script was run)
Specification: experiments/spec/generator-and-descriptors.md
Output: results/text_path_example.json, results/text_path_example.md, results/figs/fig5_text_path.pdf (main) and
        results/figs/figS_text_path_nofunction.pdf (supplement). The PDFs are not byte-reproducible (usetex font
        subsets); the plotted numbers are in the JSON.

Where the conditions leave a choice open, the choice is stated in INTERPRETATION below; it was fixed in this script
before the computation was run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np

from atact.field import procedural_field_separable
from atact.lexicon import Lexicon, load_lexicon, match_terms, split_sentences, tokenize
from atact.mapping import params
from atact.transform import t_gamma, t_gamma_eps

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve()
COND = ROOT / "experiments" / "conditions" / "text_path_example.json"
SPEC = ROOT / "experiments" / "spec" / "generator-and-descriptors.md"
LIBS = [ROOT / "src" / "atact" / n for n in ("field.py", "lexicon.py", "mapping.py", "transform.py")] + \
    [ROOT / "uv.lock"]
K2 = ROOT / "results" / "k2_gradient.json"
OUT_JSON = ROOT / "results" / "text_path_example.json"
OUT_MD = ROOT / "results" / "text_path_example.md"
FIGS = ROOT / "results" / "figs"
FIG_MAIN, FIG_SUPP = "fig5_text_path.pdf", "figS_text_path_nofunction.pdf"

OCTAVES = 4
TOL = 1e-12
VARIANTS = ("main", "function_words_removed")
EXPORTS = ("common", "minmax", "common_eps")
SMOKE_TEXTS = {"A": "The storm broke over the harbour. We waited.",
               "B": "A little light came back over the calm water. Nobody spoke, and nobody slept."}

INTERPRETATION = [
    "Sentences are split and tokenised by atact.lexicon. In the variant without function words a matched term is "
    "dropped when every token of it is in the stop-word list; V, A and Z are then recomputed from the remaining "
    "terms, and Z = 0 gives (0, 0) with the unmatched flag, as in the main variant.",
    "The gradient of S2.6 is numpy.gradient(X, 1/N), its magnitude hypot(d/dx, d/dy), maximised over all grid "
    "points, edges included. Physical slope = (height scale) |grad H| / L with height scale D / (2 s_max) for the "
    "common exports and D / (max H - min H) for min-max; angle = atan(slope) in degrees.",
    "P-T1 compares the exported min-max image z / D with (T - min T) / (max T - min T), T = T_gamma(F), written "
    "out separately, elementwise. "
    "P-T3 uses G = max |grad F| on the same grid and is checked only for gamma > 1 (sigma_eps is defined there). "
    "P-T4 is judged per text when at least two of its sentences are unmatched in the variant without function "
    "words: their (V, A) must be (0, 0), their parameters those of (0, 0), and their tiles equal on every grid and "
    "export; otherwise it is reported as not applicable. All texts share the seed and the grids.",
    "Before any tile is computed, the sentence counts and Z of every text and variant are compared with "
    "'expected_coverage' of the conditions; a difference stops the run. A prediction that fails does not stop the "
    "run; it is reported as it comes out. The real run refuses to start when the tracked inputs differ from the "
    "last commit.",
    "edge_argmax records whether the grid point of the largest slope lies in the first or last row or column; f is "
    "in general not an integer here, so the field jumps at the domain edge (S1.6), and the one-sided differences "
    "at the edge do not see the jump.",
    "In the figure, unmatched sentences (Z = 0) are ringed, and labels of coincident points are merged.",
    "Grey levels of the figure: z / D + 1/2 for the common exports (so that z = 0 is mid grey and |z| <= D/2 under "
    "ampsum and s <= s_max), z / D for min-max; both on [0, 1] with the grey colour map, no shading, origin lower.",
]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_conditions() -> dict:
    return json.loads(COND.read_text())


def stop_words() -> frozenset[str]:
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

    return frozenset(ENGLISH_STOP_WORDS)


def stop_words_sha256(words) -> str:
    return hashlib.sha256("\n".join(sorted(words)).encode()).hexdigest()


def git_state() -> dict:
    def run(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()

    paths = ["experiments/text_path_example.py", "experiments/conditions", "experiments/spec", "src",
             "pyproject.toml", "uv.lock"]
    return {"git_commit": run("rev-parse", "HEAD"), "git_dirty": bool(run("status", "--porcelain", "--", *paths))}


def identity(lex_path: Path) -> dict:
    import scipy
    import sklearn

    return {"conditions_sha256": sha256(COND), "spec_sha256": sha256(SPEC), "script_sha256": sha256(SCRIPT),
            "library_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in LIBS},
            "lexicon_sha256": sha256(lex_path), "k2_sha256": sha256(K2),
            "numpy": np.__version__, "scipy": scipy.__version__, "sklearn": sklearn.__version__,
            "python": sys.version.split()[0]}


def check_inputs(c: dict, lex_path: Path) -> float:
    """Check the lexicon, the stop-word list and the eps against the conditions; return eps."""
    if sha256(lex_path) != c["lexicon"]["file_sha256"]:
        raise SystemExit(f"{lex_path} does not match the SHA-256 of the conditions")
    v = c["variants"]["function_words_removed"]
    sw = stop_words()
    if stop_words_sha256(sw) not in v or f"{len(sw)} words" not in v:
        raise SystemExit("the stop-word list differs from the one fixed in the conditions")
    eps_cond = float(c["exports"]["common_eps"].split("eps = ")[1].split(",")[0])
    if sha256(K2) not in c["exports"]["common_eps"]:
        raise SystemExit("results/k2_gradient.json differs from the file named in the conditions")
    eps = json.loads(K2.read_text())["analysis"]["eps"]["main"]
    if eps != eps_cond:
        raise SystemExit(f"eps of k2_gradient.json ({eps!r}) differs from the conditions ({eps_cond!r})")
    return eps


def check_coverage(c: dict, out: dict) -> None:
    """The sentence counts and Z of the conditions (seen before the run); V and A are not printed."""
    exp = c["expected_coverage"]
    for name, t in out["texts"].items():
        for v in VARIANTS:
            got = [r["Z"] for r in t["variants"][v]]
            if got != exp[name][v]:
                raise SystemExit(f"coverage of text {name} ({v}) is Z = {got}, not {exp[name][v]} as in the conditions")


def lexicon_path(c: dict) -> Path:
    return ROOT / c["lexicon"]["file"].split(" ")[0]


# --- the path of the text ---------------------------------------------------------------------------------------------

def point(sentence: str, lex: Lexicon, drop: frozenset[str] | None) -> dict:
    terms = match_terms(tokenize(sentence), lex)
    if drop is not None:
        terms = [t for t in terms if not all(w in drop for w in t.split(" "))]
    z = len(terms)
    # the same arithmetic as atact.lexicon.sentence_point
    V = sum(lex.entries[t][0] for t in terms) / z if z else 0.0
    A = sum(lex.entries[t][1] for t in terms) / z if z else 0.0
    f, s, g = (float(x) for x in params(V, A))
    return {"text": sentence, "matched": terms, "Z": z, "unmatched": z == 0, "V": V, "A": A, "f": f,
            "f_frac": float(f - np.floor(f)), "s": s, "gamma": g}


def text_points(text: str, lex: Lexicon, drop: frozenset[str] | None) -> list[dict]:
    return [point(s, lex, drop) for s in split_sentences(text)]


# --- surfaces and exports ---------------------------------------------------------------------------------------------

def max_grad(X: np.ndarray) -> float:
    return max_grad_edge(X)[0]


def max_grad_edge(X: np.ndarray) -> tuple[float, bool]:
    n = X.shape[0]
    gy, gx = np.gradient(X, 1.0 / n)
    m = np.hypot(gx, gy)
    j, i = np.unravel_index(int(np.argmax(m)), m.shape)
    return float(m[j, i]), bool(i in (0, n - 1) or j in (0, n - 1))


def sigma_eps(g: float, eps: float) -> float:
    return eps ** (1.0 / g - 1.0) * (1.0 + eps**2) ** ((1.0 - 1.0 / g) / 2.0)


def minmax(X: np.ndarray) -> np.ndarray:
    return (X - X.min()) / (X.max() - X.min())


def tile(p: dict, n: int, seed: int, eps: float, d: dict) -> dict:
    """Heights in mm of the three exports and the readouts of one sentence on one grid."""
    D, L, s_max = d["D"], d["L"], d["s_max"]
    F = procedural_field_separable(p["f"], n, seed, octaves=OCTAVES, normalize="ampsum")
    T = t_gamma(F, p["gamma"])
    H, H_eps = p["s"] * T, p["s"] * t_gamma_eps(F, p["gamma"], eps)
    k = D / (2 * s_max)
    z = {"common": k * H, "minmax": D * minmax(H), "common_eps": k * H_eps}
    scale = {"common": k, "minmax": D / (H.max() - H.min()), "common_eps": k}
    src = {"common": H, "minmax": H, "common_eps": H_eps}
    G = max_grad(F)
    out = {"z": z, "G": G,
           "angle_deg": {e: float(np.degrees(np.arctan(scale[e] * max_grad(src[e]) / L))) for e in EXPORTS},
           "slope": {e: scale[e] * max_grad(src[e]) / L for e in EXPORTS},
           "edge_argmax": {e: max_grad_edge(src[e])[1] for e in EXPORTS},
           "span_mm": {e: float(z[e].max() - z[e].min()) for e in EXPORTS},
           "shape_change_mm": float(np.abs(z["common_eps"] - z["common"]).max()),
           # the exported min-max image against the min-max of T written out (s removed), not through minmax()
           "pt1_diff": float(np.abs(z["minmax"] / D - (T - T.min()) / (T.max() - T.min())).max()),
           "pt2_common_expected": float(k * p["s"] * (T.max() - T.min()))}
    if p["gamma"] > 1:
        se = sigma_eps(p["gamma"], eps)
        out["pt3_slope_bound"] = k * p["s"] * se * G / L
        out["pt3_shape_bound_mm"] = k * p["s"] * eps ** (1.0 / p["gamma"])
    return out


def run(c: dict, texts: dict[str, str], lex: Lexicon, eps: float, coverage: bool = True) -> tuple[dict, dict]:
    d = {"D": 1.2, "L": 50.0, "s_max": 0.30}
    if "L = 50 mm, D = 1.2 mm, s_max = 0.30" not in c["exports"]["dimensions"]:
        raise SystemExit("the dimensions of the conditions changed")
    seed, Ns = c["surface"]["seed"], c["surface"]["grids_N"]
    drops = {"main": None, "function_words_removed": stop_words()}
    out = {"dimensions": d, "eps": eps, "seed": seed, "grids_N": Ns, "texts": {}}
    images = {}
    for name, text in texts.items():
        out["texts"][name] = {"content": text, "variants": {}}
        for v in VARIANTS:
            rows = []
            for i, p in enumerate(text_points(text, lex, drops[v])):
                r = {**p, "grids": {}}
                for n in Ns:
                    t = tile(p, n, seed, eps, d)
                    if n == Ns[0]:
                        images[(name, v, i)] = t["z"]
                    if p["unmatched"]:
                        images[(name, v, i, n)] = t["z"]
                    r["grids"][str(n)] = {k_: v_ for k_, v_ in t.items() if k_ != "z"}
                rows.append(r)
            out["texts"][name]["variants"][v] = rows
    if coverage:
        check_coverage(c, out)
    out["predictions"] = predictions(out, images, d)
    out["comparison"] = comparison(out)
    return out, images


def all_rows(out: dict):
    for name, t in out["texts"].items():
        for v in VARIANTS:
            for i, r in enumerate(t["variants"][v]):
                yield name, v, i, r


def predictions(out: dict, images: dict, d: dict) -> dict:
    res = {}
    grids = [g for *_, r in all_rows(out) for g in r["grids"].values()]
    per = {f"{v} N={n}": max(r["grids"][str(n)]["pt1_diff"] for _, v_, _, r in all_rows(out) if v_ == v)
           for v in VARIANTS for n in out["grids_N"]}
    res["P-T1"] = {"max_diff": per, "holds": max(per.values()) <= TOL}
    span_mm = [abs(g["span_mm"]["minmax"] - d["D"]) for g in grids]
    span_c = [abs(g["span_mm"]["common"] - g["pt2_common_expected"]) for g in grids]
    res["P-T2"] = {"max_minmax_dev_mm": max(span_mm), "max_common_dev_mm": max(span_c),
                   "holds": max(span_mm) <= TOL and max(span_c) <= TOL}
    checked, ok = 0, True
    for *_, r in all_rows(out):
        if r["gamma"] > 1:
            for g in r["grids"].values():
                checked += 1
                ok &= g["slope"]["common_eps"] <= g["pt3_slope_bound"] * (1 + TOL)
                ok &= g["shape_change_mm"] <= g["pt3_shape_bound_mm"] * (1 + TOL)
    res["P-T3"] = {"cases_checked": checked, "holds": bool(ok) if checked else None}
    res["P-T4"] = {}
    for name, t in out["texts"].items():
        un = [i for i, r in enumerate(t["variants"]["function_words_removed"]) if r["unmatched"]]
        if len(un) < 2:
            res["P-T4"][name] = {"unmatched": un, "holds": None,
                                 "note": "not applicable: fewer than two unmatched sentences"}
            continue
        rows = t["variants"]["function_words_removed"]
        neutral = tuple(float(x) for x in params(0.0, 0.0))
        at_origin = all((rows[i]["V"], rows[i]["A"]) == (0.0, 0.0)
                        and (rows[i]["f"], rows[i]["s"], rows[i]["gamma"]) == neutral for i in un)
        diffs = [float(np.abs(images[(name, "function_words_removed", un[0], n)][e]
                              - images[(name, "function_words_removed", j, n)][e]).max())
                 for j in un[1:] for n in out["grids_N"] for e in EXPORTS]
        res["P-T4"][name] = {"unmatched": un, "at_origin_with_params_of_(0,0)": at_origin,
                             "max_diff_mm": max(diffs), "holds": at_origin and max(diffs) == 0.0}
    return res


def comparison(out: dict) -> dict:
    """Descriptive readouts across the texts (not predicted): Z, and the common-scale spans relative to the largest
    span over all tiles of the same variant."""
    n0 = str(out["grids_N"][0])
    res = {}
    for v in VARIANTS:
        spans = {name: [r["grids"][n0]["span_mm"]["common"] for r in t["variants"][v]]
                 for name, t in out["texts"].items()}
        top = max(x for xs in spans.values() for x in xs)
        res[v] = {name: {"Z": [r["Z"] for r in t["variants"][v]],
                         "common_span_ratio_to_largest": [x / top for x in spans[name]]}
                  for name, t in out["texts"].items()}
    return res


# --- figure -----------------------------------------------------------------------------------------------------------

PATH_STYLE = {"main": dict(marker="o", ls="-"), "function_words_removed": dict(marker="s", ls="--")}
TEXT_COLOUR = ("k", "#d95f02", "#1b9e77")


def figure(out: dict, images: dict, variant: str, path: Path) -> dict:
    import matplotlib

    matplotlib.use("pdf")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "text.usetex": True, "font.family": "serif", "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
        "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
        "lines.linewidth": 1.0, "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "pdf.fonttype": 42,
    })
    names = list(out["texts"])
    D = out["dimensions"]["D"]
    cols = []  # (text, sentence index) with a spacer between texts
    for j, name in enumerate(names):
        if j:
            cols.append(None)
        cols += [(name, i) for i in range(len(out["texts"][name]["variants"][variant]))]
    widths = [3.0, 0.3] + [0.25 if c is None else 1.0 for c in cols]
    fig = plt.figure(figsize=(6.3, 2.3))
    gs = fig.add_gridspec(3, len(widths), width_ratios=widths, wspace=0.08, hspace=0.08)
    ax = fig.add_subplot(gs[:, 0])
    ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], color="k", lw=0.6)
    for j, name in enumerate(names):
        rows = out["texts"][name]["variants"][variant]
        V, A = [r["V"] for r in rows], [r["A"] for r in rows]
        ax.plot(V, A, lw=0.7, ms=3, color=TEXT_COLOUR[j], label=f"text {name}", **PATH_STYLE[variant])
        un = [i for i, r in enumerate(rows) if r["unmatched"]]
        if un:
            ax.plot([V[i] for i in un], [A[i] for i in un], ls="none", marker="o", ms=7, mfc="none",
                    mec=TEXT_COLOUR[j], mew=0.7)
        groups: dict[tuple, list[int]] = {}
        for i, (x, y) in enumerate(zip(V, A)):
            groups.setdefault((x, y), []).append(i)
        for (x, y), idx in groups.items():
            lab = ",".join(f"{name}{i + 1}" for i in idx) + (" (no term)" if rows[idx[0]]["unmatched"] else "")
            ax.annotate(lab, (x, y), xytext=(3, 3 + 7 * j), textcoords="offset points", fontsize=7,
                        color=TEXT_COLOUR[j])
    ax.set(xlabel="$V$", ylabel="$A$", xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), aspect="equal",
           title=r"(a) path of the sentences")
    ax.legend(loc="lower left", frameon=False, handlelength=1.6)
    labels = {"common": "common", "minmax": "min--max", "common_eps": r"common, $T_{\gamma,\varepsilon}$"}
    plotted = []
    for k, e in enumerate(EXPORTS):
        for m, col in enumerate(cols):
            if col is None:
                continue
            name, i = col
            a = fig.add_subplot(gs[k, m + 2])
            z = images[(name, variant, i)][e]
            grey = z / D if e == "minmax" else z / D + 0.5
            a.imshow(grey, cmap="gray", vmin=0, vmax=1, interpolation="nearest", origin="lower")
            a.set_xticks([])
            a.set_yticks([])
            for sp in a.spines.values():
                sp.set_linewidth(0.3)
            if k == 0:
                a.set_title(f"{name}{i + 1}", pad=2)
            if m == 0:
                a.set_ylabel(labels[e], fontsize=6)
            plotted.append({"export": e, "text": name, "sentence": i + 1, "grey_min": float(grey.min()),
                            "grey_max": float(grey.max())})
    fig.text(0.70, 0.99, r"(b) one tile per sentence, $N = 128$", ha="center", va="bottom")
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, metadata={"CreationDate": None, "Creator": "experiments/text_path_example.py",
                                "Producer": None})
    plt.close(fig)
    return {"file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path), "grey": plotted}


# --- report -----------------------------------------------------------------------------------------------------------

def fmt(x, d=4) -> str:
    return f"{x:.{d}g}" if isinstance(x, float) else str(x)


def write_md(res: dict) -> str:
    a = res["analysis"]
    n0, n1 = (str(n) for n in a["grids_N"])
    L = ["# Text example of Section 6 (results as generated)", "",
         f"Conditions SHA-256 `{res['meta']['conditions_sha256']}`, script `{res['meta']['script_sha256']}`, "
         f"git `{res['meta']['git_commit']}` (dirty: {res['meta']['git_dirty']}). Seed {a['seed']}, "
         f"eps = {fmt(a['eps'])}, L = {a['dimensions']['L']:g} mm, D = {a['dimensions']['D']:g} mm, "
         f"s_max = {a['dimensions']['s_max']:g}.", ""]
    for name, t in a["texts"].items():
        L += [f"Text {name}: \"{t['content']}\"", ""]
    for v in VARIANTS:
        L += [f"## Variant: {v}", "",
              "| # | sentence | matched | Z | V | A | f | s | gamma | span common (mm) | span common eps (mm) | "
              f"angle common N={n0} / {n1} | angle min-max N={n0} / {n1} | angle common eps N={n0} / {n1} | "
              "shape change (mm) | span ratio |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for name, t in a["texts"].items():
            ratio = a["comparison"][v][name]["common_span_ratio_to_largest"]
            for i, r in enumerate(t["variants"][v]):
                g0, g1 = r["grids"][n0], r["grids"][n1]
                ang = " | ".join(f"{g0['angle_deg'][e]:.1f} / {g1['angle_deg'][e]:.1f}" for e in EXPORTS)
                L.append(f"| {name}{i + 1} | {r['text']} | {', '.join(r['matched']) or '(none)'} | {r['Z']} | "
                         f"{r['V']:.4f} | {r['A']:.4f} | {r['f']:.4f} | {r['s']:.4f} | {r['gamma']:.4f} | "
                         f"{g0['span_mm']['common']:.3f} | {g0['span_mm']['common_eps']:.3f} | {ang} | "
                         f"{g0['shape_change_mm']:.3f} | {ratio[i]:.3f} |")
        L.append("")
    L += ["Span ratio: common-scale span relative to the largest over all tiles of the variant.", "",
          "## Predictions (implementation controls)", ""]
    for k, p in a["predictions"].items():
        if k == "P-T4":
            for name, q in p.items():
                L.append(f"- P-T4 (text {name}): holds = {q['holds']}; "
                         + ", ".join(f"{x} = {fmt(y)}" for x, y in q.items() if x != "holds"))
        else:
            L.append(f"- {k}: holds = {p['holds']}; " + ", ".join(f"{x} = {fmt(y)}" for x, y in p.items()
                                                                      if x != "holds"))
    L += ["", "Figures: " + ", ".join(f["file"] for f in res["figures"].values()), ""]
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--smoke", type=Path)
    a = ap.parse_args()
    if a.report:
        res = json.loads(OUT_JSON.read_text())
        now = identity(lexicon_path(load_conditions()))
        for k in ("conditions_sha256", "spec_sha256", "script_sha256", "library_sha256", "lexicon_sha256",
                  "k2_sha256"):
            if res["meta"][k] != now[k]:
                raise SystemExit(f"{k} changed since the values were computed")
        OUT_MD.write_text(write_md(res))
        return
    c = load_conditions()
    lex_path = lexicon_path(c)
    eps = check_inputs(c, lex_path)
    if a.smoke:
        texts = SMOKE_TEXTS
        a.smoke.mkdir(parents=True, exist_ok=True)
        out_json, out_md = a.smoke / "text_path_example.json", a.smoke / "text_path_example.md"
        fig_dir = a.smoke
    else:
        texts = {name: x["content"] for name, x in c["texts"].items() if isinstance(x, dict)}
        out_json, out_md, fig_dir = OUT_JSON, OUT_MD, FIGS
        if out_json.exists():
            raise SystemExit(f"{out_json} exists; remove it to recompute")
        if git_state()["git_dirty"]:
            raise SystemExit("the conditions, the script or the library differ from the last commit; commit first")
    ident = identity(lex_path)
    meta = {**ident, **git_state(), "smoke": bool(a.smoke), "platform": f"{platform.system()} {platform.machine()}",
            "started": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    lex = load_lexicon(lex_path)
    analysis, images = run(c, texts, lex, eps, coverage=not a.smoke)
    figs = {"main": figure(analysis, images, "main", fig_dir / FIG_MAIN),
            "function_words_removed": figure(analysis, images, "function_words_removed", fig_dir / FIG_SUPP)}
    meta["finished"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if identity(lex_path) != ident:
        raise SystemExit("an input file changed during the run")
    res = {"meta": meta, "interpretation": INTERPRETATION, "analysis": analysis, "figures": figs}
    out_json.write_text(json.dumps(res, indent=1) + "\n")
    out_md.write_text(write_md(res))
    print(f"written {out_json}")


if __name__ == "__main__":
    main()
