from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, func, ForeignKey, Integer, DateTime
from typing import Optional, List
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Facility(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    logs: Mapped[list["OccupancyLog"]] = relationship(back_populates="facility")


class OccupancyLog(Base):
    __tablename__ = "occupancy_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))

    count: Mapped[int] = mapped_column(Integer)
    percent: Mapped[int] = mapped_column(Integer)

    # stored per-entry for future-proofing (i.e. gym renovations)
    capacity: Mapped[int] = mapped_column(Integer)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), index=True
    )

    facility: Mapped["Facility"] = relationship(back_populates="logs")
