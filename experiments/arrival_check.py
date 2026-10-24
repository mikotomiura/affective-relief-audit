"""Single script to run once the original code (ESM_1.zip) is available.

Usage (after steps 1-3 of the section on the arrival of the original code in the README):
  uv run python experiments/arrival_check.py --zip ~/Downloads/ESM_1.zip
Output: results/original/ with manifest.json, conformance.txt, compare.md, fig3.md, fig3.png, decompose.md, README.md

Order:
  1. Write the SHA-256 of the zip and of each extracted file to manifest.json (a record of what was run)
  2. Run the conformance tests (test_conf_* in tests/test_backends.py) against the original code
  3. Compare with the reported values (compare_reported)
  4. Regenerate Fig. 3 and compute fingerprints (when the adapter provides fig3_heights)
  5. Decomposition (decompose)

Loading the adapter imports and executes the original code. Read the original code before running it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(zip_path: Path | None, esm: Path, adapter: Path) -> dict:
    files = []
    if esm.exists():
        for p in sorted(esm.rglob("*")):
            if p.is_file():
                files.append({"path": str(p.relative_to(esm)), "bytes": p.stat().st_size, "sha256": sha256(p)})
    return {
        "zip": None if zip_path is None else {"name": zip_path.name, "bytes": zip_path.stat().st_size,
                                               "sha256": sha256(zip_path)},
        "esm_dir": str(esm), "files": files,
        "adapter": {"path": str(adapter), "sha256": sha256(adapter)},
    }


def conformance(adapter: Path) -> tuple[int, str]:
    env = {**os.environ, "ATACT_ORIGINAL_ADAPTER": str(adapter)}
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rfs", str(ROOT / "tests" / "test_backends.py"),
                        "-k", "conf and original"], capture_output=True, text=True, env=env, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def _dihedral(H):
    for k in range(4):
        R = np.rot90(H, k)
        yield f"rot{90 * k}", R
        yield f"rot{90 * k}+flip", R[:, ::-1]


def fig3_section(orig, out: Path) -> str:
    from atact import fig3

    heights = orig.fig3_heights()
    if heights is None:
        return "## 図 3\n\nアダプタに fig3_heights が無い。図 3 を描き直す関数が元のコードにあるかを確かめる。\n"
    ref = fig3.panels()
    L = ["## 図 3（元のコードで描き直した高さ vs 図から取り戻した高さ）", "",
         "高さはどちらも min-max して比べる。向きは 8 通りのうち差の最も小さいもの。"
         "図から取り戻した高さは 256 段に量子化されているので、一致なら最大の差は 1/255（約 0.004）前後になる。", "",
         "| 枚 | 格子 | 向き | 最大の差 | 相関 | 指紋の距離 | 周期数 x / y（元） | 周期数 x / y（図） |",
         "|---|---|---|---|---|---|---|---|"]
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(9, 6))
    for j, name in enumerate(fig3.PANELS):
        R = ref[name]["height"]
        H = heights.get(name)
        if H is None:
            L.append(f"| {name} | 無し | - | - | - | - | - | - |")
            continue
        Hm = (H - H.min()) / (H.max() - H.min())
        if Hm.shape == R.shape:
            best = min(((np.abs(D - R).max(), lab, D) for lab, D in _dihedral(Hm)), key=lambda x: x[0])
            md, lab, D = best
            corr = float(np.corrcoef(D.ravel(), R.ravel())[0, 1])
            cells = f"{lab} | {md:.4f} | {corr:.4f}"
        else:
            D, cells = Hm, "- | - | -"
        fpo, fpr = fig3.fingerprint(D), fig3.fingerprint(R)  # measured after aligning the orientation (x and y are not swapped)
        L.append(f"| {name} | {Hm.shape[0]} x {Hm.shape[1]} | {cells} | {fig3.distance(fpo, fpr):.2f} | "
                 f"{fpo['cycles_x']:.2f} / {fpo['cycles_y']:.2f} | {fpr['cycles_x']:.2f} / {fpr['cycles_y']:.2f} |")
        axes[0, j].imshow(R, cmap="gist_earth")
        axes[0, j].set_title(f"{name}: figure 3", fontsize=8)
        axes[1, j].imshow(D, cmap="gist_earth")
        axes[1, j].set_title(f"{name}: original code", fontsize=8)
    for ax in axes.ravel():
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(out / "fig3.png", dpi=110)
    plt.close(fig)
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=Path)
    ap.add_argument("--esm", type=Path, default=ROOT / "external" / "esm1")
    ap.add_argument("--adapter", type=Path, default=ROOT / "adapters" / "original.py")
    ap.add_argument("--out", type=Path, default=ROOT / "results" / "original")
    ap.add_argument("--jitter", type=float, nargs="+", default=[1.0, 1.25, 1.5])
    a = ap.parse_args()
    if not a.adapter.exists():
        raise SystemExit(f"アダプタが無い: {a.adapter}（adapters/original_template.py を写して埋める）")
    os.environ["ATACT_ORIGINAL_ADAPTER"] = str(a.adapter.resolve())
    a.out.mkdir(parents=True, exist_ok=True)

    status = []
    m = manifest(a.zip, a.esm, a.adapter)
    (a.out / "manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))
    status.append(f"1. manifest.json: zip {'あり' if m['zip'] else '指定なし'}、展開したファイル {len(m['files'])} 個")

    rc, log = conformance(a.adapter.resolve())
    (a.out / "conformance.txt").write_text(log)
    last = log.strip().splitlines()[-1] if log.strip() else ""
    status.append(f"2. 適合テスト: {'通った' if rc == 0 else '落ちた（所見。conformance.txt を読む）'} —— {last}")

    from atact import backends
    import compare_reported
    import decompose

    (a.out / "compare.md").write_text(compare_reported.build("original", a.jitter))
    status.append("3. 報告値との比較: compare.md")

    orig = backends.original()
    (a.out / "fig3.md").write_text(fig3_section(orig, a.out))
    status.append("4. 図 3: fig3.md（描き直せたときは fig3.png も）")

    (a.out / "decompose.md").write_text(decompose.render(decompose.cells(1.25), 1.25))
    status.append("5. 切り分け: decompose.md（ジッタ w = 1.25）")

    readme = ["# 元のコードを通した結果", "",
              f"アダプタ: `{a.adapter}`（SHA-256 {m['adapter']['sha256'][:16]}…）", "", *status, "",
              "ここの値は元のコードの生成器（とアダプタが渡した関数）を通した値。手順が「組み直し」の部分は"
              "こちらの仮定（A4〜A6）を含む。"]
    (a.out / "README.md").write_text("\n".join(readme) + "\n")
    print("\n".join(status))
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
