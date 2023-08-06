from typing import Dict, Union

from dataclasses import dataclass
from .audio_pb2 import Status


@dataclass
class AlvenirResponse:
    status: Status
    transcription: str
    full_document: Union[Dict, None] = None
