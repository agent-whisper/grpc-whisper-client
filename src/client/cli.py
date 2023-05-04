import grpc
import json
import click
import asyncio

from src.logger import logger
from src.client.app import grpcWhisperClient
from src.generated.service_pb2 import TranscriptionRequest, TranscriptionResponse
from src.generated.service_pb2_grpc import TranscriptionServiceStub


@click.command()
@click.argument("AUDIO_FILE")
@click.option(
    "--server", required=True, help='The gRPC Whisper server (e.g. "localhost:50051")'
)
@click.option(
    "--output-file",
    "-o",
    default=None,
    help="File location to save the output as json file. If omitted, will print the result in stdout instead.",
)
@click.option("--secure-port", is_flag=True, default=False)
def command(audio_file, server, output_file, secure_port):
    send_file(audio_file, server, output_file, secure_port)


def send_file(audio_file: str, server: str, output_file: str, secure_port: bool):
    client = grpcWhisperClient(server)
    transcription = client.transcribe(audio_file)

    if output_file:
        with open(output_file, "w") as f:
            json.dump(transcription.dict(), f, indent=4)
        logger.info(f"Response saved to {output_file}")
    else:
        logger.info(f"Response:\n{json.dumps(transcription.dict(), indent=4)}.")


if __name__ == "__main__":
    command()
