# Table 1, main-text version (K5)

Extracted from `results/k5_classification.json` (SHA-256 `a96c475bae36c43a71aa5b2bc9660cce530da628648afe6f8a7899c9f8cde653`, commit 3f58861) by `experiments/table1_main.py` (SHA-256 `0cd1742df4dc85b48de932bf42954a5644ce477bd693cb4cc6b8f47efe9b272a`). No new computation. Slice: N = 128, processing raw, w = 0.3 (the null conditions have no w). The full table of 544 rows is in `results/k5_classification.md`.

Predictions are numbered as in `experiments/conditions/k5_table1_predictions.json`; an asterisk marks a prediction that does not hold in this cell (evaluated from the stored accuracies with the criterion of that prediction restricted to this cell). Level: large-sample level of the frame. Intervals: 95% pair bootstrap.

| condition | repr | set | predictions | level | svm | 95% CI svm | threshold | 95% CI threshold |
|---|---|---|---|---|---|---|---|---|
| i_V | H | S | 12, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| i_V | H | C | 12, 11, 8, 10 | 0.973 | 0.969 | [0.957, 0.979] | 0.967 | [0.955, 0.977] |
| i_V | H | B | 12, 8* | 0.683 | 0.686 | [0.665, 0.708] | 0.689 | [0.668, 0.711] |
| i_V | H | SC | 12, 7, 8 | 1.000 | 1.000 | [1.000, 1.000] | - | - |
| i_V | minmax | S | 12, 6, 8 | 0.837 | 0.838 | [0.817, 0.858] | 0.836 | [0.816, 0.857] |
| i_V | minmax | C | 12, 4, 11, 8 | 0.973 | 0.969 | [0.957, 0.979] | 0.967 | [0.955, 0.977] |
| i_V | minmax | B | 12, 4, 8* | 0.683 | 0.686 | [0.665, 0.708] | 0.689 | [0.668, 0.711] |
| i_V | minmax | SC | 12, 7, 8 | 0.979 | 0.976 | [0.966, 0.985] | - | - |
| i_A | H | S | 12, 8, 10 | 0.940 | 0.929 | [0.914, 0.945] | 0.928 | [0.914, 0.944] |
| i_A | H | C | 12, 2, 8, 10 | 0.946 | 0.951 | [0.936, 0.964] | 0.950 | [0.935, 0.963] |
| i_A | H | B | 12, 2, 8, 10 | 1.000 | 0.998 | [0.995, 1.000] | 1.000 | [1.000, 1.000] |
| i_A | H | SC | 12, 7, 8 | 0.978 | 0.972 | [0.961, 0.981] | - | - |
| i_A | minmax | S | 12, 8, 10 | 0.948 | 0.944 | [0.929, 0.957] | 0.942 | [0.926, 0.955] |
| i_A | minmax | C | 12, 4, 2, 8, 10 | 0.946 | 0.951 | [0.936, 0.964] | 0.950 | [0.935, 0.963] |
| i_A | minmax | B | 12, 4, 2, 8, 10 | 1.000 | 0.998 | [0.995, 1.000] | 1.000 | [1.000, 1.000] |
| i_A | minmax | SC | 12, 7, 8 | 0.985 | 0.978 | [0.969, 0.986] | - | - |
| ii_s | H | S | 12, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s | H | C | 12, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s | H | B | 12, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s | H | SC | 12, 7, 8 | 1.000 | 1.000 | [1.000, 1.000] | - | - |
| ii_s | minmax | S | 12, 1, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s | minmax | C | 12, 4, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s | minmax | B | 12, 4, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s | minmax | SC | 12, 5, 7, 8 | 1.000 | 1.000 | [1.000, 1.000] | - | - |
| ii_s_gamma | H | S | 9, 8*, 10 | 0.505 | 0.498 | [0.492, 0.504] | 0.508 | [0.502, 0.515] |
| ii_s_gamma | H | C | 12, 8, 10 | 0.932 | 0.881 | [0.863, 0.900] | 0.934 | [0.919, 0.949] |
| ii_s_gamma | H | B | 12, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s_gamma | H | SC | 12, 7, 8 | 0.890 | 0.881 | [0.863, 0.900] | - | - |
| ii_s_gamma | minmax | S | 9, 1*, 8*, 10 | 0.504 | 0.506 | [0.498, 0.516] | 0.496 | [0.486, 0.505] |
| ii_s_gamma | minmax | C | 12, 4, 8, 10 | 0.932 | 0.881 | [0.863, 0.900] | 0.934 | [0.919, 0.949] |
| ii_s_gamma | minmax | B | 12, 4, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| ii_s_gamma | minmax | SC | 12, 7, 8 | 0.890 | 0.881 | [0.863, 0.900] | - | - |
| corners | H | S | 12, 8 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| corners | H | C | 12, 5, 8 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| corners | H | B | 12, 5, 8 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| corners | H | SC | 12, 7, 8 | 1.000 | 1.000 | [1.000, 1.000] | - | - |
| corners | minmax | S | 12, 1, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| corners | minmax | C | 12, 4, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| corners | minmax | B | 12, 4, 5, 8, 10 | 1.000 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| corners | minmax | SC | 12, 5, 7, 8 | 1.000 | 1.000 | [1.000, 1.000] | - | - |
| iii_null | H | S | 3 | 0.508 | 0.476 | [0.450, 0.503] | 0.480 | [0.450, 0.511] |
| iii_null | H | C | 3* | 0.507 | 0.481 | [0.449, 0.512] | 0.461 | [0.432, 0.490] |
| iii_null | H | B | 3* | 0.505 | 0.479 | [0.450, 0.508] | 0.472 | [0.444, 0.500] |
| iii_null | H | SC | 3 | 0.504 | 0.483 | [0.453, 0.512] | - | - |
| iii_null | minmax | S | 3 | 0.507 | 0.485 | [0.457, 0.513] | 0.514 | [0.489, 0.540] |
| iii_null | minmax | C | 3*, 4 | 0.507 | 0.481 | [0.449, 0.512] | 0.461 | [0.432, 0.490] |
| iii_null | minmax | B | 3*, 4 | 0.505 | 0.479 | [0.450, 0.508] | 0.472 | [0.444, 0.500] |
| iii_null | minmax | SC | 3 | 0.498 | 0.489 | [0.461, 0.516] | - | - |
| check_same_seed | H | S | 3 | 0.500 | 0.500 | [0.500, 0.500] | 0.500 | [0.500, 0.500] |
| check_same_seed | H | C | 3 | 0.500 | 0.500 | [0.500, 0.500] | 0.500 | [0.500, 0.500] |
| check_same_seed | H | B | 3 | 0.500 | 0.500 | [0.500, 0.500] | 0.500 | [0.500, 0.500] |
| check_same_seed | H | SC | 3 | 0.500 | 0.500 | [0.500, 0.500] | - | - |
| check_same_seed | minmax | S | 3 | 0.500 | 0.500 | [0.500, 0.500] | 0.500 | [0.500, 0.500] |
| check_same_seed | minmax | C | 3, 4 | 0.500 | 0.500 | [0.500, 0.500] | 0.500 | [0.500, 0.500] |
| check_same_seed | minmax | B | 3, 4 | 0.500 | 0.500 | [0.500, 0.500] | 0.500 | [0.500, 0.500] |
| check_same_seed | minmax | SC | 3 | 0.500 | 0.500 | [0.500, 0.500] | - | - |

