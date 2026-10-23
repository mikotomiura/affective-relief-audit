"""ジッタの幅 w（座標に U(-w,w) を足して [-1,1] で切る）と、Sq / 重心 の閾値分類の最良精度。"""
import numpy as np
exec(open('checks.py').read().split('print("== P1')[0])
def field(f, N=128, seed=42):
    rng = np.random.default_rng(seed); y, x = np.mgrid[0:N, 0:N] / N; F = np.zeros((N, N))
    for o in range(4):
        fo, a = f * 2 ** o, 0.5 ** o; px, py = rng.uniform(0, 2 * np.pi, 2)
        F += a * np.sin(2 * np.pi * fo * x + px) * np.sin(2 * np.pi * fo * y + py)
    return F / np.abs(F).max()
def centroid(H):
    Hc = H - H.mean(); A = np.abs(np.fft.fft2(Hc)); k = np.fft.fftfreq(H.shape[0]) * H.shape[0]
    R = np.hypot(*np.meshgrid(k, k)); return (R * A).sum() / A.sum()
def best_thr(a, b):
    v = np.r_[a, b]; y = np.r_[np.zeros(len(a)), np.ones(len(b))]
    return max(max(np.mean((v > t) == y), np.mean((v <= t) == y)) for t in v)
rng = np.random.default_rng(0)
for w in [0.1, 0.3, 0.5, 0.8, 1.0, 1.5]:
    feats = {0: [], 1: []}
    for cls, (V0, A0) in enumerate([(1, -1), (-1, 1)]):
        for i in range(60):
            V = np.clip(V0 + rng.uniform(-w, w), -1, 1); A = np.clip(A0 + rng.uniform(-w, w), -1, 1)
            f, s, g = params(V, A); H = s * T(field(f, seed=1000 * cls + i), g)
            feats[cls].append((H.std(), centroid(H)))
    a = np.array(feats[0]); b = np.array(feats[1])
    print(f"w={w}: Sq-thr={best_thr(a[:,0], b[:,0]):.3f}  C-thr={best_thr(a[:,1], b[:,1]):.3f}")
