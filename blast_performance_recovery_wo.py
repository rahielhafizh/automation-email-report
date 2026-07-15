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
from remover.remover_performance_ar_tod import clear_submission_folder
from services.config import get_month_id, load_config, logger, wait_timer
from services.duration_counter import (
    get_execution_duration,
    start_counter,
    stop_counter,
)
from mail.outlook_performance_recovery_wo import send_outlook_email

pyautogui.FAILSAFE = False
CONFIG = load_config()
keyboard = Controller()


def excel_config():
    logger.info("[SYSTEM] SUMMARY DAILY PERFORMANCE RECOVERY WO EXCEL WORKFLOW")
    os.startfile(CONFIG["WORKSOURCE_PERFORMANCE_RECOVERY_WO"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()

    # ── REFRESH DATA ──────────────────────────────────────────────────────────
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])
    scroller_page()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    # ── NAVIGATE TO SUMMARY SHEET ─────────────────────────────────────────────
    for _ in range(2):
        switch_to_right_sheet()

    switch_to_first_cells()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    # ── COPY SHEET TO NEW WORKBOOK ────────────────────────────────────────────
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    move_cell_horizontal()
    switch_to_first_cells()

    # ── BREAK EXTERNAL LINKS ──────────────────────────────────────────────────
    break_excel_link()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    # ── CAPTURE TABLE AS PICTURE ──────────────────────────────────────────────
    capturing_report_picture()


    # ── SAVE NEW WORKBOOK ─────────────────────────────────────────────────────
    save_new_book()
    pyautogui.write(CONFIG["SUB_PERFORMANCE_RECOVERY_WO"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()
    today = datetime.now() - timedelta(days=1)
    recovery_wo_day = today.strftime("%d")
    month_idn_title = get_month_id(today.strftime("%B"), case="title")
    cwo_filename = (
        f"Summary Daily Performance Recovery WO {recovery_wo_day} {month_idn_title}"
    )
    pyautogui.write(cwo_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    logger.info("[EXCEL] CLOSE WORKSOURCE FILE")
    switch_to_first_sheet()
    switch_to_first_cells()
    close_unsave()


def send_email():
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]

    today = datetime.now() - timedelta(days=1)
    recovery_wo_day = today.strftime("%d")
    month_idn_title = get_month_id(today.strftime("%B"), case="title")

    subject_email = (
        f"Summary Report Performance Recovery WO | {recovery_wo_day} {month_idn_title}"
    )

    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Update Performance Recovery WO {recovery_wo_day} {month_idn_title}

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
    logger.info("[SYSTEM] START SUMMARY DAILY PERFORMANCE RECOVERY WO REPORT")
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── PRE-FLIGHT CHECKS ─────────────────────────────────────────────────────
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    clear_submission_folder(target_folder=CONFIG["SUB_PERFORMANCE_RECOVERY_WO"])
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
    logger.info("[SYSTEM] SUMMARY DAILY PERFORMANCE RECOVERY WO REPORT SENT")

    # ── FINALISE ──────────────────────────────────────────────────────────────
    stop_counter()
    execution_time = get_execution_duration()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
