#!/usr/bin/env python3
"""
Holt aktuelle GTA 6 News aus dem Google News RSS-Feed und schreibt sie
nach data/news.json. Wird taeglich per GitHub Action ausgefuehrt
(.github/workflows/update-news.yml) und automatisch committet.

Keine externen Abhaengigkeiten -- laeuft mit reinem Python 3 stdlib.
"""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

FEED_URL = "https://news.google.com/rss/search?q=GTA+6&hl=de&gl=DE&ceid=DE:de"
OUTPUT = Path(__file__).resolve().parent.parent / "data" / "news.json"
MAX_ITEMS = 8


def fetch_feed(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_items(xml_text: str):
    root = ET.fromstring(xml_text)
    items = []
    for item in root.findall("./channel/item")[:MAX_ITEMS]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date_raw = item.findtext("pubDate") or ""
        try:
            dt = datetime.strptime(pub_date_raw[:25], "%a, %d %b %Y %H:%M:%S")
            date_str = dt.strftime("%d.%m.%Y")
        except ValueError:
            date_str = datetime.now(timezone.utc).strftime("%d.%m.%Y")
        if title and link:
            items.append({"date": date_str, "title": title, "link": link})
    return items


def main():
    try:
        xml_text = fetch_feed(FEED_URL)
        items = parse_items(xml_text)
    except Exception as exc:  # Netzwerkfehler, defekter Feed, etc.
        print(f"Feed-Abruf fehlgeschlagen: {exc}")
        return

    if not items:
        print("Keine News-Items gefunden -- news.json bleibt unveraendert.")
        return

    OUTPUT.write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{len(items)} News-Items geschrieben nach {OUTPUT}")


if __name__ == "__main__":
    main()
