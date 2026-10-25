# K5: Table 1 frame (predictions entered before the experiment)

Conditions: `experiments/conditions/k5_classification.json` (SHA-256 `09a914161be116f44ab83f32277e5c48db3f304370f0f2bad59e5009b152d5e6`). Predictions: `experiments/conditions/k5_table1_predictions.json` (SHA-256 `6cf0f96992bd4acab004d03f66b0566c355f84f14eb8bf869709d9a33db7693b`). Specification: `experiments/spec/generator-and-descriptors.md` (SHA-256 `0ab265408e73e8a7b75e58f60df990ebd718db0f2b8b3b3c27d501bcdad096dc`). Script SHA-256 `f27dde51be04fa2b980c63c1d966984a9007a48e8c534d82c61dd859cd69bfed`. numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, Python 3.13.12. Run started 2026-10-25T17:21:28+00:00 and finished 2026-10-25T17:21:28+00:00 (Darwin arm64, 10 logical CPUs).

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

| condition | w | N | processing | representation | set | predicted direction | predicted order | predicted level |
|---|---|---|---|---|---|---|---|---|
| i_V | 0.1 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.1 | 128 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9908 |
| i_V | 0.1 | 128 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6860 |
| i_V | 0.1 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.1 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8455 |
| i_V | 0.1 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8) | 0.9908 |
| i_V | 0.1 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6860 |
| i_V | 0.1 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9940 |
| i_V | 0.1 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.1 | 128 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9833 |
| i_V | 0.1 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6840 |
| i_V | 0.1 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.1 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8454 |
| i_V | 0.1 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.9833 |
| i_V | 0.1 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6840 |
| i_V | 0.1 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9907 |
| i_V | 0.1 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.1 | 512 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9999 |
| i_V | 0.1 | 512 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6827 |
| i_V | 0.1 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.1 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8458 |
| i_V | 0.1 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8) | 0.9999 |
| i_V | 0.1 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6827 |
| i_V | 0.1 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9999 |
| i_V | 0.1 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.1 | 512 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9999 |
| i_V | 0.1 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6807 |
| i_V | 0.1 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.1 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8458 |
| i_V | 0.1 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.9999 |
| i_V | 0.1 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6807 |
| i_V | 0.1 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9999 |
| i_V | 0.3 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.3 | 128 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9725 |
| i_V | 0.3 | 128 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6835 |
| i_V | 0.3 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.3 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8366 |
| i_V | 0.3 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8) | 0.9725 |
| i_V | 0.3 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6835 |
| i_V | 0.3 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9786 |
| i_V | 0.3 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.3 | 128 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9628 |
| i_V | 0.3 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6809 |
| i_V | 0.3 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.3 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8367 |
| i_V | 0.3 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.9628 |
| i_V | 0.3 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6809 |
| i_V | 0.3 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9726 |
| i_V | 0.3 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.3 | 512 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9967 |
| i_V | 0.3 | 512 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6801 |
| i_V | 0.3 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.3 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8375 |
| i_V | 0.3 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8) | 0.9967 |
| i_V | 0.3 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6801 |
| i_V | 0.3 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9959 |
| i_V | 0.3 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 1.0000 |
| i_V | 0.3 | 512 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9957 |
| i_V | 0.3 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6784 |
| i_V | 0.3 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_V | 0.3 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8375 |
| i_V | 0.3 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.9957 |
| i_V | 0.3 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6784 |
| i_V | 0.3 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9945 |
| i_V | 0.5 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 0.9792 |
| i_V | 0.5 | 128 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9215 |
| i_V | 0.5 | 128 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6824 |
| i_V | 0.5 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9791 |
| i_V | 0.5 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8138 |
| i_V | 0.5 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8) | 0.9215 |
| i_V | 0.5 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6824 |
| i_V | 0.5 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9268 |
| i_V | 0.5 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 0.9792 |
| i_V | 0.5 | 128 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9122 |
| i_V | 0.5 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6811 |
| i_V | 0.5 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9796 |
| i_V | 0.5 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8140 |
| i_V | 0.5 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.9122 |
| i_V | 0.5 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6811 |
| i_V | 0.5 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9212 |
| i_V | 0.5 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 0.9792 |
| i_V | 0.5 | 512 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9520 |
| i_V | 0.5 | 512 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6797 |
| i_V | 0.5 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9786 |
| i_V | 0.5 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8144 |
| i_V | 0.5 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-11) | non-increasing in w (svm; P-K5-8) | 0.9520 |
| i_V | 0.5 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6797 |
| i_V | 0.5 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9461 |
| i_V | 0.5 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= C of the same cell (svm; P-K5-10) | 0.9792 |
| i_V | 0.5 | 512 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= S of the same cell (svm; P-K5-10) | 0.9512 |
| i_V | 0.5 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 0.6785 |
| i_V | 0.5 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9792 |
| i_V | 0.5 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-6) | non-increasing in w (svm; P-K5-8) | 0.8144 |
| i_V | 0.5 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.9512 |
| i_V | 0.5 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8) | 0.6785 |
| i_V | 0.5 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9433 |
| i_A | 0.1 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9671 |
| i_A | 0.1 | 128 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9798 |
| i_A | 0.1 | 128 | raw | H | B | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9942 |
| i_A | 0.1 | 128 | raw | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9749 |
| i_A | 0.1 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9798 |
| i_A | 0.1 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9975 |
| i_A | 0.1 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9693 |
| i_A | 0.1 | 128 | hann | H | C | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9999 |
| i_A | 0.1 | 128 | hann | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9759 |
| i_A | 0.1 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_A | 0.1 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9662 |
| i_A | 0.1 | 512 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9842 |
| i_A | 0.1 | 512 | raw | H | B | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9960 |
| i_A | 0.1 | 512 | raw | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9743 |
| i_A | 0.1 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9842 |
| i_A | 0.1 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9969 |
| i_A | 0.1 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9683 |
| i_A | 0.1 | 512 | hann | H | C | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_A | 0.1 | 512 | hann | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9759 |
| i_A | 0.1 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.1 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| i_A | 0.3 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9398 |
| i_A | 0.3 | 128 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9458 |
| i_A | 0.3 | 128 | raw | H | B | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9778 |
| i_A | 0.3 | 128 | raw | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9483 |
| i_A | 0.3 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9458 |
| i_A | 0.3 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9845 |
| i_A | 0.3 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9412 |
| i_A | 0.3 | 128 | hann | H | C | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9984 |
| i_A | 0.3 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9985 |
| i_A | 0.3 | 128 | hann | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9493 |
| i_A | 0.3 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9984 |
| i_A | 0.3 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9997 |
| i_A | 0.3 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9417 |
| i_A | 0.3 | 512 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9722 |
| i_A | 0.3 | 512 | raw | H | B | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9842 |
| i_A | 0.3 | 512 | raw | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9492 |
| i_A | 0.3 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9722 |
| i_A | 0.3 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9864 |
| i_A | 0.3 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9422 |
| i_A | 0.3 | 512 | hann | H | C | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9952 |
| i_A | 0.3 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9947 |
| i_A | 0.3 | 512 | hann | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9514 |
| i_A | 0.3 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9952 |
| i_A | 0.3 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| i_A | 0.3 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9955 |
| i_A | 0.5 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.8960 |
| i_A | 0.5 | 128 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.8989 |
| i_A | 0.5 | 128 | raw | H | B | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9621 |
| i_A | 0.5 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9212 |
| i_A | 0.5 | 128 | raw | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.8995 |
| i_A | 0.5 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.8989 |
| i_A | 0.5 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9621 |
| i_A | 0.5 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9254 |
| i_A | 0.5 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.8949 |
| i_A | 0.5 | 128 | hann | H | C | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9549 |
| i_A | 0.5 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9885 |
| i_A | 0.5 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9575 |
| i_A | 0.5 | 128 | hann | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.8999 |
| i_A | 0.5 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9549 |
| i_A | 0.5 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9885 |
| i_A | 0.5 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9646 |
| i_A | 0.5 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.8958 |
| i_A | 0.5 | 512 | raw | H | C | above chance (svm; P-K5-12); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9285 |
| i_A | 0.5 | 512 | raw | H | B | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9621 |
| i_A | 0.5 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9316 |
| i_A | 0.5 | 512 | raw | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.8996 |
| i_A | 0.5 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); N = 512 >= N = 128 (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9285 |
| i_A | 0.5 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9621 |
| i_A | 0.5 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9361 |
| i_A | 0.5 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.8952 |
| i_A | 0.5 | 512 | hann | H | C | above chance (svm; P-K5-12); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9452 |
| i_A | 0.5 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9884 |
| i_A | 0.5 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9490 |
| i_A | 0.5 | 512 | hann | minmax | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.9005 |
| i_A | 0.5 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); change between N = 128 and 512 smaller than for raw C (P-K5-2) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9452 |
| i_A | 0.5 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9884 |
| i_A | 0.5 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9536 |
| ii_s | 0.1 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | raw | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | raw | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.1 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.1 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | hann | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | hann | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.1 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 128 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.1 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | raw | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | raw | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.1 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.1 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | hann | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | hann | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.1 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.1 | 512 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | raw | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | raw | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | hann | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | hann | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 128 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | raw | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | raw | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | hann | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | hann | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.3 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.3 | 512 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | raw | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | raw | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | hann | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | hann | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 128 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | raw | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | raw | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | hann | H | C | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | hann | H | B | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s | 0.5 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of corners (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s | 0.5 | 512 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of corners (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | raw | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); < S of i_V, i_A, ii_s and corners in the same column (svm; P-K5-9); <= C and B of the same cell (svm; P-K5-10) | 0.5035 |
| ii_s_gamma | 0.1 | 128 | raw | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9648 |
| ii_s_gamma | 0.1 | 128 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9357 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5048 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9648 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.9357 |
| ii_s_gamma | 0.1 | 128 | hann | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5026 |
| ii_s_gamma | 0.1 | 128 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5025 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | raw | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); < S of i_V, i_A, ii_s and corners in the same column (svm; P-K5-9); <= C and B of the same cell (svm; P-K5-10) | 0.5029 |
| ii_s_gamma | 0.1 | 512 | raw | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.7665 |
| ii_s_gamma | 0.1 | 512 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.5262 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5037 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.7665 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.5263 |
| ii_s_gamma | 0.1 | 512 | hann | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5010 |
| ii_s_gamma | 0.1 | 512 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5011 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.1 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | raw | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); < S of i_V, i_A, ii_s and corners in the same column (svm; P-K5-9); <= C and B of the same cell (svm; P-K5-10) | 0.5049 |
| ii_s_gamma | 0.3 | 128 | raw | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9324 |
| ii_s_gamma | 0.3 | 128 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.8905 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5037 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9324 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.8905 |
| ii_s_gamma | 0.3 | 128 | hann | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5028 |
| ii_s_gamma | 0.3 | 128 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5044 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | raw | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); < S of i_V, i_A, ii_s and corners in the same column (svm; P-K5-9); <= C and B of the same cell (svm; P-K5-10) | 0.5043 |
| ii_s_gamma | 0.3 | 512 | raw | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.7604 |
| ii_s_gamma | 0.3 | 512 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.5139 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5033 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.7604 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.5139 |
| ii_s_gamma | 0.3 | 512 | hann | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5009 |
| ii_s_gamma | 0.3 | 512 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5012 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.3 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | raw | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); < S of i_V, i_A, ii_s and corners in the same column (svm; P-K5-9); <= C and B of the same cell (svm; P-K5-10) | 0.5040 |
| ii_s_gamma | 0.5 | 128 | raw | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9027 |
| ii_s_gamma | 0.5 | 128 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.8388 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5047 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.9027 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.8388 |
| ii_s_gamma | 0.5 | 128 | hann | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5041 |
| ii_s_gamma | 0.5 | 128 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5042 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 128 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | raw | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); < S of i_V, i_A, ii_s and corners in the same column (svm; P-K5-9); <= C and B of the same cell (svm; P-K5-10) | 0.5043 |
| ii_s_gamma | 0.5 | 512 | raw | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.7587 |
| ii_s_gamma | 0.5 | 512 | raw | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.5106 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5039 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 0.7587 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | raw | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 0.5106 |
| ii_s_gamma | 0.5 | 512 | hann | H | S | no direction relative to chance (P-K5-9) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5009 |
| ii_s_gamma | 0.5 | 512 | hann | H | C | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | hann | H | B | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | S | no direction relative to chance (P-K5-9); <= the same row on H (P-K5-1) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 0.5009 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| ii_s_gamma | 0.5 | 512 | hann | minmax | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | raw | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | raw | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 128 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | hann | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | hann | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 128 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | raw | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | raw | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 512 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | hann | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | hann | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.1 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.1 | 512 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | raw | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | raw | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 128 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | hann | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | hann | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 128 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | raw | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | raw | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 512 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | hann | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | hann | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.3 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.3 | 512 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | raw | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | raw | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 128 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 128 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 128 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | hann | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | hann | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 128 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 128 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 128 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 128 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | raw | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | raw | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | raw | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | raw | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | raw | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 512 | raw | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 512 | raw | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 512 | raw | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | hann | H | S | above chance (svm; P-K5-12) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | hann | H | C | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | hann | H | B | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | hann | H | SC | above chance (svm; P-K5-12) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| corners | 0.5 | 512 | hann | minmax | S | above chance (svm; P-K5-12); <= the same row on H (P-K5-1); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); <= C and B of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 512 | hann | minmax | C | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 512 | hann | minmax | B | above chance (svm; P-K5-12); = the same row on H (P-K5-4); = the same row of ii_s (P-K5-5) | non-increasing in w (svm; P-K5-8); >= S of the same cell (svm; P-K5-10) | 1.0000 |
| corners | 0.5 | 512 | hann | minmax | SC | above chance (svm; P-K5-12); = the same row of ii_s (P-K5-5) | >= max(S, C) of the same cell (svm; P-K5-7); non-increasing in w (svm; P-K5-8) | 1.0000 |
| iii_null | - | 128 | raw | H | S | at chance by the TOST (P-K5-3) | none | 0.5079 |
| iii_null | - | 128 | raw | H | C | at chance by the TOST (P-K5-3) | none | 0.5073 |
| iii_null | - | 128 | raw | H | B | at chance by the TOST (P-K5-3) | none | 0.5046 |
| iii_null | - | 128 | raw | H | SC | at chance by the TOST (P-K5-3) | none | 0.5040 |
| iii_null | - | 128 | raw | minmax | S | at chance by the TOST (P-K5-3) | none | 0.5070 |
| iii_null | - | 128 | raw | minmax | C | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5073 |
| iii_null | - | 128 | raw | minmax | B | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5046 |
| iii_null | - | 128 | raw | minmax | SC | at chance by the TOST (P-K5-3) | none | 0.4976 |
| iii_null | - | 128 | hann | H | S | at chance by the TOST (P-K5-3) | none | 0.5079 |
| iii_null | - | 128 | hann | H | C | at chance by the TOST (P-K5-3) | none | 0.5068 |
| iii_null | - | 128 | hann | H | B | at chance by the TOST (P-K5-3) | none | 0.5048 |
| iii_null | - | 128 | hann | H | SC | at chance by the TOST (P-K5-3) | none | 0.4996 |
| iii_null | - | 128 | hann | minmax | S | at chance by the TOST (P-K5-3) | none | 0.5070 |
| iii_null | - | 128 | hann | minmax | C | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5068 |
| iii_null | - | 128 | hann | minmax | B | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5048 |
| iii_null | - | 128 | hann | minmax | SC | at chance by the TOST (P-K5-3) | none | 0.4959 |
| iii_null | - | 512 | raw | H | S | at chance by the TOST (P-K5-3) | none | 0.5079 |
| iii_null | - | 512 | raw | H | C | at chance by the TOST (P-K5-3) | none | 0.5067 |
| iii_null | - | 512 | raw | H | B | at chance by the TOST (P-K5-3) | none | 0.5048 |
| iii_null | - | 512 | raw | H | SC | at chance by the TOST (P-K5-3) | none | 0.5036 |
| iii_null | - | 512 | raw | minmax | S | at chance by the TOST (P-K5-3) | none | 0.5061 |
| iii_null | - | 512 | raw | minmax | C | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5067 |
| iii_null | - | 512 | raw | minmax | B | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5048 |
| iii_null | - | 512 | raw | minmax | SC | at chance by the TOST (P-K5-3) | none | 0.4972 |
| iii_null | - | 512 | hann | H | S | at chance by the TOST (P-K5-3) | none | 0.5079 |
| iii_null | - | 512 | hann | H | C | at chance by the TOST (P-K5-3) | none | 0.5065 |
| iii_null | - | 512 | hann | H | B | at chance by the TOST (P-K5-3) | none | 0.5047 |
| iii_null | - | 512 | hann | H | SC | at chance by the TOST (P-K5-3) | none | 0.5030 |
| iii_null | - | 512 | hann | minmax | S | at chance by the TOST (P-K5-3) | none | 0.5061 |
| iii_null | - | 512 | hann | minmax | C | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5065 |
| iii_null | - | 512 | hann | minmax | B | at chance by the TOST (P-K5-3); = the same row on H (P-K5-4) | none | 0.5047 |
| iii_null | - | 512 | hann | minmax | SC | at chance by the TOST (P-K5-3) | none | 0.4951 |
| check_same_seed | - | 128 | raw | H | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | raw | H | C | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | raw | H | B | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | raw | H | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | raw | minmax | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | raw | minmax | C | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 128 | raw | minmax | B | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 128 | raw | minmax | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | hann | H | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | hann | H | C | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | hann | H | B | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | hann | H | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | hann | minmax | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 128 | hann | minmax | C | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 128 | hann | minmax | B | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 128 | hann | minmax | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | raw | H | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | raw | H | C | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | raw | H | B | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | raw | H | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | raw | minmax | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | raw | minmax | C | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 512 | raw | minmax | B | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 512 | raw | minmax | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | hann | H | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | hann | H | C | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | hann | H | B | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | hann | H | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | hann | minmax | S | exactly 0.5 (P-K5-3) | none | 0.5000 |
| check_same_seed | - | 512 | hann | minmax | C | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 512 | hann | minmax | B | exactly 0.5 (P-K5-3); = the same row on H (P-K5-4) | none | 0.5000 |
| check_same_seed | - | 512 | hann | minmax | SC | exactly 0.5 (P-K5-3) | none | 0.5000 |
