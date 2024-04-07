from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, DateTime
from datetime import datetime
from nanoid import generate
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """
    Sqlalchemy base model
    """

    id: Mapped[str] = mapped_column(
        String, default=lambda: generate(size=12), primary_key=True
    )


class TrackMetaData(BaseModel):
    __tablename__ = "track_metadata"
    title: Mapped[str] = mapped_column(String)
    artist: Mapped[str] = mapped_column(String)
    album: Mapped[str] = mapped_column(String)
    duration: Mapped[str] = mapped_column(Integer)
    at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"Track(id={self.id!r}, title={self.title!r}, artist={self.artist!r}, album={self.album!r}, duration={self.duration!r}, at={self.at!r})"
