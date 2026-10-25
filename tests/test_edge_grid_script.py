"""Checks of the surfaces and of one job of experiments/edge_grid_paired.py (conditions version 2)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location(
    "edge_grid_paired", Path(__file__).resolve().parents[1] / "experiments" / "edge_grid_paired.py")
eg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eg)


def test_surfaces_match_conditions_version_2():
    ss = eg.surfaces()
    names = [s["name"] for s in ss]
    assert len(names) == len(set(names)) == 25 + 5 + 2 + 2
    rule = [s for s in ss if s["kind"] == "rule"]
    # f = 5 + 2A: every rule point has integer f (the error corrected in version 2)
    assert sorted({s["f"] for s in rule}) == [3.0, 4.0, 5.0, 6.0, 7.0]
    nonint = [s for s in ss if s["kind"] == "nonint"]
    assert [s["f"] for s in nonint] == [5.5] * 5 and sorted(s["V"] for s in nonint) == [-1, -0.5, 0, 0.5, 1]
    a0 = {s["V"]: s for s in rule if s["A"] == 0}
    for s in nonint:  # paired with the A = 0 point of the same V: only f (and gamma through p) differ
        assert a0[s["V"]]["s"] == pytest.approx(s["s"])


def test_one_job_has_every_descriptor():
    s = [x for x in eg.surfaces() if x["kind"] == "nonint"][0]
    r = eg.run_job((s, 101, 128, (0.13, 0.29), "direct"))
    v = r["values"]
    assert {"centroid_amp_raw", "centroid_amp_hann", "centroid_amp_pplus", "centroid_power_pplus", "sq_hann",
            "centroid_band_power_raw"} <= set(v)
    assert "centroid_band_power_hann" not in v
    hf = [k for k in v if k.startswith("hf_")]
    assert len(hf) == 2 * 3 * 3  # cutoffs x processings x variants
    r2 = eg.run_job((s, 101, 128, (0.13, 0.29), "decimate"))
    assert set(r2["values"]) == {"centroid_amp_raw"} | {f"hf_{c}_raw_{q}" for c in ("px", "phys")
                                                        for q in ("uint8", "float", "linear_height")}


def test_flip_surfaces_have_rms_slope_and_no_seed_dependence():
    a = [x for x in eg.surfaces() if x["name"] == "flip_a"][0]
    z1, _ = eg.make_z(a, 256, 1, 0.13, 0.29)
    z2, _ = eg.make_z(a, 256, 2, 0.13, 0.29)
    np.testing.assert_array_equal(z1, z2)
    c = a["amps"][0]
    assert np.sqrt(((2 * np.pi * 2 * c) ** 2 + (2 * np.pi * 60 * 0.316 * c) ** 2) / 2) == pytest.approx(0.01)
    # Conditions version 3: every tone lies below 64 cycles, so no grid of the file (N >= 128) aliases it
    b = [x for x in eg.surfaces() if x["name"] == "flip_b"][0]
    assert a["freqs"] == (2, 60) and b["freqs"] == (8,) and max(a["freqs"] + b["freqs"]) < 64


def test_pack_round_trip():
    rows = [{"surface": "a", "seed": 1, "crop": [0.0, 0.0], "N": 128, "sampling": "direct", "values": {"x": 1.5, "y": 2.0}},
            {"surface": "b", "seed": 2, "crop": [0.13, 0.29], "N": 128, "sampling": "decimate", "values": {"x": 0.1}}]
    assert eg.unpack(eg.pack(rows)) == rows
