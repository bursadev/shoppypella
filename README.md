# Shoppypella — interaktif prototip

Bir İsviçre pazaryeri konsepti için tıklanabilir prototip. 8 ekran, masaüstü ve
mobil görünüm, tamamı Türkçe.

**Canlı:** https://bursadev.github.io/shoppypella/

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
docs/           GitHub Pages'in yayınladığı site (üretilmiş — elle düzenlemeyin)
src/handoff/    Tasarım paketi: prototipin kaynağı (Design Component'ler + görseller)
src/fonts/      Kendi sunucumuzdan servis edilen woff2 dosyaları + @font-face css
src/photos/     Orijinal ürün fotoğrafları (arşiv; derlemede kullanılmıyor)
build.py        docs/ dizinini üreten betik
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

## Müşteri talepleri

Tasarım paketindeki `REQUIREMENTS.md` müşterinin istek listesini üretim
talimatlarına çevirir. Prototipte görünenler:

- **Fiyat gösterimi** — normal fiyat siyah, indirimli fiyat kırmızı
  (`#D92D20`), yanında üstü çizili eski fiyat.
- **Influencer sistemi** — satıcı panelinde "Influencer" menüsü ve kampanya
  kodu tablosu; sepette tek bir "İndirim / influencer kodu" alanı.
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
gösterir.
