"""Interchangeable generator backends: the reconstructed generator and the original code (ESM_1.zip) are called through the same interface.

The API of the original code is not known, so a thin adapter wrapping it (adapters/original.py) is to be
written once the code is available. The template is adapters/original_template.py. An adapter is a module with these names:

  NAME: str
  height(V, A, seed) -> 2-D ndarray              required. H of eq. (4) of Harada (2026) (before centring is acceptable)
  field(f, seed, n=128) -> ndarray | None       optional. F before T_gamma is applied. If n cannot be varied,
                                                return None for n != 128 (the check of Proposition 6 is then skipped)
  params(V, A) -> (f, s, gamma) | None          optional. Eqs. (1)-(3) of Harada (2026)
  features(H) -> (Rq, C) | None                 optional. The descriptors of the original code
  dataset() -> (X, y) | None                    optional. Features and labels of the 120 surfaces produced by the original code
  fig3_heights() -> {name: ndarray} | None       optional. Heights of the three panels of Fig. 3 of Harada (2026) (calm / anger / complex).
                                                Fig. 3 is redrawn with the original code and compared with the heights recovered from the figure

An optional name is a function returning None when the original code has no corresponding function.
"""

from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass, field as dc_field, replace
from pathlib import Path
from types import ModuleType

import numpy as np

from . import mapping
from .descriptors import centroid, rq
from .field import RenderConfig, height, procedural_field

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ADAPTER = ROOT / "adapters" / "original.py"


@dataclass
class ReconBackend:
    """Reconstructed generator. The render configuration switches between assumptions A1-A3."""

    render: RenderConfig = dc_field(default_factory=RenderConfig)
    NAME: str = "recon"

    def height(self, V, A, seed=42):
        return height(V, A, self.render, seed)

    def field(self, f, seed=42, n=None):
        cfg = self.render if n is None else replace(self.render, n=n)
        return procedural_field(float(f), cfg, seed)

    def params(self, V, A):
        return tuple(float(x) for x in mapping.params(V, A))

    def features(self, H):
        return rq(H), centroid(H)

    def dataset(self):
        return None

    def fig3_heights(self):
        return None


class AdapterBackend:
    """Wrap an adapter module, filling each missing optional function with one returning None."""

    def __init__(self, mod: ModuleType):
        if not hasattr(mod, "height"):
            raise AttributeError(f"{mod.__file__}: no height(V, A, seed)")
        self._m = mod
        self.NAME = getattr(mod, "NAME", Path(mod.__file__).stem)

    def height(self, V, A, seed=42):
        return np.asarray(self._m.height(V, A, seed), dtype=float)

    def _opt(self, name, *a):
        fn = getattr(self._m, name, None)
        return None if fn is None else fn(*a)

    def field(self, f, seed=42, n=None):
        F = self._opt("field", f, seed) if n is None else self._opt("field", f, seed, n)
        return None if F is None else np.asarray(F, dtype=float)

    def params(self, V, A):
        return self._opt("params", V, A)

    def features(self, H):
        return self._opt("features", H)

    def dataset(self):
        return self._opt("dataset")

    def fig3_heights(self):
        out = self._opt("fig3_heights")
        return None if out is None else {k: np.asarray(v, dtype=float) for k, v in out.items()}


def adapter_path() -> Path | None:
    """Environment variable ATACT_ORIGINAL_ADAPTER, or adapters/original.py. None if neither exists."""
    p = os.environ.get("ATACT_ORIGINAL_ADAPTER")
    path = Path(p) if p else DEFAULT_ADAPTER
    return path if path.exists() else None


def load_adapter(path: str | Path) -> AdapterBackend:
    """Load the adapter. Loading imports and runs the original code, so read its contents first."""
    path = Path(path)
    spec = importlib.util.spec_from_file_location(f"atact_adapter_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return AdapterBackend(mod)


def original() -> AdapterBackend | None:
    p = adapter_path()
    return None if p is None else load_adapter(p)


def available() -> dict:
    """Return the available generators by name. The original code is included only if an adapter exists."""
    out = {"recon": ReconBackend(), "recon_warp": ReconBackend(RenderConfig(warp=0.25))}
    o = original()
    if o is not None:
        out["original"] = o
    return out
