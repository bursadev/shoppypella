# Shoppypella — interaktif prototip

Bir İsviçre pazaryeri konsepti için tıklanabilir prototip. 8 ekran; masaüstü,
tablet ve mobil görünüm; tamamı Türkçe.

**Canlı:** https://bursadev.github.io/shoppypella/
**Preismodell (fiyat modeli):** https://bursadev.github.io/shoppypella/preismodell/

| Ekran | Ekran |
| --- | --- |
| Ana Sayfa | Satıcı Mağazası |
| Kategori Sayfası | Hesabım |
| Ürün Detayı | Sepet & Ödeme |
| Satıcı Kaydı | Satıcı Paneli |

Ürün görselleri ve katalog Pella Home'un gerçek ürünlerinden alınmıştır; diğer
kategorilerdeki ürünler pazaryerinin çok satıcılı yapısını göstermek için
konulmuş temsili örneklerdir.

---

## Repo yapısı

```
docs/            GitHub Pages'in yayınladığı site (üretilmiş — elle düzenlemeyin)
src/handoff/     Tasarım paketi: prototipin kaynağı (Design Component'ler + görseller)
src/preismodell/ Fiyat modeli sayfası (tek dosya, çalışma zamanı yok) → docs/preismodell/
src/fonts/       Kendi sunucumuzdan servis edilen woff2 dosyaları + @font-face css
src/photos/      Orijinal ürün fotoğrafları (arşiv; derlemede kullanılmıyor)
build.py         docs/ dizinini üreten betik
```

## Derleme

```sh
pip install pillow
python3 build.py
```

Yerelde denemek için:

```sh
cd docs && python3 -m http.server 8000
```

`file://` üzerinden **çalışmaz** — çalışma zamanı bileşenleri `fetch` ile
yüklediği için bir HTTP sunucusu gerekir.

## Nasıl çalışıyor

`src/handoff/` bir Design Component paketidir: kök bileşen
`Shoppypella.dc.html` (8 ekranın tamamı), onun içe aktardığı üç kardeş bileşen
(`ProductCard`, `Thumb`, `Footer`), çalışma zamanı (`support.js`) ve ürün
görselleri. Bir dizinden açılmak üzere tasarlandığı için statik bir sunucuda
neredeyse olduğu gibi çalışır.

`build.py` yalnızca şunları değiştirir:

- çalışma zamanını `assets/dc-runtime.js` adıyla kopyalar, sayfaya gerçek bir
  başlık, açıklama, sosyal önizleme ve favicon ekler;
- iki Google Fonts bağlantısını `src/fonts` içindeki @font-face kurallarıyla
  değiştirir — böylece site bir font CDN'ine bağlı kalmaz;
- ürün fotoğraflarını web için küçültür ve yalnızca gerçekten kullanılan
  görselleri kopyalar.

Geri kalan her şey olduğu gibi kopyalanır; tasarım paketi tek doğru kaynak
olarak kalır. dc-runtime `<dc-import name="X">` ifadesini `./X.dc.html`
dosyasını çekerek çözdüğü için kardeş bileşenler `index.html` ile aynı dizine
konur.

Çalışma zamanı React, ReactDOM ve Babel'i unpkg'den yükler, yani sayfanın
internet bağlantısına ihtiyacı vardır.

## Fiyat modeli

`src/preismodell/index.html` teklif görüşmesi için etkileşimli fiyat modelidir:
üç yol (junior / orta düzey / senior), aşama başına **tavan fiyat**, senior için
%5 / %10 / %15 ciro payı seçeneği ve tek tek seçilebilen aşamalar. Almanca,
İngilizce ve Türkçe; dil sağ üstten değişir. Sayfa tek dosyadır, kütüphane
yüklemez; `build.py` Google Fonts bağlantılarını `src/fonts` içindeki Hanken
Grotesk ve IBM Plex Mono kurallarıyla değiştirip `docs/preismodell/` altına
yazar. **Influencer Marketplace** (17.09.2026) altı lansman aşamasının üstüne kendi
tavanıyla ayrı bir aşama satırı olarak eklidir; varsayılan seçili, işareti
kaldırılabilir. "Anpassen" altındaki kaydırıcılar tarayıcıda kalır, sunucuya bir şey
gitmez; aşama ağırlıkları yalnızca adrese `#modell` eklenince görünür.

