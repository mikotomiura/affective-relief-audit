# K5: choice of the number of pairs (TOST power)

Conditions: `experiments/conditions/k5_classification.json` (SHA-256 `09a914161be116f44ab83f32277e5c48db3f304370f0f2bad59e5009b152d5e6`). Predictions: `experiments/conditions/k5_table1_predictions.json` (SHA-256 `6cf0f96992bd4acab004d03f66b0566c355f84f14eb8bf869709d9a33db7693b`). Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`). Script SHA-256 `f27dde51be04fa2b980c63c1d966984a9007a48e8c534d82c61dd859cd69bfed`. numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, Python 3.13.12. Run started 2026-10-25T15:06:39+00:00 and finished 2026-10-25T15:55:26+00:00 (Darwin arm64, 10 logical CPUs).

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

Chosen per_class_n: **480** (no candidate satisfied both requirements; the largest candidate is used)

(a) iii_null, 200 runs: smallest equivalence rate over the columns, and its complement (the observed false non-equivalence rate). (b) corners, w = 0.5, N = 128, raw, H, svm, {sq, centroid_amp}, 50 runs: mean half-width of the 95% interval.

The joint rate is the fraction of runs in which every column is declared at chance at once (P-K5-3 is a joint claim; the power rule only bounds each column).

| n | (a) min rate | column with min rate | false non-equivalence | joint rate | (a) holds | (b) mean half-width | (b) holds |
|---|---|---|---|---|---|---|---|
| 60 | 0.000 | 128|raw|H|sq|svm | 1.000 | 0.000 | no | 0.0000 | yes |
| 120 | 0.000 | 128|raw|H|centroid_band_power|svm | 1.000 | 0.000 | no | 0.0000 | yes |
| 240 | 0.290 | 128|raw|minmax|sq|svm | 0.710 | 0.000 | no | 0.0000 | yes |
| 480 | 0.730 | 128|hann|H|centroid_band_power|threshold | 0.270 | 0.080 | no | 0.0000 | yes |

Equivalence rate by column, for each n:

| column | 60 | 120 | 240 | 480 |
|---|---|---|---|---|
| 128|raw|H|sq|svm | 0.000 | 0.010 | 0.310 | 0.810 |
| 128|raw|H|sq|threshold | 0.000 | 0.110 | 0.455 | 0.785 |
| 128|raw|H|centroid_amp|svm | 0.000 | 0.010 | 0.325 | 0.790 |
| 128|raw|H|centroid_amp|threshold | 0.000 | 0.080 | 0.430 | 0.820 |
| 128|raw|H|centroid_band_power|svm | 0.000 | 0.000 | 0.360 | 0.810 |
| 128|raw|H|centroid_band_power|threshold | 0.000 | 0.085 | 0.405 | 0.755 |
| 128|raw|H|sq+centroid_amp|svm | 0.000 | 0.010 | 0.430 | 0.790 |
| 128|raw|minmax|sq|svm | 0.000 | 0.020 | 0.290 | 0.815 |
| 128|raw|minmax|sq|threshold | 0.000 | 0.065 | 0.435 | 0.775 |
| 128|raw|minmax|centroid_amp|svm | 0.000 | 0.010 | 0.325 | 0.785 |
| 128|raw|minmax|centroid_amp|threshold | 0.000 | 0.080 | 0.430 | 0.820 |
| 128|raw|minmax|centroid_band_power|svm | 0.000 | 0.000 | 0.360 | 0.810 |
| 128|raw|minmax|centroid_band_power|threshold | 0.000 | 0.085 | 0.405 | 0.755 |
| 128|raw|minmax|sq+centroid_amp|svm | 0.000 | 0.035 | 0.315 | 0.765 |
| 128|hann|H|sq|svm | 0.000 | 0.015 | 0.320 | 0.810 |
| 128|hann|H|sq|threshold | 0.000 | 0.110 | 0.455 | 0.790 |
| 128|hann|H|centroid_amp|svm | 0.000 | 0.010 | 0.300 | 0.820 |
| 128|hann|H|centroid_amp|threshold | 0.000 | 0.055 | 0.455 | 0.805 |
| 128|hann|H|centroid_band_power|svm | 0.000 | 0.000 | 0.380 | 0.795 |
| 128|hann|H|centroid_band_power|threshold | 0.000 | 0.080 | 0.410 | 0.730 |
| 128|hann|H|sq+centroid_amp|svm | 0.000 | 0.015 | 0.365 | 0.790 |
| 128|hann|minmax|sq|svm | 0.000 | 0.020 | 0.290 | 0.820 |
| 128|hann|minmax|sq|threshold | 0.000 | 0.065 | 0.435 | 0.775 |
| 128|hann|minmax|centroid_amp|svm | 0.000 | 0.010 | 0.300 | 0.815 |
| 128|hann|minmax|centroid_amp|threshold | 0.000 | 0.055 | 0.455 | 0.805 |
| 128|hann|minmax|centroid_band_power|svm | 0.000 | 0.000 | 0.385 | 0.795 |
| 128|hann|minmax|centroid_band_power|threshold | 0.000 | 0.080 | 0.410 | 0.730 |
| 128|hann|minmax|sq+centroid_amp|svm | 0.000 | 0.030 | 0.340 | 0.765 |
| 512|raw|H|sq|svm | 0.000 | 0.010 | 0.315 | 0.800 |
| 512|raw|H|sq|threshold | 0.005 | 0.075 | 0.440 | 0.770 |
| 512|raw|H|centroid_amp|svm | 0.000 | 0.010 | 0.290 | 0.765 |
| 512|raw|H|centroid_amp|threshold | 0.000 | 0.110 | 0.400 | 0.740 |
| 512|raw|H|centroid_band_power|svm | 0.000 | 0.000 | 0.350 | 0.815 |
| 512|raw|H|centroid_band_power|threshold | 0.000 | 0.065 | 0.385 | 0.735 |
| 512|raw|H|sq+centroid_amp|svm | 0.000 | 0.005 | 0.380 | 0.770 |
| 512|raw|minmax|sq|svm | 0.000 | 0.020 | 0.320 | 0.825 |
| 512|raw|minmax|sq|threshold | 0.000 | 0.080 | 0.420 | 0.765 |
| 512|raw|minmax|centroid_amp|svm | 0.000 | 0.005 | 0.295 | 0.765 |
| 512|raw|minmax|centroid_amp|threshold | 0.000 | 0.110 | 0.400 | 0.740 |
| 512|raw|minmax|centroid_band_power|svm | 0.000 | 0.000 | 0.355 | 0.815 |
| 512|raw|minmax|centroid_band_power|threshold | 0.000 | 0.065 | 0.385 | 0.735 |
| 512|raw|minmax|sq+centroid_amp|svm | 0.000 | 0.020 | 0.350 | 0.760 |
| 512|hann|H|sq|svm | 0.000 | 0.010 | 0.305 | 0.800 |
| 512|hann|H|sq|threshold | 0.005 | 0.075 | 0.440 | 0.770 |
| 512|hann|H|centroid_amp|svm | 0.000 | 0.015 | 0.290 | 0.735 |
| 512|hann|H|centroid_amp|threshold | 0.000 | 0.055 | 0.445 | 0.730 |
| 512|hann|H|centroid_band_power|svm | 0.000 | 0.000 | 0.365 | 0.810 |
| 512|hann|H|centroid_band_power|threshold | 0.000 | 0.075 | 0.410 | 0.745 |
| 512|hann|H|sq+centroid_amp|svm | 0.000 | 0.005 | 0.380 | 0.765 |
| 512|hann|minmax|sq|svm | 0.000 | 0.020 | 0.315 | 0.825 |
| 512|hann|minmax|sq|threshold | 0.000 | 0.080 | 0.420 | 0.765 |
| 512|hann|minmax|centroid_amp|svm | 0.000 | 0.020 | 0.290 | 0.735 |
| 512|hann|minmax|centroid_amp|threshold | 0.000 | 0.055 | 0.445 | 0.730 |
| 512|hann|minmax|centroid_band_power|svm | 0.000 | 0.005 | 0.365 | 0.810 |
| 512|hann|minmax|centroid_band_power|threshold | 0.000 | 0.075 | 0.410 | 0.745 |
| 512|hann|minmax|sq+centroid_amp|svm | 0.000 | 0.030 | 0.345 | 0.755 |
