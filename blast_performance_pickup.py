import os
import pyautogui
from datetime import datetime
from general_task import *
from mail.outlook_performance_pickup import send_outlook_email
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from remover.remover_performance_pickup import clear_submission_folder
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

# ───────── RUNTIME INITIALISATION
pyautogui.FAILSAFE = False
CONFIG = load_config()
pyautogui.FAILSAFE = False


# ───────── CORE WORKFLOW
def excel_config():
    logger.info("[SYSTEM] REPPO/PICKUP REPORT EXCEL WORKFLOW")

    # ──────── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_PICKUP"])
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    maximize_app_window()

    switch_to_first_sheet()
    switch_to_first_cells()

    # ──────── REFRESH ALL DATA CONNECTIONS
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    entering_operation()
    switch_to_first_cells()
    save_file()

    # ──────── CONVERT THE SUMMARY TABLE TO STATIC VALUES
    switch_to_last_sheet()
    switch_to_first_cells()
    convert_to_range()
    capture_table_as_table()
    paste_value_as_value()

    # ──────── CAPTURE THE TABLE AS AN IMAGE
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ──────── SAVE THE NEW WORKBOOK
    save_as_in()
    pyautogui.write(CONFIG["SUBMISSION_PICKUP"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ──────── ASSIGN THE STANDARDISED FILENAME
    save_as_name()
    today = datetime.now()
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    pickup_filename = f"Summary Update Pickup {today.strftime('%d')} {month_idn_title} ({today.strftime('%H.%M')})"
    pyautogui.write(pickup_filename, interval=0.05)

    # ──────── CLOSE THE EXPORTED WORKBOOK
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def send_email():
    # ──────── DEFINE RECIPIENTS AND SUBJECT LINE
    outlook_recipients = ["herberth.simbolon@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "asset.mgmt@sfi.co.id"]
    today = datetime.now()
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = f"Summary Update Reppo/Pickup | {datetime.now().strftime('%d')} {month_idn_title} ({today.strftime('%H:%M')})"

    # ──────── SET EMAIL BODY
    core_email = f"""Yth. Bapak Chief of Operating Officer,
    
Dengan hormat,

Berikut terlampir Summary Update Daily Reppo/Pickup pada {today.strftime('%d')} {month_idn_title} pukul {today.strftime('%H:%M')} WIB.

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data diperoleh secara real-time namun harap diperhatikan dan dievaluasi kembali.

"""

    footer_template = """


Hormat kami,
Asset Management Division.
Collection HO - PT Suzuki Finance Indonesia.
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

    logger.info("[DATA] REPPO/PICKUP REPORT SENT")


# ───────── ENTRY POINT
if __name__ == "__main__":
    logger.info("[SYSTEM] START REPPO/PICKUP REPORT")

    # ──────── INITIALISE THE REPORT RUN
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── CLEAR THE SUBMISSIONS DIRECTORY
    clear_submission_folder(target_folder=CONFIG["SUBMISSION_PICKUP"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── EXECUTE THE AUTOMATION WORKFLOW
    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] REPPO/PICKUP REPORT SENT")

    # ──────── FINALISE AND RESTORE THE ENVIRONMENT
    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    run_screen_keeper()
