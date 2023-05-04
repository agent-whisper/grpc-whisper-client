from typing import List
from pydantic import BaseModel

from src.generated.result_pb2 import Segment, TranscriptionResult


class TranscriptionOptions(BaseModel):
    language: str = "en"
    initialPrompt: str = None


class Segment(BaseModel):
    id: int
    seek: int
    start: float
    end: float
    text: str
    tokens: List[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float
    no_speech_prob: float

    @classmethod
    def from_proto(cls, obj: Segment):
        return cls(
            id=obj.id,
            seek=obj.seek,
            start=obj.start,
            end=obj.end,
            text=obj.text,
            tokens=[token for token in obj.tokens],
            temperature=obj.temperature,
            avg_logprob=obj.avg_logprob,
            compression_ratio=obj.compression_ratio,
            no_speech_prob=obj.no_speech_prob,
        )


class Transcription(BaseModel):
    text: str
    language: str
    segments: List[Segment]

    @classmethod
    def from_proto(cls, obj: TranscriptionResult):
        return cls(
            text=obj.text,
            language=obj.language,
            segments=[Segment.from_proto(segment) for segment in obj.segments],
        )
