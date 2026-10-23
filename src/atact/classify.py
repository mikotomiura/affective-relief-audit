"""原稿 3.4 節・4.3 節の分類の組み直し（2 つの隅の付近から 120 枚、線形 SVM）。

仮定（README の表と対応）:
  A4 ジッタは座標ごとに一様 U(-w, w) を足して [-1, 1] で切る。w は原稿に無い
  A5 各表面の種は base_seed + 番号（原稿は "seed schedule" とだけ書く）
  A6 特徴は標準化してから SVC(kernel="linear", C=1)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from .descriptors import centroid, rq
from .field import RenderConfig, height

# 原稿の 2 つの領域: positive/low-arousal と negative/high-arousal
REGIMES = {0: (1.0, -1.0), 1: (-1.0, 1.0)}


@dataclass(frozen=True)
class DatasetConfig:
    per_class: int = 60
    jitter: float = 0.2
    base_seed: int = 42
    render: RenderConfig = RenderConfig()


def make_dataset(cfg: DatasetConfig, rng_seed: int = 0):
    """特徴 X = (Rq, C) とラベル y と、使った (V, A) を返す。"""
    rng = np.random.default_rng(rng_seed)
    X, y, va = [], [], []
    i = 0
    for label, (V0, A0) in REGIMES.items():
        for _ in range(cfg.per_class):
            V = float(np.clip(V0 + rng.uniform(-cfg.jitter, cfg.jitter), -1, 1))
            A = float(np.clip(A0 + rng.uniform(-cfg.jitter, cfg.jitter), -1, 1))
            H = height(V, A, cfg.render, seed=cfg.base_seed + i)
            X.append((rq(H), centroid(H)))
            y.append(label)
            va.append((V, A))
            i += 1
    return np.array(X), np.array(y), np.array(va)


def _svm():
    return make_pipeline(StandardScaler(), SVC(kernel="linear", C=1.0))


def evaluate(X, y, seed: int = 0) -> dict:
    """原稿の表 3 と同じ並び: Rq だけ・重心だけ・両方・ラベルの並べ替え。"""
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=seed)
    out = {}
    for name, cols in {"rq": [0], "centroid": [1], "both": [0, 1]}.items():
        sc = cross_val_score(_svm(), X[:, cols], y, cv=cv)
        out[name] = (float(sc.mean()), float(sc.std()))
    yp = np.random.default_rng(seed).permutation(y)
    sc = cross_val_score(_svm(), X, yp, cv=cv)
    out["permuted"] = (float(sc.mean()), float(sc.std()))
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)
    out["holdout"] = float(_svm().fit(Xtr, ytr).score(Xte, yte))
    return out
