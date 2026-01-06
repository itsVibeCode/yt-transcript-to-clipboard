# youtube/audio_lang.py
from yt_dlp import YoutubeDL
from typing import Optional


# youtube/audio_lang.py
from yt_dlp import YoutubeDL
from typing import Optional


def normalize_lang(lang: str) -> str:
    """
    Normalize language code to base ISO 639-1.
    Examples:
        en-US -> en
        en_US -> en
        ru-RU -> ru
    """
    return lang.lower().replace('_', '-').split('-')[0]


def get_default_language(video_url: str, default: Optional[str] = None) -> Optional[str]:
    """
    Detect the default (main) audio language of a YouTube video
    and return a language code compatible with YouTube subtitles.

    Always returns base ISO 639-1 language code (e.g. 'en', 'ru').
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # 1. Best case: video-level language (already normalized by YouTube)
            lang = info.get('language')
            if lang:
                return normalize_lang(lang)

            # 2. Fallback: inspect audio formats
            for f in info.get('formats', []):
                if f.get('acodec') != 'none':
                    lang = f.get('language') or f.get('lang')
                    if lang and lang not in ('und', 'zxx'):
                        return normalize_lang(lang)

            return default

    except Exception as e:
        print(f"Error detecting audio language: {e}")
        return default


if __name__ == "__main__":
    auto_en = 'https://www.youtube.com/watch?v=Gwct_dJDjJE'
    ruru = 'https://www.youtube.com/watch?v=bu2ADsx6yR4'
    masturbist = 'https://www.youtube.com/watch?v=ZFoNBxpXen4'
    beluga = 'https://www.youtube.com/watch?v=kUjF9EH7v5s'
    lang = get_default_language(beluga)
    print("Audio language:", lang)
