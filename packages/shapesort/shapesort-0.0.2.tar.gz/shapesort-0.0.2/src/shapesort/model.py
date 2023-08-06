import logging
from typing import List, Optional

import pydantic
from pydantic import validator

_logger = logging.getLogger(__name__)


class Transcript(pydantic.BaseModel):
    """ """

    transcript: str


class ItemAlternative(pydantic.BaseModel):
    """ """

    confidence: float
    content: str


class TranscriptItem(pydantic.BaseModel):
    """ """

    start_time: Optional[float]
    end_time: Optional[float]
    alternatives: List[ItemAlternative]
    type: str

    @validator("type")
    def type_must_be_either_pronounciation_or_punctuation(cls, v):
        _set = ["pronunciation", "punctuation"]
        if v not in _set:
            raise ValueError(f"{v} must be in {_set}")
        return v


class Transcripts(pydantic.BaseModel):
    """ """

    transcripts: List[Transcript]
    items: List[TranscriptItem]

    def __getitem__(self, item):
        return self.transcripts[item]

    def __len__(self):
        return len(self.transcripts)


class TranscribeBatch(pydantic.BaseModel):
    """ """

    jobName: str
    accountId: str
    results: Transcripts

    def __getitem__(self, item):
        return self.results[item]

    def __len__(self):
        return len(self.results)
