"""Checks of experiments/text_path_figures.py on artificial stored results (the real results are not recomputed)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import text_path_example as run_  # noqa: E402
import text_path_figures as f  # noqa: E402

from atact.mapping import params

N = 32
D = {"D": 1.2, "L": 50.0, "s_max": 0.30}
real_redraw = f.redraw_tiles


@pytest.fixture(autouse=True)
def outputs_in_tmp(tmp_path, monkeypatch):
    """Every output of main() goes to a temporary directory, whatever the guards do."""
    monkeypatch.setattr(f, "OUT_ROOT", tmp_path / "out")


def row(V, A, n=N, seed=42, eps=0.35, unmatched=None):
    fp, s, g = (float(x) for x in params(V, A))
    un = (V, A) == (0, 0) if unmatched is None else unmatched
    p = {"text": "x", "matched": [] if un else ["w"], "Z": 0 if un else 1, "unmatched": un, "V": V, "A": A,
         "f": fp, "s": s, "gamma": g}
    t = run_.tile(p, n, seed, eps, D)
    return {**p, "grids": {str(n): {k: v for k, v in t.items() if k != "z"}}}


def make(pts: dict, variants=run_.VARIANTS) -> dict:
    texts = {name: {"content": name, "variants": {v: [row(V, A) for V, A in xs] for v in variants}}
             for name, xs in pts.items()}
    return {"analysis": {"grids_N": [N, 64], "seed": 42, "eps": 0.35, "dimensions": D, "texts": texts}}


@pytest.fixture
def stored():
    return make({"A": [(0.05, -0.16), (0.0, 0.0), (0.0, 0.0)], "B": [(0.03, -0.08), (-0.14, -0.13), (-0.01, -0.27)]})


def test_redrawn_tiles_match_the_stored_values(stored):
    images, check = f.redraw_tiles(stored, N)
    assert check == {"N": N, "max_abs_dev": 0.0}
    assert images[("B", "main", 2)]["common"].shape == (N, N)


def test_grid_must_be_the_first_of_the_results(stored):
    with pytest.raises(SystemExit, match="first grid"):
        f.redraw_tiles(stored, 64)


@pytest.mark.parametrize("key", ["f", "s", "gamma"])
def test_a_changed_parameter_stops_the_script(stored, key):
    stored["analysis"]["texts"]["B"]["variants"]["main"][1][key] *= 1 + 1e-6
    with pytest.raises(SystemExit, match="differs from the stored value"):
        f.redraw_tiles(stored, N)


@pytest.mark.parametrize("path", [("G",), ("shape_change_mm",), ("pt1_diff",), ("slope", "common"),
                                  ("pt3_slope_bound",)])
def test_every_stored_readout_is_compared(stored, path):
    g = stored["analysis"]["texts"]["A"]["variants"]["function_words_removed"][0]["grids"][str(N)]
    for k in path[:-1]:
        g = g[k]
    g[path[-1]] += 1e-9
    with pytest.raises(SystemExit, match="differs from the stored value"):
        f.redraw_tiles(stored, N)


def test_a_flipped_edge_flag_or_a_missing_readout_stops_the_script(stored):
    g = stored["analysis"]["texts"]["A"]["variants"]["main"][0]["grids"][str(N)]
    g["edge_argmax"]["minmax"] = not g["edge_argmax"]["minmax"]
    with pytest.raises(SystemExit, match="differs from the stored value"):
        f.redraw_tiles(stored, N)
    g["edge_argmax"]["minmax"] = not g["edge_argmax"]["minmax"]
    del g["G"]
    with pytest.raises(SystemExit, match="keys"):
        f.redraw_tiles(stored, N)


def test_a_changed_seed_or_eps_stops_the_script(stored):
    s2 = json.loads(json.dumps(stored))
    s2["analysis"]["seed"] = 43
    with pytest.raises(SystemExit):
        f.redraw_tiles(s2, N)
    stored["analysis"]["eps"] = 0.36
    with pytest.raises(SystemExit):  # only the common_eps export changes
        f.redraw_tiles(stored, N)


def test_readouts_do_not_fix_the_orientation(stored, monkeypatch):
    """A transposed field passes the readout check (as the conditions state); only check_code guards against it."""
    real = run_.procedural_field_separable
    monkeypatch.setattr(run_, "procedural_field_separable", lambda *a, **k: real(*a, **k).T)
    images, _ = f.redraw_tiles(stored, N)
    monkeypatch.setattr(run_, "procedural_field_separable", real)
    ref, _ = f.redraw_tiles(stored, N)
    assert not np.array_equal(images[("B", "main", 0)]["common"], ref[("B", "main", 0)]["common"])


def test_code_must_be_the_one_of_the_stored_results():
    import scipy

    meta = {"script_sha256": run_.sha256(run_.SCRIPT),
            "library_sha256": {str(p.relative_to(run_.ROOT)): run_.sha256(p) for p in run_.LIBS},
            "numpy": np.__version__, "scipy": scipy.__version__}
    assert f.check_code({"meta": meta})["numpy"] == np.__version__
    for k, bad in (("script_sha256", "0" * 64), ("numpy", "0.0"), ("scipy", "0.0")):
        with pytest.raises(SystemExit, match=k):
            f.check_code({"meta": {**meta, k: bad}})
    lib = dict(meta["library_sha256"])
    lib[next(iter(lib))] = "0" * 64
    with pytest.raises(SystemExit, match="library_sha256"):
        f.check_code({"meta": {**meta, "library_sha256": lib}})


def test_source_is_checked_against_the_conditions(tmp_path):
    c = f.conditions()
    p = tmp_path / "r.json"
    p.write_text("{}")
    with pytest.raises(SystemExit, match="differs from the results named"):
        f.load_source(c, p)
    assert len(f.source_sha256(c)) == 64
    if f.SOURCE.exists():
        assert run_.sha256(f.SOURCE) == f.source_sha256(c)


def test_conditions_without_figures_v2_are_refused(monkeypatch):
    c = f.conditions()
    monkeypatch.setattr(run_, "load_conditions", lambda: {**c, "version": 1})
    with pytest.raises(SystemExit, match="figures_v2"):
        f.conditions()


def test_specs_and_outputs_of_the_conditions():
    c = f.conditions()
    s = f.specs(c)
    assert [x["texts"] for x in s] == [["B"], ["A", "B"], ["A", "B"]]
    assert [x["variant"] for x in s] == ["main", "main", "function_words_removed"]
    assert [x["window"] for x in s] == [0.3, 0.3, 0.6]
    assert c["figures_v2"]["grid_N"] == 128
    out = f.outputs(c)
    assert len(out) == 4 and out[-1] == f.OUT_JSON_REL
    assert not any(x.endswith(("fig5_text_path.pdf", "figS_text_path_nofunction.pdf")) for x in out)


def test_coincident_points_share_a_label_and_a_mix_stops(stored):
    rows = stored["analysis"]["texts"]["A"]["variants"]["main"]
    assert [lab for _, lab in f.label_groups(rows, "A")] == ["A1", "A2,A3 (no term)"]
    rows[2] = {**rows[2], "unmatched": False}
    with pytest.raises(SystemExit, match="coincide"):
        f.label_groups(rows, "A")
    rows[1] = {**rows[1], "unmatched": False}
    assert [lab for _, lab in f.label_groups(rows, "A")] == ["A1", "A2,A3"]


def test_directions_start_away_from_the_centre():
    d = f.directions(1.0, 0.0, np.array([0.0, 0.0]))
    assert d[0] == pytest.approx((1.0, 0.0)) and len(set(d)) == 8
    assert f.directions(0.0, 0.0, np.array([0.0, 0.0]))[0] == pytest.approx((0.0, 1.0), abs=1e-12)


def overlap(a, b) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def test_figure_labels_are_checked_on_the_final_layout(stored, tmp_path):
    images, _ = f.redraw_tiles(stored, N)
    r = f.figure(stored, images, "main", ["A", "B"], 0.3, tmp_path / "x.pdf")
    assert (tmp_path / "x.pdf").stat().st_size > 0
    assert all(0.0 <= g["grey_min"] and g["grey_max"] <= 1.0 for g in r["grey"])
    assert len(r["grey"]) == 3 * 6
    assert clear_of_everything(r)


def test_labels_of_nearby_points_do_not_overlap(tmp_path):
    res = make({"A": [(0.10, -0.10), (0.20, 0.05)], "B": [(0.105, -0.10), (0.11, -0.095)]}, ["main"])
    images = {(name, "main", i): run_.tile(r, N, 42, 0.35, D)["z"]
              for name, t in res["analysis"]["texts"].items() for i, r in enumerate(t["variants"]["main"])}
    r = f.figure(res, images, "main", ["A", "B"], 0.3, tmp_path / "x.pdf")
    boxes = [x["box_px"] for x in r["labels"]]
    assert len(boxes) == 4 and not any(overlap(a, b) for i, a in enumerate(boxes) for b in boxes[i + 1:])


def clear_of_everything(r: dict) -> bool:
    boxes, h = [x["box_px"] for x in r["labels"]], r["point_free_px"]
    p = r["panel_px"]
    inside = all(p[0] <= b[0] and b[2] <= p[2] and p[1] <= b[1] and b[3] <= p[3] for b in boxes)
    no_labels = not any(overlap(a, b) for i, a in enumerate(boxes) for b in boxes[i + 1:])
    no_obstacles = not any(overlap(b, o) for b in boxes for o in r["obstacles_px"])
    no_points = not any(overlap(b, [x - h, y - h, x + h, y + h]) for b in boxes for x, y in r["points_px"])
    return inside and no_labels and no_obstacles and no_points


def figure_of(pts: dict, tmp_path: Path) -> dict:
    res = make(pts, ["main"])
    images = {(name, "main", i): run_.tile(r, N, 42, 0.35, D)["z"]
              for name, t in res["analysis"]["texts"].items() for i, r in enumerate(t["variants"]["main"])}
    return f.figure(res, images, "main", list(pts), 0.3, tmp_path / "x.pdf")


def test_labels_avoid_the_legend_and_the_inset(tmp_path):
    # points under the legend (upper left) and under the inset (upper right)
    r = figure_of({"A": [(-0.2, 0.17), (0.17, 0.12), (0.0, -0.1)]}, tmp_path)
    assert len(r["obstacles_px"]) == 2 and clear_of_everything(r)


def test_labels_avoid_the_points_and_the_centre(tmp_path):
    r = figure_of({"B": [(0.03, 0.0), (-0.03, 0.0), (0.0, 0.03), (0.0, -0.03)]}, tmp_path)
    assert len(r["points_px"]) == 5 and clear_of_everything(r)  # four points and the centre


def test_no_place_for_a_label_stops(tmp_path, monkeypatch):
    monkeypatch.setattr(f, "POINT_FREE_PT", 500.0)  # every direction collides with a point
    with pytest.raises(SystemExit, match="no place"):
        figure_of({"B": [(0.1, 0.1)]}, tmp_path)


def test_points_outside_a_window_stop_before_any_drawing(stored):
    figs = [{"variant": "main", "texts": ["B"], "window": 0.3},
            {"variant": "main", "texts": ["A", "B"], "window": 0.2}]
    with pytest.raises(SystemExit, match="outside the window"):
        f.check_windows(stored, figs)


def test_git_failure_stops_the_script(monkeypatch):
    real = subprocess.run

    def fail(args, **k):  # a git that fails with empty output; only check=True turns this into an error
        return real(["false"], **k)

    monkeypatch.setattr(f.subprocess, "run", fail)
    with pytest.raises(SystemExit, match="failed"):
        f.git_state()


def no_draw(*a, **k):  # if a guard is broken, stop here instead of reading the results and drawing
    raise AssertionError("the drawing started")


def test_real_run_refuses_dirty_inputs(monkeypatch):
    for name in ("load_source", "redraw_tiles", "figure"):
        monkeypatch.setattr(f, name, no_draw)
    monkeypatch.setattr(f, "git_state", lambda: {"git_commit": "x", "git_dirty": True})
    with pytest.raises(SystemExit, match="commit first"):
        f.main()
    assert not f.OUT_ROOT.exists()


@pytest.mark.parametrize("which", [0, -1])
def test_real_run_refuses_any_existing_output(monkeypatch, which):
    rel = f.outputs(f.conditions())[which]  # a figure alone, or the JSON alone
    p = f.OUT_ROOT / rel
    p.parent.mkdir(parents=True)
    p.write_text("x")
    monkeypatch.setattr(f, "git_state", no_draw)
    monkeypatch.setattr(f, "load_source", no_draw)
    with pytest.raises(SystemExit, match="exists"):
        f.main()


def test_main_writes_all_outputs_only_after_every_figure(stored, monkeypatch):
    monkeypatch.setattr(f, "git_state", lambda: {"git_commit": "x", "git_dirty": False})
    monkeypatch.setattr(f, "load_source", lambda c, p: {**stored, "meta": {}})
    monkeypatch.setattr(f, "check_code", lambda res: {"script_sha256": "s", "library_sha256": {}, "numpy": "n",
                                                      "scipy": "s"})
    monkeypatch.setattr(f, "redraw_tiles", lambda res, n: real_redraw(res, N))
    calls = {"n": 0}
    real_figure = f.figure

    def second_fails(*a, **k):
        calls["n"] += 1
        if calls["n"] == 2:
            raise SystemExit("no place for the label")
        return real_figure(*a, **k)

    monkeypatch.setattr(f, "figure", second_fails)
    with pytest.raises(SystemExit):
        f.main()
    written = [p for p in f.OUT_ROOT.rglob("*") if p.is_file()]
    assert written == []  # the first figure was drawn, but nothing reached the outputs
    monkeypatch.setattr(f, "figure", real_figure)
    f.main()
    for rel in f.outputs(f.conditions()):
        assert (f.OUT_ROOT / rel).stat().st_size > 0

