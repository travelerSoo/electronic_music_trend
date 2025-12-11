import pandas as pd
import requests



def get_beatport_track_info(artist: str, title: str):
    """Query Beatport API for BPM and genre given track title + artist."""
    # Beatport API endpoint
    API_URL = "https://api.beatport.com/v4/catalog/tracks"
    # Replace with the Bearer token you found
    HEADERS = {"Authorization": "Bearer XzbZH1N7AUlZ3v4Z6laO42XzWg1F8o"}
    params = {"artist_name": artist, "name": title}
    response = requests.get(url=API_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if results:
            first_track = results[0]
            bpm = first_track.get("bpm")
            genre = first_track.get("genre", {}).get("name")
            return bpm, genre
    return None, None

df = pd.read_csv("djmag_tracks.csv")

df["bpm"] = None
df["genre"] = None

for idx, row in df.iterrows():
    bpm, genre = get_beatport_track_info(row["artist"], row["title"])
    df.at[idx, "bpm"] = bpm
    df.at[idx, "genre"] = genre

df.to_csv("djmag_tracks_extended.csv", index=False)
