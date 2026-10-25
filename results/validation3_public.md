# Validation 3 on public measured data

Conditions: `experiments/conditions/validation3_public.json` (SHA-256 `17d233cbb87c8d9aaef9392de9304c6aa09a4c9d4b4258e1fcb1d15fd46800db`). Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`). numpy 2.5.4, scipy 1.18.1, Python 3.13.12. Run started 2026-10-25T12:55:47+00:00 and finished 2026-10-25T12:56:49+00:00 (Darwin arm64, 10 logical CPUs). The SHA-256 of all 38 Challenge files and 36 TactileDreamFusion files agreed with the conditions before any value was read.

Interpretation: robustness to resampling of one measurement on a fixed physical domain, not re-measurement with different instruments. No claim is made about the conclusions of other studies. Data sources and licences: Surface-Topography Challenge, Zenodo 10.5281/zenodo.15341939 (Pradhan et al., Tribology Letters 73, 110, 2025); CC0 at the record level (Zenodo metadata: license = cc-zero). The deposit's _README.md states that each container includes a licence file; among the containers used, only t21_fang contains one (LICENSE-cc0-1.0.txt, CC0 1.0 Universal). The record-level CC0 is relied on for the others. TactileDreamFusion (Gao et al., NeurIPS 2024), Hugging Face Ruihan28/TactileDreamFusion, revision 87c8b764bcb2ec1139de0c6435f45ac1d9f283d1; tactile_textures.zip SHA-256 e391a32d51d7eec1066e4e1e3639ccd55311b210b0526de001f1a6f5de8f4c3a; MIT (dataset card and the LICENSE file of the code repository).

## Reading of the conditions fixed before the run

- Challenge: heights are stored with dimensions (x, y) and are transposed to [y, x]. The pixel spacings along x and y (length attribute divided by the number of points) differ by at most 3.3e-4 in relative terms in the included measurements; the normal map uses their mean as the spacing of S2.8, and the side of the crop is L = P times that spacing. At the coarser levels the spacing is L/n.
- Challenge levels: the P x P crop after plane removal is level 'full'; 'half' and 'quarter' are made from it by decimate_fourier (primary) and by subsample (control). TDF levels are made from the normal map per component by decimate_normals (S5.4); the finest level is the input itself (patch with alpha dropped, central 1024 block of the tiled map) and is not re-encoded.
- TDF float variant: the decoded input normals n = rgb/255 * 2 - 1 are reduced per component by decimate_fourier in floating point and renormalised, without the uint8 re-encoding of the coarse levels (at the finest level it is the decoded input, which is itself uint8). It isolates the effect of the re-encoding, not of the input quantisation.
- V2 for TDF uses every pair of the 36 inputs (patches and tiled maps together, container = object), as the condition states every pair within a dataset; level pairs are the relative levels (finest, half, quarter). The split by input type is reported beside it. Kendall's tau is reported for V2 only; V3 restricts pairs, for which a tau over all measurements would not apply.
- centroid_band_power uses K = P/8. At the quarter level K equals n/2; the bin at -n/2 along an axis is kept by decimate_fourier and its partner at +n/2 is not, so the retained bins on the circle rho = n/2 are not exactly the same as at the finer levels; in addition the real part taken after the inverse DFT halves the unpaired boundary coefficient (noted before the computation, in relation to P-V3).
- Pairs from different containers (the main count of V2) include measurements of the same kind of specimen made by different groups with different instruments; the condition's 'not_done' excludes cross-instrument comparisons of the same specimen from the main analysis, while V2 counts all different-container pairs. V2 is followed as written; this overlap is noted, not resolved.
- Operational criteria (fixed in this script before the computation): 'increases (decreases) when the grid is coarsened' means strictly monotone over full, half, quarter for the measurement; 'the change of hf_ratio_phys is smaller' compares |quarter - full| per measurement; 'fewer flips' compares the main counts (pairs from different containers, all three pairs of levels); P-V3 'up to rounding' means a relative range over the three levels of at most 1e-9.

## Conclusions by prediction (written after the run)

This section was written by the author after reading the tables below; it is not produced by `--report`. The decisions follow the operational criteria fixed in the script before the run, also where they fail for reasons stated here; no criterion was changed after the run. Values in this section are read from the tables below (four significant figures).

- **P-V1 does not hold (0 of 2 items)**, although most measurements behave as predicted. hf_ratio_px increases strictly with coarsening for 35 of 38 Challenge measurements. Of the three exceptions, two are smooth measurements whose ratio is already 1 at the coarser levels (b15 profilometer: 1, 1, 1; b55 20x: 0.9642, 1, 1), so the strict criterion fails on ties at the upper end; one is a real exception (t23, 10000 nm: 0.6337, 0.6195, 0.7679). The change of hf_ratio_phys is smaller than that of hf_ratio_px for 31 of 38 measurements. Of the seven exceptions, three are smooth measurements where both ratios reach 1 at the same level and the changes are equal; four have a larger change for phys (b15 AFM 5 um: 0.0094 against 0.0064; t22 -100 nm: 0.185 against 0.133; t22 -5 um: 0.175 against 0.081; t23 10000 nm: 0.259 against 0.134). More generally, hf_ratio_phys is not constant over the levels for the rough measurements: from full to quarter it decreases monotonically for 11 measurements, increases monotonically for 13 and is non-monotone for 14, with changes of 0.004-0.259 for the rough measurements. The cutoff fixed in physical wavelength reduces the change relative to the pixel-fixed cutoff for most measurements but does not make the ratio grid-independent on these measured surfaces.
- **P-V2 holds** (2 of 2): hf_ratio_px has 126 flips (pairs from different containers) and hf_ratio_phys has 61. On TactileDreamFusion the counts are 118 and 0.
- **P-V3 holds in 1 of 2 items.** Over full and half the relative range of centroid_band_power is 4.0e-16. Over the three levels it is 2.1e-3, above the 1e-9 tolerance. This is the boundary effect noted before the computation: at the quarter level K = n/2, and the bins on the circle rho = n/2 are not retained in the same way as at the finer levels. As stated in the conditions, this is a check of the tools; the failure concerns the choice K = P/8 at the coarsest level, not the descriptor at K < n/2. The descriptor still has no flips under decimate_fourier.
- **P-V4 holds** (38 of 38 measurements decrease with coarsening). Not predicted: centroid_amp has 100 flips, and 32 of them reverse the order of a rougher and a smoother measurement (V3), whereas hf_ratio_px and hf_ratio_phys reverse no such pair.
- **P-V5 holds** (18 of 18 patches and 18 of 18 tiled maps increase with coarsening). Not predicted: hf_ratio_px has 12 flips among patches, 34 among tiled maps and 118 over all 36 inputs; hf_ratio_phys has none. The float variant gives nearly the same counts (123 against 118), so the flips do not arise from the uint8 re-encoding of the coarse levels.
- Control by subsampling: the counts are of the same order (hf_ratio_px 143, hf_ratio_phys 71, centroid_amp 72), and centroid_band_power, which is constant under decimate_fourier, has 15 flips under subsampling.

## Predictions

### P-V1: 0 of 2 items hold

Prediction: P-V1 (Proposition 8, part 3): hf_ratio_px increases when the grid is coarsened, for every measurement. The change of hf_ratio_phys is smaller than that of hf_ratio_px.

| part | measurements | of | not | holds |
|---|---|---|---|---|
| hf_ratio_px increases when coarsened | 35 | 38 | b15_scaraggi/0-new_b15_profilometertxt-squeezed.nc, b55_persson/0-b-persson-b55-20x-scan-1vk4-squeezed.nc, t23_skumar/01-t-23_10000-nm0_00085spm-squeezed.nc | no |
| |change| phys < |change| px | 31 | 38 | - | no |

### P-V2: 2 of 2 items hold

Prediction: P-V2: hf_ratio_px shows at least one flip (definition of V2). hf_ratio_phys shows fewer flips than hf_ratio_px.

| part | flips_px | flips_phys | holds |
|---|---|---|---|
| hf_ratio_px has at least one flip | 126 | - | yes |
| hf_ratio_phys has fewer flips | 126 | 61 | yes |

### P-V3: 1 of 2 items hold

Prediction: P-V3: centroid_band_power is grid-independent for the decimate_fourier version up to rounding (the retained bins are the same). This is a check of the tools, not a finding.

| part | max_rel_range | holds |
|---|---|---|
| centroid_band_power grid-independent (three levels) | 0.002094 | no |
| same, full and half only (K < n/2) | 3.952e-16 | yes |

### P-V4: 2 of 2 items hold

Prediction: P-V4: centroid_amp (raw) decreases when the grid is coarsened. Whether flips occur is not predicted.

| part | measurements | of | flips_main | holds |
|---|---|---|---|---|
| centroid_amp decreases when coarsened | 38 | 38 | - | yes |
| flips of centroid_amp (not predicted) | - | - | 100 | yes |

### P-V5: 5 of 5 items hold

Prediction: P-V5 (tdf): hf_ratio_px increases when the grid is coarsened. Whether flips occur is not predicted (the inputs were already high-pass filtered).

| part | inputs | of | flips_main | holds |
|---|---|---|---|---|
| tdf patch: hf_ratio_px increases when coarsened | 18 | 18 | - | yes |
| tdf patch: flips of hf_ratio_px (not predicted) | - | - | 12 | yes |
| tdf tiled: hf_ratio_px increases when coarsened | 18 | 18 | - | yes |
| tdf tiled: flips of hf_ratio_px (not predicted) | - | - | 34 | yes |
| tdf all 36 inputs: flips of hf_ratio_px (not predicted) | - | - | 118 | yes |

## V2 and V3: flips (Challenge)

Main count: pairs from different containers; pairs from the same container are reported separately and not counted as independent. Threshold: relative difference above 0.05 at both levels.

| method / descriptor | flips (main) | flips (same container) | V3 flips rougher vs smoother (main) | tau full-half, full-quarter, half-quarter |
|---|---|---|---|---|
| decimate_fourier/hf_ratio_px | 126 | 14 | 0 | 0.695, 0.559, 0.782 |
| decimate_fourier/hf_ratio_phys | 61 | 19 | 0 | 0.863, 0.764, 0.893 |
| decimate_fourier/hf_ratio_px_float | 126 | 14 | 0 | 0.698, 0.550, 0.772 |
| decimate_fourier/centroid_amp | 100 | 26 | 32 | 0.795, 0.636, 0.835 |
| decimate_fourier/centroid_amp_hann | 221 | 31 | 27 | 0.795, 0.508, 0.696 |
| decimate_fourier/centroid_band_power | 0 | 0 | 0 | 1.000, 1.000, 1.000 |
| decimate_fourier/sq | 0 | 0 | 0 | 1.000, 1.000, 1.000 |
| subsample/hf_ratio_px | 143 | 15 | 0 | 0.701, 0.545, 0.798 |
| subsample/hf_ratio_phys | 71 | 16 | 0 | 0.903, 0.763, 0.854 |
| subsample/hf_ratio_px_float | 142 | 15 | 0 | 0.701, 0.548, 0.807 |
| subsample/centroid_amp | 72 | 11 | 25 | 0.835, 0.707, 0.872 |
| subsample/centroid_amp_hann | 161 | 16 | 29 | 0.832, 0.619, 0.775 |
| subsample/centroid_band_power | 15 | 2 | 12 | 0.986, 0.954, 0.969 |
| subsample/sq | 0 | 0 | 0 | 0.997, 0.997, 1.000 |

## V2: flips (TactileDreamFusion)

| input / descriptor | flips (main) | flips (same object) | tau |
|---|---|---|---|
| all/hf_ratio_px | 118 | 0 | 0.610, 0.359, 0.705 |
| all/hf_ratio_phys | 0 | 0 | 0.978, 0.933, 0.956 |
| all/hf_ratio_px_float | 123 | 0 | 0.616, 0.343, 0.683 |
| all/hf_ratio_phys_float | 2 | 0 | 0.978, 0.937, 0.959 |
| patch/hf_ratio_px | 12 | 0 | 0.725, 0.281, 0.529 |
| patch/hf_ratio_phys | 0 | 0 | 1.000, 0.974, 0.974 |
| patch/hf_ratio_px_float | 12 | 0 | 0.752, 0.242, 0.464 |
| patch/hf_ratio_phys_float | 2 | 0 | 1.000, 0.974, 0.974 |
| tiled/hf_ratio_px | 34 | 0 | 0.529, 0.438, 0.882 |
| tiled/hf_ratio_phys | 0 | 0 | 0.922, 0.869, 0.948 |
| tiled/hf_ratio_px_float | 35 | 0 | 0.516, 0.425, 0.882 |
| tiled/hf_ratio_phys_float | 0 | 0 | 0.935, 0.882, 0.948 |

## V1 and V4: values by level (Challenge)

Values at full, half and quarter (decimate_fourier), and the relative difference of subsample from decimate_fourier at half and quarter (V4).

| measurement | surface | P | hf_ratio_px | hf_ratio_phys | centroid_amp | centroid_band_power | V4 hf_ratio_px | V4 centroid_amp |
|---|---|---|---|---|---|---|---|---|
| b15_scaraggi/0-new_b15_profilometertxt-squeezed.nc | smooth | 512 | 1, 1, 1 | 1, 1, 1 | 118.8, 71.36, 39.38 | 13.08, 13.08, 13.06 | 0, 0 | 0.04848, 0.04111 |
| b15_scaraggi/1-new_b15_afm_20umtxt-squeezed.nc | smooth | 512 | 0.9594, 0.9834, 0.9937 | 0.9594, 0.9665, 0.9581 | 126, 58.68, 30.65 | 14.87, 14.87, 14.87 | 0.00569, 0.007866 | 0.1268, 0.1358 |
| b15_scaraggi/2-new_b15_afm_5umtxt-squeezed.nc | smooth | 512 | 0.9607, 0.9619, 0.9671 | 0.9607, 0.9657, 0.9701 | 75.64, 49.45, 33.29 | 18.88, 18.88, 18.88 | 0.003049, 0.002939 | 0.04565, 0.04945 |
| b55_persson/0-b-persson-b55-20x-scan-1vk4-squeezed.nc | smooth | 512 | 0.9642, 1, 1 | 0.9642, 1, 1 | 176, 92.16, 41.89 | 14.1, 14.1, 14.1 | 0.01554, 0 | 0.06095, 0.1212 |
| b55_persson/1-b-persson-b55-100x-scan-1vk4-squeezed.nc | smooth | 512 | 0.9859, 0.9962, 1 | 0.9859, 0.9903, 1 | 166.3, 81.73, 42.97 | 32.34, 32.34, 32.34 | 0.005299, 0 | 0.09056, 0.09858 |
| t21_fang/00-t21_10-min-sonication-ipa_5xgwy-squeezed.nc | rough | 512 | 0.5864, 0.6398, 0.7858 | 0.5864, 0.6389, 0.7803 | 142.3, 75.73, 42.18 | 31.56, 31.56, 31.56 | 0.02191, 0.07342 | 0.07191, 0.07436 |
| t21_fang/01-t21_10-min-sonication-ipa_5x_location2gwy-squeezed.nc | rough | 512 | 0.5796, 0.6323, 0.7663 | 0.5796, 0.6312, 0.7603 | 144.1, 74.75, 40.95 | 29.23, 29.23, 29.23 | 0.02156, 0.07113 | 0.08071, 0.09136 |
| t21_fang/02-t21_10-min-sonication-ipa_10xgwy-squeezed.nc | rough | 512 | 0.6644, 0.7481, 0.8605 | 0.6644, 0.7443, 0.8489 | 143.9, 70.38, 38.08 | 23.45, 23.45, 23.44 | 0.03115, 0.04664 | 0.0964, 0.09988 |
| t21_fang/03-t21_10-min-sonication-ipa_10x_location2gwy-squeezed.nc | rough | 512 | 0.7062, 0.7939, 0.8963 | 0.7062, 0.7902, 0.8855 | 142.9, 69.53, 37.96 | 23.59, 23.59, 23.59 | 0.03024, 0.03859 | 0.1004, 0.1056 |
| t21_fang/04-t21_10-min-sonication-ipa_20xgwy-squeezed.nc | rough | 512 | 0.8394, 0.8947, 0.936 | 0.8394, 0.8829, 0.9117 | 124.1, 57, 30.97 | 15.33, 15.33, 15.33 | 0.01097, 0.009521 | 0.1175, 0.1187 |
| t21_fang/05-t21_10-min-sonication-ipa_20x_location2gwy-squeezed.nc | rough | 512 | 0.8418, 0.8969, 0.9375 | 0.8418, 0.886, 0.9157 | 124.1, 57.3, 31.19 | 15.75, 15.75, 15.75 | 0.01005, 0.007854 | 0.116, 0.1221 |
| t21_fang/06-t21_10-min-sonication-ipa_50xgwy-squeezed.nc | rough | 512 | 0.7514, 0.8746, 0.9295 | 0.7514, 0.7077, 0.6667 | 87.27, 38.42, 18.9 | 4.992, 4.992, 4.991 | 0.001668, 0.0006755 | 0.1311, 0.157 |
| t21_fang/07-t21_10-min-sonication-ipa_50x_location2gwy-squeezed.nc | rough | 512 | 0.7845, 0.8951, 0.9322 | 0.7845, 0.753, 0.725 | 87.01, 38.91, 19.67 | 6.238, 6.238, 6.238 | 5.101e-05, 0.00124 | 0.1227, 0.1442 |
| t21_fang/08-t21_10-min-sonication-ipa_150xgwy-squeezed.nc | rough | 512 | 0.4801, 0.6898, 0.8338 | 0.4801, 0.496, 0.4867 | 66.08, 31.21, 16.44 | 3.03, 3.03, 3.029 | 0.03381, 0.004461 | 0.1042, 0.1201 |
| t21_fang/09-t21_10-min-sonication-ipa_150x_location2gwy-squeezed.nc | rough | 512 | 0.4986, 0.7041, 0.8681 | 0.4986, 0.4776, 0.4455 | 66.89, 31.13, 15.97 | 2.757, 2.757, 2.757 | 0.01442, 0.000641 | 0.1053, 0.1326 |
| t22_skumar/00-t-22_-100-nm0_00102spm-squeezed.nc | rough | 512 | 0.6651, 0.6895, 0.798 | 0.6651, 0.5923, 0.4801 | 108.1, 46.46, 21.58 | 3.272, 3.272, 3.271 | 0.01693, 0.002776 | 0.1515, 0.2121 |
| t22_skumar/01-t-22_-250-nm0_00103spm-squeezed.nc | rough | 512 | 0.7122, 0.8123, 0.9005 | 0.7122, 0.6289, 0.5537 | 97.21, 40.97, 19.43 | 3.925, 3.925, 3.924 | 0.001946, 0.002099 | 0.155, 0.188 |
| t22_skumar/02-t-22_-500-nm0_00104spm-squeezed.nc | rough | 512 | 0.8019, 0.8965, 0.927 | 0.8019, 0.7858, 0.7685 | 81.71, 37.56, 19.77 | 6.743, 6.743, 6.743 | 0.001271, 0.0002502 | 0.1191, 0.1347 |
| t22_skumar/03-t-22_-1um0_00105spm-squeezed.nc | rough | 512 | 0.8943, 0.9267, 0.9451 | 0.8943, 0.9014, 0.9067 | 75.11, 39.05, 24.68 | 11.9, 11.9, 11.9 | 0.0005065, 0.0008621 | 0.08644, 0.06047 |
| t22_skumar/04-t-22_-5um0_00106spm-squeezed.nc | rough | 512 | 0.8627, 0.8867, 0.9441 | 0.8627, 0.8121, 0.6877 | 87.97, 49.01, 26.73 | 7.313, 7.313, 7.312 | 0.0005539, 0.002624 | 0.0715, 0.1087 |
| t22_skumar/05-t-22_-10um0_00107spm-squeezed.nc | rough | 512 | 0.3557, 0.5173, 0.7449 | 0.3557, 0.3593, 0.3598 | 64.81, 32.5, 16.38 | 2.389, 2.389, 2.388 | 0.1309, 0.05038 | 0.09621, 0.1348 |
| t22_skumar/06-t-22_-25um0_00108spm-squeezed.nc | rough | 512 | 0.3533, 0.5428, 0.7432 | 0.3533, 0.3894, 0.3909 | 81.18, 40.33, 21.74 | 3.905, 3.905, 3.903 | 0.07632, 0.02086 | 0.08957, 0.1132 |
| t22_skumar/07-t-22_-50um0_00110spm-squeezed.nc | rough | 512 | 0.3803, 0.5854, 0.7794 | 0.3803, 0.4084, 0.3998 | 70.32, 34.49, 18.49 | 3.14, 3.14, 3.139 | 0.04494, 0.01525 | 0.1018, 0.1186 |
| t23_skumar/00-t-23_50000-nm0_00087spm-squeezed.nc | rough | 512 | 0.8039, 0.8993, 0.9264 | 0.8039, 0.7898, 0.7753 | 80.56, 38.1, 20.1 | 7.018, 7.018, 7.017 | 0.0003238, 0.001413 | 0.117, 0.1306 |
| t23_skumar/01-t-23_10000-nm0_00085spm-squeezed.nc | rough | 512 | 0.6337, 0.6195, 0.7679 | 0.6337, 0.4611, 0.3747 | 102.9, 42.29, 18.22 | 3.078, 3.078, 3.075 | 0.04171, 0.003213 | 0.1783, 0.2659 |
| t23_skumar/02-t-23_25000-nm0_00086spm-squeezed.nc | rough | 512 | 0.6906, 0.8159, 0.8913 | 0.6906, 0.6292, 0.5952 | 90.27, 39.52, 19.66 | 4.929, 4.929, 4.928 | 0.001242, 0.0005144 | 0.1476, 0.1579 |
| t23_skumar/03-t-23_1um0_00088spm-squeezed.nc | rough | 512 | 0.8478, 0.8813, 0.9144 | 0.8478, 0.8437, 0.8299 | 66.79, 34.52, 21.33 | 3.667, 3.667, 3.666 | 0.0009278, 0.001909 | 0.08507, 0.06507 |
| t23_skumar/04-t-23_100-um0_00090spm-squeezed.nc | rough | 512 | 0.5251, 0.6185, 0.7704 | 0.5251, 0.5036, 0.5094 | 74.54, 37.03, 18.39 | 4.05, 4.05, 4.042 | 0.1946, 0.1762 | 0.1014, 0.1438 |
| t23_skumar/05-t-23_250-um0_00092spm-squeezed.nc | rough | 512 | 0.3501, 0.6239, 0.8124 | 0.3501, 0.4107, 0.4245 | 60.11, 28.83, 16.32 | 3.551, 3.551, 3.548 | 0.07752, 0.02571 | 0.1039, 0.0975 |
| t23_skumar/06-t-23_500-um0_00093spm-squeezed.nc | rough | 512 | 0.4688, 0.7126, 0.8604 | 0.4688, 0.5137, 0.5096 | 51.1, 26.5, 15.44 | 3.037, 3.037, 3.034 | 0.0439, 0.0194 | 0.08313, 0.08669 |
| t25_ckumar/0-t25-50x_2al3d-squeezed.nc | rough | 1024 | 0.4436, 0.7598, 0.9286 | 0.4436, 0.4789, 0.4786 | 101.1, 50.43, 28.33 | 5.985, 5.985, 5.985 | 0.01987, 0.001989 | 0.1186, 0.1128 |
| t25_ckumar/1-t25-50x_1al3d-squeezed.nc | rough | 1024 | 0.4499, 0.7562, 0.9282 | 0.4499, 0.4745, 0.4694 | 85.59, 44.03, 25.8 | 5.863, 5.863, 5.863 | 0.01508, 0.001462 | 0.1233, 0.1049 |
| t25_ckumar/2-t25-50x_3al3d-squeezed.nc | rough | 1024 | 0.4272, 0.7449, 0.9224 | 0.4272, 0.4611, 0.4588 | 78.93, 42.53, 25.52 | 5.819, 5.819, 5.819 | 0.01934, 0.001546 | 0.1127, 0.09579 |
| t26_ckumar/0-t26-50x_2al3d-squeezed.nc | rough | 1024 | 0.423, 0.7437, 0.9139 | 0.423, 0.4582, 0.4602 | 104.4, 52.09, 29.48 | 5.867, 5.867, 5.867 | 0.02027, 0.002402 | 0.1112, 0.1118 |
| t26_ckumar/1-t26-50x_1al3d-squeezed.nc | rough | 1024 | 0.4043, 0.7296, 0.9143 | 0.4043, 0.4285, 0.4245 | 81.19, 41.62, 24.72 | 5.425, 5.425, 5.425 | 0.01405, 0.00168 | 0.1147, 0.1026 |
| t26_ckumar/2-t26-50x_3al3d-squeezed.nc | rough | 1024 | 0.4403, 0.7546, 0.9169 | 0.4403, 0.4759, 0.4755 | 84.71, 46.64, 27.94 | 5.855, 5.855, 5.855 | 0.02024, 0.003616 | 0.14, 0.1203 |
| t27_esawi/0-t27-scan-size-50um-squeezed.nc | rough | 512 | 0.5857, 0.797, 0.9083 | 0.5857, 0.5985, 0.5769 | 61.65, 30.06, 16.91 | 3.549, 3.549, 3.548 | 0.01675, 0.003307 | 0.1089, 0.1094 |
| t28_esawi/0-t28-scan-size-50um-squeezed.nc | rough | 512 | 0.5082, 0.7635, 0.8998 | 0.5082, 0.5323, 0.5211 | 61.04, 30.75, 17.39 | 3.636, 3.636, 3.636 | 0.02602, 0.003449 | 0.09164, 0.09931 |

## V1: values by level (TactileDreamFusion)

| input | hf_ratio_px | hf_ratio_phys | hf_ratio_px_float |
|---|---|---|---|
| ClothBag/normal_patch.png | 0.8945, 0.9113, 0.9309 | 0.8945, 0.8945, 0.8987 | 0.8944, 0.9118, 0.9314 |
| CorkMat/normal_patch.png | 0.9212, 0.9433, 0.9731 | 0.9212, 0.9207, 0.9123 | 0.9212, 0.9432, 0.9706 |
| Corn/normal_patch.png | 0.6779, 0.9061, 0.953 | 0.6779, 0.6772, 0.6746 | 0.6781, 0.9067, 0.9533 |
| CuttingBoard/normal_patch.png | 0.9169, 0.9374, 0.9618 | 0.9169, 0.9169, 0.9104 | 0.9174, 0.9372, 0.9669 |
| Football/normal_patch.png | 0.9549, 0.9632, 0.981 | 0.9549, 0.9554, 0.9552 | 0.9557, 0.965, 0.9746 |
| GoldGoat/normal_patch.png | 0.7915, 0.8579, 0.9372 | 0.7915, 0.79, 0.7872 | 0.7916, 0.8588, 0.9386 |
| GreenSweater/normal_patch.png | 0.9215, 0.9363, 0.9509 | 0.9215, 0.9216, 0.9236 | 0.9217, 0.936, 0.9517 |
| MetalFrame/normal_patch.png | 0.9011, 0.9178, 0.9286 | 0.9011, 0.9025, 0.9075 | 0.9018, 0.9182, 0.9286 |
| Orange/normal_patch.png | 0.9285, 0.9657, 0.9974 | 0.9285, 0.9289, 0.9281 | 0.9303, 0.9712, 0.9854 |
| OrangeGlove/normal_patch.png | 0.5741, 0.8785, 0.966 | 0.5741, 0.5684, 0.5495 | 0.5753, 0.8791, 0.9664 |
| PinkCloth/normal_patch.png | 0.9346, 0.9605, 0.9839 | 0.9346, 0.9348, 0.9325 | 0.9358, 0.9605, 0.9757 |
| Potato/normal_patch.png | 0.8349, 0.9136, 0.9919 | 0.8349, 0.8348, 0.8171 | 0.8356, 0.9092, 0.9803 |
| PurpleGlove/normal_patch.png | 0.899, 0.9096, 0.9217 | 0.899, 0.8997, 0.9029 | 0.8993, 0.9097, 0.9218 |
| RedCloth1/normal_patch.png | 0.9059, 0.9328, 0.9505 | 0.9059, 0.9058, 0.9064 | 0.9063, 0.9325, 0.9499 |
| Strawberry/normal_patch.png | 0.8442, 0.9513, 0.9804 | 0.8442, 0.8438, 0.8377 | 0.8435, 0.9463, 0.9838 |
| TableTennisHandle/normal_patch.png | 0.6117, 0.7634, 0.939 | 0.6117, 0.6057, 0.5239 | 0.6094, 0.7661, 0.9578 |
| avocado/normal_patch.png | 0.7701, 0.8644, 0.8909 | 0.7701, 0.7695, 0.7687 | 0.77, 0.865, 0.8913 |
| cantaloupe/normal_patch.png | 0.812, 0.8904, 0.9388 | 0.812, 0.8109, 0.8078 | 0.8118, 0.8911, 0.9393 |
| ClothBag/tiled_normal_map.png | 0.8351, 0.8403, 0.8458 | 0.8351, 0.8355, 0.84 | 0.8344, 0.8404, 0.8459 |
| CorkMat/tiled_normal_map.png | 0.804, 0.8099, 0.8279 | 0.804, 0.8058, 0.8221 | 0.8031, 0.8099, 0.8279 |
| Corn/tiled_normal_map.png | 0.6444, 0.9277, 0.9454 | 0.6444, 0.6381, 0.6282 | 0.6445, 0.9279, 0.9437 |
| CuttingBoard/tiled_normal_map.png | 0.8169, 0.8222, 0.8382 | 0.8169, 0.8188, 0.8333 | 0.816, 0.8222, 0.8382 |
| Football/tiled_normal_map.png | 0.9021, 0.9124, 0.9181 | 0.9021, 0.9034, 0.9064 | 0.9025, 0.9128, 0.9182 |
| GoldGoat/tiled_normal_map.png | 0.7932, 0.8123, 0.8241 | 0.7932, 0.7935, 0.7986 | 0.7923, 0.8124, 0.8241 |
| GreenSweater/tiled_normal_map.png | 0.7576, 0.7644, 0.7726 | 0.7576, 0.758, 0.7639 | 0.7566, 0.7644, 0.7726 |
| MetalFrame/tiled_normal_map.png | 0.8832, 0.8996, 0.9056 | 0.8832, 0.8838, 0.8881 | 0.8832, 0.9, 0.906 |
| Orange/tiled_normal_map.png | 0.8602, 0.8802, 0.8859 | 0.8602, 0.8605, 0.863 | 0.8595, 0.8802, 0.886 |
| OrangeGlove/tiled_normal_map.png | 0.531, 0.845, 0.9371 | 0.531, 0.52, 0.5013 | 0.5317, 0.8455, 0.9378 |
| PinkCloth/tiled_normal_map.png | 0.8802, 0.8858, 0.8921 | 0.8802, 0.8806, 0.8848 | 0.8798, 0.8858, 0.892 |
| Potato/tiled_normal_map.png | 0.8946, 0.9622, 0.9864 | 0.8946, 0.8906, 0.8851 | 0.8947, 0.9617, 0.9773 |
| PurpleGlove/tiled_normal_map.png | 0.7641, 0.7686, 0.7776 | 0.7641, 0.7653, 0.7735 | 0.7634, 0.7687, 0.7777 |
| RedCloth1/tiled_normal_map.png | 0.8062, 0.8365, 0.8441 | 0.8062, 0.8068, 0.8116 | 0.8057, 0.8365, 0.8441 |
| Strawberry/tiled_normal_map.png | 0.8068, 0.9193, 0.9365 | 0.8068, 0.8031, 0.7971 | 0.8066, 0.9194, 0.9365 |
| TableTennisHandle/tiled_normal_map.png | 0.948, 0.9913, 0.9982 | 0.948, 0.9476, 0.9454 | 0.9489, 0.9849, 0.9913 |
| avocado/tiled_normal_map.png | 0.8075, 0.869, 0.8817 | 0.8075, 0.8065, 0.8066 | 0.8069, 0.8693, 0.882 |
| cantaloupe/tiled_normal_map.png | 0.8063, 0.8796, 0.8889 | 0.8063, 0.805, 0.8042 | 0.8057, 0.8797, 0.889 |
