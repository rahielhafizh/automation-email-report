import os
import pyautogui
from services.config import load_config, logger, wait_timer
from general_task import (
    capture_table_as_bitmap,
    closing_tab,
    maximize_app_window,
    refresh_excel_data,
    save_file,
    switch_to_first_cells,
    switch_to_first_sheet,
    switch_to_right_sheet,
    switch_to_table_cells,
)

CONFIG = load_config()


def process_alda_workbook() -> None:
    logger.info("[ALDA] EXCEL PROCESSING STARTED")
    os.startfile(CONFIG["WORKSOURCE_PENERIMAAN_DENDA_ALDA"])
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])
    switch_to_first_cells()
    switch_to_right_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_bitmap()
    switch_to_first_cells()
    switch_to_first_sheet()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    logger.info("[ALDA] EXCEL PROCESSING COMPLETE")
