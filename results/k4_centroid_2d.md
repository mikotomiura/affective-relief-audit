# K4 in two dimensions: growth of the frequency centroid with the grid size

Conditions: `experiments/conditions/k4_centroid_2d.json` (SHA-256 `376a638cf326d0d0a4eaf2991b6905610e925d598f3349a57e1d389edf5c00f8`). Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`). numpy 2.5.4, scipy 1.18.1, Python 3.13.12. Run started 2026-10-25T02:24:47+00:00 and finished 2026-10-25T02:56:24+00:00 (Darwin arm64, 10 logical CPUs).

Nothing here is a proof. The intervals are over seeds and do not include the systematic bias of a finite N range; local slopes and the log-corrected fit are reported for that reason.

## Reading of the conditions fixed before the run

- Decision rule of the rejection criterion: the decision ('rejected' if at least one adjusted interval excludes e(gamma), 'consistent' if all contain it) is made separately on the primary range (N 512-4096) and on the sensitivity range (N 1024-4096). If the two agree, that is the outcome; if they differ, the outcome is 'not decidable in this N range'. The decision on the primary range alone is reported beside it. (The condition file states the 'rejected' rule on the primary range and the 'not decidable' rule for differing decisions; the two overlap when only the primary range rejects. This reading was fixed before the computation.)
- oned: the height is T_gamma of the sine (no normalisation; the centroid is scale-invariant). 'hann' for oned is the one-dimensional window w(i) = sin^2(pi i/N) (the analogue of S3.1), and centroid_power and centroid_band_power for oned use |k| in place of rho (the analogue of S2.4). Only the raw centroid_amp of oned enters a prediction (P-K4-1).
- Aliasing subset: the fine array is H = T_gamma(F) on the grid of side rN with the same seed and window (F with maxabs normalisation over the fine grid; the centroid does not depend on the normalisation constant), reduced to side N by decimate_fourier; both processings and all three descriptors are computed on the reduced array.
- Operational criteria for the predictions (the condition file states directions; the thresholds below were fixed in this script before the computation): 'close to' an exponent means within 0.05 of it; 'the local slope tends to 0' means that the magnitude of the mean local slope between the two largest N is below 0.05 and below its magnitude between the two smallest N; 'does not depend on N' means that the relative range over N of every seed is at most 1e-09. Slopes are those of the primary range (N 512-4096) with 95% t intervals over seeds unless stated otherwise.
- Fields covered by the predictions that do not name one: P-K4-5, P-K4-6 and P-K4-7 are decided on sum and product1 (two-dimensional fields, the subject of K4 (c) and (d)); oned is reported in the tables but not decided. P-K4-2 is decided against 1 - 1/gamma as written (negative at gamma = 0.9); whether the slope is also within the tolerance of max(0, 1 - 1/gamma), the value implied by P-K4-1, is reported beside it.
- The secondary analysis on the decimate_fourier version uses the same simultaneous level as the main criterion (1 - 0.05/12), since it repeats a subset of the same 12 cells.

## Rejection criterion (12 cells)

Simultaneous intervals: Bonferroni, level 1 - 0.05/12 = 0.99583, t over 20 seeds.

- Decision on the primary range (N 512-4096): **rejected**
- Decision on the sensitivity range (N 1024-4096): **rejected**
- Outcome: **rejected**

| range | f | gamma | e(gamma) | slope | adjusted interval | contains e | direction |
|---|---|---|---|---|---|---|---|
| primary | 3 | 0.9 | 0.3889 | 0.3035 | [0.2959, 0.3111] | no | below |
| primary | 3 | 1.25 | 0.7000 | 0.6285 | [0.6252, 0.6319] | no | below |
| primary | 3 | 1.75 | 0.9286 | 0.8145 | [0.8136, 0.8153] | no | below |
| primary | 3 | 2.6 | 1.0000 | 0.9045 | [0.9032, 0.9058] | no | below |
| primary | 5 | 0.9 | 0.3889 | 0.2942 | [0.2859, 0.3025] | no | below |
| primary | 5 | 1.25 | 0.7000 | 0.6181 | [0.6137, 0.6226] | no | below |
| primary | 5 | 1.75 | 0.9286 | 0.8112 | [0.8099, 0.8124] | no | below |
| primary | 5 | 2.6 | 1.0000 | 0.9032 | [0.9018, 0.9045] | no | below |
| primary | 7 | 0.9 | 0.3889 | 0.2873 | [0.2785, 0.2962] | no | below |
| primary | 7 | 1.25 | 0.7000 | 0.6096 | [0.6043, 0.6149] | no | below |
| primary | 7 | 1.75 | 0.9286 | 0.8084 | [0.8067, 0.8101] | no | below |
| primary | 7 | 2.6 | 1.0000 | 0.9021 | [0.9008, 0.9035] | no | below |
| sensitivity | 3 | 0.9 | 0.3889 | 0.3124 | [0.3054, 0.3194] | no | below |
| sensitivity | 3 | 1.25 | 0.7000 | 0.6408 | [0.6383, 0.6433] | no | below |
| sensitivity | 3 | 1.75 | 0.9286 | 0.8236 | [0.8228, 0.8244] | no | below |
| sensitivity | 3 | 2.6 | 1.0000 | 0.9123 | [0.9111, 0.9136] | no | below |
| sensitivity | 5 | 0.9 | 0.3889 | 0.3037 | [0.2960, 0.3114] | no | below |
| sensitivity | 5 | 1.25 | 0.7000 | 0.6325 | [0.6291, 0.6359] | no | below |
| sensitivity | 5 | 1.75 | 0.9286 | 0.8214 | [0.8206, 0.8222] | no | below |
| sensitivity | 5 | 2.6 | 1.0000 | 0.9115 | [0.9104, 0.9127] | no | below |
| sensitivity | 7 | 0.9 | 0.3889 | 0.2971 | [0.2889, 0.3053] | no | below |
| sensitivity | 7 | 1.25 | 0.7000 | 0.6255 | [0.6214, 0.6296] | no | below |
| sensitivity | 7 | 1.75 | 0.9286 | 0.8193 | [0.8183, 0.8203] | no | below |
| sensitivity | 7 | 2.6 | 1.0000 | 0.9108 | [0.9097, 0.9119] | no | below |

### Local slopes and log-corrected fit for the 12 cells (raw, centroid_amp, direct sampling)

Local slopes are the means over seeds between consecutive N (128-256, ..., 2048-4096). The log-corrected fit is ln C = a + b ln N + c ln ln N over N 256-4096 (descriptive; mean and 95% interval over seeds).

| f | gamma | local slopes | b | c |
|---|---|---|---|---|
| 3 | 0.9 | 0.241, 0.264, 0.285, 0.304, 0.320 | 0.481 [0.478, 0.484] | -1.284 [-1.338, -1.230] |
| 3 | 1.25 | 0.514, 0.564, 0.603, 0.631, 0.651 | 0.898 [0.888, 0.909] | -1.955 [-2.047, -1.863] |
| 3 | 1.75 | 0.728, 0.766, 0.796, 0.816, 0.831 | 1.016 [1.007, 1.024] | -1.456 [-1.520, -1.392] |
| 3 | 2.6 | 0.834, 0.864, 0.888, 0.906, 0.919 | 1.074 [1.068, 1.080] | -1.227 [-1.273, -1.181] |
| 5 | 0.9 | 0.238, 0.254, 0.275, 0.295, 0.312 | 0.478 [0.475, 0.480] | -1.326 [-1.379, -1.274] |
| 5 | 1.25 | 0.496, 0.545, 0.588, 0.621, 0.644 | 0.927 [0.915, 0.938] | -2.233 [-2.336, -2.129] |
| 5 | 1.75 | 0.722, 0.759, 0.790, 0.813, 0.829 | 1.030 [1.020, 1.040] | -1.585 [-1.660, -1.509] |
| 5 | 2.6 | 0.832, 0.862, 0.886, 0.905, 0.918 | 1.080 [1.074, 1.086] | -1.279 [-1.326, -1.232] |
| 7 | 0.9 | 0.246, 0.248, 0.268, 0.288, 0.306 | 0.469 [0.467, 0.472] | -1.315 [-1.367, -1.263] |
| 7 | 1.25 | 0.492, 0.532, 0.577, 0.613, 0.638 | 0.943 [0.931, 0.956] | -2.416 [-2.530, -2.302] |
| 7 | 1.75 | 0.725, 0.754, 0.786, 0.810, 0.828 | 1.039 [1.027, 1.051] | -1.672 [-1.766, -1.579] |
| 7 | 2.6 | 0.836, 0.860, 0.884, 0.904, 0.918 | 1.084 [1.075, 1.092] | -1.315 [-1.379, -1.251] |

### Secondary analysis on the decimate_fourier version (f = 5, r = 2, seeds 1-10)

- decimate_fourier: primary rejected, sensitivity rejected, outcome rejected
- direct sampling, same cells and seeds: primary rejected, sensitivity rejected, outcome rejected

| sampling | range | gamma | slope | adjusted interval | contains e |
|---|---|---|---|---|---|
| decimate r=2 | primary | 0.9 | 0.2731 | [0.2573, 0.2889] | no |
| decimate r=2 | primary | 1.25 | 0.5787 | [0.5697, 0.5877] | no |
| decimate r=2 | primary | 1.75 | 0.7718 | [0.7693, 0.7742] | no |
| decimate r=2 | primary | 2.6 | 0.8689 | [0.8659, 0.8719] | no |
| decimate r=2 | sensitivity | 0.9 | 0.2852 | [0.2702, 0.3002] | no |
| decimate r=2 | sensitivity | 1.25 | 0.6003 | [0.5932, 0.6073] | no |
| decimate r=2 | sensitivity | 1.75 | 0.7887 | [0.7871, 0.7902] | no |
| decimate r=2 | sensitivity | 2.6 | 0.8831 | [0.8803, 0.8859] | no |
| direct | primary | 0.9 | 0.2945 | [0.2796, 0.3095] | no |
| direct | primary | 1.25 | 0.6186 | [0.6113, 0.6259] | no |
| direct | primary | 1.75 | 0.8116 | [0.8101, 0.8131] | no |
| direct | primary | 2.6 | 0.9037 | [0.9015, 0.9059] | no |
| direct | sensitivity | 0.9 | 0.3039 | [0.2900, 0.3179] | no |
| direct | sensitivity | 1.25 | 0.6327 | [0.6270, 0.6385] | no |
| direct | sensitivity | 1.75 | 0.8216 | [0.8205, 0.8226] | no |
| direct | sensitivity | 2.6 | 0.9119 | [0.9100, 0.9137] | no |

## Conclusions by prediction (written after the run)

This section was written by the author after reading the tables below; it is not produced by `--report`. The decisions follow the criteria fixed before the run, also where they fail for reasons stated here; no criterion was changed after the run.

- **Rejection criterion: rejected.** Every one of the 12 cells, on both the primary range (N 512-4096) and the sensitivity range (N 1024-4096), has a Bonferroni interval entirely below e(gamma) = min(1, 1.5 - 1/gamma) (for example f = 5: 0.294 against 0.389 at gamma = 0.9, 0.903 against 1 at gamma = 2.6). The decimate_fourier version (f = 5, r = 2) gives the same decision with lower slopes. What is withdrawn, as the condition file states, is the estimate min(1, 1.5 - 1/gamma) as the slope over these N ranges; the one-dimensional results of Appendix A are not affected. The local slopes increase with N in every cell (for example f = 5, gamma = 0.9: 0.238, 0.254, 0.275, 0.295, 0.312; gamma = 2.6: 0.832 to 0.918), so the slopes over a finite range lie below the slope at larger N, and this result does not settle the exponent as N tends to infinity. The log-corrected fit is unstable (in the 12 cells, b between 0.47 and 1.08 with c between -1.2 and -2.4) and is not used for a conclusion.
- **P-K4-1 holds** (15 of 15): the one-dimensional control behaves as proved.
- **P-K4-2 holds in 9 of 12 items.** The three items at gamma = 0.9 do not hold: the product1 slopes are 0.055-0.063, neither close to 1 - 1/gamma = -0.111 (the target as written) nor within 0.05 of 0. Their local slopes decrease with N (f = 3: 0.078 to 0.050), as the one-dimensional slopes do (0.043-0.049 over the primary range).
- **P-K4-3 holds** (12 of 12): the sum-field slopes exceed the one-dimensional value and are positive at gamma = 0.9 (0.287-0.304).
- **P-K4-4 does not hold as operationalised** (0 of 6), although the centroid is constant to within a relative range of 9.1e-11 over N 128-4096 in every item, which meets the 1e-9 tolerance. The second condition, a slope interval containing 0, fails because the values drift systematically by floating-point rounding (slopes 5e-12 to 2e-11 with intervals narrower than the drift). The power-weighted and band-fixed centroids of the same cells are constant to 6e-16.
- **P-K4-5 holds** (6 of 6).
- **P-K4-6 holds in 25 of 30 items.** For sum with gamma >= 1.75, three items have a hann slope not smaller than the raw slope (f = 3.5 and 5.5) and two have a hann slope that does not approach the integer-f value (f = 6.3).
- **P-K4-7 holds in 61 of 66 items.** Three failures (gamma = 1, integer f) are an artefact of the criterion: the power-weighted centroid is constant to rounding (local slopes of order 1e-16), and the strict inequality 'last local slope smaller than the first' then compares rounding noise. Two failures are real for the stated criterion: for sum at gamma = 2.6 and f = 5.5 and 6.3, the increments per unit ln N fall by more than a factor 2 (0.93 to 0.37 and 1.17 to 0.42).
- Implementation control: maxabs and ampsum agree to 1.6e-13.

## Predictions

### P-K4-1: 15 of 15 items hold

Prediction: P-K4-1 (one-dimensional control, Appendix A): for oned, integer f, raw, the slope approaches 1 - 1/gamma for gamma > 1 and is 0 at gamma = 1. For gamma = 0.9 the centroid converges (proved): the local slope tends to 0 (it is not 1 - 1/gamma, which would be negative).

| f | gamma | target | slope | lo | hi | local_last | holds |
|---|---|---|---|---|---|---|---|
| 3 | 0.900 | 0.000 | 0.043 | 0.043 | 0.044 | 0.039 | yes |
| 3 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | yes |
| 3 | 1.250 | 0.200 | 0.200 | 0.198 | 0.203 | 0.204 | yes |
| 3 | 1.750 | 0.429 | 0.426 | 0.421 | 0.431 | 0.435 | yes |
| 3 | 2.600 | 0.615 | 0.601 | 0.595 | 0.606 | 0.614 | yes |
| 5 | 0.900 | 0.000 | 0.046 | 0.046 | 0.047 | 0.042 | yes |
| 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | yes |
| 5 | 1.250 | 0.200 | 0.200 | 0.198 | 0.201 | 0.203 | yes |
| 5 | 1.750 | 0.429 | 0.425 | 0.422 | 0.428 | 0.432 | yes |
| 5 | 2.600 | 0.615 | 0.600 | 0.596 | 0.604 | 0.611 | yes |
| 7 | 0.900 | 0.000 | 0.049 | 0.048 | 0.049 | 0.044 | yes |
| 7 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | yes |
| 7 | 1.250 | 0.200 | 0.200 | 0.199 | 0.201 | 0.202 | yes |
| 7 | 1.750 | 0.429 | 0.425 | 0.422 | 0.427 | 0.431 | yes |
| 7 | 2.600 | 0.615 | 0.599 | 0.596 | 0.603 | 0.609 | yes |

### P-K4-2: 9 of 12 items hold

Prediction: P-K4-2 (product control): for product1 with integer f the slope is close to the one-dimensional exponent 1 - 1/gamma (straight zero lines).

| f | gamma | target | slope | lo | hi | oned_slope | within_tol_of_max(0,target) | holds |
|---|---|---|---|---|---|---|---|---|
| 3 | 0.900 | -0.111 | 0.055 | 0.055 | 0.056 | 0.043 | False | no |
| 3 | 1.250 | 0.200 | 0.229 | 0.228 | 0.231 | 0.200 | True | yes |
| 3 | 1.750 | 0.429 | 0.453 | 0.449 | 0.456 | 0.426 | True | yes |
| 3 | 2.600 | 0.615 | 0.624 | 0.620 | 0.628 | 0.601 | True | yes |
| 5 | 0.900 | -0.111 | 0.060 | 0.060 | 0.060 | 0.046 | False | no |
| 5 | 1.250 | 0.200 | 0.233 | 0.231 | 0.234 | 0.200 | True | yes |
| 5 | 1.750 | 0.429 | 0.458 | 0.455 | 0.460 | 0.425 | True | yes |
| 5 | 2.600 | 0.615 | 0.629 | 0.626 | 0.632 | 0.600 | True | yes |
| 7 | 0.900 | -0.111 | 0.063 | 0.063 | 0.063 | 0.049 | False | no |
| 7 | 1.250 | 0.200 | 0.235 | 0.234 | 0.236 | 0.200 | True | yes |
| 7 | 1.750 | 0.429 | 0.461 | 0.460 | 0.463 | 0.425 | True | yes |
| 7 | 2.600 | 0.615 | 0.633 | 0.631 | 0.635 | 0.599 | True | yes |

### P-K4-3: 12 of 12 items hold

Prediction: P-K4-3 (sum field, conjecture; gamma != 1 only): for sum with integer f and gamma != 1, the slope exceeds the one-dimensional value and is positive also at gamma = 0.9. Its value is judged by the rejection criterion. (At gamma = 1 both are 0; see P-K4-4.)

Rejection criterion outcome: rejected.

| f | gamma | oned_value | oned_slope | slope | lo | hi | holds |
|---|---|---|---|---|---|---|---|
| 3 | 0.900 | 0.000 | 0.043 | 0.304 | 0.299 | 0.308 | yes |
| 3 | 1.250 | 0.200 | 0.200 | 0.629 | 0.626 | 0.631 | yes |
| 3 | 1.750 | 0.429 | 0.426 | 0.814 | 0.814 | 0.815 | yes |
| 3 | 2.600 | 0.615 | 0.601 | 0.905 | 0.904 | 0.905 | yes |
| 5 | 0.900 | 0.000 | 0.046 | 0.294 | 0.289 | 0.300 | yes |
| 5 | 1.250 | 0.200 | 0.200 | 0.618 | 0.615 | 0.621 | yes |
| 5 | 1.750 | 0.429 | 0.425 | 0.811 | 0.810 | 0.812 | yes |
| 5 | 2.600 | 0.615 | 0.600 | 0.903 | 0.902 | 0.904 | yes |
| 7 | 0.900 | 0.000 | 0.049 | 0.287 | 0.282 | 0.293 | yes |
| 7 | 1.250 | 0.200 | 0.200 | 0.610 | 0.606 | 0.613 | yes |
| 7 | 1.750 | 0.429 | 0.425 | 0.808 | 0.807 | 0.810 | yes |
| 7 | 2.600 | 0.615 | 0.599 | 0.902 | 0.901 | 0.903 | yes |

### P-K4-4: 0 of 6 items hold

Prediction: P-K4-4 (gamma = 1, integer f): for sum and product1 the centroid does not depend on N for N >= 128 (band-limited; the highest component frequency 7 x 8 = 56 is below N/2 = 64). The slope interval contains 0.

Criterion: Slopes over N 128-4096 (the band-limited case holds from N = 128).

| field | f | rel_range_max | slope | lo | hi | holds |
|---|---|---|---|---|---|---|
| sum | 3 | 0.000 | 0.000 | 0.000 | 0.000 | no |
| sum | 5 | 0.000 | 0.000 | 0.000 | 0.000 | no |
| sum | 7 | 0.000 | 0.000 | 0.000 | 0.000 | no |
| product1 | 3 | 0.000 | 0.000 | 0.000 | 0.000 | no |
| product1 | 5 | 0.000 | 0.000 | 0.000 | 0.000 | no |
| product1 | 7 | 0.000 | 0.000 | 0.000 | 0.000 | no |

### P-K4-5: 6 of 6 items hold

Prediction: P-K4-5 (edge discontinuity, K4 (c)): for non-integer f, gamma = 1, raw, the centroid grows roughly like N / log N (corollary of the one-dimensional result). The slope is below 1 and approaches 1 as N grows (increasing local slope). Only the direction is predicted, not the value.

| field | f | slope | lo | hi | local | holds |
|---|---|---|---|---|---|---|
| sum | 3.500 | 0.888 | 0.881 | 0.895 | 0.730, 0.813, 0.862, 0.892, 0.909 | yes |
| sum | 5.500 | 0.871 | 0.859 | 0.882 | 0.652, 0.762, 0.833, 0.876, 0.901 | yes |
| sum | 6.300 | 0.824 | 0.816 | 0.831 | 0.523, 0.650, 0.761, 0.833, 0.875 | yes |
| product1 | 3.500 | 0.889 | 0.883 | 0.895 | 0.769, 0.831, 0.868, 0.891, 0.906 | yes |
| product1 | 5.500 | 0.876 | 0.867 | 0.884 | 0.704, 0.790, 0.846, 0.880, 0.900 | yes |
| product1 | 6.300 | 0.882 | 0.877 | 0.887 | 0.727, 0.808, 0.857, 0.885, 0.902 | yes |

### P-K4-6: 25 of 30 items hold

Prediction: P-K4-6 (window): for non-integer f, the hann slope approaches the hann slope of integer f at the same gamma (the edge discontinuity is removed) and is smaller than the raw slope for non-integer f.

Criterion: 'approaches': |hann slope (non-integer f) - mean hann slope (integer f)| is below the same distance for raw or below 0.05; 'smaller than raw': the 95% intervals do not overlap.

| field | f | gamma | hann_slope | hann_int_slope | raw_slope | raw_int_slope | approaches | smaller_than_raw | holds |
|---|---|---|---|---|---|---|---|---|---|
| sum | 3.500 | 0.900 | 0.289 | 0.286 | 0.876 | 0.295 | True | True | yes |
| sum | 5.500 | 0.900 | 0.304 | 0.286 | 0.852 | 0.295 | True | True | yes |
| sum | 6.300 | 0.900 | 0.239 | 0.286 | 0.813 | 0.295 | True | True | yes |
| sum | 3.500 | 1.000 | 0.000 | 0.000 | 0.888 | 0.000 | True | True | yes |
| sum | 5.500 | 1.000 | 0.000 | 0.000 | 0.871 | 0.000 | True | True | yes |
| sum | 6.300 | 1.000 | 0.000 | 0.000 | 0.824 | 0.000 | True | True | yes |
| sum | 3.500 | 1.250 | 0.601 | 0.601 | 0.858 | 0.619 | True | True | yes |
| sum | 5.500 | 1.250 | 0.636 | 0.601 | 0.835 | 0.619 | True | True | yes |
| sum | 6.300 | 1.250 | 0.517 | 0.601 | 0.798 | 0.619 | True | True | yes |
| sum | 3.500 | 1.750 | 0.786 | 0.792 | 0.840 | 0.811 | True | True | yes |
| sum | 5.500 | 1.750 | 0.833 | 0.792 | 0.833 | 0.811 | True | False | no |
| sum | 6.300 | 1.750 | 0.710 | 0.792 | 0.795 | 0.811 | False | True | no |
| sum | 3.500 | 2.600 | 0.878 | 0.885 | 0.876 | 0.903 | True | False | no |
| sum | 5.500 | 2.600 | 0.922 | 0.885 | 0.883 | 0.903 | True | False | no |
| sum | 6.300 | 2.600 | 0.819 | 0.885 | 0.843 | 0.903 | False | True | no |
| product1 | 3.500 | 0.900 | 0.058 | 0.060 | 0.888 | 0.059 | True | True | yes |
| product1 | 5.500 | 0.900 | 0.063 | 0.060 | 0.874 | 0.059 | True | True | yes |
| product1 | 6.300 | 0.900 | 0.057 | 0.060 | 0.881 | 0.059 | True | True | yes |
| product1 | 3.500 | 1.000 | 0.000 | 0.000 | 0.889 | 0.000 | True | True | yes |
| product1 | 5.500 | 1.000 | 0.000 | 0.000 | 0.876 | 0.000 | True | True | yes |
| product1 | 6.300 | 1.000 | 0.000 | 0.000 | 0.882 | 0.000 | True | True | yes |
| product1 | 3.500 | 1.250 | 0.229 | 0.234 | 0.889 | 0.232 | True | True | yes |
| product1 | 5.500 | 1.250 | 0.239 | 0.234 | 0.876 | 0.232 | True | True | yes |
| product1 | 6.300 | 1.250 | 0.208 | 0.234 | 0.876 | 0.232 | True | True | yes |
| product1 | 3.500 | 1.750 | 0.451 | 0.459 | 0.882 | 0.457 | True | True | yes |
| product1 | 5.500 | 1.750 | 0.470 | 0.459 | 0.863 | 0.457 | True | True | yes |
| product1 | 6.300 | 1.750 | 0.410 | 0.459 | 0.849 | 0.457 | True | True | yes |
| product1 | 3.500 | 2.600 | 0.618 | 0.629 | 0.863 | 0.629 | True | True | yes |
| product1 | 5.500 | 2.600 | 0.644 | 0.629 | 0.834 | 0.629 | True | True | yes |
| product1 | 6.300 | 2.600 | 0.567 | 0.629 | 0.811 | 0.629 | True | True | yes |

### P-K4-7: 61 of 66 items hold

Prediction: P-K4-7 (power weighting, K4 (d)): for integer f, centroid_power converges with N (local slope tends to 0). For non-integer f, raw, centroid_power grows roughly linearly in ln N. centroid_band_power does not depend on N for gamma = 1 and integer f (for gamma != 1, aliasing from outside K = 32 may enter, so no direction is predicted).

Criterion: 'grows roughly linearly in ln N': the increments of the seed mean per unit ln N are all positive and the last is within a factor 2 of the first.

| part | field | f | gamma | local | increments_per_lnN | rel_range_max | holds |
|---|---|---|---|---|---|---|---|
| power converges (integer f) | sum | 3 | 0.900 | 0.000, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | sum | 5 | 0.900 | 0.000, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | sum | 7 | 0.900 | 0.000, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power ~ ln N (non-integer f) | sum | 3.500 | 0.900 | - | 0.287, 0.296, 0.302, 0.306, 0.308 | - | yes |
| power ~ ln N (non-integer f) | sum | 5.500 | 0.900 | - | 0.283, 0.290, 0.298, 0.303, 0.307 | - | yes |
| power ~ ln N (non-integer f) | sum | 6.300 | 0.900 | - | 0.350, 0.342, 0.342, 0.343, 0.344 | - | yes |
| power converges (integer f) | sum | 3 | 1.000 | 0.000, -0.000, 0.000, -0.000, 0.000 | - | - | no |
| power converges (integer f) | sum | 5 | 1.000 | -0.000, -0.000, 0.000, -0.000, 0.000 | - | - | no |
| power converges (integer f) | sum | 7 | 1.000 | -0.000, 0.000, 0.000, -0.000, 0.000 | - | - | yes |
| power ~ ln N (non-integer f) | sum | 3.500 | 1.000 | - | 0.287, 0.296, 0.302, 0.306, 0.309 | - | yes |
| power ~ ln N (non-integer f) | sum | 5.500 | 1.000 | - | 0.281, 0.291, 0.298, 0.304, 0.307 | - | yes |
| power ~ ln N (non-integer f) | sum | 6.300 | 1.000 | - | 0.344, 0.340, 0.341, 0.342, 0.343 | - | yes |
| power converges (integer f) | sum | 3 | 1.250 | 0.001, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | sum | 5 | 1.250 | 0.001, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | sum | 7 | 1.250 | 0.003, 0.001, 0.000, 0.000, 0.000 | - | - | yes |
| power ~ ln N (non-integer f) | sum | 3.500 | 1.250 | - | 0.292, 0.297, 0.302, 0.306, 0.308 | - | yes |
| power ~ ln N (non-integer f) | sum | 5.500 | 1.250 | - | 0.299, 0.296, 0.300, 0.303, 0.306 | - | yes |
| power ~ ln N (non-integer f) | sum | 6.300 | 1.250 | - | 0.364, 0.343, 0.339, 0.338, 0.339 | - | yes |
| power converges (integer f) | sum | 3 | 1.750 | 0.007, 0.003, 0.001, 0.001, 0.000 | - | - | yes |
| power converges (integer f) | sum | 5 | 1.750 | 0.013, 0.006, 0.003, 0.001, 0.001 | - | - | yes |
| power converges (integer f) | sum | 7 | 1.750 | 0.021, 0.009, 0.004, 0.002, 0.001 | - | - | yes |
| power ~ ln N (non-integer f) | sum | 3.500 | 1.750 | - | 0.349, 0.321, 0.310, 0.307, 0.306 | - | yes |
| power ~ ln N (non-integer f) | sum | 5.500 | 1.750 | - | 0.453, 0.363, 0.328, 0.314, 0.309 | - | yes |
| power ~ ln N (non-integer f) | sum | 6.300 | 1.750 | - | 0.565, 0.428, 0.373, 0.350, 0.340 | - | yes |
| power converges (integer f) | sum | 3 | 2.600 | 0.031, 0.017, 0.010, 0.006, 0.003 | - | - | yes |
| power converges (integer f) | sum | 5 | 2.600 | 0.047, 0.026, 0.015, 0.009, 0.005 | - | - | yes |
| power converges (integer f) | sum | 7 | 2.600 | 0.064, 0.034, 0.020, 0.011, 0.007 | - | - | yes |
| power ~ ln N (non-integer f) | sum | 3.500 | 2.600 | - | 0.572, 0.456, 0.390, 0.353, 0.331 | - | yes |
| power ~ ln N (non-integer f) | sum | 5.500 | 2.600 | - | 0.935, 0.663, 0.510, 0.422, 0.372 | - | no |
| power ~ ln N (non-integer f) | sum | 6.300 | 2.600 | - | 1.166, 0.803, 0.602, 0.487, 0.419 | - | no |
| band power flat (gamma = 1, integer f) | sum | 3 | 1.000 | - | - | 0.000 | yes |
| band power flat (gamma = 1, integer f) | sum | 5 | 1.000 | - | - | 0.000 | yes |
| band power flat (gamma = 1, integer f) | sum | 7 | 1.000 | - | - | 0.000 | yes |
| power converges (integer f) | product1 | 3 | 0.900 | 0.000, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | product1 | 5 | 0.900 | 0.000, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | product1 | 7 | 0.900 | 0.000, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power ~ ln N (non-integer f) | product1 | 3.500 | 0.900 | - | 0.381, 0.393, 0.401, 0.407, 0.410 | - | yes |
| power ~ ln N (non-integer f) | product1 | 5.500 | 0.900 | - | 0.373, 0.386, 0.396, 0.403, 0.408 | - | yes |
| power ~ ln N (non-integer f) | product1 | 6.300 | 0.900 | - | 0.339, 0.339, 0.339, 0.341, 0.341 | - | yes |
| power converges (integer f) | product1 | 3 | 1.000 | 0.000, -0.000, -0.000, 0.000, -0.000 | - | - | yes |
| power converges (integer f) | product1 | 5 | 1.000 | -0.000, 0.000, -0.000, -0.000, -0.000 | - | - | yes |
| power converges (integer f) | product1 | 7 | 1.000 | -0.000, 0.000, 0.000, 0.000, 0.000 | - | - | no |
| power ~ ln N (non-integer f) | product1 | 3.500 | 1.000 | - | 0.381, 0.393, 0.401, 0.406, 0.409 | - | yes |
| power ~ ln N (non-integer f) | product1 | 5.500 | 1.000 | - | 0.372, 0.386, 0.396, 0.403, 0.407 | - | yes |
| power ~ ln N (non-integer f) | product1 | 6.300 | 1.000 | - | 0.340, 0.340, 0.341, 0.342, 0.343 | - | yes |
| power converges (integer f) | product1 | 3 | 1.250 | 0.000, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | product1 | 5 | 1.250 | 0.001, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | product1 | 7 | 1.250 | 0.001, 0.000, 0.000, 0.000, 0.000 | - | - | yes |
| power ~ ln N (non-integer f) | product1 | 3.500 | 1.250 | - | 0.382, 0.393, 0.401, 0.405, 0.408 | - | yes |
| power ~ ln N (non-integer f) | product1 | 5.500 | 1.250 | - | 0.377, 0.387, 0.396, 0.403, 0.407 | - | yes |
| power ~ ln N (non-integer f) | product1 | 6.300 | 1.250 | - | 0.347, 0.343, 0.343, 0.344, 0.344 | - | yes |
| power converges (integer f) | product1 | 3 | 1.750 | 0.004, 0.002, 0.001, 0.000, 0.000 | - | - | yes |
| power converges (integer f) | product1 | 5 | 1.750 | 0.007, 0.003, 0.001, 0.001, 0.000 | - | - | yes |
| power converges (integer f) | product1 | 7 | 1.750 | 0.010, 0.005, 0.002, 0.001, 0.000 | - | - | yes |
| power ~ ln N (non-integer f) | product1 | 3.500 | 1.750 | - | 0.404, 0.406, 0.405, 0.406, 0.408 | - | yes |
| power ~ ln N (non-integer f) | product1 | 5.500 | 1.750 | - | 0.435, 0.416, 0.408, 0.407, 0.408 | - | yes |
| power ~ ln N (non-integer f) | product1 | 6.300 | 1.750 | - | 0.421, 0.378, 0.359, 0.349, 0.346 | - | yes |
| power converges (integer f) | product1 | 3 | 2.600 | 0.019, 0.012, 0.007, 0.004, 0.002 | - | - | yes |
| power converges (integer f) | product1 | 5 | 2.600 | 0.029, 0.018, 0.010, 0.006, 0.003 | - | - | yes |
| power converges (integer f) | product1 | 7 | 2.600 | 0.038, 0.023, 0.013, 0.008, 0.004 | - | - | yes |
| power ~ ln N (non-integer f) | product1 | 3.500 | 2.600 | - | 0.511, 0.480, 0.446, 0.430, 0.421 | - | yes |
| power ~ ln N (non-integer f) | product1 | 5.500 | 2.600 | - | 0.672, 0.567, 0.498, 0.461, 0.439 | - | yes |
| power ~ ln N (non-integer f) | product1 | 6.300 | 2.600 | - | 0.712, 0.562, 0.473, 0.414, 0.383 | - | yes |
| band power flat (gamma = 1, integer f) | product1 | 3 | 1.000 | - | - | 0.000 | yes |
| band power flat (gamma = 1, integer f) | product1 | 5 | 1.000 | - | - | 0.000 | yes |
| band power flat (gamma = 1, integer f) | product1 | 7 | 1.000 | - | - | 0.000 | yes |

## Normalisation check (implementation control)

maxabs versus ampsum, sum field, f in {5, 5.5}, gamma in {0.9, 1.75}, seeds 1-5, every N, both processings and all descriptors: largest relative difference 1.60e-13 (agree to rounding).

## Aliasing subset (sum, f in {5, 5.5}, seeds 1-10)

Relative paired difference (decimate_fourier with r = 2 minus direct sampling, divided by the direct mean), raw processing, by N; and the residual of the reference (r = 4 minus r = 2, relative, N <= 2048).

| f | gamma | descriptor | decimate - direct (relative), N 128 ... 4096 | r4 - r2 (relative), N 128 ... 2048 |
|---|---|---|---|---|
| 5 | 0.9 | centroid_amp | -9.18e-02, -1.03e-01, -1.19e-01, -1.36e-01, -1.49e-01, -1.58e-01 | -1.12e-02, -1.56e-02, -1.90e-02, -2.15e-02, -2.37e-02 |
| 5 | 0.9 | centroid_power | -1.83e-04, -2.89e-05, -5.85e-06, -1.30e-06, -2.83e-07, -6.08e-08 | -1.21e-06, -3.02e-07, -6.94e-08, -1.55e-08, -3.48e-09 |
| 5 | 0.9 | centroid_band_power | -2.66e-06, -1.94e-07, +1.14e-08, +5.74e-09, +4.66e-10, -7.53e-11 | -1.94e-07, +1.14e-08, +5.74e-09, +4.66e-10, -7.53e-11 |
| 5 | 1.0 | centroid_amp | -1.10e-14, -2.49e-14, -1.36e-14, +8.83e-14, +4.86e-13, +2.78e-12 | -7.10e-15, -1.82e-14, -5.93e-14, -2.82e-13, -8.44e-13 |
| 5 | 1.0 | centroid_power | -5.34e-17, +8.90e-17, -1.25e-16, -3.56e-17, +3.56e-17, -1.78e-17 | +5.34e-17, +3.56e-17, -8.90e-17, -5.34e-17, -3.56e-17 |
| 5 | 1.0 | centroid_band_power | -7.54e-17, +0.00e+00, -7.54e-17, -5.65e-17, +7.54e-17, +1.88e-17 | +3.77e-17, +9.42e-17, -7.54e-17, -9.42e-17, -1.88e-17 |
| 5 | 1.25 | centroid_amp | -1.61e-01, -1.95e-01, -2.27e-01, -2.56e-01, -2.76e-01, -2.89e-01 | -3.28e-02, -4.66e-02, -5.69e-02, -6.43e-02, -7.02e-02 |
| 5 | 1.25 | centroid_power | -1.26e-03, -3.70e-04, -1.20e-04, -4.09e-05, -1.37e-05, -4.53e-06 | -2.01e-05, -8.20e-06, -2.80e-06, -9.23e-07, -3.05e-07 |
| 5 | 1.25 | centroid_band_power | -3.03e-05, -1.71e-07, -1.56e-07, -6.87e-08, -7.11e-09, +8.81e-10 | -1.71e-07, -1.56e-07, -6.87e-08, -7.11e-09, +8.81e-10 |
| 5 | 1.75 | centroid_amp | -1.95e-01, -2.27e-01, -2.58e-01, -2.85e-01, -3.04e-01, -3.17e-01 | -6.24e-02, -8.13e-02, -9.39e-02, -1.03e-01, -1.10e-01 |
| 5 | 1.75 | centroid_power | -9.96e-03, -4.34e-03, -1.97e-03, -9.23e-04, -4.25e-04, -1.93e-04 | -2.71e-04, -1.49e-04, -7.03e-05, -3.20e-05, -1.46e-05 |
| 5 | 1.75 | centroid_band_power | -3.01e-04, -1.08e-05, -1.50e-06, -5.71e-07, -7.06e-08, +6.00e-09 | -1.08e-05, -1.50e-06, -5.71e-07, -7.06e-08, +6.00e-09 |
| 5 | 2.6 | centroid_amp | -1.84e-01, -2.12e-01, -2.39e-01, -2.63e-01, -2.80e-01, -2.92e-01 | -8.19e-02, -1.03e-01, -1.16e-01, -1.26e-01, -1.34e-01 |
| 5 | 2.6 | centroid_power | -3.06e-02, -1.78e-02, -1.05e-02, -6.37e-03, -3.79e-03, -2.22e-03 | -1.28e-03, -8.89e-04, -5.38e-04, -3.16e-04, -1.86e-04 |
| 5 | 2.6 | centroid_band_power | -1.15e-03, -6.72e-05, -7.35e-06, -2.46e-06, -3.52e-07, +1.48e-08 | -6.72e-05, -7.35e-06, -2.46e-06, -3.52e-07, +1.48e-08 |
| 5.5 | 0.9 | centroid_amp | -6.61e-02, -7.31e-02, -8.17e-02, -8.75e-02, -9.17e-02, -9.43e-02 | -1.45e-02, -1.69e-02, -1.90e-02, -2.04e-02, -2.13e-02 |
| 5.5 | 0.9 | centroid_power | -1.08e-02, -1.12e-02, -1.12e-02, -1.10e-02, -1.08e-02, -1.06e-02 | -2.52e-03, -2.46e-03, -2.35e-03, -2.24e-03, -2.15e-03 |
| 5.5 | 0.9 | centroid_band_power | -2.49e-03, -9.53e-04, -4.18e-04, -1.95e-04, -9.40e-05, -4.62e-05 | -9.53e-04, -4.18e-04, -1.95e-04, -9.40e-05, -4.62e-05 |
| 5.5 | 1.0 | centroid_amp | -6.18e-02, -7.38e-02, -8.33e-02, -8.92e-02, -9.27e-02, -9.49e-02 | -1.63e-02, -1.86e-02, -2.02e-02, -2.12e-02, -2.19e-02 |
| 5.5 | 1.0 | centroid_power | -1.06e-02, -1.11e-02, -1.11e-02, -1.10e-02, -1.08e-02, -1.06e-02 | -2.50e-03, -2.44e-03, -2.33e-03, -2.23e-03, -2.15e-03 |
| 5.5 | 1.0 | centroid_band_power | -2.46e-03, -9.44e-04, -4.12e-04, -1.92e-04, -9.24e-05, -4.53e-05 | -9.44e-04, -4.12e-04, -1.92e-04, -9.24e-05, -4.53e-05 |
| 5.5 | 1.25 | centroid_amp | -7.94e-02, -8.08e-02, -8.59e-02, -8.92e-02, -9.41e-02, -9.69e-02 | -1.35e-02, -1.44e-02, -1.66e-02, -1.81e-02, -1.94e-02 |
| 5.5 | 1.25 | centroid_power | -1.16e-02, -1.11e-02, -1.09e-02, -1.08e-02, -1.06e-02, -1.04e-02 | -2.44e-03, -2.35e-03, -2.25e-03, -2.16e-03, -2.09e-03 |
| 5.5 | 1.25 | centroid_band_power | -2.40e-03, -9.12e-04, -3.94e-04, -1.83e-04, -8.81e-05, -4.31e-05 | -9.12e-04, -3.94e-04, -1.83e-04, -8.81e-05, -4.31e-05 |
| 5.5 | 1.75 | centroid_amp | -1.11e-01, -1.07e-01, -1.08e-01, -1.09e-01, -1.20e-01, -1.28e-01 | -1.60e-02, -1.42e-02, -1.69e-02, -1.85e-02, -1.99e-02 |
| 5.5 | 1.75 | centroid_power | -1.93e-02, -1.40e-02, -1.18e-02, -1.07e-02, -1.01e-02, -9.75e-03 | -2.50e-03, -2.24e-03, -2.09e-03, -1.99e-03, -1.92e-03 |
| 5.5 | 1.75 | centroid_band_power | -2.50e-03, -8.60e-04, -3.60e-04, -1.68e-04, -8.09e-05, -3.96e-05 | -8.60e-04, -3.60e-04, -1.68e-04, -8.09e-05, -3.96e-05 |
| 5.5 | 2.6 | centroid_amp | -1.33e-01, -1.33e-01, -1.32e-01, -1.37e-01, -1.54e-01, -1.71e-01 | -2.45e-02, -1.99e-02, -2.45e-02, -2.73e-02, -3.04e-02 |
| 5.5 | 2.6 | centroid_power | -3.82e-02, -2.55e-02, -1.89e-02, -1.46e-02, -1.19e-02, -1.02e-02 | -3.33e-03, -2.63e-03, -2.24e-03, -1.97e-03, -1.80e-03 |
| 5.5 | 2.6 | centroid_band_power | -3.12e-03, -8.42e-04, -3.24e-04, -1.51e-04, -7.34e-05, -3.59e-05 | -8.42e-04, -3.24e-04, -1.51e-04, -7.34e-05, -3.59e-05 |

## C ln N / N for gamma = 1 and non-integer f (check of P-K4-5)

| field | f | N 128 ... 4096 |
|---|---|---|
| sum | 3.5 | 0.709, 0.679, 0.676, 0.685, 0.700, 0.717 |
| sum | 5.5 | 0.789, 0.717, 0.691, 0.688, 0.697, 0.710 |
| sum | 6.3 | 1.029, 0.846, 0.747, 0.704, 0.690, 0.690 |
| product1 | 3.5 | 0.712, 0.700, 0.703, 0.715, 0.730, 0.745 |
| product1 | 5.5 | 0.770, 0.725, 0.711, 0.713, 0.723, 0.736 |
| product1 | 6.3 | 0.802, 0.761, 0.752, 0.757, 0.770, 0.784 |
| oned | 3.5 | 0.434, 0.416, 0.410, 0.411, 0.415, 0.421 |
| oned | 5.5 | 0.477, 0.434, 0.415, 0.410, 0.410, 0.414 |
| oned | 6.3 | 0.486, 0.434, 0.409, 0.399, 0.398, 0.400 |

## Slopes of every cell

Primary range N 512-4096 (95% t interval over seeds) and descriptive range N 128-4096 (mean).

| field | f | gamma | processing | descriptor | slope (primary) | interval | slope (128-4096) |
|---|---|---|---|---|---|---|---|
| sum | 3 | 0.9 | raw | centroid_amp | 0.3035 | [0.2986, 0.3084] | 0.2835 |
| sum | 3 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 3 | 0.9 | raw | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 0.9 | hann | centroid_amp | 0.2945 | [0.2894, 0.2996] | 0.2725 |
| sum | 3 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 3 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 3 | 1.0 | raw | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 1.0 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 3 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| sum | 3 | 1.0 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| sum | 3 | 1.25 | raw | centroid_amp | 0.6285 | [0.6264, 0.6307] | 0.5945 |
| sum | 3 | 1.25 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| sum | 3 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 1.25 | hann | centroid_amp | 0.6127 | [0.6102, 0.6152] | 0.5723 |
| sum | 3 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| sum | 3 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 1.75 | raw | centroid_amp | 0.8145 | [0.8139, 0.8150] | 0.7891 |
| sum | 3 | 1.75 | raw | centroid_power | 0.0008 | [0.0007, 0.0008] | 0.0023 |
| sum | 3 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 1.75 | hann | centroid_amp | 0.7973 | [0.7966, 0.7981] | 0.7655 |
| sum | 3 | 1.75 | hann | centroid_power | 0.0008 | [0.0007, 0.0008] | 0.0023 |
| sum | 3 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3 | 2.6 | raw | centroid_amp | 0.9045 | [0.9037, 0.9053] | 0.8835 |
| sum | 3 | 2.6 | raw | centroid_power | 0.0064 | [0.0062, 0.0066] | 0.0127 |
| sum | 3 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0002 |
| sum | 3 | 2.6 | hann | centroid_amp | 0.8883 | [0.8873, 0.8893] | 0.8613 |
| sum | 3 | 2.6 | hann | centroid_power | 0.0064 | [0.0062, 0.0066] | 0.0127 |
| sum | 3 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0002 |
| sum | 5 | 0.9 | raw | centroid_amp | 0.2942 | [0.2888, 0.2996] | 0.2748 |
| sum | 5 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 5 | 0.9 | raw | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5 | 0.9 | hann | centroid_amp | 0.2846 | [0.2792, 0.2900] | 0.2638 |
| sum | 5 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 5 | 1.0 | raw | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| sum | 5 | 1.0 | raw | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| sum | 5 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 5 | 1.0 | hann | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| sum | 5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5 | 1.25 | raw | centroid_amp | 0.6181 | [0.6153, 0.6210] | 0.5808 |
| sum | 5 | 1.25 | raw | centroid_power | 0.0001 | [0.0001, 0.0001] | 0.0004 |
| sum | 5 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5 | 1.25 | hann | centroid_amp | 0.5982 | [0.5951, 0.6012] | 0.5557 |
| sum | 5 | 1.25 | hann | centroid_power | 0.0001 | [0.0001, 0.0001] | 0.0003 |
| sum | 5 | 1.25 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| sum | 5 | 1.75 | raw | centroid_amp | 0.8112 | [0.8104, 0.8120] | 0.7843 |
| sum | 5 | 1.75 | raw | centroid_power | 0.0014 | [0.0013, 0.0014] | 0.0042 |
| sum | 5 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| sum | 5 | 1.75 | hann | centroid_amp | 0.7887 | [0.7877, 0.7897] | 0.7564 |
| sum | 5 | 1.75 | hann | centroid_power | 0.0014 | [0.0013, 0.0014] | 0.0042 |
| sum | 5 | 1.75 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5 | 2.6 | raw | centroid_amp | 0.9032 | [0.9023, 0.9040] | 0.8816 |
| sum | 5 | 2.6 | raw | centroid_power | 0.0095 | [0.0092, 0.0098] | 0.0192 |
| sum | 5 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| sum | 5 | 2.6 | hann | centroid_amp | 0.8824 | [0.8813, 0.8834] | 0.8557 |
| sum | 5 | 2.6 | hann | centroid_power | 0.0095 | [0.0092, 0.0098] | 0.0192 |
| sum | 5 | 2.6 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0002 |
| sum | 7 | 0.9 | raw | centroid_amp | 0.2873 | [0.2817, 0.2930] | 0.2702 |
| sum | 7 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| sum | 7 | 0.9 | raw | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 7 | 0.9 | hann | centroid_amp | 0.2801 | [0.2743, 0.2859] | 0.2588 |
| sum | 7 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| sum | 7 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 7 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 7 | 1.0 | raw | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 7 | 1.0 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 7 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 7 | 1.0 | hann | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| sum | 7 | 1.0 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 7 | 1.25 | raw | centroid_amp | 0.6096 | [0.6062, 0.6130] | 0.5713 |
| sum | 7 | 1.25 | raw | centroid_power | 0.0001 | [0.0001, 0.0001] | 0.0006 |
| sum | 7 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 7 | 1.25 | hann | centroid_amp | 0.5925 | [0.5888, 0.5963] | 0.5436 |
| sum | 7 | 1.25 | hann | centroid_power | 0.0001 | [0.0001, 0.0001] | 0.0006 |
| sum | 7 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 7 | 1.75 | raw | centroid_amp | 0.8084 | [0.8073, 0.8095] | 0.7817 |
| sum | 7 | 1.75 | raw | centroid_power | 0.0020 | [0.0020, 0.0021] | 0.0064 |
| sum | 7 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| sum | 7 | 1.75 | hann | centroid_amp | 0.7887 | [0.7873, 0.7902] | 0.7504 |
| sum | 7 | 1.75 | hann | centroid_power | 0.0021 | [0.0020, 0.0021] | 0.0063 |
| sum | 7 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0001 |
| sum | 7 | 2.6 | raw | centroid_amp | 0.9021 | [0.9013, 0.9030] | 0.8811 |
| sum | 7 | 2.6 | raw | centroid_power | 0.0124 | [0.0120, 0.0128] | 0.0255 |
| sum | 7 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| sum | 7 | 2.6 | hann | centroid_amp | 0.8837 | [0.8824, 0.8850] | 0.8526 |
| sum | 7 | 2.6 | hann | centroid_power | 0.0124 | [0.0120, 0.0129] | 0.0254 |
| sum | 7 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0003 |
| sum | 3.5 | 0.9 | raw | centroid_amp | 0.8760 | [0.8626, 0.8893] | 0.8306 |
| sum | 3.5 | 0.9 | raw | centroid_power | 0.0341 | [0.0265, 0.0417] | 0.0345 |
| sum | 3.5 | 0.9 | raw | centroid_band_power | -0.0005 | [-0.0008, -0.0002] | -0.0017 |
| sum | 3.5 | 0.9 | hann | centroid_amp | 0.2885 | [0.2833, 0.2938] | 0.2647 |
| sum | 3.5 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 3.5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3.5 | 1.0 | raw | centroid_amp | 0.8879 | [0.8808, 0.8951] | 0.8454 |
| sum | 3.5 | 1.0 | raw | centroid_power | 0.0344 | [0.0269, 0.0418] | 0.0348 |
| sum | 3.5 | 1.0 | raw | centroid_band_power | -0.0005 | [-0.0007, -0.0002] | -0.0017 |
| sum | 3.5 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| sum | 3.5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3.5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3.5 | 1.25 | raw | centroid_amp | 0.8581 | [0.8437, 0.8725] | 0.8193 |
| sum | 3.5 | 1.25 | raw | centroid_power | 0.0342 | [0.0273, 0.0412] | 0.0348 |
| sum | 3.5 | 1.25 | raw | centroid_band_power | -0.0004 | [-0.0007, -0.0002] | -0.0016 |
| sum | 3.5 | 1.25 | hann | centroid_amp | 0.6011 | [0.5983, 0.6038] | 0.5557 |
| sum | 3.5 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| sum | 3.5 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3.5 | 1.75 | raw | centroid_amp | 0.8403 | [0.8346, 0.8460] | 0.8146 |
| sum | 3.5 | 1.75 | raw | centroid_power | 0.0331 | [0.0272, 0.0390] | 0.0351 |
| sum | 3.5 | 1.75 | raw | centroid_band_power | -0.0004 | [-0.0006, -0.0002] | -0.0015 |
| sum | 3.5 | 1.75 | hann | centroid_amp | 0.7862 | [0.7852, 0.7871] | 0.7494 |
| sum | 3.5 | 1.75 | hann | centroid_power | 0.0009 | [0.0009, 0.0009] | 0.0028 |
| sum | 3.5 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 3.5 | 2.6 | raw | centroid_amp | 0.8757 | [0.8738, 0.8776] | 0.8555 |
| sum | 3.5 | 2.6 | raw | centroid_power | 0.0344 | [0.0300, 0.0389] | 0.0414 |
| sum | 3.5 | 2.6 | raw | centroid_band_power | -0.0003 | [-0.0006, -0.0001] | -0.0015 |
| sum | 3.5 | 2.6 | hann | centroid_amp | 0.8784 | [0.8772, 0.8796] | 0.8477 |
| sum | 3.5 | 2.6 | hann | centroid_power | 0.0071 | [0.0069, 0.0074] | 0.0144 |
| sum | 3.5 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0002 |
| sum | 5.5 | 0.9 | raw | centroid_amp | 0.8521 | [0.8330, 0.8713] | 0.7924 |
| sum | 5.5 | 0.9 | raw | centroid_power | 0.0236 | [0.0180, 0.0291] | 0.0236 |
| sum | 5.5 | 0.9 | raw | centroid_band_power | -0.0004 | [-0.0006, -0.0001] | -0.0012 |
| sum | 5.5 | 0.9 | hann | centroid_amp | 0.3035 | [0.2972, 0.3098] | 0.2614 |
| sum | 5.5 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 5.5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5.5 | 1.0 | raw | centroid_amp | 0.8707 | [0.8591, 0.8822] | 0.8106 |
| sum | 5.5 | 1.0 | raw | centroid_power | 0.0238 | [0.0183, 0.0292] | 0.0237 |
| sum | 5.5 | 1.0 | raw | centroid_band_power | -0.0004 | [-0.0006, -0.0001] | -0.0012 |
| sum | 5.5 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| sum | 5.5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5.5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5.5 | 1.25 | raw | centroid_amp | 0.8352 | [0.8203, 0.8502] | 0.7868 |
| sum | 5.5 | 1.25 | raw | centroid_power | 0.0237 | [0.0186, 0.0288] | 0.0239 |
| sum | 5.5 | 1.25 | raw | centroid_band_power | -0.0004 | [-0.0006, -0.0001] | -0.0012 |
| sum | 5.5 | 1.25 | hann | centroid_amp | 0.6361 | [0.6320, 0.6403] | 0.5492 |
| sum | 5.5 | 1.25 | hann | centroid_power | 0.0001 | [0.0001, 0.0001] | 0.0004 |
| sum | 5.5 | 1.25 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 5.5 | 1.75 | raw | centroid_amp | 0.8333 | [0.8300, 0.8366] | 0.7980 |
| sum | 5.5 | 1.75 | raw | centroid_power | 0.0235 | [0.0192, 0.0278] | 0.0265 |
| sum | 5.5 | 1.75 | raw | centroid_band_power | -0.0004 | [-0.0006, -0.0001] | -0.0012 |
| sum | 5.5 | 1.75 | hann | centroid_amp | 0.8334 | [0.8316, 0.8351] | 0.7510 |
| sum | 5.5 | 1.75 | hann | centroid_power | 0.0016 | [0.0015, 0.0016] | 0.0047 |
| sum | 5.5 | 1.75 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0001 |
| sum | 5.5 | 2.6 | raw | centroid_amp | 0.8830 | [0.8803, 0.8857] | 0.8485 |
| sum | 5.5 | 2.6 | raw | centroid_power | 0.0286 | [0.0254, 0.0317] | 0.0387 |
| sum | 5.5 | 2.6 | raw | centroid_band_power | -0.0003 | [-0.0005, -0.0001] | -0.0013 |
| sum | 5.5 | 2.6 | hann | centroid_amp | 0.9224 | [0.9209, 0.9239] | 0.8521 |
| sum | 5.5 | 2.6 | hann | centroid_power | 0.0103 | [0.0100, 0.0106] | 0.0207 |
| sum | 5.5 | 2.6 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0003 |
| sum | 6.3 | 0.9 | raw | centroid_amp | 0.8131 | [0.8047, 0.8215] | 0.7264 |
| sum | 6.3 | 0.9 | raw | centroid_power | 0.0243 | [0.0213, 0.0273] | 0.0248 |
| sum | 6.3 | 0.9 | raw | centroid_band_power | -0.0001 | [-0.0003, 0.0001] | -0.0005 |
| sum | 6.3 | 0.9 | hann | centroid_amp | 0.2392 | [0.2343, 0.2441] | 0.2388 |
| sum | 6.3 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| sum | 6.3 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| sum | 6.3 | 1.0 | raw | centroid_amp | 0.8239 | [0.8164, 0.8313] | 0.7342 |
| sum | 6.3 | 1.0 | raw | centroid_power | 0.0243 | [0.0213, 0.0273] | 0.0248 |
| sum | 6.3 | 1.0 | raw | centroid_band_power | -0.0001 | [-0.0004, 0.0001] | -0.0005 |
| sum | 6.3 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| sum | 6.3 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 6.3 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| sum | 6.3 | 1.25 | raw | centroid_amp | 0.7979 | [0.7907, 0.8051] | 0.7251 |
| sum | 6.3 | 1.25 | raw | centroid_power | 0.0239 | [0.0210, 0.0268] | 0.0247 |
| sum | 6.3 | 1.25 | raw | centroid_band_power | -0.0001 | [-0.0004, 0.0002] | -0.0005 |
| sum | 6.3 | 1.25 | hann | centroid_amp | 0.5172 | [0.5141, 0.5203] | 0.5075 |
| sum | 6.3 | 1.25 | hann | centroid_power | 0.0001 | [0.0001, 0.0001] | 0.0005 |
| sum | 6.3 | 1.25 | hann | centroid_band_power | 0.0000 | [0.0000, 0.0000] | -0.0000 |
| sum | 6.3 | 1.75 | raw | centroid_amp | 0.7948 | [0.7919, 0.7977] | 0.7519 |
| sum | 6.3 | 1.75 | raw | centroid_power | 0.0236 | [0.0210, 0.0262] | 0.0275 |
| sum | 6.3 | 1.75 | raw | centroid_band_power | -0.0001 | [-0.0005, 0.0002] | -0.0006 |
| sum | 6.3 | 1.75 | hann | centroid_amp | 0.7097 | [0.7087, 0.7107] | 0.7111 |
| sum | 6.3 | 1.75 | hann | centroid_power | 0.0018 | [0.0017, 0.0019] | 0.0056 |
| sum | 6.3 | 1.75 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0001 |
| sum | 6.3 | 2.6 | raw | centroid_amp | 0.8431 | [0.8415, 0.8446] | 0.8138 |
| sum | 6.3 | 2.6 | raw | centroid_power | 0.0293 | [0.0272, 0.0314] | 0.0412 |
| sum | 6.3 | 2.6 | raw | centroid_band_power | -0.0001 | [-0.0005, 0.0002] | -0.0009 |
| sum | 6.3 | 2.6 | hann | centroid_amp | 0.8188 | [0.8178, 0.8198] | 0.8191 |
| sum | 6.3 | 2.6 | hann | centroid_power | 0.0114 | [0.0110, 0.0118] | 0.0233 |
| sum | 6.3 | 2.6 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0004 |
| product1 | 3 | 0.9 | raw | centroid_amp | 0.0554 | [0.0550, 0.0557] | 0.0628 |
| product1 | 3 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 0.9 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 3 | 0.9 | hann | centroid_amp | 0.0558 | [0.0554, 0.0563] | 0.0630 |
| product1 | 3 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 0.9 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 3 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 1.0 | raw | centroid_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 1.0 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 1.0 | hann | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 1.0 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 3 | 1.25 | raw | centroid_amp | 0.2295 | [0.2278, 0.2311] | 0.2338 |
| product1 | 3 | 1.25 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| product1 | 3 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 3 | 1.25 | hann | centroid_amp | 0.2290 | [0.2272, 0.2309] | 0.2322 |
| product1 | 3 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| product1 | 3 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 3 | 1.75 | raw | centroid_amp | 0.4526 | [0.4493, 0.4559] | 0.4583 |
| product1 | 3 | 1.75 | raw | centroid_power | 0.0004 | [0.0004, 0.0004] | 0.0012 |
| product1 | 3 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| product1 | 3 | 1.75 | hann | centroid_amp | 0.4517 | [0.4484, 0.4550] | 0.4553 |
| product1 | 3 | 1.75 | hann | centroid_power | 0.0004 | [0.0004, 0.0004] | 0.0012 |
| product1 | 3 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| product1 | 3 | 2.6 | raw | centroid_amp | 0.6241 | [0.6201, 0.6281] | 0.6262 |
| product1 | 3 | 2.6 | raw | centroid_power | 0.0042 | [0.0041, 0.0043] | 0.0085 |
| product1 | 3 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| product1 | 3 | 2.6 | hann | centroid_amp | 0.6214 | [0.6175, 0.6252] | 0.6209 |
| product1 | 3 | 2.6 | hann | centroid_power | 0.0041 | [0.0040, 0.0043] | 0.0083 |
| product1 | 3 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0001, -0.0000] | -0.0004 |
| product1 | 5 | 0.9 | raw | centroid_amp | 0.0598 | [0.0596, 0.0600] | 0.0679 |
| product1 | 5 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 5 | 0.9 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 5 | 0.9 | hann | centroid_amp | 0.0614 | [0.0611, 0.0617] | 0.0687 |
| product1 | 5 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 5 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 5 | 1.0 | raw | centroid_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 5 | 1.0 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 5 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 5 | 1.25 | raw | centroid_amp | 0.2325 | [0.2315, 0.2336] | 0.2368 |
| product1 | 5 | 1.25 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| product1 | 5 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 5 | 1.25 | hann | centroid_amp | 0.2357 | [0.2349, 0.2366] | 0.2369 |
| product1 | 5 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| product1 | 5 | 1.25 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 5 | 1.75 | raw | centroid_amp | 0.4577 | [0.4554, 0.4599] | 0.4637 |
| product1 | 5 | 1.75 | raw | centroid_power | 0.0007 | [0.0007, 0.0008] | 0.0022 |
| product1 | 5 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| product1 | 5 | 1.75 | hann | centroid_amp | 0.4620 | [0.4603, 0.4636] | 0.4628 |
| product1 | 5 | 1.75 | hann | centroid_power | 0.0008 | [0.0007, 0.0008] | 0.0022 |
| product1 | 5 | 1.75 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0001 |
| product1 | 5 | 2.6 | raw | centroid_amp | 0.6292 | [0.6263, 0.6321] | 0.6316 |
| product1 | 5 | 2.6 | raw | centroid_power | 0.0064 | [0.0063, 0.0064] | 0.0126 |
| product1 | 5 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| product1 | 5 | 2.6 | hann | centroid_amp | 0.6317 | [0.6293, 0.6341] | 0.6284 |
| product1 | 5 | 2.6 | hann | centroid_power | 0.0064 | [0.0062, 0.0066] | 0.0126 |
| product1 | 5 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0003 |
| product1 | 7 | 0.9 | raw | centroid_amp | 0.0632 | [0.0630, 0.0633] | 0.0717 |
| product1 | 7 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 0.9 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 7 | 0.9 | hann | centroid_amp | 0.0641 | [0.0639, 0.0643] | 0.0727 |
| product1 | 7 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 0.9 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 7 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 1.0 | raw | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 1.0 | raw | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 1.0 | hann | centroid_band_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 7 | 1.25 | raw | centroid_amp | 0.2347 | [0.2339, 0.2355] | 0.2387 |
| product1 | 7 | 1.25 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| product1 | 7 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 7 | 1.25 | hann | centroid_amp | 0.2366 | [0.2358, 0.2374] | 0.2393 |
| product1 | 7 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| product1 | 7 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 7 | 1.75 | raw | centroid_amp | 0.4615 | [0.4597, 0.4633] | 0.4674 |
| product1 | 7 | 1.75 | raw | centroid_power | 0.0011 | [0.0011, 0.0011] | 0.0032 |
| product1 | 7 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| product1 | 7 | 1.75 | hann | centroid_amp | 0.4637 | [0.4619, 0.4655] | 0.4668 |
| product1 | 7 | 1.75 | hann | centroid_power | 0.0011 | [0.0011, 0.0011] | 0.0032 |
| product1 | 7 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0001 |
| product1 | 7 | 2.6 | raw | centroid_amp | 0.6330 | [0.6306, 0.6353] | 0.6352 |
| product1 | 7 | 2.6 | raw | centroid_power | 0.0083 | [0.0082, 0.0083] | 0.0163 |
| product1 | 7 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0004 |
| product1 | 7 | 2.6 | hann | centroid_amp | 0.6333 | [0.6307, 0.6359] | 0.6322 |
| product1 | 7 | 2.6 | hann | centroid_power | 0.0083 | [0.0081, 0.0084] | 0.0163 |
| product1 | 7 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0004 |
| product1 | 3.5 | 0.9 | raw | centroid_amp | 0.8878 | [0.8820, 0.8935] | 0.8534 |
| product1 | 3.5 | 0.9 | raw | centroid_power | 0.0541 | [0.0427, 0.0655] | 0.0556 |
| product1 | 3.5 | 0.9 | raw | centroid_band_power | -0.0008 | [-0.0013, -0.0003] | -0.0029 |
| product1 | 3.5 | 0.9 | hann | centroid_amp | 0.0583 | [0.0571, 0.0594] | 0.0637 |
| product1 | 3.5 | 0.9 | hann | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| product1 | 3.5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 3.5 | 1.0 | raw | centroid_amp | 0.8888 | [0.8831, 0.8946] | 0.8562 |
| product1 | 3.5 | 1.0 | raw | centroid_power | 0.0545 | [0.0436, 0.0654] | 0.0560 |
| product1 | 3.5 | 1.0 | raw | centroid_band_power | -0.0008 | [-0.0012, -0.0003] | -0.0029 |
| product1 | 3.5 | 1.0 | hann | centroid_amp | 0.0001 | [0.0001, 0.0002] | 0.0003 |
| product1 | 3.5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 3.5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 3.5 | 1.25 | raw | centroid_amp | 0.8890 | [0.8828, 0.8951] | 0.8585 |
| product1 | 3.5 | 1.25 | raw | centroid_power | 0.0547 | [0.0450, 0.0643] | 0.0562 |
| product1 | 3.5 | 1.25 | raw | centroid_band_power | -0.0008 | [-0.0012, -0.0004] | -0.0029 |
| product1 | 3.5 | 1.25 | hann | centroid_amp | 0.2290 | [0.2258, 0.2323] | 0.2268 |
| product1 | 3.5 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| product1 | 3.5 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 3.5 | 1.75 | raw | centroid_amp | 0.8818 | [0.8746, 0.8891] | 0.8507 |
| product1 | 3.5 | 1.75 | raw | centroid_power | 0.0535 | [0.0458, 0.0611] | 0.0557 |
| product1 | 3.5 | 1.75 | raw | centroid_band_power | -0.0008 | [-0.0012, -0.0004] | -0.0029 |
| product1 | 3.5 | 1.75 | hann | centroid_amp | 0.4508 | [0.4467, 0.4548] | 0.4446 |
| product1 | 3.5 | 1.75 | hann | centroid_power | 0.0005 | [0.0004, 0.0006] | 0.0014 |
| product1 | 3.5 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0001 |
| product1 | 3.5 | 2.6 | raw | centroid_amp | 0.8629 | [0.8551, 0.8708] | 0.8311 |
| product1 | 3.5 | 2.6 | raw | centroid_power | 0.0523 | [0.0470, 0.0577] | 0.0579 |
| product1 | 3.5 | 2.6 | raw | centroid_band_power | -0.0008 | [-0.0012, -0.0004] | -0.0030 |
| product1 | 3.5 | 2.6 | hann | centroid_amp | 0.6181 | [0.6139, 0.6223] | 0.6061 |
| product1 | 3.5 | 2.6 | hann | centroid_power | 0.0048 | [0.0042, 0.0053] | 0.0094 |
| product1 | 3.5 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0003 |
| product1 | 5.5 | 0.9 | raw | centroid_amp | 0.8735 | [0.8640, 0.8830] | 0.8240 |
| product1 | 5.5 | 0.9 | raw | centroid_power | 0.0396 | [0.0306, 0.0486] | 0.0401 |
| product1 | 5.5 | 0.9 | raw | centroid_band_power | -0.0006 | [-0.0010, -0.0002] | -0.0021 |
| product1 | 5.5 | 0.9 | hann | centroid_amp | 0.0629 | [0.0624, 0.0634] | 0.0682 |
| product1 | 5.5 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 5.5 | 0.9 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 5.5 | 1.0 | raw | centroid_amp | 0.8758 | [0.8674, 0.8843] | 0.8285 |
| product1 | 5.5 | 1.0 | raw | centroid_power | 0.0398 | [0.0312, 0.0485] | 0.0403 |
| product1 | 5.5 | 1.0 | raw | centroid_band_power | -0.0006 | [-0.0010, -0.0003] | -0.0021 |
| product1 | 5.5 | 1.0 | hann | centroid_amp | 0.0001 | [0.0001, 0.0001] | 0.0002 |
| product1 | 5.5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 5.5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 5.5 | 1.25 | raw | centroid_amp | 0.8759 | [0.8675, 0.8843] | 0.8302 |
| product1 | 5.5 | 1.25 | raw | centroid_power | 0.0398 | [0.0321, 0.0475] | 0.0403 |
| product1 | 5.5 | 1.25 | raw | centroid_band_power | -0.0006 | [-0.0010, -0.0003] | -0.0021 |
| product1 | 5.5 | 1.25 | hann | centroid_amp | 0.2386 | [0.2373, 0.2400] | 0.2304 |
| product1 | 5.5 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| product1 | 5.5 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| product1 | 5.5 | 1.75 | raw | centroid_amp | 0.8630 | [0.8532, 0.8729] | 0.8165 |
| product1 | 5.5 | 1.75 | raw | centroid_power | 0.0390 | [0.0329, 0.0450] | 0.0408 |
| product1 | 5.5 | 1.75 | raw | centroid_band_power | -0.0006 | [-0.0009, -0.0003] | -0.0020 |
| product1 | 5.5 | 1.75 | hann | centroid_amp | 0.4702 | [0.4681, 0.4723] | 0.4506 |
| product1 | 5.5 | 1.75 | hann | centroid_power | 0.0008 | [0.0007, 0.0008] | 0.0024 |
| product1 | 5.5 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| product1 | 5.5 | 2.6 | raw | centroid_amp | 0.8336 | [0.8252, 0.8419] | 0.7931 |
| product1 | 5.5 | 2.6 | raw | centroid_power | 0.0403 | [0.0361, 0.0445] | 0.0471 |
| product1 | 5.5 | 2.6 | raw | centroid_band_power | -0.0006 | [-0.0009, -0.0002] | -0.0021 |
| product1 | 5.5 | 2.6 | hann | centroid_amp | 0.6442 | [0.6409, 0.6474] | 0.6132 |
| product1 | 5.5 | 2.6 | hann | centroid_power | 0.0066 | [0.0062, 0.0069] | 0.0135 |
| product1 | 5.5 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0001, -0.0000] | -0.0004 |
| product1 | 6.3 | 0.9 | raw | centroid_amp | 0.8814 | [0.8766, 0.8862] | 0.8391 |
| product1 | 6.3 | 0.9 | raw | centroid_power | 0.0327 | [0.0277, 0.0378] | 0.0335 |
| product1 | 6.3 | 0.9 | raw | centroid_band_power | -0.0001 | [-0.0004, 0.0001] | -0.0007 |
| product1 | 6.3 | 0.9 | hann | centroid_amp | 0.0566 | [0.0561, 0.0571] | 0.0692 |
| product1 | 6.3 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| product1 | 6.3 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 6.3 | 1.0 | raw | centroid_amp | 0.8817 | [0.8770, 0.8865] | 0.8399 |
| product1 | 6.3 | 1.0 | raw | centroid_power | 0.0329 | [0.0278, 0.0380] | 0.0337 |
| product1 | 6.3 | 1.0 | raw | centroid_band_power | -0.0001 | [-0.0004, 0.0002] | -0.0007 |
| product1 | 6.3 | 1.0 | hann | centroid_amp | 0.0001 | [0.0001, 0.0001] | 0.0002 |
| product1 | 6.3 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 6.3 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 6.3 | 1.25 | raw | centroid_amp | 0.8764 | [0.8698, 0.8830] | 0.8311 |
| product1 | 6.3 | 1.25 | raw | centroid_power | 0.0326 | [0.0275, 0.0377] | 0.0335 |
| product1 | 6.3 | 1.25 | raw | centroid_band_power | -0.0001 | [-0.0005, 0.0002] | -0.0006 |
| product1 | 6.3 | 1.25 | hann | centroid_amp | 0.2078 | [0.2067, 0.2089] | 0.2260 |
| product1 | 6.3 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| product1 | 6.3 | 1.25 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| product1 | 6.3 | 1.75 | raw | centroid_amp | 0.8491 | [0.8356, 0.8627] | 0.8013 |
| product1 | 6.3 | 1.75 | raw | centroid_power | 0.0316 | [0.0267, 0.0365] | 0.0340 |
| product1 | 6.3 | 1.75 | raw | centroid_band_power | -0.0001 | [-0.0007, 0.0004] | -0.0007 |
| product1 | 6.3 | 1.75 | hann | centroid_amp | 0.4103 | [0.4080, 0.4126] | 0.4405 |
| product1 | 6.3 | 1.75 | hann | centroid_power | 0.0010 | [0.0009, 0.0010] | 0.0029 |
| product1 | 6.3 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| product1 | 6.3 | 2.6 | raw | centroid_amp | 0.8110 | [0.7954, 0.8267] | 0.7752 |
| product1 | 6.3 | 2.6 | raw | centroid_power | 0.0338 | [0.0294, 0.0382] | 0.0417 |
| product1 | 6.3 | 2.6 | raw | centroid_band_power | -0.0002 | [-0.0008, 0.0005] | -0.0009 |
| product1 | 6.3 | 2.6 | hann | centroid_amp | 0.5674 | [0.5608, 0.5740] | 0.5980 |
| product1 | 6.3 | 2.6 | hann | centroid_power | 0.0076 | [0.0074, 0.0078] | 0.0152 |
| product1 | 6.3 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| oned | 3 | 0.9 | raw | centroid_amp | 0.0432 | [0.0427, 0.0436] | 0.0484 |
| oned | 3 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 3 | 0.9 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| oned | 3 | 0.9 | hann | centroid_amp | 0.0438 | [0.0433, 0.0444] | 0.0488 |
| oned | 3 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 3 | 0.9 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.0 | raw | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.0 | raw | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.25 | raw | centroid_amp | 0.2004 | [0.1981, 0.2026] | 0.1993 |
| oned | 3 | 1.25 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| oned | 3 | 1.25 | hann | centroid_amp | 0.2002 | [0.1980, 0.2024] | 0.1980 |
| oned | 3 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 3 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 3 | 1.75 | raw | centroid_amp | 0.4258 | [0.4210, 0.4306] | 0.4220 |
| oned | 3 | 1.75 | raw | centroid_power | 0.0003 | [0.0003, 0.0003] | 0.0009 |
| oned | 3 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| oned | 3 | 1.75 | hann | centroid_amp | 0.4248 | [0.4207, 0.4289] | 0.4185 |
| oned | 3 | 1.75 | hann | centroid_power | 0.0003 | [0.0002, 0.0003] | 0.0008 |
| oned | 3 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0001 |
| oned | 3 | 2.6 | raw | centroid_amp | 0.6005 | [0.5948, 0.6063] | 0.5930 |
| oned | 3 | 2.6 | raw | centroid_power | 0.0032 | [0.0031, 0.0033] | 0.0063 |
| oned | 3 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| oned | 3 | 2.6 | hann | centroid_amp | 0.5981 | [0.5933, 0.6028] | 0.5873 |
| oned | 3 | 2.6 | hann | centroid_power | 0.0031 | [0.0029, 0.0033] | 0.0061 |
| oned | 3 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0001, -0.0000] | -0.0003 |
| oned | 5 | 0.9 | raw | centroid_amp | 0.0463 | [0.0460, 0.0465] | 0.0520 |
| oned | 5 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 5 | 0.9 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| oned | 5 | 0.9 | hann | centroid_amp | 0.0476 | [0.0473, 0.0479] | 0.0528 |
| oned | 5 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 5 | 1.0 | raw | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5 | 1.0 | raw | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5 | 1.25 | raw | centroid_amp | 0.1999 | [0.1985, 0.2014] | 0.1989 |
| oned | 5 | 1.25 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| oned | 5 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| oned | 5 | 1.25 | hann | centroid_amp | 0.2026 | [0.2016, 0.2036] | 0.1991 |
| oned | 5 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| oned | 5 | 1.25 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5 | 1.75 | raw | centroid_amp | 0.4250 | [0.4217, 0.4282] | 0.4213 |
| oned | 5 | 1.75 | raw | centroid_power | 0.0005 | [0.0005, 0.0005] | 0.0016 |
| oned | 5 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| oned | 5 | 1.75 | hann | centroid_amp | 0.4286 | [0.4264, 0.4308] | 0.4201 |
| oned | 5 | 1.75 | hann | centroid_power | 0.0005 | [0.0005, 0.0006] | 0.0016 |
| oned | 5 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0001 |
| oned | 5 | 2.6 | raw | centroid_amp | 0.5996 | [0.5955, 0.6037] | 0.5921 |
| oned | 5 | 2.6 | raw | centroid_power | 0.0047 | [0.0047, 0.0048] | 0.0094 |
| oned | 5 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| oned | 5 | 2.6 | hann | centroid_amp | 0.6018 | [0.5986, 0.6050] | 0.5887 |
| oned | 5 | 2.6 | hann | centroid_power | 0.0048 | [0.0046, 0.0049] | 0.0093 |
| oned | 5 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0003 |
| oned | 7 | 0.9 | raw | centroid_amp | 0.0486 | [0.0484, 0.0488] | 0.0547 |
| oned | 7 | 0.9 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 7 | 0.9 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| oned | 7 | 0.9 | hann | centroid_amp | 0.0493 | [0.0491, 0.0495] | 0.0556 |
| oned | 7 | 0.9 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 7 | 0.9 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 7 | 1.0 | raw | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 7 | 1.0 | raw | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 7 | 1.0 | raw | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 7 | 1.0 | hann | centroid_amp | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 7 | 1.0 | hann | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 7 | 1.0 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 7 | 1.25 | raw | centroid_amp | 0.1998 | [0.1987, 0.2008] | 0.1987 |
| oned | 7 | 1.25 | raw | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| oned | 7 | 1.25 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0000 |
| oned | 7 | 1.25 | hann | centroid_amp | 0.2011 | [0.2002, 0.2020] | 0.1992 |
| oned | 7 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0002 |
| oned | 7 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 7 | 1.75 | raw | centroid_amp | 0.4246 | [0.4221, 0.4272] | 0.4207 |
| oned | 7 | 1.75 | raw | centroid_power | 0.0008 | [0.0008, 0.0008] | 0.0023 |
| oned | 7 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| oned | 7 | 1.75 | hann | centroid_amp | 0.4261 | [0.4239, 0.4283] | 0.4200 |
| oned | 7 | 1.75 | hann | centroid_power | 0.0008 | [0.0007, 0.0008] | 0.0023 |
| oned | 7 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0001 |
| oned | 7 | 2.6 | raw | centroid_amp | 0.5993 | [0.5959, 0.6026] | 0.5914 |
| oned | 7 | 2.6 | raw | centroid_power | 0.0061 | [0.0061, 0.0062] | 0.0121 |
| oned | 7 | 2.6 | raw | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |
| oned | 7 | 2.6 | hann | centroid_amp | 0.5994 | [0.5961, 0.6026] | 0.5882 |
| oned | 7 | 2.6 | hann | centroid_power | 0.0061 | [0.0059, 0.0062] | 0.0120 |
| oned | 7 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0004 |
| oned | 3.5 | 0.9 | raw | centroid_amp | 0.8719 | [0.8598, 0.8840] | 0.8274 |
| oned | 3.5 | 0.9 | raw | centroid_power | 0.0410 | [0.0294, 0.0526] | 0.0421 |
| oned | 3.5 | 0.9 | raw | centroid_band_power | -0.0005 | [-0.0013, 0.0002] | -0.0021 |
| oned | 3.5 | 0.9 | hann | centroid_amp | 0.0457 | [0.0447, 0.0468] | 0.0494 |
| oned | 3.5 | 0.9 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 3.5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 3.5 | 1.0 | raw | centroid_amp | 0.8742 | [0.8657, 0.8827] | 0.8322 |
| oned | 3.5 | 1.0 | raw | centroid_power | 0.0416 | [0.0306, 0.0527] | 0.0428 |
| oned | 3.5 | 1.0 | raw | centroid_band_power | -0.0005 | [-0.0012, 0.0002] | -0.0020 |
| oned | 3.5 | 1.0 | hann | centroid_amp | 0.0001 | [-0.0000, 0.0001] | 0.0002 |
| oned | 3.5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 3.5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 3.5 | 1.25 | raw | centroid_amp | 0.8750 | [0.8698, 0.8802] | 0.8364 |
| oned | 3.5 | 1.25 | raw | centroid_power | 0.0425 | [0.0328, 0.0521] | 0.0437 |
| oned | 3.5 | 1.25 | raw | centroid_band_power | -0.0004 | [-0.0012, 0.0003] | -0.0019 |
| oned | 3.5 | 1.25 | hann | centroid_amp | 0.1981 | [0.1946, 0.2017] | 0.1923 |
| oned | 3.5 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0000 |
| oned | 3.5 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 3.5 | 1.75 | raw | centroid_amp | 0.8662 | [0.8597, 0.8727] | 0.8275 |
| oned | 3.5 | 1.75 | raw | centroid_power | 0.0425 | [0.0350, 0.0500] | 0.0444 |
| oned | 3.5 | 1.75 | raw | centroid_band_power | -0.0004 | [-0.0011, 0.0004] | -0.0017 |
| oned | 3.5 | 1.75 | hann | centroid_amp | 0.4198 | [0.4143, 0.4252] | 0.4064 |
| oned | 3.5 | 1.75 | hann | centroid_power | 0.0004 | [0.0003, 0.0005] | 0.0011 |
| oned | 3.5 | 1.75 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 3.5 | 2.6 | raw | centroid_amp | 0.8440 | [0.8348, 0.8532] | 0.8048 |
| oned | 3.5 | 2.6 | raw | centroid_power | 0.0426 | [0.0378, 0.0475] | 0.0472 |
| oned | 3.5 | 2.6 | raw | centroid_band_power | -0.0003 | [-0.0010, 0.0005] | -0.0016 |
| oned | 3.5 | 2.6 | hann | centroid_amp | 0.5900 | [0.5836, 0.5963] | 0.5707 |
| oned | 3.5 | 2.6 | hann | centroid_power | 0.0039 | [0.0033, 0.0044] | 0.0072 |
| oned | 3.5 | 2.6 | hann | centroid_band_power | 0.0000 | [-0.0000, 0.0001] | -0.0002 |
| oned | 5.5 | 0.9 | raw | centroid_amp | 0.8508 | [0.8287, 0.8729] | 0.7893 |
| oned | 5.5 | 0.9 | raw | centroid_power | 0.0295 | [0.0206, 0.0384] | 0.0299 |
| oned | 5.5 | 0.9 | raw | centroid_band_power | -0.0004 | [-0.0011, 0.0002] | -0.0016 |
| oned | 5.5 | 0.9 | hann | centroid_amp | 0.0486 | [0.0481, 0.0490] | 0.0522 |
| oned | 5.5 | 0.9 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5.5 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5.5 | 1.0 | raw | centroid_amp | 0.8553 | [0.8393, 0.8714] | 0.7963 |
| oned | 5.5 | 1.0 | raw | centroid_power | 0.0299 | [0.0214, 0.0384] | 0.0303 |
| oned | 5.5 | 1.0 | raw | centroid_band_power | -0.0004 | [-0.0011, 0.0002] | -0.0015 |
| oned | 5.5 | 1.0 | hann | centroid_amp | -0.0000 | [-0.0001, 0.0001] | 0.0000 |
| oned | 5.5 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5.5 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5.5 | 1.25 | raw | centroid_amp | 0.8570 | [0.8469, 0.8670] | 0.8005 |
| oned | 5.5 | 1.25 | raw | centroid_power | 0.0303 | [0.0229, 0.0378] | 0.0309 |
| oned | 5.5 | 1.25 | raw | centroid_band_power | -0.0004 | [-0.0010, 0.0003] | -0.0013 |
| oned | 5.5 | 1.25 | hann | centroid_amp | 0.2033 | [0.2018, 0.2049] | 0.1924 |
| oned | 5.5 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| oned | 5.5 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 5.5 | 1.75 | raw | centroid_amp | 0.8423 | [0.8322, 0.8523] | 0.7865 |
| oned | 5.5 | 1.75 | raw | centroid_power | 0.0304 | [0.0247, 0.0361] | 0.0321 |
| oned | 5.5 | 1.75 | raw | centroid_band_power | -0.0003 | [-0.0010, 0.0004] | -0.0011 |
| oned | 5.5 | 1.75 | hann | centroid_amp | 0.4325 | [0.4295, 0.4356] | 0.4062 |
| oned | 5.5 | 1.75 | hann | centroid_power | 0.0006 | [0.0005, 0.0006] | 0.0017 |
| oned | 5.5 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0001 |
| oned | 5.5 | 2.6 | raw | centroid_amp | 0.8089 | [0.7998, 0.8180] | 0.7610 |
| oned | 5.5 | 2.6 | raw | centroid_power | 0.0322 | [0.0285, 0.0360] | 0.0379 |
| oned | 5.5 | 2.6 | raw | centroid_band_power | -0.0003 | [-0.0010, 0.0004] | -0.0010 |
| oned | 5.5 | 2.6 | hann | centroid_amp | 0.6095 | [0.6043, 0.6146] | 0.5707 |
| oned | 5.5 | 2.6 | hann | centroid_power | 0.0049 | [0.0045, 0.0052] | 0.0100 |
| oned | 5.5 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0001, 0.0000] | -0.0003 |
| oned | 6.3 | 0.9 | raw | centroid_amp | 0.8392 | [0.8131, 0.8653] | 0.7737 |
| oned | 6.3 | 0.9 | raw | centroid_power | 0.0223 | [0.0157, 0.0288] | 0.0228 |
| oned | 6.3 | 0.9 | raw | centroid_band_power | -0.0001 | [-0.0004, 0.0003] | -0.0005 |
| oned | 6.3 | 0.9 | hann | centroid_amp | 0.0437 | [0.0431, 0.0443] | 0.0529 |
| oned | 6.3 | 0.9 | hann | centroid_power | 0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 6.3 | 0.9 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 6.3 | 1.0 | raw | centroid_amp | 0.8390 | [0.8125, 0.8655] | 0.7734 |
| oned | 6.3 | 1.0 | raw | centroid_power | 0.0223 | [0.0157, 0.0290] | 0.0229 |
| oned | 6.3 | 1.0 | raw | centroid_band_power | -0.0001 | [-0.0004, 0.0003] | -0.0004 |
| oned | 6.3 | 1.0 | hann | centroid_amp | 0.0001 | [-0.0000, 0.0002] | 0.0002 |
| oned | 6.3 | 1.0 | hann | centroid_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 6.3 | 1.0 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | 0.0000 |
| oned | 6.3 | 1.25 | raw | centroid_amp | 0.8243 | [0.7900, 0.8586] | 0.7559 |
| oned | 6.3 | 1.25 | raw | centroid_power | 0.0221 | [0.0153, 0.0288] | 0.0228 |
| oned | 6.3 | 1.25 | raw | centroid_band_power | -0.0001 | [-0.0005, 0.0004] | -0.0004 |
| oned | 6.3 | 1.25 | hann | centroid_amp | 0.1765 | [0.1753, 0.1778] | 0.1877 |
| oned | 6.3 | 1.25 | hann | centroid_power | 0.0000 | [0.0000, 0.0000] | 0.0001 |
| oned | 6.3 | 1.25 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0000 |
| oned | 6.3 | 1.75 | raw | centroid_amp | 0.7782 | [0.7266, 0.8299] | 0.7193 |
| oned | 6.3 | 1.75 | raw | centroid_power | 0.0214 | [0.0148, 0.0280] | 0.0233 |
| oned | 6.3 | 1.75 | raw | centroid_band_power | -0.0000 | [-0.0006, 0.0005] | -0.0004 |
| oned | 6.3 | 1.75 | hann | centroid_amp | 0.3769 | [0.3737, 0.3802] | 0.3957 |
| oned | 6.3 | 1.75 | hann | centroid_power | 0.0007 | [0.0007, 0.0007] | 0.0021 |
| oned | 6.3 | 1.75 | hann | centroid_band_power | -0.0000 | [-0.0000, 0.0000] | -0.0001 |
| oned | 6.3 | 2.6 | raw | centroid_amp | 0.7480 | [0.7047, 0.7912] | 0.7078 |
| oned | 6.3 | 2.6 | raw | centroid_power | 0.0235 | [0.0175, 0.0295] | 0.0295 |
| oned | 6.3 | 2.6 | raw | centroid_band_power | -0.0001 | [-0.0007, 0.0006] | -0.0005 |
| oned | 6.3 | 2.6 | hann | centroid_amp | 0.5362 | [0.5266, 0.5459] | 0.5558 |
| oned | 6.3 | 2.6 | hann | centroid_power | 0.0057 | [0.0055, 0.0059] | 0.0112 |
| oned | 6.3 | 2.6 | hann | centroid_band_power | -0.0000 | [-0.0000, -0.0000] | -0.0003 |

## Cells of the aliasing subset and of the normalisation check

Seed means by N (the N listed for each cell) and slopes over the part of the primary range that exists.

| sampling | r | normalize | seeds | f | gamma | processing | descriptor | N | means | slope (primary) | interval |
|---|---|---|---|---|---|---|---|---|---|---|---|
| decimate | 2 | maxabs | 10 | 5 | 0.9 | raw | centroid_amp | 128-4096 | 17.92, 20.87, 24.46, 29.06, 35.15, 43.18 | 0.2731 | [0.2637, 0.2825] |
| decimate | 2 | maxabs | 10 | 5 | 0.9 | raw | centroid_power | 128-4096 | 10.05, 10.05, 10.05, 10.05, 10.05, 10.05 | 0.0000 | [0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 0.9 | raw | centroid_band_power | 128-4096 | 9.47, 9.47, 9.47, 9.47, 9.47, 9.47 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 0.9 | hann | centroid_amp | 128-4096 | 17.83, 20.73, 24.23, 28.77, 34.74, 42.66 | 0.2716 | [0.2621, 0.2811] |
| decimate | 2 | maxabs | 10 | 5 | 0.9 | hann | centroid_power | 128-4096 | 10.07, 10.07, 10.07, 10.07, 10.07, 10.07 | 0.0000 | [0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 0.9 | hann | centroid_band_power | 128-4096 | 9.49, 9.49, 9.49, 9.49, 9.49, 9.49 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 0.9 | raw | centroid_amp | 128-2048 | 17.72, 20.55, 23.99, 28.44, 34.32 | 0.2578 | [0.2477, 0.2678] |
| decimate | 4 | maxabs | 10 | 5 | 0.9 | raw | centroid_power | 128-2048 | 10.05, 10.05, 10.05, 10.05, 10.05 | 0.0000 | [0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 0.9 | raw | centroid_band_power | 128-2048 | 9.47, 9.47, 9.47, 9.47, 9.47 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 0.9 | hann | centroid_amp | 128-2048 | 17.72, 20.54, 23.97, 28.41, 34.27 | 0.2575 | [0.2474, 0.2676] |
| decimate | 4 | maxabs | 10 | 5 | 0.9 | hann | centroid_power | 128-2048 | 10.07, 10.07, 10.07, 10.07, 10.07 | 0.0000 | [0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 0.9 | hann | centroid_band_power | 128-2048 | 9.49, 9.49, 9.49, 9.49, 9.49 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.0 | raw | centroid_amp | 128-4096 | 15.08, 15.08, 15.08, 15.08, 15.08, 15.08 | 0.0000 | [0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.0 | raw | centroid_power | 128-4096 | 9.98, 9.98, 9.98, 9.98, 9.98, 9.98 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.0 | raw | centroid_band_power | 128-4096 | 9.43, 9.43, 9.43, 9.43, 9.43, 9.43 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.0 | hann | centroid_amp | 128-4096 | 15.11, 15.11, 15.11, 15.11, 15.11, 15.11 | 0.0000 | [0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.0 | hann | centroid_power | 128-4096 | 10.00, 10.00, 10.00, 10.00, 10.00, 10.00 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.0 | hann | centroid_band_power | 128-4096 | 9.45, 9.45, 9.45, 9.45, 9.45, 9.45 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.0 | raw | centroid_amp | 128-2048 | 15.08, 15.08, 15.08, 15.08, 15.08 | 0.0000 | [0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.0 | raw | centroid_power | 128-2048 | 9.98, 9.98, 9.98, 9.98, 9.98 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.0 | raw | centroid_band_power | 128-2048 | 9.43, 9.43, 9.43, 9.43, 9.43 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.0 | hann | centroid_amp | 128-2048 | 15.11, 15.11, 15.11, 15.11, 15.11 | 0.0000 | [0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.0 | hann | centroid_power | 128-2048 | 10.00, 10.00, 10.00, 10.00, 10.00 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.0 | hann | centroid_band_power | 128-2048 | 9.45, 9.45, 9.45, 9.45, 9.45 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.25 | raw | centroid_amp | 128-4096 | 20.67, 28.01, 39.25, 56.87, 85.17, 130.73 | 0.5787 | [0.5734, 0.5841] |
| decimate | 2 | maxabs | 10 | 5 | 1.25 | raw | centroid_power | 128-4096 | 10.03, 10.05, 10.05, 10.05, 10.05, 10.05 | 0.0001 | [0.0001, 0.0001] |
| decimate | 2 | maxabs | 10 | 5 | 1.25 | raw | centroid_band_power | 128-4096 | 9.44, 9.44, 9.44, 9.44, 9.44, 9.44 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.25 | hann | centroid_amp | 128-4096 | 20.29, 27.31, 37.95, 54.87, 81.70, 125.39 | 0.5744 | [0.5688, 0.5801] |
| decimate | 2 | maxabs | 10 | 5 | 1.25 | hann | centroid_power | 128-4096 | 10.05, 10.07, 10.07, 10.07, 10.07, 10.07 | 0.0001 | [0.0001, 0.0001] |
| decimate | 2 | maxabs | 10 | 5 | 1.25 | hann | centroid_band_power | 128-4096 | 9.46, 9.46, 9.46, 9.46, 9.46, 9.46 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.25 | raw | centroid_amp | 128-2048 | 19.99, 26.70, 37.02, 53.21, 79.19 | 0.5481 | [0.5412, 0.5551] |
| decimate | 4 | maxabs | 10 | 5 | 1.25 | raw | centroid_power | 128-2048 | 10.03, 10.05, 10.05, 10.05, 10.05 | 0.0002 | [0.0002, 0.0002] |
| decimate | 4 | maxabs | 10 | 5 | 1.25 | raw | centroid_band_power | 128-2048 | 9.44, 9.44, 9.44, 9.44, 9.44 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.25 | hann | centroid_amp | 128-2048 | 19.93, 26.57, 36.77, 52.79, 78.54 | 0.5472 | [0.5401, 0.5542] |
| decimate | 4 | maxabs | 10 | 5 | 1.25 | hann | centroid_power | 128-2048 | 10.05, 10.07, 10.07, 10.07, 10.07 | 0.0002 | [0.0002, 0.0002] |
| decimate | 4 | maxabs | 10 | 5 | 1.25 | hann | centroid_band_power | 128-2048 | 9.46, 9.46, 9.46, 9.46, 9.46 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.75 | raw | centroid_amp | 128-4096 | 26.20, 41.52, 67.60, 112.67, 192.77, 336.21 | 0.7718 | [0.7703, 0.7732] |
| decimate | 2 | maxabs | 10 | 5 | 1.75 | raw | centroid_power | 128-4096 | 10.45, 10.61, 10.68, 10.71, 10.72, 10.73 | 0.0022 | [0.0021, 0.0023] |
| decimate | 2 | maxabs | 10 | 5 | 1.75 | raw | centroid_band_power | 128-4096 | 9.61, 9.61, 9.61, 9.61, 9.61, 9.61 | -0.0000 | [-0.0000, -0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 1.75 | hann | centroid_amp | 128-4096 | 25.19, 39.56, 63.60, 105.79, 179.48, 313.21 | 0.7663 | [0.7646, 0.7680] |
| decimate | 2 | maxabs | 10 | 5 | 1.75 | hann | centroid_power | 128-4096 | 10.47, 10.63, 10.70, 10.73, 10.74, 10.75 | 0.0022 | [0.0021, 0.0023] |
| decimate | 2 | maxabs | 10 | 5 | 1.75 | hann | centroid_band_power | 128-4096 | 9.63, 9.63, 9.63, 9.63, 9.63, 9.63 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.75 | raw | centroid_amp | 128-2048 | 24.56, 38.15, 61.25, 101.09, 171.60 | 0.7431 | [0.7404, 0.7457] |
| decimate | 4 | maxabs | 10 | 5 | 1.75 | raw | centroid_power | 128-2048 | 10.45, 10.61, 10.67, 10.70, 10.72 | 0.0030 | [0.0028, 0.0032] |
| decimate | 4 | maxabs | 10 | 5 | 1.75 | raw | centroid_band_power | 128-2048 | 9.61, 9.61, 9.61, 9.61, 9.61 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 1.75 | hann | centroid_amp | 128-2048 | 24.32, 37.63, 60.27, 99.27, 168.49 | 0.7415 | [0.7388, 0.7443] |
| decimate | 4 | maxabs | 10 | 5 | 1.75 | hann | centroid_power | 128-2048 | 10.47, 10.63, 10.69, 10.72, 10.74 | 0.0030 | [0.0028, 0.0032] |
| decimate | 4 | maxabs | 10 | 5 | 1.75 | hann | centroid_band_power | 128-2048 | 9.63, 9.63, 9.63, 9.63, 9.63 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 2.6 | raw | centroid_amp | 128-4096 | 30.51, 52.50, 92.30, 165.19, 302.18, 561.88 | 0.8689 | [0.8671, 0.8707] |
| decimate | 2 | maxabs | 10 | 5 | 2.6 | raw | centroid_power | 128-4096 | 11.25, 11.77, 12.07, 12.24, 12.34, 12.41 | 0.0133 | [0.0126, 0.0139] |
| decimate | 2 | maxabs | 10 | 5 | 2.6 | raw | centroid_band_power | 128-4096 | 9.92, 9.92, 9.92, 9.92, 9.92, 9.92 | -0.0000 | [-0.0000, -0.0000] |
| decimate | 2 | maxabs | 10 | 5 | 2.6 | hann | centroid_amp | 128-4096 | 28.88, 49.16, 85.16, 152.03, 275.27, 512.21 | 0.8622 | [0.8603, 0.8642] |
| decimate | 2 | maxabs | 10 | 5 | 2.6 | hann | centroid_power | 128-4096 | 11.27, 11.79, 12.08, 12.26, 12.36, 12.43 | 0.0133 | [0.0126, 0.0139] |
| decimate | 2 | maxabs | 10 | 5 | 2.6 | hann | centroid_band_power | 128-4096 | 9.93, 9.93, 9.93, 9.93, 9.93, 9.93 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 2.6 | raw | centroid_amp | 128-2048 | 28.01, 47.11, 81.58, 144.39, 261.75 | 0.8410 | [0.8385, 0.8434] |
| decimate | 4 | maxabs | 10 | 5 | 2.6 | raw | centroid_power | 128-2048 | 11.24, 11.76, 12.06, 12.24, 12.34 | 0.0167 | [0.0159, 0.0176] |
| decimate | 4 | maxabs | 10 | 5 | 2.6 | raw | centroid_band_power | 128-2048 | 9.92, 9.92, 9.92, 9.92, 9.92 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5 | 2.6 | hann | centroid_amp | 128-2048 | 27.51, 46.01, 79.43, 140.12, 253.98 | 0.8385 | [0.8359, 0.8412] |
| decimate | 4 | maxabs | 10 | 5 | 2.6 | hann | centroid_power | 128-2048 | 11.26, 11.78, 12.08, 12.26, 12.36 | 0.0167 | [0.0158, 0.0175] |
| decimate | 4 | maxabs | 10 | 5 | 2.6 | hann | centroid_band_power | 128-2048 | 9.93, 9.93, 9.93, 9.93, 9.93 | -0.0000 | [-0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5 | 0.9 | raw | centroid_amp | 128-4096 | 19.77, 23.37, 27.91, 33.83, 41.57, 51.68 | 0.2959 | [0.2813, 0.3105] |
| direct | 1 | ampsum | 5 | 5 | 0.9 | raw | centroid_power | 128-4096 | 10.03, 10.03, 10.03, 10.03, 10.03, 10.03 | 0.0000 | [0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5 | 0.9 | raw | centroid_band_power | 128-4096 | 9.45, 9.45, 9.45, 9.45, 9.45, 9.45 | -0.0000 | [-0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5 | 0.9 | hann | centroid_amp | 128-4096 | 19.12, 22.33, 26.48, 31.78, 38.92, 48.00 | 0.2863 | [0.2715, 0.3011] |
| direct | 1 | ampsum | 5 | 5 | 0.9 | hann | centroid_power | 128-4096 | 10.05, 10.05, 10.05, 10.05, 10.05, 10.05 | 0.0000 | [0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5 | 0.9 | hann | centroid_band_power | 128-4096 | 9.47, 9.47, 9.47, 9.47, 9.47, 9.47 | -0.0000 | [-0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5 | 1.75 | raw | centroid_amp | 128-4096 | 32.74, 54.09, 91.65, 158.51, 278.53, 494.83 | 0.8111 | [0.8094, 0.8129] |
| direct | 1 | ampsum | 5 | 5 | 1.75 | raw | centroid_power | 128-4096 | 10.63, 10.73, 10.77, 10.79, 10.80, 10.80 | 0.0014 | [0.0013, 0.0015] |
| direct | 1 | ampsum | 5 | 5 | 1.75 | raw | centroid_band_power | 128-4096 | 9.66, 9.65, 9.65, 9.65, 9.65, 9.65 | -0.0000 | [-0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5 | 1.75 | hann | centroid_amp | 128-4096 | 30.11, 47.92, 79.99, 134.63, 235.90, 410.40 | 0.7886 | [0.7861, 0.7911] |
| direct | 1 | ampsum | 5 | 5 | 1.75 | hann | centroid_power | 128-4096 | 10.65, 10.75, 10.79, 10.81, 10.82, 10.82 | 0.0014 | [0.0013, 0.0015] |
| direct | 1 | ampsum | 5 | 5 | 1.75 | hann | centroid_band_power | 128-4096 | 9.67, 9.67, 9.67, 9.67, 9.67, 9.67 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 0.9 | raw | centroid_amp | 128-4096 | 19.97, 31.08, 51.59, 90.22, 163.23, 301.65 | 0.8367 | [0.7983, 0.8750] |
| decimate | 2 | maxabs | 10 | 5.5 | 0.9 | raw | centroid_power | 128-4096 | 11.61, 11.80, 12.00, 12.20, 12.41, 12.62 | 0.0235 | [0.0136, 0.0334] |
| decimate | 2 | maxabs | 10 | 5.5 | 0.9 | raw | centroid_band_power | 128-4096 | 10.77, 10.76, 10.76, 10.76, 10.76, 10.76 | -0.0002 | [-0.0003, 0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 0.9 | hann | centroid_amp | 128-4096 | 18.88, 21.91, 25.40, 30.32, 36.72, 45.02 | 0.2749 | [0.2654, 0.2844] |
| decimate | 2 | maxabs | 10 | 5.5 | 0.9 | hann | centroid_power | 128-4096 | 11.07, 11.07, 11.07, 11.07, 11.07, 11.07 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 0.9 | hann | centroid_band_power | 128-4096 | 10.40, 10.40, 10.40, 10.40, 10.40, 10.40 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 0.9 | raw | centroid_amp | 128-2048 | 19.68, 30.56, 50.61, 88.38, 159.74 | 0.8133 | [0.7660, 0.8605] |
| decimate | 4 | maxabs | 10 | 5.5 | 0.9 | raw | centroid_power | 128-2048 | 11.58, 11.77, 11.97, 12.18, 12.38 | 0.0237 | [0.0137, 0.0338] |
| decimate | 4 | maxabs | 10 | 5.5 | 0.9 | raw | centroid_band_power | 128-2048 | 10.76, 10.76, 10.76, 10.76, 10.76 | -0.0001 | [-0.0002, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 0.9 | hann | centroid_amp | 128-2048 | 18.77, 21.80, 25.35, 30.06, 36.28 | 0.2582 | [0.2479, 0.2684] |
| decimate | 4 | maxabs | 10 | 5.5 | 0.9 | hann | centroid_power | 128-2048 | 11.07, 11.07, 11.07, 11.07, 11.07 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 0.9 | hann | centroid_band_power | 128-2048 | 10.40, 10.40, 10.40, 10.40, 10.40 | -0.0000 | [-0.0000, -0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.0 | raw | centroid_amp | 128-4096 | 19.15, 29.76, 50.22, 89.26, 163.50, 304.64 | 0.8594 | [0.8360, 0.8827] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.0 | raw | centroid_power | 128-4096 | 11.54, 11.72, 11.92, 12.12, 12.33, 12.54 | 0.0236 | [0.0139, 0.0333] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.0 | raw | centroid_band_power | 128-4096 | 10.73, 10.72, 10.71, 10.71, 10.71, 10.71 | -0.0002 | [-0.0003, -0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.0 | hann | centroid_amp | 128-4096 | 16.18, 16.19, 16.20, 16.20, 16.20, 16.20 | 0.0002 | [0.0001, 0.0002] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.0 | hann | centroid_power | 128-4096 | 11.00, 11.00, 11.00, 11.00, 11.00, 11.00 | -0.0000 | [-0.0000, -0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.0 | hann | centroid_band_power | 128-4096 | 10.36, 10.36, 10.36, 10.36, 10.36, 10.36 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.0 | raw | centroid_amp | 128-2048 | 18.84, 29.21, 49.20, 87.36, 159.92 | 0.8385 | [0.8054, 0.8716] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.0 | raw | centroid_power | 128-2048 | 11.51, 11.69, 11.89, 12.10, 12.30 | 0.0238 | [0.0140, 0.0336] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.0 | raw | centroid_band_power | 128-2048 | 10.72, 10.71, 10.71, 10.71, 10.71 | -0.0001 | [-0.0002, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.0 | hann | centroid_amp | 128-2048 | 16.19, 16.21, 16.21, 16.22, 16.22 | 0.0002 | [0.0002, 0.0003] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.0 | hann | centroid_power | 128-2048 | 11.00, 11.00, 11.00, 11.00, 11.00 | -0.0000 | [-0.0000, -0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.0 | hann | centroid_band_power | 128-2048 | 10.36, 10.36, 10.36, 10.36, 10.36 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.25 | raw | centroid_amp | 128-4096 | 21.14, 33.75, 56.09, 97.24, 173.38, 315.43 | 0.8242 | [0.7962, 0.8522] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.25 | raw | centroid_power | 128-4096 | 11.57, 11.78, 11.98, 12.18, 12.39, 12.59 | 0.0233 | [0.0144, 0.0323] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.25 | raw | centroid_band_power | 128-4096 | 10.72, 10.71, 10.71, 10.71, 10.71, 10.71 | -0.0001 | [-0.0003, -0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.25 | hann | centroid_amp | 128-4096 | 21.26, 28.23, 38.36, 56.19, 84.27, 128.77 | 0.5823 | [0.5770, 0.5877] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.25 | hann | centroid_power | 128-4096 | 11.04, 11.07, 11.08, 11.08, 11.08, 11.08 | 0.0001 | [0.0001, 0.0001] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.25 | hann | centroid_band_power | 128-4096 | 10.36, 10.36, 10.36, 10.36, 10.36, 10.36 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.25 | raw | centroid_amp | 128-2048 | 20.86, 33.26, 55.16, 95.47, 170.02 | 0.8051 | [0.7745, 0.8356] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.25 | raw | centroid_power | 128-2048 | 11.54, 11.75, 11.95, 12.15, 12.36 | 0.0236 | [0.0145, 0.0327] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.25 | raw | centroid_band_power | 128-2048 | 10.71, 10.71, 10.71, 10.71, 10.71 | -0.0001 | [-0.0002, -0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.25 | hann | centroid_amp | 128-2048 | 20.85, 27.74, 38.00, 54.56, 81.07 | 0.5463 | [0.5390, 0.5536] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.25 | hann | centroid_power | 128-2048 | 11.04, 11.07, 11.08, 11.08, 11.08 | 0.0002 | [0.0002, 0.0002] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.25 | hann | centroid_band_power | 128-2048 | 10.36, 10.36, 10.36, 10.36, 10.36 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.75 | raw | centroid_amp | 128-4096 | 24.21, 40.48, 68.37, 118.98, 210.53, 377.60 | 0.8214 | [0.8135, 0.8292] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.75 | raw | centroid_power | 128-4096 | 11.99, 12.35, 12.62, 12.85, 13.07, 13.27 | 0.0238 | [0.0163, 0.0313] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.75 | raw | centroid_band_power | 128-4096 | 10.86, 10.85, 10.85, 10.85, 10.85, 10.85 | -0.0001 | [-0.0003, -0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.75 | hann | centroid_amp | 128-4096 | 26.11, 40.03, 62.48, 106.51, 182.78, 317.19 | 0.7811 | [0.7797, 0.7824] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.75 | hann | centroid_power | 128-4096 | 11.49, 11.68, 11.75, 11.79, 11.81, 11.82 | 0.0025 | [0.0023, 0.0026] |
| decimate | 2 | maxabs | 10 | 5.5 | 1.75 | hann | centroid_band_power | 128-4096 | 10.52, 10.52, 10.52, 10.52, 10.52, 10.52 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.75 | raw | centroid_amp | 128-2048 | 23.82, 39.90, 67.21, 116.77, 206.35 | 0.8085 | [0.8008, 0.8163] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.75 | raw | centroid_power | 128-2048 | 11.96, 12.33, 12.59, 12.83, 13.04 | 0.0248 | [0.0173, 0.0323] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.75 | raw | centroid_band_power | 128-2048 | 10.85, 10.85, 10.85, 10.85, 10.85 | -0.0001 | [-0.0002, -0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.75 | hann | centroid_amp | 128-2048 | 25.05, 38.65, 61.16, 100.98, 171.23 | 0.7426 | [0.7399, 0.7452] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.75 | hann | centroid_power | 128-2048 | 11.48, 11.67, 11.75, 11.79, 11.81 | 0.0033 | [0.0031, 0.0035] |
| decimate | 4 | maxabs | 10 | 5.5 | 1.75 | hann | centroid_band_power | 128-2048 | 10.52, 10.52, 10.52, 10.52, 10.52 | 0.0000 | [-0.0000, 0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 2.6 | raw | centroid_amp | 128-4096 | 27.04, 47.05, 82.23, 147.71, 268.75, 493.29 | 0.8618 | [0.8587, 0.8649] |
| decimate | 2 | maxabs | 10 | 5.5 | 2.6 | raw | centroid_power | 128-4096 | 12.78, 13.55, 14.07, 14.47, 14.78, 15.05 | 0.0319 | [0.0266, 0.0373] |
| decimate | 2 | maxabs | 10 | 5.5 | 2.6 | raw | centroid_band_power | 128-4096 | 11.12, 11.11, 11.11, 11.10, 11.10, 11.10 | -0.0001 | [-0.0003, 0.0000] |
| decimate | 2 | maxabs | 10 | 5.5 | 2.6 | hann | centroid_amp | 128-4096 | 29.78, 49.16, 82.63, 152.12, 278.91, 515.68 | 0.8800 | [0.8775, 0.8826] |
| decimate | 2 | maxabs | 10 | 5.5 | 2.6 | hann | centroid_power | 128-4096 | 12.31, 12.91, 13.25, 13.46, 13.58, 13.66 | 0.0144 | [0.0136, 0.0151] |
| decimate | 2 | maxabs | 10 | 5.5 | 2.6 | hann | centroid_band_power | 128-4096 | 10.79, 10.79, 10.79, 10.79, 10.79, 10.79 | -0.0000 | [-0.0000, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 2.6 | raw | centroid_amp | 128-2048 | 26.38, 46.12, 80.21, 143.67, 260.58 | 0.8500 | [0.8469, 0.8531] |
| decimate | 4 | maxabs | 10 | 5.5 | 2.6 | raw | centroid_power | 128-2048 | 12.73, 13.51, 14.04, 14.44, 14.76 | 0.0357 | [0.0303, 0.0410] |
| decimate | 4 | maxabs | 10 | 5.5 | 2.6 | raw | centroid_band_power | 128-2048 | 11.11, 11.11, 11.10, 11.10, 11.10 | -0.0001 | [-0.0002, 0.0000] |
| decimate | 4 | maxabs | 10 | 5.5 | 2.6 | hann | centroid_amp | 128-2048 | 28.04, 46.73, 79.80, 141.40, 255.99 | 0.8408 | [0.8385, 0.8431] |
| decimate | 4 | maxabs | 10 | 5.5 | 2.6 | hann | centroid_power | 128-2048 | 12.29, 12.90, 13.24, 13.46, 13.58 | 0.0181 | [0.0172, 0.0191] |
| decimate | 4 | maxabs | 10 | 5.5 | 2.6 | hann | centroid_band_power | 128-2048 | 10.79, 10.79, 10.79, 10.79, 10.79 | 0.0000 | [-0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5.5 | 0.9 | raw | centroid_amp | 128-4096 | 21.25, 33.06, 55.08, 96.60, 175.08, 323.69 | 0.8304 | [0.7468, 0.9139] |
| direct | 1 | ampsum | 5 | 5.5 | 0.9 | raw | centroid_power | 128-4096 | 11.73, 11.93, 12.14, 12.35, 12.57, 12.78 | 0.0232 | [-0.0014, 0.0477] |
| direct | 1 | ampsum | 5 | 5.5 | 0.9 | raw | centroid_band_power | 128-4096 | 10.79, 10.76, 10.76, 10.75, 10.75, 10.75 | -0.0003 | [-0.0009, 0.0004] |
| direct | 1 | ampsum | 5 | 5.5 | 0.9 | hann | centroid_amp | 128-4096 | 20.16, 23.71, 27.19, 31.83, 40.59, 50.86 | 0.3057 | [0.2886, 0.3228] |
| direct | 1 | ampsum | 5 | 5.5 | 0.9 | hann | centroid_power | 128-4096 | 11.05, 11.05, 11.06, 11.06, 11.06, 11.06 | 0.0000 | [0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5.5 | 0.9 | hann | centroid_band_power | 128-4096 | 10.39, 10.39, 10.39, 10.39, 10.39, 10.39 | -0.0000 | [-0.0000, 0.0000] |
| direct | 1 | ampsum | 5 | 5.5 | 1.75 | raw | centroid_amp | 128-4096 | 27.37, 45.61, 77.11, 134.52, 241.43, 437.69 | 0.8355 | [0.8274, 0.8436] |
| direct | 1 | ampsum | 5 | 5.5 | 1.75 | raw | centroid_power | 128-4096 | 12.30, 12.61, 12.87, 13.09, 13.31, 13.52 | 0.0228 | [0.0042, 0.0414] |
| direct | 1 | ampsum | 5 | 5.5 | 1.75 | raw | centroid_band_power | 128-4096 | 10.93, 10.90, 10.90, 10.89, 10.89, 10.89 | -0.0002 | [-0.0008, 0.0004] |
| direct | 1 | ampsum | 5 | 5.5 | 1.75 | hann | centroid_amp | 128-4096 | 30.98, 49.91, 76.30, 124.67, 237.07, 423.12 | 0.8340 | [0.8303, 0.8377] |
| direct | 1 | ampsum | 5 | 5.5 | 1.75 | hann | centroid_power | 128-4096 | 11.69, 11.81, 11.86, 11.88, 11.89, 11.90 | 0.0016 | [0.0015, 0.0016] |
| direct | 1 | ampsum | 5 | 5.5 | 1.75 | hann | centroid_band_power | 128-4096 | 10.56, 10.55, 10.55, 10.55, 10.55, 10.55 | 0.0000 | [-0.0000, 0.0000] |

## Seed means of the centroid by N

| field | f | gamma | processing | descriptor | N 128 ... 4096 (mean; standard error of the last) |
|---|---|---|---|---|---|
| sum | 3 | 0.9 | raw | centroid_amp | 13.10, 15.49, 18.60, 22.67, 28.01, 34.98 (0.43) |
| sum | 3 | 0.9 | raw | centroid_power | 6.03, 6.03, 6.03, 6.03, 6.03, 6.03 (0.0044) |
| sum | 3 | 0.9 | raw | centroid_band_power | 5.68, 5.68, 5.68, 5.68, 5.68, 5.68 (0.0039) |
| sum | 3 | 0.9 | hann | centroid_amp | 12.50, 14.62, 17.40, 21.05, 25.84, 32.11 (0.36) |
| sum | 3 | 0.9 | hann | centroid_power | 6.06, 6.06, 6.06, 6.06, 6.06, 6.06 (0.0044) |
| sum | 3 | 0.9 | hann | centroid_band_power | 5.72, 5.72, 5.72, 5.72, 5.72, 5.72 (0.0039) |
| sum | 3 | 1.0 | raw | centroid_amp | 9.05, 9.05, 9.05, 9.05, 9.05, 9.05 (8.4e-13) |
| sum | 3 | 1.0 | raw | centroid_power | 5.99, 5.99, 5.99, 5.99, 5.99, 5.99 (3.2e-16) |
| sum | 3 | 1.0 | raw | centroid_band_power | 5.66, 5.66, 5.66, 5.66, 5.66, 5.66 (4.8e-16) |
| sum | 3 | 1.0 | hann | centroid_amp | 9.09, 9.09, 9.09, 9.09, 9.09, 9.09 (4.3e-13) |
| sum | 3 | 1.0 | hann | centroid_power | 6.02, 6.02, 6.02, 6.02, 6.02, 6.02 (2.7e-16) |
| sum | 3 | 1.0 | hann | centroid_band_power | 5.69, 5.69, 5.69, 5.69, 5.69, 5.69 (4e-16) |
| sum | 3 | 1.25 | raw | centroid_amp | 18.14, 25.91, 38.30, 58.19, 90.14, 141.50 (1.5) |
| sum | 3 | 1.25 | raw | centroid_power | 6.04, 6.04, 6.05, 6.05, 6.05, 6.05 (0.01) |
| sum | 3 | 1.25 | raw | centroid_band_power | 5.69, 5.69, 5.69, 5.69, 5.69, 5.69 (0.0075) |
| sum | 3 | 1.25 | hann | centroid_amp | 16.41, 22.85, 33.11, 49.59, 75.98, 118.37 (1.1) |
| sum | 3 | 1.25 | hann | centroid_power | 6.08, 6.08, 6.08, 6.08, 6.08, 6.08 (0.01) |
| sum | 3 | 1.25 | hann | centroid_band_power | 5.73, 5.73, 5.73, 5.73, 5.73, 5.73 (0.0075) |
| sum | 3 | 1.75 | raw | centroid_amp | 26.53, 43.97, 74.80, 129.83, 228.58, 406.68 (2.4) |
| sum | 3 | 1.75 | raw | centroid_power | 6.42, 6.46, 6.47, 6.48, 6.48, 6.48 (0.032) |
| sum | 3 | 1.75 | raw | centroid_band_power | 5.93, 5.93, 5.93, 5.93, 5.93, 5.93 (0.02) |
| sum | 3 | 1.75 | hann | centroid_amp | 23.33, 37.62, 62.70, 107.23, 186.58, 328.97 (1.8) |
| sum | 3 | 1.75 | hann | centroid_power | 6.46, 6.49, 6.50, 6.51, 6.51, 6.51 (0.032) |
| sum | 3 | 1.75 | hann | centroid_band_power | 5.96, 5.96, 5.96, 5.96, 5.96, 5.96 (0.02) |
| sum | 3 | 2.6 | raw | centroid_amp | 32.25, 57.50, 104.68, 193.78, 363.04, 686.39 (2.2) |
| sum | 3 | 2.6 | raw | centroid_power | 7.23, 7.39, 7.48, 7.53, 7.56, 7.58 (0.071) |
| sum | 3 | 2.6 | raw | centroid_band_power | 6.33, 6.33, 6.33, 6.33, 6.33, 6.33 (0.038) |
| sum | 3 | 2.6 | hann | centroid_amp | 28.36, 49.27, 88.01, 160.66, 297.66, 557.93 (1.7) |
| sum | 3 | 2.6 | hann | centroid_power | 7.27, 7.42, 7.51, 7.56, 7.59, 7.61 (0.071) |
| sum | 3 | 2.6 | hann | centroid_band_power | 6.37, 6.36, 6.36, 6.36, 6.36, 6.36 (0.038) |
| sum | 5 | 0.9 | raw | centroid_amp | 19.74, 23.29, 27.78, 33.62, 41.26, 51.25 (0.59) |
| sum | 5 | 0.9 | raw | centroid_power | 10.04, 10.04, 10.04, 10.04, 10.04, 10.04 (0.0074) |
| sum | 5 | 0.9 | raw | centroid_band_power | 9.46, 9.46, 9.46, 9.46, 9.46, 9.46 (0.0067) |
| sum | 5 | 0.9 | hann | centroid_amp | 19.10, 22.27, 26.37, 31.61, 38.66, 47.64 (0.51) |
| sum | 5 | 0.9 | hann | centroid_power | 10.06, 10.06, 10.06, 10.06, 10.06, 10.06 (0.0074) |
| sum | 5 | 0.9 | hann | centroid_band_power | 9.48, 9.48, 9.48, 9.48, 9.48, 9.48 (0.0067) |
| sum | 5 | 1.0 | raw | centroid_amp | 15.08, 15.08, 15.08, 15.08, 15.08, 15.08 (1.1e-12) |
| sum | 5 | 1.0 | raw | centroid_power | 9.98, 9.98, 9.98, 9.98, 9.98, 9.98 (8.5e-16) |
| sum | 5 | 1.0 | raw | centroid_band_power | 9.43, 9.43, 9.43, 9.43, 9.43, 9.43 (2.7e-16) |
| sum | 5 | 1.0 | hann | centroid_amp | 15.11, 15.11, 15.11, 15.11, 15.11, 15.11 (5.1e-13) |
| sum | 5 | 1.0 | hann | centroid_power | 10.00, 10.00, 10.00, 10.00, 10.00, 10.00 (5e-16) |
| sum | 5 | 1.0 | hann | centroid_band_power | 9.45, 9.45, 9.45, 9.45, 9.45, 9.45 (6.3e-16) |
| sum | 5 | 1.25 | raw | centroid_amp | 24.72, 34.87, 50.89, 76.54, 117.74, 183.98 (1.9) |
| sum | 5 | 1.25 | raw | centroid_power | 10.06, 10.07, 10.07, 10.08, 10.08, 10.08 (0.017) |
| sum | 5 | 1.25 | raw | centroid_band_power | 9.45, 9.45, 9.45, 9.45, 9.45, 9.45 (0.012) |
| sum | 5 | 1.25 | hann | centroid_amp | 23.11, 31.59, 45.43, 66.73, 102.23, 157.03 (1.5) |
| sum | 5 | 1.25 | hann | centroid_power | 10.08, 10.09, 10.10, 10.10, 10.10, 10.10 (0.017) |
| sum | 5 | 1.25 | hann | centroid_band_power | 9.47, 9.47, 9.47, 9.47, 9.47, 9.47 (0.012) |
| sum | 5 | 1.75 | raw | centroid_amp | 32.67, 53.89, 91.23, 157.76, 277.21, 492.61 (2.8) |
| sum | 5 | 1.75 | raw | centroid_power | 10.63, 10.73, 10.77, 10.79, 10.80, 10.80 (0.053) |
| sum | 5 | 1.75 | raw | centroid_band_power | 9.65, 9.64, 9.64, 9.64, 9.64, 9.64 (0.029) |
| sum | 5 | 1.75 | hann | centroid_amp | 30.05, 47.75, 79.65, 134.12, 234.89, 408.74 (2.3) |
| sum | 5 | 1.75 | hann | centroid_power | 10.65, 10.75, 10.79, 10.81, 10.82, 10.82 (0.053) |
| sum | 5 | 1.75 | hann | centroid_band_power | 9.66, 9.66, 9.66, 9.66, 9.66, 9.66 (0.029) |
| sum | 5 | 2.6 | raw | centroid_amp | 37.56, 66.84, 121.47, 224.46, 420.25, 794.23 (2.4) |
| sum | 5 | 2.6 | raw | centroid_power | 11.75, 12.14, 12.36, 12.49, 12.57, 12.61 (0.12) |
| sum | 5 | 2.6 | raw | centroid_band_power | 9.99, 9.98, 9.98, 9.98, 9.98, 9.98 (0.051) |
| sum | 5 | 2.6 | hann | centroid_amp | 34.64, 59.50, 106.69, 192.36, 359.07, 665.51 (2.1) |
| sum | 5 | 2.6 | hann | centroid_power | 11.77, 12.16, 12.38, 12.51, 12.59, 12.63 (0.12) |
| sum | 5 | 2.6 | hann | centroid_band_power | 10.00, 9.99, 9.99, 9.99, 9.99, 9.99 (0.051) |
| sum | 7 | 0.9 | raw | centroid_amp | 25.60, 30.36, 36.07, 43.43, 53.04, 65.61 (0.71) |
| sum | 7 | 0.9 | raw | centroid_power | 14.05, 14.06, 14.06, 14.06, 14.06, 14.06 (0.01) |
| sum | 7 | 0.9 | raw | centroid_band_power | 11.92, 11.92, 11.92, 11.92, 11.92, 11.92 (0.0034) |
| sum | 7 | 0.9 | hann | centroid_amp | 24.86, 29.64, 34.20, 41.12, 50.93, 60.87 (0.61) |
| sum | 7 | 0.9 | hann | centroid_power | 14.07, 14.07, 14.07, 14.07, 14.07, 14.07 (0.01) |
| sum | 7 | 0.9 | hann | centroid_band_power | 11.94, 11.94, 11.94, 11.94, 11.94, 11.94 (0.0033) |
| sum | 7 | 1.0 | raw | centroid_amp | 21.12, 21.12, 21.12, 21.12, 21.12, 21.12 (1.7e-12) |
| sum | 7 | 1.0 | raw | centroid_power | 13.98, 13.98, 13.98, 13.98, 13.98, 13.98 (5e-16) |
| sum | 7 | 1.0 | raw | centroid_band_power | 11.88, 11.88, 11.88, 11.88, 11.88, 11.88 (9.1e-16) |
| sum | 7 | 1.0 | hann | centroid_amp | 21.14, 21.14, 21.14, 21.14, 21.14, 21.14 (9.1e-13) |
| sum | 7 | 1.0 | hann | centroid_power | 13.99, 13.99, 13.99, 13.99, 13.99, 13.99 (6.1e-16) |
| sum | 7 | 1.0 | hann | centroid_band_power | 11.89, 11.89, 11.89, 11.89, 11.89, 11.89 (3.9e-16) |
| sum | 7 | 1.25 | raw | centroid_amp | 29.97, 42.14, 60.93, 90.90, 139.02, 216.41 (2.1) |
| sum | 7 | 1.25 | raw | centroid_power | 14.07, 14.10, 14.10, 14.11, 14.11, 14.11 (0.024) |
| sum | 7 | 1.25 | raw | centroid_band_power | 11.90, 11.90, 11.90, 11.90, 11.90, 11.90 (0.0063) |
| sum | 7 | 1.25 | hann | centroid_amp | 28.39, 39.75, 54.20, 80.70, 125.80, 183.88 (1.7) |
| sum | 7 | 1.25 | hann | centroid_power | 14.09, 14.11, 14.12, 14.12, 14.12, 14.12 (0.024) |
| sum | 7 | 1.25 | hann | centroid_band_power | 11.91, 11.91, 11.91, 11.91, 11.91, 11.91 (0.0064) |
| sum | 7 | 1.75 | raw | centroid_amp | 36.82, 60.87, 102.68, 177.05, 310.52, 551.28 (3) |
| sum | 7 | 1.75 | raw | centroid_power | 14.75, 14.97, 15.05, 15.09, 15.11, 15.12 (0.074) |
| sum | 7 | 1.75 | raw | centroid_band_power | 12.10, 12.10, 12.10, 12.10, 12.10, 12.10 (0.016) |
| sum | 7 | 1.75 | hann | centroid_amp | 34.50, 56.46, 89.51, 154.28, 274.42, 457.04 (2.5) |
| sum | 7 | 1.75 | hann | centroid_power | 14.77, 14.98, 15.07, 15.11, 15.13, 15.13 (0.074) |
| sum | 7 | 1.75 | hann | centroid_band_power | 12.09, 12.09, 12.09, 12.09, 12.09, 12.09 (0.016) |
| sum | 7 | 2.6 | raw | centroid_amp | 40.77, 72.80, 132.11, 243.87, 456.23, 861.98 (2.5) |
| sum | 7 | 2.6 | raw | centroid_power | 16.05, 16.77, 17.18, 17.41, 17.55, 17.63 (0.16) |
| sum | 7 | 2.6 | raw | centroid_band_power | 12.45, 12.43, 12.43, 12.43, 12.43, 12.43 (0.028) |
| sum | 7 | 2.6 | hann | centroid_amp | 38.37, 67.59, 116.43, 214.74, 404.66, 726.16 (2.3) |
| sum | 7 | 2.6 | hann | centroid_power | 16.07, 16.79, 17.19, 17.43, 17.57, 17.65 (0.16) |
| sum | 7 | 2.6 | hann | centroid_band_power | 12.41, 12.40, 12.39, 12.39, 12.39, 12.39 (0.026) |
| sum | 3.5 | 0.9 | raw | centroid_amp | 19.22, 31.84, 55.65, 100.67, 185.94, 347.89 (21) |
| sum | 3.5 | 0.9 | raw | centroid_power | 7.85, 8.05, 8.25, 8.46, 8.68, 8.89 (0.23) |
| sum | 3.5 | 0.9 | raw | centroid_band_power | 7.13, 7.10, 7.09, 7.09, 7.09, 7.09 (0.068) |
| sum | 3.5 | 0.9 | hann | centroid_amp | 13.85, 16.15, 18.77, 23.23, 28.33, 34.26 (0.38) |
| sum | 3.5 | 0.9 | hann | centroid_power | 7.06, 7.06, 7.06, 7.06, 7.06, 7.06 (0.0052) |
| sum | 3.5 | 0.9 | hann | centroid_band_power | 6.66, 6.66, 6.66, 6.66, 6.66, 6.66 (0.0046) |
| sum | 3.5 | 1.0 | raw | centroid_amp | 18.71, 31.37, 55.49, 101.27, 188.10, 353.05 (20) |
| sum | 3.5 | 1.0 | raw | centroid_power | 7.81, 8.01, 8.22, 8.42, 8.64, 8.85 (0.23) |
| sum | 3.5 | 1.0 | raw | centroid_band_power | 7.10, 7.08, 7.06, 7.06, 7.06, 7.06 (0.067) |
| sum | 3.5 | 1.0 | hann | centroid_amp | 10.33, 10.33, 10.33, 10.33, 10.33, 10.33 (0.0057) |
| sum | 3.5 | 1.0 | hann | centroid_power | 7.02, 7.02, 7.02, 7.02, 7.02, 7.02 (5.2e-05) |
| sum | 3.5 | 1.0 | hann | centroid_band_power | 6.63, 6.63, 6.63, 6.63, 6.63, 6.63 (5e-05) |
| sum | 3.5 | 1.25 | raw | centroid_amp | 20.60, 34.11, 59.05, 105.47, 192.04, 355.12 (16) |
| sum | 3.5 | 1.25 | raw | centroid_power | 7.87, 8.07, 8.28, 8.48, 8.70, 8.91 (0.21) |
| sum | 3.5 | 1.25 | raw | centroid_band_power | 7.14, 7.11, 7.10, 7.09, 7.09, 7.09 (0.064) |
| sum | 3.5 | 1.25 | hann | centroid_amp | 17.76, 24.35, 33.85, 52.88, 79.58, 118.48 (1.1) |
| sum | 3.5 | 1.25 | hann | centroid_power | 7.08, 7.08, 7.08, 7.08, 7.08, 7.08 (0.012) |
| sum | 3.5 | 1.25 | hann | centroid_band_power | 6.66, 6.66, 6.66, 6.66, 6.66, 6.66 (0.0086) |
| sum | 3.5 | 1.75 | raw | centroid_amp | 24.38, 40.91, 70.95, 125.97, 224.54, 408.33 (6.4) |
| sum | 3.5 | 1.75 | raw | centroid_power | 8.28, 8.52, 8.75, 8.96, 9.17, 9.39 (0.19) |
| sum | 3.5 | 1.75 | raw | centroid_band_power | 7.36, 7.33, 7.32, 7.31, 7.31, 7.31 (0.061) |
| sum | 3.5 | 1.75 | hann | centroid_amp | 24.79, 39.15, 62.67, 112.56, 191.26, 323.00 (1.8) |
| sum | 3.5 | 1.75 | hann | centroid_power | 7.51, 7.56, 7.58, 7.58, 7.59, 7.59 (0.037) |
| sum | 3.5 | 1.75 | hann | centroid_band_power | 6.90, 6.89, 6.89, 6.89, 6.89, 6.89 (0.023) |
| sum | 3.5 | 2.6 | raw | centroid_amp | 28.26, 49.03, 87.94, 160.86, 292.01, 545.19 (1.6) |
| sum | 3.5 | 2.6 | raw | centroid_power | 9.15, 9.55, 9.86, 10.14, 10.38, 10.61 (0.18) |
| sum | 3.5 | 2.6 | raw | centroid_band_power | 7.74, 7.71, 7.70, 7.70, 7.69, 7.69 (0.065) |
| sum | 3.5 | 2.6 | hann | centroid_amp | 29.86, 50.74, 87.90, 167.52, 302.74, 549.19 (1.7) |
| sum | 3.5 | 2.6 | hann | centroid_power | 8.41, 8.62, 8.74, 8.80, 8.84, 8.87 (0.083) |
| sum | 3.5 | 2.6 | hann | centroid_band_power | 7.30, 7.29, 7.29, 7.29, 7.29, 7.29 (0.042) |
| sum | 5.5 | 0.9 | raw | centroid_amp | 21.67, 34.23, 57.66, 101.89, 185.69, 344.80 (20) |
| sum | 5.5 | 0.9 | raw | centroid_power | 11.74, 11.94, 12.14, 12.35, 12.56, 12.77 (0.22) |
| sum | 5.5 | 0.9 | raw | centroid_band_power | 10.80, 10.78, 10.76, 10.76, 10.76, 10.76 (0.056) |
| sum | 5.5 | 0.9 | hann | centroid_amp | 20.14, 23.65, 27.10, 31.67, 40.31, 50.47 (0.54) |
| sum | 5.5 | 0.9 | hann | centroid_power | 11.06, 11.06, 11.07, 11.07, 11.07, 11.07 (0.0081) |
| sum | 5.5 | 0.9 | hann | centroid_band_power | 10.40, 10.40, 10.40, 10.40, 10.40, 10.40 (0.0073) |
| sum | 5.5 | 1.0 | raw | centroid_amp | 20.82, 33.10, 56.69, 101.65, 187.12, 349.67 (20) |
| sum | 5.5 | 1.0 | raw | centroid_power | 11.68, 11.88, 12.08, 12.28, 12.49, 12.71 (0.21) |
| sum | 5.5 | 1.0 | raw | centroid_band_power | 10.77, 10.74, 10.73, 10.72, 10.72, 10.72 (0.055) |
| sum | 5.5 | 1.0 | hann | centroid_amp | 16.12, 16.12, 16.12, 16.12, 16.12, 16.12 (0.0037) |
| sum | 5.5 | 1.0 | hann | centroid_power | 11.00, 11.00, 11.00, 11.00, 11.00, 11.00 (1.4e-05) |
| sum | 5.5 | 1.0 | hann | centroid_band_power | 10.36, 10.36, 10.36, 10.36, 10.36, 10.36 (1.3e-05) |
| sum | 5.5 | 1.25 | raw | centroid_amp | 23.28, 37.34, 62.58, 109.13, 196.04, 358.44 (15) |
| sum | 5.5 | 1.25 | raw | centroid_power | 11.76, 11.97, 12.17, 12.38, 12.59, 12.80 (0.2) |
| sum | 5.5 | 1.25 | raw | centroid_band_power | 10.78, 10.75, 10.74, 10.73, 10.73, 10.73 (0.052) |
| sum | 5.5 | 1.25 | hann | centroid_amp | 24.06, 33.24, 44.37, 62.69, 103.56, 163.32 (1.6) |
| sum | 5.5 | 1.25 | hann | centroid_power | 11.08, 11.10, 11.10, 11.10, 11.10, 11.10 (0.019) |
| sum | 5.5 | 1.25 | hann | centroid_band_power | 10.37, 10.37, 10.37, 10.37, 10.37, 10.37 (0.012) |
| sum | 5.5 | 1.75 | raw | centroid_amp | 27.47, 45.73, 77.22, 134.50, 240.99, 436.17 (5.2) |
| sum | 5.5 | 1.75 | raw | centroid_power | 12.35, 12.66, 12.91, 13.14, 13.36, 13.57 (0.18) |
| sum | 5.5 | 1.75 | raw | centroid_band_power | 10.95, 10.92, 10.91, 10.90, 10.90, 10.90 (0.053) |
| sum | 5.5 | 1.75 | hann | centroid_amp | 30.91, 49.73, 76.04, 124.23, 236.00, 421.13 (2.4) |
| sum | 5.5 | 1.75 | hann | centroid_power | 11.69, 11.81, 11.86, 11.88, 11.89, 11.90 (0.058) |
| sum | 5.5 | 1.75 | hann | centroid_band_power | 10.55, 10.55, 10.55, 10.55, 10.55, 10.55 (0.031) |
| sum | 5.5 | 2.6 | raw | centroid_amp | 31.44, 54.56, 95.06, 171.51, 318.16, 595.14 (2.1) |
| sum | 5.5 | 2.6 | raw | centroid_power | 13.50, 14.14, 14.60, 14.96, 15.25, 15.51 (0.2) |
| sum | 5.5 | 2.6 | raw | centroid_band_power | 11.25, 11.21, 11.20, 11.19, 11.19, 11.19 (0.063) |
| sum | 5.5 | 2.6 | hann | centroid_amp | 35.41, 61.45, 101.92, 180.65, 360.96, 681.71 (2.3) |
| sum | 5.5 | 2.6 | hann | centroid_power | 12.87, 13.33, 13.59, 13.75, 13.83, 13.89 (0.13) |
| sum | 5.5 | 2.6 | hann | centroid_band_power | 10.86, 10.85, 10.85, 10.85, 10.85, 10.85 (0.055) |
| sum | 6.3 | 0.9 | raw | centroid_amp | 27.53, 39.82, 62.16, 104.45, 184.70, 337.12 (6.6) |
| sum | 6.3 | 0.9 | raw | centroid_power | 13.16, 13.40, 13.64, 13.88, 14.12, 14.36 (0.14) |
| sum | 6.3 | 0.9 | raw | centroid_band_power | 10.92, 10.91, 10.90, 10.90, 10.90, 10.90 (0.035) |
| sum | 6.3 | 0.9 | hann | centroid_amp | 22.56, 26.71, 31.32, 37.46, 43.50, 51.81 (0.5) |
| sum | 6.3 | 0.9 | hann | centroid_power | 12.67, 12.67, 12.67, 12.67, 12.67, 12.67 (0.0093) |
| sum | 6.3 | 0.9 | hann | centroid_band_power | 10.75, 10.75, 10.75, 10.75, 10.75, 10.75 (0.0031) |
| sum | 6.3 | 1.0 | raw | centroid_amp | 27.15, 39.03, 61.30, 103.93, 185.21, 339.88 (6.6) |
| sum | 6.3 | 1.0 | raw | centroid_power | 13.10, 13.34, 13.57, 13.81, 14.04, 14.28 (0.14) |
| sum | 6.3 | 1.0 | raw | centroid_band_power | 10.89, 10.88, 10.87, 10.87, 10.87, 10.87 (0.038) |
| sum | 6.3 | 1.0 | hann | centroid_amp | 19.06, 19.06, 19.06, 19.07, 19.07, 19.07 (0.0021) |
| sum | 6.3 | 1.0 | hann | centroid_power | 12.59, 12.59, 12.59, 12.59, 12.59, 12.59 (6.5e-06) |
| sum | 6.3 | 1.0 | hann | centroid_band_power | 10.71, 10.71, 10.71, 10.71, 10.71, 10.71 (5.4e-06) |
| sum | 6.3 | 1.25 | raw | centroid_amp | 28.28, 41.77, 65.76, 110.01, 191.97, 345.68 (5.5) |
| sum | 6.3 | 1.25 | raw | centroid_power | 13.20, 13.45, 13.69, 13.93, 14.16, 14.40 (0.14) |
| sum | 6.3 | 1.25 | raw | centroid_band_power | 10.92, 10.91, 10.90, 10.90, 10.90, 10.90 (0.045) |
| sum | 6.3 | 1.25 | hann | centroid_amp | 26.04, 36.14, 50.89, 74.73, 102.84, 151.22 (1.4) |
| sum | 6.3 | 1.25 | hann | centroid_power | 12.68, 12.70, 12.71, 12.71, 12.71, 12.71 (0.022) |
| sum | 6.3 | 1.25 | hann | centroid_band_power | 10.73, 10.73, 10.73, 10.73, 10.73, 10.73 (0.0054) |
| sum | 6.3 | 1.75 | raw | centroid_amp | 30.78, 48.37, 79.31, 134.70, 232.10, 415.11 (3) |
| sum | 6.3 | 1.75 | raw | centroid_power | 13.87, 14.26, 14.56, 14.81, 15.06, 15.29 (0.15) |
| sum | 6.3 | 1.75 | raw | centroid_band_power | 11.13, 11.11, 11.10, 11.10, 11.10, 11.10 (0.052) |
| sum | 6.3 | 1.75 | hann | centroid_amp | 32.40, 52.41, 85.97, 145.31, 226.19, 382.33 (2.1) |
| sum | 6.3 | 1.75 | hann | centroid_power | 13.33, 13.50, 13.57, 13.60, 13.62, 13.62 (0.067) |
| sum | 6.3 | 1.75 | hann | centroid_band_power | 10.92, 10.92, 10.92, 10.92, 10.92, 10.92 (0.014) |
| sum | 6.3 | 2.6 | raw | centroid_amp | 33.52, 56.09, 97.10, 171.64, 303.23, 563.34 (1.8) |
| sum | 6.3 | 2.6 | raw | centroid_power | 15.13, 15.94, 16.50, 16.91, 17.25, 17.54 (0.19) |
| sum | 6.3 | 2.6 | raw | centroid_band_power | 11.47, 11.44, 11.43, 11.43, 11.43, 11.43 (0.057) |
| sum | 6.3 | 2.6 | hann | centroid_amp | 36.68, 63.81, 113.10, 204.59, 344.54, 630.39 (2) |
| sum | 6.3 | 2.6 | hann | centroid_power | 14.59, 15.18, 15.52, 15.71, 15.83, 15.89 (0.15) |
| sum | 6.3 | 2.6 | hann | centroid_band_power | 11.26, 11.24, 11.24, 11.24, 11.24, 11.24 (0.025) |
| product1 | 3 | 0.9 | raw | centroid_amp | 5.42, 5.72, 6.01, 6.27, 6.51, 6.74 (0.0015) |
| product1 | 3 | 0.9 | raw | centroid_power | 4.25, 4.25, 4.25, 4.25, 4.25, 4.25 (4.9e-10) |
| product1 | 3 | 0.9 | raw | centroid_band_power | 4.25, 4.25, 4.25, 4.25, 4.25, 4.25 (4.4e-12) |
| product1 | 3 | 0.9 | hann | centroid_amp | 5.43, 5.74, 6.02, 6.28, 6.53, 6.76 (0.002) |
| product1 | 3 | 0.9 | hann | centroid_power | 4.29, 4.29, 4.29, 4.29, 4.29, 4.29 (6.7e-09) |
| product1 | 3 | 0.9 | hann | centroid_band_power | 4.29, 4.29, 4.29, 4.29, 4.29, 4.29 (5.1e-09) |
| product1 | 3 | 1.0 | raw | centroid_amp | 4.24, 4.24, 4.24, 4.24, 4.24, 4.24 (1.3e-12) |
| product1 | 3 | 1.0 | raw | centroid_power | 4.24, 4.24, 4.24, 4.24, 4.24, 4.24 (2.3e-16) |
| product1 | 3 | 1.0 | raw | centroid_band_power | 4.24, 4.24, 4.24, 4.24, 4.24, 4.24 (2.3e-16) |
| product1 | 3 | 1.0 | hann | centroid_amp | 4.30, 4.30, 4.30, 4.30, 4.30, 4.30 (6.9e-13) |
| product1 | 3 | 1.0 | hann | centroid_power | 4.28, 4.28, 4.28, 4.28, 4.28, 4.28 (2.3e-16) |
| product1 | 3 | 1.0 | hann | centroid_band_power | 4.28, 4.28, 4.28, 4.28, 4.28, 4.28 (3.7e-16) |
| product1 | 3 | 1.25 | raw | centroid_amp | 7.45, 8.79, 10.39, 12.21, 14.31, 16.75 (0.021) |
| product1 | 3 | 1.25 | raw | centroid_power | 4.29, 4.29, 4.29, 4.29, 4.29, 4.29 (8e-08) |
| product1 | 3 | 1.25 | raw | centroid_band_power | 4.29, 4.29, 4.29, 4.29, 4.29, 4.29 (1.9e-10) |
| product1 | 3 | 1.25 | hann | centroid_amp | 7.33, 8.64, 10.19, 11.94, 14.02, 16.39 (0.022) |
| product1 | 3 | 1.25 | hann | centroid_power | 4.33, 4.33, 4.33, 4.33, 4.33, 4.33 (1.3e-07) |
| product1 | 3 | 1.25 | hann | centroid_band_power | 4.33, 4.33, 4.33, 4.33, 4.33, 4.33 (8.7e-08) |
| product1 | 3 | 1.75 | raw | centroid_amp | 12.66, 17.44, 24.17, 33.13, 45.30, 61.95 (0.16) |
| product1 | 3 | 1.75 | raw | centroid_power | 4.55, 4.56, 4.57, 4.57, 4.57, 4.57 (6.2e-06) |
| product1 | 3 | 1.75 | raw | centroid_band_power | 4.50, 4.50, 4.50, 4.50, 4.50, 4.50 (5.7e-09) |
| product1 | 3 | 1.75 | hann | centroid_amp | 12.17, 16.75, 23.06, 31.54, 43.21, 58.97 (0.15) |
| product1 | 3 | 1.75 | hann | centroid_power | 4.59, 4.60, 4.61, 4.61, 4.61, 4.61 (1e-05) |
| product1 | 3 | 1.75 | hann | centroid_band_power | 4.54, 4.54, 4.54, 4.54, 4.54, 4.54 (9.7e-07) |
| product1 | 3 | 2.6 | raw | centroid_amp | 18.16, 27.92, 43.39, 66.84, 102.91, 158.92 (0.51) |
| product1 | 3 | 2.6 | raw | centroid_power | 5.12, 5.19, 5.23, 5.25, 5.27, 5.28 (0.00012) |
| product1 | 3 | 2.6 | raw | centroid_band_power | 4.91, 4.90, 4.90, 4.90, 4.90, 4.90 (5.6e-08) |
| product1 | 3 | 2.6 | hann | centroid_amp | 17.25, 26.48, 40.77, 62.60, 96.41, 148.36 (0.45) |
| product1 | 3 | 2.6 | hann | centroid_power | 5.15, 5.22, 5.27, 5.29, 5.31, 5.31 (0.00017) |
| product1 | 3 | 2.6 | hann | centroid_band_power | 4.94, 4.94, 4.94, 4.94, 4.94, 4.94 (5.3e-06) |
| product1 | 5 | 0.9 | raw | centroid_amp | 8.68, 9.20, 9.70, 10.16, 10.59, 10.99 (0.0015) |
| product1 | 5 | 0.9 | raw | centroid_power | 7.09, 7.09, 7.09, 7.09, 7.09, 7.09 (5.8e-10) |
| product1 | 5 | 0.9 | raw | centroid_band_power | 7.09, 7.09, 7.09, 7.09, 7.09, 7.09 (3.6e-12) |
| product1 | 5 | 0.9 | hann | centroid_amp | 8.64, 9.21, 9.67, 10.17, 10.56, 11.00 (0.0013) |
| product1 | 5 | 0.9 | hann | centroid_power | 7.11, 7.11, 7.11, 7.11, 7.11, 7.11 (3.6e-09) |
| product1 | 5 | 0.9 | hann | centroid_band_power | 7.11, 7.11, 7.11, 7.11, 7.11, 7.11 (4.5e-09) |
| product1 | 5 | 1.0 | raw | centroid_amp | 7.07, 7.07, 7.07, 7.07, 7.07, 7.07 (1.9e-12) |
| product1 | 5 | 1.0 | raw | centroid_power | 7.07, 7.07, 7.07, 7.07, 7.07, 7.07 (1.1e-16) |
| product1 | 5 | 1.0 | raw | centroid_band_power | 7.07, 7.07, 7.07, 7.07, 7.07, 7.07 (1.1e-16) |
| product1 | 5 | 1.0 | hann | centroid_amp | 7.11, 7.11, 7.11, 7.11, 7.11, 7.11 (8.4e-13) |
| product1 | 5 | 1.0 | hann | centroid_power | 7.09, 7.09, 7.09, 7.09, 7.09, 7.09 (3.1e-16) |
| product1 | 5 | 1.0 | hann | centroid_band_power | 7.09, 7.09, 7.09, 7.09, 7.09, 7.09 (4.6e-16) |
| product1 | 5 | 1.25 | raw | centroid_amp | 11.14, 13.17, 15.59, 18.36, 21.57, 25.29 (0.021) |
| product1 | 5 | 1.25 | raw | centroid_power | 7.15, 7.15, 7.15, 7.15, 7.15, 7.15 (8.8e-08) |
| product1 | 5 | 1.25 | raw | centroid_band_power | 7.13, 7.13, 7.13, 7.13, 7.13, 7.13 (1.3e-10) |
| product1 | 5 | 1.25 | hann | centroid_amp | 10.93, 13.03, 15.23, 18.13, 21.07, 24.98 (0.017) |
| product1 | 5 | 1.25 | hann | centroid_power | 7.17, 7.18, 7.18, 7.18, 7.18, 7.18 (2e-07) |
| product1 | 5 | 1.25 | hann | centroid_band_power | 7.16, 7.16, 7.16, 7.16, 7.16, 7.16 (7.9e-08) |
| product1 | 5 | 1.75 | raw | centroid_amp | 17.12, 23.70, 32.93, 45.36, 62.25, 85.31 (0.15) |
| product1 | 5 | 1.75 | raw | centroid_power | 7.55, 7.59, 7.61, 7.61, 7.62, 7.62 (6.6e-06) |
| product1 | 5 | 1.75 | raw | centroid_band_power | 7.42, 7.42, 7.42, 7.42, 7.42, 7.42 (3.8e-09) |
| product1 | 5 | 1.75 | hann | centroid_amp | 16.50, 23.11, 31.45, 44.00, 59.33, 82.77 (0.12) |
| product1 | 5 | 1.75 | hann | centroid_power | 7.58, 7.61, 7.63, 7.64, 7.64, 7.64 (9.1e-06) |
| product1 | 5 | 1.75 | hann | centroid_band_power | 7.44, 7.44, 7.44, 7.44, 7.44, 7.44 (8.9e-07) |
| product1 | 5 | 2.6 | raw | centroid_amp | 22.89, 35.39, 55.14, 85.33, 131.90, 204.10 (0.48) |
| product1 | 5 | 2.6 | raw | centroid_power | 8.39, 8.56, 8.67, 8.73, 8.76, 8.78 (0.00012) |
| product1 | 5 | 2.6 | raw | centroid_band_power | 7.91, 7.90, 7.89, 7.89, 7.89, 7.89 (3.7e-08) |
| product1 | 5 | 2.6 | hann | centroid_amp | 21.90, 34.18, 52.04, 81.70, 123.80, 195.01 (0.4) |
| product1 | 5 | 2.6 | hann | centroid_power | 8.41, 8.58, 8.69, 8.75, 8.79, 8.81 (0.00015) |
| product1 | 5 | 2.6 | hann | centroid_band_power | 7.93, 7.92, 7.92, 7.92, 7.92, 7.92 (4.9e-06) |
| product1 | 7 | 0.9 | raw | centroid_amp | 11.80, 12.55, 13.27, 13.94, 14.56, 15.14 (0.0015) |
| product1 | 7 | 0.9 | raw | centroid_power | 9.92, 9.92, 9.92, 9.92, 9.92, 9.92 (6.4e-10) |
| product1 | 7 | 0.9 | raw | centroid_band_power | 9.92, 9.92, 9.92, 9.92, 9.92, 9.92 (2.4e-12) |
| product1 | 7 | 0.9 | hann | centroid_amp | 11.73, 12.55, 13.26, 13.87, 14.56, 15.13 (0.0016) |
| product1 | 7 | 0.9 | hann | centroid_power | 9.94, 9.94, 9.94, 9.94, 9.94, 9.94 (3.6e-09) |
| product1 | 7 | 0.9 | hann | centroid_band_power | 9.93, 9.93, 9.93, 9.93, 9.93, 9.93 (7.5e-09) |
| product1 | 7 | 1.0 | raw | centroid_amp | 9.90, 9.90, 9.90, 9.90, 9.90, 9.90 (2.2e-12) |
| product1 | 7 | 1.0 | raw | centroid_power | 9.90, 9.90, 9.90, 9.90, 9.90, 9.90 (5.5e-16) |
| product1 | 7 | 1.0 | raw | centroid_band_power | 9.90, 9.90, 9.90, 9.90, 9.90, 9.90 (5.5e-16) |
| product1 | 7 | 1.0 | hann | centroid_amp | 9.92, 9.92, 9.92, 9.92, 9.92, 9.92 (1.3e-12) |
| product1 | 7 | 1.0 | hann | centroid_power | 9.92, 9.92, 9.92, 9.92, 9.92, 9.92 (8.3e-16) |
| product1 | 7 | 1.0 | hann | centroid_band_power | 9.92, 9.92, 9.92, 9.92, 9.92, 9.92 (4.9e-16) |
| product1 | 7 | 1.25 | raw | centroid_amp | 14.46, 17.11, 20.28, 23.93, 28.15, 33.04 (0.02) |
| product1 | 7 | 1.25 | raw | centroid_power | 10.00, 10.01, 10.01, 10.01, 10.01, 10.01 (9.3e-08) |
| product1 | 7 | 1.25 | raw | centroid_band_power | 9.97, 9.97, 9.97, 9.97, 9.97, 9.97 (8.2e-11) |
| product1 | 7 | 1.25 | hann | centroid_amp | 14.19, 16.98, 20.04, 23.34, 27.88, 32.64 (0.019) |
| product1 | 7 | 1.25 | hann | centroid_power | 10.02, 10.03, 10.03, 10.03, 10.03, 10.03 (4.4e-07) |
| product1 | 7 | 1.25 | hann | centroid_band_power | 9.98, 9.98, 9.98, 9.98, 9.98, 9.98 (1.1e-07) |
| product1 | 7 | 1.75 | raw | centroid_amp | 20.73, 28.74, 40.04, 55.34, 76.16, 104.56 (0.15) |
| product1 | 7 | 1.75 | raw | centroid_power | 10.53, 10.61, 10.64, 10.65, 10.66, 10.66 (6.8e-06) |
| product1 | 7 | 1.75 | raw | centroid_band_power | 10.25, 10.25, 10.25, 10.25, 10.25, 10.25 (2.3e-09) |
| product1 | 7 | 1.75 | hann | centroid_amp | 20.01, 28.22, 38.99, 52.71, 74.35, 101.50 (0.14) |
| product1 | 7 | 1.75 | hann | centroid_power | 10.55, 10.62, 10.65, 10.67, 10.68, 10.68 (1.7e-05) |
| product1 | 7 | 1.75 | hann | centroid_band_power | 10.27, 10.26, 10.26, 10.26, 10.26, 10.26 (1.1e-06) |
| product1 | 7 | 2.6 | raw | centroid_amp | 26.43, 40.92, 63.93, 99.26, 153.83, 238.47 (0.47) |
| product1 | 7 | 2.6 | raw | centroid_power | 11.58, 11.89, 12.07, 12.18, 12.25, 12.29 (0.00013) |
| product1 | 7 | 2.6 | raw | centroid_band_power | 10.69, 10.68, 10.68, 10.68, 10.68, 10.68 (2.4e-08) |
| product1 | 7 | 2.6 | hann | centroid_amp | 25.37, 39.87, 61.62, 93.31, 148.33, 228.06 (0.46) |
| product1 | 7 | 2.6 | hann | centroid_power | 11.59, 11.90, 12.09, 12.20, 12.26, 12.30 (0.00023) |
| product1 | 7 | 2.6 | hann | centroid_band_power | 10.71, 10.70, 10.69, 10.69, 10.69, 10.69 (5.8e-06) |
| product1 | 3.5 | 0.9 | raw | centroid_amp | 18.64, 31.94, 56.97, 104.14, 193.14, 361.51 (21) |
| product1 | 3.5 | 0.9 | raw | centroid_power | 6.06, 6.33, 6.60, 6.88, 7.16, 7.44 (0.32) |
| product1 | 3.5 | 0.9 | raw | centroid_band_power | 5.61, 5.57, 5.56, 5.55, 5.55, 5.55 (0.087) |
| product1 | 3.5 | 0.9 | hann | centroid_amp | 6.24, 6.62, 6.89, 7.25, 7.56, 7.77 (0.0072) |
| product1 | 3.5 | 0.9 | hann | centroid_power | 5.00, 5.00, 5.00, 5.00, 5.00, 5.00 (4.8e-05) |
| product1 | 3.5 | 0.9 | hann | centroid_band_power | 4.99, 4.99, 4.99, 4.99, 4.99, 4.99 (4.8e-05) |
| product1 | 3.5 | 1.0 | raw | centroid_amp | 18.79, 32.30, 57.73, 105.62, 195.99, 366.94 (20) |
| product1 | 3.5 | 1.0 | raw | centroid_power | 6.05, 6.31, 6.58, 6.86, 7.14, 7.43 (0.3) |
| product1 | 3.5 | 1.0 | raw | centroid_band_power | 5.60, 5.56, 5.54, 5.54, 5.54, 5.54 (0.086) |
| product1 | 3.5 | 1.0 | hann | centroid_amp | 5.09, 5.10, 5.10, 5.10, 5.10, 5.10 (0.0048) |
| product1 | 3.5 | 1.0 | hann | centroid_power | 4.98, 4.98, 4.98, 4.98, 4.98, 4.98 (4.9e-05) |
| product1 | 3.5 | 1.0 | hann | centroid_band_power | 4.98, 4.98, 4.98, 4.98, 4.98, 4.98 (4.9e-05) |
| product1 | 3.5 | 1.25 | raw | centroid_amp | 19.18, 32.99, 59.09, 108.11, 200.62, 375.66 (17) |
| product1 | 3.5 | 1.25 | raw | centroid_power | 6.09, 6.36, 6.63, 6.91, 7.19, 7.47 (0.28) |
| product1 | 3.5 | 1.25 | raw | centroid_band_power | 5.65, 5.60, 5.59, 5.58, 5.58, 5.58 (0.083) |
| product1 | 3.5 | 1.25 | hann | centroid_amp | 8.16, 9.67, 11.02, 13.29, 15.64, 17.71 (0.034) |
| product1 | 3.5 | 1.25 | hann | centroid_power | 5.04, 5.04, 5.04, 5.04, 5.04, 5.04 (5e-05) |
| product1 | 3.5 | 1.25 | hann | centroid_band_power | 5.03, 5.03, 5.03, 5.03, 5.03, 5.03 (5e-05) |
| product1 | 3.5 | 1.75 | raw | centroid_amp | 20.01, 34.10, 60.70, 110.28, 203.84, 380.84 (14) |
| product1 | 3.5 | 1.75 | raw | centroid_power | 6.37, 6.65, 6.93, 7.21, 7.49, 7.77 (0.24) |
| product1 | 3.5 | 1.75 | raw | centroid_band_power | 5.87, 5.83, 5.82, 5.81, 5.81, 5.81 (0.079) |
| product1 | 3.5 | 1.75 | hann | centroid_amp | 13.04, 18.06, 23.39, 33.66, 46.30, 59.59 (0.14) |
| product1 | 3.5 | 1.75 | hann | centroid_power | 5.34, 5.35, 5.36, 5.36, 5.36, 5.36 (6.4e-05) |
| product1 | 3.5 | 1.75 | hann | centroid_band_power | 5.27, 5.27, 5.27, 5.27, 5.27, 5.27 (5.2e-05) |
| product1 | 3.5 | 2.6 | raw | centroid_amp | 21.46, 36.12, 63.25, 112.93, 206.00, 381.38 (9.1) |
| product1 | 3.5 | 2.6 | raw | centroid_power | 6.97, 7.32, 7.66, 7.96, 8.26, 8.55 (0.2) |
| product1 | 3.5 | 2.6 | raw | centroid_band_power | 6.30, 6.25, 6.23, 6.23, 6.22, 6.22 (0.076) |
| product1 | 3.5 | 2.6 | hann | centroid_amp | 18.14, 27.94, 39.99, 65.22, 100.69, 144.31 (0.4) |
| product1 | 3.5 | 2.6 | hann | centroid_power | 5.98, 6.07, 6.12, 6.16, 6.17, 6.18 (0.00064) |
| product1 | 3.5 | 2.6 | hann | centroid_band_power | 5.72, 5.71, 5.71, 5.71, 5.71, 5.71 (5.4e-05) |
| product1 | 5.5 | 0.9 | raw | centroid_amp | 20.22, 33.16, 57.62, 103.85, 191.26, 356.81 (22) |
| product1 | 5.5 | 0.9 | raw | centroid_power | 8.73, 8.99, 9.26, 9.53, 9.81, 10.09 (0.29) |
| product1 | 5.5 | 0.9 | raw | centroid_band_power | 8.29, 8.25, 8.23, 8.23, 8.22, 8.22 (0.069) |
| product1 | 5.5 | 0.9 | hann | centroid_amp | 9.45, 10.01, 10.56, 10.95, 11.52, 12.01 (0.0049) |
| product1 | 5.5 | 0.9 | hann | centroid_power | 7.82, 7.82, 7.82, 7.82, 7.82, 7.82 (1.2e-05) |
| product1 | 5.5 | 0.9 | hann | centroid_band_power | 7.82, 7.82, 7.82, 7.82, 7.82, 7.82 (1.2e-05) |
| product1 | 5.5 | 1.0 | raw | centroid_amp | 20.32, 33.45, 58.32, 105.29, 194.09, 362.27 (20) |
| product1 | 5.5 | 1.0 | raw | centroid_power | 8.71, 8.97, 9.24, 9.51, 9.79, 10.07 (0.28) |
| product1 | 5.5 | 1.0 | raw | centroid_band_power | 8.27, 8.23, 8.21, 8.21, 8.21, 8.20 (0.068) |
| product1 | 5.5 | 1.0 | hann | centroid_amp | 7.87, 7.88, 7.88, 7.88, 7.88, 7.88 (0.0032) |
| product1 | 5.5 | 1.0 | hann | centroid_power | 7.80, 7.80, 7.80, 7.80, 7.80, 7.80 (1.3e-05) |
| product1 | 5.5 | 1.0 | hann | centroid_band_power | 7.80, 7.80, 7.80, 7.80, 7.80, 7.80 (1.3e-05) |
| product1 | 5.5 | 1.25 | raw | centroid_amp | 20.76, 34.21, 59.61, 107.60, 198.25, 369.97 (18) |
| product1 | 5.5 | 1.25 | raw | centroid_power | 8.79, 9.05, 9.32, 9.59, 9.87, 10.15 (0.26) |
| product1 | 5.5 | 1.25 | raw | centroid_band_power | 8.34, 8.30, 8.28, 8.27, 8.27, 8.27 (0.068) |
| product1 | 5.5 | 1.25 | hann | centroid_amp | 11.77, 13.84, 16.23, 18.36, 22.24, 26.42 (0.028) |
| product1 | 5.5 | 1.25 | hann | centroid_power | 7.88, 7.89, 7.89, 7.89, 7.89, 7.89 (1.3e-05) |
| product1 | 5.5 | 1.25 | hann | centroid_band_power | 7.87, 7.87, 7.87, 7.87, 7.87, 7.87 (1.3e-05) |
| product1 | 5.5 | 1.75 | raw | centroid_amp | 22.06, 35.97, 61.77, 110.16, 201.15, 373.39 (14) |
| product1 | 5.5 | 1.75 | raw | centroid_power | 9.20, 9.50, 9.79, 10.07, 10.35, 10.64 (0.22) |
| product1 | 5.5 | 1.75 | raw | centroid_band_power | 8.63, 8.59, 8.58, 8.57, 8.57, 8.56 (0.067) |
| product1 | 5.5 | 1.75 | hann | centroid_amp | 17.39, 23.89, 32.32, 41.35, 60.50, 84.38 (0.17) |
| product1 | 5.5 | 1.75 | hann | centroid_power | 8.32, 8.37, 8.39, 8.39, 8.40, 8.40 (2.6e-05) |
| product1 | 5.5 | 1.75 | hann | centroid_band_power | 8.18, 8.18, 8.18, 8.18, 8.18, 8.18 (1.4e-05) |
| product1 | 5.5 | 2.6 | raw | centroid_amp | 24.20, 39.33, 66.47, 115.87, 206.87, 377.13 (8.5) |
| product1 | 5.5 | 2.6 | raw | centroid_power | 10.05, 10.52, 10.91, 11.26, 11.58, 11.88 (0.19) |
| product1 | 5.5 | 2.6 | raw | centroid_band_power | 9.14, 9.09, 9.07, 9.07, 9.06, 9.06 (0.068) |
| product1 | 5.5 | 2.6 | hann | centroid_amp | 22.74, 34.89, 52.15, 73.72, 124.01, 194.26 (0.49) |
| product1 | 5.5 | 2.6 | hann | centroid_power | 9.22, 9.42, 9.55, 9.62, 9.66, 9.68 (0.00028) |
| product1 | 5.5 | 2.6 | hann | centroid_band_power | 8.71, 8.70, 8.70, 8.70, 8.70, 8.70 (1.7e-05) |
| product1 | 6.3 | 0.9 | raw | centroid_amp | 21.24, 35.23, 61.79, 111.99, 206.93, 386.72 (14) |
| product1 | 6.3 | 0.9 | raw | centroid_power | 9.41, 9.64, 9.88, 10.11, 10.35, 10.59 (0.15) |
| product1 | 6.3 | 0.9 | raw | centroid_band_power | 9.07, 9.05, 9.05, 9.05, 9.05, 9.05 (0.032) |
| product1 | 6.3 | 0.9 | hann | centroid_amp | 10.58, 11.31, 11.95, 12.54, 13.06, 13.44 (0.0085) |
| product1 | 6.3 | 0.9 | hann | centroid_power | 8.95, 8.95, 8.95, 8.95, 8.95, 8.95 (4.8e-06) |
| product1 | 6.3 | 0.9 | hann | centroid_band_power | 8.95, 8.95, 8.95, 8.95, 8.95, 8.95 (5.1e-06) |
| product1 | 6.3 | 1.0 | raw | centroid_amp | 21.16, 35.14, 61.68, 111.85, 206.71, 386.31 (14) |
| product1 | 6.3 | 1.0 | raw | centroid_power | 9.40, 9.63, 9.87, 10.10, 10.34, 10.58 (0.16) |
| product1 | 6.3 | 1.0 | raw | centroid_band_power | 9.06, 9.04, 9.04, 9.04, 9.04, 9.03 (0.035) |
| product1 | 6.3 | 1.0 | hann | centroid_amp | 8.96, 8.96, 8.96, 8.96, 8.96, 8.96 (0.0017) |
| product1 | 6.3 | 1.0 | hann | centroid_power | 8.93, 8.93, 8.93, 8.93, 8.93, 8.93 (5e-06) |
| product1 | 6.3 | 1.0 | hann | centroid_band_power | 8.93, 8.93, 8.93, 8.93, 8.93, 8.93 (5e-06) |
| product1 | 6.3 | 1.25 | raw | centroid_amp | 21.46, 35.25, 61.37, 110.74, 204.03, 380.72 (15) |
| product1 | 6.3 | 1.25 | raw | centroid_power | 9.51, 9.75, 9.99, 10.23, 10.46, 10.70 (0.17) |
| product1 | 6.3 | 1.25 | raw | centroid_band_power | 9.14, 9.13, 9.12, 9.12, 9.12, 9.12 (0.044) |
| product1 | 6.3 | 1.25 | hann | centroid_amp | 12.87, 15.36, 18.18, 21.41, 24.83, 27.96 (0.037) |
| product1 | 6.3 | 1.25 | hann | centroid_power | 9.02, 9.03, 9.03, 9.03, 9.03, 9.03 (9.3e-06) |
| product1 | 6.3 | 1.25 | hann | centroid_band_power | 9.00, 9.00, 9.00, 9.00, 9.00, 9.00 (5e-06) |
| product1 | 6.3 | 1.75 | raw | centroid_amp | 22.95, 37.00, 62.82, 110.76, 200.51, 369.94 (15) |
| product1 | 6.3 | 1.75 | raw | centroid_power | 10.02, 10.31, 10.57, 10.82, 11.06, 11.30 (0.18) |
| product1 | 6.3 | 1.75 | raw | centroid_band_power | 9.46, 9.44, 9.44, 9.44, 9.44, 9.44 (0.058) |
| product1 | 6.3 | 1.75 | hann | centroid_amp | 18.50, 25.77, 35.75, 49.35, 65.74, 83.84 (0.14) |
| product1 | 6.3 | 1.75 | hann | centroid_power | 9.51, 9.57, 9.60, 9.61, 9.61, 9.62 (0.0002) |
| product1 | 6.3 | 1.75 | hann | centroid_band_power | 9.30, 9.30, 9.30, 9.30, 9.30, 9.30 (5.5e-06) |
| product1 | 6.3 | 2.6 | raw | centroid_amp | 25.28, 40.97, 68.58, 118.07, 207.81, 372.94 (12) |
| product1 | 6.3 | 2.6 | raw | centroid_power | 11.01, 11.50, 11.89, 12.22, 12.50, 12.77 (0.18) |
| product1 | 6.3 | 2.6 | raw | centroid_band_power | 9.97, 9.95, 9.94, 9.94, 9.94, 9.94 (0.07) |
| product1 | 6.3 | 2.6 | hann | centroid_amp | 23.92, 36.79, 57.13, 88.66, 131.07, 186.09 (0.97) |
| product1 | 6.3 | 2.6 | hann | centroid_power | 10.48, 10.75, 10.90, 10.99, 11.05, 11.08 (0.002) |
| product1 | 6.3 | 2.6 | hann | centroid_band_power | 9.80, 9.79, 9.79, 9.79, 9.79, 9.79 (1.3e-05) |
| oned | 3 | 0.9 | raw | centroid_amp | 3.63, 3.79, 3.93, 4.06, 4.18, 4.30 (0.00083) |
| oned | 3 | 0.9 | raw | centroid_power | 3.01, 3.01, 3.01, 3.01, 3.01, 3.01 (2.9e-10) |
| oned | 3 | 0.9 | raw | centroid_band_power | 3.01, 3.01, 3.01, 3.01, 3.01, 3.01 (2.9e-12) |
| oned | 3 | 0.9 | hann | centroid_amp | 3.61, 3.77, 3.91, 4.04, 4.17, 4.28 (0.0012) |
| oned | 3 | 0.9 | hann | centroid_power | 3.01, 3.01, 3.01, 3.01, 3.01, 3.01 (7e-09) |
| oned | 3 | 0.9 | hann | centroid_band_power | 3.01, 3.01, 3.01, 3.01, 3.01, 3.01 (5.9e-09) |
| oned | 3 | 1.0 | raw | centroid_amp | 3.00, 3.00, 3.00, 3.00, 3.00, 3.00 (3.9e-13) |
| oned | 3 | 1.0 | raw | centroid_power | 3.00, 3.00, 3.00, 3.00, 3.00, 3.00 (0) |
| oned | 3 | 1.0 | raw | centroid_band_power | 3.00, 3.00, 3.00, 3.00, 3.00, 3.00 (0) |
| oned | 3 | 1.0 | hann | centroid_amp | 3.00, 3.00, 3.00, 3.00, 3.00, 3.00 (2.7e-13) |
| oned | 3 | 1.0 | hann | centroid_power | 3.00, 3.00, 3.00, 3.00, 3.00, 3.00 (6.8e-17) |
| oned | 3 | 1.0 | hann | centroid_band_power | 3.00, 3.00, 3.00, 3.00, 3.00, 3.00 (7.9e-17) |
| oned | 3 | 1.25 | raw | centroid_amp | 4.73, 5.41, 6.22, 7.12, 8.19, 9.43 (0.011) |
| oned | 3 | 1.25 | raw | centroid_power | 3.03, 3.03, 3.03, 3.03, 3.03, 3.03 (4.5e-08) |
| oned | 3 | 1.25 | raw | centroid_band_power | 3.02, 3.02, 3.02, 3.02, 3.02, 3.02 (1.2e-10) |
| oned | 3 | 1.25 | hann | centroid_amp | 4.64, 5.31, 6.09, 6.96, 8.01, 9.23 (0.012) |
| oned | 3 | 1.25 | hann | centroid_power | 3.03, 3.03, 3.03, 3.03, 3.03, 3.03 (6.3e-08) |
| oned | 3 | 1.25 | hann | centroid_band_power | 3.02, 3.02, 3.02, 3.02, 3.02, 3.02 (8.7e-08) |
| oned | 3 | 1.75 | raw | centroid_amp | 7.62, 10.11, 13.58, 18.10, 24.33, 32.90 (0.077) |
| oned | 3 | 1.75 | raw | centroid_power | 3.17, 3.18, 3.18, 3.18, 3.18, 3.18 (3.3e-06) |
| oned | 3 | 1.75 | raw | centroid_band_power | 3.14, 3.14, 3.14, 3.14, 3.14, 3.14 (3.5e-09) |
| oned | 3 | 1.75 | hann | centroid_amp | 7.34, 9.72, 12.97, 17.25, 23.19, 31.35 (0.075) |
| oned | 3 | 1.75 | hann | centroid_power | 3.17, 3.18, 3.18, 3.18, 3.18, 3.18 (6e-06) |
| oned | 3 | 1.75 | hann | centroid_band_power | 3.15, 3.14, 3.14, 3.14, 3.14, 3.14 (8.2e-07) |
| oned | 3 | 2.6 | raw | centroid_amp | 10.80, 16.03, 24.20, 36.30, 55.11, 84.34 (0.23) |
| oned | 3 | 2.6 | raw | centroid_power | 3.48, 3.51, 3.54, 3.55, 3.56, 3.56 (5.9e-05) |
| oned | 3 | 2.6 | raw | centroid_band_power | 3.37, 3.37, 3.37, 3.37, 3.37, 3.37 (3.2e-08) |
| oned | 3 | 2.6 | hann | centroid_amp | 10.28, 15.21, 22.73, 34.02, 51.52, 78.81 (0.22) |
| oned | 3 | 2.6 | hann | centroid_power | 3.48, 3.51, 3.54, 3.55, 3.56, 3.56 (9e-05) |
| oned | 3 | 2.6 | hann | centroid_band_power | 3.38, 3.37, 3.37, 3.37, 3.37, 3.37 (3.7e-06) |
| oned | 5 | 0.9 | raw | centroid_amp | 5.88, 6.14, 6.40, 6.63, 6.84, 7.04 (0.00081) |
| oned | 5 | 0.9 | raw | centroid_power | 5.01, 5.01, 5.01, 5.01, 5.01, 5.01 (3.5e-10) |
| oned | 5 | 0.9 | raw | centroid_band_power | 5.01, 5.01, 5.01, 5.01, 5.01, 5.01 (2.4e-12) |
| oned | 5 | 0.9 | hann | centroid_amp | 5.84, 6.13, 6.36, 6.61, 6.81, 7.03 (0.00061) |
| oned | 5 | 0.9 | hann | centroid_power | 5.01, 5.01, 5.01, 5.01, 5.01, 5.01 (4.2e-09) |
| oned | 5 | 0.9 | hann | centroid_band_power | 5.01, 5.01, 5.01, 5.01, 5.01, 5.01 (4.9e-09) |
| oned | 5 | 1.0 | raw | centroid_amp | 5.00, 5.00, 5.00, 5.00, 5.00, 5.00 (9.5e-13) |
| oned | 5 | 1.0 | raw | centroid_power | 5.00, 5.00, 5.00, 5.00, 5.00, 5.00 (4.6e-17) |
| oned | 5 | 1.0 | raw | centroid_band_power | 5.00, 5.00, 5.00, 5.00, 5.00, 5.00 (4.6e-17) |
| oned | 5 | 1.0 | hann | centroid_amp | 5.00, 5.00, 5.00, 5.00, 5.00, 5.00 (3.8e-13) |
| oned | 5 | 1.0 | hann | centroid_power | 5.00, 5.00, 5.00, 5.00, 5.00, 5.00 (1.6e-16) |
| oned | 5 | 1.0 | hann | centroid_band_power | 5.00, 5.00, 5.00, 5.00, 5.00, 5.00 (1.3e-16) |
| oned | 5 | 1.25 | raw | centroid_amp | 7.22, 8.27, 9.50, 10.89, 12.51, 14.39 (0.011) |
| oned | 5 | 1.25 | raw | centroid_power | 5.04, 5.04, 5.05, 5.05, 5.05, 5.05 (5e-08) |
| oned | 5 | 1.25 | raw | centroid_band_power | 5.04, 5.04, 5.04, 5.04, 5.04, 5.04 (8.7e-11) |
| oned | 5 | 1.25 | hann | centroid_amp | 7.10, 8.18, 9.30, 10.75, 12.24, 14.22 (0.0069) |
| oned | 5 | 1.25 | hann | centroid_power | 5.04, 5.04, 5.05, 5.05, 5.05, 5.05 (1.6e-07) |
| oned | 5 | 1.25 | hann | centroid_band_power | 5.04, 5.04, 5.04, 5.04, 5.04, 5.04 (8.4e-08) |
| oned | 5 | 1.75 | raw | centroid_amp | 10.61, 14.09, 18.88, 25.20, 33.86, 45.68 (0.075) |
| oned | 5 | 1.75 | raw | centroid_power | 5.27, 5.29, 5.29, 5.30, 5.30, 5.30 (3.5e-06) |
| oned | 5 | 1.75 | raw | centroid_band_power | 5.20, 5.20, 5.20, 5.20, 5.20, 5.20 (2.4e-09) |
| oned | 5 | 1.75 | hann | centroid_amp | 10.25, 13.75, 18.09, 24.46, 32.35, 44.36 (0.046) |
| oned | 5 | 1.75 | hann | centroid_power | 5.27, 5.29, 5.29, 5.30, 5.30, 5.30 (5.3e-06) |
| oned | 5 | 1.75 | hann | centroid_band_power | 5.20, 5.20, 5.20, 5.20, 5.20, 5.20 (9.2e-07) |
| oned | 5 | 2.6 | raw | centroid_amp | 14.04, 20.84, 31.40, 47.16, 71.53, 109.23 (0.22) |
| oned | 5 | 2.6 | raw | centroid_power | 5.73, 5.82, 5.87, 5.90, 5.92, 5.93 (6.1e-05) |
| oned | 5 | 2.6 | raw | centroid_band_power | 5.47, 5.47, 5.47, 5.47, 5.47, 5.47 (2.2e-08) |
| oned | 5 | 2.6 | hann | centroid_amp | 13.44, 20.15, 29.67, 45.11, 67.22, 104.34 (0.15) |
| oned | 5 | 2.6 | hann | centroid_power | 5.73, 5.82, 5.87, 5.90, 5.92, 5.93 (6.8e-05) |
| oned | 5 | 2.6 | hann | centroid_band_power | 5.47, 5.47, 5.47, 5.47, 5.47, 5.47 (5e-06) |
| oned | 7 | 0.9 | raw | centroid_amp | 8.05, 8.43, 8.80, 9.13, 9.44, 9.73 (0.00081) |
| oned | 7 | 0.9 | raw | centroid_power | 7.01, 7.01, 7.01, 7.01, 7.01, 7.01 (3.8e-10) |
| oned | 7 | 0.9 | raw | centroid_band_power | 7.01, 7.01, 7.01, 7.01, 7.01, 7.01 (1.7e-12) |
| oned | 7 | 0.9 | hann | centroid_amp | 8.00, 8.42, 8.78, 9.09, 9.43, 9.72 (0.00085) |
| oned | 7 | 0.9 | hann | centroid_power | 7.01, 7.01, 7.01, 7.01, 7.01, 7.01 (5.1e-09) |
| oned | 7 | 0.9 | hann | centroid_band_power | 7.01, 7.01, 7.01, 7.01, 7.01, 7.01 (7.8e-09) |
| oned | 7 | 1.0 | raw | centroid_amp | 7.00, 7.00, 7.00, 7.00, 7.00, 7.00 (1.5e-12) |
| oned | 7 | 1.0 | raw | centroid_power | 7.00, 7.00, 7.00, 7.00, 7.00, 7.00 (6.4e-17) |
| oned | 7 | 1.0 | raw | centroid_band_power | 7.00, 7.00, 7.00, 7.00, 7.00, 7.00 (6.4e-17) |
| oned | 7 | 1.0 | hann | centroid_amp | 7.00, 7.00, 7.00, 7.00, 7.00, 7.00 (7.6e-13) |
| oned | 7 | 1.0 | hann | centroid_power | 7.00, 7.00, 7.00, 7.00, 7.00, 7.00 (4.6e-17) |
| oned | 7 | 1.0 | hann | centroid_band_power | 7.00, 7.00, 7.00, 7.00, 7.00, 7.00 (4.6e-17) |
| oned | 7 | 1.25 | raw | centroid_amp | 9.52, 10.90, 12.51, 14.35, 16.48, 18.96 (0.011) |
| oned | 7 | 1.25 | raw | centroid_power | 7.06, 7.06, 7.06, 7.06, 7.06, 7.06 (5.3e-08) |
| oned | 7 | 1.25 | raw | centroid_band_power | 7.04, 7.04, 7.04, 7.04, 7.04, 7.04 (5.5e-11) |
| oned | 7 | 1.25 | hann | centroid_amp | 9.36, 10.82, 12.39, 14.05, 16.34, 18.75 (0.01) |
| oned | 7 | 1.25 | hann | centroid_power | 7.06, 7.06, 7.06, 7.06, 7.06, 7.06 (3.3e-07) |
| oned | 7 | 1.25 | hann | centroid_band_power | 7.04, 7.04, 7.04, 7.04, 7.04, 7.04 (1.2e-07) |
| oned | 7 | 1.75 | raw | centroid_amp | 13.13, 17.41, 23.32, 31.16, 41.84, 56.39 (0.074) |
| oned | 7 | 1.75 | raw | centroid_power | 7.35, 7.39, 7.41, 7.41, 7.42, 7.42 (3.6e-06) |
| oned | 7 | 1.75 | raw | centroid_band_power | 7.20, 7.20, 7.20, 7.20, 7.20, 7.20 (1.5e-09) |
| oned | 7 | 1.75 | hann | centroid_amp | 12.71, 17.13, 22.77, 29.79, 40.90, 54.83 (0.078) |
| oned | 7 | 1.75 | hann | centroid_power | 7.36, 7.39, 7.41, 7.41, 7.42, 7.42 (1.1e-05) |
| oned | 7 | 1.75 | hann | centroid_band_power | 7.20, 7.20, 7.20, 7.20, 7.20, 7.20 (1.2e-06) |
| oned | 7 | 2.6 | raw | centroid_amp | 16.57, 24.56, 36.97, 55.57, 84.24, 128.51 (0.22) |
| oned | 7 | 2.6 | raw | centroid_power | 7.93, 8.09, 8.19, 8.24, 8.27, 8.29 (6.2e-05) |
| oned | 7 | 2.6 | raw | centroid_band_power | 7.46, 7.45, 7.45, 7.45, 7.45, 7.45 (1.4e-08) |
| oned | 7 | 2.6 | hann | centroid_amp | 15.91, 23.98, 35.68, 52.27, 81.28, 123.02 (0.27) |
| oned | 7 | 2.6 | hann | centroid_power | 7.94, 8.09, 8.19, 8.24, 8.27, 8.29 (0.00013) |
| oned | 7 | 2.6 | hann | centroid_band_power | 7.46, 7.45, 7.45, 7.45, 7.45, 7.45 (5.8e-06) |
| oned | 3.5 | 0.9 | raw | centroid_amp | 11.36, 18.97, 33.19, 59.86, 109.93, 204.29 (14) |
| oned | 3.5 | 0.9 | raw | centroid_power | 4.08, 4.21, 4.35, 4.49, 4.64, 4.78 (0.22) |
| oned | 3.5 | 0.9 | raw | centroid_band_power | 3.85, 3.83, 3.82, 3.82, 3.82, 3.82 (0.07) |
| oned | 3.5 | 0.9 | hann | centroid_amp | 4.15, 4.34, 4.47, 4.66, 4.81, 4.91 (0.0076) |
| oned | 3.5 | 0.9 | hann | centroid_power | 3.50, 3.50, 3.50, 3.50, 3.50, 3.50 (0.00041) |
| oned | 3.5 | 0.9 | hann | centroid_band_power | 3.50, 3.50, 3.50, 3.50, 3.50, 3.50 (0.00041) |
| oned | 3.5 | 1.0 | raw | centroid_amp | 11.46, 19.19, 33.65, 60.73, 111.60, 207.43 (13) |
| oned | 3.5 | 1.0 | raw | centroid_power | 4.07, 4.21, 4.35, 4.49, 4.64, 4.78 (0.21) |
| oned | 3.5 | 1.0 | raw | centroid_band_power | 3.85, 3.83, 3.82, 3.82, 3.82, 3.81 (0.069) |
| oned | 3.5 | 1.0 | hann | centroid_amp | 3.53, 3.53, 3.53, 3.53, 3.53, 3.53 (0.0055) |
| oned | 3.5 | 1.0 | hann | centroid_power | 3.50, 3.50, 3.50, 3.50, 3.50, 3.50 (0.00042) |
| oned | 3.5 | 1.0 | hann | centroid_band_power | 3.50, 3.50, 3.50, 3.50, 3.50, 3.50 (0.00042) |
| oned | 3.5 | 1.25 | raw | centroid_amp | 11.70, 19.59, 34.42, 62.12, 114.15, 212.17 (11) |
| oned | 3.5 | 1.25 | raw | centroid_power | 4.10, 4.24, 4.38, 4.53, 4.67, 4.82 (0.19) |
| oned | 3.5 | 1.25 | raw | centroid_band_power | 3.88, 3.86, 3.85, 3.85, 3.85, 3.85 (0.066) |
| oned | 3.5 | 1.25 | hann | centroid_amp | 5.18, 5.95, 6.62, 7.78, 8.95, 9.98 (0.027) |
| oned | 3.5 | 1.25 | hann | centroid_power | 3.53, 3.53, 3.53, 3.53, 3.53, 3.53 (0.00044) |
| oned | 3.5 | 1.25 | hann | centroid_band_power | 3.53, 3.53, 3.53, 3.53, 3.53, 3.53 (0.00044) |
| oned | 3.5 | 1.75 | raw | centroid_amp | 12.22, 20.22, 35.27, 63.14, 115.48, 214.11 (8.3) |
| oned | 3.5 | 1.75 | raw | centroid_power | 4.26, 4.41, 4.56, 4.71, 4.86, 5.00 (0.16) |
| oned | 3.5 | 1.75 | raw | centroid_band_power | 4.01, 3.99, 3.99, 3.99, 3.99, 3.98 (0.062) |
| oned | 3.5 | 1.75 | hann | centroid_amp | 7.89, 10.50, 13.23, 18.48, 24.90, 31.60 (0.1) |
| oned | 3.5 | 1.75 | hann | centroid_power | 3.69, 3.70, 3.70, 3.71, 3.71, 3.71 (0.0005) |
| oned | 3.5 | 1.75 | hann | centroid_band_power | 3.67, 3.66, 3.66, 3.66, 3.66, 3.66 (0.00049) |
| oned | 3.5 | 2.6 | raw | centroid_amp | 13.13, 21.41, 36.67, 64.31, 115.83, 212.63 (5.5) |
| oned | 3.5 | 2.6 | raw | centroid_power | 4.60, 4.79, 4.97, 5.13, 5.29, 5.44 (0.13) |
| oned | 3.5 | 2.6 | raw | centroid_band_power | 4.27, 4.25, 4.24, 4.24, 4.24, 4.24 (0.058) |
| oned | 3.5 | 2.6 | hann | centroid_amp | 10.84, 16.08, 22.45, 35.50, 53.88, 76.35 (0.34) |
| oned | 3.5 | 2.6 | hann | centroid_power | 4.04, 4.09, 4.11, 4.13, 4.14, 4.15 (0.00073) |
| oned | 3.5 | 2.6 | hann | centroid_band_power | 3.93, 3.92, 3.92, 3.92, 3.92, 3.92 (0.00055) |
| oned | 5.5 | 0.9 | raw | centroid_amp | 12.53, 19.88, 33.68, 59.65, 108.53, 200.76 (14) |
| oned | 5.5 | 0.9 | raw | centroid_power | 5.98, 6.12, 6.25, 6.39, 6.54, 6.68 (0.21) |
| oned | 5.5 | 0.9 | raw | centroid_band_power | 5.76, 5.74, 5.73, 5.73, 5.73, 5.73 (0.058) |
| oned | 5.5 | 0.9 | hann | centroid_amp | 6.32, 6.61, 6.88, 7.07, 7.35, 7.60 (0.011) |
| oned | 5.5 | 0.9 | hann | centroid_power | 5.51, 5.51, 5.51, 5.51, 5.51, 5.51 (0.00063) |
| oned | 5.5 | 0.9 | hann | centroid_band_power | 5.51, 5.51, 5.51, 5.51, 5.51, 5.51 (0.00063) |
| oned | 5.5 | 1.0 | raw | centroid_amp | 12.59, 20.05, 34.10, 60.50, 110.19, 203.93 (13) |
| oned | 5.5 | 1.0 | raw | centroid_power | 5.97, 6.11, 6.25, 6.39, 6.53, 6.67 (0.2) |
| oned | 5.5 | 1.0 | raw | centroid_band_power | 5.75, 5.73, 5.72, 5.72, 5.72, 5.72 (0.058) |
| oned | 5.5 | 1.0 | hann | centroid_amp | 5.47, 5.47, 5.47, 5.47, 5.47, 5.47 (0.0087) |
| oned | 5.5 | 1.0 | hann | centroid_power | 5.50, 5.50, 5.50, 5.50, 5.50, 5.50 (0.00064) |
| oned | 5.5 | 1.0 | hann | centroid_band_power | 5.50, 5.50, 5.50, 5.50, 5.50, 5.50 (0.00064) |
| oned | 5.5 | 1.25 | raw | centroid_amp | 12.87, 20.51, 34.85, 61.79, 112.48, 208.11 (11) |
| oned | 5.5 | 1.25 | raw | centroid_power | 6.02, 6.16, 6.30, 6.44, 6.58, 6.73 (0.18) |
| oned | 5.5 | 1.25 | raw | centroid_band_power | 5.79, 5.77, 5.76, 5.76, 5.76, 5.76 (0.057) |
| oned | 5.5 | 1.25 | hann | centroid_amp | 7.59, 8.65, 9.85, 10.91, 12.85, 14.92 (0.024) |
| oned | 5.5 | 1.25 | hann | centroid_power | 5.54, 5.55, 5.55, 5.55, 5.55, 5.55 (0.00067) |
| oned | 5.5 | 1.25 | hann | centroid_band_power | 5.54, 5.54, 5.54, 5.54, 5.54, 5.54 (0.00067) |
| oned | 5.5 | 1.75 | raw | centroid_amp | 13.68, 21.58, 36.08, 63.09, 113.66, 209.06 (8.6) |
| oned | 5.5 | 1.75 | raw | centroid_power | 6.25, 6.42, 6.57, 6.72, 6.87, 7.01 (0.15) |
| oned | 5.5 | 1.75 | raw | centroid_band_power | 5.96, 5.94, 5.94, 5.94, 5.94, 5.94 (0.056) |
| oned | 5.5 | 1.75 | hann | centroid_amp | 10.78, 14.18, 18.53, 23.10, 32.80, 44.78 (0.12) |
| oned | 5.5 | 1.75 | hann | centroid_power | 5.79, 5.81, 5.82, 5.82, 5.82, 5.83 (0.00072) |
| oned | 5.5 | 1.75 | hann | centroid_band_power | 5.71, 5.71, 5.71, 5.71, 5.71, 5.71 (0.00071) |
| oned | 5.5 | 2.6 | raw | centroid_amp | 15.01, 23.62, 38.86, 66.19, 116.24, 209.58 (5.3) |
| oned | 5.5 | 2.6 | raw | centroid_power | 6.73, 6.98, 7.19, 7.37, 7.54, 7.70 (0.13) |
| oned | 5.5 | 2.6 | raw | centroid_band_power | 6.26, 6.24, 6.24, 6.23, 6.23, 6.23 (0.055) |
| oned | 5.5 | 2.6 | hann | centroid_amp | 13.97, 20.52, 29.66, 40.82, 66.87, 102.86 (0.34) |
| oned | 5.5 | 2.6 | hann | centroid_power | 6.28, 6.38, 6.45, 6.48, 6.50, 6.51 (0.00083) |
| oned | 5.5 | 2.6 | hann | centroid_band_power | 6.02, 6.01, 6.01, 6.01, 6.01, 6.01 (0.00076) |
| oned | 6.3 | 0.9 | raw | centroid_amp | 12.90, 20.14, 33.74, 59.27, 107.31, 197.96 (15) |
| oned | 6.3 | 0.9 | raw | centroid_power | 6.49, 6.60, 6.71, 6.82, 6.94, 7.05 (0.14) |
| oned | 6.3 | 0.9 | raw | centroid_band_power | 6.33, 6.32, 6.32, 6.32, 6.32, 6.32 (0.037) |
| oned | 6.3 | 0.9 | hann | centroid_amp | 7.14, 7.51, 7.83, 8.13, 8.39, 8.57 (0.013) |
| oned | 6.3 | 0.9 | hann | centroid_power | 6.31, 6.31, 6.31, 6.31, 6.31, 6.31 (0.00045) |
| oned | 6.3 | 0.9 | hann | centroid_band_power | 6.31, 6.31, 6.31, 6.31, 6.31, 6.31 (0.00045) |
| oned | 6.3 | 1.0 | raw | centroid_amp | 12.82, 20.03, 33.58, 59.00, 106.85, 197.12 (16) |
| oned | 6.3 | 1.0 | raw | centroid_power | 6.48, 6.60, 6.71, 6.82, 6.93, 7.04 (0.14) |
| oned | 6.3 | 1.0 | raw | centroid_band_power | 6.32, 6.31, 6.31, 6.31, 6.31, 6.31 (0.04) |
| oned | 6.3 | 1.0 | hann | centroid_amp | 6.25, 6.25, 6.25, 6.25, 6.25, 6.25 (0.0083) |
| oned | 6.3 | 1.0 | hann | centroid_power | 6.30, 6.30, 6.30, 6.30, 6.30, 6.30 (0.00045) |
| oned | 6.3 | 1.0 | hann | centroid_band_power | 6.30, 6.30, 6.30, 6.30, 6.30, 6.30 (0.00045) |
| oned | 6.3 | 1.25 | raw | centroid_amp | 13.04, 20.13, 33.36, 58.15, 104.79, 192.79 (16) |
| oned | 6.3 | 1.25 | raw | centroid_power | 6.55, 6.66, 6.77, 6.89, 7.00, 7.11 (0.15) |
| oned | 6.3 | 1.25 | raw | centroid_band_power | 6.38, 6.37, 6.37, 6.37, 6.37, 6.37 (0.045) |
| oned | 6.3 | 1.25 | hann | centroid_amp | 8.40, 9.68, 11.09, 12.73, 14.44, 15.99 (0.035) |
| oned | 6.3 | 1.25 | hann | centroid_power | 6.35, 6.35, 6.35, 6.35, 6.36, 6.36 (0.00045) |
| oned | 6.3 | 1.25 | hann | centroid_band_power | 6.34, 6.34, 6.34, 6.34, 6.34, 6.34 (0.00045) |
| oned | 6.3 | 1.75 | raw | centroid_amp | 14.05, 21.38, 34.55, 58.51, 102.99, 186.31 (16) |
| oned | 6.3 | 1.75 | raw | centroid_power | 6.83, 6.97, 7.10, 7.21, 7.32, 7.44 (0.16) |
| oned | 6.3 | 1.75 | raw | centroid_band_power | 6.59, 6.58, 6.58, 6.58, 6.58, 6.58 (0.053) |
| oned | 6.3 | 1.75 | hann | centroid_amp | 11.60, 15.46, 20.57, 27.57, 35.94, 44.98 (0.097) |
| oned | 6.3 | 1.75 | hann | centroid_power | 6.62, 6.65, 6.66, 6.67, 6.67, 6.67 (0.00052) |
| oned | 6.3 | 1.75 | hann | centroid_band_power | 6.54, 6.54, 6.54, 6.54, 6.54, 6.54 (0.00045) |
| oned | 6.3 | 2.6 | raw | centroid_amp | 15.59, 24.03, 38.53, 63.80, 109.01, 190.62 (14) |
| oned | 6.3 | 2.6 | raw | centroid_power | 7.38, 7.63, 7.81, 7.96, 8.10, 8.22 (0.17) |
| oned | 6.3 | 2.6 | raw | centroid_band_power | 6.94, 6.93, 6.92, 6.92, 6.92, 6.92 (0.061) |
| oned | 6.3 | 2.6 | hann | centroid_amp | 14.82, 21.85, 32.61, 49.24, 71.44, 99.49 (0.71) |
| oned | 6.3 | 2.6 | hann | centroid_power | 7.16, 7.30, 7.37, 7.42, 7.45, 7.46 (0.0016) |
| oned | 6.3 | 2.6 | hann | centroid_band_power | 6.89, 6.88, 6.88, 6.88, 6.88, 6.88 (0.00047) |
