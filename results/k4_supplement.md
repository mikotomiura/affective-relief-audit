# K4 supplement: the centroid of the sum field up to N = 16384, extrapolations and an estimate

Conditions: `experiments/conditions/k4_supplement.json` (SHA-256 `790ad9d15d8bca8134c87c8452e0754ae275acba2860425e20dfa963f8189c0b`). Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`). Reference values of the implementation check: `results/k4_centroid_2d.json` (SHA-256 `257173c1b375595146a4f23a746fb8e2d8537a6df6426eeb1c82b40d37f6872a`). numpy 2.5.4, scipy 1.18.1, Python 3.13.12. Script SHA-256 `3547a2332cdb12d45eb8b9a69e2fb698f55f076cd7bded845cc2ebd086027886`, repository commit `f4067f515bc6320b5c4d03e76e36e1ddce32fae8`. Run started 2026-10-26T03:11:55+00:00 and finished 2026-10-26T03:45:47+00:00 (Darwin arm64, 10 logical CPUs).

Exploratory: designed after the results of K4 had been seen; not blind; not evidence for the claims of the main text. Nothing here is a proof, and the extrapolated values are not limits.

## Reading of the conditions fixed before the run

- Ranges are taken from the end of grids_N: the extrapolations use the last six N (512-16384) and, for the sensitivity range, the last five (1024-16384); the slopes of approach 1 use the last four (2048-16384) and the last three (4096-16384). With the grids of the conditions these are the ranges named there.
- Local slopes are per seed (atact.stats.local_slopes) and are placed at the geometric mean of the two grids. 'Mean local slope' is the mean over the 20 seeds.
- E1 is fitted as ln C_N = ln(a + b (N/N_max)^c), N_max the largest N of the range, which is the same model with b rescaled; scipy.optimize.least_squares (trust-region reflective) with bounds a >= -(1 - 1e-9) min C_N, b >= 0 and 0 <= c <= 1.5, started from a = 0, c = the last local slope of the range clipped to [0.01, 1.49] and b = C at N_max. A fit counts as failed if the optimiser reports no success or if c ends within 1e-06 of 0 or 1.5.
- Shell spectrum: rho = |k| in cycles per domain for every bin with rho >= 1; the shell index is floor(8 log2 rho); each bin enters with its weight of the half-plane sum (2 or 1), so that a shell holds the sum over the full plane. The density divides the shell sum of |H^_k| / N^2 by the width of the shell (the last shell cut at the largest rho of the grid, unless that would give it zero width; the last shell never enters the band of the shell exponent). The shell exponent is the least-squares slope of ln density on the logarithm of the geometric centre of the shell.
- Rate of approach: the deficit is e(gamma) - s_j for the five local slopes of the extrapolation range; 'their seed means decrease with N' is strict for each consecutive pair.
- The implementation check is made after all N <= 4096 have been computed and before any larger N is computed; if it fails, the run stops there.
- E1 failure cases beyond those on c: the growing term changes the model over the range by less than 1e-6 max C_N (b (1 - (N_min/N_max)^c) < 1e-6 max C_N; this includes b at its lower bound 0, where c is not identified), a ends within 1e-9 min C_N of its lower bound, or the fitted model value is not finite and positive at every N. Inside the optimiser a non-positive model value is evaluated as 1e-300 (a large residual); such a fit is then failed by the last rule.
- E3 uses the exact delta(gamma) (7/18, 3/10, 1/14, 3/26); the condition file also lists them rounded to four places.
- Shells are half-open, [2^(j/8), 2^((j+1)/8)); a bin is assigned by floor(8 log2 rho) in floating point, so a bin with rho exactly on an edge (for example rho = 512) goes to the shell that starts there.
- The rate of approach is given an interval only if at least 2 seeds have all five deficits positive. The difference between the two grids in the shell table is the seed mean at the larger N minus that at the smaller N, without an interval.
- Standard errors by N and per-seed values (local slopes, fits, deficit signs) are in the JSON file; the Markdown file shows the seed means and the intervals.

## Implementation check

1440 of 1440 values (N 128-4096) compared with K4; largest relative difference 6.73e-14; passed (tolerance 1e-09).

## Approach 1: local slopes and slopes over the larger ranges

Local slopes: seed means between consecutive N (128-256, ..., 8192-16384). Slopes: simultaneous intervals at level 0.99583.

| f | gamma | e(gamma) | local slopes | slope, interval, outcome | slope, interval, outcome |
|---|---|---|---|---|---|
| 3 | 0.9 | 0.3889 | 0.241, 0.264, 0.285, 0.304, 0.320, 0.334, 0.345 | 2048-16384: 0.3332 [0.3278, 0.3385] below | 4096-16384: 0.3394 [0.3346, 0.3442] below |
| 3 | 1.25 | 0.7000 | 0.514, 0.564, 0.603, 0.631, 0.651, 0.664, 0.673 | 2048-16384: 0.6628 [0.6616, 0.6641] below | 4096-16384: 0.6688 [0.6678, 0.6697] below |
| 3 | 1.75 | 0.9286 | 0.728, 0.766, 0.796, 0.816, 0.831, 0.843, 0.852 | 2048-16384: 0.8422 [0.8414, 0.8431] below | 4096-16384: 0.8476 [0.8468, 0.8484] below |
| 3 | 2.6 | 1.0000 | 0.834, 0.864, 0.888, 0.906, 0.919, 0.930, 0.938 | 2048-16384: 0.9290 [0.9280, 0.9301] below | 4096-16384: 0.9339 [0.9330, 0.9349] below |
| 5 | 0.9 | 0.3889 | 0.238, 0.254, 0.275, 0.295, 0.312, 0.327, 0.339 | 2048-16384: 0.3263 [0.3203, 0.3322] below | 4096-16384: 0.3331 [0.3277, 0.3385] below |
| 5 | 1.25 | 0.7000 | 0.496, 0.545, 0.588, 0.621, 0.644, 0.660, 0.671 | 2048-16384: 0.6582 [0.6566, 0.6599] below | 4096-16384: 0.6652 [0.6639, 0.6664] below |
| 5 | 1.75 | 0.9286 | 0.722, 0.759, 0.790, 0.813, 0.829, 0.842, 0.852 | 2048-16384: 0.8411 [0.8405, 0.8418] below | 4096-16384: 0.8468 [0.8461, 0.8475] below |
| 5 | 2.6 | 1.0000 | 0.832, 0.862, 0.886, 0.905, 0.918, 0.929, 0.938 | 2048-16384: 0.9286 [0.9276, 0.9296] below | 4096-16384: 0.9336 [0.9327, 0.9346] below |
| 7 | 0.9 | 0.3889 | 0.246, 0.248, 0.268, 0.288, 0.306, 0.322, 0.335 | 2048-16384: 0.3210 [0.3145, 0.3274] below | 4096-16384: 0.3282 [0.3224, 0.3341] below |
| 7 | 1.25 | 0.7000 | 0.492, 0.532, 0.577, 0.613, 0.638, 0.656, 0.668 | 2048-16384: 0.6543 [0.6523, 0.6564] below | 4096-16384: 0.6621 [0.6605, 0.6636] below |
| 7 | 1.75 | 0.9286 | 0.725, 0.754, 0.786, 0.810, 0.828, 0.841, 0.851 | 2048-16384: 0.8402 [0.8396, 0.8408] below | 4096-16384: 0.8461 [0.8455, 0.8467] below |
| 7 | 2.6 | 1.0000 | 0.836, 0.860, 0.884, 0.904, 0.918, 0.929, 0.938 | 2048-16384: 0.9283 [0.9273, 0.9292] below | 4096-16384: 0.9333 [0.9324, 0.9343] below |

## Approach 2: extrapolated exponents

Mean over seeds and simultaneous interval (level 0.99583); E1 over the seeds whose fit did not fail.

| f | gamma | e(gamma) | range | form | value | interval | failed seeds | outcome |
|---|---|---|---|---|---|---|---|---|
| 3 | 0.9 | 0.3889 | 512-16384 | E1 | 0.3871 | [0.3860, 0.3883] | 0 | below |
| 3 | 0.9 | 0.3889 | 512-16384 | E2 | 0.4866 | [0.4797, 0.4935] | 0 | above |
| 3 | 0.9 | 0.3889 | 512-16384 | E3 | 0.3741 | [0.3717, 0.3765] | 0 | below |
| 3 | 0.9 | 0.3889 | 1024-16384 | E1 | 0.3868 | [0.3859, 0.3878] | 0 | below |
| 3 | 0.9 | 0.3889 | 1024-16384 | E2 | 0.4870 | [0.4796, 0.4944] | 0 | above |
| 3 | 0.9 | 0.3889 | 1024-16384 | E3 | 0.3768 | [0.3748, 0.3788] | 0 | below |
| 3 | 1.25 | 0.7000 | 512-16384 | E1 | 0.6865 | [0.6855, 0.6875] | 0 | below |
| 3 | 1.25 | 0.7000 | 512-16384 | E2 | 0.8439 | [0.8326, 0.8552] | 0 | above |
| 3 | 1.25 | 0.7000 | 512-16384 | E3 | 0.7303 | [0.7267, 0.7339] | 0 | above |
| 3 | 1.25 | 0.7000 | 1024-16384 | E1 | 0.6875 | [0.6867, 0.6882] | 0 | below |
| 3 | 1.25 | 0.7000 | 1024-16384 | E2 | 0.8235 | [0.8148, 0.8323] | 0 | above |
| 3 | 1.25 | 0.7000 | 1024-16384 | E3 | 0.7236 | [0.7209, 0.7263] | 0 | above |
| 3 | 1.75 | 0.9286 | 512-16384 | E1 | 0.8543 | [0.8531, 0.8554] | 0 | below |
| 3 | 1.75 | 0.9286 | 512-16384 | E2 | 0.9881 | [0.9821, 0.9941] | 0 | above |
| 3 | 1.75 | 0.9286 | 512-16384 | E3 | 1.1122 | [1.1019, 1.1226] | 0 | above |
| 3 | 1.75 | 0.9286 | 1024-16384 | E1 | 0.8577 | [0.8567, 0.8586] | 0 | below |
| 3 | 1.75 | 0.9286 | 1024-16384 | E2 | 0.9795 | [0.9761, 0.9829] | 0 | above |
| 3 | 1.75 | 0.9286 | 1024-16384 | E3 | 1.0791 | [1.0735, 1.0847] | 0 | above |
| 3 | 2.6 | 1.0000 | 512-16384 | E1 | 0.9375 | [0.9365, 0.9385] | 0 | below |
| 3 | 2.6 | 1.0000 | 512-16384 | E2 | 1.0571 | [1.0536, 1.0607] | 0 | above |
| 3 | 2.6 | 1.0000 | 512-16384 | E3 | 1.0716 | [1.0679, 1.0754] | 0 | above |
| 3 | 2.6 | 1.0000 | 1024-16384 | E1 | 0.9412 | [0.9402, 0.9421] | 0 | below |
| 3 | 2.6 | 1.0000 | 1024-16384 | E2 | 1.0522 | [1.0501, 1.0543] | 0 | above |
| 3 | 2.6 | 1.0000 | 1024-16384 | E3 | 1.0587 | [1.0565, 1.0608] | 0 | above |
| 5 | 0.9 | 0.3889 | 512-16384 | E1 | 0.3866 | [0.3855, 0.3878] | 0 | below |
| 5 | 0.9 | 0.3889 | 512-16384 | E2 | 0.4921 | [0.4854, 0.4989] | 0 | above |
| 5 | 0.9 | 0.3889 | 512-16384 | E3 | 0.3705 | [0.3676, 0.3734] | 0 | below |
| 5 | 0.9 | 0.3889 | 1024-16384 | E1 | 0.3864 | [0.3853, 0.3874] | 0 | below |
| 5 | 0.9 | 0.3889 | 1024-16384 | E2 | 0.4939 | [0.4863, 0.5015] | 0 | above |
| 5 | 0.9 | 0.3889 | 1024-16384 | E3 | 0.3738 | [0.3714, 0.3762] | 0 | below |
| 5 | 1.25 | 0.7000 | 512-16384 | E1 | 0.6865 | [0.6855, 0.6875] | 0 | below |
| 5 | 1.25 | 0.7000 | 512-16384 | E2 | 0.8701 | [0.8565, 0.8838] | 0 | above |
| 5 | 1.25 | 0.7000 | 512-16384 | E3 | 0.7372 | [0.7330, 0.7414] | 0 | above |
| 5 | 1.25 | 0.7000 | 1024-16384 | E1 | 0.6873 | [0.6865, 0.6881] | 0 | below |
| 5 | 1.25 | 0.7000 | 1024-16384 | E2 | 0.8459 | [0.8346, 0.8572] | 0 | above |
| 5 | 1.25 | 0.7000 | 1024-16384 | E3 | 0.7292 | [0.7259, 0.7326] | 0 | above |
| 5 | 1.75 | 0.9286 | 512-16384 | E1 | 0.8543 | [0.8532, 0.8555] | 0 | below |
| 5 | 1.75 | 0.9286 | 512-16384 | E2 | 0.9992 | [0.9912, 1.0073] | 0 | above |
| 5 | 1.75 | 0.9286 | 512-16384 | E3 | 1.1335 | [1.1192, 1.1479] | 0 | above |
| 5 | 1.75 | 0.9286 | 1024-16384 | E1 | 0.8576 | [0.8566, 0.8586] | 0 | below |
| 5 | 1.75 | 0.9286 | 1024-16384 | E2 | 0.9870 | [0.9817, 0.9922] | 0 | above |
| 5 | 1.75 | 0.9286 | 1024-16384 | E3 | 1.0927 | [1.0840, 1.1015] | 0 | above |
| 5 | 2.6 | 1.0000 | 512-16384 | E1 | 0.9375 | [0.9365, 0.9385] | 0 | below |
| 5 | 2.6 | 1.0000 | 512-16384 | E2 | 1.0623 | [1.0575, 1.0671] | 0 | above |
| 5 | 2.6 | 1.0000 | 512-16384 | E3 | 1.0773 | [1.0721, 1.0825] | 0 | above |
| 5 | 2.6 | 1.0000 | 1024-16384 | E1 | 0.9410 | [0.9401, 0.9420] | 0 | below |
| 5 | 2.6 | 1.0000 | 1024-16384 | E2 | 1.0547 | [1.0518, 1.0576] | 0 | above |
| 5 | 2.6 | 1.0000 | 1024-16384 | E3 | 1.0613 | [1.0583, 1.0644] | 0 | above |
| 7 | 0.9 | 0.3889 | 512-16384 | E1 | 0.3858 | [0.3846, 0.3870] | 0 | below |
| 7 | 0.9 | 0.3889 | 512-16384 | E2 | 0.4944 | [0.4879, 0.5009] | 0 | above |
| 7 | 0.9 | 0.3889 | 512-16384 | E3 | 0.3672 | [0.3639, 0.3705] | 0 | below |
| 7 | 0.9 | 0.3889 | 1024-16384 | E1 | 0.3860 | [0.3849, 0.3871] | 0 | below |
| 7 | 0.9 | 0.3889 | 1024-16384 | E2 | 0.4985 | [0.4910, 0.5061] | 0 | above |
| 7 | 0.9 | 0.3889 | 1024-16384 | E3 | 0.3713 | [0.3686, 0.3740] | 0 | below |
| 7 | 1.25 | 0.7000 | 512-16384 | E1 | 0.6864 | [0.6853, 0.6874] | 0 | below |
| 7 | 1.25 | 0.7000 | 512-16384 | E2 | 0.8901 | [0.8747, 0.9055] | 0 | above |
| 7 | 1.25 | 0.7000 | 512-16384 | E3 | 0.7422 | [0.7376, 0.7467] | 0 | above |
| 7 | 1.25 | 0.7000 | 1024-16384 | E1 | 0.6873 | [0.6864, 0.6882] | 0 | below |
| 7 | 1.25 | 0.7000 | 1024-16384 | E2 | 0.8649 | [0.8515, 0.8782] | 0 | above |
| 7 | 1.25 | 0.7000 | 1024-16384 | E3 | 0.7340 | [0.7301, 0.7378] | 0 | above |
| 7 | 1.75 | 0.9286 | 512-16384 | E1 | 0.8543 | [0.8531, 0.8555] | 0 | below |
| 7 | 1.75 | 0.9286 | 512-16384 | E2 | 1.0077 | [0.9978, 1.0175] | 0 | above |
| 7 | 1.75 | 0.9286 | 512-16384 | E3 | 1.1498 | [1.1320, 1.1677] | 0 | above |
| 7 | 1.75 | 0.9286 | 1024-16384 | E1 | 0.8576 | [0.8565, 0.8586] | 0 | below |
| 7 | 1.75 | 0.9286 | 1024-16384 | E2 | 0.9942 | [0.9872, 1.0012] | 0 | above |
| 7 | 1.75 | 0.9286 | 1024-16384 | E3 | 1.1058 | [1.0940, 1.1176] | 0 | above |
| 7 | 2.6 | 1.0000 | 512-16384 | E1 | 0.9375 | [0.9364, 0.9385] | 0 | below |
| 7 | 2.6 | 1.0000 | 512-16384 | E2 | 1.0656 | [1.0598, 1.0715] | 0 | above |
| 7 | 2.6 | 1.0000 | 512-16384 | E3 | 1.0810 | [1.0746, 1.0874] | 0 | above |
| 7 | 2.6 | 1.0000 | 1024-16384 | E1 | 0.9410 | [0.9401, 0.9420] | 0 | below |
| 7 | 2.6 | 1.0000 | 1024-16384 | E2 | 1.0577 | [1.0538, 1.0617] | 0 | above |
| 7 | 2.6 | 1.0000 | 1024-16384 | E3 | 1.0645 | [1.0604, 1.0686] | 0 | above |

## Approach 3: shell spectrum and rate of approach

Shell exponent: slope of ln(shell density) on ln rho over the shells in the band of the conditions, mean and simultaneous interval (level 0.99583), at the two largest N; target -(1/gamma + 1/2).

| f | gamma | target | N = 8192 | N = 16384 | difference |
|---|---|---|---|---|---|
| 3 | 0.9 | -1.6111 | -1.5219 [-1.5277, -1.5160] | -1.6021 [-1.6047, -1.5995] | -0.0802 |
| 3 | 1.25 | -1.3000 | -1.1557 [-1.1624, -1.1491] | -1.2736 [-1.2767, -1.2706] | -0.1179 |
| 3 | 1.75 | -1.0714 | -0.8704 [-0.8774, -0.8633] | -1.0231 [-1.0268, -1.0195] | -0.1528 |
| 3 | 2.6 | -0.8846 | -0.6244 [-0.6316, -0.6172] | -0.8086 [-0.8128, -0.8045] | -0.1842 |
| 5 | 0.9 | -1.6111 | -1.4984 [-1.5050, -1.4918] | -1.5996 [-1.6027, -1.5964] | -0.1012 |
| 5 | 1.25 | -1.3000 | -1.1089 [-1.1163, -1.1016] | -1.2630 [-1.2672, -1.2588] | -0.1541 |
| 5 | 1.75 | -1.0714 | -0.7981 [-0.8056, -0.7906] | -1.0012 [-1.0063, -0.9960] | -0.2031 |
| 5 | 2.6 | -0.8846 | -0.5258 [-0.5330, -0.5186] | -0.7715 [-0.7774, -0.7655] | -0.2457 |
| 7 | 0.9 | -1.6111 | -1.4874 [-1.4939, -1.4808] | -1.5990 [-1.6024, -1.5956] | -0.1116 |
| 7 | 1.25 | -1.3000 | -1.0830 [-1.0902, -1.0758] | -1.2570 [-1.2610, -1.2529] | -0.1740 |
| 7 | 1.75 | -1.0714 | -0.7552 [-0.7625, -0.7479] | -0.9875 [-0.9923, -0.9827] | -0.2323 |
| 7 | 2.6 | -0.8846 | -0.4653 [-0.4723, -0.4584] | -0.7470 [-0.7525, -0.7415] | -0.2817 |

Rate of approach over the local slopes of N 512-16384: deficit e(gamma) - s_j (seed means), number of seeds with all five deficits positive, fitted slope of ln deficit on ln N_j (95% interval over those seeds) and the target -delta(gamma).

| f | gamma | deficits | positive seeds | means decrease | rate | interval | target |
|---|---|---|---|---|---|---|---|
| 3 | 0.9 | +0.1034, +0.0845, +0.0684, +0.0549, +0.0440 | 20 | yes | -0.3092 | [-0.3134, -0.3050] | -0.3889 |
| 3 | 1.25 | +0.0968, +0.0689, +0.0495, +0.0358, +0.0267 | 20 | yes | -0.4658 | [-0.4749, -0.4567] | -0.3000 |
| 3 | 1.75 | +0.1330, +0.1125, +0.0974, +0.0855, +0.0764 | 20 | yes | -0.1996 | [-0.2039, -0.1953] | -0.0714 |
| 3 | 2.6 | +0.1116, +0.0942, +0.0811, +0.0703, +0.0618 | 20 | yes | -0.2126 | [-0.2154, -0.2098] | -0.1154 |
| 5 | 0.9 | +0.1140, +0.0939, +0.0765, +0.0619, +0.0497 | 20 | yes | -0.3002 | [-0.3046, -0.2959] | -0.3889 |
| 5 | 1.25 | +0.1116, +0.0789, +0.0561, +0.0402, +0.0295 | 20 | yes | -0.4805 | [-0.4892, -0.4719] | -0.3000 |
| 5 | 1.75 | +0.1385, +0.1154, +0.0991, +0.0866, +0.0770 | 20 | yes | -0.2108 | [-0.2165, -0.2052] | -0.0714 |
| 5 | 2.6 | +0.1141, +0.0952, +0.0817, +0.0707, +0.0620 | 20 | yes | -0.2187 | [-0.2226, -0.2148] | -0.1154 |
| 7 | 0.9 | +0.1213, +0.1009, +0.0827, +0.0672, +0.0542 | 20 | yes | -0.2922 | [-0.2966, -0.2878] | -0.3889 |
| 7 | 1.25 | +0.1231, +0.0873, +0.0617, +0.0440, +0.0319 | 20 | yes | -0.4880 | [-0.4962, -0.4799] | -0.3000 |
| 7 | 1.75 | +0.1426, +0.1181, +0.1005, +0.0875, +0.0775 | 20 | yes | -0.2191 | [-0.2258, -0.2124] | -0.0714 |
| 7 | 2.6 | +0.1156, +0.0964, +0.0821, +0.0711, +0.0622 | 20 | yes | -0.2227 | [-0.2275, -0.2179] | -0.1154 |

## Conclusions by prediction (written after the run)

This section was written by the author after reading the tables of this file; it is not produced by `--report`. The decisions follow the criteria fixed before the run; no criterion was changed after the run. This is an exploration designed after K4; it is not evidence for the claims of the main text, which rest on K4 alone.

- **Implementation check: passed.** All 1440 values for N 128-4096 agree with K4 (cb369b4) to a relative difference of 6.73e-14.
- **P-S1 holds** (12 of 12). The local slopes keep increasing up to N = 16384 in every cell (for example f = 5, gamma = 0.9: 0.312, 0.327, 0.339 for 2048-4096, 4096-8192, 8192-16384; gamma = 2.6: 0.918, 0.929, 0.938). From N = 512 on, the increase of the local slope per doubling of N becomes smaller in every cell (f = 5, gamma = 0.9: 0.020, 0.017, 0.015, 0.012); at smaller N it does not in five cells.
- **P-S2 holds** (12 of 12). Over N 4096-16384 every simultaneous interval lies below e(gamma) (for example f = 5: 0.333 against 0.389 at gamma = 0.9, 0.665 against 0.700 at 1.25, 0.847 against 0.929 at 1.75, 0.934 against 1 at 2.6). Extending N by a factor 4 beyond K4 does not change the finding of K4 on finite ranges, and it still does not settle the exponent as N tends to infinity.
- **P-S3 (no direction predicted): the extrapolated value depends on the form, and the three forms bracket e(gamma).** No E1 fit failed. E1 is below e(gamma) in all 24 cell-range combinations, closest at gamma = 0.9 (0.386-0.387 against 0.389) and farthest at gamma = 1.75 (0.854-0.858 against 0.929). E2 is above in all 24 (for example 0.49-0.50 at gamma = 0.9 and 1.05-1.07 at gamma = 2.6). E3 is below at gamma = 0.9 (0.367-0.377) and above in the other 18 combinations, reaching 1.08-1.15 at gamma = 1.75, above the largest value the estimate allows. The intervals over seeds are narrow (widths of 0.001 to 0.04) compared with these differences between forms, so the uncertainty of the extrapolation is set by the choice of form, not by the seeds. The extrapolations do not decide whether the exponent is e(gamma).
- **P-S4 holds in 7 of 12 items.** At N = 16384 the shell exponent over 512 <= rho < 2048 is within 0.05 of -(1/gamma + 1/2) at gamma = 0.9 and 1.25 for all f (differences of 0.009-0.043) and at gamma = 1.75 for f = 3. It is shallower than the target at gamma = 1.75 for f = 5 and 7 (-1.001 and -0.987 against -1.071) and at gamma = 2.6 for all f (-0.747 to -0.809 against -0.885). On the same band the exponent at N = 8192 is shallower in every cell, by 0.08-0.28, and the difference is largest where the target is shallowest (gamma = 2.6, f = 7). The shell exponent on a fixed band therefore still depends on the grid at these N, so the values at N = 16384 do not show the asymptotic decay. They are consistent with the assumed decay for gamma <= 1.25, but neither confirm nor exclude it for gamma >= 1.75.
- **P-S5 does not hold** (0 of 12). The first two conditions hold in every cell: the five deficits e(gamma) - s_j are positive in all 20 seeds and their means decrease with N. The third condition fails everywhere: the fitted rate does not match -delta(gamma). It is slower than the estimate at gamma = 0.9 (-0.29 to -0.31 against -0.389) and faster at gamma = 1.25 (-0.47 to -0.49 against -0.30), 1.75 (-0.20 to -0.22 against -0.071) and 2.6 (-0.21 to -0.22 against -0.115). The orders of the corrections derived in approach 3 are therefore not seen over N 512-16384. Together with P-S4, this is consistent with the shell spectrum not yet being in the asymptotic regime the estimate assumes at these N, but the run does not separate this from a failure of the assumptions themselves (the next term of S(rho), the constants P and D, or inflection points of the zero lines). As fixed before the run, the estimate is not extended after these results.
- **What this exploration supports.** Up to N = 16384 the local slopes of the sum field remain below e(gamma) = min(1, 1.5 - 1/gamma) and keep increasing; extrapolations of reasonable forms lie on both sides of e(gamma); and the estimate's premise on the shell decay is approached at gamma <= 1.25 but its predicted rate of approach is not observed. The exponent as N tends to infinity remains open. The text of Appendix B (slopes over finite N ranges and the rejection of the estimate as the slope over those ranges) is not changed by this file.

## Predictions

### P-S1: 12 of 12 items hold

Prediction: P-S1 (approach 1): in every one of the 12 cells, the mean local slope 4096-8192 is larger than the mean local slope 2048-4096, and the mean local slope 8192-16384 is larger than the mean local slope 4096-8192.

| f | gamma | local_last_three | holds |
|---|---|---|---|
| 3 | 0.900 | 0.320, 0.334, 0.345 | yes |
| 3 | 1.250 | 0.651, 0.664, 0.673 | yes |
| 3 | 1.750 | 0.831, 0.843, 0.852 | yes |
| 3 | 2.600 | 0.919, 0.930, 0.938 | yes |
| 5 | 0.900 | 0.312, 0.327, 0.339 | yes |
| 5 | 1.250 | 0.644, 0.660, 0.671 | yes |
| 5 | 1.750 | 0.829, 0.842, 0.852 | yes |
| 5 | 2.600 | 0.918, 0.929, 0.938 | yes |
| 7 | 0.900 | 0.306, 0.322, 0.335 | yes |
| 7 | 1.250 | 0.638, 0.656, 0.668 | yes |
| 7 | 1.750 | 0.828, 0.841, 0.851 | yes |
| 7 | 2.600 | 0.918, 0.929, 0.938 | yes |

### P-S2: 12 of 12 items hold

Prediction: P-S2 (approach 1): in every one of the 12 cells, the simultaneous interval of the slope over N 4096-16384 lies entirely below e(gamma).

| f | gamma | e | slope | lo | hi | holds |
|---|---|---|---|---|---|---|
| 3 | 0.900 | 0.389 | 0.339 | 0.335 | 0.344 | yes |
| 3 | 1.250 | 0.700 | 0.669 | 0.668 | 0.670 | yes |
| 3 | 1.750 | 0.929 | 0.848 | 0.847 | 0.848 | yes |
| 3 | 2.600 | 1.000 | 0.934 | 0.933 | 0.935 | yes |
| 5 | 0.900 | 0.389 | 0.333 | 0.328 | 0.339 | yes |
| 5 | 1.250 | 0.700 | 0.665 | 0.664 | 0.666 | yes |
| 5 | 1.750 | 0.929 | 0.847 | 0.846 | 0.848 | yes |
| 5 | 2.600 | 1.000 | 0.934 | 0.933 | 0.935 | yes |
| 7 | 0.900 | 0.389 | 0.328 | 0.322 | 0.334 | yes |
| 7 | 1.250 | 0.700 | 0.662 | 0.660 | 0.664 | yes |
| 7 | 1.750 | 0.929 | 0.846 | 0.845 | 0.847 | yes |
| 7 | 2.600 | 1.000 | 0.933 | 0.932 | 0.934 | yes |

### P-S3: outcomes reported (no direction predicted)

Prediction: P-S3 (approach 2): no direction is predicted. For each cell, form and range the outcome ('contains e(gamma)', 'below', 'above' or 'not determined') is reported.

See the table of approach 2.

### P-S4: 7 of 12 items hold

Prediction: P-S4 (approach 3, the assumption on the shell density): in every one of the 12 cells, the simultaneous interval of the shell exponent at N = 16384 contains a value within 0.05 of -(alpha + 1/2).

| f | gamma | target | exponent | lo | hi | width | holds |
|---|---|---|---|---|---|---|---|
| 3 | 0.900 | -1.611 | -1.602 | -1.605 | -1.600 | 0.005 | yes |
| 3 | 1.250 | -1.300 | -1.274 | -1.277 | -1.271 | 0.006 | yes |
| 3 | 1.750 | -1.071 | -1.023 | -1.027 | -1.020 | 0.007 | yes |
| 3 | 2.600 | -0.885 | -0.809 | -0.813 | -0.804 | 0.008 | no |
| 5 | 0.900 | -1.611 | -1.600 | -1.603 | -1.596 | 0.006 | yes |
| 5 | 1.250 | -1.300 | -1.263 | -1.267 | -1.259 | 0.008 | yes |
| 5 | 1.750 | -1.071 | -1.001 | -1.006 | -0.996 | 0.010 | no |
| 5 | 2.600 | -0.885 | -0.771 | -0.777 | -0.766 | 0.012 | no |
| 7 | 0.900 | -1.611 | -1.599 | -1.602 | -1.596 | 0.007 | yes |
| 7 | 1.250 | -1.300 | -1.257 | -1.261 | -1.253 | 0.008 | yes |
| 7 | 1.750 | -1.071 | -0.987 | -0.992 | -0.983 | 0.010 | no |
| 7 | 2.600 | -0.885 | -0.747 | -0.753 | -0.742 | 0.011 | no |

### P-S5: 0 of 12 items hold

Prediction: P-S5 (approach 3, the rate of approach): in every one of the 12 cells, the five deficits e(gamma) - s_j are positive in all 20 seeds, their seed means decrease with N, and the 95% interval of the fitted rate contains -delta(gamma). (The positive sign is implied by the estimate only at gamma = 1.25 and 1.75; at gamma = 0.9 and 2.6 it is expected from the local slopes of K4.)

| f | gamma | target | n_positive_seeds | mean_decreasing | rate | lo | hi | holds |
|---|---|---|---|---|---|---|---|---|
| 3 | 0.900 | -0.389 | 20 | True | -0.309 | -0.313 | -0.305 | no |
| 3 | 1.250 | -0.300 | 20 | True | -0.466 | -0.475 | -0.457 | no |
| 3 | 1.750 | -0.071 | 20 | True | -0.200 | -0.204 | -0.195 | no |
| 3 | 2.600 | -0.115 | 20 | True | -0.213 | -0.215 | -0.210 | no |
| 5 | 0.900 | -0.389 | 20 | True | -0.300 | -0.305 | -0.296 | no |
| 5 | 1.250 | -0.300 | 20 | True | -0.481 | -0.489 | -0.472 | no |
| 5 | 1.750 | -0.071 | 20 | True | -0.211 | -0.216 | -0.205 | no |
| 5 | 2.600 | -0.115 | 20 | True | -0.219 | -0.223 | -0.215 | no |
| 7 | 0.900 | -0.389 | 20 | True | -0.292 | -0.297 | -0.288 | no |
| 7 | 1.250 | -0.300 | 20 | True | -0.488 | -0.496 | -0.480 | no |
| 7 | 1.750 | -0.071 | 20 | True | -0.219 | -0.226 | -0.212 | no |
| 7 | 2.600 | -0.115 | 20 | True | -0.223 | -0.227 | -0.218 | no |

## Seed means of the centroid by N

| f | gamma | N 128 ... 16384 (mean; standard error of the last) |
|---|---|---|
| 3 | 0.9 | 13.10, 15.49, 18.60, 22.67, 28.01, 34.98, 44.11, 56.03 (0.8) |
| 3 | 1.25 | 18.14, 25.91, 38.30, 58.19, 90.14, 141.50, 224.24, 357.62 (3.9) |
| 3 | 1.75 | 26.53, 43.97, 74.80, 129.83, 228.58, 406.68, 729.53, 1316.94 (7.3) |
| 3 | 2.6 | 32.25, 57.50, 104.68, 193.78, 363.04, 686.39, 1307.50, 2505.24 (7.3) |
| 5 | 0.9 | 19.74, 23.29, 27.78, 33.62, 41.26, 51.25, 64.31, 81.37 (1.1) |
| 5 | 1.25 | 24.72, 34.87, 50.89, 76.54, 117.74, 183.98, 290.68, 462.68 (4.9) |
| 5 | 1.75 | 32.67, 53.89, 91.23, 157.76, 277.21, 492.61, 883.03, 1593.41 (8.5) |
| 5 | 2.6 | 37.56, 66.84, 121.47, 224.46, 420.25, 794.23, 1512.45, 2897.55 (7.9) |
| 7 | 0.9 | 25.60, 30.36, 36.07, 43.43, 53.04, 65.61, 82.02, 103.47 (1.4) |
| 7 | 1.25 | 29.97, 42.14, 60.93, 90.90, 139.02, 216.41, 341.02, 541.91 (5.6) |
| 7 | 1.75 | 36.82, 60.87, 102.68, 177.05, 310.52, 551.28, 987.55, 1781.40 (9.3) |
| 7 | 2.6 | 40.77, 72.80, 132.11, 243.87, 456.23, 861.98, 1641.07, 3143.58 (8.1) |
