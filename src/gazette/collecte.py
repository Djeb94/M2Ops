"""Collecte : transforme un flux RSS en items pour le bronze."""
from datetime import UTC, datetime
from urllib.parse import urlparse

import feedparser


def _date_utc(entry):
    """feedparser fournit published_parsed déjà ramené en UTC."""
    if not entry.get("published_parsed"):
        return None
    return datetime(*entry.published_parsed[:6], tzinfo=UTC).isoformat()


def _rubrique(lien):
    """Pas de <category> chez Le Monde : la rubrique est le 1er segment de l'URL."""
    segments = [s for s in urlparse(lien).path.split("/") if s]
    return segments[0] if segments else None


def parse_feed(contenu: bytes, source: str) -> list[dict]:
    """XML du flux -> liste d'items. Fonction pure : aucun accès réseau."""
    items = []
    for entry in feedparser.parse(contenu).entries:
        lien = entry.get("link", "")
        items.append({
            "source": source,
            "guid": entry.get("id", lien),
            "titre": entry.get("title", "").strip(),
            "extrait": entry.get("summary", "").strip(),
            "lien": lien,
            "date_publication": _date_utc(entry),
            "rubrique": _rubrique(lien),
        })
    return items
