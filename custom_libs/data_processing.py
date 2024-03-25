import pandas as pd


def prepare_serial_numbers(df):
    """
    Подготовка исходного DataFrame путем добавления и форматирования
    столбцов для дальнейшей работы.
    """
    # Создаем копию DataFrame для безопасной работы с данными
    df_prepared = df.copy()
    # Форматируем серийные номера как строки и сохраняем в "Чистый С/Н"
    df_prepared["Чистый С/Н"] = df_prepared["Серийный номер"].astype(str)
    # Создаем пустой столбец "Извлечённый С/Н" для будущих результатов
    df_prepared["Извлечённый С/Н"] = ''
    return df_prepared

def combine_dataframes(df1, df2):
    """
    Объединение двух DataFrame в один с переиндексацией.
    """
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df