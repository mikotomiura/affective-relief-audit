"""Values reported in Harada (2026) (revised manuscript, Section 4.3 and Tables 1-3), kept as the reference for comparison.

These are the reported numbers, not numbers reproduced here.
"""

# Table 3: stratified 5-fold cross-validation repeated 20 times (mean, standard deviation). Stored as proportions
TABLE3 = {
    "rq": (0.916, 0.049),
    "centroid": (0.742, 0.085),
    "both": (0.921, 0.048),
    "permuted": (0.500, 0.095),
}

# One 75/25 split: 29 of 30 correct (Section 4.3)
HOLDOUT = {"accuracy": 0.967, "n_test": 30, "n_correct": 29}

# Table 2
TABLE2 = {
    "n": 128,
    "octaves": 4,
    "warp": 0.25,
    "seed": 42,
    "per_class": 60,
    "f_range": (3.0, 7.0),
    "s_range": (0.06, 0.30),
    "gamma_range": (0.9, 2.6),
}

# The three panels of Fig. 3 (coordinates are not given in the text)
FIG3_PANELS = ("calm", "anger", "complex")
