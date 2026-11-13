
import json
from datetime import UTC, datetime
from pathlib import Path

import requests

USER_AGENT = "LaGazette-M2Ops/0.1 (projet etudiant Efrei)"


def fetch_feed(url: str, timeout: int = 20) -> bytes:
    """Télécharge le flux. Erreur sur 403/429/5xx : on n'insiste pas."""
    reponse = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    reponse.raise_for_status()
    return reponse.content


def ecrire_bronze(items: list[dict], source: str, url: str, racine: Path = Path("data/bronze")) -> Path:
    """Un fichier par run : data/bronze/source=<s>/date=<AAAA-MM-JJ>/run_<HHMMSS>.json"""
    maintenant = datetime.now(UTC)
    dossier = racine / f"source={source}" / f"date={maintenant:%Y-%m-%d}"
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / f"run_{maintenant:%H%M%S}.json"
    contenu = {
        "source": source,
        "url": url,
        "recupere_le": maintenant.isoformat(),
        "nb_items": len(items),
        "items": items,
    }
    chemin.write_text(json.dumps(contenu, ensure_ascii=False, indent=2), encoding="utf-8")
    return chemin