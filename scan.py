import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

QUERIES = {
    "Airdrops gratuits France":
        "crypto airdrop gratuit France sans dépôt",
    "Recompenses crypto":
        "crypto learn earn rewards free",
    "Kraken":
        "Kraken crypto rewards earn France",
    "Coinbase":
        "Coinbase rewards quests France"
}

MOTS = (
    "airdrop", "reward", "recompens",
    "récompens", "gratuit", "free",
    "earn", "quest"
)

EXCLUSIONS = (
    "casino", "gambling", "deposit bonus",
    "price prediction", "trading signals"
)

resultats = []
erreurs = []
urls_vues = set()

for nom, recherche in QUERIES.items():

    parametres = urlencode({
        "q": recherche,
        "hl": "fr",
        "gl": "FR",
        "ceid": "FR:fr"
    })

    url = (
        "https://news.google.com/rss/search?"
        + parametres
    )

    try:
        requete = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            requete, timeout=20
        ) as reponse:
            racine = ET.fromstring(reponse.read())

        for article in racine.findall(
            "./channel/item"
        )[:15]:

            titre = article.findtext(
                "title", ""
            ).strip()

            lien = article.findtext(
                "link", ""
            ).strip()

            titre_minuscule = titre.lower()

            if (
                lien
                and lien not in urls_vues
                and any(
                    mot in titre_minuscule
                    for mot in MOTS
                )
                and not any(
                    mot in titre_minuscule
                    for mot in EXCLUSIONS
                )
            ):
                urls_vues.add(lien)

                resultats.append({
                    "source": nom,
                    "titre": titre,
                    "lien": lien,
                    "statut": "Article non verifie"
                })

    except Exception as erreur:
        erreurs.append(
            f"{nom}: {type(erreur).__name__}: {erreur}"
        )

Path("docs").mkdir(exist_ok=True)

contenu = {
    "date": datetime.now(
        timezone.utc
    ).isoformat(),

    "avertissement":
        "Articles a verifier : aucune "
        "recompense garantie.",

    "opportunites": resultats,
    "erreurs_sources": erreurs
}

Path("docs/results.json").write_text(
    json.dumps(
        contenu,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

print(
    f"{len(resultats)} articles detectes ; "
    f"{len(erreurs)} erreurs de sources"
)

for erreur in erreurs:
    print("Source indisponible :", erreur)
