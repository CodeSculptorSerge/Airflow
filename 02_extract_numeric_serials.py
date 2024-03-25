from pathlib import Path

import pandas as pd

from custom_libs.data_filtering import filter_serial_numbers
from custom_libs.excel_utils import dataframe_to_excel


# Определяем абсолютный путь до текущей директории
ROOT = Path(__file__).resolve().parent

input_path = ROOT / "input_data" / "Выгрузка.xlsx"
output_path = ROOT / "output_data" / "02_Извлечённые_без_ct.xlsx"


def main() -> None:
    # Чтение данных
    df = pd.read_excel(input_path)
    
    # Фильтрация данных
    filtered_df = filter_serial_numbers(df)
    
    # Вызов функции сохранения DataFrame в Excel с форматированием
    # Правильный вызов функции с передачей необходимых аргументов
    dataframe_to_excel(filtered_df, output_path)

    print(f"Отфильтрованные данные были сохранены в файл: {output_path}")


if __name__ == '__main__':
    main()
    