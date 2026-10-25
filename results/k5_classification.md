# K5: Table 1

Conditions: `experiments/conditions/k5_classification.json` (SHA-256 `09a914161be116f44ab83f32277e5c48db3f304370f0f2bad59e5009b152d5e6`). Predictions: `experiments/conditions/k5_table1_predictions.json` (SHA-256 `6cf0f96992bd4acab004d03f66b0566c355f84f14eb8bf869709d9a33db7693b`). Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`). Script SHA-256 `f27dde51be04fa2b980c63c1d966984a9007a48e8c534d82c61dd859cd69bfed`. numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, Python 3.13.12. Run started 2026-10-25T17:21:43+00:00 and finished 2026-10-25T18:54:26+00:00 (Darwin arm64, 10 logical CPUs).

## Reading of the conditions fixed before the run

- Groups: group 0 is the first centre listed for the condition and group 1 the second (i_V: V = -0.5 / 0.5; i_A: A = -0.5 / 0.5; ii_s, ii_s_gamma and corners: (1, -1) / (-1, 1)). iii_null and check_same_seed use the (f, s, gamma) of corner (1, -1) for both groups.
- Jitter (decision recorded before any computation): the surface of group g with seed s draws u = default_rng([s, g, 1]).uniform(-1, 1, 2) and its jitter is w u. (The decision before any computation named default_rng([s, g]); an independent check found before the power runs that SeedSequence pads the entropy with zeros, so [s, 0] gives the same draws as default_rng(s), and group-0 jitter would have equalled the first two phase draws of the field rescaled. The third word 1 makes the stream distinct for both groups.) i_V adds w u[0] to V only and i_A adds w u[1] to A only; ii_s, ii_s_gamma and corners add both and clip to [-1, 1]. The same u is used for the three values of w and for every condition, N, processing and representation, so these differ only in the quantity named.
- Surface: F by S1.1-S1.4 (maxabs, four octaves, no warp; atact.field.procedural_field_separable), H = s T_gamma(F) (S2.2). Representation H uses H; minmax uses (H - min H) / (max H - min H). Processing raw computes the descriptors on the representation minus its mean; hann on the windowed array of S3.1. sq is S2.5, centroid_amp S2.3, centroid_band_power S2.4 with power weighting and 0 < rho <= 32.
- Cross-validation: pair i is relabelled perm[i] with perm = default_rng(0).permutation(n), and sklearn GroupKFold with five splits forms the folds from these labels. Both surfaces of a pair are always in the same fold. The fold assignment depends only on the pair indices, so it is the same under every label permutation.
- svm: StandardScaler and SVC(kernel='linear', C=1) fitted on the training folds. threshold: on the training folds, the cut between two adjacent distinct values (or below or above all values) and the direction that maximise training accuracy; ties are broken by the first maximum in the order (direction 'greater is group 1' before 'smaller is group 1', smaller cut first). Accuracy is the fraction of the 2n surfaces predicted correctly out of fold.
- Bootstrap: the pairs are resampled with replacement (indices from default_rng(1), the same 2000 replicates for every row with the same n); the out-of-fold predictions are kept fixed and the accuracy of each replicate is the fraction of correct predictions among the resampled pairs. Percentile intervals use numpy.percentile (linear). TOST: 'at chance' if the 90% interval of accuracy - 0.5 lies strictly inside (-0.05, 0.05).
- Permutation: 999 replicates; in each, the labels of each pair are swapped with probability 1/2 (draws from default_rng(2)), and the whole pipeline (fold assignment, standardisation, classifier fit, threshold choice) is run again. p = (1 + number of permuted accuracies >= observed) / 1000.
- tost_chance and perm_p are given for each classifier (svm for every descriptor set, threshold for the single-descriptor sets).
- Power (decisions recorded before any computation): (a) run r of iii_null uses seeds 100000 + 1000 r + i (group 0) and 300000 + 1000 r + i (group 1), r = 0..199; for a candidate n the first n pairs are used. Equivalence must be declared in at least 80% of runs in every column of iii_null (both N, processings, representations, descriptor sets and classifiers). (b) run r of corners (w = 0.5, N = 128, raw, H, svm, {sq, centroid_amp}) uses seed 500000 + 1000 r + i for both groups, r = 0..49; the mean half-width of the 95% interval must be at most 0.05. If no candidate satisfies both, the largest candidate (480) is used and this is stated in the results.
- Large-sample level (decision recorded before any computation): set A uses seeds 2000000 + j and set B 3000000 + j for both groups (iii_null group 1: 4000000 + j and 5000000 + j), j = 0..4999. One descriptor: the best threshold on set A, with its accuracy on set A (the level) and, beside it, on set B. Two descriptors: the svm of the experiment trained on set A and evaluated on set B. For iii_null the in-sample threshold accuracy exceeds 0.5 by selection, which is reported and not corrected.
- Mechanism check: descriptors of i_V and i_A at the jitter-free centres for seeds 1000-1099, by group (mean, standard deviation, minimum and maximum).
- Clipping: for ii_s, ii_s_gamma and corners, the fraction of surfaces with at least one coordinate clipped to the boundary is reported for each w.
- P-K5-4 and P-K5-5 compare accuracies for exact equality. Descriptor values that agree only to rounding (relative 1e-13) can still give a different svm accuracy: the weight of the soft-margin SVM is unique but its intercept need not be, and a rounding-level change of which support vectors lie on the margin moves the intercept chosen by the solver (in a smoke run, one fold had the same weight and intercepts -0.104 and -0.035, with 24 and 25 support vectors; a solver tolerance of 1e-12 instead of 1e-3 gave the same accuracies). The accuracies of every unequal cell are listed beside the count. This was noticed in a smoke run before the experiment and the criterion was not changed.
- Limits stated before the run (from the independent checks): the bootstrap keeps the out-of-fold predictions fixed, so its interval does not include the variation from refitting the classifier, and the power runs (a) measure how often equivalence is declared when the true accuracy is 0.5, not the error rate at the margins 0.45 and 0.55. The power rule bounds each column of iii_null separately, while P-K5-3 is a joint claim over all columns; the joint rate observed in the power runs is reported beside it. The large-sample level of one descriptor is the in-sample accuracy of the best threshold, which is biased upwards by selection (not only for iii_null), and the level of two descriptors is the accuracy of a linear SVM; both are estimates for these classifier families and can lie below the Bayes accuracy when the best decision region is not a half-line or half-plane. The held-out accuracy of the threshold on set B is reported beside the level.
- Correction of a basis stated before the run (the criterion is unchanged): the basis of P-K5-9 says that sq differs between the groups through the sampling of the maximum. For integer f coprime to N (f = 3 and 7 at N = 128 and 512) the map i -> f i mod N permutes the grid, so the sampled arrays of the two surfaces of a pair are permutations of each other and raw sq is identical; under ii_s_gamma sq differs only because the jittered f is not an integer (edge of the domain), and under hann also through the window.
- Diagnostics added before the run beside unchanged criteria: for P-K5-2 the number of violations in which raw C has the same accuracy at both N (so that no smaller change is possible), and for P-K5-8 the number of violations outside the S rows of ii_s_gamma. Row tags name the classifier ('svm') where a criterion is evaluated on svm only; for pairwise predictions (P-K5-1, -2, -4, -6, -7, -9, -11) the tag is attached to the row predicted to be smaller, equal or derived, not to both rows. perm_p counts permuted accuracies >= observed - 1e-12, a guard against floating-point noise; accuracies are multiples of 1/(2n), so it does not change the count.
- Smoke runs (--smoke) use seeds from 900000 upwards with 20 pairs, fewer replicates and fewer runs; they test the script only and their values are not used for any decision.

per_class_n = 480 (results/k5_power.json). Frame: results/k5_table1_frame.json (SHA-256 `4c234a1e0deb0e72e4d6442fcf94ccb9fce42cbfe47495d4caa35e7d6942a89f`). Set names: S = [sq], C = [centroid_amp], B = [centroid_band_power], SC = [sq, centroid_amp].

## Predictions

### P-K5-1: 0 of 2 items hold

Criterion: For ii_s, ii_s_gamma and corners, in every cell with the same w, N and processing, the accuracy of S on minmax is at most the accuracy of S on H; evaluated separately for svm and threshold.

| part | counts | holds |
|---|---|---|
| S on minmax <= S on H (svm) | cells 36; violations 4 | no |
| S on minmax <= S on H (threshold) | cells 36; violations 4 | no |

Violating cells: ['ii_s_gamma', '0.3', '128', 'raw']; ['ii_s_gamma', '0.3', '128', 'hann']; ['ii_s_gamma', '0.5', '128', 'hann']; ['ii_s_gamma', '0.5', '512', 'raw']; ['ii_s_gamma', '0.1', '128', 'hann']; ['ii_s_gamma', '0.5', '128', 'raw']; ['ii_s_gamma', '0.5', '512', 'raw']; ['ii_s_gamma', '0.5', '512', 'hann']

### P-K5-2: 5 of 6 items hold

Criterion: For i_A, raw centroid_amp (set C), the accuracy at N = 512 is at least that at N = 128 for every w and representation (svm and threshold separately). The absolute difference between N = 512 and N = 128 is smaller for B (raw) and for C (hann) than for C (raw), compared within the same w, representation and classifier.

| part | counts | holds |
|---|---|---|
| i_A raw C: N 512 >= N 128 (svm) | cells 6; violations 0 | yes |
| i_A raw C: N 512 >= N 128 (threshold) | cells 6; violations 2 | no |
| i_A: |change with N| of raw B < that of raw C (svm) | cells 6; violations 0; violations_with_raw_C_unchanged 0 | yes |
| i_A: |change with N| of hann C < that of raw C (svm) | cells 6; violations 0; violations_with_raw_C_unchanged 0 | yes |
| i_A: |change with N| of raw B < that of raw C (threshold) | cells 6; violations 0; violations_with_raw_C_unchanged 0 | yes |
| i_A: |change with N| of hann C < that of raw C (threshold) | cells 6; violations 0; violations_with_raw_C_unchanged 0 | yes |

Violating cells: ['0.1', 'H']; ['0.1', 'minmax']

### P-K5-3: 1 of 2 items hold

Criterion: iii_null is 'at chance' by the TOST in every column. check_same_seed has accuracy exactly 0.5 in every column.

| part | counts | holds |
|---|---|---|
| iii_null at chance by the TOST in every column | columns 56; violations 11 | no |
| check_same_seed accuracy exactly 0.5 | columns 56; violations 0 | yes |

Violating cells: iii_null|128|raw|H|centroid_amp|threshold; iii_null|128|raw|H|centroid_band_power|threshold; iii_null|128|raw|minmax|centroid_amp|threshold; iii_null|128|raw|minmax|centroid_band_power|threshold; iii_null|128|hann|H|sq|svm; iii_null|128|hann|H|centroid_band_power|threshold; iii_null|128|hann|minmax|centroid_band_power|threshold; iii_null|512|raw|H|sq+centroid_amp|svm; iii_null|512|hann|H|centroid_band_power|threshold; iii_null|512|hann|H|sq+centroid_amp|svm; iii_null|512|hann|minmax|centroid_band_power|threshold

### P-K5-4: 2 of 2 items hold

Criterion: The largest relative difference between centroid_amp (and centroid_band_power) on minmax and on H, over all surfaces, is below 1e-9. The accuracies of C and of B on minmax equal those on H in every cell (both classifiers); the number of unequal cells is reported.

| part | counts | holds |
|---|---|---|
| centroids on minmax equal those on H (largest relative difference) | value 2.987e-13 | yes |
| accuracies of C and B equal on minmax and H | unequal_cells 0 | yes |

### P-K5-5: 3 of 3 items hold

Criterion: The largest relative difference between ii_s and corners of every descriptor on minmax, and of the two centroids on H, is below 1e-9. The accuracies of ii_s and corners are equal in every minmax row and in the C and B rows on H (both classifiers); the number of unequal cells is reported.

| part | counts | holds |
|---|---|---|
| ii_s and corners: descriptors on minmax equal (largest relative difference) | value 2.476e-14 | yes |
| ii_s and corners: centroids on H equal (largest relative difference) | value 1.528e-14 | yes |
| ii_s and corners: accuracies equal in the predicted rows | unequal_cells 0 | yes |

### P-K5-6: 3 of 3 items hold

Criterion: For i_V, raw, H, every N and w: sq of the group-0 surface exceeds sq of the group-1 surface in every pair. For i_V, the accuracy of S on minmax is at most that of S on H in every cell with the same w, N and processing (svm and threshold separately).

| part | counts | holds |
|---|---|---|
| i_V raw H: sq of group 0 > sq of group 1 in every pair (all N and w) | pairs 2880; violations 0 | yes |
| i_V: S on minmax <= S on H (svm) | cells 12; violations 0 | yes |
| i_V: S on minmax <= S on H (threshold) | cells 12; violations 0 | yes |

### P-K5-7: 0 of 1 items hold

Criterion: In every cell of the non-null conditions, the svm accuracy of SC is at least the larger of the svm accuracies of S and C.

| part | counts | holds |
|---|---|---|
| svm: SC >= max(S, C) | cells 120; violations 7 | no |

Violating cells: i_V|0.1|512|raw|minmax SC 0.9990 < 1.0000; i_V|0.3|512|hann|minmax SC 0.9958 < 0.9969; i_V|0.5|128|hann|H SC 0.9781 < 0.9792; i_V|0.5|512|raw|H SC 0.9760 < 0.9792; i_V|0.5|512|hann|H SC 0.9760 < 0.9792; i_V|0.5|512|hann|minmax SC 0.9479 < 0.9510; i_A|0.3|128|hann|H SC 0.9958 < 0.9990

### P-K5-8: 0 of 1 items hold

Criterion: For every non-null condition and column, the svm accuracy is non-increasing in w: acc(w = 0.1) >= acc(w = 0.3) >= acc(w = 0.5).

| part | counts | holds |
|---|---|---|
| svm accuracy non-increasing in w | columns 160; violations 10; violations_outside_S_rows_of_ii_s_gamma 4 | no |

Violating cells: i_V|128|raw|H|B: 0.6854, 0.6865, 0.6802; i_V|128|raw|minmax|B: 0.6854, 0.6865, 0.6802; i_V|128|hann|H|B: 0.6802, 0.6813, 0.6771; i_V|128|hann|minmax|B: 0.6802, 0.6813, 0.6771; ii_s_gamma|128|raw|H|S: 0.5000, 0.4979, 0.5073; ii_s_gamma|128|raw|minmax|S: 0.4969, 0.5062, 0.5031; ii_s_gamma|128|hann|H|S: 0.5021, 0.4979, 0.5010; ii_s_gamma|128|hann|minmax|S: 0.4990, 0.5052, 0.5021; ii_s_gamma|512|raw|minmax|S: 0.4990, 0.5000, 0.5052; ii_s_gamma|512|hann|H|S: 0.5000, 0.5010, 0.5000

### P-K5-9: 1 of 1 items hold

Criterion: For raw H, the svm accuracy of S in ii_s_gamma is lower than that of S in i_V, i_A, ii_s and corners, in every column with the same w and N. No direction relative to chance is predicted for the S rows of ii_s_gamma.

| part | counts | holds |
|---|---|---|
| raw H: S of ii_s_gamma lower than S of the other non-null conditions | columns 6; violations 0 | yes |

### P-K5-10: 0 of 1 items hold

Criterion: svm accuracies within each cell: for i_A, ii_s and ii_s_gamma (both representations) and corners on minmax, acc(C) >= acc(S) and acc(B) >= acc(S). For i_V on H, acc(S) >= acc(C).

| part | counts | holds |
|---|---|---|
| order of single descriptors (svm) | cells 96; violations 3 | no |

Violating cells: ii_s|H|0.5|128|raw: S 1.0000 C 0.9979 B 1.0000; ii_s|minmax|0.5|128|raw: S 1.0000 C 0.9979 B 1.0000; corners|minmax|0.5|128|raw: S 1.0000 C 0.9979 B 1.0000

### P-K5-11: 2 of 2 items hold

Criterion: For i_V, raw C, the accuracy at N = 512 is at least that at N = 128 for every w and representation (svm and threshold separately).

| part | counts | holds |
|---|---|---|
| i_V raw C: N 512 >= N 128 (svm) | cells 6; violations 0 | yes |
| i_V raw C: N 512 >= N 128 (threshold) | cells 6; violations 0 | yes |

### P-K5-12: 0 of 1 items hold

Criterion: Above chance: in every row of the non-null conditions except the S rows of ii_s_gamma, the 95% pair-bootstrap interval of the svm accuracy lies above 0.5.

| part | counts | holds |
|---|---|---|
| 95% interval of the svm accuracy above 0.5 | rows 456; violations 12 | no |

Violating cells: ii_s_gamma_w0.1|512|raw|H|centroid_amp; ii_s_gamma_w0.1|512|raw|H|sq+centroid_amp; ii_s_gamma_w0.1|512|raw|minmax|centroid_amp; ii_s_gamma_w0.1|512|raw|minmax|sq+centroid_amp; ii_s_gamma_w0.3|512|raw|H|centroid_amp; ii_s_gamma_w0.3|512|raw|H|sq+centroid_amp; ii_s_gamma_w0.3|512|raw|minmax|centroid_amp; ii_s_gamma_w0.3|512|raw|minmax|sq+centroid_amp; ii_s_gamma_w0.5|512|raw|H|centroid_amp; ii_s_gamma_w0.5|512|raw|H|sq+centroid_amp; ii_s_gamma_w0.5|512|raw|minmax|centroid_amp; ii_s_gamma_w0.5|512|raw|minmax|sq+centroid_amp

## Conclusions by prediction (written after the run)

This section was written by hand after the run and after the generated results were committed unedited. It does not change any criterion. The judgements are those of the Predictions section above; the text states what the measured values show beside each prediction. Statements marked "supplementary" rest on checks that are not in the registered list of computations and are not used as the basis of any claim.

Summary: 4 of the 12 predictions hold in every part (P-K5-4, -5, -6, -11), 1 holds in its single part (P-K5-9), 2 hold in some parts (P-K5-2: 5 of 6; P-K5-3: 1 of 2), and 5 do not hold (P-K5-1, -7, -8, -10, -12).

**P-K5-1 (does not hold).** The order "S on minmax <= S on H" fails in 4 of 36 cells for each classifier. All violations are in the S rows of ii_s_gamma, whose accuracies lie between 0.497 and 0.507 in both representations, so the order is between two values at chance. For ii_s and corners the prediction holds in every cell. The prediction did not exclude cells in which both accuracies are at chance, and it is recorded as not holding.

**P-K5-2 (5 of 6 parts hold).** With svm, the accuracy of raw C for i_A at N = 512 is at least that at N = 128 in every cell. With the threshold, it fails at w = 0.1 in both representations (0.9833 at N = 128, 0.9823 at N = 512, one surface out of 960). The four parts on the size of the change with N (raw B and hann C smaller than raw C) hold for both classifiers, with no violation in which raw C was unchanged.

**P-K5-3 (1 of 2 parts hold).** check_same_seed has accuracy exactly 0.5 in all 56 columns. iii_null is not declared at chance in 11 of 56 columns. In all 11 the lower end of the 90% interval lies below 0.45; none exceeds 0.55. The accuracies of iii_null lie between 0.461 and 0.514 (mean 0.483 over the 56 columns). The power runs at per_class_n = 480, which did not meet the power rule (smallest per-column rate 0.73), predicted this: the per-column rates imply on average 12.3 columns not declared at chance, and all 56 columns were declared together in 8% of the 200 runs. The mean accuracy over runs in the power runs was 0.4996, so the shift below 0.5 here is one realisation on the low side. The permutation p values of iii_null (0.27 to 0.98) do not indicate accuracy above chance. The prediction does not hold, and the reason is the limited power at the sample size used, which was stated before the run.

**P-K5-4 (holds).** The centroids on minmax and on H agree to a relative difference of 3.0e-13, and the accuracies of C and B are equal in every cell for both classifiers. The svm discrepancy through the intercept, noted in the smoke run (Reading of the conditions), did not occur in the experiment.

**P-K5-5 (holds).** ii_s and corners agree on every descriptor on minmax (relative difference 2.5e-14) and on the centroids on H (1.5e-14), and their accuracies are equal in every predicted row.

**P-K5-6 (holds).** For i_V, raw, H, sq of group 0 exceeds sq of group 1 in all 2880 pairs, and S on minmax is at most S on H in every cell for both classifiers.

**P-K5-7 (does not hold).** The svm accuracy of SC is below the larger of S and C in 7 of 120 cells (6 of i_V, 1 of i_A). The largest shortfall is 0.0032 (three surfaces out of 960); in every violating cell the better single descriptor has accuracy 0.95 or higher.

**P-K5-8 (does not hold).** The svm accuracy is not non-increasing in w in 10 of 160 columns. Six are S rows of ii_s_gamma at chance. The other four are the B rows of i_V at N = 128, where the accuracy at w = 0.3 exceeds that at w = 0.1 by one surface out of 960 (0.0010).

**P-K5-9 (holds).** For raw H, the svm accuracy of S under ii_s_gamma is below that of the other non-null conditions in all 6 columns. The basis stated with the prediction was partly wrong (Reading of the conditions: for integer f coprime to N, raw sq of the two surfaces of a pair is identical). The prediction holding does not support that basis.

**P-K5-10 (does not hold).** The order of single descriptors fails in 3 of 96 cells: ii_s on H and on minmax and corners on minmax, at w = 0.5, N = 128, raw, where S and B have accuracy 1.0 and C has 0.9979 (two surfaces). The order for i_V on H (S >= C) holds.

**P-K5-11 (holds).** For i_V, raw C, the accuracy at N = 512 is at least that at N = 128 in every cell for both classifiers.

**P-K5-12 (does not hold).** The 95% interval of the svm accuracy lies above 0.5 in 444 of 456 rows. The 12 exceptions are the C and SC rows of ii_s_gamma at N = 512, raw, for every w and both representations (svm accuracy 0.506 to 0.519). In the same rows the threshold reaches 0.761 to 0.773, close to the large-sample levels of the frame (0.759 to 0.767, best threshold on set A). The large-sample level of these rows was taken from the threshold for both classifiers, so it does not predict the svm accuracy.

Supplementary (not in the registered list of computations): in ii_s_gamma at w = 0.1, N = 512, raw, H, centroid_amp of each group has a point mass at its minimum (9.05 for group 0 and 21.12 for group 1, also the medians) and a long upper tail (maxima 63.9 and 72.2). This matches the clipping fractions (0.758 of the surfaces have a clipped coordinate; their f is the integer at the corner). A linear SVM (C = 1) and a logistic regression fitted to all 960 surfaces of this cell have training accuracies of 0.519, while the best threshold lies between the two point masses. The hinge and logistic losses are pulled by the upper tail of group 0, and their cut does not separate the point masses. At N = 128 the tails are short (maxima 22.7 and 35.9) and the svm reaches 0.90 on all data. This is offered as a reading of the failure of P-K5-12, not as a tested mechanism.

## Table 1

| condition | w | N | proc | repr | set | level (large sample) | svm | 95% CI svm | threshold | 95% CI threshold | at chance (TOST) | perm p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| i_V | 0.1 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | raw | H | C | 0.9908 | 0.9854 | [0.9771, 0.9917] | 0.9854 | [0.9781, 0.9917] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | raw | H | B | 0.6860 | 0.6854 | [0.6635, 0.7073] | 0.6802 | [0.6583, 0.701] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.1 | 128 | raw | minmax | S | 0.8455 | 0.8490 | [0.8292, 0.8698] | 0.8531 | [0.8344, 0.874] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | raw | minmax | C | 0.9908 | 0.9854 | [0.9771, 0.9917] | 0.9854 | [0.9781, 0.9917] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | raw | minmax | B | 0.6860 | 0.6854 | [0.6635, 0.7073] | 0.6802 | [0.6583, 0.701] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | raw | minmax | SC | 0.9940 | 0.9927 | [0.9865, 0.9979] | - | - | svm no | svm 0.001 |
| i_V | 0.1 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | hann | H | C | 0.9833 | 0.9781 | [0.9688, 0.9865] | 0.976 | [0.9656, 0.9854] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | hann | H | B | 0.6840 | 0.6802 | [0.6583, 0.7021] | 0.6823 | [0.6625, 0.7031] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.1 | 128 | hann | minmax | S | 0.8454 | 0.8490 | [0.8292, 0.8698] | 0.8542 | [0.8344, 0.875] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | hann | minmax | C | 0.9833 | 0.9781 | [0.9688, 0.9865] | 0.976 | [0.9656, 0.9854] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | hann | minmax | B | 0.6840 | 0.6802 | [0.6583, 0.7021] | 0.6823 | [0.6625, 0.7031] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 128 | hann | minmax | SC | 0.9907 | 0.9896 | [0.9833, 0.9948] | - | - | svm no | svm 0.001 |
| i_V | 0.1 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | raw | H | C | 0.9999 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | raw | H | B | 0.6827 | 0.6854 | [0.6635, 0.7073] | 0.6792 | [0.6583, 0.7] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.1 | 512 | raw | minmax | S | 0.8458 | 0.8479 | [0.8281, 0.8688] | 0.851 | [0.8313, 0.8719] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | raw | minmax | C | 0.9999 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | raw | minmax | B | 0.6827 | 0.6854 | [0.6635, 0.7073] | 0.6792 | [0.6583, 0.7] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | raw | minmax | SC | 0.9999 | 0.9990 | [0.9969, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.1 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | hann | H | C | 0.9999 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | hann | H | B | 0.6807 | 0.6813 | [0.6594, 0.7021] | 0.6781 | [0.6573, 0.6979] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.1 | 512 | hann | minmax | S | 0.8458 | 0.8479 | [0.8281, 0.8688] | 0.851 | [0.8313, 0.8719] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | hann | minmax | C | 0.9999 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | hann | minmax | B | 0.6807 | 0.6813 | [0.6594, 0.7021] | 0.6781 | [0.6573, 0.6979] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.1 | 512 | hann | minmax | SC | 0.9999 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | raw | H | C | 0.9725 | 0.9688 | [0.9573, 0.9792] | 0.9667 | [0.9552, 0.9771] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | raw | H | B | 0.6835 | 0.6865 | [0.6646, 0.7083] | 0.6885 | [0.6677, 0.7115] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 128 | raw | minmax | S | 0.8366 | 0.8375 | [0.8167, 0.8583] | 0.8365 | [0.8156, 0.8573] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | raw | minmax | C | 0.9725 | 0.9688 | [0.9573, 0.9792] | 0.9667 | [0.9552, 0.9771] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | raw | minmax | B | 0.6835 | 0.6865 | [0.6646, 0.7083] | 0.6885 | [0.6677, 0.7115] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | raw | minmax | SC | 0.9786 | 0.9760 | [0.9656, 0.9854] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | hann | H | C | 0.9628 | 0.9594 | [0.9469, 0.9719] | 0.9594 | [0.9468, 0.9719] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | hann | H | B | 0.6809 | 0.6813 | [0.6594, 0.7031] | 0.6823 | [0.6615, 0.7042] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 128 | hann | minmax | S | 0.8367 | 0.8385 | [0.8177, 0.8594] | 0.8385 | [0.8187, 0.8604] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | hann | minmax | C | 0.9628 | 0.9594 | [0.9469, 0.9719] | 0.9594 | [0.9468, 0.9719] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | hann | minmax | B | 0.6809 | 0.6813 | [0.6594, 0.7031] | 0.6823 | [0.6615, 0.7042] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 128 | hann | minmax | SC | 0.9726 | 0.9646 | [0.9521, 0.975] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | raw | H | C | 0.9967 | 0.9969 | [0.9927, 1] | 0.9969 | [0.9927, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | raw | H | B | 0.6801 | 0.6823 | [0.6604, 0.7042] | 0.6792 | [0.6583, 0.701] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 512 | raw | minmax | S | 0.8375 | 0.8406 | [0.8208, 0.8615] | 0.8333 | [0.8135, 0.8542] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | raw | minmax | C | 0.9967 | 0.9969 | [0.9927, 1] | 0.9969 | [0.9927, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | raw | minmax | B | 0.6801 | 0.6823 | [0.6604, 0.7042] | 0.6792 | [0.6583, 0.701] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | raw | minmax | SC | 0.9959 | 0.9969 | [0.9927, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | hann | H | C | 0.9957 | 0.9969 | [0.9927, 1] | 0.9948 | [0.9896, 0.999] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | hann | H | B | 0.6784 | 0.6781 | [0.6562, 0.7] | 0.6813 | [0.6604, 0.7031] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_V | 0.3 | 512 | hann | minmax | S | 0.8375 | 0.8406 | [0.8208, 0.8615] | 0.8333 | [0.8135, 0.8542] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | hann | minmax | C | 0.9957 | 0.9969 | [0.9927, 1] | 0.9948 | [0.9896, 0.999] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | hann | minmax | B | 0.6784 | 0.6781 | [0.6562, 0.7] | 0.6813 | [0.6604, 0.7031] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.3 | 512 | hann | minmax | SC | 0.9945 | 0.9958 | [0.9917, 0.999] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 128 | raw | H | S | 0.9792 | 0.9792 | [0.9698, 0.9875] | 0.9729 | [0.9625, 0.9823] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | raw | H | C | 0.9215 | 0.9271 | [0.9104, 0.9437] | 0.9271 | [0.9104, 0.9427] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | raw | H | B | 0.6824 | 0.6802 | [0.6583, 0.7021] | 0.6969 | [0.675, 0.7188] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | raw | H | SC | 0.9791 | 0.9792 | [0.9698, 0.9875] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 128 | raw | minmax | S | 0.8138 | 0.8177 | [0.7969, 0.8385] | 0.8135 | [0.7927, 0.8354] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | raw | minmax | C | 0.9215 | 0.9271 | [0.9104, 0.9437] | 0.9271 | [0.9104, 0.9427] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | raw | minmax | B | 0.6824 | 0.6802 | [0.6583, 0.7021] | 0.6969 | [0.675, 0.7188] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | raw | minmax | SC | 0.9268 | 0.9281 | [0.9115, 0.9437] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 128 | hann | H | S | 0.9792 | 0.9792 | [0.9698, 0.9875] | 0.9729 | [0.9625, 0.9823] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | hann | H | C | 0.9122 | 0.9125 | [0.8938, 0.9292] | 0.9073 | [0.8896, 0.925] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | hann | H | B | 0.6811 | 0.6771 | [0.6542, 0.699] | 0.6844 | [0.6635, 0.7073] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | hann | H | SC | 0.9796 | 0.9781 | [0.9677, 0.9875] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 128 | hann | minmax | S | 0.8140 | 0.8177 | [0.7969, 0.8385] | 0.8135 | [0.7927, 0.8354] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | hann | minmax | C | 0.9122 | 0.9125 | [0.8938, 0.9292] | 0.9073 | [0.8896, 0.925] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | hann | minmax | B | 0.6811 | 0.6771 | [0.6542, 0.699] | 0.6844 | [0.6635, 0.7073] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 128 | hann | minmax | SC | 0.9212 | 0.9198 | [0.9021, 0.9354] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 512 | raw | H | S | 0.9792 | 0.9792 | [0.9698, 0.9875] | 0.9729 | [0.9625, 0.9823] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | raw | H | C | 0.9520 | 0.9490 | [0.9354, 0.9625] | 0.9542 | [0.9406, 0.9667] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | raw | H | B | 0.6797 | 0.6781 | [0.6562, 0.7] | 0.6802 | [0.6583, 0.7021] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | raw | H | SC | 0.9786 | 0.9760 | [0.9656, 0.9854] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 512 | raw | minmax | S | 0.8144 | 0.8187 | [0.7979, 0.8396] | 0.8146 | [0.7927, 0.8365] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | raw | minmax | C | 0.9520 | 0.9490 | [0.9354, 0.9625] | 0.9542 | [0.9406, 0.9667] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | raw | minmax | B | 0.6797 | 0.6781 | [0.6562, 0.7] | 0.6802 | [0.6583, 0.7021] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | raw | minmax | SC | 0.9461 | 0.9490 | [0.9354, 0.9625] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 512 | hann | H | S | 0.9792 | 0.9792 | [0.9698, 0.9875] | 0.9729 | [0.9625, 0.9823] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | hann | H | C | 0.9512 | 0.9510 | [0.9375, 0.9635] | 0.951 | [0.9375, 0.9635] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | hann | H | B | 0.6785 | 0.6760 | [0.6531, 0.6979] | 0.6792 | [0.6583, 0.701] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | hann | H | SC | 0.9792 | 0.9760 | [0.9656, 0.9854] | - | - | svm no | svm 0.001 |
| i_V | 0.5 | 512 | hann | minmax | S | 0.8144 | 0.8187 | [0.7979, 0.8396] | 0.8146 | [0.7927, 0.8365] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | hann | minmax | C | 0.9512 | 0.9510 | [0.9375, 0.9635] | 0.951 | [0.9375, 0.9635] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | hann | minmax | B | 0.6785 | 0.6760 | [0.6531, 0.6979] | 0.6792 | [0.6583, 0.701] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_V | 0.5 | 512 | hann | minmax | SC | 0.9433 | 0.9479 | [0.9343, 0.9604] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 128 | raw | H | S | 0.9671 | 0.9563 | [0.9437, 0.9688] | 0.9531 | [0.9396, 0.9667] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | raw | H | C | 0.9798 | 0.9844 | [0.9771, 0.9917] | 0.9833 | [0.975, 0.9917] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | raw | H | SC | 0.9942 | 0.9906 | [0.9844, 0.9958] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 128 | raw | minmax | S | 0.9749 | 0.9760 | [0.9667, 0.9854] | 0.9708 | [0.9604, 0.9812] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | raw | minmax | C | 0.9798 | 0.9844 | [0.9771, 0.9917] | 0.9833 | [0.975, 0.9917] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | raw | minmax | SC | 0.9975 | 0.9990 | [0.9969, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 128 | hann | H | S | 0.9693 | 0.9542 | [0.9406, 0.9656] | 0.9563 | [0.9437, 0.9677] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | hann | H | SC | 0.9999 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 128 | hann | minmax | S | 0.9759 | 0.9760 | [0.9656, 0.9854] | 0.9708 | [0.9604, 0.9812] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 512 | raw | H | S | 0.9662 | 0.9542 | [0.9406, 0.9656] | 0.9521 | [0.9396, 0.9646] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | raw | H | C | 0.9842 | 0.9854 | [0.9771, 0.9927] | 0.9823 | [0.9729, 0.9896] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | raw | H | SC | 0.9960 | 0.9958 | [0.9917, 0.999] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 512 | raw | minmax | S | 0.9743 | 0.9708 | [0.9604, 0.9802] | 0.9656 | [0.9542, 0.9771] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | raw | minmax | C | 0.9842 | 0.9854 | [0.9771, 0.9927] | 0.9823 | [0.9729, 0.9896] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | raw | minmax | SC | 0.9969 | 0.9969 | [0.9927, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 512 | hann | H | S | 0.9683 | 0.9552 | [0.9427, 0.9667] | 0.951 | [0.9385, 0.9635] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.1 | 512 | hann | minmax | S | 0.9759 | 0.9719 | [0.9615, 0.9812] | 0.9698 | [0.9594, 0.9792] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.1 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 128 | raw | H | S | 0.9398 | 0.9292 | [0.9135, 0.9448] | 0.9281 | [0.9135, 0.9437] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | raw | H | C | 0.9458 | 0.9510 | [0.9365, 0.9635] | 0.95 | [0.9354, 0.9625] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | raw | H | B | 1.0000 | 0.9979 | [0.9948, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | raw | H | SC | 0.9778 | 0.9719 | [0.9615, 0.9812] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 128 | raw | minmax | S | 0.9483 | 0.9437 | [0.9292, 0.9573] | 0.9417 | [0.926, 0.9552] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | raw | minmax | C | 0.9458 | 0.9510 | [0.9365, 0.9635] | 0.95 | [0.9354, 0.9625] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | raw | minmax | B | 1.0000 | 0.9979 | [0.9948, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | raw | minmax | SC | 0.9845 | 0.9781 | [0.9688, 0.9865] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 128 | hann | H | S | 0.9412 | 0.9302 | [0.9146, 0.9458] | 0.9302 | [0.9146, 0.9458] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | hann | H | C | 0.9984 | 0.9990 | [0.9969, 1] | 0.9979 | [0.9948, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | hann | H | SC | 0.9985 | 0.9958 | [0.9917, 0.999] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 128 | hann | minmax | S | 0.9493 | 0.9448 | [0.9302, 0.9583] | 0.95 | [0.9365, 0.9625] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | hann | minmax | C | 0.9984 | 0.9990 | [0.9969, 1] | 0.9979 | [0.9948, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 128 | hann | minmax | SC | 0.9997 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 512 | raw | H | S | 0.9417 | 0.9313 | [0.9156, 0.9458] | 0.9302 | [0.9146, 0.9448] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | raw | H | C | 0.9722 | 0.9625 | [0.95, 0.974] | 0.9552 | [0.9427, 0.9677] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | raw | H | SC | 0.9842 | 0.9812 | [0.9729, 0.9896] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 512 | raw | minmax | S | 0.9492 | 0.9448 | [0.9302, 0.9583] | 0.9427 | [0.9281, 0.9563] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | raw | minmax | C | 0.9722 | 0.9625 | [0.95, 0.974] | 0.9552 | [0.9427, 0.9677] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | raw | minmax | SC | 0.9864 | 0.9729 | [0.9625, 0.9823] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 512 | hann | H | S | 0.9422 | 0.9333 | [0.9187, 0.9479] | 0.9292 | [0.9135, 0.9448] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | hann | H | C | 0.9952 | 0.9917 | [0.9854, 0.9969] | 0.9958 | [0.9917, 0.999] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | hann | H | SC | 0.9947 | 0.9927 | [0.9875, 0.9979] | - | - | svm no | svm 0.001 |
| i_A | 0.3 | 512 | hann | minmax | S | 0.9514 | 0.9469 | [0.9323, 0.9604] | 0.9521 | [0.9385, 0.9646] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | hann | minmax | C | 0.9952 | 0.9917 | [0.9854, 0.9969] | 0.9958 | [0.9917, 0.999] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.3 | 512 | hann | minmax | SC | 0.9955 | 0.9979 | [0.9948, 1] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 128 | raw | H | S | 0.8960 | 0.8865 | [0.8677, 0.9052] | 0.8802 | [0.8604, 0.9] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | raw | H | C | 0.8989 | 0.9031 | [0.8854, 0.9208] | 0.9052 | [0.8875, 0.9229] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | raw | H | B | 0.9621 | 0.9625 | [0.951, 0.974] | 0.9625 | [0.951, 0.974] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | raw | H | SC | 0.9212 | 0.9167 | [0.899, 0.9333] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 128 | raw | minmax | S | 0.8995 | 0.8927 | [0.874, 0.9104] | 0.8875 | [0.8688, 0.9073] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | raw | minmax | C | 0.8989 | 0.9031 | [0.8854, 0.9208] | 0.9052 | [0.8875, 0.9229] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | raw | minmax | B | 0.9621 | 0.9625 | [0.951, 0.974] | 0.9625 | [0.951, 0.974] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | raw | minmax | SC | 0.9254 | 0.9271 | [0.9104, 0.9427] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 128 | hann | H | S | 0.8949 | 0.8844 | [0.8667, 0.9031] | 0.8833 | [0.8646, 0.9021] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | hann | H | C | 0.9549 | 0.9583 | [0.9458, 0.9708] | 0.9615 | [0.95, 0.9729] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | hann | H | B | 0.9885 | 0.9896 | [0.9833, 0.9958] | 0.9896 | [0.9833, 0.9958] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | hann | H | SC | 0.9575 | 0.9615 | [0.95, 0.9729] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 128 | hann | minmax | S | 0.8999 | 0.8969 | [0.8792, 0.9146] | 0.8938 | [0.874, 0.9115] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | hann | minmax | C | 0.9549 | 0.9583 | [0.9458, 0.9708] | 0.9615 | [0.95, 0.9729] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | hann | minmax | B | 0.9885 | 0.9896 | [0.9833, 0.9958] | 0.9896 | [0.9833, 0.9958] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 128 | hann | minmax | SC | 0.9646 | 0.9656 | [0.9542, 0.9771] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 512 | raw | H | S | 0.8958 | 0.8875 | [0.8688, 0.9062] | 0.8771 | [0.8573, 0.8959] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | raw | H | C | 0.9285 | 0.9302 | [0.9135, 0.9458] | 0.926 | [0.9094, 0.9417] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | raw | H | B | 0.9621 | 0.9625 | [0.951, 0.974] | 0.9625 | [0.95, 0.974] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | raw | H | SC | 0.9316 | 0.9323 | [0.9167, 0.9469] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 512 | raw | minmax | S | 0.8996 | 0.8958 | [0.8771, 0.9135] | 0.8875 | [0.8688, 0.9073] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | raw | minmax | C | 0.9285 | 0.9302 | [0.9135, 0.9458] | 0.926 | [0.9094, 0.9417] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | raw | minmax | B | 0.9621 | 0.9625 | [0.951, 0.974] | 0.9625 | [0.95, 0.974] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | raw | minmax | SC | 0.9361 | 0.9396 | [0.924, 0.9542] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 512 | hann | H | S | 0.8952 | 0.8875 | [0.8688, 0.9062] | 0.8833 | [0.8646, 0.9021] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | hann | H | C | 0.9452 | 0.9469 | [0.9333, 0.9604] | 0.9469 | [0.9333, 0.9604] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | hann | H | B | 0.9884 | 0.9896 | [0.9833, 0.9958] | 0.9896 | [0.9833, 0.9958] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | hann | H | SC | 0.9490 | 0.9500 | [0.9365, 0.9635] | - | - | svm no | svm 0.001 |
| i_A | 0.5 | 512 | hann | minmax | S | 0.9005 | 0.8958 | [0.8781, 0.9135] | 0.8917 | [0.8719, 0.9094] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | hann | minmax | C | 0.9452 | 0.9469 | [0.9333, 0.9604] | 0.9469 | [0.9333, 0.9604] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | hann | minmax | B | 0.9884 | 0.9896 | [0.9833, 0.9958] | 0.9896 | [0.9833, 0.9958] | svm no; threshold no | svm 0.001; threshold 0.001 |
| i_A | 0.5 | 512 | hann | minmax | SC | 0.9536 | 0.9552 | [0.9427, 0.9677] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 128 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 128 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 512 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.1 | 512 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.1 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 128 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 128 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 512 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.3 | 512 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.3 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | raw | H | C | 1.0000 | 0.9979 | [0.9948, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 128 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | raw | minmax | C | 1.0000 | 0.9979 | [0.9948, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 128 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 512 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s | 0.5 | 512 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s | 0.5 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.1 | 128 | raw | H | S | 0.5035 | 0.5000 | [0.4948, 0.5052] | 0.4979 | [0.4917, 0.5031] | svm yes; threshold yes | svm 0.565; threshold 0.681 |
| ii_s_gamma | 0.1 | 128 | raw | H | C | 0.9648 | 0.8979 | [0.8792, 0.9167] | 0.9552 | [0.9427, 0.9677] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | raw | H | SC | 0.9357 | 0.8979 | [0.8792, 0.9167] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | S | 0.5048 | 0.4969 | [0.4875, 0.5052] | 0.4958 | [0.4896, 0.501] | svm yes; threshold yes | svm 0.785; threshold 0.83 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | C | 0.9648 | 0.8979 | [0.8792, 0.9167] | 0.9552 | [0.9427, 0.9677] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | SC | 0.9357 | 0.8979 | [0.8792, 0.9167] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.1 | 128 | hann | H | S | 0.5026 | 0.5021 | [0.5, 0.5052] | 0.499 | [0.4948, 0.5021] | svm yes; threshold yes | svm 0.123; threshold 0.739 |
| ii_s_gamma | 0.1 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | S | 0.5025 | 0.4990 | [0.4938, 0.5031] | 0.5052 | [0.5, 0.5115] | svm yes; threshold yes | svm 0.754; threshold 0.039 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.1 | 512 | raw | H | S | 0.5029 | 0.5031 | [0.4969, 0.5094] | 0.501 | [0.4979, 0.5052] | svm yes; threshold yes | svm 0.226; threshold 0.397 |
| ii_s_gamma | 0.1 | 512 | raw | H | C | 0.7665 | 0.5188 | [0.4875, 0.551] | 0.7729 | [0.75, 0.7948] | svm yes; threshold no | svm 0.24; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | raw | H | SC | 0.5262 | 0.5188 | [0.4875, 0.551] | - | - | svm yes | svm 0.234 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | S | 0.5037 | 0.4990 | [0.4906, 0.5073] | 0.499 | [0.4927, 0.5062] | svm yes; threshold yes | svm 0.645; threshold 0.586 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | C | 0.7665 | 0.5188 | [0.4875, 0.551] | 0.7729 | [0.75, 0.7948] | svm yes; threshold no | svm 0.24; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | SC | 0.5263 | 0.5188 | [0.4875, 0.551] | - | - | svm yes | svm 0.239 |
| ii_s_gamma | 0.1 | 512 | hann | H | S | 0.5010 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 0.995; threshold 0.99 |
| ii_s_gamma | 0.1 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | S | 0.5011 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 0.999; threshold 0.869 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.3 | 128 | raw | H | S | 0.5049 | 0.4979 | [0.4917, 0.5042] | 0.5083 | [0.5021, 0.5146] | svm yes; threshold yes | svm 0.706; threshold 0.074 |
| ii_s_gamma | 0.3 | 128 | raw | H | C | 0.9324 | 0.8812 | [0.8625, 0.9] | 0.9344 | [0.9187, 0.949] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | raw | H | SC | 0.8905 | 0.8812 | [0.8625, 0.9] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | S | 0.5037 | 0.5062 | [0.4979, 0.5156] | 0.4958 | [0.4865, 0.5052] | svm yes; threshold yes | svm 0.129; threshold 0.757 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | C | 0.9324 | 0.8812 | [0.8625, 0.9] | 0.9344 | [0.9187, 0.949] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | SC | 0.8905 | 0.8812 | [0.8625, 0.9] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.3 | 128 | hann | H | S | 0.5028 | 0.4979 | [0.4938, 0.5021] | 0.5 | [0.4969, 0.5031] | svm yes; threshold yes | svm 0.846; threshold 0.539 |
| ii_s_gamma | 0.3 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | S | 0.5044 | 0.5052 | [0.5, 0.5115] | 0.4969 | [0.4906, 0.5021] | svm yes; threshold yes | svm 0.088; threshold 0.85 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.3 | 512 | raw | H | S | 0.5043 | 0.5021 | [0.4958, 0.5083] | 0.4969 | [0.4906, 0.5031] | svm yes; threshold yes | svm 0.332; threshold 0.776 |
| ii_s_gamma | 0.3 | 512 | raw | H | C | 0.7604 | 0.5115 | [0.4792, 0.5437] | 0.7615 | [0.7396, 0.7844] | svm yes; threshold no | svm 0.411; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | raw | H | SC | 0.5139 | 0.5115 | [0.4792, 0.5437] | - | - | svm yes | svm 0.4 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | S | 0.5033 | 0.5000 | [0.4927, 0.5073] | 0.4917 | [0.4833, 0.499] | svm yes; threshold yes | svm 0.565; threshold 0.963 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | C | 0.7604 | 0.5115 | [0.4792, 0.5437] | 0.7615 | [0.7396, 0.7844] | svm yes; threshold no | svm 0.411; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | SC | 0.5139 | 0.5115 | [0.4792, 0.5437] | - | - | svm yes | svm 0.392 |
| ii_s_gamma | 0.3 | 512 | hann | H | S | 0.5009 | 0.5010 | [0.5, 0.5031] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 0.494; threshold 0.998 |
| ii_s_gamma | 0.3 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | S | 0.5012 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 0.996; threshold 0.68 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.5 | 128 | raw | H | S | 0.5040 | 0.5073 | [0.5, 0.5146] | 0.4979 | [0.4896, 0.5062] | svm yes; threshold yes | svm 0.028; threshold 0.687 |
| ii_s_gamma | 0.5 | 128 | raw | H | C | 0.9027 | 0.8406 | [0.8187, 0.8615] | 0.9125 | [0.8958, 0.9281] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | raw | H | SC | 0.8388 | 0.8406 | [0.8187, 0.8615] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | S | 0.5047 | 0.5031 | [0.4948, 0.5125] | 0.5062 | [0.499, 0.5135] | svm yes; threshold yes | svm 0.312; threshold 0.151 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | C | 0.9027 | 0.8406 | [0.8187, 0.8615] | 0.9125 | [0.8958, 0.9281] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | SC | 0.8388 | 0.8406 | [0.8187, 0.8615] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.5 | 128 | hann | H | S | 0.5041 | 0.5010 | [0.4979, 0.5052] | 0.5 | [0.4948, 0.5052] | svm yes; threshold yes | svm 0.41; threshold 0.525 |
| ii_s_gamma | 0.5 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | S | 0.5042 | 0.5021 | [0.5, 0.5052] | 0.5 | [0.4958, 0.5042] | svm yes; threshold yes | svm 0.229; threshold 0.529 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.5 | 512 | raw | H | S | 0.5043 | 0.5010 | [0.4938, 0.5083] | 0.4969 | [0.4906, 0.5031] | svm yes; threshold yes | svm 0.478; threshold 0.799 |
| ii_s_gamma | 0.5 | 512 | raw | H | C | 0.7587 | 0.5062 | [0.474, 0.5385] | 0.7635 | [0.7417, 0.7865] | svm yes; threshold no | svm 0.484; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | raw | H | SC | 0.5106 | 0.5062 | [0.474, 0.5385] | - | - | svm yes | svm 0.472 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | S | 0.5039 | 0.5052 | [0.4958, 0.5146] | 0.4979 | [0.4896, 0.5062] | svm yes; threshold yes | svm 0.181; threshold 0.666 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | C | 0.7587 | 0.5062 | [0.474, 0.5385] | 0.7635 | [0.7417, 0.7865] | svm yes; threshold no | svm 0.484; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | SC | 0.5106 | 0.5062 | [0.474, 0.5385] | - | - | svm yes | svm 0.469 |
| ii_s_gamma | 0.5 | 512 | hann | H | S | 0.5009 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 0.998; threshold 0.781 |
| ii_s_gamma | 0.5 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | S | 0.5009 | 0.5000 | [0.5, 0.5] | 0.5042 | [0.501, 0.5083] | svm yes; threshold yes | svm 0.997; threshold 0.008 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 128 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 128 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 512 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.1 | 512 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.1 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 128 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 128 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 512 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.3 | 512 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.3 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 128 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | raw | H | C | 1.0000 | 0.9979 | [0.9948, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 128 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | raw | minmax | C | 1.0000 | 0.9979 | [0.9948, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 128 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 128 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 128 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 512 | raw | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | raw | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | raw | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | raw | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 512 | raw | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | raw | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | raw | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | raw | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 512 | hann | H | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | hann | H | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | hann | H | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | hann | H | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| corners | 0.5 | 512 | hann | minmax | S | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | hann | minmax | C | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | hann | minmax | B | 1.0000 | 1.0000 | [1, 1] | 1 | [1, 1] | svm no; threshold no | svm 0.001; threshold 0.001 |
| corners | 0.5 | 512 | hann | minmax | SC | 1.0000 | 1.0000 | [1, 1] | - | - | svm no | svm 0.001 |
| iii_null | - | 128 | raw | H | S | 0.5079 | 0.4760 | [0.45, 0.5031] | 0.4802 | [0.45, 0.5115] | svm yes; threshold yes | svm 0.909; threshold 0.833 |
| iii_null | - | 128 | raw | H | C | 0.5073 | 0.4813 | [0.449, 0.5125] | 0.4615 | [0.4323, 0.4896] | svm yes; threshold no | svm 0.814; threshold 0.983 |
| iii_null | - | 128 | raw | H | B | 0.5046 | 0.4792 | [0.45, 0.5083] | 0.4719 | [0.4437, 0.5] | svm yes; threshold no | svm 0.839; threshold 0.923 |
| iii_null | - | 128 | raw | H | SC | 0.5040 | 0.4833 | [0.4531, 0.5125] | - | - | svm yes | svm 0.813 |
| iii_null | - | 128 | raw | minmax | S | 0.5070 | 0.4854 | [0.4573, 0.5125] | 0.5135 | [0.4885, 0.5396] | svm yes; threshold yes | svm 0.764; threshold 0.273 |
| iii_null | - | 128 | raw | minmax | C | 0.5073 | 0.4813 | [0.449, 0.5125] | 0.4615 | [0.4323, 0.4896] | svm yes; threshold no | svm 0.814; threshold 0.983 |
| iii_null | - | 128 | raw | minmax | B | 0.5046 | 0.4792 | [0.45, 0.5083] | 0.4719 | [0.4437, 0.5] | svm yes; threshold no | svm 0.839; threshold 0.923 |
| iii_null | - | 128 | raw | minmax | SC | 0.4976 | 0.4885 | [0.4615, 0.5156] | - | - | svm yes | svm 0.74 |
| iii_null | - | 128 | hann | H | S | 0.5079 | 0.4740 | [0.4448, 0.5021] | 0.4802 | [0.45, 0.5115] | svm no; threshold yes | svm 0.929; threshold 0.834 |
| iii_null | - | 128 | hann | H | C | 0.5068 | 0.4865 | [0.4542, 0.5188] | 0.4906 | [0.4604, 0.5188] | svm yes; threshold yes | svm 0.732; threshold 0.678 |
| iii_null | - | 128 | hann | H | B | 0.5048 | 0.4792 | [0.45, 0.5083] | 0.4698 | [0.4417, 0.4969] | svm yes; threshold no | svm 0.839; threshold 0.942 |
| iii_null | - | 128 | hann | H | SC | 0.4996 | 0.5052 | [0.474, 0.5334] | - | - | svm yes | svm 0.422 |
| iii_null | - | 128 | hann | minmax | S | 0.5070 | 0.4854 | [0.4573, 0.5125] | 0.5135 | [0.4885, 0.5396] | svm yes; threshold yes | svm 0.764; threshold 0.273 |
| iii_null | - | 128 | hann | minmax | C | 0.5068 | 0.4865 | [0.4542, 0.5188] | 0.4906 | [0.4604, 0.5188] | svm yes; threshold yes | svm 0.733; threshold 0.678 |
| iii_null | - | 128 | hann | minmax | B | 0.5048 | 0.4792 | [0.45, 0.5083] | 0.4698 | [0.4417, 0.4969] | svm yes; threshold no | svm 0.836; threshold 0.942 |
| iii_null | - | 128 | hann | minmax | SC | 0.4959 | 0.4948 | [0.4688, 0.5219] | - | - | svm yes | svm 0.637 |
| iii_null | - | 512 | raw | H | S | 0.5079 | 0.4802 | [0.451, 0.5094] | 0.4906 | [0.4583, 0.5219] | svm yes; threshold yes | svm 0.856; threshold 0.702 |
| iii_null | - | 512 | raw | H | C | 0.5067 | 0.4760 | [0.4458, 0.5073] | 0.4938 | [0.4646, 0.5208] | svm yes; threshold yes | svm 0.869; threshold 0.621 |
| iii_null | - | 512 | raw | H | B | 0.5048 | 0.4802 | [0.451, 0.5094] | 0.4771 | [0.449, 0.5042] | svm yes; threshold yes | svm 0.821; threshold 0.876 |
| iii_null | - | 512 | raw | H | SC | 0.5036 | 0.4677 | [0.4385, 0.4958] | - | - | svm no | svm 0.944 |
| iii_null | - | 512 | raw | minmax | S | 0.5061 | 0.4823 | [0.4552, 0.5104] | 0.5042 | [0.476, 0.5312] | svm yes; threshold yes | svm 0.82; threshold 0.435 |
| iii_null | - | 512 | raw | minmax | C | 0.5067 | 0.4760 | [0.4458, 0.5073] | 0.4938 | [0.4646, 0.5208] | svm yes; threshold yes | svm 0.869; threshold 0.621 |
| iii_null | - | 512 | raw | minmax | B | 0.5048 | 0.4802 | [0.451, 0.5094] | 0.4771 | [0.449, 0.5042] | svm yes; threshold yes | svm 0.822; threshold 0.876 |
| iii_null | - | 512 | raw | minmax | SC | 0.4972 | 0.4813 | [0.4542, 0.5083] | - | - | svm yes | svm 0.836 |
| iii_null | - | 512 | hann | H | S | 0.5079 | 0.4802 | [0.451, 0.5094] | 0.4906 | [0.4583, 0.5219] | svm yes; threshold yes | svm 0.852; threshold 0.702 |
| iii_null | - | 512 | hann | H | C | 0.5065 | 0.4771 | [0.4458, 0.5073] | 0.4896 | [0.4615, 0.5177] | svm yes; threshold yes | svm 0.866; threshold 0.7 |
| iii_null | - | 512 | hann | H | B | 0.5047 | 0.4792 | [0.45, 0.5083] | 0.4719 | [0.4437, 0.5] | svm yes; threshold no | svm 0.834; threshold 0.927 |
| iii_null | - | 512 | hann | H | SC | 0.5030 | 0.4688 | [0.4416, 0.4969] | - | - | svm no | svm 0.936 |
| iii_null | - | 512 | hann | minmax | S | 0.5061 | 0.4823 | [0.4552, 0.5104] | 0.5042 | [0.476, 0.5312] | svm yes; threshold yes | svm 0.818; threshold 0.435 |
| iii_null | - | 512 | hann | minmax | C | 0.5065 | 0.4771 | [0.4458, 0.5073] | 0.4896 | [0.4615, 0.5177] | svm yes; threshold yes | svm 0.868; threshold 0.7 |
| iii_null | - | 512 | hann | minmax | B | 0.5047 | 0.4792 | [0.45, 0.5083] | 0.4719 | [0.4437, 0.5] | svm yes; threshold no | svm 0.837; threshold 0.927 |
| iii_null | - | 512 | hann | minmax | SC | 0.4951 | 0.4854 | [0.4573, 0.5125] | - | - | svm yes | svm 0.793 |
| check_same_seed | - | 128 | raw | H | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | raw | H | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | raw | H | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | raw | H | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |
| check_same_seed | - | 128 | raw | minmax | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | raw | minmax | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | raw | minmax | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | raw | minmax | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |
| check_same_seed | - | 128 | hann | H | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | hann | H | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | hann | H | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | hann | H | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |
| check_same_seed | - | 128 | hann | minmax | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | hann | minmax | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | hann | minmax | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 128 | hann | minmax | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |
| check_same_seed | - | 512 | raw | H | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | raw | H | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | raw | H | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | raw | H | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |
| check_same_seed | - | 512 | raw | minmax | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | raw | minmax | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | raw | minmax | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | raw | minmax | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |
| check_same_seed | - | 512 | hann | H | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | hann | H | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | hann | H | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | hann | H | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |
| check_same_seed | - | 512 | hann | minmax | S | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | hann | minmax | C | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | hann | minmax | B | 0.5000 | 0.5000 | [0.5, 0.5] | 0.5 | [0.5, 0.5] | svm yes; threshold yes | svm 1; threshold 1 |
| check_same_seed | - | 512 | hann | minmax | SC | 0.5000 | 0.5000 | [0.5, 0.5] | - | - | svm yes | svm 1 |

## Mechanism check (jitter-free centres, seeds 1000-1099)

| condition | group | N | repr | proc | descriptor | mean | sd | min | max |
|---|---|---|---|---|---|---|---|---|---|
| i_V_centre | 0 | 128 | H | raw | sq | 0.13076 | 0.00471 | 0.12198 | 0.14289 |
| i_V_centre | 0 | 128 | H | raw | centroid_amp | 33.873 | 0.661 | 32.365 | 35.885 |
| i_V_centre | 0 | 128 | H | raw | centroid_band_power | 9.6984 | 0.158 | 9.3437 | 10.102 |
| i_V_centre | 0 | 128 | H | hann | sq | 0.049036 | 0.00177 | 0.045738 | 0.053573 |
| i_V_centre | 0 | 128 | H | hann | centroid_amp | 31.111 | 0.681 | 29.667 | 33.261 |
| i_V_centre | 0 | 128 | H | hann | centroid_band_power | 9.7134 | 0.157 | 9.3631 | 10.122 |
| i_V_centre | 0 | 128 | minmax | raw | sq | 0.28479 | 0.00997 | 0.26373 | 0.31167 |
| i_V_centre | 0 | 128 | minmax | raw | centroid_amp | 33.873 | 0.661 | 32.365 | 35.885 |
| i_V_centre | 0 | 128 | minmax | raw | centroid_band_power | 9.6984 | 0.158 | 9.3437 | 10.102 |
| i_V_centre | 0 | 128 | minmax | hann | sq | 0.1068 | 0.00374 | 0.098915 | 0.11686 |
| i_V_centre | 0 | 128 | minmax | hann | centroid_amp | 31.111 | 0.681 | 29.667 | 33.261 |
| i_V_centre | 0 | 128 | minmax | hann | centroid_band_power | 9.7134 | 0.157 | 9.3631 | 10.122 |
| i_V_centre | 0 | 512 | H | raw | sq | 0.13067 | 0.00471 | 0.12171 | 0.14289 |
| i_V_centre | 0 | 512 | H | raw | centroid_amp | 98.536 | 2.16 | 93.956 | 104.71 |
| i_V_centre | 0 | 512 | H | raw | centroid_band_power | 9.6938 | 0.158 | 9.3394 | 10.096 |
| i_V_centre | 0 | 512 | H | hann | sq | 0.049002 | 0.00177 | 0.045643 | 0.053586 |
| i_V_centre | 0 | 512 | H | hann | centroid_amp | 85.984 | 1.99 | 81.734 | 92.123 |
| i_V_centre | 0 | 512 | H | hann | centroid_band_power | 9.709 | 0.157 | 9.357 | 10.112 |
| i_V_centre | 0 | 512 | minmax | raw | sq | 0.28459 | 0.00996 | 0.2637 | 0.31143 |
| i_V_centre | 0 | 512 | minmax | raw | centroid_amp | 98.536 | 2.16 | 93.956 | 104.71 |
| i_V_centre | 0 | 512 | minmax | raw | centroid_band_power | 9.6938 | 0.158 | 9.3394 | 10.096 |
| i_V_centre | 0 | 512 | minmax | hann | sq | 0.10672 | 0.00373 | 0.098887 | 0.11679 |
| i_V_centre | 0 | 512 | minmax | hann | centroid_amp | 85.984 | 1.99 | 81.734 | 92.123 |
| i_V_centre | 0 | 512 | minmax | hann | centroid_band_power | 9.709 | 0.157 | 9.357 | 10.112 |
| i_V_centre | 1 | 128 | H | raw | sq | 0.060205 | 0.00265 | 0.055226 | 0.067463 |
| i_V_centre | 1 | 128 | H | raw | centroid_amp | 30.98 | 0.628 | 29.525 | 32.845 |
| i_V_centre | 1 | 128 | H | raw | centroid_band_power | 9.5669 | 0.112 | 9.2926 | 9.8474 |
| i_V_centre | 1 | 128 | H | hann | sq | 0.022577 | 0.000993 | 0.020709 | 0.025295 |
| i_V_centre | 1 | 128 | H | hann | centroid_amp | 28.507 | 0.618 | 27.171 | 30.411 |
| i_V_centre | 1 | 128 | H | hann | centroid_band_power | 9.5843 | 0.111 | 9.3128 | 9.8629 |
| i_V_centre | 1 | 128 | minmax | raw | sq | 0.26429 | 0.0107 | 0.24179 | 0.29173 |
| i_V_centre | 1 | 128 | minmax | raw | centroid_amp | 30.98 | 0.628 | 29.525 | 32.845 |
| i_V_centre | 1 | 128 | minmax | raw | centroid_band_power | 9.5669 | 0.112 | 9.2926 | 9.8474 |
| i_V_centre | 1 | 128 | minmax | hann | sq | 0.099109 | 0.004 | 0.090679 | 0.10939 |
| i_V_centre | 1 | 128 | minmax | hann | centroid_amp | 28.507 | 0.618 | 27.171 | 30.411 |
| i_V_centre | 1 | 128 | minmax | hann | centroid_band_power | 9.5843 | 0.111 | 9.3128 | 9.8629 |
| i_V_centre | 1 | 512 | H | raw | sq | 0.060154 | 0.00265 | 0.055174 | 0.067464 |
| i_V_centre | 1 | 512 | H | raw | centroid_amp | 81.836 | 2.1 | 77.359 | 87.55 |
| i_V_centre | 1 | 512 | H | raw | centroid_band_power | 9.5649 | 0.112 | 9.2908 | 9.8449 |
| i_V_centre | 1 | 512 | H | hann | sq | 0.022558 | 0.000994 | 0.02069 | 0.025299 |
| i_V_centre | 1 | 512 | H | hann | centroid_amp | 71.542 | 1.88 | 67.528 | 77.001 |
| i_V_centre | 1 | 512 | H | hann | centroid_band_power | 9.5824 | 0.111 | 9.31 | 9.8619 |
| i_V_centre | 1 | 512 | minmax | raw | sq | 0.26407 | 0.0107 | 0.24175 | 0.29146 |
| i_V_centre | 1 | 512 | minmax | raw | centroid_amp | 81.836 | 2.1 | 77.359 | 87.55 |
| i_V_centre | 1 | 512 | minmax | raw | centroid_band_power | 9.5649 | 0.112 | 9.2908 | 9.8449 |
| i_V_centre | 1 | 512 | minmax | hann | sq | 0.099025 | 0.004 | 0.090656 | 0.1093 |
| i_V_centre | 1 | 512 | minmax | hann | centroid_amp | 71.542 | 1.88 | 67.528 | 77.001 |
| i_V_centre | 1 | 512 | minmax | hann | centroid_band_power | 9.5824 | 0.111 | 9.31 | 9.8619 |
| i_A_centre | 0 | 128 | H | raw | sq | 0.087719 | 0.00434 | 0.079044 | 0.1 |
| i_A_centre | 0 | 128 | H | raw | centroid_amp | 21.067 | 0.513 | 19.913 | 22.546 |
| i_A_centre | 0 | 128 | H | raw | centroid_band_power | 7.6578 | 0.0807 | 7.4686 | 7.8677 |
| i_A_centre | 0 | 128 | H | hann | sq | 0.032895 | 0.00163 | 0.029641 | 0.037501 |
| i_A_centre | 0 | 128 | H | hann | centroid_amp | 21.086 | 0.512 | 19.933 | 22.563 |
| i_A_centre | 0 | 128 | H | hann | centroid_band_power | 7.6827 | 0.0808 | 7.4948 | 7.8929 |
| i_A_centre | 0 | 128 | minmax | raw | sq | 0.25795 | 0.0112 | 0.23391 | 0.28599 |
| i_A_centre | 0 | 128 | minmax | raw | centroid_amp | 21.067 | 0.513 | 19.913 | 22.546 |
| i_A_centre | 0 | 128 | minmax | raw | centroid_band_power | 7.6578 | 0.0807 | 7.4686 | 7.8677 |
| i_A_centre | 0 | 128 | minmax | hann | sq | 0.096733 | 0.00418 | 0.087715 | 0.10725 |
| i_A_centre | 0 | 128 | minmax | hann | centroid_amp | 21.086 | 0.512 | 19.933 | 22.563 |
| i_A_centre | 0 | 128 | minmax | hann | centroid_band_power | 7.6827 | 0.0808 | 7.4948 | 7.8929 |
| i_A_centre | 0 | 512 | H | raw | sq | 0.086511 | 0.00419 | 0.078566 | 0.098299 |
| i_A_centre | 0 | 512 | H | raw | centroid_amp | 47.388 | 1.4 | 44.481 | 51.361 |
| i_A_centre | 0 | 512 | H | raw | centroid_band_power | 7.6562 | 0.0796 | 7.465 | 7.8704 |
| i_A_centre | 0 | 512 | H | hann | sq | 0.032442 | 0.00157 | 0.029462 | 0.036862 |
| i_A_centre | 0 | 512 | H | hann | centroid_amp | 47.407 | 1.4 | 44.501 | 51.379 |
| i_A_centre | 0 | 512 | H | hann | centroid_band_power | 7.6811 | 0.0797 | 7.4912 | 7.8956 |
| i_A_centre | 0 | 512 | minmax | raw | sq | 0.25425 | 0.011 | 0.23109 | 0.28182 |
| i_A_centre | 0 | 512 | minmax | raw | centroid_amp | 47.388 | 1.4 | 44.481 | 51.361 |
| i_A_centre | 0 | 512 | minmax | raw | centroid_band_power | 7.6562 | 0.0796 | 7.465 | 7.8704 |
| i_A_centre | 0 | 512 | minmax | hann | sq | 0.095345 | 0.00413 | 0.086661 | 0.10568 |
| i_A_centre | 0 | 512 | minmax | hann | centroid_amp | 47.407 | 1.4 | 44.501 | 51.379 |
| i_A_centre | 0 | 512 | minmax | hann | centroid_band_power | 7.6811 | 0.0797 | 7.4912 | 7.8956 |
| i_A_centre | 1 | 128 | H | raw | sq | 0.10123 | 0.00341 | 0.094678 | 0.11043 |
| i_A_centre | 1 | 128 | H | raw | centroid_amp | 34.764 | 0.75 | 33.115 | 37.115 |
| i_A_centre | 1 | 128 | H | raw | centroid_band_power | 10.56 | 0.0621 | 10.391 | 10.693 |
| i_A_centre | 1 | 128 | H | hann | sq | 0.03796 | 0.00128 | 0.035504 | 0.041412 |
| i_A_centre | 1 | 128 | H | hann | centroid_amp | 34.419 | 0.756 | 32.773 | 36.797 |
| i_A_centre | 1 | 128 | H | hann | centroid_band_power | 10.577 | 0.062 | 10.407 | 10.709 |
| i_A_centre | 1 | 128 | minmax | raw | sq | 0.29316 | 0.00977 | 0.27306 | 0.31981 |
| i_A_centre | 1 | 128 | minmax | raw | centroid_amp | 34.764 | 0.75 | 33.115 | 37.115 |
| i_A_centre | 1 | 128 | minmax | raw | centroid_band_power | 10.56 | 0.0621 | 10.391 | 10.693 |
| i_A_centre | 1 | 128 | minmax | hann | sq | 0.10993 | 0.00366 | 0.1024 | 0.11993 |
| i_A_centre | 1 | 128 | minmax | hann | centroid_amp | 34.419 | 0.756 | 32.773 | 36.797 |
| i_A_centre | 1 | 128 | minmax | hann | centroid_band_power | 10.577 | 0.062 | 10.407 | 10.709 |
| i_A_centre | 1 | 512 | H | raw | sq | 0.10095 | 0.00337 | 0.094466 | 0.10945 |
| i_A_centre | 1 | 512 | H | raw | centroid_amp | 99.261 | 2.21 | 94.466 | 105.7 |
| i_A_centre | 1 | 512 | H | raw | centroid_band_power | 10.551 | 0.0629 | 10.379 | 10.683 |
| i_A_centre | 1 | 512 | H | hann | sq | 0.037856 | 0.00127 | 0.035425 | 0.041045 |
| i_A_centre | 1 | 512 | H | hann | centroid_amp | 97.608 | 2.19 | 92.868 | 104.08 |
| i_A_centre | 1 | 512 | H | hann | centroid_band_power | 10.568 | 0.0629 | 10.397 | 10.7 |
| i_A_centre | 1 | 512 | minmax | raw | sq | 0.29237 | 0.0097 | 0.27204 | 0.31892 |
| i_A_centre | 1 | 512 | minmax | raw | centroid_amp | 99.261 | 2.21 | 94.466 | 105.7 |
| i_A_centre | 1 | 512 | minmax | raw | centroid_band_power | 10.551 | 0.0629 | 10.379 | 10.683 |
| i_A_centre | 1 | 512 | minmax | hann | sq | 0.10964 | 0.00364 | 0.10202 | 0.11959 |
| i_A_centre | 1 | 512 | minmax | hann | centroid_amp | 97.608 | 2.19 | 92.868 | 104.08 |
| i_A_centre | 1 | 512 | minmax | hann | centroid_band_power | 10.568 | 0.0629 | 10.397 | 10.7 |

## Clipping at the corners (fraction of surfaces with a clipped coordinate, group 0 / group 1)

| condition | fractions |
|---|---|
| ii_s_w0.1 | [0.7583, 0.7583] |
| ii_s_w0.3 | [0.7583, 0.7583] |
| ii_s_w0.5 | [0.7583, 0.7583] |
| ii_s_gamma_w0.1 | [0.7583, 0.7583] |
| ii_s_gamma_w0.3 | [0.7583, 0.7583] |
| ii_s_gamma_w0.5 | [0.7583, 0.7583] |
| corners_w0.1 | [0.7583, 0.7583] |
| corners_w0.3 | [0.7583, 0.7583] |
| corners_w0.5 | [0.7583, 0.7583] |
