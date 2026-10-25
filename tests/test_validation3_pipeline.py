"""Runs the pipeline of experiments/validation3_public.py on synthetic files written in a temporary directory
(no measured data are read): readers (S5.1, S5.4), crop and plane removal (S5.2), levels (S5.3), SHA-256 checks,
analysis and report."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import numpy as np
import pytest
from PIL import Image
from scipy.io import netcdf_file

from atact.measured import read_challenge

spec = importlib.util.spec_from_file_location(
    "validation3_public", Path(__file__).resolve().parents[1] / "experiments" / "validation3_public.py")
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)


def write_nc(path: Path, z: np.ndarray, unit: str, length: tuple[float, float]):
    """A -squeezed.nc file laid out as in the Challenge deposit: heights with dimensions (x, y)."""
    with netcdf_file(path, "w") as nc:
        nc.createDimension("x", z.shape[0])
        nc.createDimension("y", z.shape[1])
        h = nc.createVariable("heights", "d", ("x", "y"))
        h[:] = z
        h.unit = unit
        for name, n, ln in (("x", z.shape[0], length[0]), ("y", z.shape[1], length[1])):
            v = nc.createVariable(name, "d", (name,))
            v[:] = np.arange(n) * ln / n
            v.length = ln
            v.unit = unit


def test_s5_1_reader_transposes_and_converts_units(tmp_path):
    z = np.arange(6.0).reshape(2, 3)  # (x, y)
    write_nc(tmp_path / "a.nc", z, "nm", (2.0, 3.0))
    out, dx, dy = read_challenge(tmp_path / "a.nc")
    np.testing.assert_allclose(out, z.T * 1e-9)
    assert dx == pytest.approx(1e-9) and dy == pytest.approx(1e-9)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_pipeline_on_synthetic_files(tmp_path, monkeypatch):
    rng = np.random.default_rng(0)
    ch_dir = tmp_path / "ch" / "bundle"
    meas = []
    for k, (cont, shape, surf) in enumerate([("c1", (80, 70), "rough"), ("c1", (64, 64), "rough"),
                                             ("c2", (72, 90), "smooth"), ("c3", (70, 66), "smooth")]):
        (ch_dir / cont).mkdir(parents=True, exist_ok=True)
        p = ch_dir / cont / f"{k}-squeezed.nc"
        z = np.cumsum(rng.normal(size=shape), axis=0) * (k + 1) + 0.3 * np.arange(shape[1])
        write_nc(p, z, "um", (shape[0] * 1.0, shape[1] * 1.0))
        meas.append({"container": cont, "file": p.name, "sha256": sha(p), "P": 64, "surface": surf})
    tdf_dir = tmp_path / "tdf"
    files = []
    for obj in ("A", "B", "C"):
        (tdf_dir / obj).mkdir(parents=True)
        for name, side, alpha in (("normal_patch.png", 48, True), ("tiled_normal_map.png", 1100, False)):
            v = np.stack([rng.normal(0, 0.1, (side, side)), rng.normal(0, 0.1, (side, side)), np.ones((side, side))], -1)
            v /= np.linalg.norm(v, axis=-1, keepdims=True)
            rgb = np.round((v + 1) / 2 * 255).astype(np.uint8)
            if alpha:
                rgb = np.concatenate([rgb, np.full((side, side, 1), 255, np.uint8)], -1)
            Image.fromarray(rgb).save(tdf_dir / obj / name)
            files.append({"file": f"{obj}/{name}", "sha256": sha(tdf_dir / obj / name)})
    c = {"datasets": [{"source": "synthetic", "license": "-", "measurements": meas},
                      {"source": "synthetic", "license": "-", "files": files}],
         "predictions": [f"P-V{i} text" for i in range(1, 6)]}
    monkeypatch.setattr(v3, "CHALLENGE_DIR", tmp_path / "ch")
    monkeypatch.setattr(v3, "TDF_DIR", tdf_dir)
    rows = v3.compute(c)
    ch_rows = [r for r in rows if r["dataset"] == "challenge"]
    assert len(ch_rows) == 4 * 6  # full (both methods), half and quarter by two methods
    assert sorted({r["n"] for r in ch_rows}) == [16, 32, 64]
    full = [r for r in ch_rows if r["level"] == "full"]
    assert all(r["values"] == full[0]["values"] for r in full[:2])  # full is shared by both methods
    tiled = [r for r in rows if r["dataset"] == "tdf" and r["input"] == "tiled"]
    assert sorted({r["n"] for r in tiled}) == [256, 512, 1024]
    S = v3.analyse(c, rows)
    meta = {k: "-" for k in ("conditions_sha256", "spec_sha256", "numpy", "scipy", "python", "started", "finished", "platform")}
    md = v3.write_report(c, meta, S, rows)
    assert "P-V3" in md and "| c1/0-squeezed.nc |" in md
    # Same-container pairs are not in the main count: 4 measurements -> 6 pairs, 1 within container c1
    lp = S["challenge"]["decimate_fourier/hf_ratio_px"]["V2"]["level_pairs"][0]
    assert lp["pairs_main"] == 5 and lp["pairs_same_container"] == 1
    # A changed file stops the run before any value is read
    p = ch_dir / "c1" / "0-squeezed.nc"
    p.write_bytes(p.read_bytes() + b"\0")
    with pytest.raises(SystemExit):
        v3.compute(c)
