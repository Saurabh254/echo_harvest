from pydantic import BaseModel


class MetaData(BaseModel):
    """MetaData Schema Class"""

    title: str | None = ""
    album: str | None = ""
    artist: str | None = ""
    duration: int | None = 0

    def __str__(self) -> str:
        return f"TrackMetaData(title={self.title}, album={self.album}, artist={self.artist}, duration={self.duration})"


class MetaDataResp(MetaData):
    id: str | None


class TracksStatusResp(BaseModel):
    tracks: list[MetaDataResp]
    play_count: int = 0
    current_playing: MetaDataResp
