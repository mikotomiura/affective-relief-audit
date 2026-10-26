# Text example of Section 6 (results as generated)

Conditions SHA-256 `6765ade369abcac8b000073378ef7d0b6d9273a85145baf9f7f085c6a66b8f4b`, script `56fa1d81d8b190f309920cb91ed93e5e9f08121e67088a78b37d543d291ef795`, git `e434776ea00b307b7832d092502585bd2eba6c1b` (dirty: False). Seed 42, eps = 0.3529, L = 50 mm, D = 1.2 mm, s_max = 0.3.

Text A: "Is this the place? Where am I? Who am I?"

Text B: "Is this the old station in the cold rain? Where am I, lost among strangers on an empty platform? Who am I, when no one knows my face or my voice?"

## Variant: main

| # | sentence | matched | Z | V | A | f | s | gamma | span common (mm) | span common eps (mm) | angle common N=128 / 1024 | angle min-max N=128 / 1024 | angle common eps N=128 / 1024 | shape change (mm) | span ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | Is this the place? | is, this, place | 3 | 0.0487 | -0.1593 | 4.6813 | 0.1742 | 1.6475 | 0.579 | 0.569 | 30.8 / 51.5 | 51.0 / 69.0 | 22.9 / 26.7 | 0.033 | 0.882 |
| A2 | Where am I? | where, am | 2 | 0.0000 | 0.0000 | 5.0000 | 0.1800 | 1.7500 | 0.606 | 0.594 | 34.5 / 57.0 | 53.7 / 71.8 | 25.5 / 30.0 | 0.040 | 0.922 |
| A3 | Who am I? | am | 1 | 0.0000 | 0.0000 | 5.0000 | 0.1800 | 1.7500 | 0.606 | 0.594 | 34.5 / 57.0 | 53.7 / 71.8 | 25.5 / 30.0 | 0.040 | 0.922 |
| B1 | Is this the old station in the cold rain? | is, this, station, cold, rain | 5 | 0.0336 | -0.0828 | 4.8344 | 0.1760 | 1.6943 | 0.588 | 0.577 | 32.1 / 53.8 | 52.0 / 70.2 | 24.3 / 28.1 | 0.036 | 0.896 |
| B2 | Where am I, lost among strangers on an empty platform? | where, am, lost, among, on, empty, platform | 7 | -0.1416 | -0.1320 | 4.7360 | 0.1970 | 1.7192 | 0.657 | 0.644 | 34.7 / 58.1 | 51.7 / 71.1 | 24.9 / 30.6 | 0.042 | 1.000 |
| B3 | Who am I, when no one knows my face or my voice? | am, when, no one, face, voice | 5 | -0.0140 | -0.2676 | 4.4648 | 0.1817 | 1.6063 | 0.602 | 0.592 | 30.4 / 51.0 | 49.4 / 67.9 | 22.6 / 26.3 | 0.032 | 0.916 |

## Variant: function_words_removed

| # | sentence | matched | Z | V | A | f | s | gamma | span common (mm) | span common eps (mm) | angle common N=128 / 1024 | angle min-max N=128 / 1024 | angle common eps N=128 / 1024 | shape change (mm) | span ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | Is this the place? | place | 1 | 0.1460 | -0.4780 | 4.0440 | 0.1625 | 1.4425 | 0.528 | 0.520 | 23.0 / 38.9 | 44.0 / 61.4 | 17.4 / 20.4 | 0.021 | 0.757 |
| A2 | Where am I? | (none) | 0 | 0.0000 | 0.0000 | 5.0000 | 0.1800 | 1.7500 | 0.606 | 0.594 | 34.5 / 57.0 | 53.7 / 71.8 | 25.5 / 30.0 | 0.040 | 0.869 |
| A3 | Who am I? | (none) | 0 | 0.0000 | 0.0000 | 5.0000 | 0.1800 | 1.7500 | 0.606 | 0.594 | 34.5 / 57.0 | 53.7 / 71.8 | 25.5 / 30.0 | 0.040 | 0.869 |
| B1 | Is this the old station in the cold rain? | station, cold, rain | 3 | 0.0560 | -0.1380 | 4.7240 | 0.1733 | 1.6571 | 0.574 | 0.564 | 30.2 / 53.4 | 50.6 / 70.3 | 22.1 / 26.9 | 0.034 | 0.824 |
| B2 | Where am I, lost among strangers on an empty platform? | lost, platform | 2 | -0.2155 | 0.0030 | 5.0060 | 0.2059 | 1.8158 | 0.697 | 0.683 | 39.1 / 62.5 | 54.4 / 73.1 | 29.2 / 34.0 | 0.050 | 1.000 |
| B3 | Who am I, when no one knows my face or my voice? | face, voice | 2 | 0.1650 | -0.4840 | 4.0320 | 0.1602 | 1.4335 | 0.519 | 0.512 | 23.7 / 39.5 | 45.4 / 62.3 | 17.2 / 19.9 | 0.020 | 0.745 |

Span ratio: common-scale span relative to the largest over all tiles of the variant.

## Predictions (implementation controls)

- P-T1: holds = True; max_diff = {'main N=128': 4.440892098500626e-16, 'main N=1024': 5.551115123125783e-16, 'function_words_removed N=128': 4.440892098500626e-16, 'function_words_removed N=1024': 5.551115123125783e-16}
- P-T2: holds = True; max_minmax_dev_mm = 0, max_common_dev_mm = 1.11e-16
- P-T3: holds = True; cases_checked = 24
- P-T4 (text A): holds = True; unmatched = [1, 2], at_origin_with_params_of_(0,0) = True, max_diff_mm = 0
- P-T4 (text B): holds = None; unmatched = [], note = not applicable: fewer than two unmatched sentences

Figures: results/figs/fig5_text_path.pdf, results/figs/figS_text_path_nofunction.pdf
