# Canonical generator and descriptors (specification, version 1)

This document fixes the generator, the descriptors and the processing steps used for every computation in the paper (K4 in two dimensions, the paired edge-and-grid comparison, validation 3 on public data, and K5). It was written before those computations were run. The code in `src/atact/` implements it, and `tests/test_spec.py` checks each numbered clause against the code. If the code and this document disagree, the document is the specification and the code is a bug, unless a later version of this document says otherwise.

A Japanese version for checking is `generator-and-descriptors.ja.md`. The English version is authoritative.

## S1. Procedural field

S1.1 Domain and grid. The domain is the unit square. A grid of side N has points x_i = x0 + i/N and y_j = y0 + j/N for i, j = 0, ..., N − 1. The default window is (x0, y0) = (0, 0). Shifting (x0, y0) gives a different window on the same infinite field (used for crops).

S1.2 Field. F_raw(x, y) = Σ_{o=0}^{O−1} 2^{−o} sin(2π 2^o f x + φ_o) sin(2π 2^o f y + ψ_o), with O = 4 octaves. Frequencies are in cycles per domain. The array is indexed [j, i] (row = y).

S1.3 Phases. The generator is `numpy.random.default_rng(seed)`. For o = 0, ..., O − 1, in this order, it draws two numbers uniform on [0, 2π): first φ_o, then ψ_o. No other draws happen in the canonical generator.

S1.4 Normalisation. Canonical: F = F_raw / max over the grid of |F_raw| ("maxabs"). Variant "ampsum": F = F_raw / Σ_o 2^{−o}, a constant, so that the same surface is obtained for every window and every grid. Experiments that compare windows or grids of the same surface use "ampsum". The centroid (S2.3) does not depend on this choice, because T_γ is homogeneous and the centroid is a ratio.

S1.5 Warp. The canonical generator has no domain warp. A warp, when used as a variant, is the one in `atact.field` (assumption A3 of the repository README).

S1.6 Periodicity. F is periodic on the domain if and only if f is an integer (all octaves then complete whole periods). For non-integer f the field jumps at the domain edge. "Periodised" in K4 means using an integer f; it is not a processing step.

## S2. Height and descriptors

S2.1 Rule. (f, s, γ) come from (V, A) by equations (1)–(3) of the preprint (`atact.mapping.params`): p = (A + 1)/2, q = (1 − V)/2, f = 3 + 4p, s = 0.06 + 0.24q, γ = 0.9 + 1.7(0.65p + 0.35q), with V and A clipped to [−1, 1].

S2.2 Height. H = s T_γ(F) with T_γ(u) = sign(u) |u|^{1/γ}. The smoothed variant is T_{γ,ε}(u) = u (u² + ε²)^k / (1 + ε²)^k, k = (1/γ − 1)/2. Descriptors are computed on H − mean(H).

S2.3 Amplitude-weighted centroid (canonical, "centroid"). C = Σ_k ρ_k |Ĥ_k| / Σ_k |Ĥ_k|, where Ĥ is the 2-D DFT of H − mean(H), the sum runs over all N² bins, each component of k takes the values of `numpy.fft.fftfreq(N) * N` (that is, the integers in [−N/2, N/2)), and ρ_k = |k| (Euclidean) in cycles per domain. The DC bin has ρ = 0 and Ĥ_0 = 0, so it adds nothing.

S2.4 Power-weighted and band-fixed centroids. Power-weighted: replace |Ĥ| by |Ĥ|² in S2.3. Band-fixed: restrict both sums to bins with 0 < ρ_k ≤ K, where K is fixed in cycles per domain (physical units) and K ≤ N/2. Both amplitude and power weights are allowed; the weight is part of the condition.

S2.5 Sq. Sq = sqrt(mean((H − mean H)²)).

S2.6 Maximum gradient. max over the grid of |∇H| with `numpy.gradient(H, 1/N)` (central differences inside, one-sided at the edge).

S2.7 One-dimensional centroid. For a profile z of length N: Σ |k| |ẑ_k| / Σ |ẑ_k| over all bins (`atact.descriptors.centroid_1d`). Used for the 1-D row of figure 4.

S2.8 Normal map from a height. Given a height z in the same length unit as the side L of the domain, the slopes are `numpy.gradient(z, L/N)` (central differences, one-sided at the edge, no periodicity assumed), the normal is (−∂z/∂x, ∂z/∂y, 1) normalised (OpenGL convention), and it is stored as uint8 RGB by round((n + 1)/2 · 255) (`atact.hfratio.normal_rgb_from_height`).

S2.9 HF ratio. The HF ratio of Gao et al. (2026), copied from the authors' public code without running it (`atact.hfratio.hf_ratio`; source files and retrieval date are in that module). Its input is a uint8 normal map. Its cutoff `freq_threshold` is in pixels; the default is 120. Two cutoff rules are used: "px" (freq_threshold = 120 regardless of N) and "phys" (freq_threshold = 120 N / N_ref, which fixes the cutoff in cycles per domain; N_ref is stated in each condition file). Float variant (a control, not part of the original metric): the same computation on floating-point normals in [-1, 1] without the uint8 rounding of the input and of the filtered map (`atact.hfratio.hf_ratio_float`). Linear height variant (a control in the setting of Proposition 8, part 3): the energy of z − mean(z) after multiplying its DFT by the same Gaussian high-pass weight, divided by the energy of z − mean(z) without the DC bin (`atact.spectral.linear_hf_ratio`).

## S3. Edge treatments (for comparison only)

