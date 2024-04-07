import json
from echo_harvest.helpers import interface
from echo_harvest.internals.schemas import TracksStatusResp
from echo_harvest.internals.database import get_db
from sqlalchemy.orm import Session


class SocketEventHandler:
    def __init__(self, raw_event_resp) -> None:
        self._raw_event_resp = raw_event_resp
        self._event_resp = self.decode_event_resp(self._raw_event_resp)

    @staticmethod
    def decode_event_resp(raw_resp):
        return json.loads(raw_resp)

    def generate_response(self) -> TracksStatusResp:
        db: Session = next(get_db())
        if self._event_resp and self._event_resp["type"] == "status":
            resp = interface.get_stored_tracks_metadata(db=db)
            return json.dumps(resp, default=str)
