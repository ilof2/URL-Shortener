import enum
from typing import List

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api import db


class StatusEnum(enum.Enum):
    CREATED = "created"
    DONE = "done"
    FAILED = "failed"


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(Enum(StatusEnum), default=StatusEnum.CREATED)
    result_id: Mapped[str] = mapped_column(String(36), nullable=True, unique=True)
    urls: Mapped[List["URL"]] = relationship(back_populates="task")

    def __repr__(self):
        return f"{self.id} ({self.status})"
