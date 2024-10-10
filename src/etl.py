import os
import warnings

import openpyxl
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 50)


def list_files(file_path: str) -> list:
    files = []
    for file in os.listdir(file_path):
        full_path = os.path.join(file_path, file)
        files.append(full_path)
        files.sort()
    return files


def make_df(files: list, sheet: str) -> pd.DataFrame:
    all_dataframes = []

    months = {
        "janeiro": "1",
        "fevereiro": "2",
        "marco": "3",
        "abril": "4",
        "maio": "5",
        "junho": "6",
        "julho": "7",
        "agosto": "8",
        "setembro": "9",
        "outubro": "10",
        "novembro": "11",
        "dezembro": "12",
    }

    for file in files:
        try:
            df = pd.read_excel(file, sheet_name=sheet, engine="openpyxl")
            df["ATIVO"] = sheet
            df["FILENAME"] = os.path.basename(file)
            filename = os.path.basename(file)
            date_part = "-".join(filename.split("-")[3:5])
            date_part = date_part.replace(".xlsx", "")
            year = date_part.split("-")[0]
            month = date_part.split("-")[1]
            month_number = months.get(month)
            formated_date = f"{month_number}-{year}"
            df["DATE"] = formated_date
            all_dataframes.append(df)
        except Exception:
            continue

        combined_df = pd.concat(all_dataframes, axis=0, ignore_index=True)
        combined_df.dropna(axis="index", how="all", subset=["Produto"], inplace=True)
        combined_df.columns = [x.upper() for x in df.columns]

    return combined_df


def cleaning(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    new_df = df[df.columns.intersection(cols)]
    new_df = new_df[cols]
    return new_df




if __name__ == "__main__":
    path = "/media/lucas/Files/2.Projetos/0.mylake/bronze/investments"

    sheet_a = "ACOES"
    keep_a = [
        "ATIVO",
        "DATE",
        "CÓDIGO DE NEGOCIAÇÃO",
        "QUANTIDADE",
        "PREÇO DE FECHAMENTO",
        "VALOR ATUALIZADO",
    ]

    sheet_e = "ETF"
    keep_e = [
        "ATIVO",
        "DATE",
        "CÓDIGO DE NEGOCIAÇÃO",
        "QUANTIDADE",
        "PREÇO DE FECHAMENTO",
        "VALOR ATUALIZADO",
    ]

    sheet_f = "FUNDOS"
    keep_f = [
        "ATIVO",
        "DATE",
        "CÓDIGO DE NEGOCIAÇÃO",
        "QUANTIDADE",
        "PREÇO DE FECHAMENTO",
        "VALOR ATUALIZADO",
    ]

    sheet_rf = "RENDA FIXA"
    keep_rf = [
        "ATIVO",
        "DATE",
        "PRODUTO",
        "QUANTIDADE",
        "VALOR ATUALIZADO CURVA",
    ]

    sheet_td = "TESOURO DIRETO"
    keep_td = [
        "ATIVO",
        "DATE",
        "PRODUTO",
        "QUANTIDADE",
        "VALOR BRUTO",
        "VALOR LÍQUIDO",
    ]

    files = list_files(path)

    df_acoes = make_df(files, sheet_a)
    df_acoes_f = cleaning(df_acoes, keep_a)

    df_etf = make_df(files, sheet_e)
    df_etf_f = cleaning(df_etf, keep_e)

    df_f = make_df(files, sheet_f)
    df_f_f = cleaning(df_f, keep_f)

    df_rf = make_df(files, sheet_rf)
    df_rf_f = cleaning(df_rf, keep_rf)

    df_td = make_df(files, sheet_td)
    df_td_f = cleaning(df_td, keep_td)

    df_rv = pd.concat([df_acoes_f, df_etf_f, df_f_f], axis=0, ignore_index=True)

    rv_output_file = "renda_variavel.xlsx"
    df_rv.to_excel(rv_output_file, index=False)
    
    rf_output_file = "renda_fixa.xlsx"
    df_rf_f.to_excel(rf_output_file, index=False)
    
    td_output_file = "tesouro_direto.xlsx"
    df_td_f.to_excel(td_output_file, index=False)
