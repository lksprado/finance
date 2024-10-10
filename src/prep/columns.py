import os
import warnings

import pandas as pd

# Ignore warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


# List all files in the specified directory
def list_files(file_path: str) -> list:
    files = []
    for file in os.listdir(file_path):
        full_path = os.path.join(file_path, file)
        if file.endswith(".xlsx"):  # Ensure only Excel files are considered
            files.append(full_path)
    files.sort()
    return files


# List sheet names and their columns in the Excel files
def list_columns(fs: list) -> dict:
    sheets = {}
    for file in fs:
        df_sheets = pd.read_excel(file, sheet_name=None, engine="openpyxl")
        for sheet_name, df in df_sheets.items():
            sheets[sheet_name] = df.columns.tolist()  # Collect columns for each sheet
    return sheets


# Main execution
if __name__ == "__main__":
    path = "/media/lucas/Files/2.Projetos/0.mylake/bronze/investments"  # Replace with your actual path
    files = list_files(path)
    sheets_info = list_columns(files)

    # Create a DataFrame from the collected sheet information
    sheets_df = pd.DataFrame(
        [
            (sheet_name, ", ".join(columns))
            for sheet_name, columns in sheets_info.items()
        ],
        columns=["Sheet Name", "Columns"],
    )

    # Save the DataFrame to an Excel file
    output_file_path = "sheet_names_info.xlsx"
    sheets_df.to_excel(output_file_path, index=False)