None of these gives the "true" value; each changes the surface in its own way.

S3.1 Window. W(i, j) = sin²(π i/N) sin²(π j/N). The windowed height is X = (H − mean H) W, then X − mean X. Descriptors are then computed on X as in S2. For normal maps, the same W is applied to each component's deviation from its mean, the vector is renormalised and re-encoded as uint8 (`atact.spectral.windowed_normals`). The preliminary experiment `experiments/hf_ratio_edge.py` used the symmetric `numpy.hanning` window instead; this specification replaces it with W.

S3.2 Periodic plus smooth decomposition (Moisan 2011). H = p + s, where s solves the discrete Poisson equation with the edge-difference image as source and has mean zero (`atact.spectral.periodic_component`). Descriptors are computed on p.

S3.3 Band fixing is S2.4 with K in cycles per domain.

## S4. Aliasing separation

S4.1 The height H (after T_γ) is generated on a fine grid of side M = rN with the same window and seed, then reduced to side N by an ideal low-pass that keeps the bins whose components lie in [−N/2, N/2), with the factor (N/M)², followed by the inverse DFT (`atact.spectral.decimate_fourier`). The descriptor of this array is compared with the descriptor of the field sampled directly at side N. The transform treats the fine array as periodic; for non-integer f the low-pass therefore also acts on the edge discontinuity, which is reported and not corrected.

S4.2 The primary reference uses a fixed r = 2 for every N, so that the reference does not change with N. As a convergence check, r = 4 is also used for N ≤ 2048, and the difference between r = 2 and r = 4 is reported as residual aliasing of the reference. r = 4 is not used at N = 4096 because of memory (a 16384² double array and its transform), not because of any result.

S4.3 Plain subsampling without low-pass (`atact.spectral.subsample`) is the control that keeps aliasing.

## S5. Measured data

S5.1 Surface-Topography Challenge (Zenodo 10.5281/zenodo.15341939, CC0 at the record level). The height array is the variable `heights` of the `-squeezed.nc` file in each digital surface twin (NetCDF 3, read with `scipy.io.netcdf_file`). Units are converted to metres using the variable's `unit` attribute. The physical side lengths come from the `length` attribute of `x` and `y`.

S5.2 Square crop. The central P × P block, where P is the largest power of two not exceeding the smaller array dimension. After cropping, the least-squares plane is removed (`atact.spectral.remove_plane`). The physical side is L = P × pixel spacing.

S5.3 Grid levels. From the P × P crop, sides P/2 and P/4 are made by `decimate_fourier` (S4.1) and, as a control, by `subsample` (S4.3). The physical domain is the same at all levels.

S5.4 TactileDreamFusion (Hugging Face `Ruihan28/TactileDreamFusion`, revision 87c8b764bcb2ec1139de0c6435f45ac1d9f283d1, MIT). Inputs are the normal maps `normal_patch.png` (240 × 240; the alpha channel is dropped) and the central 1024 × 1024 block of `tiled_normal_map.png`. A normal map is decoded as n = rgb/255 · 2 − 1. Grid levels are made per component with `decimate_fourier` (sides divisible as needed: patch 240 → 120 → 60; tiled 1024 → 512 → 256), then renormalised and re-encoded as uint8 (S2.8). The pixel size is not stated by the dataset, so only the "px" and "phys" rules relative to the crop are used, not metres.

## S6. Statistics shared by the condition files

S6.1 Growth exponent. For each seed, the exponent is the least-squares slope of ln C on ln N over the N values named in the condition. The point estimate is the mean over seeds; the 95% interval is the t interval over seeds (n − 1 degrees of freedom). When a decision is taken over several cells, simultaneous intervals are used (Bonferroni: level 1 − 0.05/m for m cells), as stated in the condition file.

S6.2 Order between two surfaces. For descriptor D and grid level g, the order of surfaces a and b is sign(D_a(g) − D_b(g)) averaged over seeds or crops as stated in the condition. A flip between levels g and g′ is a pair whose sign differs and whose mean difference at both levels exceeds twice its standard error. For measured data without seeds the condition file gives a relative-difference threshold instead. Kendall's τ between the rankings at two levels is also reported.

S6.3 Environment. Package versions are fixed by `uv.lock`. Each results file records the SHA-256 of its condition file and of this document, and the numpy version.

## Correspondence

| Clause | Code | Test |
|---|---|---|
| S1.1–S1.4 | `atact.field.procedural_field`, `RenderConfig` (`x0`, `y0`, `normalize`) | `test_spec.py::test_s1_*` |
| S1.6 | — | `test_spec.py::test_s1_6_periodic_iff_integer_f` |
| S2.1–S2.2 | `atact.mapping.params`, `atact.field.height`, `atact.transform` | `test_spec.py::test_s2_2_*`, `test_math.py` |
| S2.3–S2.7 | `atact.descriptors`, `atact.spectral.centroid_band` | `test_spec.py::test_s2_*` |
| S2.8–S2.9 | `atact.hfratio` (`hf_ratio`, `hf_ratio_float`), `atact.spectral.linear_hf_ratio` | `test_hfratio.py`, `test_spec.py::test_s2_9_*` |
| S3 | `atact.spectral` | `test_spec.py::test_s3_*` |
| S4 | `atact.spectral.decimate_fourier`, `subsample` | `test_spec.py::test_s4_*` |
| S5 | `atact.spectral.remove_plane` (readers are in the experiment scripts) | `test_spec.py::test_s5_*` |
