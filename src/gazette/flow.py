"""Flow Prefect : collecte d'une source -> bronze."""
from prefect import flow, get_run_logger, task

from gazette.bronze import ecrire_bronze, fetch_feed
from gazette.collecte import parse_feed

URL_LEMONDE = "https://www.lemonde.fr/rss/une.xml"


@task(retries=2, retry_delay_seconds=60)
def telecharger(url: str) -> bytes:
    return fetch_feed(url)


@task
def parser(contenu: bytes, source: str) -> list[dict]:
    return parse_feed(contenu, source)


@task
def ecrire(items: list[dict], source: str, url: str) -> str:
    return str(ecrire_bronze(items, source, url))


@flow(name="collecte-bronze")
def collecte(source: str = "lemonde", url: str = URL_LEMONDE) -> str:
    logger = get_run_logger()
    items = parser(telecharger(url), source)
    chemin = ecrire(items, source, url)
    logger.info("%s : %d items écrits dans %s", source, len(items), chemin)
    return chemin


if __name__ == "__main__":
    collecte()