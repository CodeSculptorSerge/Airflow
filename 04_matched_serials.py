from pathlib import Path

import pandas as pd

from custom_libs.serial_number_utils import (
    preprocess_dataframes, 
    perform_matching,
    finalize_dataframes
)
from custom_libs.excel_utils import dataframe_to_excel


file = __file__
ROOT = Path(file).resolve().parent
output_path = ROOT / "input_data/Вторая_выгрузка.xlsx"
found_path = ROOT / "output_data/03_Все_найденные.xlsx"
result_path = ROOT / 'output_data/04_Результат_обработки.xlsx'


def main():
    # Чтение данных из Excel файлов
    exported_df = pd.read_excel(output_path, engine="openpyxl")
    found_df = pd.read_excel(found_path, engine="openpyxl")

    # Предобработка данных
    exported_df, found_df = preprocess_dataframes(exported_df, found_df)

    # Выполнение сопоставлений
    exported_df = perform_matching(exported_df, found_df)

    # Финализация результатов
    exported_df = finalize_dataframes(exported_df)

    # Добавление DataFrame в Excel с форматированием
    dataframe_to_excel(exported_df, result_path)

    print(f"Результат сохранён в файле: {result_path}")


if __name__ == "__main__":
    main()
