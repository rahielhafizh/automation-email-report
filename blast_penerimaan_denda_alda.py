import os
import pyautogui
from datetime import datetime
from pynput.keyboard import Controller
from general_task import *
from mail.outlook_penerimaan_denda_alda import send_outlook_email
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from services.duration_counter import (
    start_counter,
    stop_counter,
    get_execution_duration,
)
from remover.remover_penerimaan_denda_alda import clear_submission_folder
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
    logger.info("[SYSTEM] ALDA FINE REPORT EXCEL WORKFLOW")

    # ──────── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_PENERIMAAN_DENDA_ALDA"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()

    # ──────── NAVIGATE TO THE STARTING POSITION
    switch_to_right_sheet()
    switch_to_first_sheet()

    # ──────── REFRESH ALL DATA CONNECTIONS
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    # ──────── NAVIGATE TO THE TARGET SHEET
    switch_to_right_sheet()
    switch_to_right_sheet()

    # ──────── EXTRACT THE TARGET SHEET INTO A STANDALONE WORKBOOK
    switch_to_first_cells()
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    # ──────── SEVER ALL EXTERNAL LINKS
    switch_to_first_sheet()
    break_excel_link()

    # ──────── CAPTURE THE TABLE AS AN IMAGE
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ──────── SAVE THE NEW WORKBOOK
    save_new_book()
    pyautogui.write(CONFIG["SUB_PENERIMAAN_DENDA_ALDA"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ──────── ASSIGN THE STANDARDISED FILENAME
    set_new_book_name()
    today = datetime.now()
    fine_day = today.strftime("%d")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    fine_filename = f"Summary Report Penerimaan Denda Alda {fine_day} {month_idn_title} ({today.strftime('%H.%M')})"
    pyautogui.write(fine_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ──────── SAVE AND CLOSE THE SOURCE FILE
    switch_to_first_cells()
    switch_to_first_sheet()
    switch_to_first_cells()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def send_email():
    # ──────── DEFINE RECIPIENTS AND SUBJECT LINE
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]
    today = datetime.now()
    month_eng = today.strftime("%B")
    fine_year = today.strftime("%Y")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = f"Summary Report Penerimaan Denda Alda | {datetime.now().strftime('%d')} {month_idn_title} ({today.strftime('%H:%M')})"

    # ──────── SET EMAIL BODY
    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Report Penerimaan Denda Alda As Of {month_idn_title} {fine_year} Pukul {today.strftime('%H:%M')} WIB.

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
    send_outlook_email(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
    )


# ───────── ENTRY POINT
if __name__ == "__main__":
    logger.info("[SYSTEM] START ACTIVE FINE REPORT")

    # ──────── INITIALISE THE REPORT RUN
    start_counter()
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUB_PENERIMAAN_DENDA_ALDA"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── EXECUTE THE AUTOMATION WORKFLOW
    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] ACTIVE FINE REPORT SENT")

    # ──────── FINALISE AND RESTORE THE ENVIRONMENT
    stop_counter()
    execution_time = get_execution_duration()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
