from pathlib import Path

import pandas as pd

from custom_libs.data_processing import prepare_serial_numbers, combine_dataframes
from custom_libs.data_filtering import filter_serial_numbers
from custom_libs.serial_number_extractor import extract_serial_numbers_in_file
from custom_libs.excel_utils import dataframe_to_excel


# Настройка путей
file = __file__
ROOT = Path(file).resolve().parent
input_path = ROOT / "input_data/Выгрузка.xlsx"
output_path = ROOT / "output_data/03_Все_найденные.xlsx"

    
def main() -> None:
    # Загрузка данных из Excel файла в DataFrame
    df = pd.read_excel(input_path)

    # Вызов функций обработки данных
    df_ct = extract_serial_numbers_in_file(input_path)
    df_digits = filter_serial_numbers(df)

    # Подготовка данных
    df_digits_prepared = prepare_serial_numbers(df_digits)

    # Объединение DataFrame
    combined_df = combine_dataframes(df_ct, df_digits_prepared)

    # Форматирование и сохранение файла Excel
    dataframe_to_excel(combined_df, output_path)

    print(f"Объединенные данные сохранены в файл: {output_path}")


if __name__ == "__main__":
    main()
