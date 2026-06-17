from __future__ import annotations
import os
import pyautogui
from enum import IntEnum
from general_task import (
    capture_table_as_bitmap,
    close_unsave,
    maximize_app_window,
    switch_to_first_cells,
    switch_to_first_sheet,
    switch_to_right_sheet,
    switch_to_table_cells,
    refresh_excel_data,
    handle_refresh_process,
    save_file,
    closing_tab,
)
from services.config import load_config, logger, wait_timer

CONFIG = load_config()


class LorSheet(IntEnum):
    AREA = 0
    AS_OF = 1
    TODAY = 2


def refresh_workbook() -> None:
    os.startfile(CONFIG["WORKSOURCE_MOBCOLL_LOR"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()
    logger.info("[EXCEL] REFRESH EXCEL PROCESS")
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def open_workbook() -> None:
    os.startfile(CONFIG["WORKSOURCE_MOBCOLL_LOR"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()
    for _ in range(2):
        switch_to_right_sheet()
    switch_to_first_cells()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def navigate_to_sheet(sheet: LorSheet) -> None:
    for _ in range(int(sheet)):
        switch_to_right_sheet()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def finalizing() -> None:
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_bitmap()
    switch_to_first_cells()
    switch_to_first_sheet()
    switch_to_first_cells()
    close_unsave()


def take_summary_picture(sheet: LorSheet) -> None:
    logger.info(f"[LOR] CAPTURING SHEET: {sheet.name}")
    open_workbook()
    navigate_to_sheet(sheet)
    finalizing()
    logger.info(f"[LOR] SHEET {sheet.name} CAPTURE COMPLETE")
