import tkinter as tk
from tkinter import messagebox
import random
import string
import logging
from datetime import datetime


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор надёжных паролей")
        self.root.geometry("600x530")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f4")

        logging.info("Программа запущена")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="Генератор надёжных паролей",
            font=("Arial", 18, "bold"),
            bg="#f4f4f4",
            fg="#222222"
        )
        title_label.pack(pady=15)

        length_frame = tk.Frame(self.root, bg="#f4f4f4")
        length_frame.pack(pady=10)

        length_label = tk.Label(
            length_frame,
            text="Длина пароля (от 4 до 32):",
            font=("Arial", 12),
            bg="#f4f4f4"
        )
        length_label.pack(side=tk.LEFT, padx=5)

        vcmd = (self.root.register(self.validate_length_input), "%P")
        self.length_entry = tk.Entry(
            length_frame,
            font=("Arial", 12),
            width=10,
            validate="key",
            validatecommand=vcmd
        )
        self.length_entry.pack(side=tk.LEFT, padx=5)

        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)

        options_frame = tk.LabelFrame(
            self.root,
            text="Выберите типы символов",
            font=("Arial", 12, "bold"),
            bg="#f4f4f4",
            padx=10,
            pady=10
        )
        options_frame.pack(pady=15, fill="x", padx=40)

        tk.Checkbutton(
            options_frame,
            text="Строчные буквы (a-z)",
            variable=self.lower_var,
            font=("Arial", 11),
            bg="#f4f4f4"
        ).pack(anchor="w", pady=3)

        tk.Checkbutton(
            options_frame,
            text="Заглавные буквы (A-Z)",
            variable=self.upper_var,
            font=("Arial", 11),
            bg="#f4f4f4"
        ).pack(anchor="w", pady=3)

        tk.Checkbutton(
            options_frame,
            text="Цифры (0-9)",
            variable=self.digits_var,
            font=("Arial", 11),
            bg="#f4f4f4"
        ).pack(anchor="w", pady=3)

        tk.Checkbutton(
            options_frame,
            text="Специальные символы (!@#...)",
            variable=self.symbols_var,
            font=("Arial", 11),
            bg="#f4f4f4"
        ).pack(anchor="w", pady=3)

        buttons_frame = tk.Frame(self.root, bg="#f4f4f4")
        buttons_frame.pack(pady=15)

        generate_button = tk.Button(
            buttons_frame,
            text="Сгенерировать",
            font=("Arial", 11, "bold"),
            width=16,
            bg="#4CAF50",
            fg="white",
            command=self.generate_password
        )
        generate_button.grid(row=0, column=0, padx=5, pady=5)

        check_button = tk.Button(
            buttons_frame,
            text="Проверить надёжность",
            font=("Arial", 11, "bold"),
            width=18,
            bg="#2196F3",
            fg="white",
            command=self.check_strength
        )
        check_button.grid(row=0, column=1, padx=5, pady=5)

        save_button = tk.Button(
            buttons_frame,
            text="Сохранить",
            font=("Arial", 11, "bold"),
            width=16,
            bg="#FF9800",
            fg="white",
            command=self.save_password
        )
        save_button.grid(row=1, column=0, padx=5, pady=5)

        clear_button = tk.Button(
            buttons_frame,
            text="Очистить",
            font=("Arial", 11, "bold"),
            width=18,
            bg="#f44336",
            fg="white",
            command=self.clear_fields
        )
        clear_button.grid(row=1, column=1, padx=5, pady=5)

        result_label = tk.Label(
            self.root,
            text="Сгенерированный пароль:",
            font=("Arial", 12, "bold"),
            bg="#f4f4f4"
        )
        result_label.pack(pady=(10, 5))

        self.result_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            width=35,
            justify="center",
            cursor="hand2"
        )
        self.result_entry.pack(pady=5)
        self.result_entry.bind("<Button-1>", self.copy_password_on_click)

        self.copy_hint_label = tk.Label(
            self.root,
            text="Нажмите на пароль, чтобы скопировать",
            font=("Arial", 10),
            bg="#f4f4f4",
            fg="#666666"
        )
        self.copy_hint_label.pack()

        self.strength_label = tk.Label(
            self.root,
            text="Надёжность: -",
            font=("Arial", 12, "bold"),
            bg="#f4f4f4",
            fg="#333333"
        )
        self.strength_label.pack(pady=10)

        bottom_frame = tk.Frame(self.root, bg="#f4f4f4")
        bottom_frame.pack(pady=15)

        about_button = tk.Button(
            bottom_frame,
            text="О программе",
            font=("Arial", 11),
            width=15,
            command=self.open_about_window
        )
        about_button.grid(row=0, column=0, padx=10)

        history_button = tk.Button(
            bottom_frame,
            text="История",
            font=("Arial", 11),
            width=15,
            command=self.open_history_window
        )
        history_button.grid(row=0, column=1, padx=10)

    def validate_length_input(self, new_value):
        if new_value == "":
            return True
        return new_value.isdigit()

    def generate_password(self):
        length_text = self.length_entry.get().strip()

        if not length_text:
            messagebox.showerror("Ошибка", "Введите длину пароля.")
            logging.warning("Пользователь не ввёл длину пароля")
            return

        length = int(length_text)

        if length < 4 or length > 32:
            messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 32.")
            logging.warning("Введена недопустимая длина пароля: %s", length)
            return

        characters = ""
        password_symbols = []

        if self.lower_var.get():
            characters += string.ascii_lowercase
            password_symbols.append(random.choice(string.ascii_lowercase))

        if self.upper_var.get():
            characters += string.ascii_uppercase
            password_symbols.append(random.choice(string.ascii_uppercase))

        if self.digits_var.get():
            characters += string.digits
            password_symbols.append(random.choice(string.digits))

        if self.symbols_var.get():
            characters += string.punctuation
            password_symbols.append(random.choice(string.punctuation))

        if not characters:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
            logging.warning("Пользователь не выбрал ни одного типа символов")
            return

        while len(password_symbols) < length:
            password_symbols.append(random.choice(characters))

        random.shuffle(password_symbols)
        password = "".join(password_symbols)

        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)

        logging.info("Пароль успешно сгенерирован")
        self.copy_hint_label.config(
            text="Нажмите на пароль, чтобы скопировать",
            fg="#666666"
        )

        self.check_strength()

    def check_strength(self):
        password = self.result_entry.get().strip()

        if not password:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте пароль.")
            logging.warning("Попытка проверить пустой пароль")
            return

        score = 0

        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if any(char.islower() for char in password):
            score += 1
        if any(char.isupper() for char in password):
            score += 1
        if any(char.isdigit() for char in password):
            score += 1
        if any(char in string.punctuation for char in password):
            score += 1

        if score <= 2:
            strength_text = "Надёжность: слабый"
            strength_color = "red"
        elif score <= 4:
            strength_text = "Надёжность: средний"
            strength_color = "orange"
        else:
            strength_text = "Надёжность: сильный"
            strength_color = "green"

        self.strength_label.config(text=strength_text, fg=strength_color)
        logging.info("Проверена надёжность пароля: %s", strength_text)

    def copy_password_on_click(self, event=None):
        password = self.result_entry.get().strip()

        if not password:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        self.copy_hint_label.config(
            text="Пароль скопирован в буфер обмена",
            fg="green"
        )
        logging.info("Пароль скопирован в буфер обмена")

    def save_password(self):
        password = self.result_entry.get().strip()

        if not password:
            messagebox.showerror("Ошибка", "Нет пароля для сохранения.")
            logging.warning("Попытка сохранить пустой пароль")
            return

        try:
            with open("saved_passwords.txt", "a", encoding="utf-8") as file:
                file.write(f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')} - {password}\n")

            messagebox.showinfo("Успех", "Пароль сохранён в saved_passwords.txt")
            logging.info("Пароль сохранён в файл")
        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось сохранить пароль:\n{error}")
            logging.error("Ошибка при сохранении пароля: %s", error)

    def clear_fields(self):
        self.length_entry.delete(0, tk.END)
        self.result_entry.delete(0, tk.END)
        self.strength_label.config(text="Надёжность: -", fg="#333333")
        self.copy_hint_label.config(
            text="Нажмите на пароль, чтобы скопировать",
            fg="#666666"
        )
        logging.info("Поля очищены")

    def open_about_window(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("420x260")
        about_window.resizable(False, False)
        about_window.configure(bg="#f4f4f4")

        text = (
            "Генератор надёжных паролей\n\n"
            "Программа предназначена для создания\n"
            "сложных и безопасных паролей.\n\n"
            "Возможности программы:\n"
            "- генерация паролей\n"
            "- проверка надёжности\n"
            "- сохранение в файл\n"
            "- копирование в буфер обмена\n"
            "- ведение логов\n\n"
            "Разработано на Python + Tkinter"
        )

        label = tk.Label(
            about_window,
            text=text,
            font=("Arial", 11),
            bg="#f4f4f4",
            justify="left"
        )
        label.pack(padx=20, pady=20)

        logging.info("Открыто окно 'О программе'")

    def open_history_window(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("История сохранённых паролей")
        history_window.geometry("500x350")
        history_window.resizable(False, False)
        history_window.configure(bg="#f4f4f4")

        text_area = tk.Text(history_window, font=("Arial", 11), width=55, height=18)
        text_area.pack(padx=15, pady=15)

        try:
            with open("saved_passwords.txt", "r", encoding="utf-8") as file:
                content = file.read()

            if content.strip():
                text_area.insert(tk.END, content)
            else:
                text_area.insert(tk.END, "История пока пуста.")
        except FileNotFoundError:
            text_area.insert(tk.END, "Файл с сохранёнными паролями ещё не создан.")
        except Exception as error:
            text_area.insert(tk.END, f"Ошибка при открытии истории:\n{error}")

        text_area.config(state="disabled")
        logging.info("Открыто окно 'История'")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()