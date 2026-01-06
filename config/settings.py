# config/settings.py
"""
Application configuration.
"""

# ------------------------
# Hotkeys
# ------------------------
# Ordered list of keys: Ctrl + Shift + Y
HOTKEY_COMBINATION = ['ctrl', 'shift', 'y']

# ------------------------
# Timeouts
# ------------------------
SUBTITLE_DOWNLOAD_TIMEOUT = 30  # seconds

# ------------------------
# Main window
# ------------------------
MAIN_WINDOW_OPACITY = 0.85
MAIN_WINDOW_WIDTH = 700
MAIN_WINDOW_HEIGHT = 400

# ------------------------
# Notifications
# ------------------------
NOTIFICATION_VISIBLE_TIME = int(1.5 * 1000)  # 1.5 секунды
NOTIFICATION_FADE_TIME = int(0.5 * 1000)     # 0.5 секунды, если нужно
NOTIFICATION_OFFSET_X = 10
NOTIFICATION_OFFSET_Y = 10
NOTIFICATION_OPACITY = 0.9

# ------------------------
# YouTube
# ------------------------
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
