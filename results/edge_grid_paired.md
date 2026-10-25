# Paired comparison of edge and grid effects

Conditions: `experiments/conditions/edge_grid_paired.json` (SHA-256 `1ca8bfcbd382c28fd00c508e7e0004f9eecc95ee5c6f5989d7c93660e1be5a51`). Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`). numpy 2.5.4, scipy 1.18.1, Python 3.13.12. Run started 2026-10-25T02:56:57+00:00 and finished 2026-10-25T12:53:15+00:00 (Darwin arm64, 10 logical CPUs).

This computation extends an earlier one whose results had been seen (hf_ratio_edge.json, commits c2ee719 and 82efec2); it is not blind to those results. Values after a window, the periodic-plus-smooth decomposition or band fixing are not regarded as true values. Reference scale from Table 1 of Gao et al. (2026): differences in HF ratio between the compared models of 0.009-0.103.

## Reading of the conditions fixed before the run

- Conditions version 3. The five points with A = 0.25 (f = 5.5) are surfaces like the rule points but are not among the 25 rule points used for C3, C4 and C5; they enter C1, C2, the aliasing subset and P-E2 to P-E5.
- flip_positive (version 3): surface a is z = c (sin(2 pi 2 x') + 0.316 sin(2 pi 60 x')) and surface b is z = c' sin(2 pi 8 x'), with x' = x + x0 (zero phases; the crop offset shifts the tones), constant along y, in units of L. The amplitudes c and c' give a continuous RMS slope of 0.01. The surfaces have no random element, so the ten seeds give identical values; their standard error is 0 and, by S6.2, any change of sign with a non-zero difference counts as a flip. Height descriptors of these surfaces are computed on z.
- Normal maps of the rule points and sine controls come from z = H/30 (S2.8 with side 1). The float variant uses the unit normals before the uint8 encoding; for 'hann' it applies the window of S3.1 to those normals and renormalises without rounding. The linear-height variant uses z itself: raw z, the windowed z of S3.1 for 'hann', and the periodic component of S3.2 for 'pplus'.
- S6.2 order: the order of two surfaces at a level is the sign of the mean over seeds of sign(D_a - D_b); a flip also requires the mean paired difference to exceed twice its standard error over seeds at both levels.
- C3 is computed for each N and crop. The ratio (mean over seeds of C1) / C3 is reported for the C3 of each crop at the same N; the summary ratio uses the largest C3 over the crops (so that it is not inflated by a small C3). |C2| / C3 uses the C3 of the same crop at N = 2048, averaged over crops. C2 is the value at N = 2048 minus the value at N = 128 for each seed and crop; its mean and standard error are reported per crop (paired by seed), and the crop-averaged standard error is taken over the seed-level averages across crops (crops share seeds).
- C5: within each processing, the descriptors (the height descriptors computed under that processing, and the HF ratio in its two cutoffs and three variants under that processing) are ranked by the absolute standardised difference |d| between the corners (V, A) = (1, -1) and (-1, 1), d = (mean_a - mean_b) / sqrt((var_a + var_b)/2) over seeds; the signed d is reported. Whether the ranking changes is reported by counting distinct rankings.
- Operational criteria for the predictions (the condition file states directions; these were fixed in this script before the computation): P-E1 'below 1e-9 in relative terms' uses C1 and |C2| divided by the mean value; 'decreases monotonically' uses the mean over seeds and crops at successive N; P-E2 holds at an N if, for each V, the mean C1 of the point (V, 0.25) exceeds that of the rule point (V, 0), and the mean C1 of sine_jump exceeds that of every rule point with A = 0; the prediction holds if this is so at every N; P-E3 holds if the mean C1 of at least one point with A = 0.25 exceeds C3 at N = 2048 for every crop (that is, the largest C3 over crops); P-E4 compares the mean C1 (absolute) of hann centroid_amp and of pplus centroid_amp with raw centroid_amp, and of centroid_band_power with raw centroid_power (the same weighting over the full band), for each of the five points with A = 0.25 at every N, and reports the comparison of C1 relative to the mean value beside it; P-E5 uses the 25 rule points, the five points with A = 0.25 and the two sine controls for the monotonicity and |C2| parts, and the flips of C4 (the 25 rule points, as defined in the conditions) for the flip parts, with uint8 raw for the HF ratio and flips counted over all pairs of grids within each crop; P-E6 compares the mean over seeds and crops of |decimated - direct| (absolute; the relative difference is reported beside it), noting that only the point (1, -1) has gamma <= 1; P-E7 requires a flip of the px linear ratio for every crop and no flip of the phys linear ratio for any crop.

## Conclusions by prediction (written after the run)

This section was written by the author after reading the tables below; it is not produced by `--report`. The decisions follow the operational criteria fixed in the script before the run, also where they fail for reasons stated here; no criterion was changed after the run.

- **P-E1 holds in 4 of 5 items.** The crop range and the change with N of raw centroid_amp, centroid_power and sq for sine_periodic are at most 1.8e-11 in relative terms, as expected for a circular shift of a periodic band-limited field, and the change with N of the px HF ratio (0.919) is far larger than that of phys (0.00015). The item 'px HF ratio decreases monotonically with N' does not hold: with uint8 rounding the values are 0.9326, 0.9331, 0.7164, 0.1443, 0.0138, an increase of 0.0005 from N = 128 to 256. Without rounding (float variant) the same surface decreases at every step (0.9832 to 0.0126), as does the linear-height ratio.
- **P-E2 holds** (5 of 5 grids): at every N the crop range of the five points with f = 5.5 exceeds that of the rule point with f = 5 at the same V (at N = 2048, 8.5-33.7 against 0.13-0.20), and that of sine_jump (90.5 at N = 2048) exceeds every rule point with A = 0.
- **P-E3 does not hold.** At N = 2048 the largest crop range among the points with f = 5.5 is 33.7, against a range over the rule of 431; the ratio C1/C3 is 0.020-0.078 for these points and 0.21 for sine_jump. The edge effect of a non-integer f is real (P-E2) but smaller than the differences between the rule points by more than an order of magnitude for this descriptor.
- **P-E4 holds** (25 of 25 cells for each of hann, pplus and centroid_band_power), in absolute and in relative terms.
- **P-E5 holds in 3 of 4 items.** The change with N is smaller for phys than for px for all 32 surfaces, the px ranking of the 25 rule points flips (4127 grid flips with uint8 raw, minimum Kendall's tau 0.020), and phys has fewer flips (80). The item 'px decreases with N for every surface' does not hold: with uint8 raw, 18 of the 32 surfaces decrease at every step. The 14 exceptions all occur between N = 128 and 256 (10 surfaces) or between 256 and 512 (4 surfaces, all with V = 1), where the ratio is near its upper end (0.87-0.96); the increases are 0.0005-0.026, and 13 of the 14 exceed twice their standard error over seeds. With the float variant all 32 surfaces decrease at every step, so the exceptions arise from the uint8 rounding at small N. Their size reaches the lower end of the reference scale (0.009).
- **P-E6 holds** (3 of 3 grids): the mean |decimated - direct| of centroid_amp for the points with gamma > 1 (5.5, 11.3, 22.6) exceeds that of the point with gamma <= 1 (1.2, 1.7, 2.3), also in relative terms (0.17-0.24 against 0.09-0.12). Only one rule point, (1, -1), has gamma <= 1, so this comparison rests on a single surface on that side; several points with gamma > 1 and A = -0.5 have smaller relative differences (0.025-0.069) than it does.
- **P-E7 holds** (4 of 4 items): the px linear-height ratio of the positive control changes order between grids in every crop (4 flips per crop) and the phys linear-height ratio in none; the px HF ratio also changes order, with uint8 rounding in two of the five crops and without rounding in all five.
- Grid change for the rule points: the mean |C2|/C3 is 0.92 for the px HF ratio (uint8 raw), 0.30 for phys, and 0.49 for raw centroid_amp; the crop range C1/C3 at N = 2048 is below 0.006 for every descriptor.

## Predictions

### P-E1: 4 of 5 items hold

Prediction: P-E1 (negative control): for sine_periodic, the crop range (C1) of raw centroid_amp, centroid_power and sq is below 1e-9 in relative terms (circular shift of a periodic band-limited field), and so is the change with N (C2). The px HF ratio decreases monotonically with N (Proposition 8, part 3); its change with N is larger than that of phys.

| part | rel_C1_max | rel_absC2 | values | px | phys | holds |
|---|---|---|---|---|---|---|
| centroid_amp_raw: crop range and grid change | 1.815e-12 | 1.777e-11 | - | - | - | yes |
| centroid_power_raw: crop range and grid change | 2.512e-16 | 9.044e-17 | - | - | - | yes |
| sq_raw: crop range and grid change | 1.696e-16 | 5.243e-17 | - | - | - | yes |
| hf px decreases with N (uint8 raw) | - | - | 0.9326, 0.9331, 0.7164, 0.1443, 0.0138 | - | - | no |
| |C2| px > |C2| phys | - | - | - | 0.9188 | 0.0001521 | yes |

### P-E2: 5 of 5 items hold

Prediction: P-E2: for sine_jump and the five points with A = 0.25 (f = 5.5), the crop range (C1) of raw centroid_amp is larger than for the five rule points with A = 0 (f = 5).

| N | C1_A0.25_by_V | C1_A0_by_V | C1_sine_jump | pairs_larger | holds |
|---|---|---|---|---|---|
| 128 | 1.088, 1.257, 1.474, 1.761, 2.158 | 0.1035, 0.09679, 0.08893, 0.08028, 0.06943 | 6.973 | 5 | yes |
| 256 | 1.722, 2.102, 2.613, 3.287, 4.2 | 0.1764, 0.1598, 0.1414, 0.1206, 0.09651 | 13.7 | 5 | yes |
| 512 | 3.107, 3.966, 5.094, 6.595, 8.611 | 0.171, 0.1533, 0.1335, 0.1122, 0.08973 | 26.11 | 5 | yes |
| 1024 | 5.283, 7.148, 9.59, 12.83, 17.22 | 0.177, 0.1617, 0.1458, 0.1262, 0.1021 | 48.86 | 5 | yes |
| 2048 | 8.535, 12.49, 17.72, 24.62, 33.7 | 0.197, 0.1886, 0.176, 0.1567, 0.1281 | 90.54 | 5 | yes |

### P-E3: 0 of 1 items hold

Prediction: P-E3: for raw centroid_amp at N = 2048, the crop range (C1) exceeds the range over the rule (C3) for at least one of the five points with A = 0.25. Which points do so is not predicted.

| N | C3_max_over_crops | points_exceeding | largest_C1 | holds |
|---|---|---|---|---|
| 2048 | 431 |  | 33.7 | no |

### P-E4: 3 of 3 items hold

Prediction: P-E4: for hann, pplus and centroid_band_power, the crop range (C1) of the five points with A = 0.25 is smaller than for raw.

| treatment | baseline | cells_smaller | cells_smaller_relative | cells | holds |
|---|---|---|---|---|---|
| centroid_amp_hann | centroid_amp_raw | 25 | 25 | 25 | yes |
| centroid_amp_pplus | centroid_amp_raw | 25 | 25 | 25 | yes |
| centroid_band_power_raw | centroid_power_raw | 25 | 25 | 25 | yes |

### P-E5: 3 of 4 items hold

Prediction: P-E5: the px HF ratio decreases with N for every surface (as in the earlier computation; Proposition 8, part 3). The change with N is smaller for phys than for px. With px there is at least one flip in the ranking of surfaces (C4); with phys there are fewer flips than with px.

| part | surfaces_decreasing | surfaces | surfaces_smaller | flips_px | flips_phys | holds |
|---|---|---|---|---|---|---|
| px decreases with N for every surface | 18 | 32 | - | - | - | no |
| |C2| phys < |C2| px | - | 32 | 32 | - | - | yes |
| flips px >= 1 | - | - | - | 4127 | - | yes |
| flips phys < px | - | - | - | 4127 | 80 | yes |

### P-E6: 3 of 3 items hold

Prediction: P-E6 (aliasing): for points with gamma > 1, the difference in centroid_amp between the decimate_fourier version and direct sampling is larger than for points with gamma <= 1.

| N | gamma_gt_1 | gamma_le_1 | relative_gt_1 | relative_le_1 | points_le_1 | holds |
|---|---|---|---|---|---|---|
| 128 | 5.527 | 1.197 | 0.1724 | 0.09129 | V+1.0_A-1.0 | yes |
| 256 | 11.31 | 1.72 | 0.211 | 0.1109 | V+1.0_A-1.0 | yes |
| 512 | 22.6 | 2.328 | 0.2449 | 0.1249 | V+1.0_A-1.0 | yes |

### P-E7: 4 of 4 items hold

Prediction: P-E7 (positive control): for flip_positive, the linear_height ratio with the px cutoff changes order between at least one pair of grids; with the phys cutoff it does not. For hf_ratio px on the same pair, the presence of a flip is predicted but not its location.

| descriptor | flips_per_crop | sign_a_minus_b_by_N | holds |
|---|---|---|---|
| hf_px_raw_linear_height | 4, 4, 4, 4, 4 | -1, -1, -1, -1, 1 | yes |
| hf_phys_raw_linear_height | 0, 0, 0, 0, 0 | -1, -1, -1, -1, -1 | yes |
| hf_px_raw_uint8 | 4, 0, 4, 0, 0 | -1, 1, 1, 1, 1 | yes |
| hf_px_raw_float | 6, 6, 6, 6, 6 | -1, -1, 1, 1, 1 | yes |

## C4: flips and Kendall's tau among the 25 rule points

Totals over the five crops and the ten pairs of grids (grid flips), and over the five N and the ten pairs of crops (crop flips).

| descriptor | grid flips | min tau over grid pairs | crop flips | min tau over crop pairs |
|---|---|---|---|---|
| centroid_amp_hann | 252 | 0.933 | 0 | 0.993 |
| centroid_amp_pplus | 117 | 0.953 | 0 | 0.987 |
| centroid_amp_raw | 50 | 0.987 | 0 | 1.000 |
| centroid_band_power_raw | 0 | 1.000 | 0 | 1.000 |
| centroid_power_hann | 0 | 1.000 | 0 | 1.000 |
| centroid_power_pplus | 0 | 1.000 | 0 | 1.000 |
| centroid_power_raw | 0 | 1.000 | 0 | 1.000 |
| hf_phys_hann_float | 145 | 0.920 | 0 | 1.000 |
| hf_phys_hann_linear_height | 0 | 1.000 | 0 | 1.000 |
| hf_phys_hann_uint8 | 134 | 0.873 | 0 | 0.987 |
| hf_phys_pplus_float | 90 | 0.920 | 0 | 0.993 |
| hf_phys_pplus_linear_height | 0 | 1.000 | 0 | 1.000 |
| hf_phys_pplus_uint8 | 86 | 0.913 | 0 | 1.000 |
| hf_phys_raw_float | 90 | 0.927 | 0 | 1.000 |
| hf_phys_raw_linear_height | 0 | 1.000 | 0 | 1.000 |
| hf_phys_raw_uint8 | 80 | 0.913 | 0 | 0.987 |
| hf_px_hann_float | 5275 | -0.340 | 0 | 1.000 |
| hf_px_hann_linear_height | 2181 | 0.177 | 0 | 0.950 |
| hf_px_hann_uint8 | 3725 | -0.080 | 0 | 0.680 |
| hf_px_pplus_float | 5416 | -0.340 | 0 | 1.000 |
| hf_px_pplus_linear_height | 4794 | -0.913 | 5 | 0.767 |
| hf_px_pplus_uint8 | 4171 | 0.007 | 0 | 0.880 |
| hf_px_raw_float | 5416 | -0.340 | 0 | 1.000 |
| hf_px_raw_linear_height | 2993 | -0.081 | 1 | 0.946 |
| hf_px_raw_uint8 | 4127 | 0.020 | 0 | 0.840 |
| sq_hann | 0 | 1.000 | 0 | 1.000 |
| sq_pplus | 0 | 1.000 | 0 | 1.000 |
| sq_raw | 0 | 1.000 | 0 | 1.000 |

## C5: ranking of descriptors by the separation of the corners (1, -1) and (-1, 1)

| processing | distinct rankings over N and crops (of 25) | descriptors ranked first |
|---|---|---|
| raw | 5 | hf_px_raw_linear_height, sq_raw |
| hann | 7 | hf_px_hann_linear_height, sq_hann |
| pplus | 6 | hf_px_pplus_linear_height, sq_pplus |

Rankings at the default crop (0, 0):

| processing | N | ranking (|d|, descending) |
|---|---|---|
| raw | 128 | sq_raw (-139.45), hf_phys_raw_linear_height (-107.44), centroid_band_power_raw (-70.11), centroid_amp_raw (-60.38), hf_px_raw_float (+42.68), hf_phys_raw_float (-24.87), centroid_power_raw (-24.32), hf_phys_raw_uint8 (-20.62), hf_px_raw_linear_height (-16.90), hf_px_raw_uint8 (+4.30) |
| raw | 256 | hf_px_raw_linear_height (-680.03), sq_raw (-139.45), hf_phys_raw_linear_height (-107.19), centroid_band_power_raw (-69.62), centroid_amp_raw (-62.74), hf_phys_raw_float (-31.90), hf_phys_raw_uint8 (-25.48), centroid_power_raw (-23.16), hf_px_raw_float (+22.22), hf_px_raw_uint8 (+4.33) |
| raw | 512 | hf_px_raw_linear_height (-628.40), sq_raw (-139.49), hf_phys_raw_linear_height (-107.11), centroid_band_power_raw (-69.58), centroid_amp_raw (-66.98), hf_phys_raw_float (-37.88), hf_phys_raw_uint8 (-30.15), centroid_power_raw (-22.52), hf_px_raw_float (-9.99), hf_px_raw_uint8 (-5.02) |
| raw | 1024 | sq_raw (-139.50), hf_phys_raw_linear_height (-107.17), hf_px_raw_linear_height (-107.17), centroid_amp_raw (-73.94), centroid_band_power_raw (-69.60), hf_phys_raw_float (-41.00), hf_px_raw_float (-41.00), hf_phys_raw_uint8 (-32.84), hf_px_raw_uint8 (-32.84), centroid_power_raw (-22.18) |
| raw | 2048 | sq_raw (-139.50), hf_phys_raw_linear_height (-107.16), centroid_amp_raw (-80.87), centroid_band_power_raw (-69.60), hf_phys_raw_float (-41.68), hf_phys_raw_uint8 (-33.24), hf_px_raw_float (-26.18), hf_px_raw_uint8 (-24.35), centroid_power_raw (-21.99), hf_px_raw_linear_height (-17.62) |
| hann | 128 | hf_px_hann_linear_height (-240.79), sq_hann (-137.35), hf_phys_hann_linear_height (-109.88), centroid_amp_hann (-48.78), hf_px_hann_float (+40.19), hf_phys_hann_float (-25.67), centroid_power_hann (-24.20), hf_phys_hann_uint8 (-10.38), hf_px_hann_uint8 (+6.09) |
| hann | 256 | hf_px_hann_linear_height (-679.73), sq_hann (-139.41), hf_phys_hann_linear_height (-107.53), centroid_amp_hann (-56.29), hf_phys_hann_float (-33.53), centroid_power_hann (-23.21), hf_px_hann_float (+14.44), hf_phys_hann_uint8 (-13.99), hf_px_hann_uint8 (+7.85) |
| hann | 512 | hf_px_hann_linear_height (-621.18), sq_hann (-139.46), hf_phys_hann_linear_height (-107.04), centroid_amp_hann (-58.11), hf_phys_hann_float (-41.38), hf_px_hann_float (-27.75), centroid_power_hann (-22.48), hf_phys_hann_uint8 (-17.99), hf_px_hann_uint8 (-3.90) |
| hann | 1024 | sq_hann (-139.49), hf_phys_hann_linear_height (-107.10), hf_px_hann_linear_height (-107.10), centroid_amp_hann (-67.20), hf_phys_hann_float (-43.38), hf_px_hann_float (-43.38), centroid_power_hann (-22.15), hf_phys_hann_uint8 (-19.51), hf_px_hann_uint8 (-19.51) |
| hann | 2048 | sq_hann (-139.50), hf_phys_hann_linear_height (-107.01), centroid_amp_hann (-73.49), hf_phys_hann_float (-42.88), centroid_power_hann (-21.95), hf_px_hann_float (-20.98), hf_phys_hann_uint8 (-19.29), hf_px_hann_linear_height (-17.67), hf_px_hann_uint8 (-13.63) |
| pplus | 128 | sq_pplus (-107.25), hf_phys_pplus_linear_height (-98.52), centroid_amp_pplus (-46.54), hf_px_pplus_float (+43.05), hf_phys_pplus_float (-24.80), centroid_power_pplus (-23.94), hf_phys_pplus_uint8 (-20.94), hf_px_pplus_uint8 (+3.76), hf_px_pplus_linear_height (+1.71) |
| pplus | 256 | hf_px_pplus_linear_height (-313.14), sq_pplus (-123.75), hf_phys_pplus_linear_height (-102.89), centroid_amp_pplus (-49.81), hf_phys_pplus_float (-31.99), hf_phys_pplus_uint8 (-25.68), centroid_power_pplus (-22.91), hf_px_pplus_float (+22.25), hf_px_pplus_uint8 (+4.42) |
| pplus | 512 | hf_px_pplus_linear_height (-611.82), sq_pplus (-132.55), hf_phys_pplus_linear_height (-105.02), centroid_amp_pplus (-59.11), hf_phys_pplus_float (-37.97), hf_phys_pplus_uint8 (-30.18), centroid_power_pplus (-22.41), hf_px_pplus_float (-9.98), hf_px_pplus_uint8 (-4.98) |
| pplus | 1024 | sq_pplus (-136.38), hf_phys_pplus_linear_height (-106.18), hf_px_pplus_linear_height (-106.18), centroid_amp_pplus (-66.94), hf_phys_pplus_float (-41.06), hf_px_pplus_float (-41.06), hf_phys_pplus_uint8 (-32.87), hf_px_pplus_uint8 (-32.87), centroid_power_pplus (-22.13) |
| pplus | 2048 | sq_pplus (-138.04), hf_phys_pplus_linear_height (-106.66), centroid_amp_pplus (-73.06), hf_phys_pplus_float (-41.72), hf_phys_pplus_uint8 (-33.28), hf_px_pplus_float (-26.18), hf_px_pplus_uint8 (-24.36), centroid_power_pplus (-21.96), hf_px_pplus_linear_height (-17.59) |

## C1 and C3: crop range relative to the range over the rule (raw centroid_amp)

| surface | mean C1, N 128 ... 2048 | C1 / C3 (largest C3 over crops), N 128 ... 2048 | |C2| / C3 |
|---|---|---|---|
| V-1.0_A-1.0 | 0.07635, 0.09105, 0.0776, 0.09409, 0.1323 | 0.002611, 0.00153, 0.0006678, 0.0004196, 0.0003069 | 0.327 |
| V-1.0_A-0.5 | 0.3352, 0.397, 0.5746, 0.6412, 0.8127 | 0.01146, 0.00667, 0.004944, 0.002859, 0.001886 | 0.3479 |
| V-1.0_A+0.0 | 0.1035, 0.1764, 0.171, 0.177, 0.197 | 0.003539, 0.002964, 0.001471, 0.0007894, 0.0004572 | 0.71 |
| V-1.0_A+0.5 | 0.2145, 0.2152, 0.2959, 0.2204, 0.2658 | 0.007334, 0.003616, 0.002546, 0.0009829, 0.0006167 | 0.7427 |
| V-1.0_A+1.0 | 0.07509, 0.1589, 0.2496, 0.2457, 0.2511 | 0.002567, 0.00267, 0.002148, 0.001096, 0.0005826 | 0.9631 |
| V-0.5_A-1.0 | 0.06063, 0.06912, 0.06348, 0.06939, 0.09541 | 0.002073, 0.001161, 0.0005463, 0.0003094, 0.0002214 | 0.232 |
| V-0.5_A-0.5 | 0.3052, 0.3667, 0.5198, 0.5729, 0.7247 | 0.01043, 0.006162, 0.004474, 0.002555, 0.001681 | 0.2953 |
| V-0.5_A+0.0 | 0.09679, 0.1598, 0.1533, 0.1617, 0.1886 | 0.003309, 0.002685, 0.001319, 0.000721, 0.0004375 | 0.6439 |
| V-0.5_A+0.5 | 0.2031, 0.2024, 0.273, 0.2128, 0.2643 | 0.006943, 0.003401, 0.002349, 0.0009488, 0.0006131 | 0.6973 |
| V-0.5_A+1.0 | 0.07231, 0.1533, 0.2334, 0.2265, 0.2415 | 0.002472, 0.002575, 0.002008, 0.00101, 0.0005603 | 0.9237 |
| V+0.0_A-1.0 | 0.04102, 0.04334, 0.04209, 0.04068, 0.05321 | 0.001402, 0.0007282, 0.0003622, 0.0001814, 0.0001235 | 0.1311 |
| V+0.0_A-0.5 | 0.2665, 0.3246, 0.4444, 0.4836, 0.6053 | 0.009111, 0.005455, 0.003825, 0.002157, 0.001405 | 0.2359 |
| V+0.0_A+0.0 | 0.08893, 0.1414, 0.1335, 0.1458, 0.176 | 0.003041, 0.002376, 0.001149, 0.0006502, 0.0004085 | 0.5671 |
| V+0.0_A+0.5 | 0.1916, 0.1899, 0.2485, 0.2034, 0.2599 | 0.006551, 0.00319, 0.002138, 0.0009073, 0.0006031 | 0.6451 |
| V+0.0_A+1.0 | 0.06918, 0.1468, 0.2178, 0.2057, 0.2332 | 0.002366, 0.002466, 0.001874, 0.0009176, 0.0005411 | 0.8784 |
| V+0.5_A-1.0 | 0.01256, 0.01192, 0.01166, 0.009902, 0.01194 | 0.0004294, 0.0002003, 0.0001004, 4.416e-05, 2.771e-05 | 0.03095 |
| V+0.5_A-0.5 | 0.2155, 0.2625, 0.3464, 0.3665, 0.4492 | 0.007369, 0.004411, 0.002981, 0.001634, 0.001042 | 0.1691 |
| V+0.5_A+0.0 | 0.08028, 0.1206, 0.1122, 0.1262, 0.1567 | 0.002745, 0.002027, 0.0009657, 0.0005626, 0.0003635 | 0.4781 |
| V+0.5_A+0.5 | 0.1779, 0.1793, 0.2235, 0.1924, 0.2545 | 0.006084, 0.003013, 0.001924, 0.0008581, 0.0005905 | 0.5849 |
| V+0.5_A+1.0 | 0.06581, 0.1396, 0.2018, 0.1839, 0.2295 | 0.00225, 0.002345, 0.001737, 0.0008202, 0.0005324 | 0.826 |
| V+1.0_A-1.0 | 0.01687, 0.0146, 0.01307, 0.00993, 0.01088 | 0.0005768, 0.0002453, 0.0001124, 4.428e-05, 2.525e-05 | 0.03466 |
| V+1.0_A-0.5 | 0.144, 0.1716, 0.215, 0.2177, 0.2569 | 0.004925, 0.002884, 0.001851, 0.0009707, 0.000596 | 0.09512 |
| V+1.0_A+0.0 | 0.06943, 0.09651, 0.08973, 0.1021, 0.1281 | 0.002374, 0.001622, 0.0007721, 0.0004554, 0.0002972 | 0.3758 |
| V+1.0_A+0.5 | 0.1617, 0.1658, 0.1962, 0.1774, 0.2411 | 0.005528, 0.002786, 0.001688, 0.000791, 0.0005595 | 0.5151 |
| V+1.0_A+1.0 | 0.06187, 0.1317, 0.1856, 0.161, 0.2231 | 0.002116, 0.002212, 0.001597, 0.0007178, 0.0005178 | 0.7648 |
| V-1.0_A+0.25 | 1.088, 1.722, 3.107, 5.283, 8.535 | 0.03722, 0.02894, 0.02674, 0.02356, 0.0198 | 0.5907 |
| V-0.5_A+0.25 | 1.257, 2.102, 3.966, 7.148, 12.49 | 0.04299, 0.03532, 0.03413, 0.03188, 0.02897 | 0.5612 |
| V+0.0_A+0.25 | 1.474, 2.613, 5.094, 9.59, 17.72 | 0.0504, 0.0439, 0.04384, 0.04277, 0.04111 | 0.5306 |
| V+0.5_A+0.25 | 1.761, 3.287, 6.595, 12.83, 24.62 | 0.0602, 0.05524, 0.05676, 0.05719, 0.05714 | 0.4997 |
| V+1.0_A+0.25 | 2.158, 4.2, 8.611, 17.22, 33.7 | 0.07379, 0.07057, 0.0741, 0.07677, 0.0782 | 0.4698 |
| sine_periodic | 2.92e-13, 6.45e-13, 1.203e-12, 2.791e-12, 1.284e-11 | 9.985e-15, 1.084e-14, 1.036e-14, 1.245e-14, 2.978e-14 | 2.916e-13 |
| sine_jump | 6.973, 13.7, 26.11, 48.86, 90.54 | 0.2384, 0.2302, 0.2247, 0.2179, 0.2101 | 0.4238 |
| flip_a | 4.228e-13, 1.236e-12, 4.208e-12, 1.016e-11, 2.468e-11 | 1.446e-14, 2.077e-14, 3.621e-14, 4.532e-14, 5.727e-14 | 7.838e-14 |
| flip_b | 1.137e-13, 8.704e-13, 1.968e-12, 4.315e-12, 7.621e-12 | 3.887e-15, 1.463e-14, 1.694e-14, 1.924e-14, 1.768e-14 | 3.668e-14 |

C3 (largest over crops) by N for each descriptor:

| descriptor | C3, N 128 ... 2048 |
|---|---|
| centroid_amp_hann | 27.23, 54.96, 101.5, 196.6, 381.7 |
| centroid_amp_pplus | 25.63, 54.19, 109.6, 216.8, 423.1 |
| centroid_amp_raw | 29.25, 59.51, 116.2, 224.2, 431 |
| centroid_band_power_raw | 6.821, 6.803, 6.802, 6.802, 6.802 |
| centroid_power_hann | 9.911, 10.55, 10.94, 11.17, 11.3 |
| centroid_power_pplus | 9.88, 10.58, 10.97, 11.19, 11.32 |
| centroid_power_raw | 9.88, 10.57, 10.96, 11.19, 11.32 |
| hf_phys_hann_float | 0.2698, 0.3064, 0.3292, 0.3424, 0.3509 |
| hf_phys_hann_linear_height | 0.4316, 0.4314, 0.4314, 0.4314, 0.4314 |
| hf_phys_hann_uint8 | 0.2594, 0.2928, 0.3133, 0.3249, 0.3325 |
| hf_phys_pplus_float | 0.2701, 0.305, 0.3269, 0.3398, 0.3482 |
| hf_phys_pplus_linear_height | 0.4323, 0.4328, 0.4329, 0.433, 0.4329 |
| hf_phys_pplus_uint8 | 0.2643, 0.2995, 0.3214, 0.3342, 0.3431 |
| hf_phys_raw_float | 0.2702, 0.3051, 0.3269, 0.3398, 0.3482 |
| hf_phys_raw_linear_height | 0.4327, 0.4329, 0.4329, 0.4329, 0.4329 |
| hf_phys_raw_uint8 | 0.2643, 0.2996, 0.3214, 0.3342, 0.3431 |
| hf_px_hann_float | 0.05248, 0.08546, 0.2046, 0.3424, 0.4444 |
| hf_px_hann_linear_height | 0.0004527, 0.107, 0.5483, 0.4314, 0.1785 |
| hf_px_hann_uint8 | 0.04755, 0.07436, 0.1693, 0.3249, 0.4249 |
| hf_px_pplus_float | 0.1393, 0.1546, 0.2018, 0.3398, 0.4441 |
| hf_px_pplus_linear_height | 0.00124, 0.09404, 0.5589, 0.433, 0.1782 |
| hf_px_pplus_uint8 | 0.09638, 0.1144, 0.1724, 0.3342, 0.439 |
| hf_px_raw_float | 0.1395, 0.1546, 0.2018, 0.3398, 0.4441 |
| hf_px_raw_linear_height | 2.611e-05, 0.09408, 0.5589, 0.4329, 0.1782 |
| hf_px_raw_uint8 | 0.0967, 0.1144, 0.1724, 0.3342, 0.439 |
| sq_hann | 0.0581, 0.05809, 0.05809, 0.05809, 0.05809 |
| sq_pplus | 0.1543, 0.1545, 0.1547, 0.1548, 0.1549 |
| sq_raw | 0.1549, 0.1549, 0.1549, 0.1549, 0.1549 |

## Ratios for every descriptor (mean over the 25 rule points)

| descriptor | mean C1/C3 at N = 2048 | mean |C2|/C3 |
|---|---|---|
| centroid_amp_hann | 0.0007192 | 0.4985 |
| centroid_amp_pplus | 0.005833 | 0.5057 |
| centroid_amp_raw | 0.0005998 | 0.4886 |
| centroid_band_power_raw | 2.48e-06 | 0.0008035 |
| centroid_power_hann | 1.553e-05 | 0.03049 |
| centroid_power_pplus | 0.000298 | 0.02989 |
| centroid_power_raw | 8.745e-06 | 0.03058 |
| hf_phys_hann_float | 3.93e-05 | 0.3037 |
| hf_phys_hann_linear_height | 3.521e-06 | 0.0002419 |
| hf_phys_hann_uint8 | 0.002496 | 0.3135 |
| hf_phys_pplus_float | 6.256e-05 | 0.2959 |
| hf_phys_pplus_linear_height | 0.0003251 | 0.001067 |
| hf_phys_pplus_uint8 | 0.0001578 | 0.2988 |
| hf_phys_raw_float | 3.453e-05 | 0.2941 |
| hf_phys_raw_linear_height | 2.513e-06 | 0.0002234 |
| hf_phys_raw_uint8 | 0.0001351 | 0.2969 |
| hf_px_hann_float | 3.497e-05 | 1.036 |
| hf_px_hann_linear_height | 7.485e-06 | 5.01 |
| hf_px_hann_uint8 | 0.001205 | 1.014 |
| hf_px_pplus_float | 7.643e-05 | 0.985 |
| hf_px_pplus_linear_height | 0.0004184 | 5.021 |
| hf_px_pplus_uint8 | 0.0001381 | 0.9202 |
| hf_px_raw_float | 5.585e-05 | 0.9849 |
| hf_px_raw_linear_height | 5.433e-06 | 5.023 |
| hf_px_raw_uint8 | 0.0001212 | 0.9209 |
| sq_hann | 1.384e-07 | 2.482e-05 |
| sq_pplus | 0.0003879 | 0.003509 |
| sq_raw | 8.61e-08 | 1.048e-05 |

## Aliasing subset (r = 4, decimate_fourier versus direct sampling)

Mean over seeds and crops of |decimated - direct| / direct, N = 128, 256, 512.

| surface | centroid_amp_raw | hf_px_raw_uint8 | hf_phys_raw_uint8 |
|---|---|---|---|
| V-1.0_A-1.0 | 0.2157, 0.2592, 0.2844 | 0.0001709, 8.55e-05, 0.0002086 | 0.002049, 0.001072, 0.0006429 |
| V-1.0_A-0.5 | 0.05446, 0.06311, 0.06874 | 0.0007648, 0.0004579, 0.0002859 | 0.00509, 0.002052, 0.001015 |
| V-1.0_A+0.0 | 0.2508, 0.295, 0.3311 | 0.0009883, 0.0001758, 0.0003002 | 0.006497, 0.002466, 0.001182 |
| V-1.0_A+0.5 | 0.2076, 0.238, 0.2807 | 0.001488, 0.0002329, 0.0006176 | 0.007337, 0.002913, 0.001371 |
| V-1.0_A+1.0 | 0.209, 0.2785, 0.3327 | 0.00217, 0.0003803, 0.001352 | 0.007003, 0.003337, 0.001828 |
| V-0.5_A-1.0 | 0.198, 0.241, 0.267 | 0.0003573, 0.00013, 8.953e-05 | 0.000962, 0.0005765, 0.000285 |
| V-0.5_A-0.5 | 0.04976, 0.05832, 0.06384 | 0.0005791, 0.0004376, 0.0002173 | 0.003855, 0.001498, 0.0008266 |
| V-0.5_A+0.0 | 0.2488, 0.2934, 0.3301 | 0.001373, 0.0004193, 0.0001371 | 0.005426, 0.002083, 0.001072 |
| V-0.5_A+0.5 | 0.2065, 0.2373, 0.2804 | 0.001086, 0.0004591, 0.0002645 | 0.006533, 0.002403, 0.001252 |
| V-0.5_A+1.0 | 0.2101, 0.2801, 0.3349 | 0.001905, 0.0005376, 0.0005674 | 0.006609, 0.002648, 0.001549 |
| V+0.0_A-1.0 | 0.1631, 0.2043, 0.2318 | 0.001372, 8.718e-05, 4.284e-05 | 0.0005706, 0.0002226, 8.194e-05 |
| V+0.0_A-0.5 | 0.04391, 0.05232, 0.05773 | 0.001156, 0.0002965, 0.0002059 | 0.002793, 0.0009786, 0.0005572 |
| V+0.0_A+0.0 | 0.2449, 0.2899, 0.3272 | 0.0004557, 0.0001332, 0.0001208 | 0.004273, 0.001643, 0.0008931 |
| V+0.0_A+0.5 | 0.2047, 0.2359, 0.2794 | 0.0004915, 0.0002177, 0.0001597 | 0.005696, 0.002151, 0.001135 |
| V+0.0_A+1.0 | 0.2109, 0.2813, 0.3367 | 0.002621, 0.000724, 0.0001217 | 0.006285, 0.002177, 0.001271 |
| V+0.5_A-1.0 | 0.07212, 0.1002, 0.1263 | 0.002803, 5.861e-05, 1.684e-05 | 0.0003074, 0.0001207, 3.547e-05 |
| V+0.5_A-0.5 | 0.0363, 0.04438, 0.04968 | 0.007198, 0.0008613, 0.000229 | 0.002327, 0.0008603, 0.0002847 |
| V+0.5_A+0.0 | 0.2379, 0.2831, 0.321 | 0.001199, 0.0003705, 0.0001243 | 0.002992, 0.001066, 0.0006701 |
| V+0.5_A+0.5 | 0.2018, 0.2334, 0.2771 | 0.0009579, 0.000388, 0.000131 | 0.005088, 0.001825, 0.001005 |
| V+0.5_A+1.0 | 0.2113, 0.282, 0.338 | 0.001174, 0.0002496, 0.0001644 | 0.005806, 0.002143, 0.001123 |
| V+1.0_A-1.0 | 0.09129, 0.1109, 0.1249 | 0.0141, 0.000283, 4.593e-05 | 0.0008359, 0.0002297, 7.875e-05 |
| V+1.0_A-0.5 | 0.02536, 0.03254, 0.0377 | 0.03877, 0.003564, 0.000247 | 0.003028, 0.0008487, 0.0003759 |
| V+1.0_A+0.0 | 0.2253, 0.2704, 0.3088 | 0.009237, 0.002152, 8.701e-05 | 0.001906, 0.0006368, 0.0004322 |
| V+1.0_A+0.5 | 0.1972, 0.2291, 0.2729 | 0.005888, 0.001732, 0.000239 | 0.003861, 0.001653, 0.0008147 |
| V+1.0_A+1.0 | 0.211, 0.2818, 0.3384 | 0.00454, 0.001124, 0.0002729 | 0.005059, 0.001837, 0.001092 |
| V-1.0_A+0.25 | 0.1376, 0.1346, 0.1377 | 0.002041, 0.003752, 0.003048 | 0.005769, 0.003015, 0.001957 |
| V-0.5_A+0.25 | 0.1321, 0.1291, 0.1321 | 0.001683, 0.002943, 0.001737 | 0.008876, 0.005954, 0.004267 |
| V+0.0_A+0.25 | 0.1257, 0.1228, 0.1259 | 0.001243, 0.001298, 0.0002648 | 0.01253, 0.009748, 0.008046 |
| V+0.5_A+0.25 | 0.1182, 0.1158, 0.1192 | 0.001886, 0.0005175, 0.0027 | 0.01619, 0.01443, 0.01448 |
| V+1.0_A+0.25 | 0.1095, 0.1081, 0.1123 | 0.007927, 0.002053, 0.006094 | 0.01888, 0.01867, 0.02332 |
| sine_periodic | 1.719e-14, 3.643e-14, 7.342e-14 | 0, 0, 0 | 0, 0, 0 |
| sine_jump | 0.07578, 0.09016, 0.1012 | 0.001471, 0.003356, 0.03561 | 0.3071, 0.4216, 0.4742 |
| flip_a | 9.681e-15, 5.461e-14, 1.738e-13 | 0, 0, 0 | 0, 0, 0 |
| flip_b | 1.936e-14, 7.403e-14, 2.559e-13 | 0, 0, 0 | 0, 0, 0 |

## Seed and crop means of every descriptor by N

| descriptor | surface | N 128 ... 2048 |
|---|---|---|
| centroid_amp_hann | V-1.0_A-1.0 | 20.42, 31.29, 49.68, 81.1, 134.9 |
| centroid_amp_hann | V-1.0_A-0.5 | 23.57, 36.92, 60.01, 100.9, 173.5 |
| centroid_amp_hann | V-1.0_A+0.0 | 32, 52.91, 91.58, 159.6, 288.9 |
| centroid_amp_hann | V-1.0_A+0.5 | 35.65, 60.84, 106.6, 191.1, 348.8 |
| centroid_amp_hann | V-1.0_A+1.0 | 38.13, 67.34, 116, 214.2, 404 |
| centroid_amp_hann | V-0.5_A-1.0 | 18.17, 26.52, 40.2, 62.79, 100.1 |
| centroid_amp_hann | V-0.5_A-0.5 | 22.41, 34.21, 54.23, 89.02, 149.7 |
| centroid_amp_hann | V-0.5_A+0.0 | 31.04, 50.47, 86, 147.7, 263.6 |
| centroid_amp_hann | V-0.5_A+0.5 | 35.04, 59.12, 102.4, 182, 329 |
| centroid_amp_hann | V-0.5_A+1.0 | 37.69, 66.06, 112.8, 206.9, 388 |
| centroid_amp_hann | V+0.0_A-1.0 | 15.18, 20.47, 28.73, 41.76, 62.2 |
| centroid_amp_hann | V+0.0_A-0.5 | 20.98, 30.91, 47.35, 75.24, 122.6 |
| centroid_amp_hann | V+0.0_A+0.0 | 29.88, 47.56, 79.41, 133.8, 234.5 |
| centroid_amp_hann | V+0.0_A+0.5 | 34.3, 57.09, 97.64, 171.3, 306.2 |
| centroid_amp_hann | V+0.0_A+1.0 | 37.18, 64.58, 109.1, 198.5, 369.8 |
| centroid_amp_hann | V+0.5_A-1.0 | 10.94, 12.4, 14.56, 17.72, 22.34 |
| centroid_amp_hann | V+0.5_A-0.5 | 19.13, 26.77, 39, 59.07, 91.98 |
| centroid_amp_hann | V+0.5_A+0.0 | 28.43, 44.01, 71.53, 117.5, 201 |
| centroid_amp_hann | V+0.5_A+0.5 | 33.42, 54.66, 91.97, 158.9, 279.9 |
| centroid_amp_hann | V+0.5_A+1.0 | 36.59, 62.86, 104.9, 188.9, 348.9 |
| centroid_amp_hann | V+1.0_A-1.0 | 12.49, 14.61, 17.39, 21.05, 25.84 |
| centroid_amp_hann | V+1.0_A-0.5 | 16.64, 21.37, 28.61, 39.95, 57.62 |
| centroid_amp_hann | V+1.0_A+0.0 | 26.58, 39.59, 61.99, 98.41, 162.7 |
| centroid_amp_hann | V+1.0_A+0.5 | 32.33, 51.71, 85.2, 144.3, 249.4 |
| centroid_amp_hann | V+1.0_A+1.0 | 35.88, 60.81, 99.92, 177.7, 324.8 |
| centroid_amp_hann | V-1.0_A+0.25 | 33.56, 56.82, 91.52, 157.7, 310.9 |
| centroid_amp_hann | V-0.5_A+0.25 | 32.77, 54.74, 86.91, 147.6, 288.5 |
| centroid_amp_hann | V+0.0_A+0.25 | 31.81, 52.27, 81.56, 136.1, 262.8 |
| centroid_amp_hann | V+0.5_A+0.25 | 30.65, 49.3, 75.29, 122.9, 233.3 |
| centroid_amp_hann | V+1.0_A+0.25 | 29.2, 45.65, 67.86, 107.6, 199.6 |
| centroid_amp_hann | sine_periodic | 7.106, 7.106, 7.106, 7.106, 7.106 |
| centroid_amp_hann | sine_jump | 7.876, 7.88, 7.881, 7.882, 7.883 |
| centroid_amp_hann | flip_a | 16.03, 16.03, 16.03, 16.03, 16.03 |
| centroid_amp_hann | flip_b | 8.031, 8.031, 8.031, 8.031, 8.031 |
| centroid_amp_pplus | V-1.0_A-1.0 | 23.77, 37.5, 60.59, 99.88, 167.1 |
| centroid_amp_pplus | V-1.0_A-0.5 | 25.21, 39.58, 63.92, 106.3, 181.1 |
| centroid_amp_pplus | V-1.0_A+0.0 | 34.65, 59.67, 105, 188.3, 341.9 |
| centroid_amp_pplus | V-1.0_A+0.5 | 36.04, 62.11, 109.4, 196.7, 359.2 |
| centroid_amp_pplus | V-1.0_A+1.0 | 39.97, 71.84, 131, 242.7, 454.9 |
| centroid_amp_pplus | V-0.5_A-1.0 | 21.42, 32.22, 49.57, 77.86, 124.3 |
| centroid_amp_pplus | V-0.5_A-0.5 | 24.24, 37.15, 58.48, 94.8, 157.5 |
| centroid_amp_pplus | V-0.5_A+0.0 | 33.71, 57.13, 98.99, 174.8, 312.8 |
| centroid_amp_pplus | V-0.5_A+0.5 | 35.5, 60.5, 105.4, 187.6, 339.4 |
| centroid_amp_pplus | V-0.5_A+1.0 | 39.57, 70.57, 127.7, 235, 437.8 |
| centroid_amp_pplus | V+0.0_A-1.0 | 18.42, 25.73, 36.59, 53.07, 78.49 |
| centroid_amp_pplus | V+0.0_A-0.5 | 23.07, 34.23, 52.05, 81.47, 130.7 |
| centroid_amp_pplus | V+0.0_A+0.0 | 32.57, 54.07, 91.8, 158.9, 279.1 |
| centroid_amp_pplus | V+0.0_A+0.5 | 34.86, 58.62, 100.8, 177.1, 316.6 |
| centroid_amp_pplus | V+0.0_A+1.0 | 39.11, 69.1, 123.9, 226.2, 418 |
| centroid_amp_pplus | V+0.5_A-1.0 | 14.57, 17.76, 21.51, 26.13, 32.22 |
| centroid_amp_pplus | V+0.5_A-0.5 | 21.59, 30.64, 44.36, 65.94, 100.5 |
| centroid_amp_pplus | V+0.5_A+0.0 | 31.16, 50.35, 83.19, 140.2, 240 |
| centroid_amp_pplus | V+0.5_A+0.5 | 34.08, 56.37, 95.33, 164.9, 290.3 |
| centroid_amp_pplus | V+0.5_A+1.0 | 38.56, 67.37, 119.5, 215.9, 395.1 |
| centroid_amp_pplus | V+1.0_A-1.0 | 15.79, 19.6, 23.98, 29.09, 35.24 |
| centroid_amp_pplus | V+1.0_A-0.5 | 19.67, 26.12, 35.01, 47.85, 66.95 |
| centroid_amp_pplus | V+1.0_A+0.0 | 29.37, 45.74, 72.79, 118.2, 195.1 |
| centroid_amp_pplus | V+1.0_A+0.5 | 33.14, 53.67, 88.87, 150.6, 259.8 |
| centroid_amp_pplus | V+1.0_A+1.0 | 37.91, 65.32, 114.3, 203.8, 368.5 |
| centroid_amp_pplus | V-1.0_A+0.25 | 28.95, 49.45, 84.18, 148.8, 272.8 |
| centroid_amp_pplus | V-0.5_A+0.25 | 28.05, 47.35, 79.72, 139.3, 252.5 |
| centroid_amp_pplus | V+0.0_A+0.25 | 26.98, 44.91, 74.57, 128.3, 229.5 |
| centroid_amp_pplus | V+0.5_A+0.25 | 25.72, 42.03, 68.57, 115.8, 203.4 |
| centroid_amp_pplus | V+1.0_A+0.25 | 24.19, 38.57, 61.49, 101.3, 173.6 |
| centroid_amp_pplus | sine_periodic | 10.86, 12.05, 12.95, 13.56, 13.95 |
| centroid_amp_pplus | sine_jump | 10.25, 11.36, 12.68, 14.2, 15.89 |
| centroid_amp_pplus | flip_a | 15.77, 19.05, 21.63, 23.69, 25.09 |
| centroid_amp_pplus | flip_b | 9.671, 11.07, 12.13, 12.82, 13.25 |
| centroid_amp_raw | V-1.0_A-1.0 | 23.09, 36.33, 58.88, 97.54, 164 |
| centroid_amp_raw | V-1.0_A-0.5 | 23.55, 36.9, 60, 100.9, 173.5 |
| centroid_amp_raw | V-1.0_A+0.0 | 34.84, 59.76, 104.9, 187.8, 340.8 |
| centroid_amp_raw | V-1.0_A+0.5 | 36.01, 61.68, 108.4, 194.8, 356.1 |
| centroid_amp_raw | V-1.0_A+1.0 | 40.59, 72.57, 131.8, 243.5, 455.6 |
| centroid_amp_raw | V-0.5_A-1.0 | 20.35, 30.47, 47.13, 74.68, 120.3 |
| centroid_amp_raw | V-0.5_A-0.5 | 22.39, 34.19, 54.22, 89.01, 149.7 |
| centroid_amp_raw | V-0.5_A+0.0 | 33.81, 57.04, 98.62, 173.9, 311.3 |
| centroid_amp_raw | V-0.5_A+0.5 | 35.39, 59.94, 104.2, 185.5, 335.9 |
| centroid_amp_raw | V-0.5_A+1.0 | 40.16, 71.24, 128.4, 235.7, 438.2 |
| centroid_amp_raw | V+0.0_A-1.0 | 16.65, 22.99, 32.93, 48.56, 73.14 |
| centroid_amp_raw | V+0.0_A-0.5 | 20.96, 30.89, 47.33, 75.22, 122.6 |
| centroid_amp_raw | V+0.0_A+0.0 | 32.53, 53.72, 91.05, 157.6, 276.9 |
| centroid_amp_raw | V+0.0_A+0.5 | 34.65, 57.88, 99.3, 174.6, 312.6 |
| centroid_amp_raw | V+0.0_A+1.0 | 39.65, 69.69, 124.5, 226.6, 418.2 |
| centroid_amp_raw | V+0.5_A-1.0 | 11.35, 13.08, 15.61, 19.3, 24.69 |
| centroid_amp_raw | V+0.5_A-0.5 | 19.11, 26.75, 38.98, 59.05, 91.96 |
| centroid_amp_raw | V+0.5_A+0.0 | 30.91, 49.62, 81.88, 138.1, 236.9 |
| centroid_amp_raw | V+0.5_A+0.5 | 33.75, 55.42, 93.54, 162, 285.8 |
| centroid_amp_raw | V+0.5_A+1.0 | 39.05, 67.85, 119.9, 216.1, 395 |
| centroid_amp_raw | V+1.0_A-1.0 | 13.09, 15.48, 18.6, 22.69, 28.03 |
| centroid_amp_raw | V+1.0_A-0.5 | 16.61, 21.35, 28.58, 39.92, 57.6 |
| centroid_amp_raw | V+1.0_A+0.0 | 28.79, 44.44, 70.64, 115.1, 190.7 |
| centroid_amp_raw | V+1.0_A+0.5 | 32.65, 52.43, 86.65, 147.1, 254.6 |
| centroid_amp_raw | V+1.0_A+1.0 | 38.32, 65.64, 114.5, 203.7, 367.9 |
| centroid_amp_raw | V-1.0_A+0.25 | 29.7, 50.81, 87.56, 155.7, 284.3 |
| centroid_amp_raw | V-0.5_A+0.25 | 29, 49.27, 84.46, 149.2, 270.8 |
| centroid_amp_raw | V+0.0_A+0.25 | 28.21, 47.55, 81.07, 142.4, 256.9 |
| centroid_amp_raw | V+0.5_A+0.25 | 27.31, 45.64, 77.4, 135.2, 242.6 |
| centroid_amp_raw | V+1.0_A+0.25 | 26.27, 43.5, 73.46, 127.9, 228.7 |
| centroid_amp_raw | sine_periodic | 7.071, 7.071, 7.071, 7.071, 7.071 |
| centroid_amp_raw | sine_jump | 20.39, 34.21, 60.37, 109.8, 203 |
| centroid_amp_raw | flip_a | 15.93, 15.93, 15.93, 15.93, 15.93 |
| centroid_amp_raw | flip_b | 8, 8, 8, 8, 8 |
| centroid_band_power_raw | V-1.0_A-1.0 | 5.782, 5.781, 5.781, 5.781, 5.781 |
| centroid_band_power_raw | V-1.0_A-0.5 | 7.784, 7.782, 7.781, 7.781, 7.781 |
| centroid_band_power_raw | V-1.0_A+0.0 | 9.734, 9.729, 9.728, 9.728, 9.728 |
| centroid_band_power_raw | V-1.0_A+0.5 | 10.66, 10.64, 10.64, 10.64, 10.64 |
| centroid_band_power_raw | V-1.0_A+1.0 | 12.47, 12.46, 12.46, 12.46, 12.46 |
| centroid_band_power_raw | V-0.5_A-1.0 | 5.719, 5.719, 5.719, 5.719, 5.719 |
| centroid_band_power_raw | V-0.5_A-0.5 | 7.714, 7.713, 7.713, 7.713, 7.713 |
| centroid_band_power_raw | V-0.5_A+0.0 | 9.675, 9.671, 9.671, 9.671, 9.671 |
| centroid_band_power_raw | V-0.5_A+0.5 | 10.6, 10.59, 10.59, 10.59, 10.59 |
| centroid_band_power_raw | V-0.5_A+1.0 | 12.42, 12.4, 12.4, 12.4, 12.4 |
| centroid_band_power_raw | V+0.0_A-1.0 | 5.672, 5.672, 5.672, 5.672, 5.672 |
| centroid_band_power_raw | V+0.0_A-0.5 | 7.648, 7.647, 7.647, 7.647, 7.647 |
| centroid_band_power_raw | V+0.0_A+0.0 | 9.615, 9.612, 9.612, 9.612, 9.612 |
| centroid_band_power_raw | V+0.0_A+0.5 | 10.54, 10.53, 10.53, 10.53, 10.53 |
| centroid_band_power_raw | V+0.0_A+1.0 | 12.36, 12.35, 12.35, 12.35, 12.35 |
| centroid_band_power_raw | V+0.5_A-1.0 | 5.653, 5.653, 5.653, 5.653, 5.653 |
| centroid_band_power_raw | V+0.5_A-0.5 | 7.589, 7.589, 7.589, 7.589, 7.589 |
| centroid_band_power_raw | V+0.5_A+0.0 | 9.555, 9.553, 9.553, 9.553, 9.553 |
| centroid_band_power_raw | V+0.5_A+0.5 | 10.47, 10.47, 10.47, 10.47, 10.47 |
| centroid_band_power_raw | V+0.5_A+1.0 | 12.3, 12.29, 12.29, 12.29, 12.29 |
| centroid_band_power_raw | V+1.0_A-1.0 | 5.687, 5.687, 5.687, 5.687, 5.687 |
| centroid_band_power_raw | V+1.0_A-0.5 | 7.547, 7.547, 7.547, 7.547, 7.547 |
| centroid_band_power_raw | V+1.0_A+0.0 | 9.498, 9.497, 9.497, 9.497, 9.497 |
| centroid_band_power_raw | V+1.0_A+0.5 | 10.41, 10.4, 10.4, 10.4, 10.4 |
| centroid_band_power_raw | V+1.0_A+1.0 | 12.24, 12.23, 12.23, 12.23, 12.23 |
| centroid_band_power_raw | V-1.0_A+0.25 | 11.07, 11.05, 11.05, 11.05, 11.05 |
| centroid_band_power_raw | V-0.5_A+0.25 | 11.02, 11, 11, 11, 11 |
| centroid_band_power_raw | V+0.0_A+0.25 | 10.97, 10.95, 10.95, 10.95, 10.95 |
| centroid_band_power_raw | V+0.5_A+0.25 | 10.92, 10.91, 10.9, 10.9, 10.9 |
| centroid_band_power_raw | V+1.0_A+0.25 | 10.87, 10.86, 10.85, 10.85, 10.85 |
| centroid_band_power_raw | sine_periodic | 7.071, 7.071, 7.071, 7.071, 7.071 |
| centroid_band_power_raw | sine_jump | 8.28, 8.259, 8.254, 8.253, 8.253 |
| centroid_band_power_raw | flip_a | 2, 2, 2, 2, 2 |
| centroid_band_power_raw | flip_b | 8, 8, 8, 8, 8 |
| centroid_power_hann | V-1.0_A-1.0 | 6.21, 6.222, 6.227, 6.229, 6.229 |
| centroid_power_hann | V-1.0_A-0.5 | 8.529, 8.59, 8.616, 8.629, 8.635 |
| centroid_power_hann | V-1.0_A+0.0 | 10.96, 11.14, 11.22, 11.27, 11.29 |
| centroid_power_hann | V-1.0_A+0.5 | 13.42, 13.81, 14.02, 14.13, 14.19 |
| centroid_power_hann | V-1.0_A+1.0 | 15.89, 16.57, 16.96, 17.19, 17.32 |
| centroid_power_hann | V-0.5_A-1.0 | 6.112, 6.117, 6.119, 6.12, 6.12 |
| centroid_power_hann | V-0.5_A-0.5 | 8.373, 8.411, 8.427, 8.434, 8.436 |
| centroid_power_hann | V-0.5_A+0.0 | 10.77, 10.9, 10.96, 10.99, 11.01 |
| centroid_power_hann | V-0.5_A+0.5 | 13.22, 13.54, 13.71, 13.79, 13.84 |
| centroid_power_hann | V-0.5_A+1.0 | 15.69, 16.28, 16.61, 16.79, 16.9 |
| centroid_power_hann | V+0.0_A-1.0 | 6.043, 6.044, 6.044, 6.045, 6.045 |
| centroid_power_hann | V+0.0_A-0.5 | 8.23, 8.251, 8.258, 8.261, 8.263 |
| centroid_power_hann | V+0.0_A+0.0 | 10.58, 10.68, 10.72, 10.74, 10.74 |
| centroid_power_hann | V+0.0_A+0.5 | 13.02, 13.27, 13.4, 13.46, 13.49 |
| centroid_power_hann | V+0.0_A+1.0 | 15.48, 15.99, 16.26, 16.4, 16.48 |
| centroid_power_hann | V+0.5_A-1.0 | 6.018, 6.018, 6.018, 6.018, 6.018 |
| centroid_power_hann | V+0.5_A-0.5 | 8.109, 8.118, 8.121, 8.122, 8.123 |
| centroid_power_hann | V+0.5_A+0.0 | 10.4, 10.46, 10.49, 10.5, 10.5 |
| centroid_power_hann | V+0.5_A+0.5 | 12.81, 13.01, 13.09, 13.13, 13.15 |
| centroid_power_hann | V+0.5_A+1.0 | 15.27, 15.69, 15.9, 16.01, 16.07 |
| centroid_power_hann | V+1.0_A-1.0 | 6.064, 6.064, 6.064, 6.064, 6.064 |
| centroid_power_hann | V+1.0_A-0.5 | 8.027, 8.029, 8.03, 8.03, 8.03 |
| centroid_power_hann | V+1.0_A+0.0 | 10.24, 10.27, 10.28, 10.29, 10.29 |
| centroid_power_hann | V+1.0_A+0.5 | 12.61, 12.74, 12.8, 12.83, 12.84 |
| centroid_power_hann | V+1.0_A+1.0 | 15.05, 15.39, 15.55, 15.63, 15.67 |
| centroid_power_hann | V-1.0_A+0.25 | 12.19, 12.46, 12.6, 12.67, 12.71 |
| centroid_power_hann | V-0.5_A+0.25 | 12, 12.21, 12.31, 12.37, 12.39 |
| centroid_power_hann | V+0.0_A+0.25 | 11.8, 11.96, 12.03, 12.07, 12.08 |
| centroid_power_hann | V+0.5_A+0.25 | 11.6, 11.71, 11.76, 11.78, 11.79 |
| centroid_power_hann | V+1.0_A+0.25 | 11.41, 11.48, 11.51, 11.52, 11.53 |
| centroid_power_hann | sine_periodic | 7.095, 7.095, 7.095, 7.095, 7.095 |
| centroid_power_hann | sine_jump | 7.8, 7.8, 7.8, 7.8, 7.8 |
| centroid_power_hann | flip_a | 7.343, 7.343, 7.343, 7.343, 7.343 |
| centroid_power_hann | flip_b | 8.021, 8.021, 8.021, 8.021, 8.021 |
| centroid_power_pplus | V-1.0_A-1.0 | 6.186, 6.192, 6.194, 6.195, 6.196 |
| centroid_power_pplus | V-1.0_A-0.5 | 8.521, 8.573, 8.594, 8.605, 8.61 |
| centroid_power_pplus | V-1.0_A+0.0 | 10.95, 11.12, 11.21, 11.25, 11.27 |
| centroid_power_pplus | V-1.0_A+0.5 | 13.42, 13.81, 14.01, 14.12, 14.18 |
| centroid_power_pplus | V-1.0_A+1.0 | 15.86, 16.56, 16.95, 17.17, 17.31 |
| centroid_power_pplus | V-0.5_A-1.0 | 6.088, 6.087, 6.087, 6.086, 6.086 |
| centroid_power_pplus | V-0.5_A-0.5 | 8.365, 8.394, 8.404, 8.409, 8.412 |
| centroid_power_pplus | V-0.5_A+0.0 | 10.76, 10.89, 10.95, 10.98, 10.99 |
| centroid_power_pplus | V-0.5_A+0.5 | 13.23, 13.54, 13.69, 13.78, 13.82 |
| centroid_power_pplus | V-0.5_A+1.0 | 15.66, 16.28, 16.6, 16.78, 16.89 |
| centroid_power_pplus | V+0.0_A-1.0 | 6.019, 6.014, 6.012, 6.011, 6.011 |
| centroid_power_pplus | V+0.0_A-0.5 | 8.221, 8.233, 8.236, 8.237, 8.238 |
| centroid_power_pplus | V+0.0_A+0.0 | 10.57, 10.66, 10.7, 10.72, 10.72 |
| centroid_power_pplus | V+0.0_A+0.5 | 13.02, 13.27, 13.38, 13.44, 13.47 |
| centroid_power_pplus | V+0.0_A+1.0 | 15.46, 15.98, 16.25, 16.39, 16.47 |
| centroid_power_pplus | V+0.5_A-1.0 | 5.994, 5.988, 5.985, 5.984, 5.984 |
| centroid_power_pplus | V+0.5_A-0.5 | 8.101, 8.1, 8.098, 8.098, 8.098 |
| centroid_power_pplus | V+0.5_A+0.0 | 10.4, 10.45, 10.47, 10.48, 10.48 |
| centroid_power_pplus | V+0.5_A+0.5 | 12.82, 13, 13.08, 13.12, 13.14 |
| centroid_power_pplus | V+0.5_A+1.0 | 15.25, 15.68, 15.89, 16, 16.06 |
| centroid_power_pplus | V+1.0_A-1.0 | 6.04, 6.034, 6.032, 6.031, 6.031 |
| centroid_power_pplus | V+1.0_A-0.5 | 8.018, 8.011, 8.007, 8.005, 8.005 |
| centroid_power_pplus | V+1.0_A+0.0 | 10.23, 10.26, 10.26, 10.27, 10.27 |
| centroid_power_pplus | V+1.0_A+0.5 | 12.61, 12.74, 12.79, 12.81, 12.82 |
| centroid_power_pplus | V+1.0_A+1.0 | 15.04, 15.38, 15.54, 15.62, 15.66 |
| centroid_power_pplus | V-1.0_A+0.25 | 12.19, 12.49, 12.64, 12.72, 12.77 |
| centroid_power_pplus | V-0.5_A+0.25 | 11.99, 12.23, 12.35, 12.41, 12.44 |
| centroid_power_pplus | V+0.0_A+0.25 | 11.79, 11.97, 12.06, 12.1, 12.12 |
| centroid_power_pplus | V+0.5_A+0.25 | 11.59, 11.72, 11.78, 11.8, 11.82 |
| centroid_power_pplus | V+1.0_A+0.25 | 11.39, 11.48, 11.52, 11.54, 11.54 |
| centroid_power_pplus | sine_periodic | 7.081, 7.075, 7.072, 7.071, 7.071 |
| centroid_power_pplus | sine_jump | 7.619, 7.618, 7.619, 7.619, 7.619 |
| centroid_power_pplus | flip_a | 6.933, 7.209, 7.291, 7.292, 7.282 |
| centroid_power_pplus | flip_b | 7.939, 7.986, 7.997, 7.999, 8 |
| centroid_power_raw | V-1.0_A-1.0 | 6.177, 6.188, 6.193, 6.195, 6.196 |
| centroid_power_raw | V-1.0_A-0.5 | 8.504, 8.565, 8.591, 8.604, 8.61 |
| centroid_power_raw | V-1.0_A+0.0 | 10.94, 11.12, 11.2, 11.25, 11.27 |
| centroid_power_raw | V-1.0_A+0.5 | 13.41, 13.8, 14, 14.11, 14.18 |
| centroid_power_raw | V-1.0_A+1.0 | 15.86, 16.56, 16.95, 17.17, 17.31 |
| centroid_power_raw | V-0.5_A-1.0 | 6.078, 6.084, 6.085, 6.086, 6.086 |
| centroid_power_raw | V-0.5_A-0.5 | 8.348, 8.386, 8.402, 8.408, 8.411 |
| centroid_power_raw | V-0.5_A+0.0 | 10.75, 10.88, 10.94, 10.98, 10.99 |
| centroid_power_raw | V-0.5_A+0.5 | 13.21, 13.53, 13.69, 13.77, 13.82 |
| centroid_power_raw | V-0.5_A+1.0 | 15.67, 16.27, 16.6, 16.78, 16.89 |
| centroid_power_raw | V+0.0_A-1.0 | 6.009, 6.01, 6.011, 6.011, 6.011 |
| centroid_power_raw | V+0.0_A-0.5 | 8.205, 8.226, 8.233, 8.236, 8.237 |
| centroid_power_raw | V+0.0_A+0.0 | 10.56, 10.65, 10.7, 10.72, 10.72 |
| centroid_power_raw | V+0.0_A+0.5 | 13, 13.26, 13.38, 13.44, 13.47 |
| centroid_power_raw | V+0.0_A+1.0 | 15.46, 15.98, 16.24, 16.39, 16.47 |
| centroid_power_raw | V+0.5_A-1.0 | 5.984, 5.984, 5.984, 5.984, 5.984 |
| centroid_power_raw | V+0.5_A-0.5 | 8.084, 8.093, 8.096, 8.097, 8.097 |
| centroid_power_raw | V+0.5_A+0.0 | 10.38, 10.44, 10.47, 10.48, 10.48 |
| centroid_power_raw | V+0.5_A+0.5 | 12.8, 12.99, 13.08, 13.12, 13.14 |
| centroid_power_raw | V+0.5_A+1.0 | 15.25, 15.68, 15.89, 16, 16.06 |
| centroid_power_raw | V+1.0_A-1.0 | 6.03, 6.03, 6.03, 6.03, 6.03 |
| centroid_power_raw | V+1.0_A-0.5 | 8.002, 8.004, 8.004, 8.005, 8.005 |
| centroid_power_raw | V+1.0_A+0.0 | 10.22, 10.25, 10.26, 10.27, 10.27 |
| centroid_power_raw | V+1.0_A+0.5 | 12.59, 12.73, 12.79, 12.81, 12.82 |
| centroid_power_raw | V+1.0_A+1.0 | 15.03, 15.38, 15.54, 15.62, 15.65 |
| centroid_power_raw | V-1.0_A+0.25 | 12.84, 13.34, 13.71, 14.01, 14.28 |
| centroid_power_raw | V-0.5_A+0.25 | 12.65, 13.1, 13.43, 13.71, 13.97 |
| centroid_power_raw | V+0.0_A+0.25 | 12.46, 12.85, 13.16, 13.42, 13.67 |
| centroid_power_raw | V+0.5_A+0.25 | 12.27, 12.61, 12.9, 13.15, 13.39 |
| centroid_power_raw | V+1.0_A+0.25 | 12.08, 12.39, 12.65, 12.9, 13.14 |
| centroid_power_raw | sine_periodic | 7.071, 7.071, 7.071, 7.071, 7.071 |
| centroid_power_raw | sine_jump | 8.721, 9.031, 9.342, 9.653, 9.963 |
| centroid_power_raw | flip_a | 7.266, 7.266, 7.266, 7.266, 7.266 |
| centroid_power_raw | flip_b | 8, 8, 8, 8, 8 |
| hf_phys_hann_float | V-1.0_A-1.0 | 0.5004, 0.5544, 0.5747, 0.5837, 0.5878 |
| hf_phys_hann_float | V-1.0_A-0.5 | 0.5823, 0.6534, 0.6795, 0.6893, 0.692 |
| hf_phys_hann_float | V-1.0_A+0.0 | 0.6393, 0.7137, 0.7402, 0.7488, 0.7502 |
| hf_phys_hann_float | V-1.0_A+0.5 | 0.6822, 0.7508, 0.7759, 0.7844, 0.7857 |
| hf_phys_hann_float | V-1.0_A+1.0 | 0.7154, 0.7731, 0.7968, 0.8061, 0.8084 |
| hf_phys_hann_float | V-0.5_A-1.0 | 0.4901, 0.5398, 0.5566, 0.5634, 0.5666 |
| hf_phys_hann_float | V-0.5_A-0.5 | 0.5773, 0.6484, 0.6744, 0.6854, 0.6899 |
| hf_phys_hann_float | V-0.5_A+0.0 | 0.6408, 0.7189, 0.7474, 0.7581, 0.7611 |
| hf_phys_hann_float | V-0.5_A+0.5 | 0.6898, 0.7634, 0.7904, 0.8002, 0.8023 |
| hf_phys_hann_float | V-0.5_A+1.0 | 0.7282, 0.7906, 0.8151, 0.8248, 0.8274 |
| hf_phys_hann_float | V+0.0_A-1.0 | 0.4815, 0.5272, 0.5403, 0.5445, 0.5461 |
| hf_phys_hann_float | V+0.0_A-0.5 | 0.5701, 0.6395, 0.6636, 0.6738, 0.6788 |
| hf_phys_hann_float | V+0.0_A+0.0 | 0.6394, 0.72, 0.75, 0.7626, 0.7679 |
| hf_phys_hann_float | V+0.0_A+0.5 | 0.6946, 0.7736, 0.8034, 0.8151, 0.819 |
| hf_phys_hann_float | V+0.0_A+1.0 | 0.7389, 0.8077, 0.8343, 0.845, 0.8484 |
| hf_phys_hann_float | V+0.5_A-1.0 | 0.4782, 0.5218, 0.533, 0.5359, 0.5367 |
| hf_phys_hann_float | V+0.5_A-0.5 | 0.5621, 0.6286, 0.6494, 0.6571, 0.6606 |
| hf_phys_hann_float | V+0.5_A+0.0 | 0.6351, 0.7163, 0.7459, 0.759, 0.7658 |
| hf_phys_hann_float | V+0.5_A+0.5 | 0.6958, 0.7791, 0.8115, 0.8258, 0.8325 |
| hf_phys_hann_float | V+0.5_A+1.0 | 0.7458, 0.8214, 0.8518, 0.8648, 0.8702 |
| hf_phys_hann_float | V+1.0_A-1.0 | 0.4845, 0.5288, 0.5405, 0.5435, 0.5443 |
| hf_phys_hann_float | V+1.0_A-0.5 | 0.5555, 0.6192, 0.637, 0.6422, 0.6439 |
| hf_phys_hann_float | V+1.0_A+0.0 | 0.6286, 0.7084, 0.7356, 0.7467, 0.7525 |
| hf_phys_hann_float | V+1.0_A+0.5 | 0.6932, 0.7782, 0.8114, 0.8268, 0.8359 |
| hf_phys_hann_float | V+1.0_A+1.0 | 0.7477, 0.8281, 0.8622, 0.8784, 0.8876 |
| hf_phys_hann_float | V-1.0_A+0.25 | 0.6623, 0.7346, 0.7604, 0.7688, 0.77 |
| hf_phys_hann_float | V-0.5_A+0.25 | 0.667, 0.7439, 0.7719, 0.782, 0.7844 |
| hf_phys_hann_float | V+0.0_A+0.25 | 0.6688, 0.7498, 0.7802, 0.7926, 0.7971 |
| hf_phys_hann_float | V+0.5_A+0.25 | 0.6672, 0.7507, 0.7825, 0.7967, 0.8038 |
| hf_phys_hann_float | V+1.0_A+0.25 | 0.6624, 0.7461, 0.7769, 0.7907, 0.7985 |
| hf_phys_hann_float | sine_periodic | 0.147, 0.147, 0.147, 0.147, 0.147 |
| hf_phys_hann_float | sine_jump | 0.1948, 0.1948, 0.1948, 0.1948, 0.1948 |
| hf_phys_hann_float | flip_a | 0.2882, 0.9763, 0.9868, 0.9885, 0.9888 |
| hf_phys_hann_float | flip_b | 0.2116, 0.2116, 0.2116, 0.2116, 0.2116 |
| hf_phys_hann_linear_height | V-1.0_A-1.0 | 0.1288, 0.1288, 0.1288, 0.1288, 0.1288 |
| hf_phys_hann_linear_height | V-1.0_A-0.5 | 0.225, 0.225, 0.225, 0.225, 0.225 |
| hf_phys_hann_linear_height | V-1.0_A+0.0 | 0.3335, 0.3335, 0.3335, 0.3335, 0.3335 |
| hf_phys_hann_linear_height | V-1.0_A+0.5 | 0.4442, 0.4444, 0.4444, 0.4444, 0.4444 |
| hf_phys_hann_linear_height | V-1.0_A+1.0 | 0.5516, 0.5518, 0.5518, 0.5518, 0.5518 |
| hf_phys_hann_linear_height | V-0.5_A-1.0 | 0.1246, 0.1246, 0.1246, 0.1246, 0.1246 |
| hf_phys_hann_linear_height | V-0.5_A-0.5 | 0.2195, 0.2195, 0.2195, 0.2195, 0.2195 |
| hf_phys_hann_linear_height | V-0.5_A+0.0 | 0.3281, 0.3282, 0.3282, 0.3282, 0.3282 |
| hf_phys_hann_linear_height | V-0.5_A+0.5 | 0.4397, 0.4398, 0.4398, 0.4398, 0.4398 |
| hf_phys_hann_linear_height | V-0.5_A+1.0 | 0.5481, 0.5482, 0.5482, 0.5482, 0.5482 |
| hf_phys_hann_linear_height | V+0.0_A-1.0 | 0.1215, 0.1215, 0.1215, 0.1215, 0.1215 |
| hf_phys_hann_linear_height | V+0.0_A-0.5 | 0.2143, 0.2143, 0.2143, 0.2143, 0.2143 |
| hf_phys_hann_linear_height | V+0.0_A+0.0 | 0.3227, 0.3227, 0.3227, 0.3227, 0.3227 |
| hf_phys_hann_linear_height | V+0.0_A+0.5 | 0.4349, 0.4351, 0.4351, 0.4351, 0.4351 |
| hf_phys_hann_linear_height | V+0.0_A+1.0 | 0.5443, 0.5445, 0.5445, 0.5445, 0.5445 |
| hf_phys_hann_linear_height | V+0.5_A-1.0 | 0.1204, 0.1204, 0.1204, 0.1204, 0.1204 |
| hf_phys_hann_linear_height | V+0.5_A-0.5 | 0.2098, 0.2098, 0.2098, 0.2098, 0.2098 |
| hf_phys_hann_linear_height | V+0.5_A+0.0 | 0.3174, 0.3174, 0.3174, 0.3174, 0.3174 |
| hf_phys_hann_linear_height | V+0.5_A+0.5 | 0.4301, 0.4302, 0.4302, 0.4302, 0.4302 |
| hf_phys_hann_linear_height | V+0.5_A+1.0 | 0.5404, 0.5405, 0.5405, 0.5405, 0.5405 |
| hf_phys_hann_linear_height | V+1.0_A-1.0 | 0.1228, 0.1228, 0.1228, 0.1228, 0.1228 |
| hf_phys_hann_linear_height | V+1.0_A-0.5 | 0.2067, 0.2067, 0.2067, 0.2067, 0.2067 |
| hf_phys_hann_linear_height | V+1.0_A+0.0 | 0.3124, 0.3124, 0.3124, 0.3124, 0.3124 |
| hf_phys_hann_linear_height | V+1.0_A+0.5 | 0.4252, 0.4253, 0.4253, 0.4253, 0.4253 |
| hf_phys_hann_linear_height | V+1.0_A+1.0 | 0.5364, 0.5365, 0.5365, 0.5365, 0.5365 |
| hf_phys_hann_linear_height | V-1.0_A+0.25 | 0.3891, 0.3891, 0.3891, 0.3891, 0.3891 |
| hf_phys_hann_linear_height | V-0.5_A+0.25 | 0.3841, 0.3841, 0.3841, 0.3841, 0.3841 |
| hf_phys_hann_linear_height | V+0.0_A+0.25 | 0.3789, 0.3789, 0.379, 0.379, 0.379 |
| hf_phys_hann_linear_height | V+0.5_A+0.25 | 0.3737, 0.3737, 0.3737, 0.3738, 0.3738 |
| hf_phys_hann_linear_height | V+1.0_A+0.25 | 0.3687, 0.3687, 0.3687, 0.3687, 0.3687 |
| hf_phys_hann_linear_height | sine_periodic | 0.1473, 0.1473, 0.1473, 0.1473, 0.1473 |
| hf_phys_hann_linear_height | sine_jump | 0.1953, 0.1953, 0.1953, 0.1953, 0.1953 |
| hf_phys_hann_linear_height | flip_a | 0.09292, 0.09292, 0.09292, 0.09292, 0.09292 |
| hf_phys_hann_linear_height | flip_b | 0.2116, 0.2116, 0.2116, 0.2116, 0.2116 |
| hf_phys_hann_uint8 | V-1.0_A-1.0 | 0.5024, 0.5559, 0.5761, 0.585, 0.589 |
| hf_phys_hann_uint8 | V-1.0_A-0.5 | 0.5827, 0.6534, 0.6794, 0.6892, 0.6919 |
| hf_phys_hann_uint8 | V-1.0_A+0.0 | 0.6391, 0.7132, 0.7396, 0.7483, 0.7496 |
| hf_phys_hann_uint8 | V-1.0_A+0.5 | 0.6817, 0.75, 0.775, 0.7835, 0.7848 |
| hf_phys_hann_uint8 | V-1.0_A+1.0 | 0.7145, 0.7721, 0.7957, 0.805, 0.8073 |
| hf_phys_hann_uint8 | V-0.5_A-1.0 | 0.4948, 0.5438, 0.5602, 0.5669, 0.5701 |
| hf_phys_hann_uint8 | V-0.5_A-0.5 | 0.5785, 0.649, 0.6749, 0.6858, 0.6903 |
| hf_phys_hann_uint8 | V-0.5_A+0.0 | 0.6409, 0.7186, 0.747, 0.7577, 0.7607 |
| hf_phys_hann_uint8 | V-0.5_A+0.5 | 0.6895, 0.7628, 0.7898, 0.7995, 0.8017 |
| hf_phys_hann_uint8 | V-0.5_A+1.0 | 0.7276, 0.7898, 0.8142, 0.8239, 0.8265 |
| hf_phys_hann_uint8 | V+0.0_A-1.0 | 0.4928, 0.5373, 0.55, 0.554, 0.5555 |
| hf_phys_hann_uint8 | V+0.0_A-0.5 | 0.5741, 0.6423, 0.6661, 0.676, 0.681 |
| hf_phys_hann_uint8 | V+0.0_A+0.0 | 0.6409, 0.7206, 0.7502, 0.7627, 0.7679 |
| hf_phys_hann_uint8 | V+0.0_A+0.5 | 0.6948, 0.7732, 0.8028, 0.8146, 0.8185 |
| hf_phys_hann_uint8 | V+0.0_A+1.0 | 0.7385, 0.807, 0.8336, 0.8443, 0.8477 |
| hf_phys_hann_uint8 | V+0.5_A-1.0 | 0.5092, 0.5507, 0.5612, 0.564, 0.5647 |
| hf_phys_hann_uint8 | V+0.5_A-0.5 | 0.5738, 0.6381, 0.6582, 0.6656, 0.669 |
| hf_phys_hann_uint8 | V+0.5_A+0.0 | 0.6406, 0.7198, 0.7487, 0.7614, 0.7681 |
| hf_phys_hann_uint8 | V+0.5_A+0.5 | 0.6979, 0.7798, 0.8117, 0.8259, 0.8326 |
| hf_phys_hann_uint8 | V+0.5_A+1.0 | 0.7461, 0.821, 0.8513, 0.8643, 0.8697 |
| hf_phys_hann_uint8 | V+1.0_A-1.0 | 0.6056, 0.6431, 0.6529, 0.6557, 0.6561 |
| hf_phys_hann_uint8 | V+1.0_A-0.5 | 0.6081, 0.6648, 0.6811, 0.6865, 0.6885 |
| hf_phys_hann_uint8 | V+1.0_A+0.0 | 0.6531, 0.7276, 0.7528, 0.7629, 0.7681 |
| hf_phys_hann_uint8 | V+1.0_A+0.5 | 0.7034, 0.7854, 0.8168, 0.8314, 0.84 |
| hf_phys_hann_uint8 | V+1.0_A+1.0 | 0.7516, 0.8299, 0.8631, 0.8788, 0.8879 |
| hf_phys_hann_uint8 | V-1.0_A+0.25 | 0.6619, 0.7339, 0.7597, 0.7681, 0.7693 |
| hf_phys_hann_uint8 | V-0.5_A+0.25 | 0.6669, 0.7434, 0.7713, 0.7815, 0.7839 |
| hf_phys_hann_uint8 | V+0.0_A+0.25 | 0.6696, 0.7498, 0.7799, 0.7923, 0.7968 |
| hf_phys_hann_uint8 | V+0.5_A+0.25 | 0.6707, 0.7525, 0.7837, 0.7976, 0.8047 |
| hf_phys_hann_uint8 | V+1.0_A+0.25 | 0.6784, 0.7578, 0.7866, 0.7994, 0.8068 |
| hf_phys_hann_uint8 | sine_periodic | 0.1526, 0.1523, 0.1522, 0.1521, 0.152 |
| hf_phys_hann_uint8 | sine_jump | 0.2003, 0.2002, 0.2002, 0.2002, 0.2002 |
| hf_phys_hann_uint8 | flip_a | 1, 1, 1, 1, 1 |
| hf_phys_hann_uint8 | flip_b | 0.3825, 0.3471, 0.3241, 0.31, 0.2896 |
| hf_phys_pplus_float | V-1.0_A-1.0 | 0.4976, 0.5506, 0.571, 0.5803, 0.5846 |
| hf_phys_pplus_float | V-1.0_A-0.5 | 0.5762, 0.6443, 0.6701, 0.6804, 0.6834 |
| hf_phys_pplus_float | V-1.0_A+0.0 | 0.6278, 0.6962, 0.7222, 0.7316, 0.7333 |
| hf_phys_pplus_float | V-1.0_A+0.5 | 0.6639, 0.7239, 0.7486, 0.7583, 0.7603 |
| hf_phys_pplus_float | V-1.0_A+1.0 | 0.6886, 0.7372, 0.7611, 0.7721, 0.775 |
| hf_phys_pplus_float | V-0.5_A-1.0 | 0.4882, 0.5372, 0.5538, 0.5607, 0.564 |
| hf_phys_pplus_float | V-0.5_A-0.5 | 0.5734, 0.6423, 0.6681, 0.6793, 0.684 |
| hf_phys_pplus_float | V-0.5_A+0.0 | 0.6333, 0.7065, 0.7341, 0.7453, 0.7487 |
| hf_phys_pplus_float | V-0.5_A+0.5 | 0.677, 0.7427, 0.7684, 0.7792, 0.7821 |
| hf_phys_pplus_float | V-0.5_A+1.0 | 0.7083, 0.7611, 0.7845, 0.796, 0.7997 |
| hf_phys_pplus_float | V+0.0_A-1.0 | 0.4802, 0.5253, 0.5383, 0.5425, 0.544 |
| hf_phys_pplus_float | V+0.0_A-0.5 | 0.5679, 0.6359, 0.6598, 0.6701, 0.6752 |
| hf_phys_pplus_float | V+0.0_A+0.0 | 0.6354, 0.7127, 0.7418, 0.7545, 0.7601 |
| hf_phys_pplus_float | V+0.0_A+0.5 | 0.6873, 0.7602, 0.7882, 0.8004, 0.8049 |
| hf_phys_pplus_float | V+0.0_A+1.0 | 0.7265, 0.7869, 0.8113, 0.8231, 0.8276 |
| hf_phys_pplus_float | V+0.5_A-1.0 | 0.4771, 0.5203, 0.5315, 0.5344, 0.5351 |
| hf_phys_pplus_float | V+0.5_A-0.5 | 0.5609, 0.6266, 0.6473, 0.655, 0.6585 |
| hf_phys_pplus_float | V+0.5_A+0.0 | 0.6335, 0.7129, 0.742, 0.7551, 0.762 |
| hf_phys_pplus_float | V+0.5_A+0.5 | 0.693, 0.7727, 0.8038, 0.818, 0.8249 |
| hf_phys_pplus_float | V+0.5_A+1.0 | 0.7402, 0.8106, 0.8386, 0.8515, 0.8576 |
| hf_phys_pplus_float | V+1.0_A-1.0 | 0.4837, 0.5276, 0.5392, 0.5422, 0.543 |
| hf_phys_pplus_float | V+1.0_A-0.5 | 0.5546, 0.618, 0.6358, 0.6409, 0.6426 |
| hf_phys_pplus_float | V+1.0_A+0.0 | 0.6282, 0.7071, 0.7342, 0.7453, 0.7512 |
| hf_phys_pplus_float | V+1.0_A+0.5 | 0.693, 0.7764, 0.8092, 0.8246, 0.8337 |
| hf_phys_pplus_float | V+1.0_A+1.0 | 0.7468, 0.8252, 0.8583, 0.8741, 0.8833 |
| hf_phys_pplus_float | V-1.0_A+0.25 | 0.6636, 0.7241, 0.7477, 0.7568, 0.7586 |
| hf_phys_pplus_float | V-0.5_A+0.25 | 0.6741, 0.7403, 0.7653, 0.7756, 0.7786 |
| hf_phys_pplus_float | V+0.0_A+0.25 | 0.6813, 0.7536, 0.7809, 0.7927, 0.7975 |
| hf_phys_pplus_float | V+0.5_A+0.25 | 0.6839, 0.7611, 0.7903, 0.8035, 0.8104 |
| hf_phys_pplus_float | V+1.0_A+0.25 | 0.6817, 0.7607, 0.7897, 0.8027, 0.8101 |
| hf_phys_pplus_float | sine_periodic | 0.1437, 0.1434, 0.1434, 0.1434, 0.1434 |
| hf_phys_pplus_float | sine_jump | 0.2188, 0.2217, 0.2226, 0.2229, 0.2229 |
| hf_phys_pplus_float | flip_a | 0.3697, 0.9757, 0.9868, 0.9884, 0.9888 |
| hf_phys_pplus_float | flip_b | 0.2086, 0.2082, 0.2081, 0.2081, 0.2081 |
| hf_phys_pplus_linear_height | V-1.0_A-1.0 | 0.1264, 0.1262, 0.1261, 0.1261, 0.1261 |
| hf_phys_pplus_linear_height | V-1.0_A-0.5 | 0.2227, 0.2223, 0.2222, 0.2221, 0.2221 |
| hf_phys_pplus_linear_height | V-1.0_A+0.0 | 0.3313, 0.3311, 0.331, 0.3309, 0.3309 |
| hf_phys_pplus_linear_height | V-1.0_A+0.5 | 0.4426, 0.4425, 0.4424, 0.4424, 0.4424 |
| hf_phys_pplus_linear_height | V-1.0_A+1.0 | 0.5497, 0.5504, 0.5505, 0.5506, 0.5506 |
| hf_phys_pplus_linear_height | V-0.5_A-1.0 | 0.1222, 0.122, 0.1219, 0.1219, 0.1219 |
| hf_phys_pplus_linear_height | V-0.5_A-0.5 | 0.2172, 0.2168, 0.2166, 0.2166, 0.2166 |
| hf_phys_pplus_linear_height | V-0.5_A+0.0 | 0.3259, 0.3256, 0.3256, 0.3255, 0.3255 |
| hf_phys_pplus_linear_height | V-0.5_A+0.5 | 0.4381, 0.438, 0.4378, 0.4378, 0.4378 |
| hf_phys_pplus_linear_height | V-0.5_A+1.0 | 0.5462, 0.5468, 0.5469, 0.547, 0.547 |
| hf_phys_pplus_linear_height | V+0.0_A-1.0 | 0.1191, 0.1189, 0.1188, 0.1188, 0.1188 |
| hf_phys_pplus_linear_height | V+0.0_A-0.5 | 0.2119, 0.2115, 0.2114, 0.2113, 0.2113 |
| hf_phys_pplus_linear_height | V+0.0_A+0.0 | 0.3204, 0.3202, 0.3201, 0.3201, 0.3201 |
| hf_phys_pplus_linear_height | V+0.0_A+0.5 | 0.4334, 0.4332, 0.4331, 0.433, 0.433 |
| hf_phys_pplus_linear_height | V+0.0_A+1.0 | 0.5426, 0.5431, 0.5432, 0.5432, 0.5432 |
| hf_phys_pplus_linear_height | V+0.5_A-1.0 | 0.118, 0.1178, 0.1177, 0.1177, 0.1177 |
| hf_phys_pplus_linear_height | V+0.5_A-0.5 | 0.2074, 0.207, 0.2069, 0.2068, 0.2068 |
| hf_phys_pplus_linear_height | V+0.5_A+0.0 | 0.3151, 0.3148, 0.3147, 0.3147, 0.3147 |
| hf_phys_pplus_linear_height | V+0.5_A+0.5 | 0.4285, 0.4283, 0.4282, 0.4282, 0.4281 |
| hf_phys_pplus_linear_height | V+0.5_A+1.0 | 0.5387, 0.5391, 0.5392, 0.5392, 0.5392 |
| hf_phys_pplus_linear_height | V+1.0_A-1.0 | 0.1204, 0.1201, 0.12, 0.12, 0.12 |
| hf_phys_pplus_linear_height | V+1.0_A-0.5 | 0.2043, 0.2039, 0.2037, 0.2037, 0.2037 |
| hf_phys_pplus_linear_height | V+1.0_A+0.0 | 0.3101, 0.3098, 0.3097, 0.3097, 0.3097 |
| hf_phys_pplus_linear_height | V+1.0_A+0.5 | 0.4237, 0.4234, 0.4233, 0.4232, 0.4232 |
| hf_phys_pplus_linear_height | V+1.0_A+1.0 | 0.5348, 0.5351, 0.5351, 0.5351, 0.5352 |
| hf_phys_pplus_linear_height | V-1.0_A+0.25 | 0.3896, 0.3905, 0.3909, 0.3911, 0.3913 |
| hf_phys_pplus_linear_height | V-0.5_A+0.25 | 0.3845, 0.3854, 0.3858, 0.386, 0.3861 |
| hf_phys_pplus_linear_height | V+0.0_A+0.25 | 0.3793, 0.3801, 0.3805, 0.3807, 0.3808 |
| hf_phys_pplus_linear_height | V+0.5_A+0.25 | 0.374, 0.3748, 0.3752, 0.3754, 0.3755 |
| hf_phys_pplus_linear_height | V+1.0_A+0.25 | 0.3688, 0.3696, 0.3699, 0.3702, 0.3703 |
| hf_phys_pplus_linear_height | sine_periodic | 0.1438, 0.1435, 0.1434, 0.1434, 0.1434 |
| hf_phys_pplus_linear_height | sine_jump | 0.1877, 0.1876, 0.1876, 0.1876, 0.1876 |
| hf_phys_pplus_linear_height | flip_a | 0.0872, 0.0915, 0.09259, 0.09253, 0.09234 |
| hf_phys_pplus_linear_height | flip_b | 0.2063, 0.2077, 0.208, 0.2081, 0.2081 |
| hf_phys_pplus_uint8 | V-1.0_A-1.0 | 0.4977, 0.5507, 0.5711, 0.5803, 0.5846 |
| hf_phys_pplus_uint8 | V-1.0_A-0.5 | 0.5761, 0.6442, 0.6701, 0.6803, 0.6833 |
| hf_phys_pplus_uint8 | V-1.0_A+0.0 | 0.6277, 0.6961, 0.7221, 0.7315, 0.7333 |
| hf_phys_pplus_uint8 | V-1.0_A+0.5 | 0.6638, 0.7238, 0.7485, 0.7582, 0.7602 |
| hf_phys_pplus_uint8 | V-1.0_A+1.0 | 0.6885, 0.7371, 0.761, 0.772, 0.775 |
| hf_phys_pplus_uint8 | V-0.5_A-1.0 | 0.4887, 0.5376, 0.5541, 0.561, 0.5643 |
| hf_phys_pplus_uint8 | V-0.5_A-0.5 | 0.5734, 0.6423, 0.6681, 0.6792, 0.684 |
| hf_phys_pplus_uint8 | V-0.5_A+0.0 | 0.6333, 0.7064, 0.734, 0.7452, 0.7486 |
| hf_phys_pplus_uint8 | V-0.5_A+0.5 | 0.6769, 0.7425, 0.7683, 0.7791, 0.782 |
| hf_phys_pplus_uint8 | V-0.5_A+1.0 | 0.7081, 0.761, 0.7844, 0.7959, 0.7996 |
| hf_phys_pplus_uint8 | V+0.0_A-1.0 | 0.4815, 0.5265, 0.5394, 0.5435, 0.5451 |
| hf_phys_pplus_uint8 | V+0.0_A-0.5 | 0.5682, 0.6362, 0.66, 0.6702, 0.6754 |
| hf_phys_pplus_uint8 | V+0.0_A+0.0 | 0.6354, 0.7125, 0.7416, 0.7544, 0.7599 |
| hf_phys_pplus_uint8 | V+0.0_A+0.5 | 0.6872, 0.7601, 0.7881, 0.8002, 0.8048 |
| hf_phys_pplus_uint8 | V+0.0_A+1.0 | 0.7263, 0.7867, 0.8111, 0.8229, 0.8275 |
| hf_phys_pplus_uint8 | V+0.5_A-1.0 | 0.4818, 0.5244, 0.5355, 0.5383, 0.5391 |
| hf_phys_pplus_uint8 | V+0.5_A-0.5 | 0.5625, 0.6278, 0.6483, 0.6559, 0.6594 |
| hf_phys_pplus_uint8 | V+0.5_A+0.0 | 0.6343, 0.7132, 0.7423, 0.7553, 0.7622 |
| hf_phys_pplus_uint8 | V+0.5_A+0.5 | 0.6931, 0.7724, 0.8035, 0.8177, 0.8245 |
| hf_phys_pplus_uint8 | V+0.5_A+1.0 | 0.74, 0.8103, 0.8383, 0.8513, 0.8574 |
| hf_phys_pplus_uint8 | V+1.0_A-1.0 | 0.5124, 0.5536, 0.5645, 0.5673, 0.568 |
| hf_phys_pplus_uint8 | V+1.0_A-0.5 | 0.5638, 0.6253, 0.6428, 0.6478, 0.6495 |
| hf_phys_pplus_uint8 | V+1.0_A+0.0 | 0.633, 0.7106, 0.7373, 0.7481, 0.7538 |
| hf_phys_pplus_uint8 | V+1.0_A+0.5 | 0.695, 0.7781, 0.8101, 0.825, 0.8338 |
| hf_phys_pplus_uint8 | V+1.0_A+1.0 | 0.7453, 0.8238, 0.8569, 0.8726, 0.8822 |
| hf_phys_pplus_uint8 | V-1.0_A+0.25 | 0.6635, 0.7241, 0.7477, 0.7567, 0.7586 |
| hf_phys_pplus_uint8 | V-0.5_A+0.25 | 0.674, 0.7402, 0.7652, 0.7755, 0.7785 |
| hf_phys_pplus_uint8 | V+0.0_A+0.25 | 0.6812, 0.7535, 0.7808, 0.7926, 0.7973 |
| hf_phys_pplus_uint8 | V+0.5_A+0.25 | 0.6843, 0.7612, 0.7902, 0.8035, 0.8103 |
| hf_phys_pplus_uint8 | V+1.0_A+0.25 | 0.6854, 0.7633, 0.7917, 0.8043, 0.8115 |
| hf_phys_pplus_uint8 | sine_periodic | 0.1446, 0.1443, 0.1443, 0.1443, 0.1443 |
| hf_phys_pplus_uint8 | sine_jump | 0.2193, 0.2222, 0.2232, 0.2235, 0.2235 |
| hf_phys_pplus_uint8 | flip_a | 1, 1, 1, 1, 1 |
| hf_phys_pplus_uint8 | flip_b | 0.4448, 0.4207, 0.4557, 0.4557, 0.4471 |
| hf_phys_raw_float | V-1.0_A-1.0 | 0.4981, 0.5507, 0.571, 0.5803, 0.5846 |
| hf_phys_raw_float | V-1.0_A-0.5 | 0.5769, 0.6444, 0.6702, 0.6804, 0.6834 |
| hf_phys_raw_float | V-1.0_A+0.0 | 0.6284, 0.6964, 0.7222, 0.7316, 0.7333 |
| hf_phys_raw_float | V-1.0_A+0.5 | 0.6645, 0.724, 0.7486, 0.7583, 0.7603 |
| hf_phys_raw_float | V-1.0_A+1.0 | 0.6891, 0.7374, 0.7611, 0.7721, 0.775 |
| hf_phys_raw_float | V-0.5_A-1.0 | 0.4887, 0.5372, 0.5538, 0.5607, 0.564 |
| hf_phys_raw_float | V-0.5_A-0.5 | 0.5741, 0.6424, 0.6681, 0.6793, 0.684 |
| hf_phys_raw_float | V-0.5_A+0.0 | 0.634, 0.7066, 0.7342, 0.7453, 0.7487 |
| hf_phys_raw_float | V-0.5_A+0.5 | 0.6776, 0.7428, 0.7685, 0.7792, 0.7821 |
| hf_phys_raw_float | V-0.5_A+1.0 | 0.7087, 0.7612, 0.7846, 0.7961, 0.7997 |
| hf_phys_raw_float | V+0.0_A-1.0 | 0.4807, 0.5253, 0.5383, 0.5425, 0.544 |
| hf_phys_raw_float | V+0.0_A-0.5 | 0.5686, 0.636, 0.6598, 0.67, 0.6752 |
| hf_phys_raw_float | V+0.0_A+0.0 | 0.6361, 0.7128, 0.7418, 0.7545, 0.7601 |
| hf_phys_raw_float | V+0.0_A+0.5 | 0.688, 0.7603, 0.7883, 0.8004, 0.8049 |
| hf_phys_raw_float | V+0.0_A+1.0 | 0.727, 0.787, 0.8113, 0.8231, 0.8276 |
| hf_phys_raw_float | V+0.5_A-1.0 | 0.4776, 0.5203, 0.5315, 0.5344, 0.5351 |
| hf_phys_raw_float | V+0.5_A-0.5 | 0.5616, 0.6267, 0.6473, 0.655, 0.6585 |
| hf_phys_raw_float | V+0.5_A+0.0 | 0.6342, 0.713, 0.7421, 0.7551, 0.762 |
| hf_phys_raw_float | V+0.5_A+0.5 | 0.6937, 0.7728, 0.8038, 0.818, 0.8249 |
| hf_phys_raw_float | V+0.5_A+1.0 | 0.7409, 0.8107, 0.8387, 0.8515, 0.8576 |
| hf_phys_raw_float | V+1.0_A-1.0 | 0.4841, 0.5276, 0.5392, 0.5422, 0.543 |
| hf_phys_raw_float | V+1.0_A-0.5 | 0.5554, 0.618, 0.6357, 0.6409, 0.6426 |
| hf_phys_raw_float | V+1.0_A+0.0 | 0.629, 0.7072, 0.7342, 0.7453, 0.7512 |
| hf_phys_raw_float | V+1.0_A+0.5 | 0.6938, 0.7766, 0.8092, 0.8246, 0.8337 |
| hf_phys_raw_float | V+1.0_A+1.0 | 0.7475, 0.8254, 0.8584, 0.8742, 0.8833 |
| hf_phys_raw_float | V-1.0_A+0.25 | 0.6573, 0.7191, 0.7435, 0.7527, 0.7546 |
| hf_phys_raw_float | V-0.5_A+0.25 | 0.6679, 0.735, 0.7607, 0.7712, 0.7742 |
| hf_phys_raw_float | V+0.0_A+0.25 | 0.6753, 0.7482, 0.776, 0.788, 0.7928 |
| hf_phys_raw_float | V+0.5_A+0.25 | 0.6781, 0.7555, 0.7851, 0.7986, 0.8056 |
| hf_phys_raw_float | V+1.0_A+0.25 | 0.6761, 0.7551, 0.7844, 0.7976, 0.8051 |
| hf_phys_raw_float | sine_periodic | 0.1436, 0.1434, 0.1434, 0.1434, 0.1434 |
| hf_phys_raw_float | sine_jump | 0.2313, 0.233, 0.2335, 0.2336, 0.2336 |
| hf_phys_raw_float | flip_a | 0.3697, 0.9757, 0.9868, 0.9884, 0.9888 |
| hf_phys_raw_float | flip_b | 0.2086, 0.2082, 0.2081, 0.2081, 0.2081 |
| hf_phys_raw_linear_height | V-1.0_A-1.0 | 0.1261, 0.1261, 0.1261, 0.1261, 0.1261 |
| hf_phys_raw_linear_height | V-1.0_A-0.5 | 0.2221, 0.2222, 0.2221, 0.2221, 0.2221 |
| hf_phys_raw_linear_height | V-1.0_A+0.0 | 0.3309, 0.3309, 0.3309, 0.3309, 0.3309 |
| hf_phys_raw_linear_height | V-1.0_A+0.5 | 0.4422, 0.4424, 0.4424, 0.4424, 0.4424 |
| hf_phys_raw_linear_height | V-1.0_A+1.0 | 0.5503, 0.5505, 0.5506, 0.5506, 0.5506 |
| hf_phys_raw_linear_height | V-0.5_A-1.0 | 0.1219, 0.1219, 0.1219, 0.1219, 0.1219 |
| hf_phys_raw_linear_height | V-0.5_A-0.5 | 0.2166, 0.2166, 0.2166, 0.2166, 0.2166 |
| hf_phys_raw_linear_height | V-0.5_A+0.0 | 0.3255, 0.3255, 0.3255, 0.3255, 0.3255 |
| hf_phys_raw_linear_height | V-0.5_A+0.5 | 0.4376, 0.4378, 0.4378, 0.4378, 0.4378 |
| hf_phys_raw_linear_height | V-0.5_A+1.0 | 0.5467, 0.547, 0.547, 0.547, 0.547 |
| hf_phys_raw_linear_height | V+0.0_A-1.0 | 0.1188, 0.1188, 0.1188, 0.1188, 0.1188 |
| hf_phys_raw_linear_height | V+0.0_A-0.5 | 0.2113, 0.2113, 0.2113, 0.2113, 0.2113 |
| hf_phys_raw_linear_height | V+0.0_A+0.0 | 0.32, 0.3201, 0.3201, 0.3201, 0.3201 |
| hf_phys_raw_linear_height | V+0.0_A+0.5 | 0.4329, 0.433, 0.433, 0.433, 0.433 |
| hf_phys_raw_linear_height | V+0.0_A+1.0 | 0.543, 0.5432, 0.5432, 0.5432, 0.5432 |
| hf_phys_raw_linear_height | V+0.5_A-1.0 | 0.1177, 0.1177, 0.1177, 0.1177, 0.1177 |
| hf_phys_raw_linear_height | V+0.5_A-0.5 | 0.2068, 0.2068, 0.2068, 0.2068, 0.2068 |
| hf_phys_raw_linear_height | V+0.5_A+0.0 | 0.3147, 0.3147, 0.3147, 0.3147, 0.3147 |
| hf_phys_raw_linear_height | V+0.5_A+0.5 | 0.428, 0.4281, 0.4281, 0.4281, 0.4281 |
| hf_phys_raw_linear_height | V+0.5_A+1.0 | 0.5391, 0.5392, 0.5393, 0.5393, 0.5393 |
| hf_phys_raw_linear_height | V+1.0_A-1.0 | 0.12, 0.12, 0.12, 0.12, 0.12 |
| hf_phys_raw_linear_height | V+1.0_A-0.5 | 0.2037, 0.2037, 0.2037, 0.2037, 0.2037 |
| hf_phys_raw_linear_height | V+1.0_A+0.0 | 0.3097, 0.3097, 0.3097, 0.3097, 0.3097 |
| hf_phys_raw_linear_height | V+1.0_A+0.5 | 0.4231, 0.4232, 0.4232, 0.4232, 0.4232 |
| hf_phys_raw_linear_height | V+1.0_A+1.0 | 0.535, 0.5351, 0.5352, 0.5352, 0.5352 |
| hf_phys_raw_linear_height | V-1.0_A+0.25 | 0.4199, 0.4206, 0.4208, 0.4208, 0.4209 |
| hf_phys_raw_linear_height | V-0.5_A+0.25 | 0.4153, 0.4159, 0.4161, 0.4161, 0.4162 |
| hf_phys_raw_linear_height | V+0.0_A+0.25 | 0.4105, 0.4111, 0.4113, 0.4113, 0.4113 |
| hf_phys_raw_linear_height | V+0.5_A+0.25 | 0.4056, 0.4063, 0.4064, 0.4065, 0.4065 |
| hf_phys_raw_linear_height | V+1.0_A+0.25 | 0.4009, 0.4015, 0.4017, 0.4017, 0.4017 |
| hf_phys_raw_linear_height | sine_periodic | 0.1434, 0.1434, 0.1434, 0.1434, 0.1434 |
| hf_phys_raw_linear_height | sine_jump | 0.2389, 0.2396, 0.2398, 0.2398, 0.2398 |
| hf_phys_raw_linear_height | flip_a | 0.09206, 0.09206, 0.09206, 0.09206, 0.09206 |
| hf_phys_raw_linear_height | flip_b | 0.2081, 0.2081, 0.2081, 0.2081, 0.2081 |
| hf_phys_raw_uint8 | V-1.0_A-1.0 | 0.4982, 0.5508, 0.5711, 0.5803, 0.5846 |
| hf_phys_raw_uint8 | V-1.0_A-0.5 | 0.5768, 0.6443, 0.6701, 0.6803, 0.6833 |
| hf_phys_raw_uint8 | V-1.0_A+0.0 | 0.6284, 0.6963, 0.7221, 0.7315, 0.7333 |
| hf_phys_raw_uint8 | V-1.0_A+0.5 | 0.6644, 0.7239, 0.7485, 0.7582, 0.7602 |
| hf_phys_raw_uint8 | V-1.0_A+1.0 | 0.6889, 0.7373, 0.761, 0.772, 0.775 |
| hf_phys_raw_uint8 | V-0.5_A-1.0 | 0.4892, 0.5377, 0.5541, 0.561, 0.5643 |
| hf_phys_raw_uint8 | V-0.5_A-0.5 | 0.5742, 0.6424, 0.6681, 0.6792, 0.684 |
| hf_phys_raw_uint8 | V-0.5_A+0.0 | 0.634, 0.7066, 0.7341, 0.7452, 0.7486 |
| hf_phys_raw_uint8 | V-0.5_A+0.5 | 0.6775, 0.7427, 0.7684, 0.7791, 0.782 |
| hf_phys_raw_uint8 | V-0.5_A+1.0 | 0.7086, 0.7611, 0.7845, 0.7959, 0.7996 |
| hf_phys_raw_uint8 | V+0.0_A-1.0 | 0.482, 0.5265, 0.5394, 0.5435, 0.5451 |
| hf_phys_raw_uint8 | V+0.0_A-0.5 | 0.569, 0.6363, 0.66, 0.6702, 0.6754 |
| hf_phys_raw_uint8 | V+0.0_A+0.0 | 0.6361, 0.7126, 0.7416, 0.7544, 0.7599 |
| hf_phys_raw_uint8 | V+0.0_A+0.5 | 0.6879, 0.7602, 0.7881, 0.8002, 0.8048 |
| hf_phys_raw_uint8 | V+0.0_A+1.0 | 0.7269, 0.7868, 0.8112, 0.8229, 0.8275 |
| hf_phys_raw_uint8 | V+0.5_A-1.0 | 0.4822, 0.5244, 0.5355, 0.5383, 0.5391 |
| hf_phys_raw_uint8 | V+0.5_A-0.5 | 0.5633, 0.628, 0.6483, 0.6559, 0.6594 |
| hf_phys_raw_uint8 | V+0.5_A+0.0 | 0.6351, 0.7134, 0.7423, 0.7553, 0.7622 |
| hf_phys_raw_uint8 | V+0.5_A+0.5 | 0.694, 0.7726, 0.8036, 0.8177, 0.8245 |
| hf_phys_raw_uint8 | V+0.5_A+1.0 | 0.7406, 0.8104, 0.8383, 0.8513, 0.8574 |
| hf_phys_raw_uint8 | V+1.0_A-1.0 | 0.5129, 0.5537, 0.5645, 0.5673, 0.568 |
| hf_phys_raw_uint8 | V+1.0_A-0.5 | 0.5644, 0.6253, 0.6427, 0.6478, 0.6495 |
| hf_phys_raw_uint8 | V+1.0_A+0.0 | 0.6339, 0.7108, 0.7374, 0.7481, 0.7538 |
| hf_phys_raw_uint8 | V+1.0_A+0.5 | 0.696, 0.7784, 0.8101, 0.825, 0.8338 |
| hf_phys_raw_uint8 | V+1.0_A+1.0 | 0.7461, 0.824, 0.8569, 0.8726, 0.8822 |
| hf_phys_raw_uint8 | V-1.0_A+0.25 | 0.6572, 0.719, 0.7434, 0.7526, 0.7545 |
| hf_phys_raw_uint8 | V-0.5_A+0.25 | 0.6678, 0.7349, 0.7606, 0.7711, 0.7741 |
| hf_phys_raw_uint8 | V+0.0_A+0.25 | 0.6752, 0.7481, 0.7759, 0.7879, 0.7927 |
| hf_phys_raw_uint8 | V+0.5_A+0.25 | 0.6785, 0.7556, 0.7851, 0.7986, 0.8056 |
| hf_phys_raw_uint8 | V+1.0_A+0.25 | 0.6798, 0.7578, 0.7864, 0.7991, 0.8064 |
| hf_phys_raw_uint8 | sine_periodic | 0.1443, 0.1443, 0.1443, 0.1443, 0.1443 |
| hf_phys_raw_uint8 | sine_jump | 0.2317, 0.2334, 0.2338, 0.234, 0.234 |
| hf_phys_raw_uint8 | flip_a | 1, 1, 1, 1, 1 |
| hf_phys_raw_uint8 | flip_b | 0.4448, 0.4311, 0.4525, 0.4541, 0.4467 |
| hf_px_hann_float | V-1.0_A-1.0 | 0.9899, 0.952, 0.7941, 0.5837, 0.3529 |
| hf_px_hann_float | V-1.0_A-0.5 | 0.9807, 0.9632, 0.8648, 0.6893, 0.4784 |
| hf_px_hann_float | V-1.0_A+0.0 | 0.97, 0.9484, 0.8943, 0.7488, 0.5548 |
| hf_px_hann_float | V-1.0_A+0.5 | 0.9587, 0.9299, 0.9018, 0.7844, 0.6054 |
| hf_px_hann_float | V-1.0_A+1.0 | 0.9472, 0.9124, 0.897, 0.8061, 0.6409 |
| hf_px_hann_float | V-0.5_A-1.0 | 0.9943, 0.9568, 0.7877, 0.5634, 0.3249 |
| hf_px_hann_float | V-0.5_A-0.5 | 0.9885, 0.9754, 0.8709, 0.6854, 0.4708 |
| hf_px_hann_float | V-0.5_A+0.0 | 0.9811, 0.9656, 0.909, 0.7581, 0.5644 |
| hf_px_hann_float | V-0.5_A+0.5 | 0.9727, 0.9504, 0.9209, 0.8002, 0.6233 |
| hf_px_hann_float | V-0.5_A+1.0 | 0.9639, 0.9349, 0.9178, 0.8248, 0.6624 |
| hf_px_hann_float | V+0.0_A-1.0 | 0.9972, 0.9598, 0.7812, 0.5445, 0.2987 |
| hf_px_hann_float | V+0.0_A-0.5 | 0.9942, 0.9848, 0.8731, 0.6738, 0.4508 |
| hf_px_hann_float | V+0.0_A+0.0 | 0.9899, 0.9807, 0.9218, 0.7626, 0.5671 |
| hf_px_hann_float | V+0.0_A+0.5 | 0.9847, 0.9703, 0.9406, 0.8151, 0.6408 |
| hf_px_hann_float | V+0.0_A+1.0 | 0.9789, 0.9586, 0.9411, 0.845, 0.6872 |
| hf_px_hann_float | V+0.5_A-1.0 | 0.9989, 0.9617, 0.7788, 0.5359, 0.2868 |
| hf_px_hann_float | V+0.5_A-0.5 | 0.9978, 0.9907, 0.8718, 0.6571, 0.422 |
| hf_px_hann_float | V+0.5_A+0.0 | 0.9959, 0.9918, 0.9303, 0.759, 0.5562 |
| hf_px_hann_float | V+0.5_A+0.5 | 0.9935, 0.9867, 0.958, 0.8258, 0.6526 |
| hf_px_hann_float | V+0.5_A+1.0 | 0.9906, 0.9802, 0.9649, 0.8648, 0.7133 |
| hf_px_hann_float | V+1.0_A-1.0 | 0.9996, 0.9638, 0.7848, 0.5435, 0.293 |
| hf_px_hann_float | V+1.0_A-0.5 | 0.9995, 0.9935, 0.8691, 0.6422, 0.3975 |
| hf_px_hann_float | V+1.0_A+0.0 | 0.9991, 0.9978, 0.9329, 0.7467, 0.5295 |
| hf_px_hann_float | V+1.0_A+0.5 | 0.9985, 0.9969, 0.9689, 0.8268, 0.6479 |
| hf_px_hann_float | V+1.0_A+1.0 | 0.9978, 0.9951, 0.9834, 0.8784, 0.7312 |
| hf_px_hann_float | V-1.0_A+0.25 | 0.9644, 0.9392, 0.9001, 0.7688, 0.5825 |
| hf_px_hann_float | V-0.5_A+0.25 | 0.977, 0.9582, 0.9174, 0.782, 0.5971 |
| hf_px_hann_float | V+0.0_A+0.25 | 0.9874, 0.9758, 0.9342, 0.7926, 0.6084 |
| hf_px_hann_float | V+0.5_A+0.25 | 0.9947, 0.9895, 0.9474, 0.7967, 0.6097 |
| hf_px_hann_float | V+1.0_A+0.25 | 0.9988, 0.9975, 0.9542, 0.7907, 0.5928 |
| hf_px_hann_float | sine_periodic | 0.9947, 0.9904, 0.7163, 0.147, 0.01314 |
| hf_px_hann_float | sine_jump | 0.9936, 0.9902, 0.7988, 0.1948, 0.01861 |
| hf_px_hann_float | flip_a | 0.8538, 0.9824, 0.9872, 0.9885, 0.9884 |
| hf_px_hann_float | flip_b | 1, 0.9997, 0.828, 0.2116, 0.02064 |
| hf_px_hann_linear_height | V-1.0_A-1.0 | 0.9996, 0.8946, 0.4241, 0.1288, 0.03243 |
| hf_px_hann_linear_height | V-1.0_A-0.5 | 1, 0.9843, 0.6306, 0.225, 0.06512 |
| hf_px_hann_linear_height | V-1.0_A+0.0 | 1, 0.9987, 0.7994, 0.3335, 0.107 |
| hf_px_hann_linear_height | V-1.0_A+0.5 | 1, 0.9999, 0.9089, 0.4444, 0.1549 |
| hf_px_hann_linear_height | V-1.0_A+1.0 | 1, 1, 0.9651, 0.5518, 0.2067 |
| hf_px_hann_linear_height | V-0.5_A-1.0 | 0.9996, 0.8937, 0.4202, 0.1246, 0.03028 |
| hf_px_hann_linear_height | V-0.5_A-0.5 | 1, 0.9842, 0.6272, 0.2195, 0.06137 |
| hf_px_hann_linear_height | V-0.5_A+0.0 | 1, 0.9987, 0.7975, 0.3282, 0.1023 |
| hf_px_hann_linear_height | V-0.5_A+0.5 | 1, 0.9999, 0.908, 0.4398, 0.1499 |
| hf_px_hann_linear_height | V-0.5_A+1.0 | 1, 1, 0.9648, 0.5482, 0.2018 |
| hf_px_hann_linear_height | V+0.0_A-1.0 | 0.9995, 0.8931, 0.4174, 0.1215, 0.02874 |
| hf_px_hann_linear_height | V+0.0_A-0.5 | 1, 0.984, 0.624, 0.2143, 0.05791 |
| hf_px_hann_linear_height | V+0.0_A+0.0 | 1, 0.9987, 0.7955, 0.3227, 0.09767 |
| hf_px_hann_linear_height | V+0.0_A+0.5 | 1, 0.9999, 0.9071, 0.4351, 0.1448 |
| hf_px_hann_linear_height | V+0.0_A+1.0 | 1, 1, 0.9645, 0.5445, 0.1968 |
| hf_px_hann_linear_height | V+0.5_A-1.0 | 0.9995, 0.893, 0.4168, 0.1204, 0.02814 |
| hf_px_hann_linear_height | V+0.5_A-0.5 | 1, 0.9839, 0.6213, 0.2098, 0.05498 |
| hf_px_hann_linear_height | V+0.5_A+0.0 | 1, 0.9987, 0.7936, 0.3174, 0.09318 |
| hf_px_hann_linear_height | V+0.5_A+0.5 | 1, 0.9999, 0.9062, 0.4302, 0.1397 |
| hf_px_hann_linear_height | V+0.5_A+1.0 | 1, 1, 0.9641, 0.5405, 0.1916 |
| hf_px_hann_linear_height | V+1.0_A-1.0 | 0.9996, 0.8937, 0.4202, 0.1228, 0.02898 |
| hf_px_hann_linear_height | V+1.0_A-0.5 | 1, 0.9838, 0.6196, 0.2067, 0.05294 |
| hf_px_hann_linear_height | V+1.0_A+0.0 | 1, 0.9987, 0.7918, 0.3124, 0.08903 |
| hf_px_hann_linear_height | V+1.0_A+0.5 | 1, 0.9999, 0.9053, 0.4253, 0.1345 |
| hf_px_hann_linear_height | V+1.0_A+1.0 | 1, 1, 0.9638, 0.5365, 0.1862 |
| hf_px_hann_linear_height | V-1.0_A+0.25 | 1, 0.9997, 0.8618, 0.3891, 0.1303 |
| hf_px_hann_linear_height | V-0.5_A+0.25 | 1, 0.9997, 0.8605, 0.3841, 0.1254 |
| hf_px_hann_linear_height | V+0.0_A+0.25 | 1, 0.9997, 0.8591, 0.379, 0.1205 |
| hf_px_hann_linear_height | V+0.5_A+0.25 | 1, 0.9997, 0.8577, 0.3738, 0.1156 |
| hf_px_hann_linear_height | V+1.0_A+0.25 | 1, 0.9997, 0.8564, 0.3687, 0.1108 |
| hf_px_hann_linear_height | sine_periodic | 1, 0.9982, 0.7207, 0.1473, 0.01316 |
| hf_px_hann_linear_height | sine_jump | 1, 0.9996, 0.8056, 0.1953, 0.01864 |
| hf_px_hann_linear_height | flip_a | 0.8071, 0.3249, 0.1189, 0.09292, 0.09089 |
| hf_px_hann_linear_height | flip_b | 1, 0.9997, 0.8281, 0.2116, 0.02064 |
| hf_px_hann_uint8 | V-1.0_A-1.0 | 0.9629, 0.9492, 0.7944, 0.585, 0.3553 |
| hf_px_hann_uint8 | V-1.0_A-0.5 | 0.9681, 0.9567, 0.8638, 0.6892, 0.479 |
| hf_px_hann_uint8 | V-1.0_A+0.0 | 0.9671, 0.9467, 0.8932, 0.7483, 0.5548 |
| hf_px_hann_uint8 | V-1.0_A+0.5 | 0.9574, 0.9289, 0.9005, 0.7835, 0.605 |
| hf_px_hann_uint8 | V-1.0_A+1.0 | 0.9455, 0.911, 0.8954, 0.805, 0.6402 |
| hf_px_hann_uint8 | V-0.5_A-1.0 | 0.9615, 0.9552, 0.7896, 0.5669, 0.3298 |
| hf_px_hann_uint8 | V-0.5_A-0.5 | 0.9653, 0.9575, 0.8701, 0.6858, 0.4722 |
| hf_px_hann_uint8 | V-0.5_A+0.0 | 0.9677, 0.9587, 0.9078, 0.7577, 0.5647 |
| hf_px_hann_uint8 | V-0.5_A+0.5 | 0.9689, 0.9485, 0.9197, 0.7995, 0.6231 |
| hf_px_hann_uint8 | V-0.5_A+1.0 | 0.962, 0.9337, 0.9166, 0.8239, 0.662 |
| hf_px_hann_uint8 | V+0.0_A-1.0 | 0.9667, 0.9502, 0.7869, 0.554, 0.3099 |
| hf_px_hann_uint8 | V+0.0_A-0.5 | 0.9653, 0.9491, 0.873, 0.676, 0.4542 |
| hf_px_hann_uint8 | V+0.0_A+0.0 | 0.9634, 0.9574, 0.9202, 0.7627, 0.5682 |
| hf_px_hann_uint8 | V+0.0_A+0.5 | 0.9669, 0.9612, 0.9383, 0.8146, 0.6411 |
| hf_px_hann_uint8 | V+0.0_A+1.0 | 0.9681, 0.955, 0.9395, 0.8443, 0.6871 |
| hf_px_hann_uint8 | V+0.5_A-1.0 | 0.9501, 0.9433, 0.7987, 0.564, 0.3166 |
| hf_px_hann_uint8 | V+0.5_A-0.5 | 0.98, 0.9414, 0.8756, 0.6656, 0.4327 |
| hf_px_hann_uint8 | V+0.5_A+0.0 | 0.9678, 0.9428, 0.9278, 0.7614, 0.5598 |
| hf_px_hann_uint8 | V+0.5_A+0.5 | 0.9654, 0.9533, 0.9513, 0.8259, 0.6539 |
| hf_px_hann_uint8 | V+0.5_A+1.0 | 0.9642, 0.9603, 0.9559, 0.8643, 0.7137 |
| hf_px_hann_uint8 | V+1.0_A-1.0 | 0.9889, 0.9825, 0.8706, 0.6557, 0.4085 |
| hf_px_hann_uint8 | V+1.0_A-0.5 | 0.9864, 0.9331, 0.8962, 0.6865, 0.4479 |
| hf_px_hann_uint8 | V+1.0_A+0.0 | 0.9635, 0.934, 0.9277, 0.7629, 0.5493 |
| hf_px_hann_uint8 | V+1.0_A+0.5 | 0.9799, 0.9464, 0.941, 0.8314, 0.656 |
| hf_px_hann_uint8 | V+1.0_A+1.0 | 0.9796, 0.9474, 0.9451, 0.8788, 0.7347 |
| hf_px_hann_uint8 | V-1.0_A+0.25 | 0.9633, 0.9382, 0.899, 0.7681, 0.5823 |
| hf_px_hann_uint8 | V-0.5_A+0.25 | 0.9697, 0.9548, 0.9162, 0.7815, 0.5972 |
| hf_px_hann_uint8 | V+0.0_A+0.25 | 0.9664, 0.9613, 0.9321, 0.7923, 0.609 |
| hf_px_hann_uint8 | V+0.5_A+0.25 | 0.9671, 0.9492, 0.9423, 0.7976, 0.6119 |
| hf_px_hann_uint8 | V+1.0_A+0.25 | 0.9808, 0.9463, 0.9344, 0.7994, 0.6054 |
| hf_px_hann_uint8 | sine_periodic | 0.9363, 0.9222, 0.7169, 0.1521, 0.01839 |
| hf_px_hann_uint8 | sine_jump | 0.9628, 0.9379, 0.7975, 0.2002, 0.02454 |
| hf_px_hann_uint8 | flip_a | 0.8957, 1, 1, 1, 1 |
| hf_px_hann_uint8 | flip_b | 1, 1, 0.4143, 0.31, 0.6356 |
| hf_px_pplus_float | V-1.0_A-1.0 | 0.9692, 0.939, 0.784, 0.5803, 0.3534 |
| hf_px_pplus_float | V-1.0_A-0.5 | 0.9427, 0.9308, 0.8432, 0.6804, 0.4785 |
| hf_px_pplus_float | V-1.0_A+0.0 | 0.9142, 0.8996, 0.8589, 0.7316, 0.5515 |
| hf_px_pplus_float | V-1.0_A+0.5 | 0.8864, 0.8685, 0.8541, 0.7583, 0.597 |
| hf_px_pplus_float | V-1.0_A+1.0 | 0.8603, 0.8415, 0.8403, 0.7721, 0.6273 |
| hf_px_pplus_float | V-0.5_A-1.0 | 0.9826, 0.9513, 0.781, 0.5607, 0.3246 |
| hf_px_pplus_float | V-0.5_A-0.5 | 0.9648, 0.955, 0.8565, 0.6793, 0.4709 |
| hf_px_pplus_float | V-0.5_A+0.0 | 0.9435, 0.9305, 0.8828, 0.7453, 0.5627 |
| hf_px_pplus_float | V-0.5_A+0.5 | 0.9211, 0.9025, 0.8823, 0.7792, 0.6175 |
| hf_px_pplus_float | V-0.5_A+1.0 | 0.8987, 0.8765, 0.8693, 0.796, 0.652 |
| hf_px_pplus_float | V+0.0_A-1.0 | 0.9917, 0.9595, 0.7769, 0.5425, 0.2982 |
| hf_px_pplus_float | V+0.0_A-0.5 | 0.9818, 0.9747, 0.8653, 0.6701, 0.4505 |
| hf_px_pplus_float | V+0.0_A+0.0 | 0.9687, 0.9599, 0.9059, 0.7545, 0.5665 |
| hf_px_pplus_float | V+0.0_A+0.5 | 0.9536, 0.9389, 0.9139, 0.8004, 0.6377 |
| hf_px_pplus_float | V+0.0_A+1.0 | 0.9375, 0.9171, 0.9044, 0.8231, 0.6804 |
| hf_px_pplus_float | V+0.5_A-1.0 | 0.997, 0.9645, 0.776, 0.5344, 0.2864 |
| hf_px_pplus_float | V+0.5_A-0.5 | 0.9929, 0.9877, 0.8685, 0.655, 0.4215 |
| hf_px_pplus_float | V+0.5_A+0.0 | 0.987, 0.9828, 0.9237, 0.7551, 0.5558 |
| hf_px_pplus_float | V+0.5_A+0.5 | 0.9795, 0.9716, 0.9448, 0.818, 0.6515 |
| hf_px_pplus_float | V+0.5_A+1.0 | 0.971, 0.9583, 0.9438, 0.8515, 0.71 |
| hf_px_pplus_float | V+1.0_A-1.0 | 0.9994, 0.9678, 0.7827, 0.5422, 0.2926 |
| hf_px_pplus_float | V+1.0_A-0.5 | 0.9985, 0.9942, 0.8681, 0.6409, 0.397 |
| hf_px_pplus_float | V+1.0_A+0.0 | 0.9971, 0.996, 0.9321, 0.7453, 0.5291 |
| hf_px_pplus_float | V+1.0_A+0.5 | 0.9952, 0.9932, 0.9663, 0.8246, 0.6476 |
| hf_px_pplus_float | V+1.0_A+1.0 | 0.9928, 0.9892, 0.9777, 0.8741, 0.7305 |
| hf_px_pplus_float | V-1.0_A+0.25 | 0.9015, 0.8842, 0.8595, 0.7568, 0.585 |
| hf_px_pplus_float | V-0.5_A+0.25 | 0.9335, 0.917, 0.8863, 0.7756, 0.6021 |
| hf_px_pplus_float | V+0.0_A+0.25 | 0.9621, 0.95, 0.9145, 0.7927, 0.6157 |
| hf_px_pplus_float | V+0.5_A+0.25 | 0.9837, 0.9776, 0.9392, 0.8035, 0.6184 |
| hf_px_pplus_float | V+1.0_A+0.25 | 0.9963, 0.9945, 0.9539, 0.8027, 0.6022 |
| hf_px_pplus_float | sine_periodic | 0.9832, 0.982, 0.7158, 0.1434, 0.01259 |
| hf_px_pplus_float | sine_jump | 0.9812, 0.9791, 0.7933, 0.2229, 0.03246 |
| hf_px_pplus_float | flip_a | 0.9013, 0.981, 0.987, 0.9884, 0.9884 |
| hf_px_pplus_float | flip_b | 0.9999, 0.9998, 0.8327, 0.2081, 0.01996 |
| hf_px_pplus_linear_height | V-1.0_A-1.0 | 0.9999, 0.9073, 0.4158, 0.1261, 0.03207 |
| hf_px_pplus_linear_height | V-1.0_A-0.5 | 0.9998, 0.9888, 0.6286, 0.2221, 0.06463 |
| hf_px_pplus_linear_height | V-1.0_A+0.0 | 0.9997, 0.9991, 0.8019, 0.3309, 0.1064 |
| hf_px_pplus_linear_height | V-1.0_A+0.5 | 0.9996, 0.9998, 0.9121, 0.4424, 0.1542 |
| hf_px_pplus_linear_height | V-1.0_A+1.0 | 0.9991, 0.9996, 0.9671, 0.5506, 0.206 |
| hf_px_pplus_linear_height | V-0.5_A-1.0 | 0.9999, 0.9066, 0.4118, 0.1219, 0.02992 |
| hf_px_pplus_linear_height | V-0.5_A-0.5 | 0.9999, 0.9887, 0.6252, 0.2166, 0.06088 |
| hf_px_pplus_linear_height | V-0.5_A+0.0 | 0.9997, 0.9992, 0.8, 0.3255, 0.1017 |
| hf_px_pplus_linear_height | V-0.5_A+0.5 | 0.9997, 0.9998, 0.9113, 0.4378, 0.1493 |
| hf_px_pplus_linear_height | V-0.5_A+1.0 | 0.9992, 0.9996, 0.9668, 0.547, 0.2012 |
| hf_px_pplus_linear_height | V+0.0_A-1.0 | 1, 0.906, 0.4089, 0.1188, 0.02838 |
| hf_px_pplus_linear_height | V+0.0_A-0.5 | 0.9999, 0.9886, 0.622, 0.2113, 0.05742 |
| hf_px_pplus_linear_height | V+0.0_A+0.0 | 0.9998, 0.9992, 0.7981, 0.3201, 0.09708 |
| hf_px_pplus_linear_height | V+0.0_A+0.5 | 0.9997, 0.9998, 0.9104, 0.433, 0.1442 |
| hf_px_pplus_linear_height | V+0.0_A+1.0 | 0.9993, 0.9996, 0.9666, 0.5432, 0.1961 |
| hf_px_pplus_linear_height | V+0.5_A-1.0 | 1, 0.9059, 0.4083, 0.1177, 0.02779 |
| hf_px_pplus_linear_height | V+0.5_A-0.5 | 1, 0.9886, 0.6193, 0.2068, 0.05449 |
| hf_px_pplus_linear_height | V+0.5_A+0.0 | 0.9998, 0.9992, 0.7962, 0.3147, 0.09258 |
| hf_px_pplus_linear_height | V+0.5_A+0.5 | 0.9998, 0.9999, 0.9095, 0.4282, 0.139 |
| hf_px_pplus_linear_height | V+0.5_A+1.0 | 0.9993, 0.9997, 0.9662, 0.5392, 0.1909 |
| hf_px_pplus_linear_height | V+1.0_A-1.0 | 1, 0.9066, 0.4118, 0.12, 0.02862 |
| hf_px_pplus_linear_height | V+1.0_A-0.5 | 1, 0.9885, 0.6175, 0.2037, 0.05244 |
| hf_px_pplus_linear_height | V+1.0_A+0.0 | 0.9999, 0.9992, 0.7944, 0.3097, 0.08843 |
| hf_px_pplus_linear_height | V+1.0_A+0.5 | 0.9998, 0.9999, 0.9087, 0.4232, 0.1338 |
| hf_px_pplus_linear_height | V+1.0_A+1.0 | 0.9994, 0.9997, 0.9659, 0.5351, 0.1855 |
| hf_px_pplus_linear_height | V-1.0_A+0.25 | 0.9984, 0.9948, 0.8382, 0.3911, 0.1344 |
| hf_px_pplus_linear_height | V-0.5_A+0.25 | 0.9985, 0.9948, 0.8365, 0.386, 0.1295 |
| hf_px_pplus_linear_height | V+0.0_A+0.25 | 0.9985, 0.9948, 0.8349, 0.3807, 0.1244 |
| hf_px_pplus_linear_height | V+0.5_A+0.25 | 0.9985, 0.9947, 0.8332, 0.3754, 0.1194 |
| hf_px_pplus_linear_height | V+1.0_A+0.25 | 0.9986, 0.9947, 0.8315, 0.3702, 0.1145 |
| hf_px_pplus_linear_height | sine_periodic | 1, 0.999, 0.7242, 0.1434, 0.01259 |
| hf_px_pplus_linear_height | sine_jump | 0.9981, 0.9928, 0.7685, 0.1876, 0.01898 |
| hf_px_pplus_linear_height | flip_a | 0.8391, 0.2795, 0.1096, 0.09253, 0.09111 |
| hf_px_pplus_linear_height | flip_b | 0.9935, 0.9975, 0.8322, 0.2081, 0.01996 |
| hf_px_pplus_uint8 | V-1.0_A-1.0 | 0.9534, 0.9369, 0.784, 0.5803, 0.3535 |
| hf_px_pplus_uint8 | V-1.0_A-0.5 | 0.9409, 0.9306, 0.8431, 0.6803, 0.4784 |
| hf_px_pplus_uint8 | V-1.0_A+0.0 | 0.9141, 0.8996, 0.8588, 0.7315, 0.5514 |
| hf_px_pplus_uint8 | V-1.0_A+0.5 | 0.8864, 0.8684, 0.854, 0.7582, 0.5969 |
| hf_px_pplus_uint8 | V-1.0_A+1.0 | 0.8603, 0.8413, 0.8403, 0.772, 0.6272 |
| hf_px_pplus_uint8 | V-0.5_A-1.0 | 0.9375, 0.9527, 0.7811, 0.561, 0.325 |
| hf_px_pplus_uint8 | V-0.5_A-0.5 | 0.9565, 0.9517, 0.8562, 0.6792, 0.4709 |
| hf_px_pplus_uint8 | V-0.5_A+0.0 | 0.9408, 0.9303, 0.8826, 0.7452, 0.5626 |
| hf_px_pplus_uint8 | V-0.5_A+0.5 | 0.9207, 0.9023, 0.8822, 0.7791, 0.6174 |
| hf_px_pplus_uint8 | V-0.5_A+1.0 | 0.8985, 0.8764, 0.8692, 0.7959, 0.6519 |
| hf_px_pplus_uint8 | V+0.0_A-1.0 | 0.9197, 0.9455, 0.7769, 0.5435, 0.2996 |
| hf_px_pplus_uint8 | V+0.0_A-0.5 | 0.9397, 0.947, 0.8657, 0.6702, 0.4507 |
| hf_px_pplus_uint8 | V+0.0_A+0.0 | 0.9544, 0.9553, 0.9061, 0.7544, 0.5663 |
| hf_px_pplus_uint8 | V+0.0_A+0.5 | 0.9539, 0.9385, 0.9139, 0.8002, 0.6375 |
| hf_px_pplus_uint8 | V+0.0_A+1.0 | 0.9344, 0.917, 0.9042, 0.8229, 0.6802 |
| hf_px_pplus_uint8 | V+0.5_A-1.0 | 0.9101, 0.922, 0.7775, 0.5383, 0.2911 |
| hf_px_pplus_uint8 | V+0.5_A-0.5 | 0.9293, 0.9251, 0.8655, 0.6559, 0.4227 |
| hf_px_pplus_uint8 | V+0.5_A+0.0 | 0.9305, 0.9396, 0.9238, 0.7553, 0.5558 |
| hf_px_pplus_uint8 | V+0.5_A+0.5 | 0.9446, 0.9543, 0.9429, 0.8177, 0.6512 |
| hf_px_pplus_uint8 | V+0.5_A+1.0 | 0.9534, 0.9556, 0.9432, 0.8513, 0.7097 |
| hf_px_pplus_uint8 | V+1.0_A-1.0 | 0.9275, 0.8663, 0.7914, 0.5673, 0.3176 |
| hf_px_pplus_uint8 | V+1.0_A-0.5 | 0.9255, 0.8906, 0.8707, 0.6478, 0.4058 |
| hf_px_pplus_uint8 | V+1.0_A+0.0 | 0.9357, 0.928, 0.9357, 0.7481, 0.532 |
| hf_px_pplus_uint8 | V+1.0_A+0.5 | 0.9357, 0.9295, 0.9473, 0.825, 0.6482 |
| hf_px_pplus_uint8 | V+1.0_A+1.0 | 0.9293, 0.9309, 0.9492, 0.8726, 0.73 |
| hf_px_pplus_uint8 | V-1.0_A+0.25 | 0.9013, 0.884, 0.8595, 0.7567, 0.5849 |
| hf_px_pplus_uint8 | V-0.5_A+0.25 | 0.9333, 0.917, 0.8862, 0.7755, 0.6019 |
| hf_px_pplus_uint8 | V+0.0_A+0.25 | 0.9582, 0.9467, 0.9145, 0.7926, 0.6155 |
| hf_px_pplus_uint8 | V+0.5_A+0.25 | 0.9396, 0.9507, 0.9368, 0.8035, 0.6182 |
| hf_px_pplus_uint8 | V+1.0_A+0.25 | 0.9552, 0.947, 0.948, 0.8043, 0.6034 |
| hf_px_pplus_uint8 | sine_periodic | 0.9326, 0.9331, 0.7164, 0.1443, 0.0138 |
| hf_px_pplus_uint8 | sine_jump | 0.9409, 0.9464, 0.7938, 0.2235, 0.0334 |
| hf_px_pplus_uint8 | flip_a | 0.7374, 1, 1, 1, 1 |
| hf_px_pplus_uint8 | flip_b | 0.6467, 0.5333, 0.4288, 0.4557, 0.092 |
| hf_px_raw_float | V-1.0_A-1.0 | 0.9692, 0.939, 0.784, 0.5803, 0.3534 |
| hf_px_raw_float | V-1.0_A-0.5 | 0.9426, 0.9308, 0.8432, 0.6804, 0.4785 |
| hf_px_raw_float | V-1.0_A+0.0 | 0.9141, 0.8996, 0.8589, 0.7316, 0.5515 |
| hf_px_raw_float | V-1.0_A+0.5 | 0.8862, 0.8685, 0.8542, 0.7583, 0.597 |
| hf_px_raw_float | V-1.0_A+1.0 | 0.8601, 0.8415, 0.8404, 0.7721, 0.6273 |
| hf_px_raw_float | V-0.5_A-1.0 | 0.9825, 0.9513, 0.781, 0.5607, 0.3246 |
| hf_px_raw_float | V-0.5_A-0.5 | 0.9647, 0.955, 0.8565, 0.6793, 0.4709 |
| hf_px_raw_float | V-0.5_A+0.0 | 0.9434, 0.9305, 0.8828, 0.7453, 0.5627 |
| hf_px_raw_float | V-0.5_A+0.5 | 0.9209, 0.9025, 0.8823, 0.7792, 0.6175 |
| hf_px_raw_float | V-0.5_A+1.0 | 0.8985, 0.8765, 0.8694, 0.7961, 0.652 |
| hf_px_raw_float | V+0.0_A-1.0 | 0.9917, 0.9595, 0.7769, 0.5425, 0.2982 |
| hf_px_raw_float | V+0.0_A-0.5 | 0.9818, 0.9747, 0.8653, 0.67, 0.4504 |
| hf_px_raw_float | V+0.0_A+0.0 | 0.9687, 0.9599, 0.9059, 0.7545, 0.5665 |
| hf_px_raw_float | V+0.0_A+0.5 | 0.9535, 0.9388, 0.914, 0.8004, 0.6377 |
| hf_px_raw_float | V+0.0_A+1.0 | 0.9373, 0.9171, 0.9044, 0.8231, 0.6804 |
| hf_px_raw_float | V+0.5_A-1.0 | 0.997, 0.9645, 0.776, 0.5344, 0.2864 |
| hf_px_raw_float | V+0.5_A-0.5 | 0.9929, 0.9877, 0.8685, 0.655, 0.4215 |
| hf_px_raw_float | V+0.5_A+0.0 | 0.987, 0.9828, 0.9237, 0.7551, 0.5558 |
| hf_px_raw_float | V+0.5_A+0.5 | 0.9794, 0.9716, 0.9448, 0.818, 0.6515 |
| hf_px_raw_float | V+0.5_A+1.0 | 0.9709, 0.9582, 0.9438, 0.8515, 0.71 |
| hf_px_raw_float | V+1.0_A-1.0 | 0.9994, 0.9678, 0.7827, 0.5422, 0.2926 |
| hf_px_raw_float | V+1.0_A-0.5 | 0.9985, 0.9942, 0.8681, 0.6409, 0.397 |
| hf_px_raw_float | V+1.0_A+0.0 | 0.9971, 0.996, 0.9321, 0.7453, 0.5291 |
| hf_px_raw_float | V+1.0_A+0.5 | 0.9952, 0.9932, 0.9663, 0.8246, 0.6476 |
| hf_px_raw_float | V+1.0_A+1.0 | 0.9928, 0.9892, 0.9777, 0.8742, 0.7305 |
| hf_px_raw_float | V-1.0_A+0.25 | 0.9, 0.8833, 0.8574, 0.7527, 0.5805 |
| hf_px_raw_float | V-0.5_A+0.25 | 0.9322, 0.9161, 0.8839, 0.7712, 0.5974 |
| hf_px_raw_float | V+0.0_A+0.25 | 0.9612, 0.9492, 0.912, 0.788, 0.6108 |
| hf_px_raw_float | V+0.5_A+0.25 | 0.9833, 0.9771, 0.9367, 0.7986, 0.6135 |
| hf_px_raw_float | V+1.0_A+0.25 | 0.9962, 0.9943, 0.9514, 0.7976, 0.5972 |
| hf_px_raw_float | sine_periodic | 0.9832, 0.982, 0.7158, 0.1434, 0.01259 |
| hf_px_raw_float | sine_jump | 0.9799, 0.9775, 0.7913, 0.2336, 0.04216 |
| hf_px_raw_float | flip_a | 0.9013, 0.981, 0.987, 0.9884, 0.9884 |
| hf_px_raw_float | flip_b | 0.9999, 0.9998, 0.8327, 0.2081, 0.01996 |
| hf_px_raw_linear_height | V-1.0_A-1.0 | 1, 0.9073, 0.4158, 0.1261, 0.03206 |
| hf_px_raw_linear_height | V-1.0_A-0.5 | 1, 0.9889, 0.6286, 0.2221, 0.06463 |
| hf_px_raw_linear_height | V-1.0_A+0.0 | 1, 0.9993, 0.802, 0.3309, 0.1064 |
| hf_px_raw_linear_height | V-1.0_A+0.5 | 1, 1, 0.9121, 0.4424, 0.1542 |
| hf_px_raw_linear_height | V-1.0_A+1.0 | 1, 1, 0.9672, 0.5506, 0.206 |
| hf_px_raw_linear_height | V-0.5_A-1.0 | 1, 0.9066, 0.4118, 0.1219, 0.02991 |
| hf_px_raw_linear_height | V-0.5_A-0.5 | 1, 0.9888, 0.6252, 0.2166, 0.06088 |
| hf_px_raw_linear_height | V-0.5_A+0.0 | 1, 0.9993, 0.8001, 0.3255, 0.1017 |
| hf_px_raw_linear_height | V-0.5_A+0.5 | 1, 1, 0.9113, 0.4378, 0.1493 |
| hf_px_raw_linear_height | V-0.5_A+1.0 | 1, 1, 0.967, 0.547, 0.2012 |
| hf_px_raw_linear_height | V+0.0_A-1.0 | 1, 0.906, 0.4089, 0.1188, 0.02838 |
| hf_px_raw_linear_height | V+0.0_A-0.5 | 1, 0.9887, 0.622, 0.2113, 0.05742 |
| hf_px_raw_linear_height | V+0.0_A+0.0 | 1, 0.9993, 0.7981, 0.3201, 0.09708 |
| hf_px_raw_linear_height | V+0.0_A+0.5 | 1, 1, 0.9105, 0.433, 0.1442 |
| hf_px_raw_linear_height | V+0.0_A+1.0 | 1, 1, 0.9667, 0.5432, 0.1961 |
| hf_px_raw_linear_height | V+0.5_A-1.0 | 1, 0.9059, 0.4083, 0.1177, 0.02778 |
| hf_px_raw_linear_height | V+0.5_A-0.5 | 1, 0.9886, 0.6193, 0.2068, 0.05449 |
| hf_px_raw_linear_height | V+0.5_A+0.0 | 1, 0.9993, 0.7962, 0.3147, 0.09258 |
| hf_px_raw_linear_height | V+0.5_A+0.5 | 1, 1, 0.9096, 0.4281, 0.139 |
| hf_px_raw_linear_height | V+0.5_A+1.0 | 1, 1, 0.9663, 0.5393, 0.1909 |
| hf_px_raw_linear_height | V+1.0_A-1.0 | 1, 0.9066, 0.4118, 0.12, 0.02862 |
| hf_px_raw_linear_height | V+1.0_A-0.5 | 1, 0.9885, 0.6175, 0.2037, 0.05244 |
| hf_px_raw_linear_height | V+1.0_A+0.0 | 1, 0.9993, 0.7944, 0.3097, 0.08843 |
| hf_px_raw_linear_height | V+1.0_A+0.5 | 1, 1, 0.9087, 0.4232, 0.1338 |
| hf_px_raw_linear_height | V+1.0_A+1.0 | 1, 1, 0.966, 0.5352, 0.1855 |
| hf_px_raw_linear_height | V-1.0_A+0.25 | 0.9999, 0.9986, 0.8639, 0.4208, 0.1489 |
| hf_px_raw_linear_height | V-0.5_A+0.25 | 0.9999, 0.9986, 0.8626, 0.4161, 0.1442 |
| hf_px_raw_linear_height | V+0.0_A+0.25 | 0.9999, 0.9986, 0.8613, 0.4113, 0.1394 |
| hf_px_raw_linear_height | V+0.5_A+0.25 | 0.9999, 0.9986, 0.8599, 0.4065, 0.1346 |
| hf_px_raw_linear_height | V+1.0_A+0.25 | 0.9999, 0.9986, 0.8585, 0.4017, 0.13 |
| hf_px_raw_linear_height | sine_periodic | 1, 0.999, 0.7242, 0.1434, 0.01258 |
| hf_px_raw_linear_height | sine_jump | 0.9999, 0.998, 0.8083, 0.2398, 0.04493 |
| hf_px_raw_linear_height | flip_a | 0.848, 0.28, 0.1089, 0.09206, 0.09084 |
| hf_px_raw_linear_height | flip_b | 1, 0.9999, 0.8328, 0.2081, 0.01996 |
| hf_px_raw_uint8 | V-1.0_A-1.0 | 0.9534, 0.9369, 0.784, 0.5803, 0.3535 |
| hf_px_raw_uint8 | V-1.0_A-0.5 | 0.9408, 0.9306, 0.8431, 0.6803, 0.4784 |
| hf_px_raw_uint8 | V-1.0_A+0.0 | 0.914, 0.8996, 0.8588, 0.7315, 0.5514 |
| hf_px_raw_uint8 | V-1.0_A+0.5 | 0.8862, 0.8684, 0.8541, 0.7582, 0.5969 |
| hf_px_raw_uint8 | V-1.0_A+1.0 | 0.86, 0.8413, 0.8403, 0.772, 0.6272 |
| hf_px_raw_uint8 | V-0.5_A-1.0 | 0.9375, 0.9527, 0.7811, 0.561, 0.325 |
| hf_px_raw_uint8 | V-0.5_A-0.5 | 0.9566, 0.9517, 0.8562, 0.6792, 0.4709 |
| hf_px_raw_uint8 | V-0.5_A+0.0 | 0.9406, 0.9303, 0.8826, 0.7452, 0.5626 |
| hf_px_raw_uint8 | V-0.5_A+0.5 | 0.9205, 0.9023, 0.8822, 0.7791, 0.6174 |
| hf_px_raw_uint8 | V-0.5_A+1.0 | 0.8983, 0.8763, 0.8692, 0.7959, 0.6519 |
| hf_px_raw_uint8 | V+0.0_A-1.0 | 0.9193, 0.9455, 0.7769, 0.5435, 0.2996 |
| hf_px_raw_uint8 | V+0.0_A-0.5 | 0.94, 0.9471, 0.8657, 0.6702, 0.4507 |
| hf_px_raw_uint8 | V+0.0_A+0.0 | 0.9546, 0.9553, 0.9061, 0.7544, 0.5663 |
| hf_px_raw_uint8 | V+0.0_A+0.5 | 0.9538, 0.9384, 0.9139, 0.8002, 0.6375 |
| hf_px_raw_uint8 | V+0.0_A+1.0 | 0.9345, 0.917, 0.9042, 0.8229, 0.6802 |
| hf_px_raw_uint8 | V+0.5_A-1.0 | 0.9099, 0.9219, 0.7775, 0.5383, 0.291 |
| hf_px_raw_uint8 | V+0.5_A-0.5 | 0.9317, 0.9252, 0.8655, 0.6559, 0.4227 |
| hf_px_raw_uint8 | V+0.5_A+0.0 | 0.931, 0.9397, 0.9238, 0.7553, 0.5558 |
| hf_px_raw_uint8 | V+0.5_A+0.5 | 0.945, 0.9544, 0.9429, 0.8177, 0.6512 |
| hf_px_raw_uint8 | V+0.5_A+1.0 | 0.9539, 0.9556, 0.9432, 0.8513, 0.7097 |
| hf_px_raw_uint8 | V+1.0_A-1.0 | 0.9243, 0.8664, 0.7914, 0.5673, 0.3176 |
| hf_px_raw_uint8 | V+1.0_A-0.5 | 0.9311, 0.8912, 0.8708, 0.6478, 0.4058 |
| hf_px_raw_uint8 | V+1.0_A+0.0 | 0.9347, 0.9275, 0.9357, 0.7481, 0.532 |
| hf_px_raw_uint8 | V+1.0_A+0.5 | 0.937, 0.9294, 0.9473, 0.825, 0.6482 |
| hf_px_raw_uint8 | V+1.0_A+1.0 | 0.9317, 0.9313, 0.9492, 0.8726, 0.7301 |
| hf_px_raw_uint8 | V-1.0_A+0.25 | 0.8998, 0.8831, 0.8573, 0.7526, 0.5804 |
| hf_px_raw_uint8 | V-0.5_A+0.25 | 0.9323, 0.9161, 0.8838, 0.7711, 0.5973 |
| hf_px_raw_uint8 | V+0.0_A+0.25 | 0.9585, 0.9458, 0.912, 0.7879, 0.6106 |
| hf_px_raw_uint8 | V+0.5_A+0.25 | 0.9416, 0.9497, 0.9342, 0.7986, 0.6132 |
| hf_px_raw_uint8 | V+1.0_A+0.25 | 0.9542, 0.936, 0.9461, 0.7991, 0.5983 |
| hf_px_raw_uint8 | sine_periodic | 0.9326, 0.9331, 0.7164, 0.1443, 0.0138 |
| hf_px_raw_uint8 | sine_jump | 0.9436, 0.9414, 0.7911, 0.234, 0.04298 |
| hf_px_raw_uint8 | flip_a | 0.6447, 1, 1, 1, 1 |
| hf_px_raw_uint8 | flip_b | 0.6467, 0.5333, 0.4212, 0.4541, 0.0919 |
| sq_hann | V-1.0_A-1.0 | 0.04704, 0.04704, 0.04704, 0.04704, 0.04704 |
| sq_hann | V-1.0_A-0.5 | 0.05244, 0.05244, 0.05244, 0.05244, 0.05244 |
| sq_hann | V-1.0_A+0.0 | 0.05703, 0.05703, 0.05703, 0.05703, 0.05703 |
| sq_hann | V-1.0_A+0.5 | 0.06097, 0.06097, 0.06097, 0.06097, 0.06097 |
| sq_hann | V-1.0_A+1.0 | 0.06439, 0.06439, 0.06439, 0.06439, 0.06439 |
| sq_hann | V-0.5_A-1.0 | 0.03497, 0.03497, 0.03497, 0.03497, 0.03497 |
| sq_hann | V-0.5_A-0.5 | 0.03972, 0.03972, 0.03972, 0.03972, 0.03972 |
| sq_hann | V-0.5_A+0.0 | 0.04372, 0.04372, 0.04372, 0.04372, 0.04372 |
| sq_hann | V-0.5_A+0.5 | 0.04714, 0.04714, 0.04714, 0.04714, 0.04714 |
| sq_hann | V-0.5_A+1.0 | 0.05009, 0.05009, 0.05009, 0.05009, 0.05009 |
| sq_hann | V+0.0_A-1.0 | 0.02403, 0.02403, 0.02403, 0.02403, 0.02403 |
| sq_hann | V+0.0_A-0.5 | 0.02795, 0.02795, 0.02795, 0.02795, 0.02795 |
| sq_hann | V+0.0_A+0.0 | 0.03123, 0.03123, 0.03123, 0.03123, 0.03123 |
| sq_hann | V+0.0_A+0.5 | 0.03402, 0.03402, 0.03402, 0.03402, 0.03402 |
| sq_hann | V+0.0_A+1.0 | 0.03641, 0.03641, 0.03641, 0.03641, 0.03641 |
| sq_hann | V+0.5_A-1.0 | 0.0144, 0.0144, 0.0144, 0.0144, 0.0144 |
| sq_hann | V+0.5_A-0.5 | 0.01729, 0.01729, 0.01729, 0.01729, 0.01729 |
| sq_hann | V+0.5_A+0.0 | 0.01969, 0.01969, 0.01969, 0.01969, 0.01969 |
| sq_hann | V+0.5_A+0.5 | 0.02172, 0.02172, 0.02172, 0.02172, 0.02172 |
| sq_hann | V+0.5_A+1.0 | 0.02345, 0.02345, 0.02345, 0.02345, 0.02345 |
| sq_hann | V+1.0_A-1.0 | 0.006299, 0.006299, 0.006299, 0.006299, 0.006299 |
| sq_hann | V+1.0_A-0.5 | 0.007899, 0.007899, 0.007899, 0.007899, 0.007899 |
| sq_hann | V+1.0_A+0.0 | 0.009224, 0.009224, 0.009224, 0.009224, 0.009224 |
| sq_hann | V+1.0_A+0.5 | 0.01033, 0.01033, 0.01033, 0.01033, 0.01033 |
| sq_hann | V+1.0_A+1.0 | 0.01127, 0.01127, 0.01127, 0.01127, 0.01127 |
| sq_hann | V-1.0_A+0.25 | 0.05907, 0.05907, 0.05907, 0.05907, 0.05907 |
| sq_hann | V-0.5_A+0.25 | 0.04549, 0.04549, 0.04549, 0.04549, 0.04549 |
| sq_hann | V+0.0_A+0.25 | 0.03268, 0.03268, 0.03268, 0.03268, 0.03268 |
| sq_hann | V+0.5_A+0.25 | 0.02074, 0.02074, 0.02074, 0.02074, 0.02074 |
| sq_hann | V+1.0_A+0.25 | 0.009802, 0.009802, 0.009802, 0.009802, 0.009802 |
| sq_hann | sine_periodic | 0.03375, 0.03375, 0.03375, 0.03375, 0.03375 |
| sq_hann | sine_jump | 0.03375, 0.03375, 0.03375, 0.03375, 0.03375 |
| sq_hann | flip_a | 3.283e-05, 3.283e-05, 3.283e-05, 3.283e-05, 3.283e-05 |
| sq_hann | flip_b | 7.46e-05, 7.46e-05, 7.46e-05, 7.46e-05, 7.46e-05 |
| sq_pplus | V-1.0_A-1.0 | 0.1245, 0.1249, 0.1252, 0.1253, 0.1254 |
| sq_pplus | V-1.0_A-0.5 | 0.1387, 0.1393, 0.1395, 0.1397, 0.1398 |
| sq_pplus | V-1.0_A+0.0 | 0.151, 0.1515, 0.1518, 0.1519, 0.152 |
| sq_pplus | V-1.0_A+0.5 | 0.1615, 0.162, 0.1623, 0.1624, 0.1625 |
| sq_pplus | V-1.0_A+1.0 | 0.1707, 0.1711, 0.1714, 0.1715, 0.1716 |
| sq_pplus | V-0.5_A-1.0 | 0.09257, 0.0929, 0.09308, 0.09317, 0.09321 |
| sq_pplus | V-0.5_A-0.5 | 0.1051, 0.1055, 0.1057, 0.1058, 0.1058 |
| sq_pplus | V-0.5_A+0.0 | 0.1158, 0.1161, 0.1164, 0.1165, 0.1165 |
| sq_pplus | V-0.5_A+0.5 | 0.1248, 0.1252, 0.1255, 0.1256, 0.1256 |
| sq_pplus | V-0.5_A+1.0 | 0.1328, 0.1331, 0.1333, 0.1334, 0.1335 |
| sq_pplus | V+0.0_A-1.0 | 0.06361, 0.06384, 0.06396, 0.06402, 0.06405 |
| sq_pplus | V+0.0_A-0.5 | 0.07393, 0.07422, 0.07437, 0.07445, 0.07449 |
| sq_pplus | V+0.0_A+0.0 | 0.08271, 0.08298, 0.08313, 0.08321, 0.08325 |
| sq_pplus | V+0.0_A+0.5 | 0.0901, 0.0904, 0.09055, 0.09064, 0.09068 |
| sq_pplus | V+0.0_A+1.0 | 0.09653, 0.09677, 0.09692, 0.09701, 0.09705 |
| sq_pplus | V+0.5_A-1.0 | 0.03811, 0.03825, 0.03832, 0.03836, 0.03838 |
| sq_pplus | V+0.5_A-0.5 | 0.04572, 0.0459, 0.046, 0.04604, 0.04607 |
| sq_pplus | V+0.5_A+0.0 | 0.05214, 0.05231, 0.0524, 0.05245, 0.05248 |
| sq_pplus | V+0.5_A+0.5 | 0.05751, 0.0577, 0.0578, 0.05786, 0.05788 |
| sq_pplus | V+0.5_A+1.0 | 0.06215, 0.06231, 0.06241, 0.06246, 0.06249 |
| sq_pplus | V+1.0_A-1.0 | 0.01667, 0.01673, 0.01677, 0.01678, 0.01679 |
| sq_pplus | V+1.0_A-0.5 | 0.0209, 0.02098, 0.02102, 0.02104, 0.02105 |
| sq_pplus | V+1.0_A+0.0 | 0.02442, 0.0245, 0.02455, 0.02457, 0.02459 |
| sq_pplus | V+1.0_A+0.5 | 0.02736, 0.02745, 0.0275, 0.02753, 0.02754 |
| sq_pplus | V+1.0_A+1.0 | 0.02988, 0.02996, 0.03001, 0.03003, 0.03005 |
| sq_pplus | V-1.0_A+0.25 | 0.1543, 0.1544, 0.1544, 0.1545, 0.1545 |
| sq_pplus | V-0.5_A+0.25 | 0.1188, 0.1189, 0.1189, 0.1189, 0.1189 |
| sq_pplus | V+0.0_A+0.25 | 0.08533, 0.08538, 0.08541, 0.08543, 0.08544 |
| sq_pplus | V+0.5_A+0.25 | 0.05415, 0.05418, 0.0542, 0.05421, 0.05422 |
| sq_pplus | V+1.0_A+0.25 | 0.02558, 0.0256, 0.02561, 0.02561, 0.02561 |
| sq_pplus | sine_periodic | 0.08935, 0.08966, 0.08983, 0.08991, 0.08996 |
| sq_pplus | sine_jump | 0.08756, 0.08755, 0.08755, 0.08755, 0.08755 |
| sq_pplus | flip_a | 9.024e-05, 8.803e-05, 8.728e-05, 8.728e-05, 8.738e-05 |
| sq_pplus | flip_b | 0.0001987, 0.0001985, 0.0001986, 0.0001988, 0.0001989 |
| sq_raw | V-1.0_A-1.0 | 0.1254, 0.1254, 0.1254, 0.1254, 0.1254 |
| sq_raw | V-1.0_A-0.5 | 0.1398, 0.1398, 0.1398, 0.1398, 0.1398 |
| sq_raw | V-1.0_A+0.0 | 0.1521, 0.1521, 0.1521, 0.1521, 0.1521 |
| sq_raw | V-1.0_A+0.5 | 0.1626, 0.1626, 0.1626, 0.1626, 0.1626 |
| sq_raw | V-1.0_A+1.0 | 0.1717, 0.1717, 0.1717, 0.1717, 0.1717 |
| sq_raw | V-0.5_A-1.0 | 0.09326, 0.09326, 0.09326, 0.09326, 0.09326 |
| sq_raw | V-0.5_A-0.5 | 0.1059, 0.1059, 0.1059, 0.1059, 0.1059 |
| sq_raw | V-0.5_A+0.0 | 0.1166, 0.1166, 0.1166, 0.1166, 0.1166 |
| sq_raw | V-0.5_A+0.5 | 0.1257, 0.1257, 0.1257, 0.1257, 0.1257 |
| sq_raw | V-0.5_A+1.0 | 0.1336, 0.1336, 0.1336, 0.1336, 0.1336 |
| sq_raw | V+0.0_A-1.0 | 0.06408, 0.06408, 0.06408, 0.06408, 0.06408 |
| sq_raw | V+0.0_A-0.5 | 0.07453, 0.07453, 0.07453, 0.07453, 0.07453 |
| sq_raw | V+0.0_A+0.0 | 0.08329, 0.08329, 0.08329, 0.08329, 0.08329 |
| sq_raw | V+0.0_A+0.5 | 0.09072, 0.09072, 0.09072, 0.09072, 0.09072 |
| sq_raw | V+0.0_A+1.0 | 0.0971, 0.0971, 0.0971, 0.0971, 0.0971 |
| sq_raw | V+0.5_A-1.0 | 0.0384, 0.0384, 0.0384, 0.0384, 0.0384 |
| sq_raw | V+0.5_A-0.5 | 0.0461, 0.04609, 0.04609, 0.04609, 0.04609 |
| sq_raw | V+0.5_A+0.0 | 0.05251, 0.05251, 0.05251, 0.05251, 0.05251 |
| sq_raw | V+0.5_A+0.5 | 0.05791, 0.05791, 0.05791, 0.05791, 0.05791 |
| sq_raw | V+0.5_A+1.0 | 0.06252, 0.06252, 0.06252, 0.06252, 0.06252 |
| sq_raw | V+1.0_A-1.0 | 0.0168, 0.0168, 0.0168, 0.0168, 0.0168 |
| sq_raw | V+1.0_A-0.5 | 0.02107, 0.02107, 0.02107, 0.02107, 0.02107 |
| sq_raw | V+1.0_A+0.0 | 0.0246, 0.0246, 0.0246, 0.0246, 0.0246 |
| sq_raw | V+1.0_A+0.5 | 0.02756, 0.02756, 0.02756, 0.02756, 0.02756 |
| sq_raw | V+1.0_A+1.0 | 0.03006, 0.03006, 0.03006, 0.03006, 0.03006 |
| sq_raw | V-1.0_A+0.25 | 0.1575, 0.1575, 0.1575, 0.1575, 0.1575 |
| sq_raw | V-0.5_A+0.25 | 0.1213, 0.1213, 0.1213, 0.1213, 0.1213 |
| sq_raw | V+0.0_A+0.25 | 0.08715, 0.08715, 0.08715, 0.08715, 0.08715 |
| sq_raw | V+0.5_A+0.25 | 0.05532, 0.05532, 0.05532, 0.05532, 0.05532 |
| sq_raw | V+1.0_A+0.25 | 0.02614, 0.02614, 0.02614, 0.02614, 0.02614 |
| sq_raw | sine_periodic | 0.09, 0.09, 0.09, 0.09, 0.09 |
| sq_raw | sine_jump | 0.09, 0.09, 0.09, 0.09, 0.09 |
| sq_raw | flip_a | 8.755e-05, 8.755e-05, 8.755e-05, 8.755e-05, 8.755e-05 |
| sq_raw | flip_b | 0.0001989, 0.0001989, 0.0001989, 0.0001989, 0.0001989 |
