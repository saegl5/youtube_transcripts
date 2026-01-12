import re

def extract_video_id(url_or_id: str) -> str:
    s = url_or_id.strip()

    # Accept raw video IDs
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s

    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, s)
        if m:
            return m.group(1)

    raise ValueError(f"Could not extract a video id from: {url_or_id}")
