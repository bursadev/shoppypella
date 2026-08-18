# Shoppypella — Kickoff Sunumu (reveal.js)

İsviçre çok-satıcılı pazaryeri için uygulama başlangıç görüşmesi sunumu.
Dil: **Türkçe** (ekran adları Almanca korunmuştur). 28 slayt.

## Açmak
- En basit: `index.html` dosyasını çift tıklayıp tarayıcıda açın.
- Veya yerel sunucu ile (önerilir):
  ```
  cd shoppypella-praesentation
  python3 -m http.server 8000
  # tarayıcı: http://localhost:8000
  ```

## Kullanım (reveal.js)
- İlerle/geri: **→ / ←** veya **Boşluk**
- Genel bakış: **Esc** (veya **O**)
- Tam ekran: **F**  ·  Konuşmacı notları: **S**

## İçerik akışı
1. Başlık · 2. Gündem · 3. Shoppypella nedir? · 4. Pazaryeri analizi · 5. Sayfa haritası (sitemap)
- **A** Alıcı: Startseite, Kategorie-Seite, Produktdetail, Verkäufer-Shop (+ alt ekranlar)
- **B** Sepet & Kasa: Warenkorb & Kasse (+ checkout adımları / onay)
- **C** Kimlik doğrulama (5 ekran)
- **D** Mein Konto: genel bakış + alt sayfalar + Einstellungen (5 sekme)
- **E** Verkäufer: Registrierung, Dashboard (+ alt ekranlar)
- **F** Sistem / genel sayfalar
- Tasarım sistemi · Yol haritası (Faz 1 MVP + Faz 2 büyüme) · Teknik yaklaşım · Sonraki adımlar

**●** = Mockup hazır (gerçek görsel var)  ·  **○** = yeni tasarlanacak. (Hiçbir ekran henüz tasarlanıp uygulanmadı.)

## Dosyalar
- `index.html` — sunumun tamamı (kendi içinde, çevrimdışı çalışır)
- `reveal/` — reveal.js 5.1.0 (yerel)
- `screens/` — 8 ana ekranın gerçek görselleri (prototipten render edildi; navigator/cihaz çerçevesi olmadan)

> Görseller `Shoppypella.dc.html` prototipinden üretildi. Yalnızca çevrimiçi gereken tek şey
> başlık fontu (Hanken Grotesk, Google Fonts); internet yoksa sistem fontuna düşer.
