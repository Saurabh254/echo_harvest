from pydantic import BaseModel


class MetaData(BaseModel):
    """MetaData Schema Class"""

    title: str | None = ""
    album: str | None = ""
    artist: str | None = ""
    duration: int | None = 0
