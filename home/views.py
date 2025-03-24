from django.shortcuts import render
import requests
from datetime import datetime



def get_genres():
    """Mengambil daftar genre dari API Jikan."""
    url = "https://api.jikan.moe/v4/genres/anime"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])  # Ambil daftar genre
    return []


def filter_hentai(anime_list):
    """Menghapus anime yang memiliki genre Hentai."""
    filtered_anime = []
    for anime in anime_list:
        genres = [genre["name"].lower() for genre in anime.get("genres", [])]
        if "hentai" not in genres:
            filtered_anime.append(anime)
    return filtered_anime


def get_seasons():
    """Menghasilkan daftar season dan tahun tanpa duplikasi."""
    current_year = datetime.now().year
    seasons = ["winter", "spring", "summer", "fall"]
    years = list(range(current_year, 2000,-1))
    return {"seasons": seasons, "years": years}



def get_anime(request):
    page = int(request.GET.get("page", 1))  # Ambil nomor halaman, default = 1
    genre_id = request.GET.get("genre", "")
    selected_season = request.GET.get("season", "")
    selected_year = request.GET.get("year", "")

    url = "https://api.jikan.moe/v4/anime"

    # Parameter API
    params1 = {
        "page": page,
        "sort": "desc",
        "order_by": "start_date",
    }
    

    params2 = params1.copy()
    params2["page"] = page + 1  # Halaman berikutnya

    if selected_season and selected_year:
        url = f"https://api.jikan.moe/v4/seasons/{selected_year}/{selected_season}"
        params1 = {"page": page}
        params2 = {"page": page + 1}
        
    if genre_id:
        params1["genres"] = genre_id
        params2["genres"] = genre_id

    response1 = requests.get(url, params=params1)
    response2 = requests.get(url, params=params2)

    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json().get("data", [])
        data2 = response2.json().get("data", [])

        combined_anime = {anime["mal_id"]: anime for anime in data1 + data2}.values()
        filtered_anime = filter_hentai(combined_anime)
        has_next_page = response2.json().get("pagination", {}).get("has_next_page", False)

        season_data = get_seasons()

        return render(
            request,
            "index.html",
            {
                "anime_list": list(filtered_anime)[:30],
                "current_page": page,
                "has_next_page": has_next_page,
                "genres": get_genres(),
                "seasons": season_data["seasons"],
                "years": season_data["years"],
                "selected_season": selected_season,
                "selected_year": selected_year,
                "selected_genre": (
                    int(genre_id) if genre_id else None
                ),  # Genre yang sedang dipilih
            },
        )
    else:
        return render(request, "index.html", {"error": "Anime not found"})

def get_anime_info(request, anime_id):
    """Mengambil detail anime berdasarkan anime_id termasuk trailer video."""
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"
    response = requests.get(url)
    if response.status_code == 200:
        anime_info = response.json().get("data", {})

        # Cek apakah ada trailer video
        trailer_url = anime_info.get("trailer", {}).get("embed_url", "")

        return render(
            request,
            "details/index.html",
            {
                "anime": anime_info,
                "trailer_url": trailer_url,  # Kirim trailer ke template
            },
        )
    else:
        return render(request, "details/index.html", {"error": "Anime not found"})
