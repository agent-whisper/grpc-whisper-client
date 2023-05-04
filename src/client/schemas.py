import json

from typing import List
from pydantic import BaseModel
from datetime import timedelta
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

    def output_srt(self) -> str:
        output = [
            f"{self.id + 1}",
            f"{self._format_timing(self.start)} --> {self._format_timing(self.end)}",
            self.text,
        ]
        return "\n".join(output)

    def _format_timing(self, total_seconds: float):
        td = timedelta(seconds=total_seconds)
        if td.microseconds > 0:
            microseconds = str(td.microseconds)[:3]
            timing = f"{str(timedelta(seconds=td.seconds))},{microseconds}"
        else:
            timing = f"{str(td)},000"
        if total_seconds < 36_000:
            return f"0{timing}"
        else:
            return timing


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

    def format(self, format: str, **kwargs):
        if format == "json":
            return self.output_json(**kwargs)
        elif format == "text":
            return self.output_text(delimiter=kwargs.get("delimiter", "\n"))
        elif format == "srt":
            return self.output_srt(**kwargs)
        raise ValueError(f"Unsupported format: {format}")

    def output_json(
        self,
        *,
        output_dir: str = None,
        ensure_ascii: bool = False,
        encoding: str = "utf-8",
    ):
        if output_dir:
            with open(output_dir, "w", encoding=encoding) as f:
                json.dump(self.dict(), f, ensure_ascii=ensure_ascii, indent=4)
        else:
            return json.dumps(self.dict(), ensure_ascii=ensure_ascii, indent=4)

    def output_text(self, *, delimiter=" "):
        return delimiter.join(segment.text for segment in self.segments)

    def output_srt(self, *, output_dir: str = None, encoding: str = "utf-8"):
        output = "\n\n".join([segment.output_srt() for segment in self.segments])
        if output_dir:
            with open(output_dir, "w", encoding=encoding) as f:
                f.write(output)
        else:
            return output
