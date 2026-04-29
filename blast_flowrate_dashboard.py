import os
import pyautogui
from datetime import datetime
from pynput.keyboard import Controller
from general_task import *
from outlook_flowrate import send_outlook_email
from data_validate_flowrate_mail import validate_flowrate_file
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from services.duration_counter import start_counter, stop_counter, get_duration_result
from services.remover_flowrate import clear_submission_folder
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
    logger.info("[SYSTEM] FLOWRATE REPORT EXCEL WORKFLOW")

    # ──────── VERIFY THE SOURCE FILE IS ACCESSIBLE
    if not os.path.exists(CONFIG["WORKSOURCE_FLOWRATE"]):
        logger.error(f"[ERROR] SOURCE FILE NOT FOUND : {CONFIG['WORKSOURCE_FLOWRATE']}")
        return None

    # ──────── OPEN THE SOURCE WORKBOOK
    os.startfile(CONFIG["WORKSOURCE_FLOWRATE"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTYFIVE_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()

    # ──────── REFRESH ALL DATA CONNECTIONS
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWOHALF_MINUTE"])
    move_cursor_figure_eight()
    scroller_page()
    wait_timer(CONFIG["WAIT_TIME"]["TWOHALF_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    # ──────── NAVIGATE TO THE TARGET SHEET
    for _ in range(2):
        switch_to_right_sheet()
    switch_to_first_cells()

    # ──────── EXTRACT THE TARGET SHEET INTO A STANDALONE WORKBOOK
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_MINUTE"])
    move_cursor_figure_eight()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    # ──────── SEVER ALL EXTERNAL LINKS
    switch_to_table_cells()
    break_excel_link()

    # ──────── CAPTURE THE TABLE AS AN IMAGE
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    # ──────── SAVE THE NEW WORKBOOK
    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_FLOWRATE"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    # ──────── ASSIGN THE STANDARDISED FILENAME
    set_new_book_name()
    today = datetime.now()
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    flowrate_filename = f"Summary Report Flowrate {datetime.now().strftime('%d')} {month_idn_title} ({today.strftime('%H.%M')})"
    pyautogui.write(flowrate_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    # ──────── CLOSE THE EXPORTED WORKBOOK
    switch_to_right_sheet()
    switch_to_first_sheet()
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    # ──────── SAVE AND CLOSE THE SOURCE FILE
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_right_sheet()
    switch_to_first_cells()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    # ──────── RETURN THE EXPORT PATH FOR DOWNSTREAM VALIDATION
    created_file_path = os.path.join(
        CONFIG["SUBMISSION_FLOWRATE"], f"{flowrate_filename}.xlsx"
    )
    return created_file_path


def send_email():
    # ──────── DEFINE RECIPIENTS AND SUBJECT LINE
    outlook_recipients = ["herberth.simbolon@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "asset.mgmt@sfi.co.id"]
    today = datetime.now()
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = f"Summary Update Prediksi Flowrate | {datetime.now().strftime('%d')} {month_idn_title} ({today.strftime('%H:%M')})"

    # ──────── SET EMAIL BODY
    core_email = f"""Yth. Bapak Chief of Operating Officer,

Dengan hormat,

Berikut terlampir Summary Update Daily Flowrate per tanggal {datetime.now().strftime('%d')} {month_idn_title} pukul {today.strftime('%H:%M')} WIB.

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


def validate_and_send_email(created_file_path):
    # ──────── VERIFY THE FILE PATH AND CONFIRM PHYSICAL EXISTENCE
    if not created_file_path:
        logger.error("[ERROR] NO FILE PATH PROVIDED")
        return False

    if not os.path.exists(created_file_path):
        logger.error(f"[ERROR] FLOWRATE FILE NOT FOUND : {created_file_path}")
        return False

    # ──────── VALIDATE DATA INTEGRITY AND DISPATCH THE EMAIL
    try:
        validation_result = validate_flowrate_file(created_file_path)
        if validation_result:
            logger.info("[DATA] VALIDATION COMPLETE")
            send_email()
            return True
        else:
            logger.warning("[DATA] VALIDATION FAILED")
            return False
    except Exception as exc:
        logger.error(f"[ERROR] VALIDATION ERROR : {exc}")
        return False


# ───────── ENTRY POINT
def main():
    logger.info("[SYSTEM] START FLOWRATE REPORT")

    # ──────── INITIALISE THE REPORT RUN
    start_counter()

    try:
        capslock_checking()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        # ──────── CLEAR THE SUBMISSIONS DIRECTORY
        clear_submission_folder(target_folder=CONFIG["SUBMISSION_FLOWRATE"])
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        find_screen_keeper_process()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        stop_screen_keeper()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        # ──────── EXECUTE THE AUTOMATION WORKFLOW
        created_file_path = excel_config()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        if not created_file_path:
            logger.error("[ERROR] FLOWRATE REPORT NOT CREATED")
            return

        if not os.path.exists(created_file_path):
            logger.error(f"[ERROR] FILE NOT FOUND : {created_file_path}")
            return

        logger.info(f"[SYSTEM] REPORT CREATED : {os.path.basename(created_file_path)}")

        if validate_and_send_email(created_file_path):
            logger.info("[SYSTEM] PROCESS VALID FLOWRATE REPORT")
        else:
            logger.warning("[SYSTEM] PROCESS INVALID FLOWRATE REPORT")

    except KeyboardInterrupt:
        logger.warning("[SYSTEM] PROCESS INTERRUPTED BY USER")
    except Exception as exc:
        logger.exception(f"[ERROR] EXCEPTION : {exc}")

    finally:
        # ──────── FINALISE AND RESTORE THE ENVIRONMENT
        stop_counter()
        execution_time = get_duration_result()
        logger.info(f"[TIMER] TOTAL : {execution_time}")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        run_screen_keeper()


if __name__ == "__main__":
    main()
