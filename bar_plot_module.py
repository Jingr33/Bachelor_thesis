import sys
import os
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import openpyxl
import xlwings as xw
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

if __name__ == "__main__":
    SOURCE_PATH = sys.argv[1]
    PARAMETER_NAME = sys.argv[2]
    XNAME = sys.argv[3]
    XSCALE = sys.argv[4]
    TITLE_PARAMETER_NAME = sys.argv[5]

    workbook = openpyxl.load_workbook(os.path.join(SOURCE_PATH, "overview.xlsx"), data_only=True, keep_vba=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    model_names = [rows[0][i] for i in range(1, len(rows[0]), 2)]
    
    for i in range(len(model_names)):
        model_names[i] = model_names[i].split('_')[-1]

    ########################
    # model_names = [model_names[2], model_names[3], model_names[1], model_names[0], model_names[4]]
    #######################xx

    last_row = []
    with xw.App(visible=False) as app:
        wb = app.books.open(os.path.join(SOURCE_PATH, "overview.xlsx"))
        sheet = wb.sheets[0]

        last_row_idx = sheet.used_range.last_cell.row
        last_row = sheet.range(f"{last_row_idx}:{last_row_idx}").value  

        wb.close()

    map50s = [last_row[i] for i in range(1, len(last_row), 2) if last_row[i] is not None]
    map5095s = [last_row[j] for j in range(2, len(last_row), 2) if last_row[j] is not None]
    
    #################xx
    # map50s = [map50s[2], map50s[3], map50s[1], map50s[0], map50s[4]]
    # map5095s = [map5095s[2], map5095s[3], map5095s[1], map5095s[0], map5095s[4]]
    ###################


    x = np.arange(len(model_names))  # pozice na ose X
    width = 0.25  # šířka sloupců

    fig, ax = plt.subplots(figsize=(9, 3))
    bars1 = ax.bar(x - width/2, map50s, width, label='mAP50', color='#1f77b4')
    bars2 = ax.bar(x + width/2, map5095s, width, label='mAP50:95', color='#d62728')

    # Přidání popisků a titulků
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.2f}".replace('.', ',')))
    ax.set_ylabel('Hodnota metriky')
    ax.set_xlabel('modelu YOLO11m')
    ax.set_title('Výsledky tréninku finálního modelu metodou křížové validace')
    ax.set_xticks(x)
    ax.set_xticklabels(model_names)
    ax.legend(loc = "lower center", framealpha=1)

    # Desetinné čárky v popiscích hodnot na sloupcích
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}'.replace('.', ','),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # výška popisku nad sloupcem
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}'.replace('.', ','),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(4, 3),  # výška popisku nad sloupcem
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)


    # Styl
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    
    plt.savefig(os.path.join(SOURCE_PATH, "overview_plot.png"))  # uloží obrázek jako PNG
    plt.close()
    print('Scatter plot created!')   