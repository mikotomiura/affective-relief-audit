# K2: maximum gradient against N, and the eps example

Conditions: `experiments/conditions/k2_gradient_and_figures.json` (SHA-256 `1f1570a347deacf9dbd28579d6f323e9c3afe999df3b0969a7ed2790aab9503f`). Specification SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`. Script SHA-256 `6d0c1b6be9edf40859cfedbe8b8df8e1a95559fcbef0cdc38fd8fcbc979888f3`. Commit 4dba646 (dirty: True). numpy 2.5.4, scipy 1.18.1, Python 3.13.12, 4 workers. Run started 2026-10-26T04:25:14+00:00 and finished 2026-10-26T04:26:27+00:00 (Darwin arm64, 10 logical CPUs).

## Reading of the conditions fixed before the run

- The gradient of S2.6 is numpy.gradient(X, 1/N) for X = F, H and H_eps on the same F; its magnitude is hypot(d/dx, d/dy) and the maximum is over all grid points, edges included. edge_argmax is true when the grid point of the maximum lies in the first or last row or column.
- Primary normalisation ampsum (F = F_raw / 1.875); the secondary maxabs values (G and M only) use F_raw divided by its maximum absolute value over the same grid.
- G* is the largest G_4096 (ampsum) over the 20 seeds at the point 'high'. Each eps = e_min G* / (2 L) is computed once with its own (L, e_min); the main eps is used at every point, the sensitivity values at 'high' only.
- Ratios, slopes and changes are computed per seed and then summarised over seeds (mean, minimum, maximum; slopes also with the 95% t interval of S6.1). P-G5: |mean Meps_4096 / mean Meps_1024 - 1| < 0.05 and mean M_4096 / mean M_1024 > 2, on seed means.
- P-G4 and P-G6 are checked for every seed and N at the points with gamma > 1 and for every eps computed there. The shape error is max |T_{gamma,eps}(F) - T_gamma(F)| over the grid (that is max |H_eps - H| / s).
- Physical quantities use z = D H / (2 s_max): slope = D |grad H| / (2 s_max L), angle = atan(slope) in degrees, span = D (max H - min H) / (2 s_max). The band width at a seed is 2 eps L / G_4096 of that seed, in mm. The grid bound on the smoothed slope uses G*, the continuous bound uses G_bound = 2 pi f O / 1.875.

## Predictions

### P-G1: 2 of 2 items hold

- point = mid, min_ratio = 2.5664, mean_ratio = 3.3050, reference = 3.2813, holds = True
- point = high, min_ratio = 4.7325, mean_ratio = 5.4734, reference = 5.5080, holds = True

### P-G2: 2 of 2 items hold

- point = mid, mean = 0.4247, ci95 = [0.412176800646751, 0.4371497360180723], reference = 0.4286, holds = True
- point = high, mean = 0.6055, ci95 = [0.5923530951028383, 0.6186575228079613], reference = 0.6154, holds = True

### P-G3: 1 of 1 items hold

- max_ratio = 1.1375, mean_slope = 0.0031, holds = True

### P-G4: 4 of 4 items hold

- point = mid, eps = main, largest_Meps_over_bound = 0.9994, holds = True
- point = high, eps = main, largest_Meps_over_bound = 0.9987, holds = True
- point = high, eps = L50_e0.05, largest_Meps_over_bound = 0.9797, holds = True
- point = high, eps = L100_e0.4, largest_Meps_over_bound = 0.9956, holds = True

### P-G5: 1 of 3 items hold

- eps = main, Meps_4096_over_1024 = 1.0193, M_4096_over_1024 = 2.3215, holds = True
- eps = L50_e0.05, Meps_4096_over_1024 = 1.3788, M_4096_over_1024 = 2.3215, holds = False
- eps = L100_e0.4, Meps_4096_over_1024 = 1.0537, M_4096_over_1024 = 2.3215, holds = False

### P-G6: 4 of 4 items hold

- point = mid, eps = main, max = 0.1107, bound_eps^(1/gamma) = 0.5515, holds = True
- point = high, eps = main, max = 0.2236, bound_eps^(1/gamma) = 0.6699, holds = True
- point = high, eps = L50_e0.05, max = 0.1029, bound_eps^(1/gamma) = 0.3011, holds = True
- point = high, eps = L100_e0.4, max = 0.1743, bound_eps^(1/gamma) = 0.5131, holds = True

## Growth with N (seed means over 20 seeds; ampsum unless marked)

### point low

| quantity | N = 128 | N = 256 | N = 512 | N = 1024 | N = 2048 | N = 4096 | ratio 2048/128 (mean, min-max) | slope 512-4096 (mean [95% CI]) |
|---|---|---|---|---|---|---|---|---|
| G | 31.932 | 33.714 | 34.259 | 34.399 | 34.435 | 34.443 | 1.078 (1.028-1.096) | 0.0025 [0.0024, 0.0025] |
| M | 1.784 | 1.907 | 1.945 | 1.955 | 1.957 | 1.958 | 1.097 (1.027-1.137) | 0.0031 [0.0029, 0.0033] |
| G (maxabs) | 41.165 | 43.411 | 44.107 | 44.284 | 44.329 | 44.339 | 1.077 (1.024-1.096) | 0.0024 [0.0024, 0.0025] |
| M (maxabs) | 2.360 | 2.521 | 2.570 | 2.583 | 2.587 | 2.587 | 1.095 (1.027-1.135) | 0.0031 [0.0029, 0.0033] |
| Meps (main) | 1.800 | 1.899 | 1.929 | 1.937 | 1.939 | 1.940 | 1.077 (1.025-1.108) | 0.0025 [0.0022, 0.0027] |

Local slopes of M (seed means): 0.0953, 0.0280, 0.0074, 0.0019, 0.0005
Seeds whose maximum of M lies on the edge, by N: 5, 1, 0, 0, 0, 0

### point mid

| quantity | N = 128 | N = 256 | N = 512 | N = 1024 | N = 2048 | N = 4096 | ratio 2048/128 (mean, min-max) | slope 512-4096 (mean [95% CI]) |
|---|---|---|---|---|---|---|---|---|
| G | 47.805 | 54.328 | 56.599 | 57.199 | 57.357 | 57.397 | 1.203 (1.064-1.268) | 0.0064 [0.0059, 0.0069] |
| M | 15.667 | 21.078 | 28.560 | 38.310 | 51.405 | 69.082 | 3.305 (2.566-4.467) | 0.4247 [0.4122, 0.4371] |
| G (maxabs) | 61.589 | 69.974 | 72.864 | 73.636 | 73.838 | 73.889 | 1.201 (1.063-1.268) | 0.0064 [0.0059, 0.0069] |
| M (maxabs) | 18.085 | 24.306 | 32.936 | 44.161 | 59.247 | 79.614 | 3.303 (2.561-4.466) | 0.4246 [0.4122, 0.4371] |
| Meps (main) | 11.651 | 14.105 | 15.369 | 15.741 | 15.841 | 15.867 | 1.365 (1.126-1.462) | 0.0146 [0.0135, 0.0157] |

Local slopes of M (seed means): 0.4301, 0.4375, 0.4237, 0.4239, 0.4267
Seeds whose maximum of M lies on the edge, by N: 20, 15, 13, 12, 10, 10

### point high

| quantity | N = 128 | N = 256 | N = 512 | N = 1024 | N = 2048 | N = 4096 | ratio 2048/128 (mean, min-max) | slope 512-4096 (mean [95% CI]) |
|---|---|---|---|---|---|---|---|---|
| G | 59.060 | 73.070 | 78.156 | 79.801 | 80.230 | 80.339 | 1.364 (1.134-1.539) | 0.0127 [0.0122, 0.0132] |
| M | 42.363 | 65.485 | 99.886 | 151.709 | 230.884 | 352.201 | 5.473 (4.732-6.853) | 0.6055 [0.5924, 0.6187] |
| G (maxabs) | 76.072 | 94.111 | 100.617 | 102.733 | 103.283 | 103.423 | 1.362 (1.133-1.538) | 0.0126 [0.0122, 0.0131] |
| M (maxabs) | 46.587 | 72.019 | 109.848 | 166.807 | 253.844 | 387.205 | 5.471 (4.726-6.852) | 0.6055 [0.5923, 0.6186] |
| Meps (main) | 27.874 | 36.036 | 42.036 | 44.414 | 45.091 | 45.271 | 1.629 (1.325-1.975) | 0.0339 [0.0311, 0.0368] |
| Meps (L50_e0.05) | 41.014 | 60.684 | 81.913 | 107.155 | 132.681 | 147.748 | 3.263 (2.521-4.241) | 0.2861 [0.2563, 0.3160] |
| Meps (L100_e0.4) | 33.934 | 45.184 | 56.152 | 63.324 | 65.997 | 66.726 | 1.968 (1.549-2.638) | 0.0798 [0.0712, 0.0883] |

Local slopes of M (seed means): 0.6270, 0.6108, 0.6022, 0.6052, 0.6092
Seeds whose maximum of M lies on the edge, by N: 20, 20, 19, 19, 18, 18

## Worked example (point 'high': f = 7, s = 0.30, gamma = 2.6; D = 1.2 mm)

### main: L = 50 mm, e_min = 0.4 mm

eps = 0.3529, sigma_eps = 1.9681, G* = 88.227. Band width 2 eps L / G_4096 over seeds: 0.4000-0.5494 mm. Actual span of the relief at the largest N: 1.0175-1.1088 mm. Bound on the slope of the smoothed relief: grid 2.084 (64.4 deg), continuous 2.216 (65.7 deg). Shape error at the largest N: 0.1342 mm (bound 0.4020 mm).

| N | grid spacing (mm) | T_gamma: angle (deg), mean (min-max) | T_gamma_eps: angle | s F: angle |
|---|---|---|---|---|
| 128 | 0.3906 | 59.3 (53.9-62.8) | 48.0 (43.5-53.7) | 35.3 (30.4-38.8) |
| 256 | 0.1953 | 69.0 (64.1-71.5) | 55.1 (49.5-58.0) | 41.2 (34.7-43.5) |
| 512 | 0.0977 | 75.9 (72.9-77.4) | 59.1 (53.6-62.1) | 43.1 (37.1-45.9) |
| 1024 | 0.0488 | 80.6 (78.7-81.7) | 60.5 (55.0-63.6) | 43.7 (37.4-46.4) |
| 2048 | 0.0244 | 83.8 (82.6-84.7) | 60.8 (55.1-64.0) | 43.8 (37.6-46.6) |
| 4096 | 0.0122 | 85.9 (85.1-86.6) | 60.9 (55.2-64.1) | 43.9 (37.6-46.6) |

### L50_e0.05: L = 50 mm, e_min = 0.05 mm

eps = 0.0441, sigma_eps = 6.8292, G* = 88.227. Band width 2 eps L / G_4096 over seeds: 0.0500-0.0687 mm. Actual span of the relief at the largest N: 1.0175-1.1088 mm. Bound on the slope of the smoothed relief: grid 7.230 (82.1 deg), continuous 7.689 (82.6 deg). Shape error at the largest N: 0.0617 mm (bound 0.1806 mm).

| N | grid spacing (mm) | T_gamma: angle (deg), mean (min-max) | T_gamma_eps: angle | s F: angle |
|---|---|---|---|---|
| 128 | 0.3906 | 59.3 (53.9-62.8) | 58.5 (52.8-61.4) | 35.3 (30.4-38.8) |
| 256 | 0.1953 | 69.0 (64.1-71.5) | 67.4 (62.7-70.7) | 41.2 (34.7-43.5) |
| 512 | 0.0977 | 75.9 (72.9-77.4) | 72.9 (70.0-75.7) | 43.1 (37.1-45.9) |
| 1024 | 0.0488 | 80.6 (78.7-81.7) | 76.8 (74.7-78.9) | 43.7 (37.4-46.4) |
| 2048 | 0.0244 | 83.8 (82.6-84.7) | 79.3 (76.9-81.0) | 43.8 (37.6-46.6) |
| 4096 | 0.0122 | 85.9 (85.1-86.6) | 80.3 (77.8-81.6) | 43.9 (37.6-46.6) |

### L100_e0.4: L = 100 mm, e_min = 0.4 mm

eps = 0.1765, sigma_eps = 2.9357, G* = 88.227. Band width 2 eps L / G_4096 over seeds: 0.4000-0.5494 mm. Actual span of the relief at the largest N: 1.0175-1.1088 mm. Bound on the slope of the smoothed relief: grid 1.554 (57.2 deg), continuous 1.653 (58.8 deg). Shape error at the largest N: 0.1046 mm (bound 0.3079 mm).

| N | grid spacing (mm) | T_gamma: angle (deg), mean (min-max) | T_gamma_eps: angle | s F: angle |
|---|---|---|---|---|
| 128 | 0.7812 | 40.2 (34.5-44.2) | 34.1 (28.3-39.2) | 19.5 (16.3-21.9) |
| 256 | 0.3906 | 52.5 (45.9-56.2) | 42.0 (36.6-46.3) | 23.7 (19.1-25.4) |
| 512 | 0.1953 | 63.3 (58.4-65.9) | 48.2 (42.4-50.9) | 25.1 (20.7-27.3) |
| 1024 | 0.0977 | 71.6 (68.3-73.8) | 51.6 (45.1-55.1) | 25.6 (20.9-27.7) |
| 2048 | 0.0488 | 77.7 (75.4-79.6) | 52.7 (46.1-56.5) | 25.7 (21.0-27.9) |
| 4096 | 0.0244 | 81.9 (80.3-83.3) | 53.0 (46.2-56.8) | 25.7 (21.1-27.9) |


## Conclusions by prediction (written after the run)

This section was written by hand after the run and after the generated results were committed unedited (59c213e). It does not change any criterion. The record of the run says "dirty: True": at the start of the run the file `src/atact/lexicon.py`, which this script does not import, was untracked; it was committed (94a5730) while the run was going. The script, condition file and library files read by the run have the SHA-256 of commits 4dba646 and c43c855.

Summary: P-G1, P-G2, P-G3, P-G4 and P-G6 hold in every item; P-G5 holds for the main eps and not for the two sensitivity values.

**P-G1 (holds).** From N = 128 to 2048 the maximum gradient of H grows by 3.31 (mean over seeds; 2.57-4.47) at gamma = 1.75 and by 5.47 (4.73-6.85) at gamma = 2.6, against 16^(1 - 1/gamma) = 3.28 and 5.51.

**P-G2 (holds).** The slope of ln M on ln N over N 512-4096 is 0.425 [0.412, 0.437] at gamma = 1.75 and 0.606 [0.592, 0.619] at gamma = 2.6, against 1 - 1/gamma = 0.429 and 0.615. The local slopes stay between 0.42 and 0.44 and between 0.60 and 0.63 from N = 128 on. The maxabs normalisation gives the same slopes to the third decimal.

**P-G3 (holds).** At gamma = 0.9 the ratio is at most 1.14 and the slope over N 512-4096 is 0.003; the field itself (G) changes by the same amount (ratio 1.08), so the change at small N comes from the central difference of the field, not from T_gamma.

**P-G4 (holds).** The largest ratio of Meps to s sigma_eps G over all seeds, N and eps is 0.9994.

**P-G5 (holds for the main eps only).** With the main eps (0.353) the mean maximum gradient of the smoothed height changes by 1.9% between N = 1024 and 4096, while that of H grows by 2.32. With eps = 0.044 (L = 50 mm, e_min = 0.05 mm) it still grows by 1.38, and with eps = 0.176 (L = 100 mm, e_min = 0.4 mm) by 1.054, just above the 5% of the criterion. The smoothed slope stops changing only once the grid resolves the band of width about 2 eps / G: at the smallest eps the band (0.05-0.07 mm) spans one grid spacing at N = 1024 and four to six at N = 4096. As written in the conditions, the main eps makes this prediction hold almost by construction.

**P-G6 (holds).** The shape error is at most 0.35 times the bound eps^(1/gamma) in every item (for example 0.224 against 0.670 at the point 'high' with the main eps).

**Worked example.** With L = 50 mm, D = 1.2 mm and e_min = 0.4 mm, the rule for eps gives eps = 0.353, not a small number: the highest octave of the field (56 cycles per 50 mm) has its half period at the scale of the nozzle, so the band that T_{gamma,eps} smooths is a large part of the surface and the linear reading of the band width is only indicative. On the common scale the steepest slope of the unsmoothed relief at the corner (V, A) = (-1, 1) rises with the grid from 59 degrees (N = 128, grid spacing 0.39 mm) to 86 degrees (N = 4096); the smoothed relief stays at 61 degrees from N = 1024 on, below the continuous bound of 66 degrees, and the field without T_gamma (s F) at 44 degrees. The smoothing changes the height by at most 0.13 mm on a relief that spans 1.02-1.11 mm (under the ampsum normalisation the span stays below D). On a tile of 100 mm the same nozzle gives eps = 0.176 and a smoothed slope of 53 degrees.

**Observed beside the predictions (not tested).** The grid point of the largest gradient of H lies on the edge of the domain, where numpy.gradient uses a one-sided difference over one spacing instead of a central difference over two, in 18-20 of the 20 seeds at every N at the point 'high' and in 10-20 at the point 'mid'; for the smoothed height this becomes rare as N grows (at most 2 of 20 at N = 4096). The location of the maximum of F itself was not recorded. The growth exponent is unaffected (the local slopes agree with 1 - 1/gamma), but the level of M at a given N depends on the difference scheme at the edge.
