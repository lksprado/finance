# THIS SCRIPT IS ABOUT TO LISTING SHEET NAMES IN A FOLDER

import os
import warnings

import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


# LIST ALL FILES
def list_files(file_path: str) -> list:
    files = []
    for file in os.listdir(file_path):
        full_path = os.path.join(file_path, file)
        files.append(full_path)
        files.sort()
    return files


# LIST SHEET NAMES
def list_sheets(fs: list) -> dict:
    sheets = {}
    for file in fs:
        df_sheets = pd.read_excel(file, sheet_name=None, engine="openpyxl")
        sheets[file] = list(df_sheets.keys())
    return sheets


# SEE SHEET NAMES
if __name__ == "__main__":
    path = "/media/lucas/Files/2.Projetos/0.mylake/bronze/investments"

    files = list_files(path)

    sheet_names = list_sheets(files)
    for file, sheets in sheet_names.items():
        print(f"{file}: {', '.join(sheets)}")
