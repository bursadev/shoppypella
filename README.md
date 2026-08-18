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

Ürün görselleri ve katalog Pella Home'un gerçek ürünlerinden alınmıştır.

---

## Repo yapısı

```
docs/          GitHub Pages'in yayınladığı site (üretilmiş — elle düzenlemeyin)
components/    Design Component kaynakları (ProductCard, Thumb, Footer)
src/           Kaynak malzeme: orijinal paket + ürün fotoğrafları
build.py       docs/ dizinini üreten betik
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

`src/shoppypella-tr.html` kendi kendini açan tek dosyalık bir pakettir: UUID ile
adreslenen base64 varlıklardan oluşan bir manifest, ve her varlık referansının o
çıplak UUID olduğu bir şablon. Çalışma zamanında paketleyici her UUID'yi bir
`blob:` URL'ine çevirir.

Statik bir sunucuda buna gerek yok. `build.py` varlıkları diske yazar ve
UUID'leri göreli yollara çevirir. Bu, pakette bozuk olan `assets/imgNN.jpeg`
ürün referanslarını da onarır — paket içinde bunları çözecek bir dosya sistemi
yoktu.

Paket ayrıca `ProductCard`, `Thumb` ve `Footer` bileşenlerine atıfta bulunuyor
ama hiçbirini içermiyordu; bu yüzden tüm ürün ızgaraları ve küçük görseller boş
kutu olarak görünüyordu. dc-runtime `<dc-import name="X">` ifadesini `./X.dc.html`
dosyasını çekerek çözer — statik bir sunucunun gerçekten sunabileceği bir şey.
Bu üç bileşen `components/` altında yazılmıştır.

Çalışma zamanı React, ReactDOM ve Babel'i unpkg'den yükler, yani sayfanın
internet bağlantısına ihtiyacı vardır.
