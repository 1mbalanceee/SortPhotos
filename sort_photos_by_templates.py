import os
import shutil
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


class PhotoSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Sorter")
        self.root.geometry("600x400")

        self.csv_file = None
        self.photo_folder = None
        self.base_output_path = "D:\\ШКОЛЫ 2024-2025\\февраль"

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

        # Кнопка выполнения
        self.run_button = tk.Button(root, text="Выполнить", command=self.run_program)
        self.run_button.pack(pady=20)

    def select_csv(self):
        self.csv_file = filedialog.askopenfilename(title="Выберите файл CSV", filetypes=[("CSV files", "*.csv")])
        if self.csv_file:
            self.csv_label.config(text=f"Выбран файл: {os.path.basename(self.csv_file)}")

    def select_photo_folder(self):
        self.photo_folder = filedialog.askdirectory(title="Выберите папку с фотографиями", initialdir=self.base_output_path)
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

            folder_name = self.output_entry.get().strip()
            if not folder_name:
                messagebox.showerror("Ошибка", "Вы не ввели название выходной папки!")
                return

            output_folder = os.path.join(self.base_output_path, folder_name)
            os.makedirs(output_folder, exist_ok=True)

            process_frames(self.csv_file, self.photo_folder, output_folder)

            messagebox.showinfo("Успех", f"Фотографии успешно распределены в папке: {output_folder}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


def process_frames(table_path, source_folder, target_folder):
    df = pd.read_csv(table_path, delimiter=',', encoding='windows-1251')

    for index, row in df.iterrows():
        plot = str(row['Сюжет'])
        dimension = str(row['Размерность']).replace('к', 'Комплект').replace('маг', 'Магнит')
        extra_conditions = row.get('Доп условий', '')

        plot_path = os.path.join(target_folder, plot)
        dimension_path = os.path.join(plot_path, dimension)

        os.makedirs(dimension_path, exist_ok=True)

        photo_number = str(index + 1)
        original_photo_name = f"н ({photo_number}).jpg"
        source_file = os.path.join(source_folder, original_photo_name)

        if pd.notna(extra_conditions) and extra_conditions.strip():
            new_photo_name = f"н({photo_number})+{extra_conditions.strip()}.jpg"
            target_file = os.path.join(dimension_path, new_photo_name)
        else:
            target_file = os.path.join(dimension_path, original_photo_name)

        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
        else:
            print(f"Файл {source_file} не найден")


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoSorterApp(root)
    root.mainloop()
