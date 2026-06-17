# Execution time : 12 Minutes
from services.capslock_checker import capslock_checking
from services.config import load_config, logger, wait_timer
from services.duration_counter import start_counter, start_counter, stop_counter
from services.report.lor.excel_processor import refresh_workbook
from services.report.lor.dispatcher import (
    dispatch_area_report,
    dispatch_as_of_report,
    dispatch_today_report,
)
from screen_keeper import (
    find_screen_keeper_process,
    run_screen_keeper,
    stop_screen_keeper,
)

CONFIG = load_config()


def dispatch_sequence_lor() -> None:
    if not dispatch_area_report():
        logger.error("[LOR] AREA REPORT FAILED — SEQUENCE ABORTED")
        return
    logger.info("[LOR] AREA REPORT DISPATCHED")

    if not dispatch_as_of_report():
        logger.error("[LOR] AS-OF REPORT FAILED — SEQUENCE ABORTED")
        return
    logger.info("[LOR] AS-OF REPORT DISPATCHED")

    if not dispatch_today_report():
        logger.error("[LOR] TODAY REPORT FAILED")
        return
    logger.info("[LOR] TODAY REPORT DISPATCHED")


if __name__ == "__main__":
    logger.info("[SYSTEM] START LOR REPORT GROUP DELIVERY")
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    refresh_workbook()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    dispatch_sequence_lor()
    logger.info("[SYSTEM] LOR REPORT GROUP DELIVERY COMPLETE")

    stop_counter()
    execution_time = start_counter()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
