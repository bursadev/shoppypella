# Handoff: Shoppypella — Multi-Vendor Marketplace (Switzerland)

> **See also `REQUIREMENTS.md`** — the client's implementation requirements (price display rules, influencer system, domain/SSL, social media, cargo tracking, legal texts, technical checklist). It complements this design README.

## Overview
Shoppypella is a multi-vendor e-commerce marketplace for the Swiss market (think Galaxus / Hepsiburada / Amazon-style), built around the seller brand **Pella Home** (household, cleaning & cosmetic products). The prototype covers the 8 core screens of the buyer + seller experience, in **German**, priced in **CHF**, responsive for **desktop and mobile**, with the brand color **orange**. **All on-screen copy is in Turkish** (priced in CHF for the Swiss market).

A live "mockup navigator" wraps the prototype: a left rail to jump between the 8 screens, a Desktop/Mobil device toggle, and four design-system selectors (Font / Radius / Background / Accent) used to trial visual directions. **The navigator and device-frame chrome are presentation tooling only — they are NOT part of the product UI** and must not be reproduced in the real app.

## About the Design Files
The file in this bundle (`Shoppypella.dc.html` plus `ProductCard.dc.html`, `Footer.dc.html`, `Thumb.dc.html`, and `assets/`) is a **design reference created in HTML** — a prototype showing intended look and behavior, not production code to copy directly. The `.dc.html` format is a self-contained streaming-component prototype format; it is **not** a framework you should adopt.

The task is to **recreate these designs in the target codebase's existing environment** (React, Vue, Svelte, SwiftUI, etc.) using its established component library, routing, and state patterns. If no front-end environment exists yet, choose the most appropriate stack for a content-heavy commerce SPA (e.g. React + a router + a component lib) and implement there. Treat the HTML as the source of truth for layout, spacing, color, type and copy.

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, Turkish copy and interactions are all specified. Recreate the UI pixel-accurately using the codebase's existing primitives. The only thing intentionally exploratory is the **theming layer** (see Design Tokens → Theming) — productionize the default (Classic: solid orange, white background, Hanken Grotesk, normal radius) unless the team selects another combination.

## Global Layout & Shell

