from services.capslock_checker import capslock_checking
from services.config import load_config, logger, wait_timer
from services.report.alda.dispatcher import dispatch_alda_report
from services.report.alda.excel_processor import process_alda_workbook
from services.duration_counter import start_counter, stop_counter, get_execution_duration
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

CONFIG = load_config()


if __name__ == "__main__":
    logger.info("[SYSTEM] START ALDA REPORT")
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    process_alda_workbook()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    dispatch_alda_report()
    logger.info("[SYSTEM] ALDA REPORT SENT")

    stop_counter()
    execution_time = start_counter()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
