# Implementation Requirements — Shoppypella.com (Client Feedback)

This document translates the client's requirements list into concrete implementation instructions for the production site **shoppypella.com**. The design reference for all UI decisions is `Shoppypella.dc.html` (see README.md). Items below are ordered as in the client's brief; each states what the mockup already demonstrates and what must be built in production.

## 1. Design / Mockup Alignment
- Implement the production UI to match the mockup in this package (all 8 screens: Home, Category, Product Detail, Seller Store, Seller Signup, Seller Dashboard, Customer Account, Cart & Checkout).
- Must be fully **responsive** across desktop, tablet and mobile. The mockup demonstrates desktop and mobile (device toggle); tablet behavior: layouts use flex-wrap with fluid bases — verify no element collapses at intermediate widths. Known pattern to preserve: the header search has `min-width:220px`, the header row wraps (`flex-wrap:wrap`), and the "Ara" button is `flex-shrink:0`; keep equivalent constraints in production CSS.
- On the Seller Store page, only the avatar tile overlaps the cover gradient (`margin-top:-58px` on the avatar); the store title/badges sit fully below the gradient on white.

## 2. Price Display
- **Normal price: black** (`#1B1A18` / ink token).
- **Discounted price: red** (`#D92D20`).
- Discounted products additionally show the original price **struck through** in muted gray (`#B8B3AB`) next to the red price, plus (on product detail) a savings chip ("CHF 4.– tasarruf").
- Implemented in the mockup via a `priceColor` field on product data (`hasOld ? '#D92D20' : ink`) — reproduce as a derived value in the product presenter/component, not hard-coded per product.

## 3. Influencer Integration
The mockup's Seller Dashboard contains an **"Influencer" nav item** and an **"Influencer Kampanyaları" panel** — build a real system behind it:
- CRUD for influencer campaign codes (code, influencer handle, platform, discount %, validity, usage limits). Mockup shows: ELIF10 (@elifstyle, Instagram, %10), LARA15 (@larahome, TikTok, %15), MELIS10 (@melisbeauty, YouTube, %10) + "+ Yeni kod oluştur" button.
- Codes are redeemable in checkout: the cart summary's code field is labeled **"İndirim / influencer kodu"** — one input for both regular and influencer codes; the backend distinguishes them.
- Per-influencer tracking: uses count and attributed revenue (mockup columns: Kod, Influencer, Platform, İndirim, Kullanım, Ciro). Attribute orders that redeem a code to that influencer; consider UTM/ref-link attribution as a later extension.
- Architecture must allow adding new campaign types (percentage, fixed amount, free shipping) without schema rework.

## 4. Domain
- Primary domain: **shoppypella.com** (mockup URLs use it throughout; seller side on `satici.shoppypella.com`).
- Configure for global use (no country-locked TLD logic; language/currency handled in-app).
- **SSL mandatory site-wide**: HTTPS redirect + HSTS. The mockup footer shows an "SSL güvenli" note; the real trust indicator is the browser padlock.
- Redirect `www.shoppypella.com` → `shoppypella.com` (or vice-versa — pick ONE canonical host) with 301s.

## 5. Social Media Integration
- Footer contains icon links (38×38 rounded tiles, #2a2825 bg) for **Instagram, TikTok, Facebook, Pinterest, YouTube** → point each to the real account URLs (mockup uses `https://instagram.com/shoppypella` etc. as placeholders — replace with actual handles).
- Icons are inline SVGs in `Footer.dc.html`; in production use the brand's icon set or the official brand SVGs (respect each platform's brand guidelines).
- Optional (client: "gerektiğinde"): an embedded social feed section (e.g. Instagram grid) — not in the mockup; design before building.

## 6. Cargo / Shipment Tracking
- Customers must see shipment status per order. Mockup (Hesabım → Siparişlerim): orders with status "Yolda" show **carrier + clickable tracking number** ("Swiss Post · 99.00.123456.78") under the order date; the order card also has a "Kargo takip" action.
- Production: store carrier + tracking number per shipment; link to the carrier's tracking page (Swiss Post, DPD, DHL …) or an embedded tracking view.
- Integrate carriers via their APIs where possible (e.g. Swiss Post tracking API) so status updates automatically; fall back to manual tracking-number entry by the seller in the Seller Dashboard (Kargo section).
- Status chips in the mockup: Yolda (orange tint), Teslim edildi (green tint) — extend with the carrier's real state machine (etiket oluşturuldu, taşımada, dağıtımda, teslim edildi, iade).

## 7. Legal Texts
- The legal documents are **provided by the client's lawyer — integration only, do not draft content**.
- Footer has a dedicated **"Yasal"** column with: Gizlilik Politikası, KVKK / Veri Koruma, Çerez Politikası, Kullanım Koşulları, Mesafeli Satış Sözleşmesi, İade & Değişim Politikası, Kargo & Teslimat Koşulları. Each becomes a real page/route.
- Checkout: below the "Siparişi onayla" button there is a consent line linking to Mesafeli Satış Sözleşmesi and İade Politikası — keep it (or make it a required checkbox if legal requires explicit consent).
- Add a cookie-consent banner wired to the Çerez Politikası (not in the mockup; required for EU/CH visitors — keep it visually minimal, brand orange accent).
- Surface the relevant texts in other flows where applicable: seller signup already links Satıcı Sözleşmesi + Gizlilik Politikası at the AGB checkbox.

## 8. General Technical Requirements (production checklist)
- All integrations (payment, cargo, influencer codes, social) tested together.
- Cross-device testing: desktop, tablet, mobile (real devices + emulators).
- Performance: optimize page speed (image lazy-loading, responsive image sizes, code splitting; product images are 1:1 squares — serve as WebP/AVIF).
- SEO basics: semantic HTML, per-page titles/meta, canonical URLs on one host, product structured data (schema.org Product/Offer), sitemap, robots.txt, hreflang if multi-language.
- Test all forms, buttons, links and the full order/payment flow.
- Fix any technical errors degrading UX (console errors, broken links, layout collapses at intermediate breakpoints).

**Goal:** a professional, trustworthy, globally usable and scalable e-commerce platform on shoppypella.com.
