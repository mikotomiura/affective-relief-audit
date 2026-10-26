"""Checks of the numbers plotted by experiments/figures_main.py (not of the drawing)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import figures_main as fm  # noqa: E402

from atact.mapping import params


def test_fig4_series_are_the_stored_k4_means():
    cells = json.loads(fm.K4.read_text())["summary"]["cells"]
    man = json.loads((fm.FIGS / "figures_main.json").read_text())["fig4"]["series"]
    for c in cells:
        key = f"{c['field']}|f={c['f']}|gamma={c['gamma']}"
        if key in man and c["processing"] == "raw" and c["descriptor"] == "centroid_amp" and c["sampling"] == "direct":
            assert man[key] == c["mean_by_N"]
    assert len([k for k in man if "supplement" not in k]) == 3 * 2 * 4


def test_fig2_panels_follow_the_rule():
    panels = json.loads((fm.FIGS / "figures_main.json").read_text())["fig2"]["panels"]
    assert len(panels) == 25
    for p in panels:
        assert params(p["V"], p["A"]) == pytest.approx((p["f"], p["s"], p["gamma"]))
        assert 0 <= p["common_range"][0] <= p["common_range"][1] <= 1


def test_fig3_uses_the_registered_results():
    man = json.loads((fm.FIGS / "figures_main.json").read_text())["fig3"]
    res = json.loads(fm.K2.read_text())
    assert man["eps"] == res["analysis"]["eps"]["main"]
    assert man["sources"]["results/k2_gradient.json"] == fm.sha256(fm.K2)
    assert man["series"]["high"]["M"] == res["analysis"]["points"]["high"]["M"]["seed_mean_by_N"]
