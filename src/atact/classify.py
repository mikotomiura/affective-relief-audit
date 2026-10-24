"""Reconstruction of the classification of Sections 3.4 and 4.3 of Harada (2026) (120 surfaces near two corners, linear SVM).

Assumptions (numbering as in the README table):
  A4 Jitter: uniform U(-w, w) added to each coordinate and clipped to [-1, 1]; w is not given in the preprint
  A5 Seed of each surface: base_seed + index (the preprint states only "seed schedule")
  A6 Features are standardised before SVC(kernel="linear", C=1)
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

# The two regions of the preprint: positive/low-arousal and negative/high-arousal
REGIMES = {0: (1.0, -1.0), 1: (-1.0, 1.0)}


@dataclass(frozen=True)
class DatasetConfig:
    per_class: int = 60
    jitter: float = 0.2
    base_seed: int = 42
    render: RenderConfig = RenderConfig()


def default_features(H):
    return rq(H), centroid(H)


def make_dataset(cfg: DatasetConfig, rng_seed: int = 0, backend=None, features=None):
    """Return features X = (Rq, C), labels y, and the (V, A) used.

    backend has height(V, A, seed) (atact.backends); if None, the reconstruction under cfg.render is used.
    features maps H to two numbers; if None, the reconstruction of eqs. (5)(6) of Harada (2026) is used.
    Generator and descriptors can be replaced independently, so discrepancies with the original code can be isolated.
    """
    rng = np.random.default_rng(rng_seed)
    gen = (lambda V, A, sd: height(V, A, cfg.render, seed=sd)) if backend is None else backend.height
    feat = default_features if features is None else features
    X, y, va = [], [], []
    i = 0
    for label, (V0, A0) in REGIMES.items():
        for _ in range(cfg.per_class):
            V = float(np.clip(V0 + rng.uniform(-cfg.jitter, cfg.jitter), -1, 1))
            A = float(np.clip(A0 + rng.uniform(-cfg.jitter, cfg.jitter), -1, 1))
            H = gen(V, A, cfg.base_seed + i)
            X.append(tuple(feat(H)))
            y.append(label)
            va.append((V, A))
            i += 1
    return np.array(X), np.array(y), np.array(va)


def _svm():
    return make_pipeline(StandardScaler(), SVC(kernel="linear", C=1.0))


def evaluate(X, y, seed: int = 0) -> dict:
    """Same layout as Table 3 of Harada (2026): Rq only, centroid only, both, label permutation."""
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
