import requests
from django.conf import settings

class JikanError(Exception):
    pass

def jikan_get(path: str, params: dict = None) -> dict:
    url = settings.JIKAN_BASE_URL.rstrip("/") + path
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
    except requests.RequestException as e:
        raise JikanError(f"Error llamando a Jikan: {e}")
    payload = r.json()
    return payload.get("data", {})

def fetch_genres(media: str = "anime") -> list[dict]:
    """
    Devuelve la lista de géneros de 'anime' o 'manga'.
    """
    return jikan_get(f"/genres/{media}")

def fetch_anime_by_genre(genre_id: int, page: int = 1, limit: int = 20) -> list[dict]:
    """
    Devuelve una lista de animes que incluyen el genre_id dado.
    """
    return jikan_get(
        path="/anime",
        params={"genres": genre_id, "page": page, "limit": limit}
    )