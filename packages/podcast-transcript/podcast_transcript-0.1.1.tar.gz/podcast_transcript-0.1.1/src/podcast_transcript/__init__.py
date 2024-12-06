import argparse
from rich.console import Console
from .single_track import transcribe


def transcribe_cli():
    console = Console()

    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="Transcribe an MP3 file from a given URL."
    )

    # Add the mp3_url positional argument
    parser.add_argument("mp3_url", type=str, help="URL of the MP3 file to transcribe.")

    # Parse the command-line arguments
    try:
        args = parser.parse_args()
        mp3_url = args.mp3_url
    except argparse.ArgumentError as e:
        console.print(f"[red]Argument parsing error: {e}[/red]")
        exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error during argument parsing: {e}[/red]")
        exit(1)

    # Start transcription process
    try:
        console.print(f"[blue]Starting transcription for:[/blue] {mp3_url}")
        transcript_paths = transcribe(mp3_url)
        for name, path in transcript_paths.items():
            console.print(
                f"[green]Transcript in {name} format saved to:[/green] {path}"
            )
        console.print("[green]Transcription complete![/green]")
        exit(0)
    except Exception as e:
        console.print(f"[red]Error during transcription: {e}[/red]")
        exit(1)


if __name__ == "__main__":
    transcribe_cli()
