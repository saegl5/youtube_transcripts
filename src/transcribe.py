from __future__ import annotations

from typing import Optional

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled  # type: ignore

from .utils import extract_video_id


def transcript_from_url(url_or_id: str, languages: Optional[list[str]] = None) -> str:
    """
    Returns transcript as a single string for any YouTube URL where captions exist.

    Uses youtube-transcript-api. Compatible with both:
    - new API: YouTubeTranscriptApi().fetch() / .list()
    - old API: YouTubeTranscriptApi.get_transcript() / .list_transcripts()
    """
    languages = languages or ["en", "en-US"]
    video_id = extract_video_id(url_or_id)

    # ---- New API path (documented) ----
    ytt_api = YouTubeTranscriptApi()

    if hasattr(ytt_api, "fetch") and hasattr(ytt_api, "list"):
        try:
            fetched = ytt_api.fetch(video_id, languages=languages)
            # fetched is iterable, each item has `.text`
            lines = [snippet.text.replace("\n", " ").strip() for snippet in fetched if snippet.text]
            return "\n".join([ln for ln in lines if ln])
        except Exception:
            # Fall through to a more explicit search/translate approach
            pass

        try:
            transcript_list = ytt_api.list(video_id)

            transcript = None

            # Prefer manually created
            for lang in languages:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    break
                except Exception:
                    pass

            # Then generated
            if transcript is None:
                for lang in languages:
                    try:
                        transcript = transcript_list.find_generated_transcript([lang])
                        break
                    except Exception:
                        pass

            # Then translate to first preferred language
            if transcript is None:
                target = languages[0]
                for t in transcript_list:
                    if getattr(t, "is_translatable", False):
                        transcript = t.translate(target)
                        break

            if transcript is None:
                raise RuntimeError(
                    "No transcript available for this video (no captions, disabled, or unavailable)."
                )

            fetched = transcript.fetch()
            lines = [snippet.text.replace("\n", " ").strip() for snippet in fetched if snippet.text]
            return "\n".join([ln for ln in lines if ln])

        except (NoTranscriptFound, TranscriptsDisabled):
            raise RuntimeError("No transcript available (not found or disabled).")

    # ---- Old API fallback (legacy) ----
    # If you ever use an older youtube-transcript-api version again
    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        items = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)  # type: ignore[attr-defined]
        lines = [(it.get("text") or "").replace("\n", " ").strip() for it in items]
        lines = [x for x in lines if x]
        return "\n".join(lines)

    raise RuntimeError(
        "Unsupported youtube-transcript-api version: missing expected methods."
    )
