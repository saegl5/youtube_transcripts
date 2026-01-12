import sys
from .transcribe import transcript_from_url


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python -m src "<youtube_url_or_video_id>"')
        raise SystemExit(1)

    transcript = transcript_from_url(
        sys.argv[1],
        languages=["en", "en-US"]
    )

    print(transcript)


if __name__ == "__main__":
    main()
