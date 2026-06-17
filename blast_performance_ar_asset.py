import os
import pyautogui
from datetime import datetime, timedelta
from general_task import *
from pynput.keyboard import Controller
from services.capslock_checker import capslock_checking
from services.chrome_checker import open_outlook
from remover.remover_performance_ar_asset import clear_submission_folder
from services.config import get_month_id, load_config, logger, wait_timer
from services.duration_counter import (
    get_execution_duration,
    start_counter,
    stop_counter,
)
from mail.outlook_penerimaan_denda_aktif import send_outlook_email
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

pyautogui.FAILSAFE = False
CONFIG = load_config()
keyboard = Controller()


def excel_config():
    logger.info("[SYSTEM] SUMMARY PERFORMANCE AR REPORT EXCEL WORKFLOW")

    # ── OPEN & NAVIGATE ───────────────────────────────────────────────────────
    os.startfile(CONFIG["WORKSOURCE_PERFORMANCE_AR_ASSET"])
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])
    maximize_app_window()
    logger.info("[EXCEL] NAVIGATE TO TARGET SHEET")
    for _ in range(3):
        switch_to_first_sheet()
    for _ in range(14):
        switch_to_right_sheet()

    # ── REFRESH DATA ──────────────────────────────────────────────────────────
    logger.info("[EXCEL] REFRESH EXCEL PROCESS")
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["THREEHALF_MINUTE"])
    handle_refresh_process()
    wait_timer(CONFIG["WAIT_TIME"]["THREEHALF_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    # ── COPY SHEET TO NEW WORKBOOK ────────────────────────────────────────────
    logger.info("[EXCEL] MOVE AND COPY WORKBOOK")
    for _ in range(3):
        select_sheet_down()

    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["FOUR_MINUTE"])
    handle_move_copy_process()
    wait_timer(CONFIG["WAIT_TIME"]["FOUR_MINUTE"])
    handle_move_copy_process()
    move_cursor_figure_eight()

    logger.info("[EXCEL] NAVIGATE IN NEW WORKBOOK")
    switch_to_right_sheet()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    switch_to_first_cells()
    move_cell_horizontal()
    switch_to_first_sheet()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── BREAK EXTERNAL LINKS ──────────────────────────────────────────────────
    logger.info("[EXCEL] BREAK EXTERNAL LINKS")
    move_cursor_figure_eight()
    break_excel_link()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    handle_breaklink_process()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    handle_breaklink_process()
    move_cursor_figure_eight()
    escaping()

    # ── NAVIGATE TO SUMMARY SHEET ─────────────────────────────────────────────
    for _ in range(2):
        switch_to_right_sheet()
    for _ in range(5):
        switch_to_left_sheet()

    # ── CAPTURE TABLE AS PICTURE ──────────────────────────────────────────────
    logger.info("[EXCEL] CAPTURE TABLE AS PICTURE")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ── SAVE NEW WORKBOOK ─────────────────────────────────────────────────────
    logger.info("[EXCEL] SAVE NEW WORKBOOK")
    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_PERFORMANCE"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    today = datetime.now() - timedelta(days=1)
    performance_day = today.strftime("%d")
    month_idn_title = get_month_id(today.strftime("%B"), case="title")
    performance_filename = f"Summary Performance AR, Remedial & Asset As Of {performance_day} {month_idn_title}"
    pyautogui.write(performance_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    # ── CLOSE WORKBOOKS ───────────────────────────────────────────────────────
    move_cursor_figure_eight()
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    logger.info("[EXCEL] CLOSE WORKSOURCE FILE")
    switch_to_first_sheet()
    switch_to_first_cells()
    close_unsave()


def send_email():
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]

    today = datetime.now() - timedelta(days=1)
    performance_day = today.strftime("%d")
    performance_year = today.strftime("%Y")
    month_idn_title = get_month_id(today.strftime("%B"), case="title")

    subject_email = (
        f"Summary Performance AR, Remedial & Asset As Of "
        f"{performance_day} {month_idn_title} {performance_year}"
    )

    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Performance AR, Remedial & Asset As Of {performance_day} {month_idn_title} {performance_year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

"""

    footer_template = """

Note : Report Asset Tentative

Hormat kami,
Asset Management Division
Collection HO - PT Suzuki Finance Indonesia
"""

    send_outlook_email(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
    )


if __name__ == "__main__":
    logger.info("[SYSTEM] START SUMMARY PERFORMANCE AR REPORT")
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── PRE-FLIGHT CHECKS ─────────────────────────────────────────────────────
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    clear_submission_folder(target_folder=CONFIG["SUB_PERFORMANCE_AR_ASSET"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── PRE-FLIGHT OUTLOOK ────────────────────────────────────────────────────
    open_outlook()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ── EXCEL PROCESSING ──────────────────────────────────────────────────────
    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── EMAIL DISPATCH ────────────────────────────────────────────────────────
    send_email()
    logger.info("[SYSTEM] SUMMARY PERFORMANCE AR REPORT SENT")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── FINALISE ──────────────────────────────────────────────────────────────
    stop_counter()
    execution_time = get_execution_duration()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
