from services.config import load_config, logger
from services.message_formatter import ReportTimestamp
from services.whatsapp_sender import send_to_group
from services.report.denda_aktif.message_builder import build_denda_aktif_message

CONFIG = load_config()


def dispatch_denda_aktif_report() -> bool:
    logger.info("[DENDA AKTIF] INITIATING REPORT DISPATCH")
    try:
        link = CONFIG.get("ASSET_GROUP")
        if not link:
            raise ValueError("GROUP LINK NOT FOUND")
        result = send_to_group(link, build_denda_aktif_message(ReportTimestamp.now()))
        if result:
            logger.info("[DENDA AKTIF] DISPATCH SUCCESSFUL")
        else:
            logger.error("[DENDA AKTIF] DISPATCH FAILED")
        return bool(result)
    except Exception as e:
        logger.error(f"[DENDA AKTIF] DISPATCH ERROR: {e}")
        return False
