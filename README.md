# VI·Watch — GTA 6 Countdown & Preorder-Hub

Live unter: **https://mr43content.github.io/vi-watch/**

Automatisierte Affiliate-Site nach demselben Prinzip wie solarcheck-rlp.de:
statisch, GitHub Pages, SEO-Content, Affiliate-Links — plus ein täglicher Bot,
der News automatisch aktualisiert.

## Status: bereits eingerichtet & deployed

- Impressum/Datenschutz mit echten Pflichtangaben befüllt
- Domain-Platzhalter durch den echten GitHub-Pages-Link ersetzt
- Alle Dateien committed, GitHub Pages aktiviert
- News-Bot läuft täglich automatisch (siehe Abschnitt 4)

## 1. Noch offen (optional, jederzeit nachrüstbar)

- **Affiliate-Links**: In `index.html` 5 Platzhalter-Links im Preorder-Vergleich
  (`#AFF-PSN-STD`, `#AFF-XBOX-STD`, `#AFF-AMAZON-STD`, `#AFF-MM-STD`,
  `#AFF-ULTIMATE`) mit echten Tracking-Links ersetzen (Amazon PartnerNet,
  Awin, Adcell).
- **Google Analytics 4**: `python3 setup.py` erneut ausführen und nur die
  Measurement-ID angeben — trägt den Tracking-Code automatisch überall ein
  und ergänzt den Datenschutz-Abschnitt entsprechend. Änderungen danach
  einfach committen (z. B. über die GitHub-Weboberfläche oder `git push`).
- **Eigene Domain** (z. B. vi-watch.de): `setup.py` mit der neuen Domain
  erneut laufen lassen, dann in **Settings → Pages → Custom domain**
  eintragen + CNAME beim Registrar setzen.
- **Social-Share-Bild**: `assets/og-image.png` wurde noch nicht hochgeladen
  (Binärdatei, nicht über die Text-API pushbar) — einzelne Datei per
  Drag&Drop im Repo nachreichen, falls gewünscht. Ohne sie funktioniert
  die Seite normal, nur Link-Vorschauen auf Social Media zeigen kein Bild.

## 2. setup.py wiederverwenden

```bash
python3 setup.py
```

Idempotent — bereits ausgefüllte Felder bleiben unangetastet, wenn du sie
beim erneuten Lauf leer lässt. Nur für die Felder, die du diesmal ausfüllst,
werden die entsprechenden Platzhalter ersetzt.

## 3. Was bereits fertig ist

- Live-Countdown bis 19.11.2026, automatisch aktualisierter News-Ticker
- Preorder-Vergleichstabelle mit den offiziell bestätigten Preisen
  (79,99 € Standard / 99,99 € Ultimate)
- 2 SEO-Artikel (Preorder-Guide, PS5 Pro vs. Series X) mit bestätigten Fakten
- Eigenständiges Favicon + OG/Twitter-Card-Tags — keine kopierten Logos
- 404-Seite im gleichen Design
- Rechtliche Pflichtseiten (Impressum, Datenschutz) vollständig befüllt
- Affiliate-Disclaimer + Marken-Disclaimer im Footer aller Seiten

## 4. Die Automatisierung (News-Bot)

`.github/workflows/update-news.yml` läuft täglich um 06:00 UTC automatisch:

1. Holt aktuelle GTA-6-Schlagzeilen aus dem Google-News-RSS-Feed
   (`scripts/fetch_news.py`, keine externen Abhängigkeiten).
2. Schreibt sie nach `data/news.json`.
3. Committet & pusht automatisch — der News-Ticker auf der Startseite
   lädt diese Datei live nach.

Manuell auslösen: Repo → **Actions → Update GTA 6 News → Run workflow**.
Läuft kostenlos in GitHub Actions (Free-Tier reicht massiv aus).

## 5. Content-Roadmap (wenn Zeit ist)

Jeder neue Artikel = neue `.html` in `articles/`, Karte in `index.html`
unter `#guides` ergänzen, URL in `sitemap.xml` eintragen. Themen mit
hohem Suchvolumen, sobald News dazu kommen:

- Trailer 3 / neue Gameplay-Reveals
- Leonida-Map: alle bestätigten Locations
- Lucia & Jason: Story-Leaks & Charakter-Infos
- "GTA 6 PC Release" — Speculation-Artikel performt schon jetzt stark
  und zieht bis 2027/28 weiter Traffic
- Reaktionen auf "Ultimate Edition lohnt sich nicht" — Diskussion läuft
  bereits in der Community, eigener Artikel dazu hat Potenzial

## 6. Rechtliches

Disclaimer ("kein offizielles Rockstar/Take-Two-Projekt") ist bereits
im Footer von `index.html` sowie in beiden Artikeln verbaut. Design,
Favicon sind eigenständig erstellt — keine offiziellen Bilder, Logos
oder Marketing-Assets verwendet.
