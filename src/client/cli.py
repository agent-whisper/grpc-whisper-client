import click

from src.logger import logger
from src.client.app import grpcWhisperClient


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
@click.option("--language", default="en", show_default=True, help="The audio language.")
@click.option(
    "--format",
    "-f",
    default="json",
    show_default=True,
    type=click.Choice(["json", "srt", "text"]),
    help="How the transcription result should be outputted.",
)
@click.option("--secure-port", is_flag=True, default=False)
def command(audio_file, server, output_file, format, language, secure_port):
    client = grpcWhisperClient(server)
    transcription = client.transcribe(audio_file, opt={"language": language})

    if output_file:
        transcription.format(format, output_dir=output_file)
        logger.info(f"Response saved to {output_file}")
    else:
        logger.info(f"Response:\n{transcription.format(format)}.")


if __name__ == "__main__":
    command()
