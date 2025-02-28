import csv
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_csv(input_csv, output_csv):
    """
    Преобразует CSV файл из формата с повторяющимися данными и запятыми в формат с уникальными данными и точками с запятой.
    """
    with open(input_csv, newline='', encoding="utf-8") as infile, open(output_csv, "w", newline='', encoding="utf-8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, delimiter=';')

        # Преобразуем заголовки
        headers = next(reader)
        new_headers = headers[:4]  # Берем только первые 4 столбца
        writer.writerow(new_headers)

        for row in reader:
            # Оставляем только первые 4 столбца
            cleaned_row = row[:4]
            # Убираем лишние пробелы
            cleaned_row = [cell.strip() for cell in cleaned_row]
            # Записываем строку в новый файл
            writer.writerow(cleaned_row)

def distribute_photos(photo_folder, csv_file, output_folder):
    if not os.path.exists(photo_folder):
        raise FileNotFoundError(f"Ошибка: Папка {photo_folder} не найдена.")

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Ошибка: Файл {csv_file} не найден.")

    # Этап 1: Преобразование CSV в правильный формат
    cleaned_csv_file = "cleaned_students.csv"
    convert_csv(csv_file, cleaned_csv_file)

    # Этап 2: Сортировка фотографий
    # Создание выходной папки
    os.makedirs(output_folder, exist_ok=True)

    with open(cleaned_csv_file, newline='', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')
        headers = next(reader)  # Пропускаем заголовок

        for row in reader:
            if len(row) < 4:
                print(f"Ошибка в строке: {row}. Пропускаем.")
                continue

            name = row[0]
            numbers = row[1:4]

            student_folder = os.path.join(output_folder, name)
            os.makedirs(student_folder, exist_ok=True)

            categories = ["число", "сидя", "стоя"]
            for category, num in zip(categories, numbers):
                if not num:  # Пропускаем пустые значения
                    continue

                category_folder = os.path.join(student_folder, category)
                os.makedirs(category_folder, exist_ok=True)

                photo_name = f"н ({num}).jpg"
                photo_path = os.path.join(photo_folder, photo_name)

                if os.path.exists(photo_path):
                    shutil.copy(photo_path, os.path.join(category_folder, photo_name))
                else:
                    print(f"Фотография {photo_name} не найдена.")

# Интерфейс
class PhotoSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Sorter")
        self.root.geometry("600x400")

        self.csv_file = None
        self.photo_folder = None

        # Выбор CSV файла
        self.csv_label = tk.Label(root, text="Выберите файл CSV")
        self.csv_label.pack(pady=10)

        self.csv_button = tk.Button(root, text="Выбрать CSV", command=self.select_csv)
        self.csv_button.pack(pady=5)

        # Выбор папки для фотографий
        self.photo_label = tk.Label(root, text="Выберите папку с фотографиями")
        self.photo_label.pack(pady=10)

        self.photo_button = tk.Button(root, text="Выбрать папку", command=self.select_photo_folder)
        self.photo_button.pack(pady=5)

        # Ввод названия выходной папки
        self.output_label = tk.Label(root, text="Введите название для выходной папки")
        self.output_label.pack(pady=10)

        self.output_entry = tk.Entry(root, width=40)
        self.output_entry.pack(pady=5)

        # Кнопка завершения
        self.run_button = tk.Button(root, text="Выполнить", command=self.run_program)
        self.run_button.pack(pady=20)

    def select_csv(self):
        self.csv_file = filedialog.askopenfilename(title="Выберите файл CSV", filetypes=[("CSV files", "*.csv")])
        if self.csv_file:
            self.csv_label.config(text=f"Выбран файл: {os.path.basename(self.csv_file)}")

    def select_photo_folder(self):
        initial_dir = "D:/ШКОЛЫ 2024-2025/февраль"
        self.photo_folder = filedialog.askdirectory(title="Выберите папку с фотографиями", initialdir=initial_dir)
        if self.photo_folder:
            self.photo_label.config(text=f"Выбрана папка: {self.photo_folder}")

    def run_program(self):
        try:
            if not self.csv_file:
                messagebox.showerror("Ошибка", "Вы не выбрали CSV файл!")
                return

            if not self.photo_folder:
                messagebox.showerror("Ошибка", "Вы не выбрали папку с фотографиями!")
                return

            folder_name = self.output_entry.get()
            if not folder_name:
                messagebox.showerror("Ошибка", "Вы не ввели название выходной папки!")
                return

            output_folder = os.path.join(os.path.expanduser("~/Desktop"), folder_name)
            distribute_photos(self.photo_folder, self.csv_file, output_folder)

            messagebox.showinfo("Успех", f"Фотографии успешно распределены в папке: {output_folder}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoSorterApp(root)
    root.mainloop()