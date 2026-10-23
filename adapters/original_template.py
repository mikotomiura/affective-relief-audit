"""元のコード（ESM_1.zip）を包むアダプタのひな形。

使い方:
  1. ESM_1.zip を external/esm1/ に展開する（external/ は git の外）。中身を読んでから先へ進む。
  2. このファイルを adapters/original.py に写し、下の TODO を元のコードの関数で埋める。
  3. uv run pytest -q tests/test_backends.py で、アダプタが約束を守るかを確かめる。

元のコードの関数名や引数は届くまで分からない。ここでは「何を返せばよいか」だけを決める。
元のコードに無いものは None を返したままにする（それ自体が分かったことになる）。
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

NAME = "original"
ESM = Path(__file__).resolve().parents[1] / "external" / "esm1"

# TODO: 元のコードのモジュールを import する。例:
# sys.path.insert(0, str(ESM / "src"))
# import affective_relief as orig


def height(V: float, A: float, seed: int = 42) -> np.ndarray:
    """式 (4) の H = s T_gamma(F)。min-max の前の、単位のある高さ。128 x 128 を想定。"""
    raise NotImplementedError("元のコードの高さの関数を呼ぶ")


def field(f: float, seed: int = 42, n: int = 128) -> np.ndarray | None:
    """T_gamma をかける前の F（n x n）。元のコードが分けていなければ None。

    格子の大きさ n を変えられなければ、n != 128 のときに None を返す（命題 6 の検査が skip になる）。
    """
    return None


def params(V: float, A: float):
    """(f, s, gamma)。元のコードの写像。式 (1)-(3) と違えば、それが所見になる。"""
    return None


def features(H: np.ndarray):
    """元のコードの (Rq, C)。式 (5)(6) の実装の違いを見るために使う。"""
    return None


def dataset():
    """元のコードが作った (X, y)。X は 120 x 2 の (Rq, C)、y は 0/1。

    ラベルの向きは recon と合わせる: 0 = positive/low-arousal、1 = negative/high-arousal。
    元のコードが保存した行列（CSV など）があれば、それを読むだけでよい。
    """
    return None


def fig3_heights():
    """図 3 の 3 枚 {"calm": H, "anger": H, "complex": H}。元のコードの図を描く手順で作った高さ。

    図 3 は 256 x 256 の格子で描かれている（表 2 の 128 ではない。atact.fig3 の冒頭を参照）。
    元のコードが図を描く関数を持っていなければ None。色を付ける前の高さを返す。
    """
    return None
