import requests
from rich import print
from retrying import retry
from urllib.parse import urlparse


class HTTP:
    """HTTP Request"""

    def __init__(self, url) -> None:
        self.url = url
        self.timeout = 15

    @retry(stop_max_attempt_number=3)
    def get_data(self) -> dict:
        """HTTP GET"""
        r = requests.get(self.url, timeout=self.timeout)
        if r.status_code == 200:
            return r.json()
        else:
            print(r.json())


class TMDB:
    """TMDB API"""

    def __init__(self) -> None:
        self.api_url = "https://api.themoviedb.org/3"
        self.api_key = "10ee896781efe0090b9889362386ae74"
        self.language = "en-US"

    # TV Show
    def get_tv(self, tv_url: str) -> dict:
        """Get TV Show Data

        Args:
            tv_url (str): for example: https://www.themoviedb.org/tv/1399-game-of-thrones

        Returns:
            dict: TV Show Data
        """
        # Parse URL
        tv_urlparse = urlparse(tv_url)
        tv_api_url = f"{self.api_url}{tv_urlparse.path}?api_key={self.api_key}&language={self.language}"
        return HTTP(tv_api_url).get_data()
