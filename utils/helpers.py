# utils/helpers.py
"""
Utility helper functions used across the project.
"""

import re
from typing import List, Dict


def is_non_empty_string(value) -> bool:
    """
    Check if value is a non-empty string.
    """
    return isinstance(value, str) and bool(value.strip())


def clean_subtitle_text(raw_text: str) -> str:
    """
    Clean subtitle text from timestamps, indexes and formatting.

    Supports SRT / VTT-like formats.

    Args:
        raw_text (str): raw subtitle content

    Returns:
        str: cleaned plain text
    """
    if not is_non_empty_string(raw_text):
        return ""

    text = raw_text

    # Remove subtitle indexes (numbers on separate lines)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)

    # Remove timestamps (SRT & VTT)
    text = re.sub(
        r'\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[.,]\d{3}',
        '',
        text
    )

    # Remove HTML tags (like <i>, <b>, etc.)
    text = re.sub(r'<[^>]+>', '', text)

    # Remove extra empty lines
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()

# utils/segment_helpers.py
"""
Helper to clean YouTube subtitles in segment (JSON) format.
"""


def clean_segment_subtitles(segment_data: Dict) -> str:
    """
    Clean YouTube segmented subtitles (JSON) into plain text.

    Args:
        segment_data (dict): subtitle data containing 'events' with 'segs'

    Returns:
        str: concatenated and cleaned subtitle text
    """
    if not segment_data or 'events' not in segment_data:
        return ""

    cleaned_lines: List[str] = []

    for event in segment_data['events']:
        segs = event.get('segs') or []
        for seg in segs:
            text = seg.get('utf8', '').replace('\n', ' ').strip()
            if text:
                cleaned_lines.append(text)

    # Join all segments with a space
    return ' '.join(cleaned_lines)
