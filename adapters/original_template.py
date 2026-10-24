"""Template for an adapter wrapping the original code (ESM_1.zip).

Usage:
  1. Unpack ESM_1.zip into external/esm1/ (external/ is outside git). Read its contents before proceeding.
  2. Copy this file to adapters/original.py and fill the TODOs below with functions of the original code.
  3. Run uv run pytest -q tests/test_backends.py to check that the adapter keeps its contract.

The function names and arguments of the original code are not known. Here only what each function must return is fixed.
Leave anything absent from the original code returning None (that is itself a finding).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

NAME = "original"
ESM = Path(__file__).resolve().parents[1] / "external" / "esm1"

# TODO: import the module of the original code. Example:
# sys.path.insert(0, str(ESM / "src"))
# import affective_relief as orig


def height(V: float, A: float, seed: int = 42) -> np.ndarray:
    """H = s T_gamma(F), eq. (4) of Harada (2026). Height with units, before min-max. A 128 x 128 grid is assumed."""
    raise NotImplementedError("元のコードの高さの関数を呼ぶ")


def field(f: float, seed: int = 42, n: int = 128) -> np.ndarray | None:
    """F before T_gamma is applied (n x n). None if the original code does not separate it.

    If the grid size n cannot be varied, return None for n != 128 (the check of Proposition 6 is then skipped).
    """
    return None


def params(V: float, A: float):
    """(f, s, gamma). The mapping of the original code. If it differs from eqs. (1)-(3), that is a finding."""
    return None


def features(H: np.ndarray):
    """(Rq, C) of the original code. Used to see differences in the implementation of eqs. (5)(6)."""
    return None


def dataset():
    """(X, y) produced by the original code. X is 120 x 2 (Rq, C); y is 0/1.

    The label orientation matches the reconstruction: 0 = positive/low-arousal, 1 = negative/high-arousal.
    If the original code saved a matrix (e.g. CSV), it suffices to read it.
    """
    return None


def fig3_heights():
    """The three panels of Fig. 3, {"calm": H, "anger": H, "complex": H}: heights produced by the procedure the original code uses to draw the figure.

    Fig. 3 is drawn on a 256 x 256 grid (not the 128 of Table 2; see the head of atact.fig3).
    None if the original code has no function that draws the figure. Return the height before colouring.
    """
    return None
