from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api import db


class URL(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    old_url: Mapped[str] = mapped_column(unique=True)
    short_url: Mapped[str] = mapped_column(String(36), nullable=True, unique=True)

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=True)
    task: Mapped["Task"] = relationship(back_populates="urls")

    def __repr__(self):
        return f"{self.id}: {self.old_url} - {self.short_url}"
