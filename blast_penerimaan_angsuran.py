import os
import pyautogui
from datetime import datetime
from general_task import *
from pynput.keyboard import Controller
from remover.remover_penerimaan_angsuran import clear_submission_folder
from services.config import load_config, wait_timer, logger, get_month_id
from mail.outlook_penerimaan_angsuran import send_outlook_email
from services.capslock_checker import capslock_checking
from services.duration_counter import (
    start_counter,
    stop_counter,
    get_execution_duration,
)
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
    logger.info("[SYSTEM] INSTALLMENT PAYMENT REPORT EXCEL WORKFLOW")

    # ──────── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_PENERIMAAN_ANGSURAN"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    maximize_app_window()
    switch_to_first_cells()

    # ──────── REFRESH ALL DATA CONNECTIONS
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    move_cursor_figure_eight()
    scroller_page()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    # ──────── NAVIGATE TO THE TARGET SHEET
    switch_to_first_sheet()
    switch_to_first_cells()
    for _ in range(2):
        switch_to_right_sheet()
    switch_to_first_cells()

    # ──────── EXTRACT THE TARGET SHEET INTO A STANDALONE WORKBOOK
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])
    move_cursor_figure_eight()
    scroller_page()

    # ──────── SEVER ALL EXTERNAL LINKS
    switch_to_first_sheet()
    break_excel_link()
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    escaping()
    
    # ──────── CAPTURE THE TABLE AS AN IMAGE
    capturing_report_picture()

    # ──────── SAVE THE NEW WORKBOOK
    save_new_book()
    pyautogui.write(CONFIG["SUB_PENERIMAAN_ANGSURAN"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    # ──────── ASSIGN THE STANDARDISED FILENAME
    set_new_book_name()
    today = datetime.now()
    payment_day = today.strftime("%d")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    payment_filename = f"Summary Report Update Penerimaan Angsuran - {payment_day} {month_idn_title} ({today.strftime('%H.%M')})"
    pyautogui.write(payment_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    # ──────── CLOSE THE EXPORTED WORKBOOK
    switch_to_right_sheet()
    switch_to_first_sheet()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    move_cursor_figure_eight()
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    move_cursor_figure_eight()
    
    # ──────── SAVE AND CLOSE THE SOURCE FILE
    move_cell_horizontal()
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_right_sheet()
    switch_to_first_cells()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def send_email():
    # ──────── DEFINE RECIPIENTS AND SUBJECT LINE
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "herberth.simbolon@sfi.co.id"]
    today = datetime.now()
    year = today.strftime("%Y")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = f"Summary Update Penerimaan Angsuran | {datetime.now().strftime('%d')} {month_idn_title} ({today.strftime('%H:%M')})"

    # ──────── SET EMAIL BODY
    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Update Penerimaan Angsuran As Of {month_idn_title} {year} pukul {today.strftime('%H:%M')} WIB.

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


# ───────── ENTRY POINT
if __name__ == "__main__":
    logger.info("[SYSTEM] START INSTALLMENT PAYMENT REPORT")

    # ──────── INITIALISE THE REPORT RUN
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUB_PENERIMAAN_ANGSURAN"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # ──────── EXECUTE THE AUTOMATION WORKFLOW
    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] INSTALLMENT PAYMENT REPORT SENT")

    # ──────── FINALISE AND RESTORE THE ENVIRONMENT
    stop_counter()
    execution_time = get_execution_duration()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    logger.info("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
