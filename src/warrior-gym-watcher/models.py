from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, func, ForeignKey
from typing import Optional, List
from datetime import datetime


class Base(DeclarativeBase):
    pass
