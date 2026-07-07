import requests
import os
import sys
import webbrowser
import random
import pyfiglet
from dotenv import load_dotenv

# Load TMDB API key from .env file instead of storing it in the source code
load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"
API_KEY = os.getenv("TMDB_API_KEY") 
if not API_KEY:
    sys.exit("Missing TMDB API key. Please add it to your .env file.")
LANGUAGES = {"en": "English", "ko": "Korean", "ja": "Japanese", "fr": "French", "es": "Spanish", "zh": "Chinese", "th": "Thai"}
MOVIE_GENRES, TV_GENRES = {}, {}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_json(url, params):
    # Fetch data from TMDB API and handle connection errors
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        sys.exit("Unable to connect to TMDB. Please check your internet/API key and try again.")
    
def choose_media():
    while (media := input("Choose media (movie/tv): ").strip().lower()) not in {"movie", "tv"}:
           print("Please type 'movie' or 'tv' only.")
    return media

def show_header():
    # Display the CineMatch title banner in the terminal
    header = pyfiglet.figlet_format("CineMatch", font="doom")
    print(header)

def load_genres():
    # Load movie and TV genres once at startup to avoid repeated API requests
    def fetch(endpoint):
        data = get_json(f"{BASE_URL}/{endpoint}", {"api_key": API_KEY}) or {}
        return {g["id"]: g["name"] for g in data.get("genres", [])}
    return fetch("genre/movie/list"), fetch("genre/tv/list")

def format_genres(genre_ids, genres_dict):
    return ", ".join(genres_dict.get(g) for g in genre_ids if genres_dict.get(g)) or "N/A"

def get_title(item):
    # TMDB uses "title" for movies and "name" for TV shows
    return item.get("title") or item.get("name") or "Unknown"

def get_release_date(item):
    # TMDB uses different release date fields for movies and TV shows
    return (item.get("release_date") or item.get("first_air_date") or "N/A")

def search_title(): 
    clear_screen()
    media = choose_media()
    media_label = "movie" if media == "movie" else "tv show"
    query = input(f"Search a {media_label} you like: ").strip()
    if not query: 
        print("Invalid input") 
        return None 
    data = get_json(f"{BASE_URL}/search/{media}", {"api_key": API_KEY, "query": query}) 
    if not data or not data.get("results"):
        print("No results found.") 
        return None 
    results = data["results"]
    print("\n========== SEARCH RESULTS ==========") 
    for i, item in enumerate(results, 1): 
        print(f"{i}. {get_title(item)} ({get_release_date(item)[:4]})") 
    
    print("0. Back to Main Menu")
    while True: 
        try: 
            choice = int(input(f"\nSelect a {media_label}: ")) 
            if choice == 0: return None
            if 1 <= choice <= len(results): return {**results[choice - 1], "media_type": media} 
        except ValueError: 
            pass
        print(f"Please enter 0-{len(results)} only.")
    
def similar_titles():
    # Retrieve recommendations based on the user's selected movie or TV show
    selected = search_title()
    if not selected: return
    media = selected["media_type"]
    data = get_json(f"{BASE_URL}/{media}/{selected['id']}/recommendations", {"api_key": API_KEY})
    title = get_title(selected)
    results = (data or {}).get("results", [])[:10]
    if not results:
        print("No recommendations found. Try another title.")
        return
    media_label = "MOVIES" if media == "movie" else "TV SHOWS"
    clear_screen()
    print(f"\n===== SIMILAR {media_label} LIKE {title.upper()} ({get_release_date(selected)[:4]}) =====")
    for i, item in enumerate(results, 1):
        print(f"{i}. {get_title(item)} ({get_release_date(item)[:4]})") 
    
    print("0. Back to Main Menu")
    while True:
        try:
            choice = int(input("\nSelect a title to view details: "))
            if choice == 0: return
            if 1 <= choice <= len(results):
                view_details(results[choice - 1])
                return
        except ValueError:
            pass
        print(f"Please enter 0-{len(results)} only.")

def view_trending():
    clear_screen()
    media = choose_media()
    data = get_json(f"{BASE_URL}/trending/{media}/day", {"api_key": API_KEY}) 
    results = [r for r in (data or {}).get("results", []) if r.get("vote_average") and r.get("vote_count")][:10]
    if not results:
        print("No trending items.") 
        return
    media_label = "movies" if media == "movie" else "tv shows"
    print(f"\n====== TRENDING {media_label.upper()} TODAY =====")
    for i, item in enumerate(results, 1):
        print(f"{i}. {get_title(item)}")

    print("0. Back to Main Menu")
    while True:
        try:
            choice = int(input("\nSelect: "))
            if choice == 0: return
            if 1 <= choice <= len(results): 
                view_details(results[choice - 1])
                return
        except ValueError:
            pass
        print(f"Please enter 0-{len(results)} only.")

def random_recommendations():
    print("\n========== SURPRISE ME! ==========")
    media = choose_media()
    # Filter recommendations to prioritize highly rated and well-reviewed titles
    data = get_json(f"{BASE_URL}/discover/{media}",
    {
        "api_key": API_KEY,
        "sort_by": "vote_average.desc",
        "vote_average.gte": 6.5,
        "vote_count.gte": 300,
        "page": random.randint(1, 50)
    })

    results = (data or {}).get("results", [])
    if not results:
        print("No recommendations found. Try again.")
        return
    print("\n🎲 Your Random Recommendation:")
    view_details(random.choice(results))    

def view_details(item):
    media = item.get("media_type") or ("movie" if item.get("title") else "tv")
    genres = MOVIE_GENRES if media == "movie" else TV_GENRES
    genre_text = format_genres(item.get("genre_ids", []), genres)
    rating = item.get("vote_average") or "N/A"
    title = get_title(item)
    release_date =  get_release_date(item)
    language = LANGUAGES.get(item.get('original_language'), item.get('original_language', 'N/A'))
    overview =  item.get('overview') or 'No summary available.'

    print("========== DETAILS ==========")
    print(f"{'Title':<10}: {title}")
    print(f"{'Type':<10}: {media}")
    print(f"{'Genres':<10}: {genre_text}")
    print(f"{'Release':<10}: {release_date}")
    print(f"{'Rating':<10}: ⭐ {rating:.1f}/10")
    print(f"{'Language':<10}: {language}")

    print("\nOVERVIEW")
    print("-" * 10)
    print(overview)

    if input("\nShow poster? (yes/no): ").strip().lower() == "yes":
        if item.get("poster_path"):
            webbrowser.open(IMAGE_URL + item["poster_path"])
        else:
            print("No poster available.")
    
    input("Press Enter to continue...")

def main():
    global MOVIE_GENRES, TV_GENRES
    MOVIE_GENRES, TV_GENRES = load_genres()
    while True:
        clear_screen()
        show_header()
        print("\n========== MAIN MENU ==========")
        print("1. Find Similar Movies/TV Shows")
        print("2. Trending Today")
        print("3. Surprise Me")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            similar_titles()
        elif choice == "2":
            view_trending()
        elif choice == "3":
            random_recommendations()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid option. Select 1-4 only.")
        
if __name__ == "__main__":
    main()
