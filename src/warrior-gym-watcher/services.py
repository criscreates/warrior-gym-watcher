import requests
from bs4 import BeautifulSoup
import json
import http
from fake_useragent import UserAgent


class FacilityOccupancyService:
    def __init__(self):
        self.url = "https://warrior.uwaterloo.ca/FacilityOccupancy"
        self.ua = UserAgent()
        self.session = requests.Session()

    def _get_headers(self):
        return {"User-Agent": self.ua.random}

    def fetch_occupancy(self) -> list[dict]:
        try:
            response = requests.get(self.url, headers=self._get_headers())
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"HTTP error: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        return self._parse_soup(soup)

    def _parse_soup(self, soup: BeautifulSoup) -> list[dict]:
        results = []

        cards = soup.find_all("div", class_="occupancy-card")

        for card in cards:
            name_tag = card.find("h2")
            chart_data = card.find("canvas", class_="occupancy-chart")

            if not name_tag or not chart_data:
                continue

            name = name_tag.get_text(strip=True)

            cur_count = int(chart_data.get("data-occupancy", 0))
            remaining = int(chart_data.get("data-remaining", 0))
            ratio = float(chart_data.get("data-ratio", 0))

            results.append(
                {
                    "facility_name": name,
                    "count": cur_count,
                    "percent": int(ratio * 100),
                    "capacity": cur_count + remaining,
                }
            )

        return results
