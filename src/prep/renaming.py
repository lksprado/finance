# RENAMING SHEET NAMES

import os
import warnings

import openpyxl
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def list_files(file_path: str) -> list:
    files = []
    for file in os.listdir(file_path):
        full_path = os.path.join(file_path, file)
        files.append(full_path)
        files.sort()
    return files


def rename_sheets(file: str, sheet_mapping: dict) -> None:
    workbook = openpyxl.load_workbook(file)

    for sheet_name in workbook.sheetnames:
        if sheet_name in sheet_mapping:
            workbook[sheet_name].title = sheet_mapping[sheet_name]

    workbook.save(file)


if __name__ == "__main__":
    path = "/media/lucas/Files/2.Projetos/0.mylake/bronze/investments"

    sheet_mapping = {
        "Posição - Ações": "ACOES",
        "Posição - ETF": "ETF",
        "Posição - Fundos": "FUNDOS",
        "Posição - Renda Fixa": "RENDA FIXA",
        "Posição - Tesouro Direto": "TESOURO DIRETO",
        "Proventos Recebidos": "PROVENTOS",
        "Negociações": "NEGOCIACOES",
        "Acoes": "ACOES",
        "Renda Fixa": "RENDA FIXA",
        "Tesouro Direto": "TESOURO DIRETO",
        "ACOES1": "ACOES",
        "RENDA FIXA1": "RENDA FIXA",
        "TESOURO DIRETO1": "TESOURO DIRETO",
        "Fundo de Investimento": "FUNDOS"
    }

    files = list_files(path)

    for file in files:
        rename_sheets(file, sheet_mapping)
