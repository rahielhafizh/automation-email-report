import os
import pyautogui
from datetime import datetime
from pynput.keyboard import Controller
from general_task import *
from mail.outlook_performance_cash_in import send_outlook_email
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from services.duration_counter import (
    start_counter,
    stop_counter,
    get_execution_duration,
)

from remover.remover_performance_cash_in import clear_submission_folder
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

# ───────── RUNTIME INITIALISATION
pyautogui.FAILSAFE = False
CONFIG = load_config()
keyboard = Controller()


# ───────── CORE WORKFLOW
def excel_config():
    logger.info("[SYSTEM] CASH IN REPORT EXCEL WORKFLOW")

    # ──────── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_PERFORMANCE_CASH_IN"])
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    maximize_app_window()

    # ──────── REFRESH ALL DATA CONNECTIONS
    switch_to_first_sheet()
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    move_cursor_figure_eight()
    scroller_page()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    switch_to_first_cells()

    # ──────── NAVIGATE TO THE TARGET SHEET
    for _ in range(5):
        switch_to_right_sheet()

    # ──────── EXTRACT THE TARGET SHEET INTO NEW WORKBOOK
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])

    # ──────── SEVER ALL EXTERNAL LINKS
    switch_to_first_sheet()
    break_excel_link()

    # ──────── CAPTURE THE TABLE AS AN IMAGE
    capturing_report_picture()

    # ──────── SAVE THE NEW WORKBOOK
    save_new_book()
    pyautogui.write(CONFIG["SUB_PERFORMANCE_CASH_IN"])
    confirm()

    # ──────── ASSIGN THE STANDARDISED FILENAME
    set_new_book_name()
    today = datetime.now()
    report_day = today.strftime("%d")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    report_filename = (
        f"Report Performance Cash In Today vs N-1 ({report_day} {month_idn_title})"
    )
    pyautogui.write(report_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ──────── CLOSE THE EXPORTED WORKBOOK
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ──────── SAVE AND CLOSE THE SOURCE FILE
    switch_to_first_sheet()
    switch_to_first_cells()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()


def send_email():
    # ──────── DEFINE RECIPIENTS AND SUBJECT LINE
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]
    today = datetime.now()
    report_day = today.strftime("%d")
    report_year = today.strftime("%Y")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")

    subject_email = (
        f"Report Performance Cash In Today ({report_day} {month_idn_title}) vs N-1"
    )

    # ──────── SET EMAIL BODY
    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Report Performance Cash In Today ({report_day} {month_idn_title} {report_year}) vs N-1.

Catatan:
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

"""

    footer_template = """


Hormat kami,
Asset Management Division
Collection HO - PT Suzuki Finance Indonesia
"""

    # ──────── DISPATCH THE EMAIL VIA OUTLOOK
    try:
        send_outlook_email(
            outlook_recipients,
            secondary_recipients,
            subject_email,
            core_email,
            footer_template,
        )
    except Exception as exc:
        logger.error(f"[ERROR] FAILED TO SEND EMAIL : {exc}")
        raise


# ───────── ENTRY POINT
if __name__ == "__main__":
    logger.info("[SYSTEM] START CASH IN REPORT")

    # ──────── INITIALISE THE REPORT RUN
    start_counter()
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    clear_submission_folder(target_folder=CONFIG["SUB_PERFORMANCE_CASH_IN"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── EXECUTE THE AUTOMATION WORKFLOW
    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] CASH IN REPORT SENT")

    # ──────── FINALISE AND RESTORE THE ENVIRONMENT
    stop_counter()
    execution_time = get_execution_duration()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
