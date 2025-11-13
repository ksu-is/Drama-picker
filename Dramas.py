# Skipping the import section for now will go back and do that after fuctions are done

from typing import List, Dict, Optional
import json
import os
import sys
import subprocess
from urllib.parse import urljoin
from bs4 import BeautifulSoup


OUTPUT_FILE = "dramas.json"
IMDB_URL = "https://www.imdb.com"
HEADERS = {"User-Agent": "DramaPickerBot/1.0 (+https://example.com)"}


def fetch_html(url: str, timeout: int = 15) -> Optional[str]:
    """
    Fetch HTML using the curl command (subprocess). Returns the page HTML or None on error.
    """
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