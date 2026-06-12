import os
import pyautogui
from datetime import datetime, timedelta
from pynput.keyboard import Controller
from general_task import *
from mail.outlook_performance_cwo_wo import send_outlook_email
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from services.duration_counter import start_counter, stop_counter, start_counter_result
from remover.remover_performance_cwo_wo import clear_submission_folder
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
    logger.info("[SYSTEM] CWO/WO REPORT EXCEL WORKFLOW")

    # ──────── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_PERFORMANCE_CWO_WO"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()

    # ──────── REFRESH ALL DATA CONNECTIONS
    switch_to_first_sheet()
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    # ──────── NAVIGATE TO THE TARGET SHEET
    for _ in range(2):
        switch_to_right_sheet()

    # ──────── EXTRACT THE TARGET SHEET INTO A STANDALONE WORKBOOK
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    # ──────── SEVER ALL EXTERNAL LINKS
    switch_to_first_sheet()
    break_excel_link()

    # ──────── CAPTURE THE TABLE AS AN IMAGE
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ──────── SAVE THE NEW WORKBOOK
    save_new_book()
    pyautogui.write(CONFIG["SUB_PERFORMANCE_CWO_WO"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ──────── ASSIGN THE STANDARDISED FILENAME
    set_new_book_name()
    today = datetime.now() - timedelta(days=1)
    cwo_day = today.strftime("%d")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    cwo_filename = f"Summary Performance Dashboard CWO - WO {cwo_day} {month_idn_title}"
    pyautogui.write(cwo_filename, interval=0.05)
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
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
 

def send_email():
    # ──────── DEFINE RECIPIENTS AND SUBJECT LINE
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]
    today = datetime.now() - timedelta(days=1)
    cwo_day = today.strftime("%d")
    cwo_year = today.strftime("%Y")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = (
        f"Summary Performance Dashboard CWO - WO | {cwo_day} {month_idn_title} {cwo_year}"
    )

    # ──────── SET EMAIL BODY
    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Performance Dashboard CWO - WO & Estimasi WO {cwo_day} {month_idn_title} {cwo_year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

"""

    footer_template = """


Hormat kami,
Asset Management Division
Collection HO - PT Suzuki Finance Indonesia
"""

    # ──────── DISPATCH THE EMAIL VIA OUTLOOK
    send_outlook_email(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
    )


# ───────── ENTRY POINT
if __name__ == "__main__":
    logger.info("[SYSTEM] START CWO / WO REPORT")

    # ──────── INITIALISE THE REPORT RUN
    start_counter()
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── CLEAR THE SUBMISSIONS DIRECTORY
    clear_submission_folder(target_folder=CONFIG["SUB_PERFORMANCE_CWO_WO"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── EXECUTE THE AUTOMATION WORKFLOW
    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] CWO / WO REPORT SENT")

    # ──────── FINALISE AND RESTORE THE ENVIRONMENT
    stop_counter()
    execution_time = start_counter_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
