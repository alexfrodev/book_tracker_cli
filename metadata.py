"""Handles book metadata fetching from APIs with caching"""

import json
import requests
import typer
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


METADATA_CACHE = Path("metada_cache")
METADATA_CACHE.mkdir(exist_ok=True)


class MetadataFetcher:
    @staticmethod
    def _get_cache_key(title:str, author:str ="") -> str:
        """Generate cache filename"""
        key = f"{title.lower.replace(' ', '_')}"
        if author:
            key += f"_{author.lower.replace(' ', '_')}"
        return f"{key[:100]}.json"

    @staticmethod
    def _fetch_from_api(title:str, author:str = "") -> Optional[Dict]:
        """API call to Open Library"""
        try:
            params = {"q": f"{title}+{author}" if author else title, "limit":1}
            response = requests.get(
                "https://openlibrary.org/search.json",
                params=params,
                timeout=5
            )
            response.raise_for_status()
            return response.json
        except Exception as e:
            typer.echo(f"API Error:{str(e)}", err=True)
            return None
    @classmethod
    def fetch_metadata(cls, title:str, author:str = "") -> Optional[Dict]:
        """Main method: tries cache, then API"""
        cache_file = METADATA_CACHE / cls._get_cache_key(title, author)

        #Try cache
        if cache_file.exists():
            cached_data = json.loads(cache_file.read_text())
            if datetime.now() - cached_data["timestamp"] < 86400:
                return cached_data["data"]

        #Fetch from API
        raw_data = cls._fetch_from_api(title, author)
        if not raw_data or not raw_data.get("docs"):
            return None
        #TEMP
        print("RAW API RESPONSE:", raw_data)

        #Parse data
        book_data = raw_data["docs"][0]
        parsed = {
            "title": book_data.get("title", title), 
            "author": ", ".join(book_data.get("author_name", [])) or "Unknown",
            "year": book_data.get("first_publish_year"), 
            "isbn": book_data.get("isbn", [None])[0], 
            "publisher": ", ".join(book_data.get("publisher", [])),
            "page_count": book_data.get("number_of_pages"),
            "description": (
            book_data["description"]
            if isinstance(book_data.get("description"), str)

            else " ".join(book_data["description"])
            if isinstance(book_data.get("description"), list)

            else"No desciption avaliable"
            ),
            "olid": book_data.get("edition_key", [None])[0]
        }

        #Save to cache
        cache_file.write_text(json.dumps({
            "timestamp": datetime.now().timestamp(),
            "data": parsed
        }))

        return parsed
