import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Subtitles Downloader")
        self.geometry("600x400")

        # Логовое текстовое поле (все консольные сообщения)
        self.log_text = tk.Text(self, wrap="word", state="disabled", height=20)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Поле текущего уведомления (цветной текст)
        self.notification_label = tk.Label(self, text="", anchor="w", font=("Arial", 12))
        self.notification_label.pack(fill="x", padx=10, pady=(0,10))

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
        self.log_text.see("end")
        self.log_text.config(state="disabled")
