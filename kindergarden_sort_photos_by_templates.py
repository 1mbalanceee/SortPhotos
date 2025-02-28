import os
import shutil
import pandas as pd

def process_frames(table_path, source_folder, target_folder):
    df = pd.read_csv(table_path, delimiter=',', encoding='windows-1251')  # Читаем таблицу CSV

    for index, row in df.iterrows():
        group = str(row['Группа'])  # Получаем номер группы
        plot = str(row['Сюжет'])
        dimension = str(row['Размерность']).replace('к', 'Комплект').replace('маг', 'Магнит')  # Обработка "к"
        extra_conditions = row.get('Доп условий', '')

        # Формируем пути
        group_path = os.path.join(target_folder, group)  # Папка группы
        plot_path = os.path.join(group_path, plot)  # Папка сюжета внутри группы
        dimension_path = os.path.join(plot_path, dimension)  # Папка размерности внутри сюжета

        # Создаем папки, если их нет
        os.makedirs(dimension_path, exist_ok=True)

        # Формируем имя файла
        photo_number = str(index + 1)  # Номер строки как номер фото
        original_photo_name = f"н ({photo_number}).jpg"
        source_file = os.path.join(source_folder, original_photo_name)

        if pd.notna(extra_conditions) and extra_conditions.strip():
            new_photo_name = f"н({photo_number})+{extra_conditions.strip()}.jpg"
            target_file = os.path.join(dimension_path, new_photo_name)
        else:
            target_file = os.path.join(dimension_path, original_photo_name)

        # Перемещаем файл
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
        else:
            print(f"Файл {source_file} не найден")

# Использование
process_frames("students.csv", "C:\\Users\\PC\\Desktop\\input_photos", "sorted_frames")
