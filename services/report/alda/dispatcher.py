from services.config import load_config, logger
from services.message_formatter import ReportTimestamp
from services.whatsapp_sender import send_to_group
from services.report.alda.message_builder import build_alda_message

CONFIG = load_config()


def dispatch_alda_report() -> bool:
    logger.info("[ALDA] INITIATING REPORT DISPATCH")
    try:
        link = CONFIG.get("ASSET_GROUP")
        if not link:
            raise ValueError("GROUP LINK NOT FOUND")
        result = send_to_group(link, build_alda_message(ReportTimestamp.now()))
        if result:
            logger.info("[ALDA] DISPATCH SUCCESSFUL")
        else:
            logger.error("[ALDA] DISPATCH FAILED")
        return bool(result)
    except Exception as e:
        logger.error(f"[ALDA] DISPATCH ERROR: {e}")
        return False
