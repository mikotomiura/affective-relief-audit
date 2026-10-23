# 重心の定義の変種と命題 7（組み直しの生成器での値・雑音なし）

報告（表 3）: Rq だけ 91.6、重心だけ 74.2 ± 8.5、両方 92.1。

列は重心だけの精度（両方の精度）。w はジッタ。既定の定義（式 (6) の素直な読み）は 1 行目。

| 重み | 中心化 | min-max の後 | 半平面 | 半径を丸める | ワープ 0.0 w=1.0 | ワープ 0.0 w=1.25 | ワープ 0.0 w=1.5 | ワープ 0.25 w=1.0 | ワープ 0.25 w=1.25 | ワープ 0.25 w=1.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| amp | True | - | False | False | 95.5 (99.3) | 89.6 (95.3) | 85.9 (89.1) | 96.5 (98.1) | 85.6 (93.6) | 83.1 (88.3) |
| amp | True | - | False | True | 95.5 (99.3) | 89.5 (95.1) | 85.8 (89.1) | 96.5 (98.1) | 85.8 (93.6) | 83.2 (88.3) |
| amp | True | - | True | False | 95.6 (99.3) | 89.6 (95.5) | 85.9 (89.2) | 96.5 (98.4) | 85.6 (93.5) | 82.7 (88.5) |
| amp | True | - | True | True | 95.5 (99.4) | 89.5 (95.3) | 85.8 (89.1) | 96.5 (98.4) | 85.6 (93.4) | 82.7 (88.7) |
| amp | True | minmax | False | False | 95.5 (99.3) | 89.6 (95.3) | 85.9 (89.1) | 96.5 (98.1) | 85.6 (93.6) | 83.1 (88.3) |
| amp | True | minmax | False | True | 95.5 (99.3) | 89.5 (95.1) | 85.7 (89.1) | 96.5 (98.1) | 85.8 (93.6) | 83.2 (88.3) |
| amp | True | minmax | True | False | 95.6 (99.3) | 89.6 (95.5) | 85.9 (89.2) | 96.5 (98.4) | 85.6 (93.5) | 82.7 (88.5) |
| amp | True | minmax | True | True | 95.5 (99.4) | 89.5 (95.3) | 85.8 (89.1) | 96.5 (98.4) | 85.6 (93.4) | 82.7 (88.7) |
| amp | False | - | False | False | 95.5 (99.2) | 89.4 (95.3) | 85.9 (89.1) | 96.7 (97.9) | 85.0 (93.8) | 83.4 (89.0) |
| amp | False | - | False | True | 95.5 (99.3) | 89.4 (95.2) | 85.7 (89.1) | 96.7 (97.9) | 85.1 (93.8) | 83.4 (89.0) |
| amp | False | - | True | False | 95.5 (99.3) | 89.3 (95.5) | 85.9 (89.2) | 96.2 (97.9) | 85.6 (93.7) | 83.1 (89.5) |
| amp | False | - | True | True | 95.5 (99.3) | 89.2 (95.4) | 85.8 (89.2) | 96.2 (98.0) | 85.6 (93.7) | 83.2 (89.5) |
| amp | False | minmax | False | False | 96.8 (99.3) | 90.6 (96.1) | 86.7 (89.5) | 96.8 (99.2) | 85.6 (93.6) | 83.0 (89.2) |
| amp | False | minmax | False | True | 96.8 (99.3) | 90.6 (96.1) | 86.7 (89.5) | 96.8 (99.2) | 85.8 (93.6) | 82.9 (89.2) |
| amp | False | minmax | True | False | 98.6 (99.4) | 91.4 (97.0) | 87.8 (89.8) | 96.5 (99.2) | 88.0 (94.5) | 83.5 (89.6) |
| amp | False | minmax | True | True | 98.8 (99.4) | 91.3 (97.0) | 87.7 (89.8) | 96.5 (99.2) | 88.0 (94.5) | 83.6 (89.6) |
| power | True | - | False | False | 98.2 (99.3) | 90.0 (96.5) | 81.9 (90.3) | 93.2 (99.5) | 84.7 (95.0) | 77.5 (89.3) |
| power | True | - | False | True | 98.3 (99.2) | 90.4 (96.1) | 81.6 (90.2) | 93.4 (99.5) | 84.2 (95.0) | 77.5 (89.0) |
| power | True | - | True | False | 98.3 (99.4) | 90.4 (96.4) | 82.0 (90.3) | 92.5 (99.5) | 84.4 (94.6) | 77.4 (89.4) |
| power | True | - | True | True | 98.3 (99.4) | 90.4 (96.0) | 81.6 (90.2) | 92.4 (99.7) | 84.1 (94.6) | 77.6 (89.2) |
| power | True | minmax | False | False | 98.2 (99.3) | 90.0 (96.5) | 81.9 (90.3) | 93.2 (99.5) | 84.7 (95.0) | 77.5 (89.3) |
| power | True | minmax | False | True | 98.3 (99.2) | 90.4 (96.1) | 81.6 (90.2) | 93.4 (99.5) | 84.2 (95.0) | 77.5 (89.0) |
| power | True | minmax | True | False | 98.3 (99.4) | 90.4 (96.4) | 82.0 (90.3) | 92.5 (99.5) | 84.4 (94.6) | 77.4 (89.4) |
| power | True | minmax | True | True | 98.3 (99.4) | 90.4 (96.0) | 81.6 (90.2) | 92.4 (99.7) | 84.1 (94.6) | 77.6 (89.2) |
| power | False | - | False | False | 98.3 (99.2) | 89.9 (96.5) | 81.8 (90.3) | 86.9 (98.5) | 80.2 (95.0) | 74.2 (89.7) |
| power | False | - | False | True | 98.3 (99.2) | 90.3 (96.1) | 81.5 (90.2) | 86.5 (98.4) | 79.9 (94.9) | 74.5 (89.7) |
| power | False | - | True | False | 98.3 (99.3) | 90.3 (96.5) | 81.9 (90.3) | 84.6 (97.7) | 77.4 (95.0) | 73.8 (89.8) |
| power | False | - | True | True | 98.3 (99.2) | 90.3 (96.1) | 81.5 (90.2) | 84.4 (97.7) | 76.8 (95.0) | 74.0 (89.9) |
| power | False | minmax | False | False | 97.7 (99.2) | 92.5 (94.8) | 85.3 (90.9) | 91.8 (97.1) | 86.0 (94.6) | 78.3 (90.8) |
| power | False | minmax | False | True | 98.0 (99.2) | 92.5 (94.9) | 85.7 (90.9) | 91.7 (97.2) | 85.9 (94.5) | 78.5 (90.8) |
| power | False | minmax | True | False | 97.5 (99.2) | 92.7 (94.7) | 86.1 (90.7) | 89.6 (96.8) | 84.6 (94.0) | 77.7 (90.2) |
| power | False | minmax | True | True | 97.5 (99.2) | 92.5 (94.8) | 86.9 (90.9) | 89.4 (96.9) | 84.2 (94.0) | 77.9 (90.3) |

