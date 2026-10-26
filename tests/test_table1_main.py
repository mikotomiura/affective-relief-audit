"""Checks of experiments/table1_main.py against the stored judgement of the predictions (results/k5_classification.json)."""

from __future__ import annotations

import collections
import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import table1_main as t  # noqa: E402


@pytest.fixture(scope="module")
def rows():
    return t.load_rows()


def violations(rows) -> collections.Counter:
    ix = t.index(rows)
    bad = collections.Counter()
    for k, r in ix.items():
        for text in r["predicted_direction"] + r["predicted_order"]:
            if text != "none" and t.evaluate(text, k, ix) is False:
                bad[t.pid(text)] += 1
    return bad


def test_slice_has_56_cells_from_existing_rows(rows):
    cells = t.build(rows)
    assert len(cells) == 7 * 4 * 2
    assert len({(c["condition"], c["representation"], c["descriptor_set"]) for c in cells}) == 56
    assert all(c["N"] == 128 and c["processing"] == "raw" for c in cells)
    assert {c["w"] for c in cells if c["condition"] not in t.NULL} == {0.3}
    assert {c["w"] for c in cells if c["condition"] in t.NULL} == {None}


def test_reevaluation_matches_stored_judgement(rows):
    """Over all 544 rows, the per-row evaluation reproduces the violation counts of the stored judgement.

    Multiplicities: P-K5-2 and P-K5-11 tag both N rows of a pair; P-K5-8 tags the three w rows of a column;
    P-K5-10 tags the S and C rows of a violating cell; P-K5-1 counts a cell once if either classifier fails.
    """
    stored = {k: sum(p.get("violations", 0) or 0 for p in v) for k, v in
              t.json.loads(t.SRC.read_text())["summary"]["predictions"].items()}
    got = violations(rows)
    assert got["P-K5-1"] == 7          # union of 4 (svm) and 4 (threshold) cells sharing one
    assert got["P-K5-2"] == 2 * stored["P-K5-2"]
    assert got["P-K5-3"] == stored["P-K5-3"] == 11
    for p in ("P-K5-4", "P-K5-5", "P-K5-6", "P-K5-9", "P-K5-11"):
        assert got[p] == stored[p] == 0
    assert got["P-K5-7"] == stored["P-K5-7"] == 7
    assert got["P-K5-8"] == 3 * stored["P-K5-8"] == 30
    assert got["P-K5-10"] == 2 * stored["P-K5-10"] == 6
    assert got["P-K5-12"] == stored["P-K5-12"] == 12


def test_changed_accuracy_changes_the_mark(rows):
    """Positive control: lowering the stored svm accuracy of one cell makes its P-K5-7 mark fail."""
    rows2 = copy.deepcopy(rows)
    for r in rows2:
        if (r["condition"], r["w"], r["N"], r["processing"], r["representation"], tuple(r["descriptor_set"])) == (
                "corners", 0.3, 128, "raw", "H", ("sq", "centroid_amp")):
            r["estimate_finite_svm"] = 0.9
    cell = next(c for c in t.build(rows2) if (c["condition"], c["representation"], c["descriptor_set"]) ==
                ("corners", "H", "SC"))
    assert any(p["id"] == "P-K5-7" and p["holds"] is False for p in cell["predictions"])


def test_wrong_source_is_refused(tmp_path, monkeypatch):
    bad = tmp_path / "k5.json"
    bad.write_text("{}")
    monkeypatch.setattr(t, "SRC", bad)
    with pytest.raises(SystemExit):
        t.load_rows()
