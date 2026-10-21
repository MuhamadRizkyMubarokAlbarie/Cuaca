import glob
import sys
import numpy as np
import pandas as pd


def baca_bmkg_bulanan(path):
    """Baca file Data Iklim Bulanan BMKG (ada blok info stasiun di atas tabel)."""
    mentah = pd.read_excel(path, header=None)
    idx = mentah.index[mentah.iloc[:, 0].astype(str).str.strip() == "Periode"][0]
    tabel = mentah.iloc[idx + 1:, :2].copy()
    tabel.columns = ["periode", "rr"]
    tabel = tabel[tabel["periode"].astype(str).str.match(r"^\d{4}-\d{2}$")]
    tabel["tanggal"] = pd.to_datetime(tabel["periode"] + "-01")
    tabel["rr"] = pd.to_numeric(tabel["rr"], errors="coerce")
    tabel["rr"] = tabel["rr"].replace([8888, 9999], np.nan)
    return tabel[["tanggal", "rr"]]


if __name__ == "__main__":
    berkas = sorted(glob.glob("data/raw/DataIklimBulanan*.xlsx"))
    if not berkas:
        sys.exit("Tidak ada file DataIklimBulanan*.xlsx di data/raw/")
    df = pd.concat([baca_bmkg_bulanan(f) for f in berkas])
    df = (df.drop_duplicates("tanggal").sort_values("tanggal")
            .set_index("tanggal").asfreq("MS"))
    df["bulan"] = df.index.month
    df["tahun"] = df.index.year

    print("Jumlah bulan:", len(df), "| hilang:", int(df["rr"].isna().sum()))
    print("Rentang:", df.index.min().date(), "-", df.index.max().date())
    print(df.groupby("bulan")["rr"].agg(["count", "mean", "std", "min", "max"]).round(1))
    df.to_csv("data/curah_hujan_bulanan_bersih.csv")