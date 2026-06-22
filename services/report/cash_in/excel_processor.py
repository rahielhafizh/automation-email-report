import os
import pyautogui
from general_task import (
    capture_table_as_bitmap,
    closing_tab,
    maximize_app_window,
    refresh_excel_data,
    save_file,
    scroller_page,
    switch_to_first_cells,
    switch_to_first_sheet,
    switch_to_right_sheet,
    switch_to_table_cells,
    move_cursor_figure_eight,
)
from services.config import load_config, logger, wait_timer

CONFIG = load_config()

_CASH_IN_SHEET_INDEX = 10


def process_cash_in_workbook() -> None:
    logger.info("[CASH IN] EXCEL PROCESSING STARTED")
    os.startfile(CONFIG["WORKSOURCE_PENERIMAAN_CASH_IN"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    move_cursor_figure_eight()
    scroller_page()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])

    switch_to_first_cells()
    for _ in range(_CASH_IN_SHEET_INDEX):
        switch_to_right_sheet()

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_bitmap()
    switch_to_first_cells()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])
    closing_tab()
    logger.info("[CASH IN] EXCEL PROCESSING COMPLETE")
