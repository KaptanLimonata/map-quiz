# Ortam

Tespit tarihi: 2026-08-04

- OS: Windows 11 Pro 10.0.26200
- Shell: PowerShell 5.1 (`&&` ve ternary yok, `;` + `if ($?)` kullan). Git Bash de mevcut.
- Python: 3.14 - `C:\Python314\python.exe`
- Node: `C:\Program Files\nodejs\node.exe`
- mapshaper: global npm paketi olarak kuruldu -> `C:\Users\Burak\AppData\Roaming\npm\mapshaper.ps1`
  (topoloji koruyan harita basitlestirme; komsu ulke sinirlarinda bosluk olusturmaz)
- Ag erisimi: var, ancak arac cagrilari varsayilan olarak sandbox'ta calisiyor.
  Indirme yaparken `dangerouslyDisableSandbox: true` gerekiyor.
- Proje git deposu degil.

## Kullanilan veri
Natural Earth vector, GitHub raw:
`https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson`
- 242 feature, 99.613 koordinat noktasi, 3 MB
- Faydali alanlar: NAME_EN, NAME_TR (Turkce adlar hazir), ISO_A3, TYPE, CONTINENT
- Dikkat: Israil, Kazakistan ve Kuba TYPE alaninda "Sovereign country" degil
  ("Disputed" / "Sovereignty"); ulke listesi cikarirken elle eklenmeleri gerekir.
