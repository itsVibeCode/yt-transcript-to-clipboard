# youtube/subtitle_downloader.py
"""
Module for downloading and cleaning YouTube subtitles with default audio language.
"""

from yt_dlp import YoutubeDL
from typing import Optional, Union
from utils.helpers import clean_subtitle_text, clean_segment_subtitles
from youtube.default_lang import get_default_language
import requests


def download_subtitles(video_url: str, timeout: int = 30) -> Optional[str]:
    """
    Download subtitles (captions) from a YouTube video in the language of the main audio track.

    Args:
        video_url (str): full YouTube video URL
        timeout (int): max time in seconds to wait

    Returns:
        str: cleaned subtitle text if SRT available,
             cleaned segment text if only JSON segments available,
             None if no subtitles at all
    """
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitlesformat': 'srt',
        'quiet': True,
        'no_warnings': True,
    }

    default_lang = get_default_language(video_url)
    if not default_lang:
        print("Cannot determine default audio language")
        return None

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # 1. Check requested_subtitles (SRT)
            requested = info.get('requested_subtitles') or {}
            if requested and default_lang in requested:
                sub_url = requested[default_lang]['url']
                r = requests.get(sub_url, timeout=timeout)
                if r.status_code == 200:
                    # Clean SRT text
                    return clean_subtitle_text(r.text)

            # 2. Check normal subtitles (may be segmented JSON)
            subtitles = info.get('subtitles') or {}
            if subtitles and default_lang in subtitles:
                entry = subtitles[default_lang]
                sub_text = _fetch_subtitle_url(entry, timeout)
                if sub_text:
                    # If entry is already SRT, clean with SRT cleaner
                    if isinstance(sub_text, str):
                        return clean_subtitle_text(sub_text)
                    # If entry is segment JSON/dict, clean with segment cleaner
                    elif isinstance(sub_text, dict):
                        return clean_segment_subtitles(sub_text)

            # 3. Check automatic_captions (may be segmented JSON)
            auto_subs = info.get('automatic_captions') or {}
            if auto_subs and default_lang in auto_subs:
                entry = auto_subs[default_lang]
                sub_text = _fetch_subtitle_url(entry, timeout)
                if sub_text:
                    if isinstance(sub_text, str):
                        return clean_subtitle_text(sub_text)
                    elif isinstance(sub_text, dict):
                        return clean_segment_subtitles(sub_text)

            print(f"No subtitles found for default language: {default_lang}")
            return None

    except Exception as e:
        print(f"Error downloading subtitles: {e}")
        return None


def _fetch_subtitle_url(entry: Union[dict, list], timeout: int) -> Optional[Union[str, dict]]:
    """
    Fetch subtitle content from URL(s). Returns string (SRT) or dict (JSON segments).

    Args:
        entry (dict|list): subtitle info from yt-dlp
        timeout (int): HTTP request timeout

    Returns:
        str|dict: subtitle content
    """
    urls = []
    if isinstance(entry, list):
        for fmt in entry:
            if 'url' in fmt:
                urls.append(fmt['url'])
    elif isinstance(entry, dict) and 'url' in entry:
        urls.append(entry['url'])
    else:
        return None

    for url in urls:
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                content_type = r.headers.get('Content-Type', '')
                if 'json' in content_type or 'javascript' in content_type:
                    return r.json()  # return segment dict
                else:
                    return r.text  # return SRT string
        except Exception as e:
            print(f"Error fetching subtitle URL {url}: {e}")
    return None

if __name__ == "__main__":
    auto_en = 'https://www.youtube.com/watch?v=Gwct_dJDjJE'
    ruru = 'https://www.youtube.com/watch?v=bu2ADsx6yR4'
    masturbist = 'https://www.youtube.com/watch?v=ZFoNBxpXen4'
    res_raw = download_subtitles(ruru)
    # print(res_raw)
    print('*'*1000)
    print(res_raw)
