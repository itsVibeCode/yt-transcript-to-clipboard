from clipboard.clipboard_manager import get_clipboard_text, set_clipboard_text
from youtube.url_parser import extract_video_id
from youtube.subtitle_downloader import download_subtitles
from utils.helpers import clean_subtitle_text
from utils.async_runner import run_with_timeout
from core.logger_setup import get_logger

class AppController:
    def __init__(self, main_window, timeout: int = 30):
        self.main_window = main_window
        self.timeout = timeout
        self.logger = get_logger()

    def handle_hotkey(self):
        """Вызывается при нажатии горячей клавиши."""
        try:
            self._notify("Starting subtitle download…", type_="info")

            result, status = run_with_timeout(
                self._process_clipboard,
                timeout=self.timeout
            )

            if status == "timeout":
                self.logger.error("Operation timed out")
                self._notify("Subtitle download timed out", type_="error")
            elif status == "error":
                self.logger.error(f"Processing error: {result}")
                self._notify(f"Error while processing subtitles: {result}", type_="error")
            else:
                self.logger.info("Operation completed successfully")
                self._notify("Subtitles copied to clipboard!", type_="success")

        finally:
            # В конце каждой попытки ставим разделитель в лог
            if self.main_window:
                self.main_window.after(0, self.main_window.add_attempt_separator)
    def _process_clipboard(self):
        """Основная обработка: копируем буфер, получаем ID видео, скачиваем субтитры, очищаем, копируем обратно."""
        text = get_clipboard_text()
        if not text:
            raise ValueError("Clipboard is empty or not text")
        self.logger.info("Clipboard text read")
        if self.main_window:
            self.main_window.after(0, lambda: self.main_window.log_message("Clipboard text read..."))

        video_id = extract_video_id(text)
        if not video_id:
            msg = "Clipboard does not contain a YouTube video link."
            # self.logger.info(msg)
            self.main_window.log_message(msg)
            raise ValueError(msg)
        self.logger.info(f"YouTube video detected: https://www.youtube.com/watch?v={video_id}")
        if self.main_window:
            self.main_window.after(0, lambda: self.main_window.log_message(f"YouTube video detected: https://www.youtube.com/watch?v={video_id}"))

        subtitles_raw = download_subtitles(f"https://www.youtube.com/watch?v={video_id}")
        if not subtitles_raw:
            raise RuntimeError("Failed to download subtitles")
        self.logger.info("Subtitles downloaded")
        if self.main_window:
            self.main_window.after(0, lambda: self.main_window.log_message("Subtitles downloaded"))

        clean_text = clean_subtitle_text(subtitles_raw)
        set_clipboard_text(clean_text)
        self.logger.info("Clean subtitles copied to clipboard")
        if self.main_window:
            self.main_window.after(0, lambda: self.main_window.log_message("Clean subtitles copied to clipboard"))

    def _notify(self, message: str, type_: str = "info"):
        """Выводим важное уведомление внизу и в консоль."""
        print(message)
        if self.main_window:
            self.main_window.after(0, lambda: self.main_window.show_notification(message, type_))
