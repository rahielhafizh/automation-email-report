import pyperclip
from datetime import date, datetime
from screen_keeper import (
    find_screen_keeper_process,
    run_screen_keeper,
    stop_screen_keeper,
)
from services.rrd_checker import check_flowrate_status
from services.config import load_config, logger, wait_timer
from services.whatsapp_sender import send_to_group
from services.duration_counter import start_counter, stop_counter, start_counter_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)
from typing import Optional

CONFIG = load_config()
VALID_INDICATOR = "✅"
INVALID_INDICATOR = "❎"


def format_report_date(running_report_date: date) -> str:
    return running_report_date.strftime("%d/%m/%Y")


def format_update_time(periode_update: datetime) -> str:
    return periode_update.strftime("%d/%m/%Y (%H:%M)")


def setup_message(
    is_valid: bool,
    running_report_date: Optional[date],
    periode_update: Optional[datetime],
) -> str:
    if running_report_date is None:
        return (
            f"Validasi Tabel Dashboard Control\n\n"
            f"Tabel Tidak Tersedia {INVALID_INDICATOR}"
        )

    indicator = VALID_INDICATOR if is_valid else INVALID_INDICATOR
    rrd_display = format_report_date(running_report_date)
    periode_display = (
        format_update_time(periode_update) if periode_update is not None else "-"
    )

    return (
        f"Validasi Tabel Dashboard Control\n\n"
        f"Tanggal RunningReportDate : {rrd_display} {indicator}\n"
        f"Data diperbarui pada : {periode_display}"
    )


def sent_checking_result() -> bool:
    logger.info("[INFO] DASHBOARD CONTROL VALIDATION")
    group_link = CONFIG.get("ASSET_GROUP")

    if not group_link:
        logger.error("[INFO] LINK NOT FOUND IN CONFIG")
        return False

    try:
        is_valid, running_report_date, periode_update = check_flowrate_status()
        message = setup_message(is_valid, running_report_date, periode_update)
        pyperclip.copy(message)
        logger.info("[INFO] MESSAGE COPIED TO CLIPBOARD")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        result = send_to_group(group_link, message="")
        if result:
            logger.info(f"[INFO] MESSAGE DISPATCHED")
            return True

        logger.error("[INFO] DISPATCH FAILED")
        return False

    except Exception as e:
        logger.error(f"[INFO] UNEXPECTED ERROR : {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("[SYSTEM] START DASHBOARD CONTROL VALIDATION")
    start_counter()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    sent_checking_result()
    logger.info("[SYSTEM] DASHBOARD CONTROL VALIDATION SENT")
    stop_counter()
    execution_time = start_counter()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
