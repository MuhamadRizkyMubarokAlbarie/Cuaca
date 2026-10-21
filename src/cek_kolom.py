import glob
import pandas as pd

berkas = sorted(glob.glob("data/raw/DataIklimBulanan_2024-10_2026-09.xlsx"))
print("File ditemukan:", berkas)

f = berkas[0]
df = pd.read_excel(f) if f.endswith((".xlsx", ".xls")) else pd.read_csv(f)

print("\nNama kolom:")
print(list(df.columns))
print("\n10 baris pertama:")
print(df.head(10).to_string())