# Cuaca: Simulasi Curah Hujan Harian

Deskripsi Simulasi dan Pemodelan
Proyek ini mensimulasikan curah hujan bulanan di Stasiun Meteorologi Citeko Kabupaten Bogor menggunakan rantai Markov tiga keadaan dan simulasi Monte Carlo.

- Keadaan bulan: Kering (< 100 mm), Lembab (100-200 mm), Basah (> 200 mm).
- Matriks transisi dihitung dari 23 perpindahan antarbulan pada data BMKG.
- Curah hujan tiap bulan simulasi diambil Random dari data bulan
  yang berkeadaan sama.
- Simulasi dijalankan 5.000 kali untuk 12 bulan ke depan (Okt 2026 - Sep 2027)
  dan 600 bulan untuk validasi.

Pokok Permasalahan: berapa peluang bulan basah dan bulan kering ke depan
setelah periode kering Juni-September 2026?

Hasil
- Proporsi keadaan pada simulasi mendekati data (basah 65% vs 62,5%).
- Rata-rata bulanan simulasi 266 mm vs data 256 mm; simpangan baku 158 vs 165 mm.
- Peluang bulan basah naik dari 26% (Okt 2026) menjadi sekitar 63% (setelah 12 bulan).
- Rata-rata curah hujan simulasi menuju sekitar 260 mm/bulan.

Keterbatasan
- Data hanya 24 bulan Saja (BMKG Data Online hanya menyediakan Data Periode 2024-2026).
- Peluang transisi tidak mengenal musim.
- Transisi Basah ke Kering bernilai 0 karena belum teramati, Tapi bukan mustahil.
- Rentang 90% sangat lebar karena nilai simulasi Terbatas Oleh Datanya.
- Hasil ini adalah skenario simulasi, bukan ramalan cuaca yaa.

Sumber Data
- Sumber: BMKG Data Online (https://dataonline.bmkg.go.id)
- Stasiun: Staisun Meteorologi Citeko Kabupaten Bogor
- Rentang data: 2024-2026
- Tanggal unduh: 22-10-2026

Bahasa Pemrograman
Python (pandas, numpy, scipy, matplotlib)
