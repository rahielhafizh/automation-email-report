from services.config import load_config, logger
from services.message_formatter import ReportTimestamp
from services.whatsapp_sender import send_to_group
from services.report.cash_in.message_builder import build_cash_in_message

CONFIG = load_config()


def dispatch_cash_in_report() -> bool:
    logger.info("[CASH IN] INITIATING REPORT DISPATCH")
    try:
        link = CONFIG.get("ASSET_GROUP")
        if not link:
            raise ValueError("GROUP LINK NOT FOUND")
        result = send_to_group(link, build_cash_in_message(ReportTimestamp.now()))
        if result:
            logger.info("[CASH IN] DISPATCH SUCCESSFUL")
        else:
            logger.error("[CASH IN] DISPATCH FAILED")
        return bool(result)
    except Exception as e:
        logger.error(f"[CASH IN] DISPATCH ERROR: {e}")
        return False
