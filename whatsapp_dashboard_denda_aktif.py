from services.capslock_checker import capslock_checking
from services.config import load_config, logger, wait_timer
from services.duration_counter import start_counter, start_counter, stop_counter
from services.report.denda_aktif.dispatcher import dispatch_denda_aktif_report
from services.report.denda_aktif.excel_processor import process_denda_aktif_workbook
from screen_keeper import (
    find_screen_keeper_process,
    run_screen_keeper,
    stop_screen_keeper,
)

CONFIG = load_config()


if __name__ == "__main__":
    logger.info("[SYSTEM] START DENDA AKTIF REPORT")
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    process_denda_aktif_workbook()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    dispatch_denda_aktif_report()
    logger.info("[SYSTEM] DENDA AKTIF REPORT SENT")

    stop_counter()
    execution_time = start_counter()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
