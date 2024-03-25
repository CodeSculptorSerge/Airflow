import re
import pandas as pd


# Регулярные выражения для выделения серийных номеров
serial_number_pattern = re.compile(r"(s/n|sn|с/н|сн)\s?\d*ct\d+", re.IGNORECASE)
prefix_pattern = re.compile(r"^(s/n|sn|с/н|сн)\s*", re.IGNORECASE)

def extract_single_serial_number(input_string):
    """
    Извлекает единичный серийный номер из строки, если таковой присутствует.
    """
    # Поиск совпадения в строке с использованием регулярного выражения
    match = serial_number_pattern.search(input_string)
    if match:
        return match.group(0)
    return None

def extract_serial_numbers_in_file(filepath):
    """
    Чтение данных из Excel файла, фильтрация по категории и
    извлечение серийных номеров.
    """
    # Чтение файла с использованием предоставленной функции
    df = pd.read_excel(filepath)
    
    # Фильтрация данных по категории "POS-терминалы"
    df_POS = df[df["Категория"] == "POS-терминалы"].copy()

    # Применение функции извлечения серийных номеров к каждой строке
    df_POS.loc[:, "Извлечённый С/Н"] = df_POS.apply(
        lambda row: extract_single_serial_number(str(row['Название']))
        or extract_single_serial_number(str(row["Серийный номер"])),
        axis=1
    )

    # Удаление строк, где серийный номер не был извлечен (столбец NaN)
    df_serials = df_POS.dropna(subset=["Извлечённый С/Н"]).copy()

    # Очистка серийных номеров от префиксов и лишних пробелов
    df_serials.loc[:, "Чистый С/Н"] = df_serials["Извлечённый С/Н"].apply(
        lambda x: prefix_pattern.sub('', x).strip()
    )

    return df_serials
