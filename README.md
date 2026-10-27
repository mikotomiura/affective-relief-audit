<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/media/logo-dark.png">
    <img alt="affective-relief-audit" src="docs/media/logo-light.png" width="720">
  </picture>
</p>

<p align="center"><b>English</b> | <a href="README.ja.md">日本語</a></p>

This repository accompanies the paper *A generative rule from affect to tactile relief: what it decides, what its
spectral descriptors measure, and what classification accuracy checks* (Mikoto Miura and Yuusuke Harada). It holds the
generator, the tests, the specification, the conditions fixed before each computation, the scripts, the results and
the supplement.

## The rule in one picture

A rule of this type maps a point of an input space, here valence *V* and arousal *A* in [−1, 1]², affinely to the
parameters of a procedural field, reshapes the field with a signed power and exports it as a height map. The rule read
in the paper ([Harada 2026](https://doi.org/10.21203/rs.3.rs-8696852/v1)) sets, with *p* = (*A* + 1)/2 and
*q* = (1 − *V*)/2,

- frequency *f* = 3 + 4*p*, amplitude *s* = 0.06 + 0.24*q*, exponent γ = 0.9 + 1.7 (0.65*p* + 0.35*q*),
- height *H* = *s* · sign(*F*) |*F*|^(1/γ), where *F* is a four-octave field of products of sines scaled to [−1, 1].

<p align="center">
  <img alt="The input point moves over the square of valence and arousal and the relief follows the rule"
       src="docs/media/rule.gif" width="640">
</p>

The three parameters move together: the rule has three parameters but only two degrees of freedom. The second
animation shows one consequence. On one height scale shared by all works, the relief flattens as valence grows,
because valence alone sets the amplitude *s*. Exported image by image with min–max scaling, every relief spans the full
depth, and the difference disappears.

<p align="center">
  <img alt="The same reliefs on one common height scale and under a per-image min-max export"
       src="docs/media/export.gif" width="640">
</p>

The animations are illustrations made by `tools/readme_media.py` with one fixed seed; no number in the paper comes from
them.

## What the paper shows

- The rule has three parameters but two degrees of freedom, and a per-image min–max export removes the parameter set
  by valence alone.
- Its signed power makes the steepest slope depend on the grid unless the power is smoothed at a chosen length.
- The amplitude-weighted frequency centroid measures the grid, and for non-integer frequency the edge of the domain,
  as well as the frequency.
- For the field without warp, the direction and order of classification accuracy were predicted before the experiment,
  with small failures; the level, computed beforehand by simulation, agreed for the classifiers it was computed for,
  and two qualitative predictions of level failed. Accuracy checks whether an intended difference reaches a
  descriptor, not whether a surface conveys an emotion.
- The paper proposes that the height scale, the smoothing and the band of a spectral descriptor be stated with a work
  made by such a rule.

## Relation to the original rule

The rule was published as a preprint by the second author ([Harada 2026](https://doi.org/10.21203/rs.3.rs-8696852/v1)).
Its code has been lost. The generator in `src/atact/` is a reconstruction from the description in the preprint, and
every number in the paper comes from this reconstruction. The assumptions that fill the gaps in the description are in
`experiments/spec/generator-and-descriptors.md`, with a test of each clause against the code. Because the original
code is not available, a difference between our values and the values reported in the preprint cannot be traced to its
source (Supplement S7).

## Contents

| Path | Contents |
|---|---|
| `src/atact/` | The reconstructed generator: the map from (*V*, *A*) to (*f*, *s*, γ), the field, the transform, the exports, the descriptors, the classifiers and the statistics |
| `tests/` | Tests of the propositions of the paper and of the code against the specification |
| `experiments/spec/` | The specification of the generator and the descriptors (English; a Japanese version beside it) |
| `experiments/conditions/` | The conditions of each computation, fixed and committed before it was run; `INDEX.json` lists them |
| `experiments/` | One script per computation (see the table below) |
| `results/` | The results; every file records the SHA-256 of its conditions file, its script and the specification, the package versions and the commit at which it was run |
| `results/figs/` | The figures of the paper |
| `supplement/supplement.pdf` | The supplement of the paper |
| `tools/readme_media.py` | The logo and the animations of this page |
| `tools/graphical_abstract.py` | The graphical abstract for the journal (`docs/media/graphical-abstract.png`) |
| `adapters/original_template.py`, `experiments/arrival_check.py` | An interface for running the original code, should it become available |
| `experiments/legacy/` and the scripts not listed below | Earlier checks of the reconstruction, kept for the record; the paper does not use them |

## Reproducing the results

Requirements: Python 3.12 or later and [uv](https://docs.astral.sh/uv/). Package versions are fixed by `uv.lock`.

```bash
uv sync
uv run pytest -q          # 343 tests pass; 14 are skipped (they need the original code)
```

Each results file is regenerated by one command from the repository root (Supplement S9):

| Results | Command (`uv run python experiments/...`) |
|---|---|
| `k2_gradient` | `k2_gradient.py` |
| `k4_centroid_2d` | `k4_centroid_2d.py` |
| `edge_grid_paired` | `edge_grid_paired.py` |
| `validation3_public` | `validation3_public.py` |
| `k5_power`, `k5_large_sample`, `k5_classification` | `k5_classification.py --power`, `--large-sample`, `--frame`, then without options |
| `table1_main` | `table1_main.py` |
| `variants_reported` | `variants_reported.py` |
| `text_path_example` | `text_path_example.py`, then `text_path_figures.py` |
| `observable_dof` | `observable_dof.py` |
| `k4_supplement`, `v3_reduction_supplement` | `k4_supplement.py`, `v3_reduction_supplement.py` |
| `cband_cutoff_sensitivity` | `cband_cutoff_sensitivity.py` |
| Figures 1–4 | `figures_main.py` |

Some computations take hours (the classification experiment of Table 1 in particular).

The supplement and the results files cite commits by their hashes in the working repository in which the computations
were run. This history was prepared from that repository by removing the LaTeX source of the manuscript and setting
the author name, with the files and the dates unchanged; `commit-map.tsv` maps each original hash to the commit here.

Some records of the earlier, exploratory checks are in Japanese: their scripts, conditions and reports, and the report
`results/observable_dof.md` cited by the supplement. They are kept unchanged because their SHA-256 are recorded in the
results. English translations are beside them: `experiments/conditions/*.en.json` and `results/observable_dof.en.md`.

External data:

- The text example of the paper needs the NRC VAD Lexicon v2.1 (`NRC-VAD-Lexicon-v2.1.txt`), which is available from
  its authors and is not redistributed here.
- The measured surfaces are read from their public records: the Surface-Topography Challenge
  ([doi:10.5281/zenodo.15341939](https://doi.org/10.5281/zenodo.15341939)) and TactileDreamFusion on Hugging Face
  (revision `87c8b764bcb2ec1139de0c6435f45ac1d9f283d1`).

## Citation

Please cite the paper:

> Miura, M. and Harada, Y. A generative rule from affect to tactile relief: what it decides, what its spectral
> descriptors measure, and what classification accuracy checks. Manuscript.

and this archive (also in `CITATION.cff`):

> Miura, M. and Harada, Y. (2026). affective-relief-audit: generator, tests, results and supplement for 'A generative
> rule from affect to tactile relief'. Zenodo. https://doi.org/10.5281/zenodo.23681773

and, for the rule itself, the preprint:

> Harada, Y. (2026). Affective Tactility: Cross-Modal Translation from Natural Language to Procedural Height Maps.
> Preprint, Research Square. https://doi.org/10.21203/rs.3.rs-8696852/v1

The source is at https://github.com/mikotomiura/affective-relief-audit.

## License

The code is released under the MIT License (`LICENSE`). The documents, the results and the figures are released under
the Creative Commons Attribution 4.0 International License (`LICENSE-docs`).

## Authors

- Mikoto Miura, Independent Researcher ([ORCID 0009-0000-4196-0508](https://orcid.org/0009-0000-4196-0508))
- Yuusuke Harada, Graduate School of Humanities and Social Sciences, Hiroshima University, Japan
  ([ORCID 0009-0006-7252-5115](https://orcid.org/0009-0006-7252-5115))
