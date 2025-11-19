
from typing import List, Dict, Optional
import json
import os
import sys
import subprocess
from urllib.parse import urljoin
from bs4 import BeautifulSoup


OUTPUT_FILE = "dramas.json"
IMDB_URL = "https://www.imdb.com/chart/toptv/"
HEADERS = {"User-Agent": "DramaPickerBot/1.0" "(+https://www.imdb.com/chart/toptv/)"}


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
        
        
# default output file paths used by save_output and for simple printing
movies_path = "movies.txt"
tv_path = "tvshows.txt"

print(movies_path, "Movies List:")
print(tv_path, "TV Shows List:")
















import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urljoin
import re

BASE_URL = "https://www.imdb.com/"

def get_tv_links(url):
    """
    Scrape IMDb homepage for TV show links.
    Only keeps links with '/title/tt#######/' and containing 'TV' in category.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    # Pattern to match title links
    title_pattern = re.compile(r"^/title/tt\d+/")
    for a in soup.find_all("a", href=True):
        # ensure `a` is a Tag (not a NavigableString/PageElement) so .get is available
        if not isinstance(a, Tag):
            continue
        href_attr = a.get("href")
        if not href_attr:
            continue
        # AttributeValueList or other non-str types can occur; coerce to str and split once
        href = str(href_attr).split("?", 1)[0]
        if title_pattern.match(href):
            full_url = urljoin(url, href)
            links.append(full_url)

    # Remove duplicates
    links = sorted(list(set(links)))
    return links

def extract_tv_metadata(tv_url):
    """
    Scrape metadata from a TV show page.
    Returns a dictionary with Title, Year, Rating, Genres, Episodes, URL.
    """
    response = requests.get(tv_url)
    soup = BeautifulSoup(response.text, "html.parser")

    metadata = {"URL": tv_url}

    # Title
    title_tag = soup.find("h1")
    metadata["Title"] = title_tag.get_text(strip=True) if title_tag else "N/A"

    # Year
    year_tag = soup.find("span", id="titleYear")
    metadata["Year"] = year_tag.get_text(strip=True) if year_tag else "N/A"

    # Rating
    rating_tag = soup.find("span", itemprop="ratingValue")
    metadata["Rating"] = rating_tag.get_text(strip=True) if rating_tag else "N/A"

    # Genres
    genre_tags = soup.find_all("a", href=re.compile(r"/search/title\?genres="))
    metadata["Genres"] = ", ".join([g.get_text(strip=True) for g in genre_tags]) if genre_tags else "N/A"

    # Number of episodes (if available)
    episode_tag = soup.find("span", class_="bp_sub_heading")
    if episode_tag and "Episodes" in episode_tag.get_text():
        metadata["Episodes"] = episode_tag.get_text(strip=True)
    else:
        # Try alternative method
        episodes_alt = soup.find("div", class_="EpisodeList")
        metadata["Episodes"] = "Available" if episodes_alt else "N/A"

    return metadata

def save_tv_metadata(tv_data_list, filename="tv_metadata.txt"):
    """Save TV metadata into a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        for tv in tv_data_list:
            for key, value in tv.items():
                f.write(f"{key}: {value}\n")
            f.write("-" * 50 + "\n")
    print(f"Saved {len(tv_data_list)} TV shows to {filename}!")

# -------------------------
# MAIN PROGRAM
# -------------------------

print("=== IMDb TV Show Metadata Scraper ===")

# IMDb URL to scrape from
url = "https://www.imdb.com/chart/toptv/"

print(f"Scraping TV show links from {url} ...")
tv_links = get_tv_links(url)
print(f"Found {len(tv_links)} TV show links!\n")

tv_metadata_list = []
for i, link in enumerate(tv_links, start=1):
    print(f"Processing {i}/{len(tv_links)}: {link}")
    try:
        metadata = extract_tv_metadata(link)
        tv_metadata_list.append(metadata)
    except Exception as e:
        print(f"Failed to process {link}: {e}")

save_tv_metadata(tv_metadata_list)