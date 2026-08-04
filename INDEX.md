# World Map Quiz - INDEX

## Durum: TAMAMLANDI (2026-08-04)
Teslim: `world-map-quiz.html` (205 KB, tek dosya, offline).
Repo: https://github.com/KaptanLimonata/map-quiz (private) · main @ 85a4a3c

Rastgele sorulan ülkeyi dünya haritasında bulma oyunu; masaüstü, mobil ve iOS.
İstenen 9 gereksinimin tamamı karşılandı (özellik listesi: README.md).
Veri hattı kuruldu ve çalışır durumda: Natural Earth 50m -> 197 ülke -> mapshaper %18
-> 17.7k nokta -> HTML içine gömme (tools/, adımlar README'de).

## Doğrulama (tarayıcıda çalıştırıldı)
- Tıklama: aranan ülke 197/197 ulaşılabilir, yanlış tıklamalar 197/197 doğru
  adlandırılıyor, okyanus etkisiz (mobil 375x812, tüm dünya görünümü)
- Coğrafi veri: 35 şehirden 33'ü doğru ülkede (2 sapma kıyı şehri, oynanışı etkilemiyor);
  197/197 iç nokta kendi poligonunda
- Akıcılık: dünya görünümü 69 FPS, zoom'da 137 FPS (kaydırma sırasında gerçek kare süresi)
- Oyun akışı ve TR/EN geçişi geçti; konsol hatası ve hata ayıklama kodu yok

## Dosyalar
- `world-map-quiz.html` - teslim edilen oyun
- `tools/` - veriyi yeniden üreten hat (step1..step4 + template.html; asıl kaynak template)
- `README.md` - kullanım, yeniden üretme, detay/hız dengesi tablosu
- `environment.md` - araç zinciri ve veri kaynağı notları
- `history.md` - kök neden kayıtları

## Bilinen sınırlar
- Dünya görünümünde çok sıkışık bölgelerde (Küba/Jamaika, İtalya/San Marino) yanlış
  cevap verirken komşu seçilebilir; zoom yapınca düzelir. Aranan ülke her zaman doğru seçilir.
- Kıyı çizgileri %18 basitleştirilmiş; çok yüksek zoomda hafif köşeli görünür.
- Portrait telefonda tüm dünya gösterildiğinde üst/alt boşluk kalır (Mercator kare oranı).
