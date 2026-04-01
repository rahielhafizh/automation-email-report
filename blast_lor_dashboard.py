import os
import pyautogui
from datetime import datetime, timedelta
from pynput.keyboard import Key, Controller
from general_task import *
from outlook_lor import send_outlook_email
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from services.duration_counter import start_counter, stop_counter, get_duration_result
from services.remover_lor import clear_submission_folder
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

# ─── RUNTIME INITIALISATION
CONFIG = load_config()
keyboard = Controller()


# ─── CORE WORKFLOW
def excel_config():
    logger.info("[SYSTEM] MOBCOLL LOR REPORT EXCEL WORKFLOW")

    # ── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_LOR"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()

    # ── REFRESH ALL DATA CONNECTIONS
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    # ── NAVIGATE TO THE TARGET SHEET
    for _ in range(2):
        switch_to_right_sheet()
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    # ── SEVER ALL EXTERNAL LINKS
    break_excel_link()

    # ── CAPTURE THE TABLE AS AN IMAGE
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ── SAVE THE NEW WORKBOOK
    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_LOR"])
    confirm()

    # ── ASSIGN THE STANDARDISED FILENAME
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    set_new_book_name()
    yesterday = datetime.now() - timedelta(days=1)
    lor_day = yesterday.strftime("%d")
    year = yesterday.strftime("%Y")
    month_eng = yesterday.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    lor_filename = f"Summary Mobcoll LOR Periode {lor_day} {month_idn_title} {year}"
    pyautogui.write(lor_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    # ── SAVE AND CLOSE THE SOURCE FILE
    switch_to_first_sheet()
    switch_to_first_cells()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    logger.info("[SYSTEM] MOBCOLL LOR WORKFLOW COMPLETE")


def send_email():
    # ── DEFINE RECIPIENTS AND COMPOSE THE SUBJECT LINE
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = "collho.3@sfi.co.id"
    yesterday = datetime.now() - timedelta(days=1)
    year = yesterday.strftime("%Y")
    month_eng = yesterday.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = f"Summary Update Mobcoll LOR | Periode {month_idn_title} {year}"

    # ── COMPOSE THE EMAIL BODY
    core_email = f"""Dear All,

Dengan hormat,
Berikut terlampir Summary Update Penugasan dan Kunjungan PIC LOR pada Periode {month_idn_title} {year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Harap diperhatikan serta dapat dievaluasi kembali.
"""

    footer_template = """


Hormat kami,
Asset Management Division.
Collection HO - PT Suzuki Finance Indonesia.
"""

    # ── DISPATCH THE EMAIL VIA OUTLOOK
    send_outlook_email(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
    )


# ─── ENTRY POINT
if __name__ == "__main__":
    logger.info("[SYSTEM] START MOBCOLL LOR REPORT")

    # ── INITIALISE THE REPORT RUN
    start_counter()
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    clear_submission_folder(target_folder=CONFIG["SUBMISSION_LOR"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ── EXECUTE THE AUTOMATION WORKFLOW
    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] MOBCOLL LOR REPORT SENT")

    # ── FINALISE AND RESTORE THE ENVIRONMENT
    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
