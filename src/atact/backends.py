"""生成器の差し替え口。組み直しの生成器と、元のコード（ESM_1.zip）を同じ形で呼ぶ。

元のコードの API は分からないので、元のコードを包む薄いアダプタ（adapters/original.py）を
届いてから書く。ひな形は adapters/original_template.py。アダプタは次の名前を持つモジュール:

  NAME: str
  height(V, A, seed) -> 2 次元の ndarray      必須。式 (4) の H（中心化の前でよい）
  field(f, seed, n=128) -> ndarray | None       任意。T_gamma をかける前の F。n を変えられなければ
                                                n != 128 で None を返す（命題 6 の検査が skip になる）
  params(V, A) -> (f, s, gamma) | None          任意。式 (1)-(3)
  features(H) -> (Rq, C) | None                 任意。元のコードの記述子
  dataset() -> (X, y) | None                    任意。元のコードが作った 120 枚の特徴とラベル
  fig3_heights() -> {name: ndarray} | None       任意。図 3 の 3 枚（calm / anger / complex）の高さ。
                                                元のコードで図 3 を描き直し、図から取り戻した高さと比べる

任意のものは、元のコードに相当する関数が無ければ None を返す関数にしておく。
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
    """組み直しの生成器。render で A1〜A3 の仮定を切り替える。"""

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
    """アダプタのモジュールを、足りない任意の関数を None で埋めて包む。"""

    def __init__(self, mod: ModuleType):
        if not hasattr(mod, "height"):
            raise AttributeError(f"{mod.__file__}: height(V, A, seed) がない")
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
    """環境変数 ATACT_ORIGINAL_ADAPTER か、adapters/original.py。無ければ None。"""
    p = os.environ.get("ATACT_ORIGINAL_ADAPTER")
    path = Path(p) if p else DEFAULT_ADAPTER
    return path if path.exists() else None


def load_adapter(path: str | Path) -> AdapterBackend:
    """アダプタを読み込む。読み込むと元のコードが import されて動くので、先に中身を読むこと。"""
    path = Path(path)
    spec = importlib.util.spec_from_file_location(f"atact_adapter_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return AdapterBackend(mod)


def original() -> AdapterBackend | None:
    p = adapter_path()
    return None if p is None else load_adapter(p)


def available() -> dict:
    """使える生成器を名前で返す。元のコードは、アダプタがあるときだけ入る。"""
    out = {"recon": ReconBackend(), "recon_warp": ReconBackend(RenderConfig(warp=0.25))}
    o = original()
    if o is not None:
        out["original"] = o
    return out
