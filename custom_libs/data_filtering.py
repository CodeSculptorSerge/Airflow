import pandas as pd
import re


def filter_serial_numbers(df):
    """
    Фильтрация DataFrame по критериям: только записи категории "POS-терминалы" и
    серийные номера, состоящие исключительно из цифр.
    """
    # Применяем фильтры к DataFrame
    filtered_df = df[
        (df["Категория"] == "POS-терминалы") &  # Фильтрация по категории

        # Фильтрация по формату серийного номера
        (df["Серийный номер"].astype(str).str.match(r"^\d+$"))
    ]
    return filtered_df