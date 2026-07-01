from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
)

def extract_video_id(url : str) -> str:
    parsed_url = urlparse(url)

    # Normal YouTube URL
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]

    # Short YouTube URL
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    return None

def get_transcript(url: str) -> str:
    

    video_id = extract_video_id(url)

    if video_id is None:
        raise ValueError("Invalid YouTube URL.")

    try:
        ytt_api = YouTubeTranscriptApi()

        transcripts = ytt_api.fetch(
            video_id,
            languages=["en"]
        )

        transcript = " ".join(
            snippet.text
            for snippet in transcripts
        )

        return transcript

    except NoTranscriptFound:
        raise Exception("English transcript not found.")

    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")

    except Exception as e:
        raise Exception(f"Unexpected Error: {e}")