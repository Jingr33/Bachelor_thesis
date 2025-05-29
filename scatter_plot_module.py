import sys
import os
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import openpyxl
import xlwings as xw
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

if __name__ == "__main__":
    SOURCE_PATH = sys.argv[1]
    PARAMETER_NAME = sys.argv[2]
    XNAME = sys.argv[3]
    XSCALE = sys.argv[4]
    TITLE_PARAMETER_NAME = sys.argv[5]

    workbook = openpyxl.load_workbook(os.path.join(SOURCE_PATH, "overview.xlsx"), data_only=True, keep_vba=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    training_names = [rows[0][i] for i in range(1, len(rows[0]), 2)]

    param_values = []
    for training_name in training_names:
        train_params = training_name.split('_')
        for train_param in train_params:
            if PARAMETER_NAME in str(train_param):
                value = str(train_param).lstrip(PARAMETER_NAME)
                param_values.append(float(value))

    last_row = []
    with xw.App(visible=False) as app:
        wb = app.books.open(os.path.join(SOURCE_PATH, "overview.xlsx"))
        sheet = wb.sheets[0]

        last_row_idx = sheet.used_range.last_cell.row
        last_row = sheet.range(f"{last_row_idx}:{last_row_idx}").value  

        wb.close()

    map50s = [last_row[i] for i in range(1, len(last_row), 2) if last_row[i] is not None]
    map5095s = [last_row[j] for j in range(2, len(last_row), 2) if last_row[j] is not None]

    formatter_x = ticker.FuncFormatter(lambda x, _: f"{x:.0f}".replace('.', ','))
    formatter_y = ticker.FuncFormatter(lambda x, _: f"{x:.2f}".replace('.', ','))
    plt.gca().yaxis.set_major_formatter(formatter_y)
    plt.gca().xaxis.set_major_formatter(formatter_x)

    plt.scatter(param_values, map50s, color='#1f77b4', label='@mAP50')
    plt.scatter(param_values, map5095s, color='#d62728', label='@mAP50:95')

    plt.title(f"Porovnání metrik modelu při různých {TITLE_PARAMETER_NAME}")
    plt.xlabel(XNAME)
    plt.ylabel("@mAP50 / @mAP50:95")
    plt.legend(loc='center left', framealpha=1)
    if XSCALE != "":
        plt.xscale(XSCALE)

    for x, y in zip(param_values, map50s):
        plt.text(x, y - 0.014, f"[{x:.0f}; {y:.2f}]".replace('.', ','), ha='left', color='black', fontsize=8)

    for x, y in zip(param_values, map5095s):
        plt.text(x, y + 0.009, f"[{x:.0f}; {y:.2f}]".replace('.', ','), ha='left', color='black', fontsize=8)

    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.savefig(os.path.join(SOURCE_PATH, f"overview_plot_{PARAMETER_NAME}.png"))  # uloží obrázek jako PNG
    plt.close()
    print('Scatter plot created!')   