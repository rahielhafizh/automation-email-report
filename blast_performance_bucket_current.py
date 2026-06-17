import os
import pyautogui
from datetime import datetime, timedelta
from general_task import *
from pynput.keyboard import Controller
from screen_keeper import (
    find_screen_keeper_process,
    run_screen_keeper,
    stop_screen_keeper,
)
from services.capslock_checker import capslock_checking
from services.chrome_checker import open_outlook
from remover.remover_performance_bucket_current import clear_submission_folder
from services.config import get_month_id, load_config, logger, wait_timer
from services.duration_counter import get_execution_duration, start_counter, stop_counter
from mail.outlook_performance_bucket_current import send_outlook_email

pyautogui.FAILSAFE = False
CONFIG = load_config()
keyboard = Controller()


def excel_config():
    logger.info("[SYSTEM] SUMMARY PERFORMANCE BUCKET CURRENT WORKFLOW")

    # ── OPEN & NAVIGATE ───────────────────────────────────────────────────────
    os.startfile(CONFIG["WORKSOURCE_PERFORMANCE_BUCKET_CURRENT"])
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])
    maximize_app_window()
    logger.info("[EXCEL] NAVIGATE TO TARGET SHEET")
    switch_to_first_sheet()
    for _ in range(2):
        switch_to_right_sheet()

    # ── REFRESH DATA ──────────────────────────────────────────────────────────
    logger.info("[EXCEL] REFRESH EXCEL PROCESS")
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])
    handle_refresh_process()
    entering_operation()
    switch_to_first_cells()

    # ── COPY SHEET TO NEW WORKBOOK ────────────────────────────────────────────
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])

    logger.info("[EXCEL] NAVIGATE IN NEW WORKBOOK")
    switch_to_right_sheet()
    switch_to_first_cells()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    switch_to_first_sheet()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── BREAK EXTERNAL LINKS ──────────────────────────────────────────────────
    logger.info("[EXCEL] BREAK EXTERNAL LINKS")
    break_excel_link()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])
    handle_breaklink_process()
    move_cursor_figure_eight()
    escaping()

    # ── CAPTURE TABLE AS PICTURE ──────────────────────────────────────────────
    move_cursor_figure_eight()
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ── SAVE NEW WORKBOOK ─────────────────────────────────────────────────────
    logger.info("[EXCEL] SAVE NEW WORKBOOK")
    save_new_book()
    pyautogui.write(CONFIG["SUB_PERFORMANCE_BUCKET_CURRENT"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    today = datetime.now() - timedelta(days=1)
    bucket_day = today.strftime("%d")
    month_idn_title = get_month_id(today.strftime("%B"), case="title")
    bucket_filename = (
        f"Summary Performance Bucket Current {bucket_day} {month_idn_title}"
    )
    pyautogui.write(bucket_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    # ── CLOSE WORKBOOKS ───────────────────────────────────────────────────────
    move_cursor_figure_eight()
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    logger.info("[EXCEL] CLOSE WORKSOURCE FILE")
    switch_to_first_sheet()
    switch_to_first_cells()
    close_unsave()


def send_email():
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]

    today = datetime.now() - timedelta(days=1)
    bucket_day = today.strftime("%d")
    bucket_year = today.strftime("%Y")
    month_idn_title = get_month_id(today.strftime("%B"), case="title")

    subject_email = f"Summary Performance Bucket Current {bucket_day} {month_idn_title} {bucket_year}"

    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Performance Bucket Current {bucket_day} {month_idn_title} {bucket_year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

"""

    footer_template = """


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
    logger.info("[SYSTEM] START SUMMARY PERFORMANCE BUCKET CURRENT REPORT")
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── PRE-FLIGHT CHECKS ─────────────────────────────────────────────────────
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    clear_submission_folder(target_folder=CONFIG["SUB_PERFORMANCE_BUCKET_CURRENT"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── EXCEL PROCESSING ──────────────────────────────────────────────────────
    excel_config()  
    
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── EMAIL DISPATCH ────────────────────────────────────────────────────────
    send_email()
    logger.info("[SYSTEM] SUMMARY PERFORMANCE BUCKET CURRENT REPORT SENT")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── FINALISE ──────────────────────────────────────────────────────────────
    stop_counter()
    execution_time = get_execution_duration()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
