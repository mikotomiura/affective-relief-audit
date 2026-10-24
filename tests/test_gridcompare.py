"""解像度をまたぐ比較の部品（atact.gridcompare）の確かめ。"""

import numpy as np

from atact.gridcompare import (border_discontinuity, center_crop, field_and_grad, glcm_score,
                               gradient_continuity, height_scale, resize_lanczos, seam_metrics,
                               upsample)


def test_glcm_score_constant_below_noise():
    rng = np.random.default_rng(0)
    flat = np.full((128, 128), 100, np.uint8)
    noise = rng.integers(0, 256, (128, 128)).astype(np.uint8)
    assert glcm_score(flat) < glcm_score(noise)


def test_seam_metrics_match_hand_computation():
    img = np.array([[0, 1, 3], [2, 2, 2], [5, 4, 0]], np.float32)[..., None].repeat(3, -1)
    # x: 右端と左端の差の絶対値 |3-0|, |2-2|, |0-5| の平均
    assert abs(border_discontinuity(img, "x") - (3 + 0 + 5) / 3) < 1e-6
    # x の 1 行目: across = 0-3 = -3, right = 3-1 = 2, left = 1-0 = 1 -> |-3-2| + |1+3| = 9
    row1 = 9.0
    row2 = 0.0
    # 3 行目: across = 5-0 = 5, right = 0-4 = -4, left = 4-5 = -1 -> |5+4| + |-1-5| = 15
    row3 = 15.0
    assert abs(gradient_continuity(img, "x") - (row1 + row2 + row3) / 3) < 1e-6


def test_periodic_field_has_small_border_after_resize():
    # f が奇数なら中央の半分は基本の段で継ぎ目をもつ（f が偶数だと切り出しも周期的になる）
    _, fx, fy = field_and_grad(3, 4, 256, 1)
    h0 = height_scale(3, 4, 0.3)
    v = np.stack([-h0 * fx, h0 * fy, np.ones_like(fx)], -1)
    rgb = np.round((v / np.linalg.norm(v, axis=-1, keepdims=True) + 1) / 2 * 255).astype(np.uint8)
    assert seam_metrics(resize_lanczos(rgb, 128))["border_avg"] < seam_metrics(center_crop(rgb, 128))["border_avg"]


def test_fourier_upsampling_reproduces_native_gradient():
    _, fx, fy = field_and_grad(4, 3, 64, 2, max_freq=16)
    _, gx, gy = field_and_grad(4, 3, 256, 2, max_freq=16)
    up = upsample(np.stack([fx, fy], -1), 256, "fourier")
    assert np.allclose(up[..., 0], gx, atol=1e-8) and np.allclose(up[..., 1], gy, atol=1e-8)


def test_height_scale_gives_target_rms_slope():
    _, fx, fy = field_and_grad(4, 5, 512, 3)
    h0 = height_scale(4, 5, 0.3)
    assert abs(np.sqrt(np.mean(h0**2 * (fx**2 + fy**2))) - 0.3) < 1e-6


def test_dropped_octaves_keep_remaining_phases():
    a, _, _ = field_and_grad(4, 3, 64, 5)
    b, _, _ = field_and_grad(4, 6, 64, 5, max_freq=16)
    assert np.allclose(a, b)
