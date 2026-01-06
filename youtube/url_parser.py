# youtube/url_parser.py
"""
Module to parse YouTube URLs and extract video ID.
"""

from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from a URL.

    Supports:
        - Full URLs: https://www.youtube.com/watch?v=VIDEO_ID
        - Short URLs: https://youtu.be/VIDEO_ID
        - URLs with timecode or additional parameters
    Returns None if URL is not a valid YouTube video.
    """
    if not isinstance(url, str) or not url.strip():
        return None

    url = url.strip()
    parsed = urlparse(url)

    # Short URL: youtu.be/VIDEO_ID
    if parsed.netloc in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/")

    # Full URL: youtube.com/watch?v=VIDEO_ID
    if parsed.netloc in ("youtube.com", "www.youtube.com"):
        if parsed.path == "/watch":
            query = parse_qs(parsed.query)
            video_ids = query.get("v")
            if video_ids:
                return video_ids[0]

    return None
