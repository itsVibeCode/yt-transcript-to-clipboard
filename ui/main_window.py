import os
import sys
import tkinter as tk

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Transcript Downloader")
        self.geometry("600x400")
        ico_path = resource_path("assets/icon.ico")
        png_path = resource_path("assets/icon.png")
        try:
            self.iconbitmap(ico_path)  # Windows
        except Exception:
            pass

        try:
            icon = tk.PhotoImage(file=png_path)
            self.iconphoto(True, icon)  # cross-platform
        except Exception:
            pass

        # Логовое текстовое поле (все консольные сообщения)
        self.log_text = tk.Text(self, wrap="word", state="disabled", height=20)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Поле текущего уведомления (цветной текст)
        self.notification_label = tk.Label(self, text="", anchor="w", font=("Arial", 12))
        self.notification_label.pack(fill="x", padx=10, pady=(0,10))
        self.log_message('Copy YouTube link and press Ctrl + Shift + Y')

    def log_message(self, message: str):
        """Выводим обычное сообщение в логовое поле"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def show_notification(self, message: str, type_: str = "info"):
        """Выводим цветное уведомление внизу, не дублируем в лог"""
        color = "blue"
        if type_ == "success":
            color = "green"
        elif type_ == "error":
            color = "red"

        self.notification_label.config(text=message, fg=color)

    def add_attempt_separator(self):
        """Ставим разделитель после завершения одной попытки"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", "------------------------------\n")
        self.log_message('Copy YouTube link and press Ctrl + Shift + Y')
        self.log_text.see("end")
        self.log_text.config(state="disabled")
