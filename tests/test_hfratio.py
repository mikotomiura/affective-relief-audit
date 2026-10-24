"""HF ratio の写し（atact.hfratio）と、切り出しの場（experiments/hf_ratio_edge.py）の確かめ。"""

import importlib.util
from pathlib import Path

import numpy as np

from atact.field import RenderConfig, procedural_field
from atact.hfratio import cutoff_ratio, hf_ratio, normal_rgb_from_height

spec = importlib.util.spec_from_file_location(
    "hf_ratio_edge", Path(__file__).resolve().parents[1] / "experiments" / "hf_ratio_edge.py")
exp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp)


def test_flat_normal_map_has_zero_ratio():
    rgb = normal_rgb_from_height(np.zeros((64, 64)))
    assert hf_ratio(rgb) == 0.0


def test_cutoff_is_fixed_in_pixels():
    # cutoff = cutoff_ratio * 半対角 = N / (120 * FWHM)。画素あたりの周期にすると N によらない
    for n in (256, 1024):
        c = cutoff_ratio(n, n, 120) * np.hypot(n // 2, n // 2)
        assert abs(c / n - 1 / (120 * np.sqrt(2 * np.log(2)))) < 1e-9


def test_field_at_zero_offset_matches_generator():
    F = exp.field(5.5, 4, 128, 3, 0.0, 0.0)
    G = procedural_field(5.5, RenderConfig(n=128, normalize="none"), seed=3) / 1.875
    assert np.allclose(F, G)


def test_integer_f_is_shift_invariant_under_periodic_crop():
    # f が整数なら窓をずらしても表面は巡回シフトになり、DFT のエネルギー比は変わらない（量子化の誤差を除く）
    a = exp.field(5.0, 4, 128, 1, 0.0, 0.0)
    b = exp.field(5.0, 4, 128, 1, 0.5, 0.25)
    assert np.allclose(np.roll(a, (-32, -64), axis=(0, 1)), b, atol=1e-9)


def test_high_frequency_content_raises_ratio():
    n = 256
    y, x = np.mgrid[0:n, 0:n] / n
    lo = hf_ratio(normal_rgb_from_height(0.01 * np.sin(2 * np.pi * 2 * x)))
    hi = hf_ratio(normal_rgb_from_height(0.001 * np.sin(2 * np.pi * 64 * x)))
    assert hi > lo