## 要約

- 重心だけの精度の最小: 73.8%（{'weight': 'power', 'center': False, 'rescale': None, 'half': True, 'rho_round': False}、ワープ 0.25、w = 1.5）。そのときの Rq だけは 87.0%。
- Rq だけの精度（定義に依らない）: ワープ 0.0 w=1.0: 99.5、ワープ 0.0 w=1.25: 92.0、ワープ 0.0 w=1.5: 86.2、ワープ 0.25 w=1.0: 98.1、ワープ 0.25 w=1.25: 90.0、ワープ 0.25 w=1.5: 87.0。
- Rq − 重心 の最大: +13.7 ポイント（{'weight': 'power', 'center': False, 'rescale': None, 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.0）。報告は +17.4。
- 中心化してから測る定義では、min-max の有無で値が変わらない（重心は場のアフィン変換に依らないため）。
- 重心だけ・Rq だけの両方が報告の標準偏差 1 つ分以内に入る行: 23 行。
  - {'weight': 'amp', 'center': True, 'rescale': None, 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 82.7 / 両方 88.7
  - {'weight': 'amp', 'center': True, 'rescale': 'minmax', 'half': True, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 82.7 / 両方 88.5
  - {'weight': 'amp', 'center': True, 'rescale': 'minmax', 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 82.7 / 両方 88.7
  - {'weight': 'power', 'center': True, 'rescale': None, 'half': False, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.5 / 両方 89.3
  - {'weight': 'power', 'center': True, 'rescale': None, 'half': False, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.5 / 両方 89.0
  - {'weight': 'power', 'center': True, 'rescale': None, 'half': True, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.4 / 両方 89.4
  - {'weight': 'power', 'center': True, 'rescale': None, 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.6 / 両方 89.2
  - {'weight': 'power', 'center': True, 'rescale': 'minmax', 'half': False, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.5 / 両方 89.3
  - {'weight': 'power', 'center': True, 'rescale': 'minmax', 'half': False, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.5 / 両方 89.0
  - {'weight': 'power', 'center': True, 'rescale': 'minmax', 'half': True, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.4 / 両方 89.4
  - {'weight': 'power', 'center': True, 'rescale': 'minmax', 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.6 / 両方 89.2
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': False, 'rho_round': False}、ワープ 0.25、w = 1.25: Rq 90.0 / 重心 80.2 / 両方 95.0
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': False, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 74.2 / 両方 89.7
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': False, 'rho_round': True}、ワープ 0.25、w = 1.25: Rq 90.0 / 重心 79.9 / 両方 94.9
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': False, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 74.5 / 両方 89.7
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': True, 'rho_round': False}、ワープ 0.25、w = 1.25: Rq 90.0 / 重心 77.4 / 両方 95.0
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': True, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 73.8 / 両方 89.8
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.25: Rq 90.0 / 重心 76.8 / 両方 95.0
  - {'weight': 'power', 'center': False, 'rescale': None, 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 74.0 / 両方 89.9
  - {'weight': 'power', 'center': False, 'rescale': 'minmax', 'half': False, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 78.3 / 両方 90.8
  - {'weight': 'power', 'center': False, 'rescale': 'minmax', 'half': False, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 78.5 / 両方 90.8
  - {'weight': 'power', 'center': False, 'rescale': 'minmax', 'half': True, 'rho_round': False}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.7 / 両方 90.2
  - {'weight': 'power', 'center': False, 'rescale': 'minmax', 'half': True, 'rho_round': True}、ワープ 0.25、w = 1.5: Rq 87.0 / 重心 77.9 / 両方 90.3
