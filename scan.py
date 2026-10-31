import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

SOURCES = {
    "Coinbase": "https://www.coinbase.com/blog/rss.xml","CoinGecko": "https://blog.coingecko.com/feed/"

resultats = []

for nom, url in SOURCES.items():
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "CryptoCollector/1.0"}
        )

        with urllib.request.urlopen(req, timeout=15) as r:
            contenu = r.read()

        racine = ET.fromstring(contenu)

        for article in racine.findall(".//item")[:10]:
            titre = article.findtext("title", "")
            lien = article.findtext("link", "")

            mots = ["airdrop", "reward", "free",
                    "gratuit", "earn", "quest"]

            if any(m in titre.lower() for m in mots):
                resultats.append({
                    "source": nom,
                    "titre": titre,
                    "lien": lien
                })

    except Exception as e:
        print(f"Erreur {nom}: {e}")

Path("docs").mkdir(exist_ok=True)

donnees = {
    "date": datetime.now(timezone.utc).isoformat(),
    "opportunites": resultats
}

Path("docs/results.json").write_text(
    json.dumps(donnees, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"{len(resultats)} articles détectés")
