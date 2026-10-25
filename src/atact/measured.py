"""Readers for the measured data of validation 3 (spec S5): Surface-Topography Challenge heights (NetCDF 3) and
TactileDreamFusion normal maps (PNG)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

_TO_METRES = {"m": 1.0, "mm": 1e-3, "um": 1e-6, "µm": 1e-6, "nm": 1e-9, "pm": 1e-12}


def unit_factor(unit) -> float:
    """Factor that converts a length in `unit` to metres (S5.1)."""
    u = unit.decode() if isinstance(unit, bytes) else str(unit)
    if u not in _TO_METRES:
        raise ValueError(f"unknown unit {u!r}")
    return _TO_METRES[u]


def read_challenge(path: Path) -> tuple[np.ndarray, float, float]:
    """S5.1: the variable `heights` of a -squeezed.nc file, in metres, indexed [y, x] (row = y, as in S1.1).

    The file stores heights with dimensions (x, y); the array is transposed. Returns (z, dx, dy), where dx and dy are
    the pixel spacings in metres, the `length` attribute of x and y divided by the number of points.
    """
    from scipy.io import netcdf_file

    with netcdf_file(path, "r", mmap=False) as nc:
        h = nc.variables["heights"]
        if h.dimensions != ("x", "y"):
            raise ValueError(f"unexpected dimensions {h.dimensions}")
        z = np.array(h.data, dtype=float) * unit_factor(h._attributes["unit"])
        fill = h._attributes.get("_FillValue")
        if fill is not None and np.any(np.asarray(h.data) == fill):
            raise ValueError("array contains fill values")
        out = []
        for name in ("x", "y"):
            v = nc.variables[name]
            out.append(float(v._attributes["length"]) * unit_factor(v._attributes["unit"]) / len(v.data))
    return z.T.copy(), out[0], out[1]


def largest_pow2(n: int) -> int:
    """S5.2: the largest power of two not exceeding n."""
    return 1 << (int(n).bit_length() - 1)


def central_crop(a: np.ndarray, p: int) -> np.ndarray:
    """The central p x p block of a 2-D array (or of the first two axes)."""
    r0 = (a.shape[0] - p) // 2
    c0 = (a.shape[1] - p) // 2
    if r0 < 0 or c0 < 0:
        raise ValueError("crop larger than the array")
    return a[r0:r0 + p, c0:c0 + p]


def read_normal_png(path: Path) -> np.ndarray:
    """S5.4: a normal map as uint8 RGB (an alpha channel, if present, is dropped)."""
    from PIL import Image

    with Image.open(path) as im:
        a = np.asarray(im)
    if a.ndim != 3 or a.shape[2] not in (3, 4) or a.dtype != np.uint8:
        raise ValueError(f"unexpected image {a.shape} {a.dtype}")
    return a[..., :3].copy()