## Predictions that do not hold in a cell of this slice

- i_V, H, B: non-increasing in w (svm; P-K5-8)
- i_V, minmax, B: non-increasing in w (svm; P-K5-8)
- ii_s_gamma, H, S: non-increasing in w (svm; P-K5-8)
- ii_s_gamma, minmax, S: <= the same row on H (P-K5-1)
- ii_s_gamma, minmax, S: non-increasing in w (svm; P-K5-8)
- iii_null, H, C: at chance by the TOST (P-K5-3)
- iii_null, H, B: at chance by the TOST (P-K5-3)
- iii_null, minmax, C: at chance by the TOST (P-K5-3)
- iii_null, minmax, B: at chance by the TOST (P-K5-3)

## Wording of the predictions in this slice

- P-K5-1: <= the same row on H (P-K5-1)
- P-K5-2: N = 512 >= N = 128 (P-K5-2)
- P-K5-2: change between N = 128 and 512 smaller than for raw C (P-K5-2)
- P-K5-3: at chance by the TOST (P-K5-3)
- P-K5-3: exactly 0.5 (P-K5-3)
- P-K5-4: = the same row on H (P-K5-4)
- P-K5-5: = the same row of corners (P-K5-5)
- P-K5-5: = the same row of ii_s (P-K5-5)
- P-K5-6: <= the same row on H (P-K5-6)
- P-K5-7: >= max(S, C) of the same cell (svm; P-K5-7)
- P-K5-8: non-increasing in w (svm; P-K5-8)
- P-K5-9: < S of i_V, i_A, ii_s and corners in the same column (svm; P-K5-9)
- P-K5-9: no direction relative to chance (P-K5-9)
- P-K5-10: <= C and B of the same cell (svm; P-K5-10)
- P-K5-10: <= S of the same cell (svm; P-K5-10)
- P-K5-10: >= C of the same cell (svm; P-K5-10)
- P-K5-10: >= S of the same cell (svm; P-K5-10)
- P-K5-11: N = 512 >= N = 128 (P-K5-11)
- P-K5-12: above chance (svm; P-K5-12)
