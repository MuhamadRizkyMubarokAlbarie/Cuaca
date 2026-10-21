import glob
import numpy as np
import pandas as pd

# 1. Gabungkan semua file mentah (sesuaikan ekstensi: .xlsx atau .csv)
berkas = sorted(glob.glob("data/raw/*.xlsx"))
df = pd.concat([pd.read_excel(f) for f in berkas], ignore_index=True)

# 2. Standarkan tanggal dan curah hujan (sesuaikan nama kolom dengan file kamu)
df["tanggal"] = pd.to_datetime(df["TANGGAL"], dayfirst=True, errors="coerce")
df["RR"] = pd.to_numeric(df["RR"], errors="coerce")

# 3. 8888 = tidak terukur, 9999 = tidak ada data
df["RR"] = df["RR"].replace([8888, 9999], np.nan)

# 4. Urutkan, buang duplikat, pastikan tanggal berurutan harian
df = (df.dropna(subset=["tanggal"])
        .drop_duplicates("tanggal")
        .sort_values("tanggal")
        .set_index("tanggal")
        .asfreq("D"))

# 5. Laporan kelengkapan data per tahun
print("Persentase data hilang per tahun:")
print(df["RR"].isna().groupby(df.index.year).mean().mul(100).round(1))

# 6. Definisi hari hujan (ambang 1 mm)
AMBANG = 1.0
df["hujan"] = np.where(df["RR"].isna(), np.nan, (df["RR"] >= AMBANG).astype(float))

# 7. Ringkasan awal
print("\nRentang:", df.index.min().date(), "sampai", df.index.max().date())
print("Peluang hari hujan:", round(df["hujan"].mean(), 3))
print("Rata-rata hujan pada hari hujan (mm):", round(df.loc[df["hujan"] == 1, "RR"].mean(), 2))
print("Hujan maksimum (mm):", df["RR"].max())

df[["RR", "hujan"]].to_csv("data/curah_hujan_bersih.csv")
