# Table 2: checks for a rule of the type of Section 2, and the decisions left to the artist

Written by hand from Propositions 1-8 (`advice/planA-math.md`, revision 2) and the registered results cited in the
last column. Basis: "type" = a proposition that holds for every rule of the type (an affine map to the parameters of a
procedural field, a signed power, an export and descriptors), under the condition stated; "field" = a result for the field of Section 2, proved in
one dimension and computed in two. The column "In this rule" is for the rule read in the paper; the checks have not been
tried on other rules. (Revised 2026-10-26 after the pre-review of the manuscript: basis column added, row 4 restated. Revised again after the
second round: rows 2 and 5 have basis "type", row 4 names the type proposition for the band and limits the edge
statement to gamma <= 1.25, where the raw slopes for non-integer f exceed those for integer f in results cb369b4,
P-K4-6 table; at gamma = 1.75 and 2.6 they do not. Third revision: the steepest slope of 61 degrees is the value at
N = 4096; the grid independence of the band-fixed centroid is exact here only at gamma = 1 and integer f.)

## Checks

| # | Check | What to compute | Basis | In this rule | Source |
|---|---|---|---|---|---|
| 1 | Rank of the map from the input to the parameters | rank of the Jacobian M of (V, A) -> (f, s, gamma); the image of the input square | type | rank 2: the image is a parallelogram in the plane gamma = 0.9 + 0.27625 (f - 3) + 2.479 (s - 0.06); three parameters, two degrees of freedom | Proposition 1; Fig. 1 |
| 2 | Normalisation before the shaping transform | whether the transform is homogeneous, and what the normalisation of the field changes | type | T_gamma is homogeneous of degree 1/gamma, so after max-normalisation the shape does not depend on the scale of F; the normalisation acts on the amplitude only | Proposition 2 (5) |
| 3 | Quantities removed by the export | the export written as a map, and which parameters it cancels | type | the per-image min-max export cancels s exactly (the min-max tiles of the text example agree with the min-max of T_gamma(F), computed without s, to 5.6e-16); V then acts only through gamma. A common height scale keeps s | Proposition 4; Fig. 2; results ad02721 (P-T1) |
| 4 | Dependence of a descriptor on the grid and on the edge of the domain | the descriptor at several N; integer and non-integer f; with and without a window | field (the centroid theorem in one dimension, Conjecture 1 in two); type for the band (the proposition on descriptors that do not depend on the grid) | the amplitude-weighted centroid grows with N on the sum field at the four values gamma != 1 computed, also at gamma = 0.9 (slopes 0.29-0.91 over N 512-4096, f = 3, 5, 7), and at gamma <= 1.25 faster for non-integer f because of the edge jump; a power weight with a fixed band reduces both, and is independent of the grid for a band-limited periodic surface (here only at gamma = 1 and integer f) | Propositions 5 and 7; Fig. 4; results cb369b4 and 32e2ffe |
| 5 | Largest slope | the maximum gradient at several N | type, at a transversal zero | grows like N^(1 - 1/gamma) for gamma > 1 (slopes 0.425 and 0.606 over N 512-4096, against 0.429 and 0.615); under T_{gamma,eps} it stops changing once the grid resolves the smoothed band (1.9% between N = 1024 and 4096 for eps = 0.353; still growing for eps = 0.044) | Proposition 6; Fig. 3; results 59c213e |
| 6 | Degrees of freedom that can be observed | the minimum over the stages of the rank: inputs, the map, the export, the descriptors | type | at most 2 after the min-max export; with a hypothetical third input, rank 3 on H and 2 after the export | Proposition 4 (corollary); results 0f320bc |

## Left to the artist

| Decision | Why it is not fixed by the rule | In this paper |
|---|---|---|
| The common height scale (depth D and the largest amplitude s_max) | the min-max export removes the amplitude; only a scale shared by all works keeps it | D = 1.2 mm for s_max = 0.30 in the example |
| eps of T_{gamma,eps} | for gamma > 1 the largest slope of T_gamma has no grid-independent value; eps sets it, and with it how much of the shape near the zero lines is changed | tied to the smallest printable feature in the example: eps = 0.353 for a 50 mm tile and a 0.4 mm nozzle, a steepest slope of 61 degrees at N = 4096 instead of 59-86 degrees (N = 128-4096), and a height change of at most 0.13 mm on a relief that spans 1.02-1.11 mm |
| The band and the weight of a spectral descriptor | the amplitude-weighted centroid over the full band measures the grid and the edge as well as f; the band decides which octaves count | the power-weighted centroid with a fixed band (K = 32 cycles per domain) |
