# clipboard/clipboard_manager.py
import pyperclip

def get_clipboard_text() -> str | None:
    """
    Get current text from clipboard.
    Returns None if clipboard is empty or content is not text.
    """
    try:
        text = pyperclip.paste()
        if isinstance(text, str) and text.strip():
            return text.strip()
        return None
    except Exception as e:
        print(f"Error reading clipboard: {e}")
        return None

def set_clipboard_text(text: str) -> None:
    """
    Set given text to clipboard.
    """
    try:
        pyperclip.copy(text)
    except Exception as e:
        print(f"Error writing to clipboard: {e}")
