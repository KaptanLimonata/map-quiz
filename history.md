# Çözüm Geçmişi

Yalnızca tekrar karşılaşılabilecek veya bilinmezse zaman kaybettirecek kök nedenler.

---

2026-08-04 · Küçük ülke daireleri büyük komşuya tıklamayı engelliyordu
Sorun: Fransa'nın ortasına tıklayınca İsviçre, İtalya'ya tıklayınca San Marino seçiliyordu; 197 ülkenin 19'u kendi merkezinden tıklanamıyordu.
Kök neden: Dünya görünümünde mikro devlet daireleri fiziksel olarak komşusunun üzerinde. Hit test'te daireye koşulsuz öncelik verilmişti; tolerans daraltmak da işe yaramadı çünkü San Marino gerçekten İtalya'nın içinde.
Çözüm: hitTest artık o an sorulan ülkenin id'sini alıyor (`preferId`). Önce hedefle eşleşen aday, sonra gerçek geometri, en son daire. Sonuç: aranan ülke 197/197, yanlış tıklamalar 197/197 doğru adlandırılıyor.
"Daire toleransını küçültmek yeter" sanılıyordu, yetmedi.

2026-08-04 · Canvas'ta tek birleşik Path2D stroke, ayrı ayrı stroke'tan yavaş
Sorun: Pan sırasında 28 FPS.
Kök neden: Tüm ülke sınırlarını tek Path2D'de toplayıp tek `stroke()` çağırmak, 197 ülkeyi ayrı ayrı stroke etmekten ~5x YAVAŞ (ölçüm: 22ms vs 4ms). Sezgiye ters; "daha az çağrı = daha hızlı" varsayımı burada geçersiz.
Çözüm: Görünür ülkeler tek tek stroke ediliyor (culling'den de faydalanıyor). 28 -> 69 FPS.
Not: `fill` neredeyse bedava (197 fill = 0.2ms); maliyet stroke'ta.

2026-08-04 · Uzak ada/bölgeler zoom yapılınca kayboluyordu
Sorun: Fransız Guyanası, Alaska, Kaliningrad'a zoom yapılınca çizilmiyordu.
Kök neden: Viewport culling, ülkenin yalnızca EN BÜYÜK parçasının bbox'ını kullanıyordu. Fransa'nın bbox'ı Avrupa'da olduğu için Güney Amerika'ya bakarken Fransa tamamen atlanıyordu.
Çözüm: Init'te tüm parçaları kapsayan ayrı bir `full` bbox hesaplanıyor; culling onu kullanıyor, zoom/odaklama ise ana kütlenin bbox'ını.

2026-08-04 · Tarayıcı önizlemesi eski dosyayı gösteriyordu (test tuzağı)
Sorun: Kod değişiklikleri test sonuçlarına yansımadı; saatlerce eski sürüm test edildi.
Kök neden: `location.reload()` file:// önbelleğinden eski HTML'i veriyor. Sayfa uzunluğu kontrol edilmezse fark edilmiyor.
Çözüm: Yeniden yüklerken `navigate` aracını `tabId` + `force` ile kullan. Her testin başında sürümü doğrula (ör. yeni eklenen bir fonksiyon adının kaynakta olup olmadığı).

2026-08-04 · setTimeout tabanlı FPS ölçümü yanıltıcı
Sorun: Performans 40ms/frame ölçüldü, ama çizim bench'i 0.2ms diyordu.
Kök neden: Test döngüsü `await sleep(16)` ile ilerliyordu; ölçülen şey setTimeout gecikmesiydi, uygulamanın frame süresi değil.
Çözüm: Ölçüm ve olay gönderimi `requestAnimationFrame` içinden yapılmalı. Ayrıca boşta rAF aralığı ölçülüp taban çizgisi (bu makinede 7ms/143Hz) doğrulanmalı.
