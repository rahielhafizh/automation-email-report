import os
import pyautogui
from datetime import datetime, timedelta
from general_task import *
from pynput.keyboard import Controller
from services.config import load_config, wait_timer, logger, get_month_id
from outlook_stopsell import send_outlook_email
from services.capslock_checker import capslock_checking
from remover.remover_stopsell import clear_submission_folder
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

# ───────── RUNTIME INITIALISATION
CONFIG = load_config()
keyboard = Controller()


# ───────── CORE WORKFLOW
def excel_config():
    logger.info("[SYSTEM] STOPSELL REPORT EXCEL WORKFLOW")

    # ──────── RESOLVE YESTERDAY'S DATE FOR PRIOR-DAY REPORTING PERIOD
    yesterday = datetime.now() - timedelta(days=1)
    year = yesterday.strftime("%Y")
    month_eng = yesterday.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_text = f"{month_idn_title} {year}"
    body_text = f"{month_idn_title} {year}"
    filename_text = f"{yesterday.day} {month_idn_title} {year}"

    # ──────── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_STOPSELL"])
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()

    # ──────── REFRESH ALL DATA CONNECTIONS
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_MINUTE"])
    entering_operation()

    # ──────── NAVIGATE TO THE TARGET SHEET
    switch_to_right_sheet()
    select_sheet_half_down()

    # ──────── EXTRACT THE TARGET SHEET INTO A STANDALONE WORKBOOK
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])

    # ──────── SEVER ALL EXTERNAL LINKS
    break_excel_link()

    # ──────── CAPTURE THE TABLE AS AN IMAGE
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_right_sheet()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ──────── SAVE THE NEW WORKBOOK
    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_STOPSELL"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    # ──────── ASSIGN THE STANDARDISED FILENAME
    set_new_book_name()
    stopsell_filename = (
        f"Summary Penugasan & Kunjungan Cabang Stop Sell ({filename_text})"
    )
    pyautogui.write(stopsell_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])

    # ──────── CLOSE THE EXPORTED WORKBOOK
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    # ──────── SAVE AND CLOSE THE SOURCE FILE
    switch_to_first_sheet()
    switch_to_right_sheet()
    switch_to_first_cells()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    # ──────── RETURN DATE TOKENS FOR EMAIL COMPOSITION
    return subject_text, body_text


def send_email(subject_text, body_text):
    # ──────── DEFINE RECIPIENTS AND SUBJECT LINE
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]
    subject_email = (
        f"Summary Penugasan & Kunjungan Cabang Stop Sell As Of | {subject_text}"
    )

    # ──────── SET EMAIL BODY
    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Penugasan dan Kunjungan Cabang Stop Sell As of {body_text}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.
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


def main():
    logger.info("[SYSTEM] START STOP SELL REPORT")

    # ──────── INITIALISE THE REPORT RUN
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── CLEAR THE SUBMISSIONS DIRECTORY
    clear_submission_folder(target_folder=CONFIG["SUBMISSION_STOPSELL"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── EXECUTE THE AUTOMATION WORKFLOW
    subject_text, body_text = excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email(subject_text, body_text)
    logger.info("[SYSTEM] STOP SELL REPORT COMPLETED")

    # ──────── FINALISE AND RESTORE THE ENVIRONMENT
    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()


# ───────── ENTRY POINT
if __name__ == "__main__":
    main()
