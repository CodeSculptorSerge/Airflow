import pandas as pd
import re


def preprocess_dataframes(exported_df, found_df):
    # Преобразование серийных номеров из обеих таблиц в строки
    exported_df["Serial_Number"] = exported_df["Серийный номер"].astype(str)
    found_df["Clean_SN"] = found_df["Чистый С/Н"].astype(str)
    return exported_df, found_df

def perform_matching(exported_df, found_df):
    # Вызов функций для шагов согласования
    exported_df = match_step1(exported_df, found_df)
    found_df["Normalize_SN1"] = found_df["Clean_SN"].apply(normalize_without_ct)
    exported_df = match_step2(exported_df, found_df)
    found_df["Normalize_SN2"] = found_df["Clean_SN"].apply(remove_last_digit)
    exported_df = match_step3(exported_df, found_df)
    exported_df = match_step4(exported_df, found_df)
    return exported_df

def match_step1(df, found_df):
    # Поиск соответствия по полному совпадению серийного номера без учета регистра
    df["Matched_Step1"] = df["Serial_Number"].apply(
        lambda sn: found_df[
            found_df["Clean_SN"].str.lower() == sn.lower()
        ]["Clean_SN"].values[0]
        if not found_df[
            found_df["Clean_SN"].str.lower() == sn.lower()
        ].empty else None)
    return df

def match_step2(df, found_df):
    # Нормализация серийных номеров (без "CT") и их сравнение
    df["Normalize_SN1"] = df.apply(
        lambda row: None if row["Matched_Step1"] else 
            normalize_without_ct(row["Serial_Number"]), axis=1)
    df["Matched_Step2"] = df["Normalize_SN1"].apply(
        lambda sn: found_df[
            found_df["Normalize_SN1"] == sn
        ]["Clean_SN"].values[0]
        if sn and not found_df[
            found_df["Normalize_SN1"] == sn
        ].empty else None)
    return df

def match_step3(df, found_df):
    # Сравнение серийных номеров после удаления последней цифры
    df["Matched_Step3"] = df.apply(
        lambda row: None if row["Matched_Step1"] or row["Matched_Step2"] else
            found_df[
                found_df["Normalize_SN2"] == row["Serial_Number"]
            ]["Clean_SN"].values[0]
            if not found_df[
                found_df["Normalize_SN2"] == row["Serial_Number"]
            ].empty else None, axis=1)
    return df

def match_step4(df, found_df):
    # Взаимное сравнение серийных номеров после удаления последней цифры из обоих
    df["Normalize_SN3"] = df["Serial_Number"].apply(remove_last_digit)
    df["Matched_Step4"] = df.apply(
        lambda row: None if any(
            row[step] for step in [
                "Matched_Step1", "Matched_Step2", "Matched_Step3"
            ]) else
            found_df[
                found_df["Clean_SN"] == row["Normalize_SN3"]
            ]["Clean_SN"].values[0]
            if not found_df[
                found_df["Clean_SN"] == row["Normalize_SN3"]
            ].empty else None, axis=1)
    return df

def finalize_dataframes(df):
    # Вывод результатов сравнения и удаление ненужных столбцов
    df["Результат сравнения"] = df.apply(
        lambda row: "s/n присутствует в первой выгрузке"
        if any(
            pd.notnull(row[step]) for step in [
                "Matched_Step1", "Matched_Step2",
                "Matched_Step3", "Matched_Step4"
            ]) else "s/n отсутствует или не найден в первой выгрузке", axis=1)    
    return df

def remove_last_digit(serial):
    # Удаление последней цифры из серийного номера
    return serial[:-1] if serial and serial[-1].isdigit() else serial

def normalize_without_ct(serial):
    # Удаление префикса "CT" для нормализации серийного номера
    return re.sub(r".*CT", '', serial, flags=re.IGNORECASE)
