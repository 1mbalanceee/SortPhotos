import os
import shutil
import pandas as pd
from tkinter import Tk, filedialog, simpledialog, messagebox, Button, Checkbutton, BooleanVar

def process_photos(excel_file, input_folder, output_folder, with_backup):
    # Создаем папки для поз и чисел
    output_folder_pose = os.path.join(output_folder, "позы")
    output_folder_number = os.path.join(output_folder, "число")

    os.makedirs(output_folder_pose, exist_ok=True)
    os.makedirs(output_folder_number, exist_ok=True)

    # Читаем Excel
    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()

    # Перебор строк в таблице
    for index, row in df.iterrows():
        # Проверка на пустые значения
        if pd.isna(row['позы']) or pd.isna(row['число']):
            continue  # Пропуск пустых строк

        # Преобразуем значения в целые числа
        try:
            pose = int(row['позы'])
            number = int(row['число'])
        except ValueError:
            print(f"Ошибка преобразования значений на строке {index}: поза = {row['позы']}, число = {row['число']}")
            continue  # Если преобразовать не удалось, пропускаем эту строку

        print(f'Обрабатываем: поза = {pose}, число = {number}')

        # Путь к фото для позы и числа
        pose_photo = f"н ({pose}).JPG"
        number_photo = f"н ({number}).JPG"

        # Проверка наличия фотографий
        pose_photo_path = os.path.join(input_folder, pose_photo)
        number_photo_path = os.path.join(input_folder, number_photo)

        if os.path.exists(pose_photo_path):
            print(f'Фото для позы {pose} найдено')
            # Перемещение или копирование фото для позы
            if with_backup:
                shutil.move(pose_photo_path, os.path.join(output_folder_pose, pose_photo))
            else:
                shutil.copy(pose_photo_path, os.path.join(output_folder_pose, pose_photo))
        else:
            print(f'⚠ Фото для позы {pose} не найдено')

        if os.path.exists(number_photo_path):
            print(f'Фото для числа {number} найдено')
            # Перемещение или копирование фото для числа
            if with_backup:
                shutil.move(number_photo_path, os.path.join(output_folder_number, number_photo))
            else:
                shutil.copy(number_photo_path, os.path.join(output_folder_number, number_photo))
        else:
            print(f'⚠ Фото для числа {number} не найдено')

    print("Сортировка завершена!")

def select_file():
    return filedialog.askopenfilename(title="Выберите файл Excel", filetypes=[("Excel Files", "*.xlsx")])

def select_folder(title):
    return filedialog.askdirectory(title=title)

def create_new_folder():
    folder_name = simpledialog.askstring("Введите название папки", "Введите название новой папки:")
    if folder_name:
        project_folder = os.getcwd()
        new_folder_path = os.path.join(project_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)
        return new_folder_path
    return None

def start_gui():
    # Создаем графическое окно
    root = Tk()
    root.withdraw()  # Скрыть основное окно

    # Выбор файла Excel
    excel_file = select_file()
    if not excel_file:
        messagebox.showerror("Ошибка", "Файл Excel не выбран.")
        return

    # Выбор исходной папки
    input_folder = select_folder("Выберите исходную папку с фотографиями")
    if not input_folder:
        messagebox.showerror("Ошибка", "Исходная папка не выбрана.")
        return

    # Создание новой папки
    output_folder = create_new_folder()
    if not output_folder:
        messagebox.showerror("Ошибка", "Не удалось создать папку.")
        return

    # Выбор режима с запасными фото
    with_backup_var = BooleanVar(value=False)
    with_backup = Checkbutton(root, text="Режим с запасными фото (перемещать фото)", variable=with_backup_var)
    with_backup.pack()

    # Кнопка запуска
    def on_start_button_click():
        process_photos(excel_file, input_folder, output_folder, with_backup_var.get())
        messagebox.showinfo("Готово", "Сортировка завершена!")

    start_button = Button(root, text="Начать сортировку", command=on_start_button_click)
    start_button.pack()

    root.deiconify()  # Показываем окно
    root.mainloop()

if __name__ == "__main__":
    start_gui()
