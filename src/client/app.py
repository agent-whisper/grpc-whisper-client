import grpc

from typing import Union, Dict
from pathlib import Path
from src.client.schemas import TranscriptionOptions, Transcription
from src.generated.service_pb2 import TranscriptionRequest, TranscriptionResponse
from src.generated.service_pb2_grpc import TranscriptionServiceStub


class grpcWhisperClient:
    channel: grpc.Channel
    stub: TranscriptionServiceStub

    def __init__(self, address: str):
        self.channel = grpc.insecure_channel(address)
        self.stub = TranscriptionServiceStub(self.channel)

    def __del__(self):
        self.channel.close()

    def transcribe(
        self,
        audio: Union[bytes, str, Path],
        *,
        opt: Union[TranscriptionOptions, Dict] = None
    ) -> Transcription:
        if not opt:
            opt = {}
        if isinstance(opt, TranscriptionOptions):
            opt = opt.dict()

        payload = audio
        if isinstance(audio, (str, Path)):
            with open(audio, "rb") as f:
                payload = f.read()
        request = TranscriptionRequest(data=payload, **opt)
        response: TranscriptionResponse = self.stub.Transcribe(request)
        assert response.success, response.message
        return Transcription.from_proto(response.result)
