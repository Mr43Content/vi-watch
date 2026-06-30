#!/usr/bin/env python3
"""
setup.py — einmaliger Einrichtungsassistent fuer VI.Watch

Fragt Domain, Impressum-Daten, optional Analytics-ID und Affiliate-Links ab
und trägt alles automatisch in index.html, beide Artikel, impressum.html,
datenschutz.html, sitemap.xml, robots.txt und 404.html ein.

Aufruf:  python3 setup.py
Mehrfach ausfuehrbar -- ueberschreibt nur, was du beantwortest.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ALL_FILES = [
    "index.html",
    "404.html",
    "articles/preorder-guide.html",
    "articles/ps5pro-vs-seriesx.html",
    "impressum.html",
    "datenschutz.html",
    "sitemap.xml",
    "robots.txt",
]

GA4_SNIPPET = """<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{gid}');
</script>"""

GA4_PRIVACY_TEXT = (
    "Diese Seite nutzt Google Analytics 4 (Google Ireland Limited) zur "
    "statistischen Auswertung der Nutzung. Es werden IP-Adressen "
    "gekürzt verarbeitet. Rechtsgrundlage ist deine Einwilligung gem. "
    "Art. 6 Abs. 1 lit. a DSGVO. Du kannst diese jederzeit über die "
    "Cookie-Einstellungen widerrufen."
)


def ask(label, default=""):
    suffix = f" [{default}]" if default else " (Enter = überspringen)"
    val = input(f"{label}{suffix}: ").strip()
    return val or default


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main():
    print("=== VI·Watch Setup ===\n")

    domain = ask("Domain (z.B. gta6-watch.de, ohne https://)")
    domain = domain.replace("https://", "").replace("http://", "").strip("/")

    print("\n-- Impressum / Pflichtangaben --")
    name = ask("Name oder Firmenname")
    strasse = ask("Straße und Hausnummer")
    ort = ask("PLZ und Ort")
    email = ask("E-Mail-Adresse")
    telefon = ask("Telefon (optional)")
    ustid = ask("USt-IdNr. (optional, sonst Enter)")

    print("\n-- Analytics (optional) --")
    ga_id = ask("Google Analytics 4 Measurement-ID (z.B. G-XXXXXXX)")

    print("\n-- Affiliate-Links (optional, sonst Enter = Platzhalter bleibt) --")
    aff_psn = ask("PlayStation Store Affiliate-Link")
    aff_xbox = ask("Xbox Store Affiliate-Link")
    aff_amazon = ask("Amazon Affiliate-Link")
    aff_mm = ask("MediaMarkt/Saturn Affiliate-Link")
    aff_ultimate = ask("Ultimate Edition Affiliate-Link")

    changed = []
    skipped = []

    for rel in ALL_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        text = read(path)
        original = text

        if domain:
            text = text.replace("example.com", domain)

        if name:
            text = text.replace("[DEIN NAME / FIRMENNAME]", name)
            text = text.replace("[DEIN NAME]", name)
        if strasse:
            text = text.replace("[STRASSE UND HAUSNUMMER]", strasse)
        if ort:
            text = text.replace("[PLZ ORT]", ort)
        if email:
            text = text.replace("[DEINE-EMAIL@DOMAIN.DE]", email)
        if strasse and ort:
            text = text.replace("[ANSCHRIFT]", f"{strasse}, {ort}")
        if email:
            text = text.replace("[E-MAIL]", email)

        if telefon:
            text = text.replace("Telefon: [OPTIONAL]", f"Telefon: {telefon}")
        else:
            text = re.sub(r"\s*Telefon: \[OPTIONAL\]<br>\n?", "", text)
            text = text.replace("    Telefon: [OPTIONAL]\n  </p>", "  </p>")

        if ustid:
            text = text.replace(
                "[FALLS VORHANDEN: USt-IdNr. gemäß § 27a UStG] — sonst Zeile entfernen.",
                f"USt-IdNr. gemäß § 27a UStG: {ustid}",
            )
        else:
            text = re.sub(
                r"\s*<h2>Umsatzsteuer-ID</h2>\s*<p>\[FALLS VORHANDEN:[^<]*</p>\n?",
                "\n",
                text,
            )

        if ga_id:
            text = text.replace(
                "<!-- GA4: Snippet hier einfügen -->",
                GA4_SNIPPET.format(gid=ga_id),
            )
            text = text.replace(
                "[FALLS GENUTZT: Google Analytics / Search Console — Zweck, "
                "Rechtsgrundlage (Einwilligung gem. Art. 6 Abs. 1 lit. a DSGVO) "
                "und Cookie-Banner-Hinweis hier ergänzen, analog zu "
                "solarcheck-rlp.de.]",
                GA4_PRIVACY_TEXT,
            )

        if aff_psn:
            text = text.replace('href="#AFF-PSN-STD"', f'href="{aff_psn}"')
        if aff_xbox:
            text = text.replace('href="#AFF-XBOX-STD"', f'href="{aff_xbox}"')
        if aff_amazon:
            text = text.replace('href="#AFF-AMAZON-STD"', f'href="{aff_amazon}"')
        if aff_mm:
            text = text.replace('href="#AFF-MM-STD"', f'href="{aff_mm}"')
        if aff_ultimate:
            text = text.replace('href="#AFF-ULTIMATE"', f'href="{aff_ultimate}"')

        if text != original:
            write(path, text)
            changed.append(rel)

    print("\n=== Fertig ===")
    print("Aktualisiert:", ", ".join(changed) if changed else "(nichts)")

    remaining = []
    if not domain:
        remaining.append("Domain (noch example.com)")
    if not all([name, strasse, ort, email]):
        remaining.append("Impressum-Pflichtfelder unvollständig")
    if not ga_id:
        remaining.append("Google Analytics nicht eingerichtet")
    for label, val in [
        ("PlayStation-Link", aff_psn), ("Xbox-Link", aff_xbox),
        ("Amazon-Link", aff_amazon), ("MediaMarkt-Link", aff_mm),
        ("Ultimate-Edition-Link", aff_ultimate),
    ]:
        if not val:
            remaining.append(f"Affiliate: {label} fehlt noch")

    if remaining:
        print("\nNoch offen (Skript erneut ausführen, um zu ergänzen):")
        for r in remaining:
            print(" -", r)
    else:
        print("\nAlles eingetragen. Bereit zum Deploy (siehe README.md, Schritt 1).")


if __name__ == "__main__":
    main()
