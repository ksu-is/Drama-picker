
from typing import List, Dict, Optional
import json
import os
import sys
import subprocess
from urllib.parse import urljoin
from bs4 import BeautifulSoup


OUTPUT_FILE = "dramas.json"
IMDB_URL = "https://www.imdb.com"
HEADERS = {"User-Agent": "DramaPickerBot/1.0" "(+https://www.imdb.com)"}


def fetch_html(url: str, timeout: int = 15) -> Optional[str]:

    try:
        # -s: silent, -S: show errors, -L: follow redirects, --max-time uses seconds
        proc = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", HEADERS.get("User-Agent", ""), url],
            capture_output=True,
            text=True,
            check=True,
        )
        return proc.stdout
    except subprocess.CalledProcessError as e:
        print("curl failed:", e)
        return None
    except Exception as e:
        print("Fetch error:", e)
        return None
    
def save_output(data: Dict, movies_path: str = "movies.txt", tv_path: str = "tvshows.txt") -> None:
    """
    Save the output data to text files.
    """
    try:
        with open(movies_path, "w", encoding="utf-8") as mf:
            for item in data.get("movies", []):
                title = item.get("title", "")
                url = item.get("url", "")
                genres = ", ".join(item.get("genres", []))
                watched = "yes" if item.get("watch") else "no"
                mf.write(f"{title} | {url} | {genres} | {watched}\n")
        with open(tv_path, "w", encoding="utf-8") as tf:
            for item in data.get("tv_shows", []):
                title = item.get("title", "")
                url = item.get("url", "")
                genres = ",".join(item.get("genres", []))
                watched = "yes" if item.get("watch") else "no"
                tf.write(f"{title} | {url} | {genres} | {watched}\n")
        print(f"Saved movies to {movies_path} and tv shows to {tv_path}")
    except Exception as e:
        print("Save error:", e)