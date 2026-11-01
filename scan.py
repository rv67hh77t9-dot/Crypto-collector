import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

SOURCES = {
  "Airdrops gratuits France": (

        "https://news.google.com/rss/search?"

        "q=crypto+airdrop+free+France"

        "&hl=fr&gl=FR&ceid=FR:fr"

    ),

    "Recompenses crypto": (

        "https://news.google.com/rss/search?"

        "q=crypto+learn+earn+rewards"

        "&hl=en-US&gl=US&ceid=US:en"
    ),    "Kraken recompenses": (
        "https://news.google.com/rss/search?"
        "q=Kraken+crypto+rewards+earn"
        "&hl=fr&gl=FR&ceid=FR:fr"
    ),
}
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
