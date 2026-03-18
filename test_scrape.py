import requests
from bs4 import BeautifulSoup
import json
import http
from fake_useragent import UserAgent


def test_scrape():
    url = "https://warrior.uwaterloo.ca/FacilityOccupancy"

    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    response = requests.get(url, headers=headers)

    if response.status_code != http.HTTPStatus.OK:
        print(f"Failed to access site, status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    cards = soup.find_all("div", class_="occupancy-card")

    for card in cards:
        name_tag = card.find("h2")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)

        chart_data = card.find("canvas", class_="occupancy-chart")
        if not chart_data:
            continue

        cur_count = int(chart_data.get("data-occupancy", 0))
        remaining = int(chart_data.get("data-remaining", 0))
        ratio = float(chart_data.get("data-ratio", 0))

        max_cap = cur_count + remaining
        cap_pct = int(ratio * 100)

        results.append(
            {
                "facility-name": name,
                "count": cur_count,
                "percent": cap_pct,
                "capacity": max_cap,
            }
        )

    return results


if __name__ == "__main__":
    results = test_scrape()

    if results:
        print(json.dumps(results, indent=4))