## Müşteri talepleri

Tasarım paketindeki `REQUIREMENTS.md` müşterinin istek listesini üretim
talimatlarına çevirir. Prototipte görünenler:

- **Fiyat gösterimi** — normal fiyat siyah, indirimli fiyat kırmızı
  (`#D92D20`), yanında üstü çizili eski fiyat.
- **Influencer sistemi** — satıcı panelinde "Influencer" menüsü ve kampanya
  kodu tablosu; sepette tek bir "İndirim / influencer kodu" alanı. (Müşterinin
  17.09.2026 geri bildirimiyle bu, satıcının ürün başına komisyon açtığı üç
  taraflı bir **Influencer Marketplace**'e genişledi — satıcı, influencer ve
  yönetim panelleri; prototip henüz eski hâli gösteriyor.)
- **Kargo takibi** — Hesabım › Siparişlerim'de taşıyıcı adı, tıklanabilir takip
  numarası ve "Kargo takip" aksiyonu; durum etiketleri (Yolda / Teslim edildi).
- **Sosyal medya** — footer'da Instagram, TikTok, Facebook, Pinterest, YouTube
  bağlantıları.
- **Yasal metinler** — footer'da ayrı "Yasal" sütunu (Gizlilik, KVKK, Çerez,
  Kullanım Koşulları, Mesafeli Satış, İade, Kargo) ve ödeme adımında onay
  satırı. Metinlerin kendisi müşterinin hukukçusundan gelecek.
- **Alan adı** — ekran adresleri `shoppypella.com`, satıcı tarafı
  `satici.shoppypella.com`.

Bunların arkasındaki gerçek sistemler (kampanya kodu CRUD'u ve atıfı, taşıyıcı
API'leri, SSL/HSTS, çerez onayı, SEO) üretim işidir; prototip yalnızca arayüzü
gösterir. Üretim sitesi `shoppypella.com` ayrı bir WordPress/WooCommerce
kurulumudur ve bu repoda değildir.

### Yasal sayfa adresleri

Footer'daki yasal bağlantılar aşağıdaki adreslere gider. Üretimde bu slug'larla
sayfa açılması gerekir:

```
/gizlilik-politikasi/          /kullanim-kosullari/
/kvkk-veri-koruma/             /mesafeli-satis-sozlesmesi/
/cerez-politikasi/             /iade-degisim-politikasi/
                               /kargo-teslimat-kosullari/
```

## Cihaz modları

Navigatördeki Desktop / Tablet / Mobil düğmesi çerçeve genişliğini değiştirir:
1240 px, 834 px ve 402 px. Tablet modunda başlıktaki "Satıcı ol" bağlantısı
gizlenir, iki sütunlu yerleşimlerin flex tabanları küçülür ve panel KPI'ları
2×2 dizilir — böylece ara genişliklerde hiçbir sütun alt satıra düşmez.

Prototipin kendisi sabit genişlikli bir çerçeve olduğu için tarayıcı penceresini
daraltmak tablet modunu tetiklemez; tablet yerleşimini görmek için düğmeyi
kullanın. Üretimde bunların karşılığı gerçek CSS breakpoint'leridir.

## Tasarım paketine göre farklarımız

`src/handoff/` teslim edilen paketin kopyasıdır; üzerine yapılan düzeltmeler:

- **Tablet modu** — üçüncü bir cihaz genişliği ve ona bağlı sütun tabanları.
- **`loading="lazy"` + `decoding="async"`** — tüm ürün görsellerinde.
- **Gerçek bağlantılar** — footer'daki yasal metinler ve sipariş takip numarası
  artık `<a>`; takip numarası taşıyıcının (Swiss Post / DPD / DHL) sorgu
  adresine gider. Sosyal medya bağlantıları yeni sekmede açılır.
- **Fiyatlar satır ortasından bölünmüyor** — dar kartlarda `white-space:nowrap`.
- **`&amp;` hatası** — satıcı kaydı sayfasındaki iki başlık `&amp;` yerine artık
  `&` gösteriyor (aynı iki başlık Türkçeleştirildi).
