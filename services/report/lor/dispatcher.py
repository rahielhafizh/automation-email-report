from __future__ import annotations
from services.config import load_config, logger
from services.message_formatter import ReportTimestamp
from services.whatsapp_sender import send_to_group
from services.report.lor.excel_processor import LorSheet, take_summary_picture
from services.report.lor.message_builder import (
    build_area_message,
    build_as_of_message,
    build_today_message,
)

CONFIG = load_config()


def _resolve_group_link() -> str:
    link = CONFIG.get("ASSET_GROUP")
    if not link:
        raise ValueError("GROUP LINK NOT FOUND")
    return link


def _dispatch(sheet: LorSheet, message: str, label: str) -> bool:
    try:
        take_summary_picture(sheet)
        result = send_to_group(_resolve_group_link(), message)
        if result:
            logger.info(f"[LOR {label}] DISPATCH SUCCESSFUL")
        else:
            logger.error(f"[LOR {label}] DISPATCH FAILED")
        return bool(result)
    except Exception as e:
        logger.error(f"[LOR {label}] DISPATCH ERROR: {e}")
        return False


def dispatch_area_report() -> bool:
    logger.info("[LOR AREA] INITIATING REPORT DISPATCH")
    return _dispatch(LorSheet.AREA, build_area_message(ReportTimestamp.now()), "AREA")


def dispatch_as_of_report() -> bool:
    logger.info("[LOR AS-OF] INITIATING REPORT DISPATCH")
    return _dispatch(
        LorSheet.AS_OF, build_as_of_message(ReportTimestamp.now()), "AS-OF"
    )


def dispatch_today_report() -> bool:
    logger.info("[LOR TODAY] INITIATING REPORT DISPATCH")
    return _dispatch(
        LorSheet.TODAY, build_today_message(ReportTimestamp.now()), "TODAY"
    )
