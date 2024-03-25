from pathlib import Path

from custom_libs.serial_number_extractor import extract_serial_numbers_in_file
from custom_libs.excel_utils import dataframe_to_excel


# Задаем корневой путь к текущей директории
ROOT = Path(__file__).resolve().parent

# Определяем путь к входным и выходным данным
input_path = ROOT / "input_data" / "Выгрузка.xlsx"
output_path = ROOT / "output_data" / "01_Извлечённые_ct.xlsx"


def main() -> None:
    # Осуществляем чтение файла, извлечение серийных номеров и запись результата в выходной файл
    df_serials_found = extract_serial_numbers_in_file(input_path)
    dataframe_to_excel(df_serials_found, output_path)
    
    print(f"Серийные номера успешно извлечены и сохранены в файл: {output_path}")


if __name__ == '__main__':
    main()