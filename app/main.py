"""CineMatch web app — FastAPI version of the original terminal code."""
import os
import random

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Load the TMDB API key from the .env file (not hard-coded).
load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w300"
API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Missing TMDB API key. Add TMDB_API_KEY to your .env file."
    )

LANGUAGES = {
    "en": "English", "ko": "Korean", "ja": "Japanese", "fr": "French",
    "es": "Spanish", "zh": "Chinese", "th": "Thai",
}

# Loaded once at startup so we don't re-fetch genres on every request.
MOVIE_GENRES = {}
TV_GENRES = {}

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# ============ TMDB helpers ============

def get_json(endpoint: str, params: dict) -> dict:
    """Fetch data from TMDB and return the JSON, or {} on any error."""
    params["api_key"] = API_KEY
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}

def load_genres():
    """Load movie and TV genre names once at startup."""
    global MOVIE_GENRES, TV_GENRES

    def fetch(endpoint):
        data = get_json(f"/{endpoint}", {}) or {}
        return {g["id"]: g["name"] for g in data.get("genres", [])}

    MOVIE_GENRES, TV_GENRES = fetch("genre/movie/list"), fetch("genre/tv/list")

def format_genres(genre_ids, genres_dict) -> str:
    """Turn a list of genre IDs into a comma-separated string of names."""
    return ", ".join(genres_dict.get(g) for g in genre_ids if genres_dict.get(g)) or "N/A"

def get_title(item) -> str:
    """TMDB uses 'title' for movies and 'name' for TV shows."""
    return item.get("title") or item.get("name") or "Unknown"

def get_release_date(item) -> str:
    """Different release date fields for movies vs TV shows."""
    return item.get("release_date") or item.get("first_air_date") or "N/A"

def to_card(item: dict, content_type: str) -> dict:
    """Shape a TMDB result into the dictionary the templates expect."""
    genres = MOVIE_GENRES if content_type == "movie" else TV_GENRES
    return {
        "id": item.get("id"),
        "title": get_title(item),
        "media_type": content_type,
        "overview": item.get("overview") or "No summary available.",
        "poster_url": IMAGE_URL + item["poster_path"] if item.get("poster_path") else None,
        "release_date": get_release_date(item),
        "year": get_release_date(item)[:4],
        "rating": item.get("vote_average") or "N/A",
        "genres_text": format_genres(item.get("genre_ids", []), genres),
        "language": LANGUAGES.get(
            item.get("original_language"),
            item.get("original_language", "N/A"),
        ),
    }

def search_titles(query: str, content_type: str) -> list:
    """Search TMDB by title for movies or TV shows."""
    data = get_json(f"/search/{content_type}", {"query": query})
    return [to_card(item, content_type) for item in data.get("results", [])]

def get_recommendations(media_id: str, content_type: str) -> list:
    """Get similar/recommended titles for a given movie/TV id."""
    data = get_json(f"/{content_type}/{media_id}/recommendations", {})
    return [to_card(item, content_type) for item in data.get("results", [])[:10]]

def get_trending(content_type: str) -> list:
    """Get titles trending today, keeping only well-rated ones."""
    data = get_json(f"/trending/{content_type}/day", {})
    results = [
        r for r in data.get("results", [])
        if r.get("vote_average") and r.get("vote_count")
    ][:10]
    return [to_card(item, content_type) for item in results]

def get_surprise(content_type: str, min_rating: float, min_votes: int) -> list:
    """Pick a random well-rated title from a random discover page."""
    data = get_json(f"/discover/{content_type}", {
        "sort_by": "vote_average.desc",
        "vote_average.gte": min_rating,
        "vote_count.gte": min_votes,
        "page": random.randint(1, 50),
    })
    results = data.get("results", [])
    if not results:
        return []
    return to_card(random.choice(results), content_type)

# ============ Routes ============

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "CineMatch"},
    )

@app.get("/similar")
def similar_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="similar.html",
        context={
            "title": "Find Similar",
            "content_type": "movie",
            "movie_title": "",
            "search_results": None,
            "recommendations": None,
        },
    )

@app.post("/similar")
def similar_action(
    request: Request,
    action: str = Form(...),
    content_type: str = Form("movie"),
    movie_title: str = Form(""),
    selected_id: str = Form(None),
):
    search_results = None
    recommendations = None

    if action == "search":
        search_results = search_titles(movie_title, content_type)
    elif action == "recommend" and selected_id:
        recommendations = get_recommendations(selected_id, content_type)

    return templates.TemplateResponse(
        request=request,
        name="similar.html",
        context={
            "title": "Find Similar",
            "content_type": content_type,
            "movie_title": movie_title,
            "search_results": search_results,
            "recommendations": recommendations,
        },
    )

@app.get("/trending")
def trending_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="trending.html",
        context={
            "title": "Trending Today",
            "content_type": "movie",
            "trending_items": None,
        },
    )

@app.post("/trending")
def trending_action(request: Request, content_type: str = Form("movie")):
    return templates.TemplateResponse(
        request=request,
        name="trending.html",
        context={
            "title": "Trending Today",
            "content_type": content_type,
            "trending_items": get_trending(content_type),
        },
    )

@app.get("/surprise")
def surprise_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="surprise.html",
        context={
            "title": "Surprise Me",
            "content_type": "movie",
            "surprise_items": None,
        },
    )

@app.post("/surprise")
def surprise_action(
    request: Request,
    content_type: str = Form("movie"),
    min_rating: float = Form(6.5),
    min_votes: int = Form(300),
):
    return templates.TemplateResponse(
        request=request,
        name="surprise.html",
        context={
            "title": "Surprise Me",
            "content_type": content_type,
            "min_rating": min_rating,
            "min_votes": min_votes,
            "surprise_items": get_surprise(content_type, min_rating, min_votes),
        },
    )

# Load genres once when the app starts.
load_genres()