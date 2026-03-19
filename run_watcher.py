import sys
import os
from warrior_gym_watcher.database import SessionLocal, init_db
from warrior_gym_watcher.services import FacilityOccupancyService
from warrior_gym_watcher.crud import sync_scraped_data


def run():
    init_db()
    service = FacilityOccupancyService()
    raw_data: list[dict] = service.fetch_occupancy()

    if not raw_data:
        print("No data found, portal may be down!")
        return

    try:
        with SessionLocal() as db:
            sync_scraped_data(db, raw_data)
            print("Data successfully fetched!")
    except Exception as e:
        print(f"Database sync failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
