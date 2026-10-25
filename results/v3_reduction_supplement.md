# Supplementary exploration of validation 3: reduction methods

Conditions: `experiments/conditions/v3_reduction_supplement.json` (SHA-256 `7f2f6108fae7862686a38f366212ac7478b8b8d39ca2045060be6f920d2d9b2a`). Data and their check: `experiments/conditions/validation3_public.json` (SHA-256 `17d233cbb87c8d9aaef9392de9304c6aa09a4c9d4b4258e1fcb1d15fd46800db`). Specification SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`. numpy 2.5.4, scipy 1.18.1, Python 3.13.12. Run started 2026-10-25T14:19:10+00:00 and finished 2026-10-25T14:21:41+00:00 (Darwin arm64, 10 logical CPUs).

**Status: exploratory.** Designed after the results of validation 3 had been seen; not blind; no predictions. Its results are for the supplement and are not used as evidence for the claims of the main text.

## Summary (written by the author after the run; exploratory)

This section is not produced by `--report`. The exploration has no predictions; the statements below describe the tables.

- The counts of flips of validation 3 do not depend on the reduction method in the direction that matters: hf_ratio_px has 126, 133 and 143 flips under decimate_fourier, mirror and subsample, and hf_ratio_phys has fewer under each (61, 84, 71). centroid_amp reverses a rougher and a smoother measurement 32, 29 and 25 times; hf_ratio_px and hf_ratio_phys reverse none.
- Without a boundary jump and with nearly linear normals (mirror, heights x 1e-3), hf_ratio_phys decreases from full to quarter for 35 of 38 measurements (mean -0.110): the content term is never positive (25 negative) and the term of differences on the coarse grid is negative for 35. In this regime the change is explained by the loss of the content above the coarse Nyquist frequency and by the attenuation of the central differences near the coarse Nyquist frequency, both of which lower the ratio.
- With the measured slopes, mirror gives 26 decreasing, 9 increasing and 3 non-monotone measurements; the increases occur on the steepest crops and disappear in the small-slope control, which attributes them to the nonlinearity of the normal map.
- Under decimate_fourier the content term is positive for 22 measurements (8 under mirror, none under mirror with small slopes). The periodic ideal low-pass of a non-periodic crop adds oscillations near the boundary; most of the increases of hf_ratio_phys reported in validation 3 come from this.
- The sampling term (normals of a band-limited height taken on the coarse grid) is small (mean absolute value at most 0.009).
- centroid_band_power is constant over the levels only under decimate_fourier (validation 3, P-V3 over full and half); under mirror and subsample it increases for 36 and 38 measurements.

## Reading of the conditions

- Exploratory: designed after the results of validation 3 had been seen; not blind; no predictions; for the supplement only.
- mirror: even extension of the P x P crop to 2P x 2P, ideal low-pass keeping the bins whose components lie in [-n, n) of that frame (the same physical band as [-n/2, n/2) on the P x P frame), sampled at every (P/n)-th pixel of the first quadrant. The full level is the crop itself for every reduction.
- Decomposition of the change of hf_ratio_phys_float from full to level n: content = s1 - s0 (heights band-limited to level n, normals on the grid P), sampling = s2 - s1 (the normals of s1 taken at every (P/n)-th pixel), differences = s3 - s2 (normals computed from the reduced heights on the grid n). For the subsample reduction there is no band-limit, so it is not decomposed.

## Direction of the change with coarsening (38 measurements)

| reduction | descriptor | increasing | decreasing | non-monotone | mean abs(quarter - full) | V2 flips (main) | V3 flips (main) |
|---|---|---|---|---|---|---|---|
| decimate_fourier | hf_ratio_px | 35 | 0 | 3 | 0.2404 | 126 | 0 |
| decimate_fourier | hf_ratio_phys | 13 | 11 | 14 | 0.06597 | 61 | 0 |
| decimate_fourier | hf_ratio_phys_float | 12 | 13 | 13 | 0.066 | 61 | 0 |
| decimate_fourier | centroid_amp | 0 | 38 | 0 | 70.21 | 100 | 32 |
| decimate_fourier | centroid_band_power | 0 | 12 | 26 | 0.001633 | 0 | 0 |
| mirror | hf_ratio_px | 34 | 0 | 4 | 0.233 | 133 | 0 |
| mirror | hf_ratio_phys | 9 | 26 | 3 | 0.09126 | 84 | 0 |
| mirror | hf_ratio_phys_float | 8 | 28 | 2 | 0.09129 | 84 | 0 |
| mirror | centroid_amp | 0 | 38 | 0 | 69.22 | 96 | 29 |
| mirror | centroid_band_power | 36 | 0 | 2 | 0.133 | 0 | 0 |
| subsample | hf_ratio_px | 36 | 0 | 2 | 0.228 | 143 | 0 |
| subsample | hf_ratio_phys | 9 | 26 | 3 | 0.07552 | 71 | 0 |
| subsample | hf_ratio_phys_float | 7 | 29 | 2 | 0.07483 | 71 | 0 |
| subsample | centroid_amp | 0 | 38 | 0 | 67.32 | 72 | 25 |
| subsample | centroid_band_power | 38 | 0 | 0 | 1.589 | 15 | 12 |

## Decomposition of the change of hf_ratio_phys_float (means over the 38 measurements)

Mean of the absolute value, mean, and numbers of measurements with the term above 0.005 or below -0.005.

| band-limit / level | term | mean abs | mean | > 0.005 | < -0.005 |
|---|---|---|---|---|---|
| decimate_fourier/half | total | 0.03658 | +0.0049 | 20 | 12 |
| decimate_fourier/half | content | 0.04199 | +0.0354 | 20 | 7 |
| decimate_fourier/half | sampling | 0.0001874 | +0.0001 | 0 | 0 |
| decimate_fourier/half | differences | 0.04669 | -0.0307 | 7 | 26 |
| decimate_fourier/half/small_slope | total | 0.06691 | +0.0328 | 17 | 12 |
| decimate_fourier/half/small_slope | content | 0.1179 | +0.1169 | 22 | 2 |
| decimate_fourier/half/small_slope | sampling | 0.0001786 | -0.0001 | 0 | 0 |
| decimate_fourier/half/small_slope | differences | 0.08395 | -0.0839 | 0 | 29 |
| decimate_fourier/quarter | total | 0.066 | +0.0013 | 20 | 16 |
| decimate_fourier/quarter | content | 0.06044 | +0.0323 | 22 | 12 |
| decimate_fourier/quarter | sampling | 0.008919 | -0.0082 | 2 | 19 |
| decimate_fourier/quarter | differences | 0.04945 | -0.0228 | 7 | 29 |
| decimate_fourier/quarter/small_slope | total | 0.07496 | +0.0068 | 13 | 21 |
| decimate_fourier/quarter/small_slope | content | 0.1046 | +0.0867 | 17 | 14 |
| decimate_fourier/quarter/small_slope | sampling | 0.00246 | -0.0025 | 0 | 9 |
| decimate_fourier/quarter/small_slope | differences | 0.07746 | -0.0775 | 0 | 35 |
| mirror/half | total | 0.04224 | -0.0227 | 7 | 20 |
| mirror/half | content | 0.01153 | -0.0054 | 6 | 13 |
| mirror/half | sampling | 0.0002677 | +0.0000 | 0 | 0 |
| mirror/half | differences | 0.033 | -0.0174 | 6 | 20 |
| mirror/half/small_slope | total | 0.05789 | -0.0579 | 0 | 28 |
| mirror/half/small_slope | content | 0.01765 | -0.0176 | 0 | 19 |
| mirror/half/small_slope | sampling | 0.0002353 | -0.0001 | 0 | 0 |
| mirror/half/small_slope | differences | 0.04015 | -0.0401 | 0 | 26 |
| mirror/quarter | total | 0.09129 | -0.0440 | 8 | 29 |
| mirror/quarter | content | 0.04601 | -0.0238 | 8 | 20 |
| mirror/quarter | sampling | 0.001222 | +0.0009 | 3 | 0 |
| mirror/quarter | differences | 0.04752 | -0.0212 | 7 | 29 |
| mirror/quarter/small_slope | total | 0.1102 | -0.1102 | 0 | 35 |
| mirror/quarter/small_slope | content | 0.06264 | -0.0626 | 0 | 25 |
| mirror/quarter/small_slope | sampling | 0.0005494 | +0.0001 | 1 | 0 |
| mirror/quarter/small_slope | differences | 0.04766 | -0.0477 | 0 | 35 |

## Values by measurement (hf_ratio_phys; full, half, quarter)

| measurement | surface | RMS slope | boundary jump / RMS height | decimate_fourier | mirror | subsample |
|---|---|---|---|---|---|---|
| b15_scaraggi/0-new_b15_profilometertxt-squeezed.nc | smooth | 0.02379 | 1.156 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 |
| b15_scaraggi/1-new_b15_afm_20umtxt-squeezed.nc | smooth | 0.1955 | 0.5056 | 0.9594, 0.9665, 0.9581 | 0.9594, 0.9664, 0.9578 | 0.9594, 0.9677, 0.9648 |
| b15_scaraggi/2-new_b15_afm_5umtxt-squeezed.nc | smooth | 0.1597 | 1.064 | 0.9607, 0.9657, 0.9701 | 0.9607, 0.966, 0.9701 | 0.9607, 0.9658, 0.9701 |
| b55_persson/0-b-persson-b55-20x-scan-1vk4-squeezed.nc | smooth | 0.1809 | 1.444 | 0.9642, 1, 1 | 0.9642, 1, 1 | 0.9642, 0.9913, 1 |
| b55_persson/1-b-persson-b55-100x-scan-1vk4-squeezed.nc | smooth | 0.2989 | 1.558 | 0.9859, 0.9903, 1 | 0.9859, 0.9908, 1 | 0.9859, 0.9844, 0.9919 |
| t21_fang/00-t21_10-min-sonication-ipa_5xgwy-squeezed.nc | rough | 5.158 | 1.272 | 0.5864, 0.6389, 0.7803 | 0.5864, 0.6388, 0.7794 | 0.5864, 0.6249, 0.7245 |
| t21_fang/01-t21_10-min-sonication-ipa_5x_location2gwy-squeezed.nc | rough | 5.876 | 1.259 | 0.5796, 0.6312, 0.7603 | 0.5796, 0.6312, 0.7597 | 0.5796, 0.6177, 0.7079 |
| t21_fang/02-t21_10-min-sonication-ipa_10xgwy-squeezed.nc | rough | 3.25 | 1.635 | 0.6644, 0.7443, 0.8489 | 0.6644, 0.7445, 0.8492 | 0.6644, 0.7215, 0.8115 |
| t21_fang/03-t21_10-min-sonication-ipa_10x_location2gwy-squeezed.nc | rough | 2.499 | 1.384 | 0.7062, 0.7902, 0.8855 | 0.7062, 0.7902, 0.885 | 0.7062, 0.7668, 0.8538 |
| t21_fang/04-t21_10-min-sonication-ipa_20xgwy-squeezed.nc | rough | 1.077 | 1.431 | 0.8394, 0.8829, 0.9117 | 0.8394, 0.8828, 0.9102 | 0.8394, 0.8742, 0.9053 |
| t21_fang/05-t21_10-min-sonication-ipa_20x_location2gwy-squeezed.nc | rough | 1.057 | 1.46 | 0.8418, 0.886, 0.9157 | 0.8418, 0.8863, 0.9157 | 0.8418, 0.8781, 0.9101 |
| t21_fang/06-t21_10-min-sonication-ipa_50xgwy-squeezed.nc | rough | 0.6173 | 1.07 | 0.7514, 0.7077, 0.6667 | 0.7514, 0.6995, 0.6512 | 0.7514, 0.7079, 0.6594 |
| t21_fang/07-t21_10-min-sonication-ipa_50x_location2gwy-squeezed.nc | rough | 0.648 | 1.559 | 0.7845, 0.753, 0.725 | 0.7845, 0.7477, 0.7125 | 0.7845, 0.7533, 0.718 |
| t21_fang/08-t21_10-min-sonication-ipa_150xgwy-squeezed.nc | rough | 1.48 | 1.79 | 0.4801, 0.496, 0.4867 | 0.4801, 0.4373, 0.3991 | 0.4801, 0.4422, 0.4021 |
| t21_fang/09-t21_10-min-sonication-ipa_150x_location2gwy-squeezed.nc | rough | 0.8691 | 1.137 | 0.4986, 0.4776, 0.4455 | 0.4986, 0.4478, 0.4005 | 0.4986, 0.4533, 0.4059 |
| t22_skumar/00-t-22_-100-nm0_00102spm-squeezed.nc | rough | 3.202 | 2.089 | 0.6651, 0.5923, 0.4801 | 0.6651, 0.5752, 0.4058 | 0.6651, 0.6235, 0.5267 |
| t22_skumar/01-t-22_-250-nm0_00103spm-squeezed.nc | rough | 1.124 | 1.392 | 0.7122, 0.6289, 0.5537 | 0.7122, 0.6158, 0.5238 | 0.7122, 0.6448, 0.5602 |
| t22_skumar/02-t-22_-500-nm0_00104spm-squeezed.nc | rough | 0.5927 | 1.249 | 0.8019, 0.7858, 0.7685 | 0.8019, 0.7827, 0.7615 | 0.8019, 0.7862, 0.7662 |
| t22_skumar/03-t-22_-1um0_00105spm-squeezed.nc | rough | 0.4284 | 1.431 | 0.8943, 0.9014, 0.9067 | 0.8943, 0.9014, 0.9061 | 0.8943, 0.901, 0.9059 |
| t22_skumar/04-t-22_-5um0_00106spm-squeezed.nc | rough | 0.8295 | 4.07 | 0.8627, 0.8121, 0.6877 | 0.8627, 0.805, 0.6103 | 0.8627, 0.8092, 0.6509 |
| t22_skumar/05-t-22_-10um0_00107spm-squeezed.nc | rough | 1.493 | 1.497 | 0.3557, 0.3593, 0.3598 | 0.3557, 0.2527, 0.2035 | 0.3557, 0.2615, 0.2119 |
| t22_skumar/06-t-22_-25um0_00108spm-squeezed.nc | rough | 3.44 | 2.604 | 0.3533, 0.3894, 0.3909 | 0.3533, 0.3335, 0.3078 | 0.3533, 0.3293, 0.3147 |
| t22_skumar/07-t-22_-50um0_00110spm-squeezed.nc | rough | 2.175 | 1.828 | 0.3803, 0.4084, 0.3998 | 0.3803, 0.3512, 0.3082 | 0.3803, 0.3648, 0.3133 |
| t23_skumar/00-t-23_50000-nm0_00087spm-squeezed.nc | rough | 0.6259 | 1.667 | 0.8039, 0.7898, 0.7753 | 0.8039, 0.7862, 0.7684 | 0.8039, 0.7893, 0.7718 |
| t23_skumar/01-t-23_10000-nm0_00085spm-squeezed.nc | rough | 2.865 | 1.904 | 0.6337, 0.4611, 0.3747 | 0.6337, 0.4243, 0.2813 | 0.6337, 0.5124, 0.3781 |
| t23_skumar/02-t-23_25000-nm0_00086spm-squeezed.nc | rough | 1.056 | 1.662 | 0.6906, 0.6292, 0.5952 | 0.6906, 0.6173, 0.5702 | 0.6906, 0.6345, 0.5841 |
| t23_skumar/03-t-23_1um0_00088spm-squeezed.nc | rough | 0.6955 | 1.712 | 0.8478, 0.8437, 0.8299 | 0.8478, 0.8434, 0.8297 | 0.8478, 0.8438, 0.8306 |
| t23_skumar/04-t-23_100-um0_00090spm-squeezed.nc | rough | 1.498 | 2.793 | 0.5251, 0.5036, 0.5094 | 0.5251, 0.325, 0.2206 | 0.5251, 0.3495, 0.2468 |
| t23_skumar/05-t-23_250-um0_00092spm-squeezed.nc | rough | 1.801 | 2.264 | 0.3501, 0.4107, 0.4245 | 0.3501, 0.3218, 0.2978 | 0.3501, 0.3255, 0.2995 |
| t23_skumar/06-t-23_500-um0_00093spm-squeezed.nc | rough | 0.9754 | 1.591 | 0.4688, 0.5137, 0.5096 | 0.4688, 0.4493, 0.4201 | 0.4688, 0.4502, 0.4207 |
| t25_ckumar/0-t25-50x_2al3d-squeezed.nc | rough | 0.4751 | 1.657 | 0.4436, 0.4789, 0.4786 | 0.4436, 0.4397, 0.4281 | 0.4436, 0.442, 0.4301 |
| t25_ckumar/1-t25-50x_1al3d-squeezed.nc | rough | 0.3771 | 1.27 | 0.4499, 0.4745, 0.4694 | 0.4499, 0.4451, 0.4318 | 0.4499, 0.4476, 0.4338 |
| t25_ckumar/2-t25-50x_3al3d-squeezed.nc | rough | 0.4687 | 1.524 | 0.4272, 0.4611, 0.4588 | 0.4272, 0.4235, 0.4114 | 0.4272, 0.4256, 0.4133 |
| t26_ckumar/0-t26-50x_2al3d-squeezed.nc | rough | 0.5518 | 1.73 | 0.423, 0.4582, 0.4602 | 0.423, 0.4193, 0.408 | 0.423, 0.4215, 0.4101 |
| t26_ckumar/1-t26-50x_1al3d-squeezed.nc | rough | 0.4069 | 1.158 | 0.4043, 0.4285, 0.4245 | 0.4043, 0.4009, 0.39 | 0.4043, 0.403, 0.392 |
| t26_ckumar/2-t26-50x_3al3d-squeezed.nc | rough | 0.4937 | 1.592 | 0.4403, 0.4759, 0.4755 | 0.4403, 0.4358, 0.4234 | 0.4403, 0.4383, 0.4256 |
| t27_esawi/0-t27-scan-size-50um-squeezed.nc | rough | 0.7722 | 1.552 | 0.5857, 0.5985, 0.5769 | 0.5857, 0.5598, 0.5203 | 0.5857, 0.5622, 0.5248 |
| t28_esawi/0-t28-scan-size-50um-squeezed.nc | rough | 0.9033 | 1.774 | 0.5082, 0.5323, 0.5211 | 0.5082, 0.4843, 0.4491 | 0.5082, 0.4858, 0.4512 |

## Decomposition by measurement (quarter; content, sampling, differences)

| measurement | decimate_fourier | mirror | mirror, heights x 1e-3 |
|---|---|---|---|
| b15_scaraggi/0-new_b15_profilometertxt-squeezed.nc | -0.005, -0.000, -0.019 | -0.005, -0.000, -0.019 | -0.005, -0.000, -0.019 |
| b15_scaraggi/1-new_b15_afm_20umtxt-squeezed.nc | -0.011, +0.000, -0.011 | -0.011, +0.000, -0.011 | -0.009, -0.000, -0.013 |
| b15_scaraggi/2-new_b15_afm_5umtxt-squeezed.nc | +0.002, -0.000, -0.003 | +0.001, -0.000, -0.003 | -0.002, -0.000, -0.009 |
| b55_persson/0-b-persson-b55-20x-scan-1vk4-squeezed.nc | +0.001, +0.000, -0.010 | +0.002, +0.000, -0.012 | -0.005, +0.000, -0.012 |
| b55_persson/1-b-persson-b55-100x-scan-1vk4-squeezed.nc | +0.001, -0.000, +0.005 | +0.001, -0.000, +0.005 | -0.001, +0.000, -0.002 |
| t21_fang/00-t21_10-min-sonication-ipa_5xgwy-squeezed.nc | +0.066, -0.000, +0.128 | +0.065, -0.000, +0.128 | -0.001, -0.000, -0.003 |
| t21_fang/01-t21_10-min-sonication-ipa_5x_location2gwy-squeezed.nc | +0.063, -0.001, +0.118 | +0.063, -0.001, +0.117 | -0.001, -0.000, -0.003 |
| t21_fang/02-t21_10-min-sonication-ipa_10xgwy-squeezed.nc | +0.086, +0.000, +0.098 | +0.087, -0.000, +0.098 | -0.003, +0.000, -0.007 |
| t21_fang/03-t21_10-min-sonication-ipa_10x_location2gwy-squeezed.nc | +0.089, +0.000, +0.090 | +0.090, +0.000, +0.089 | -0.002, -0.000, -0.007 |
| t21_fang/04-t21_10-min-sonication-ipa_20xgwy-squeezed.nc | +0.042, +0.000, +0.030 | +0.043, -0.000, +0.028 | -0.008, +0.000, -0.014 |
| t21_fang/05-t21_10-min-sonication-ipa_20x_location2gwy-squeezed.nc | +0.043, -0.000, +0.031 | +0.044, -0.000, +0.029 | -0.007, +0.000, -0.012 |
| t21_fang/06-t21_10-min-sonication-ipa_50xgwy-squeezed.nc | -0.035, -0.002, -0.048 | -0.054, +0.000, -0.047 | -0.083, +0.000, -0.059 |
| t21_fang/07-t21_10-min-sonication-ipa_50x_location2gwy-squeezed.nc | -0.027, -0.000, -0.033 | -0.038, +0.000, -0.034 | -0.063, -0.000, -0.047 |
| t21_fang/08-t21_10-min-sonication-ipa_150xgwy-squeezed.nc | +0.072, -0.021, -0.045 | -0.039, +0.000, -0.043 | -0.069, +0.001, -0.058 |
| t21_fang/09-t21_10-min-sonication-ipa_150x_location2gwy-squeezed.nc | +0.018, -0.012, -0.058 | -0.048, -0.000, -0.050 | -0.079, -0.000, -0.063 |
| t22_skumar/00-t-22_-100-nm0_00102spm-squeezed.nc | -0.080, -0.006, -0.099 | -0.123, +0.001, -0.136 | -0.270, +0.000, -0.211 |
| t22_skumar/01-t-22_-250-nm0_00103spm-squeezed.nc | -0.080, -0.006, -0.073 | -0.110, +0.000, -0.078 | -0.189, +0.000, -0.099 |
| t22_skumar/02-t-22_-500-nm0_00104spm-squeezed.nc | -0.013, -0.000, -0.020 | -0.020, +0.000, -0.020 | -0.045, +0.000, -0.032 |
| t22_skumar/03-t-22_-1um0_00105spm-squeezed.nc | +0.005, +0.000, +0.008 | +0.006, +0.000, +0.006 | -0.005, +0.000, -0.012 |
| t22_skumar/04-t-22_-5um0_00106spm-squeezed.nc | -0.049, +0.006, -0.132 | -0.067, +0.007, -0.192 | -0.102, +0.007, -0.206 |
| t22_skumar/05-t-22_-10um0_00107spm-squeezed.nc | +0.091, -0.041, -0.046 | -0.116, +0.001, -0.037 | -0.119, +0.001, -0.041 |
| t22_skumar/06-t-22_-25um0_00108spm-squeezed.nc | +0.129, -0.009, -0.082 | +0.022, +0.020, -0.087 | -0.176, -0.001, -0.170 |
| t22_skumar/07-t-22_-50um0_00110spm-squeezed.nc | +0.099, -0.015, -0.064 | -0.011, +0.008, -0.069 | -0.159, -0.001, -0.114 |
| t23_skumar/00-t-23_50000-nm0_00087spm-squeezed.nc | -0.012, +0.000, -0.017 | -0.018, +0.000, -0.017 | -0.039, -0.000, -0.029 |
| t23_skumar/01-t-23_10000-nm0_00085spm-squeezed.nc | -0.161, -0.023, -0.075 | -0.266, -0.001, -0.085 | -0.414, -0.002, -0.111 |
| t23_skumar/02-t-23_25000-nm0_00086spm-squeezed.nc | -0.048, -0.004, -0.044 | -0.078, -0.000, -0.043 | -0.131, -0.000, -0.058 |
| t23_skumar/03-t-23_1um0_00088spm-squeezed.nc | -0.015, +0.005, -0.008 | -0.003, -0.000, -0.015 | -0.010, -0.000, -0.032 |
| t23_skumar/04-t-23_100-um0_00090spm-squeezed.nc | +0.080, -0.029, -0.066 | -0.233, -0.001, -0.070 | -0.235, -0.001, -0.073 |
| t23_skumar/05-t-23_250-um0_00092spm-squeezed.nc | +0.154, -0.032, -0.048 | -0.024, -0.001, -0.027 | -0.029, -0.001, -0.036 |
| t23_skumar/06-t-23_500-um0_00093spm-squeezed.nc | +0.105, -0.018, -0.046 | -0.015, -0.000, -0.034 | -0.020, -0.000, -0.039 |
| t25_ckumar/0-t25-50x_2al3d-squeezed.nc | +0.087, -0.015, -0.037 | -0.001, -0.000, -0.014 | -0.004, -0.000, -0.017 |
| t25_ckumar/1-t25-50x_1al3d-squeezed.nc | +0.068, -0.011, -0.038 | -0.002, -0.000, -0.016 | -0.003, -0.000, -0.020 |
| t25_ckumar/2-t25-50x_3al3d-squeezed.nc | +0.084, -0.015, -0.037 | -0.001, +0.000, -0.015 | -0.002, +0.000, -0.018 |
| t26_ckumar/0-t26-50x_2al3d-squeezed.nc | +0.088, -0.016, -0.035 | -0.001, -0.000, -0.014 | -0.003, -0.000, -0.019 |
| t26_ckumar/1-t26-50x_1al3d-squeezed.nc | +0.069, -0.011, -0.038 | -0.001, +0.000, -0.013 | -0.001, +0.000, -0.016 |
| t26_ckumar/2-t26-50x_3al3d-squeezed.nc | +0.090, -0.015, -0.039 | -0.001, -0.000, -0.016 | -0.006, -0.000, -0.026 |
| t27_esawi/0-t27-scan-size-50um-squeezed.nc | +0.052, -0.012, -0.049 | -0.021, +0.002, -0.046 | -0.055, +0.002, -0.057 |
| t28_esawi/0-t28-scan-size-50um-squeezed.nc | +0.077, -0.015, -0.050 | -0.019, +0.001, -0.041 | -0.026, +0.001, -0.049 |
