"""案 A の命題を数値で確かめる。生成器は本文の記述からの再構成（元コードではない）。"""
import numpy as np
from scipy.special import gamma as G

T = lambda u, g: np.sign(u) * np.abs(u) ** (1.0 / g)


def params(V, A):
    p, q = (A + 1) / 2, (1 - V) / 2
    return 3 + 4 * p, 0.06 + 0.24 * q, 0.9 + 1.7 * (0.65 * p + 0.35 * q)


print("== P1 像は平行四辺形（列ベクトルの内積）")
dV = np.array([0, -0.12, -0.2975]); dA = np.array([2, 0, 0.5525])
print("dV.dA =", dV @ dA, " rank =", np.linalg.matrix_rank(np.c_[dV, dA]))
for V, A in [(1, -1), (-1, 1), (0, 0), (0.3, -0.7)]:
    f, s, g = params(V, A)
    print(f"  ({V},{A}) gamma={g:.4f} from (f,s)={0.9+0.27625*(f-3)+1.7*0.35*(s-0.06)/0.24:.4f}")

print("== P3 単一正弦の RMS: E|sin|^(2/g) = Γ(1/g+1/2)/(√π Γ(1/g+1))")
th = np.linspace(0, 2 * np.pi, 2_000_001)[:-1]
for g in [0.9, 1.0, 1.75, 2.6]:
    num = np.mean(np.abs(np.sin(th)) ** (2 / g))
    cf = G(1 / g + 0.5) / (np.sqrt(np.pi) * G(1 / g + 1))
    print(f"  g={g}: numeric={num:.6f} closed={cf:.6f}  rms={np.sqrt(cf):.4f}")

print("== P4 Tγ(sin) のフーリエ係数の減衰（奇数次のみ・傾き ≈ -(1+1/g)）")
M = 1 << 18
x = np.arange(M) / M
for g in [0.9, 1.75, 2.6]:
    c = np.abs(np.fft.rfft(T(np.sin(2 * np.pi * x), g))) / M
    n = np.arange(len(c))
    odd = n[(n % 2 == 1) & (n > 50) & (n < 2000)]
    slope = np.polyfit(np.log(odd), np.log(c[odd]), 1)[0]
    print(f"  g={g}: even max={c[2::2][:200].max():.2e}  slope={slope:.3f}  theory={-(1+1/g):.3f}")

print("== P4' 1 次元の振幅重みの重心（f=5）は解像度で動くか")
for g in [0.9, 1.0, 1.75, 2.6]:
    row = []
    for N in [128, 512, 2048, 8192]:
        xx = np.arange(N) / N
        c = np.abs(np.fft.rfft(T(np.sin(2 * np.pi * 5 * xx), g)))[1:]
        k = np.arange(1, len(c) + 1)
        row.append((k * c).sum() / c.sum())
    print(f"  g={g}: " + "  ".join(f"N={N}:{r:.2f}" for N, r in zip([128, 512, 2048, 8192], row)))


def field(f, N=128, seed=42, warp=0.0):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:N, 0:N] / N
    F = np.zeros((N, N))
    for o in range(4):
        fo, a = f * 2 ** o, 0.5 ** o
        px, py = rng.uniform(0, 2 * np.pi, 2)
        F += a * np.sin(2 * np.pi * fo * x + px) * np.sin(2 * np.pi * fo * y + py)
    return F / np.abs(F).max()


def centroid(H):
    Hc = H - H.mean()
    A = np.abs(np.fft.fft2(Hc))
    k = np.fft.fftfreq(H.shape[0]) * H.shape[0]
    R = np.hypot(*np.meshgrid(k, k))
    return (R * A).sum() / A.sum()


print("== P5 2 次元・本文の 2 つの隅（4 オクターブ・N=128）")
for V, A in [(1, -1), (-1, 1)]:
    f, s, g = params(V, A)
    F = field(f)
    H = s * T(F, g)
    Hn = (H - H.min()) / (H.max() - H.min())
    print(f"  ({V},{A}) f={f} s={s} g={g:.3f}: Sq={H.std():.4f} Sq/s={T(F,g).std():.4f}"
          f"  C(H)={centroid(H):.2f}  C(F)={centroid(F):.2f}  Sq(minmax)={Hn.std():.4f}")
print("  minmax は s に依らない:", np.allclose(*[(lambda H: (H - H.min()) / (H.max() - H.min()))(s * T(field(5), 1.75)) for s in (0.06, 0.3)]))

print("== P5' 重心の比 vs f の比 7/3=2.333（γ を固定 / 本文どおり）")
for gs in [(1.0, 1.0), (0.9, 2.6)]:
    c3 = centroid(T(field(3), gs[0])); c7 = centroid(T(field(7), gs[1]))
    print(f"  g=({gs[0]},{gs[1]}): C3={c3:.2f} C7={c7:.2f} ratio={c7/c3:.3f}")
for N in [128, 256, 512, 1024]:
    c3 = centroid(T(field(3, N), 0.9)); c7 = centroid(T(field(7, N), 2.6))
    print(f"  N={N}: C3={c3:.2f} C7={c7:.2f} ratio={c7/c3:.3f}")

print("== P6 最大勾配（格子間隔あたり）は解像度で発散するか")
for g in [0.9, 1.75, 2.6]:
    out = []
    for N in [128, 256, 512, 1024, 2048]:
        Z = T(field(5, N), g)
        gy, gx = np.gradient(Z, 1.0 / N)
        out.append(np.hypot(gx, gy).max())
    print(f"  g={g}: " + "  ".join(f"{o:.0f}" for o in out), " growth128->2048 =", f"{out[-1]/out[0]:.2f}", " theory 16^(1-1/g) =", f"{16**max(0,1-1/g):.2f}")

print("== P7 台地の割合 |Tγ(F)| > 0.9 と |F| > 0.9^g")
F = field(5)
for g in [0.9, 1.75, 2.6]:
    print(f"  g={g}: plateau={np.mean(np.abs(T(F,g))>0.9):.3f}  (|F|>0.9: {np.mean(np.abs(F)>0.9):.3f})")