### Marketplace header (buyer screens: Home, Category, Product, Store, Account, Cart)
- **Desktop** (sticky, z above content):
  1. Dark utility strip (`--ink` #1B1A18, text #cfcac3, 12.5px): truck icon + "Kostenloser Versand ab CHF 49.–" · "Lieferung in die ganze Schweiz" · "30 Tage Rückgaberecht", centered with `·` separators.
  2. Main bar (white, 1px bottom border #ECE9E4, padding 16px 28px, gap 22px): logo left; a **large search** (`flex:1`, max-width 840px, height 52px, 2px solid #1B1A18 border, radius 13px) containing a search icon, input ("Wonach suchen Sie? z. B. Mikrofasertücher", 15px) and an orange "Suchen" button (padding 0 30px); right cluster: "Pella verkaufen? / **Verkäufer werden**" (orange), account ("Anmelden / Mein Konto" + user icon), cart pill (bg #FFF1E8, cart icon + "CHF 38.20" + count badge "3").
  - Note: there is **no** category nav bar under the header and **no** "Alle Kategorien" dropdown inside the search (both were intentionally removed).
- **Mobile** (≤ ~430px frame):
  - Orange strip: "Gratis Versand ab CHF 49.–".
  - Compact bar: hamburger (left), logo (center-left), cart (right, with badge).
  - Search row: a tappable pill ("Wonach suchen Sie?", bg #F6F3EF, radius 11px).
  - **Bottom tab bar** (sticky bottom): Start (home), Kategorien (list), Warenkorb (cart + badge), Konto (user). Active = orange, inactive = #9A958D.

### Category sidebar (Home, desktop) — Galaxus-style
- A bordered card (`aside`, border 1px #ECE9E4, radius var, **solid white background**, overflow hidden), width ~234px (min 212 / max 280).
- Header row: bg #FAF8F5, menu icon (orange) + "Alle Kategorien", 14px/800.
- Each category = a clickable row (icon in orange + name + chevron). Rows are an **accordion**: clicking expands that category to reveal an indented sub-list (sub bg #FAFAF8, dotted bullet + sub-name, padding-left 47px). Only **one** category is open at a time; the open row is orange (#F2660F) with a down-chevron (⌄), closed rows are #4a4742 with ›.
- **Mobile**: the sidebar is hidden; the hamburger opens it as a **left drawer overlay** (panel width 84%, max 340px, solid white, shadow; dark backdrop rgba(27,26,24,.45) on the right that closes on tap; ✕ button top-right). Same accordion; tapping a sub-item navigates to the category page and closes the drawer.

### Footer (buyer screens)
Dark (`--ink`), 4 columns: brand blurb + payment chips (TWINT / VISA / Mastercard / Rechnung); "Einkaufen", "Verkaufen", "Service" link lists; bottom bar "© 2026 Shoppypella AG · Zürich, Schweiz" and "🌐 Schweiz · Deutsch · CHF".

## Screens / Views

> **Language note:** The UI is implemented in **Turkish**. Some copy is quoted in German in the per-screen notes below (an earlier draft language); those German strings map 1:1 to the Turkish text now in the `.dc.html` files. **Treat the `.dc.html` files as the source of truth for exact wording.** Key terms: Verkäufer→Satıcı, Warenkorb→Sepet, Kasse→Ödeme, Bestellungen→Siparişler, Lieferung→Teslimat, Zahlung→Ödeme, Rückgabe→İade, Bewertungen→Yorumlar, Haushalt & Wohnen→Ev & Yaşam.

### 1. Startseite (Home) — `shoppypella.ch`
- **Purpose**: entry point, browse categories and featured products.
- **Layout**: content padding 22px 24px; a flex row → left **category sidebar** + right **main column** (`flex:3 1 540px`). Below the row (full width): USP trust strip + footer.
- **Hero** (feature card, radius 20px, padding 42×40, min-height 240): eyebrow "WILLKOMMEN BEI SHOPPYPELLA" (orange, 13px/800, tracking .06em), headline "Der Marktplatz der Schweiz." (40px/900, max 16ch), sub "Tausende Produkte von geprüften Schweizer Verkäufern – von Elektronik bis Haushalt." (16px, #5a564f), CTA "Jetzt entdecken →" (orange button, white text). Default bg = light tint gradient (#FFF1E8 → #FFE4D3). *(Accent=Verlauf turns this into an orange→fiery-red gradient with white text — see Theming.)*
- **Beliebte Produkte**: section header (h2 22px/900 + "Alle ansehen →") then a **4-up product grid** (each card `flex:1 1 22%; min-width:150px`; gap 14px → 4 per row desktop, 2 on mobile), 8 items.
- **Neu eingetroffen**: same header + same 4-up grid, 4 items.
- **USP strip**: 4 cards (`flex:1 1 200px`, bg #FAF8F5, border #ECE9E4, radius 14px): truck "Schweizweit geliefert / Gratis ab CHF 49.–"; rotate "30 Tage Rückgabe / Einfach & kostenlos"; lock "Sichere Zahlung / TWINT · Karte · Rechnung"; message "Support DE/FR/IT / Mo–Fr 8–18 Uhr".

### 2. Kategorie-Seite (Category) — `shoppypella.ch/c/haushalt-wohnen`
- **Purpose**: browse/filter products in a category.
- Breadcrumb: Startseite › **Haushalt & Wohnen** › Reinigung & Pflege.
- **Banner** (feature card, light tint gradient, radius var, padding 24×28): h1 "Haushalt & Wohnen" (28px/900) + "248 Produkte in 5 Unterkategorien · 32 geprüfte Verkäufer". *(Verlauf accent → gradient bg, white text.)*
- **Subcategory pills** row: label "Unterkategorie:" + pills [Alle] [**Reinigung & Pflege** (active=orange)] [Aufbewahrung] [Raumdüfte] [Heimtextilien] [Beleuchtung] (inactive = white, border #E2DDD5, radius 20px).
- **Body**: flex row → **filter sidebar** (border card, radius 16px, padding 18): "Filter"; Preis (CHF) range with two inputs + a track with two orange thumbs (8%–70%); checkbox groups: Unterkategorie (Reinigung & Pflege ✓, Aufbewahrung, Raumdüfte, Heimtextilien), Bewertung (★4 & mehr ✓, ★3 & mehr), Verkäufer (Pella Home ✓, CleanPro CH, HausGut), Verfügbarkeit (Sofort lieferbar ✓, Gratis Versand). Checked = orange fill + white ✓; counts right-aligned in #B8B3AB.
- **Right**: sort bar (bg #FAF8F5: "9 von 248 Produkten" + "Sortieren: Beliebtheit ▾") then product grid (`flex:1 1 180px; max 230`), 9 items; pagination ‹ 1 2 3 … 28 › (active 1 = orange).

### 3. Produktdetail (Product) — `shoppypella.ch/p/london-blue-250ml`
- **Purpose**: view & buy a product.
- Breadcrumb: Startseite › Raumdüfte › **London Blue 250 ml**.
- **Gallery** (left, `flex:1 1 360`, `flex-direction:row-reverse`): main image tile (bg #FAF8F5, aspect 1:1, radius 18, "−24%" badge top-left) + a column of 4 thumbnails (68×68, active border orange).
- **Buy box** (right, `flex:1 1 360`): seller chip "Pella Home ✓ Geprüft" (links to store); h1 "Lufterfrischer „London Blue" – Raum- & Textilduft 250 ml" (27px/900); rating "★★★★★ 4.7 · 128 Bewertungen | 340+ verkauft"; price block **CHF 12.90** (34px/900) + struck CHF 16.90 + "Sie sparen CHF 4.–" chip + "inkl. MwSt. · zzgl. Versand"; Duftrichtung chips (London Blue active, Rose Paris, Lavendel, Vanille); quantity stepper (− 1 +) + "● Auf Lager" (green #2E7D5B); actions: **In den Warenkorb** (orange, flex 2), **Sofort kaufen** (dark, flex 1), heart button; delivery card (3 rows: truck "Lieferung Mi, 2. Juli", package "Verkauf & Versand durch Pella Home", rotate "30 Tage kostenlose Rückgabe").
- **Below**: tabs (Beschreibung active / Bewertungen (128) / Versand); description paragraphs; spec table (2-col key/value: Inhalt 250 ml, Anwendung Raum & Textil, Duftdauer bis 24 h, Herkunft, Verkäufer, Artikel-Nr.); **ratings panel** (4.7 big + 5-bar histogram [78/15/4/2/1] + 3 verified reviews with name·city, ★, date, text). Then "Das könnte Ihnen auch gefallen" product grid.

### 4. Verkäufer-Shop (Seller store) — `shoppypella.ch/shop/pella-home`
- **Purpose**: a seller's storefront.
- **Cover** banner (150px, gradient #1B1A18 → #3a2419 → #F2660F). Avatar tile "P" (96px, white, radius 22, overlaps cover −46px) + name "Pella Home" + badges "✓ Geprüfter Verkäufer" (dark), "★ Top-Verkäufer 2026" (orange tint) + "★ 4.8 · 1'240 Bewertungen · 96% positive · 📍 Versand aus Zürich" + buttons "+ Folgen" (orange), "Nachricht" (outline).
- **Stats** row (4 cards): 64 Produkte · 4.8★ Bewertung · 3'400 Follower · < 2 Std. Antwortzeit.
- **Tabs**: Alle Produkte / Bestseller / Über uns / Bewertungen.
- Featured strip: "MEISTVERKAUFT — Raumdüfte 250 ml" card + "Über Pella Home" blurb card. Then a product grid (9 items) + footer.

### 5. Verkäufer-Registrierung (Seller signup) — `verkaufen.shoppypella.ch/start`
- **Purpose**: onboard a new seller. Own top bar (logo + "Verkäufer-Center" + "Schon registriert? Anmelden") — NOT the marketplace header.
- Two columns. **Left**: title "Verkäufer werden" + sub; a **4-step stepper** (1 Konto ✓done, 2 Firmendaten ✓active orange, 3 Verifizierung, 4 Fertig) with connectors; a "Firmendaten" form card with fields (Firmenname, Rechtsform ▾, UID-Nummer CHE-…, Strasse & Nr., PLZ, Ort, Kanton ▾, IBAN, Kontaktperson, E-Mail) rendered as labeled bordered inputs (pre-filled, color #1B1A18); AGB checkbox; buttons "Zurück" (outline) + "Weiter zur Verifizierung →" (orange, advances to Dashboard).
- **Right** (dark `--ink` panel): "WARUM SHOPPYPELLA?" + headline + 3 KPI tiles (0.– Startgebühr · 5% Provision · 48 Std. Freischaltung) + benefit list (globe/package/card/trending with title+desc) + testimonial card ("…Umsatz verdreifacht." — Atiye T., Pella Home).

### 6. Verkäufer-Dashboard (Seller panel) — `verkaufen.shoppypella.ch/dashboard`
- **Purpose**: seller back-office. Own dark top app bar (logo + "Verkäufer-Center" + bell + "Pella Home" avatar). Page bg #F6F3EF.
- Left **dashboard sidebar** (white): nav items (chart Übersicht active orange-tint, package Produkte, receipt Bestellungen, truck Versand, card Auszahlungen, star Bewertungen, settings Einstellungen) + "Shop-Tarif Basic · 5% Provision / Upgrade auf Plus →" card.
- **Main**: greeting "Willkommen zurück, Atiye"; two alert cards (orange-left-border "2 Bestellungen warten auf Versand / Bearbeiten →"; "3 Produkte mit niedrigem Lagerbestand"); **4 KPI cards** (Umsatz heute CHF 1'248 ▲+12.4%, Bestellungen 37 ▲+5, Conversion 3.2% ▲+0.3pp, Shop-Bewertung 4.8★); a **bar chart** "Umsatz pro Tag" (7 bars Mo–So, Fri highlighted orange, others #F7C9A6) + "Nächste Auszahlung CHF 2'140" dark card; **Neueste Bestellungen** table (Bestellung / Produkt / Kunde / Betrag / Status — status chips Zu versenden=orange tint, Versendet=green tint, Storniert=red tint); **Top-Produkte** list (thumb + name + sold + stock; low stock in red #C24A3A, else green #2E7D5B).

### 7. Mein Konto (Customer account) — `shoppypella.ch/konto`
- **Purpose**: customer self-service.
- Left: profile card (dark gradient, avatar "MK" + "Maria Keller / Mitglied seit 2024") + account nav (home Übersicht active, package Bestellungen, pin Adressen, card Zahlungsmethoden, heart Wunschliste, star Bewertungen, settings Einstellungen, Abmelden).
- Right: greeting "Hallo Maria"; 4 stat cards (14 Bestellungen, CHF 312 Gespart, 8 Wunschliste, 2 Bewertungen); **Meine Bestellungen** list (each: thumb + #id + status chip + product + date + amount + action button "Sendung verfolgen / Erneut kaufen / Bewerten"); two cards: "📍 Standard-Adresse" (Maria Keller, Seefeldstrasse 88, 8008 Zürich) + "💳 Zahlungsmethoden" (TWINT +41 79 ••• 42, VISA •••• 4821).

### 8. Warenkorb & Kasse (Cart & checkout) — `shoppypella.ch/warenkorb`
- **Purpose**: review cart and check out, single page.
- Title "Warenkorb & Kasse" + **3-step indicator** (1 Warenkorb done, 2 Lieferung active, 3 Zahlung).
- Two columns. **Left**: seller group card "Pella Home · 3 Artikel · Versand aus Zürich" with line items (thumb + name + variant + "● Sofort lieferbar" + qty stepper + line total + "Entfernen"); **Lieferadresse** (selected "Zuhause" card orange-bordered + "+ Neue Adresse"); **Lieferart** (Standard 2–3 Tage = Gratis, selected; Express morgen = CHF 9.90); **Zahlungsart** radio cards (TWINT selected, Karte, PayPal, Rechnung).
- **Right** (sticky **Zusammenfassung**): Gutscheincode input + Einlösen; rows Zwischensumme CHF 49.10, Versand **Gratis** (green), Rabatt · WILLKOMMEN10 **− CHF 4.90** (orange); **Gesamt CHF 44.20** (24px/900) + "inkl. CHF 3.31 MwSt (8.1%)"; **Kostenpflichtig bestellen** button (orange); "🔒 Sichere SSL-Zahlung · Käuferschutz" + payment chips.

## Interactions & Behavior
- **Routing**: navigator rail and in-page links switch the active screen (single-page state, not URL routing in the prototype — implement as real routes). Header logo → Home; category rows/pills → Category; product cards → Product; seller chip/avatar → Store; cart icon/buttons → Cart; "Verkäufer werden" → Seller signup; signup "Weiter" → Dashboard.
- **Category accordion**: single-open; click toggles. **Mobile drawer**: hamburger opens, ✕/backdrop closes, sub-item closes + navigates.
- **Hover**: product cards lift (`translateY(-2px)` + shadow `0 8px 24px rgba(27,26,24,.10)`, border → #E0DCD5); category rows hover bg #FFF8F2 / text orange.
- **Responsive**: layouts use flex-wrap with fluid bases so they reflow; the mobile breakpoint is driven by the device toggle in the prototype → in production use real CSS breakpoints (~430px). Mobile-specific: hamburger drawer, bottom tab bar, single-column reflow, product grids 2-up.
- All product grids: desktop 4-up on Home ("Beliebte"/"Neu"), ~5-up on Category/Store; mobile 2-up.

## State Management
- `screen` (active view) → replace with router.
- `device` (desktop/mobile) → prototype-only; production uses media queries.
- `openCat` (which sidebar category is expanded; default "Haushalt & Wohnen").
- `mobileMenu` (drawer open/closed).
- Theming selectors `fontSel / radiusSel / bgSel / accentSel` → prototype-only; pick one combination for production.
- Real app needs: product catalog + categories/subcategories, cart contents & totals, auth/customer, seller/store data, orders, dashboard metrics — all hard-coded in the prototype (`renderVals()` in `Shoppypella.dc.html`).

## Design Tokens

### Color
- **Primary (brand orange)**: `#F2660F`. Hover/strong red-orange used in gradients: `#E0322B` / `#E22617`.
- **Tints**: `#FFF1E8` (primary tint), `#FFF8F2` / `#FFF4EC` (lighter), `#FFE4D3` (hero gradient end), tint borders `#F3E1D2`/`#F6E1D0`/`#F0E2D4`.
- **Ink / dark surfaces**: `#1B1A18`. Secondary dark text `#4a4742`.
- **Text**: heading/ink `#1B1A18`; body secondary `#6E6A64`; muted `#9A958D`; faint `#B8B3AB`.
- **Neutral surfaces**: white `#fff`; soft `#FAF8F5`; hairlines `#ECE9E4` / `#F5F2EE` / `#F0EDE8`.
- **Semantic**: success green `#2E7D5B`; danger red `#C24A3A`; status chips use the tint/ink pairs noted per screen.
- **Stage backdrop** (navigator only, not product): `#E9E6E1`.

### Typography
- Default family **Hanken Grotesk** (Google Fonts, weights 400–900). Headings inherit body unless a theme swaps them.
- Scale seen: hero 40/900, h1 27–28/900, h2 22–24/900, body 14–16, small 12.5–13.5, micro 11–12. Headline tracking ~ −.01 to −.02em; eyebrows +.06em.

### Spacing & Radius
- Spacing: 4 / 8 / 12 / 14 / 16 / 18 / 22 / 24 / 28 / 40 px.
- Radius (default theme): buttons ~12px, cards/inputs ~14px, panels/sections ~16px, hero/cover ~20px, pills 20px+, frame 16–18px.

### Shadows
- Card hover `0 8px 24px rgba(27,26,24,.10)`. Floating tiles `0 8px 24px rgba(0,0,0,.12)`. Frame `0 12px 40px rgba(27,26,24,.16)` (prototype chrome only).

### Theming (exploratory — productionize ONE combination)
The prototype exposes four independent axes via CSS custom properties on the root; the developer should bake the chosen combination into the design system rather than ship the switcher. **Brand orange is constant in every combination.**
- **Font** (`--font`, `--font-head`): Grotesk (Hanken) · Rund (Nunito) · Serif headings (Spectral) · Space (Space Grotesk headings).
- **Radius** (`--r-lg`,`--r-md`,`--r-btn`): Normal (16/14/12) · Eckig (5/4/5) · Rund (18/16/14) · Pill (26/22/26).
- **Background** (`--canvas`, the shop page bg): Weiss (#FEFCFA) · Punkte (radial dot grid) · Streifen (45° stripes) · Verlauf (soft warm gradient) · Kreise (multicolor radial blobs + **glassmorphism**: cards become `rgba(255,255,255,.55)` + `backdrop-filter:blur(14px)` via `--card/--card2/--card-bd/--blur`).
- **Akzent** (`--accent-bg`, and feature-card vars): Solid (flat orange fills) · Verlauf (orange→fiery-red gradient on buttons/badges/logo AND on feature cards — hero + category banner get the gradient with white text via `--feature-bg/--feature-fg/--feature-sub/--feature-ey/--feature-btn-*`).
- **Recommended production default**: Grotesk + Normal + Weiss + Solid (the "Classic" look).

## Assets
- **Logo**: original `assets/logo.pdf` ("Shoppypella"); the prototype renders the wordmark in HTML/CSS as "shoppy**pella**" (orange "pella") with a rounded orange "S" tile — replace with the real logo asset.
- **Product photography**: 12 real Pella product JPEGs in `assets/img01.jpeg … img12.jpeg` (room/fabric sprays London Blue & Rose Paris, mop heads, microfiber cloths, scouring pads, towel sets). Used across all product cards/grids/thumbnails. Images sit on white tiles with `mix-blend-mode:multiply`.
- **Icons**: a custom inline-SVG stroke icon set (Lucide-style: truck, lock, user, cart, search, menu, heart, star, package, card, chart, receipt, settings, bell, monitor, gamepad, sofa, utensils, shirt, sparkles, dumbbell, basket, wrench, tag, globe, home, list, etc.) defined once as an SVG `<symbol>` sprite and referenced via `<use>`. Replace with the codebase's icon library (Lucide/Heroicons map 1:1 by name).
- Fonts via Google Fonts: Hanken Grotesk (primary), plus Nunito / Space Grotesk / Spectral (only if a non-default font theme is chosen).

## Files
- `Shoppypella.dc.html` — the full prototype: all 8 screens, the shell (header/footer/sidebar/drawer/bottom-bar), the navigator chrome, the SVG icon sprite, the theming engine, and all data (`renderVals()`).
- `ProductCard.dc.html` — the reusable product card (image tile + badge + wishlist + seller + name + rating + price). Honors theme vars (`--card`, `--blur`, `--r-md`, `--accent-bg`, `--font`).
- `Footer.dc.html` — the marketplace footer.
- `Thumb.dc.html` — tiny image wrapper used for data-bound thumbnails.
- `assets/` — product images + original logo PDF.

> Implementation note: the `.dc.html` files use a streaming-template syntax (`{{ }}` holes, `<sc-for>`, `<sc-if>`, `<dc-import>`) — read them for structure/values, but reimplement with the target framework's own components, loops and conditionals. Colors/radii/fonts are expressed as `var(--token, fallback)`; map these to the codebase's design-token system.
