import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)          # seed tetap -> hasil bisa diulang
KEADAAN = ["Kering", "Lembab", "Basah"]  # 0, 1, 2
BATAS_KERING, BATAS_BASAH = 100, 200     # mm/bulan

# 1. Data
df = pd.read_csv("data/curah_hujan_bulanan_bersih.csv", parse_dates=["tanggal"])
df = df.dropna(subset=["rr"]).reset_index(drop=True)
rr = df["rr"].to_numpy()
keadaan = np.where(rr < BATAS_KERING, 0, np.where(rr <= BATAS_BASAH, 1, 2))

# 2. Matriks transisi (dihitung dari data)
hitung = np.zeros((3, 3), dtype=int)
for a, b in zip(keadaan[:-1], keadaan[1:]):
    hitung[a, b] += 1
baris = hitung.sum(axis=1, keepdims=True)
P = np.where(baris > 0, hitung / np.maximum(baris, 1), 1 / 3)

print("Jumlah bulan:", len(rr))
print("Proporsi keadaan (data):", dict(zip(KEADAAN, (np.bincount(keadaan, minlength=3) / len(rr)).round(3).tolist())))
print("\nJumlah transisi:\n", pd.DataFrame(hitung, KEADAAN, KEADAAN))
print("\nMatriks transisi P:\n", pd.DataFrame(P, KEADAAN, KEADAAN).round(3))

# 3. Sampel curah hujan per keadaan (bootstrap empiris)
sampel = {k: rr[keadaan == k] for k in range(3)}
for k in range(3):
    print(f"{KEADAAN[k]}: n={len(sampel[k])}, rata-rata={sampel[k].mean():.1f} mm")


def simulasi(n_bulan, awal, n_ulang=5000):
    """Kembalikan array keadaan dan curah hujan, bentuk (n_ulang, n_bulan)."""
    s = np.empty((n_ulang, n_bulan), dtype=int)
    x = np.empty((n_ulang, n_bulan))
    cur = np.full(n_ulang, awal) if np.isscalar(awal) else awal.copy()
    for t in range(n_bulan):
        u = rng.random(n_ulang)
        cum = P[cur].cumsum(axis=1)
        cur = (u[:, None] > cum).sum(axis=1).clip(0, 2)
        s[:, t] = cur
        for k in range(3):
            m = cur == k
            x[m, t] = rng.choice(sampel[k], size=m.sum())
    return s, x


# 4. Validasi: simulasi jangka panjang vs data
s_panjang, x_panjang = simulasi(600, rng.integers(0, 3, 5000), n_ulang=5000)
print("\nVALIDASI (simulasi 600 bulan x 5000 ulangan)")
print("Proporsi keadaan simulasi:", dict(zip(KEADAAN, (np.bincount(s_panjang.ravel(), minlength=3) / s_panjang.size).round(3).tolist())))
print(f"Rata-rata curah hujan bulanan: data={rr.mean():.1f} mm | simulasi={x_panjang.mean():.1f} mm")
print(f"Simpangan baku: data={rr.std(ddof=1):.1f} mm | simulasi={x_panjang.std():.1f} mm")

# 5. Prediksi 12 bulan ke depan dari keadaan terakhir
awal = int(keadaan[-1])
s_pred, x_pred = simulasi(12, awal)
bulan = pd.period_range(df["tanggal"].iloc[-1], periods=13, freq="M")[1:].astype(str)
ringkas = pd.DataFrame({
    "bulan": bulan,
    "rata2_mm": x_pred.mean(axis=0).round(1),
    "p5": np.percentile(x_pred, 5, axis=0).round(1),
    "p95": np.percentile(x_pred, 95, axis=0).round(1),
    "peluang_basah": (s_pred == 2).mean(axis=0).round(3),
    "peluang_kering": (s_pred == 0).mean(axis=0).round(3),
})
print("\nPREDIKSI 12 BULAN (mulai dari keadaan terakhir:", KEADAAN[awal] + ")")
print(ringkas.to_string(index=False))
total = x_pred.sum(axis=1)
print(f"\nTotal 12 bulan: rata-rata={total.mean():.0f} mm, rentang 90% = {np.percentile(total,5):.0f}-{np.percentile(total,95):.0f} mm")

# 6. Grafik dan simpan hasil
os.makedirs("hasil", exist_ok=True)
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].bar(df["tanggal"], rr, width=20, color="steelblue")
ax[0].axhline(BATAS_BASAH, ls="--", c="gray"); ax[0].axhline(BATAS_KERING, ls=":", c="gray")
ax[0].set_title("Data BMKG Citeko (bulanan)"); ax[0].set_ylabel("mm")
ax[1].fill_between(range(1, 13), np.percentile(x_pred, 5, axis=0), np.percentile(x_pred, 95, axis=0), alpha=.3)
ax[1].plot(range(1, 13), x_pred.mean(axis=0), c="navy")
ax[1].set_title("Simulasi 12 bulan ke depan (rata-rata dan rentang 90%)")
ax[1].set_xlabel("bulan ke-"); ax[1].set_ylabel("mm")
plt.tight_layout(); plt.savefig("hasil/simulasi_markov.png", dpi=150)
ringkas.to_csv("hasil/prediksi_12_bulan.csv", index=False)
print("\nTersimpan: hasil/simulasi_markov.png dan hasil/prediksi_12_bulan.csv")