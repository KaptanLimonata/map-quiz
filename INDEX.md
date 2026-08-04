# World Map Quiz - INDEX

## Durum: TAMAMLANDI (2026-08-04)
Teslim edilen dosya: `world-map-quiz.html` (205 KB, tek dosya, offline çalışır).

## Hedef
Rastgele sorulan ülkeyi dünya haritasında bulma oyunu. Masaüstü, mobil ve iOS Safari.
Tüm harita verisi HTML içine gömülü; internet veya kurulum gerekmez.

## Gereksinimler ve karşılanma durumu
1. Üstte her zaman görünen overlay, aranan ülke adı - tamam
2. Ülkeler rastgele, tekrarsız sırayla - tamam
3. Altta "Geç" butonu - tamam
4. 2 yanlış tıklamada doğruyu göster - tamam (ülkeye uçar, işaretler)
5. Rahat zoom/pan (pinch, tekerlek, çift dokunma, +/- butonları) - tamam
6. Estetik CSS - tamam (koyu okyanus teması, cam efektli paneller)
7. 194-200 ülke - 197 (193 BM üyesi + Vatikan, Tayvan, Kosova, Filistin)
8. Çok küçük ülkeler için tıklanabilir daireler - tamam
9. Doğru bilinen ülke yeşil yanıp beyaza döner ve öyle kalır - tamam

## Adımlar
- [x] 1. Ortam tespiti -> environment.md
- [x] 2. Natural Earth 50m verisi, 197 ülke seçimi + Somaliland/KKTC/Hong Kong/Makao birleştirme
- [x] 3. Basitleştirme (mapshaper %18) ve kompakt kodlama -> 17.7k nokta, 170 KB veri
- [x] 4. Canvas renderer, Mercator projeksiyon, pan/zoom
- [x] 5. Quiz mantığı, skor, dil değiştirici, bitiş ekranı
- [x] 6. CSS tasarım ve overlay
- [x] 7. Doğrulama (aşağıda)

## Doğrulama sonuçları
- Coğrafi veri: 35 bilinen şehirden 33'ü doğru ülkede (2 sapma kıyı şehri, basitleştirme
  kaynaklı, oynanışı etkilemiyor); 197/197 ülkenin iç noktası kendi poligonu içinde
- Hit test (mobil 375x812, tüm dünya görünümü): aranan ülke 197/197 ulaşılabilir,
  yanlış tıklamalar 197/197 doğru adlandırılıyor, okyanus tıklamaları etkisiz
- Oyun akışı: doğru cevap / iki yanlış / geç / beyaz kalıcılık / dil değiştirme - hepsi geçti
- Performans (pan sırasında, gerçek frame süresi): dünya görünümü 69 FPS, zoom'da 137 FPS
- Konsol hatası yok; teslim dosyasında hata ayıklama kodu yok

## Dosyalar
- `world-map-quiz.html` - teslim edilen oyun
- `tools/` - veriyi yeniden üreten pipeline (step1..step4 + template.html)
- `README.md` - kullanım ve yeniden üretme talimatı
- `environment.md` - araç zinciri ve veri kaynağı notları
- `history.md` - kök neden kayıtları

## Bilinen sınırlar
- Dünya görünümünde çok sıkışık bölgelerde (Küba/Jamaika, İtalya/San Marino) yanlış
  cevap verirken komşu seçilebilir; zoom yapınca düzelir. Aranan ülke her zaman doğru seçilir.
- Kıyı çizgileri %18 basitleştirilmiş; çok yüksek zoomda hafif köşeli görünür.
- Portrait telefonda tüm dünya gösterildiğinde üst/alt boşluk kalır (Mercator kare oranı).
