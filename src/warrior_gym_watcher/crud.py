from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas


def get_facility_by_name(db: Session, name: str) -> models.Facility | None:
    """
    Looks up a facility by name.
    """
    query = select(models.Facility).where(models.Facility.name == name)
    return db.execute(query).scalar_one_or_none()


def create_facility(db: Session, facility: schemas.FacilityCreate) -> models.Facility:
    """
    Adds a new facility to the database if it doesn't exist.
    """
    db_facility = models.Facility(name=facility.name)
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility


def create_occupancy_log(
    db: Session, log_data: schemas.OccupancyCreate, facility_id: int
) -> models.OccupancyLog:
    """
    Creates a historical snapshot of a facility's occupancy.
    """
    db_log = models.OccupancyLog(
        facility_id=facility_id,
        count=log_data.count,
        percent=log_data.percent,
        capacity=log_data.capacity,
    )
    db.add(db_log)
    db.commit()
    return db_log


def sync_scraped_data(db: Session, raw_data_list: list[dict]):
    """
    Validate raw scraped dictionaries into Pydantic schemas,
    find/create the appropriate facility,
    log current occupancy.
    """

    for raw_item in raw_data_list:
        occupancy_in = schemas.OccupancyCreate(**raw_item)
        facility = get_facility_by_name(db, occupancy_in.facility_name)

        if not facility:
            print(f"New facility found: {occupancy_in.facility_name}")
            new_fac = schemas.FacilityCreate(name=occupancy_in.facility_name)
            facility = create_facility(db, new_fac)

        create_occupancy_log(db, occupancy_in, facility.id)
