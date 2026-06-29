import io
import logging
import sys
import time
from io import TextIOWrapper
from typing import Any, Optional

import pyautogui
from colorlog import ColoredFormatter

_pyautogui_configured = False


# ─── LOGGER FORMATTER ─────────────────────────────────────────────────────────
class SafeColoredFormatter(ColoredFormatter):
    DATE_FORMAT = "%d-%m-%Y %H:%M:%S"

    def formatTime(
        self, record: logging.LogRecord, datefmt: Optional[str] = None
    ) -> str:
        ct = self.converter(record.created)
        return time.strftime(self.DATE_FORMAT, ct)

    def format(self, record: logging.LogRecord) -> str:
        try:
            return super().format(record)
        except UnicodeEncodeError:
            record.msg = record.msg.encode("ascii", errors="replace").decode("ascii")
            record.args = ()
            try:
                return super().format(record)
            except Exception:
                return f"[LOG] {record.levelname}: {record.getMessage()}"


# ─── LOGGER SETUP ─────────────────────────────────────────────────────────────
def setup_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = SafeColoredFormatter(
            fmt=(
                "\n"
                "%(log_color)s[%(asctime)s]\n"
                "• CONDITION  : %(levelname)s\n"
                "• SOURCE     : %(filename)s:%(lineno)d\n"
                "• FUNCTION   : %(funcName)s()\n"
                "• MESSAGE    : %(message)s\n"
                "\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
            ),
            datefmt=None,
            log_colors={
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "bold_yellow",
                "ERROR": "thin_red",
                "CRITICAL": "bold_red",
            },
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)

        stream = stream_handler.stream
        if isinstance(stream, TextIOWrapper):
            try:
                stream.reconfigure(errors="replace")
            except Exception:
                pass
        elif hasattr(stream, "buffer"):
            try:
                stream_handler.stream = io.TextIOWrapper(
                    stream.buffer,
                    encoding="utf-8",
                    errors="replace",
                    line_buffering=True,
                )
            except Exception:
                pass

        logger.addHandler(stream_handler)

    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("urllib3.util.retry").setLevel(logging.WARNING)
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(
        logging.WARNING
    )
    logging.getLogger("requests.packages.urllib3.util.retry").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logger


logger = setup_logger()


# ─── EMAIL DISTRIBUTION LISTS ─────────────────────────────────────────────────
DEFAULT_CC_SPPI: list[str] = [
    "agnes.tri@sfi.co.id",
    "ardi.supriyono@sfi.co.id",
    "swacita.apriyanti@sfi.co.id",
    "rio.maulana@sfi.co.id",
    "hermawan.nugroho@sfi.co.id",
    "ugi.lugina@sfi.co.id",
]

DEFAULT_CC_MOKAS: list[str] = [
    "angelita.roma@sfi.co.id",
    "alfian.tejo@sfi.co.id",
    "aris.sumartono@sfi.co.id",
    "brian.yektibudi@sfi.co.id",
]


# ─── APPLICATION PATHS ────────────────────────────────────────────────────────
APPLICATION_PATHS = {
    "CHROME_PATH": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "OUTLOOK_PATH": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office 2013\\Outlook 2013.lnk",
}


# ─── FOLDER PATHS ─────────────────────────────────────────────────────────────
FOLDER_PATHS = {
    # SUBMISSION OUTLOOK
    "SUB_MOBCOLL_LOR": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Kunjungan_Mobcoll_LoR",
    "SUB_MOBCOLL_REGULER": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Kunjungan_Mobcoll",
    "SUB_MOBCOLL_MONITORING": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Monitoring_Mobcoll",
    "SUB_PENERIMAAN_ANGSURAN": rf"D:\Rahiel Hafizh\Submission\Outlook\Penerimaan_Angsuran",
    "SUB_PENERIMAAN_CASH_IN": rf"D:\Rahiel Hafizh\Submission\Outlook\Penerimaan_CashIn",
    "SUB_PENERIMAAN_DENDA_AKTIF": rf"D:\Rahiel Hafizh\Submission\Outlook\Penerimaan_Denda_Aktif",
    "SUB_PENERIMAAN_DENDA_ALDA": rf"D:\Rahiel Hafizh\Submission\Outlook\Penerimaan_Denda_Alda",
    "SUB_PERFORMANCE_AR_ASSET": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_AR_Remedial_Asset",
    "SUB_PERFORMANCE_AR_TOD": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_AR_TOD",
    "SUB_PERFORMANCE_BUCKET_CURRENT": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Bucket_Current",
    "SUB_PERFORMANCE_BUCKET_OVERDUE": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Bucket_Overdue",
    "SUB_PERFORMANCE_CWO_WO": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_CWO_WO_Estimasi_WO",
    "SUB_PERFORMANCE_PICKUP": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Update_Pickup",
    "SUB_PERFORMANCE_RECOVERY_WO": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Recovery_WO",
    "SUB_PERFORMANCE_STOPSELL": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Kunjungan_StopSell",
    "SUB_PROGRESS_FLOWRATE": rf"D:\Rahiel Hafizh\Submission\Outlook\Progress_Update_Flowrate",
    "SUB_PROGRESS_REDUCE_WO": rf"D:\Rahiel Hafizh\Submission\Outlook\Progress_Reduce_WO",
    # SUBMISSION WHATSAPP
    "SUB_WHATSAPP_MOBCOLL_LOR": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_Kunjungan_Mobcoll_LoR",
    "SUB_WHATSAPP_MOBCOLL_REGULER": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_Kunjungan_Mobcoll",
    "SUB_WHATSAPP_PENERIMAAN_CASH_IN": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Penerimaan_CashIn",
    "SUB_WHATSAPP_PENERIMAAN_DENDA_AKTIF": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Penerimaan_Denda_Aktif",
    "SUB_WHATSAPP_PENERIMAAN_DENDA_ALDA": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Penerimaan_Denda_Alda",
    "SUB_WHATSAPP_PERFORMANCE_AR_ASSET": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_AR_Remedial_Asset",
    "SUB_WHATSAPP_PERFORMANCE_AR_TOD": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_AR_TOD",
    "SUB_WHATSAPP_PERFORMANCE_BUCKET_CURRENT": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_Bucket_Current",
    "SUB_WHATSAPP_PERFORMANCE_BUCKET_OVERDUE": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_Bucket_Overdue",
    "SUB_WHATSAPP_PERFORMANCE_CWO_WO": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_CWO_WO_Estimasi_WO",
    "SUB_WHATSAPP_PERFORMANCE_PICKUP": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_Update_Pickup",
    "SUB_WHATSAPP_PERFORMANCE_RECOVERY_WO": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_Recovery_WO",
    "SUB_WHATSAPP_PERFORMANCE_STOPSELL": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Performance_Kunjungan_StopSell",
    "SUB_WHATSAPP_PROGRESS_FLOWRATE": rf"D:\Rahiel Hafizh\Submission\Whatsapp\Progress_Update_Flowrate",
    # WORKSOURCE FILE
    "WORKSOURCE_MOBCOLL_REGULER": rf"D:\Rahiel Hafizh\Submission\Outlook\Performance_Kunjungan_Mobcoll\Summary_Performance_Kunjungan_Mobcoll_Reguler.xlsx",
    "WORKSOURCE_MOBCOLL_LOR": rf"D:\Rahiel Hafizh\Source\Summary_Performance_Kunjungan_Mobcoll_LoR.xlsx",
    "WORKSOURCE_MOBCOLL_MONITORING": rf"D:\Rahiel Hafizh\Source\Summary_Performance_Monitoring_Mobcoll.xlsx",
    "WORKSOURCE_PENERIMAAN_ANGSURAN": rf"D:\Rahiel Hafizh\Source\Summary_Penerimaan_Angsuran.xlsx",
    "WORKSOURCE_PENERIMAAN_CASH_IN": rf"D:\Rahiel Hafizh\Source\Summary_Penerimaan_CashIn.xlsx",
    "WORKSOURCE_PENERIMAAN_DENDA_AKTIF": rf"D:\Rahiel Hafizh\Source\Summary_Penerimaan_Denda_Aktif.xlsx",
    "WORKSOURCE_PENERIMAAN_DENDA_ALDA": rf"D:\Rahiel Hafizh\Source\Summary_Penerimaan_Denda_Alda.xlsx",
    "WORKSOURCE_PERFORMANCE_AR_ASSET": rf"D:\Rahiel Hafizh\Source\Summary_Performance_AR_Remedial_Asset.xlsx",
    "WORKSOURCE_PERFORMANCE_AR_TOD": rf"D:\Rahiel Hafizh\Source\Summary_Performance_AR_TOD.xlsx",
    "WORKSOURCE_PERFORMANCE_BUCKET_CURRENT": rf"D:\Rahiel Hafizh\Source\Summary_Performance_Bucket_Current.xlsx",
    "WORKSOURCE_PERFORMANCE_BUCKET_OVERDUE": rf"D:\Rahiel Hafizh\Source\Summary_Performance_Bucket_Overdue.xlsx",
    "WORKSOURCE_PERFORMANCE_CWO_WO": rf"D:\Rahiel Hafizh\Source\Summary_Performance_CWO_WO_Estimasi_WO.xlsx",
    "WORKSOURCE_PERFORMANCE_PICKUP": rf"D:\Rahiel Hafizh\Source\Summary_Performance_Update_Pickup.xlsx",
    "WORKSOURCE_PERFORMANCE_RECOVERY_WO": rf"D:\Rahiel Hafizh\Source\Summary_Performance_Recovery_WO.xlsx",
    "WORKSOURCE_PERFORMANCE_STOPSELL": rf"D:\Rahiel Hafizh\Source\Summary_Performance_Kunjungan_StopSell.xlsx",
    "WORKSOURCE_PROGRESS_FLOWRATE": rf"D:\Rahiel Hafizh\Source\Summary_Progress_Update_Flowrate_Ori.xlsx",
    "WORKSOURCE_PROGRESS_REDUCE_WO": rf"D:\Rahiel Hafizh\Source\Summary_Progress_Reduce_WO.xlsx",
}


# ─── CONTACT INFORMATION ──────────────────────────────────────────────────────
CONTACT_INFO = {
    "ASSET_GROUP": "https://web.whatsapp.com/accept?code=KblwmcubP6g04LzqwooTYV",
    "ADMIN_PRIMARY": "+6281382427588",
    "PERSONAL_COO": "+6282311919875",
    "PERSONAL_ONE": "+6285893093275",
    "PERSONAL_TWO": "+6281299606260",
    "PERSONAL_THREE": "+6285781690029",
    "PERSONAL_FOUR": "+6281282426399",
    "PERSONAL_FIVE": "+628988171583",
}


# ─── TIMING CONFIGURATION ─────────────────────────────────────────────────────
WAIT_TIMES = {
    # MICROSECOND
    "HUNDRED_MICROSECOND": 0.0001,
    "TWO_HUNDRED_MICROSECOND": 0.0002,
    "FIVE_HUNDRED_MICROSECOND": 0.0005,
    # MILLISECOND
    "ONE_MILLISECOND": 0.001,
    "TWO_MILLISECOND": 0.002,
    "FIVE_MILLISECOND": 0.005,
    "TEN_MILLISECOND": 0.01,
    "TWENTY_MILLISECOND": 0.02,
    "FIFTY_MILLISECOND": 0.05,
    "HUNDRED_MILLISECOND": 0.1,
    "TWO_HUNDRED_MILLISECOND": 0.2,
    # SUB-SECOND
    "TENTH_SECOND": 0.1,
    "EIGHTH_SECOND": 0.125,
    "QUARTER_SECOND": 0.25,
    "THIRD_SECOND": 0.33,
    "HALF_SECOND": 0.5,
    "THREE_QUARTER_SECOND": 0.75,
    # STANDARD SECOND
    "ONE_SECOND": 1,
    "ONEHALF_SECOND": 1.5,
    "TWO_SECOND": 2,
    "TWOHALF_SECOND": 2.5,
    "THREE_SECOND": 3,
    "FOUR_SECOND": 4,
    "FIVE_SECOND": 5,
    "SIX_SECOND": 6,
    "SEVEN_SECOND": 7,
    "EIGHT_SECOND": 8,
    "NINE_SECOND": 9,
    "TEN_SECOND": 10,
    "TWELVE_SECOND": 12,
    "FIFTEEN_SECOND": 15,
    "EIGHTEEN_SECOND": 18,
    "TWENTY_SECOND": 20,
    "TWENTYFIVE_SECOND": 25,
    "THIRTY_SECOND": 30,
    "THIRTYFIVE_SECOND": 35,
    "FORTY_SECOND": 40,
    "FORTYFIVE_SECOND": 45,
    "FIFTY_SECOND": 50,
    "FIFTYFIVE_SECOND": 55,
    # MINUTE-BASED
    "ONE_MINUTE": 60,
    "ONEHALF_MINUTE": 90,
    "TWO_MINUTE": 120,
    "TWOHALF_MINUTE": 150,
    "THREE_MINUTE": 180,
    "THREEHALF_MINUTE": 210,
    "FOUR_MINUTE": 240,
    "FIVE_MINUTE": 300,
    "SIX_MINUTE": 360,
    "SEVEN_MINUTE": 420,
    "EIGHT_MINUTE": 480,
    "NINE_MINUTE": 540,
    "TEN_MINUTE": 600,
    "TWELVE_MINUTE": 720,
    "FIFTEEN_MINUTE": 900,
    "TWENTY_MINUTE": 1200,
    "TWENTYFIVE_MINUTE": 1500,
    "THIRTY_MINUTE": 1800,
    "THIRTYFIVE_MINUTE": 2100,
    "FORTY_MINUTE": 2400,
    "FORTYFIVE_MINUTE": 2700,
    "FIFTY_MINUTE": 3000,
    "FIFTYFIVE_MINUTE": 3300,
    "SIXTY_MINUTE": 3600,
}


# ─── PYAUTOGUI SETTINGS ───────────────────────────────────────────────────────
PYAUTOGUI_SETTINGS = {
    "FAILSAFE": False,
    "TRUE_CONDITION": True,
    "FALSE_CONDITION": False,
    "PAUSE": 0.1,
    "DURATION": 0.1,
    "INTERVAL": 0.05,
    "LOG_SCREENSHOTS": False,
    "SCREENSHOT_FOLDER": "screenshots",
    "MINIMUM_DURATION": 0.1,
    "MINIMUM_SLEEP": 0.05,
    "MAXIMUM_SLEEP": 2.0,
    "DEFAULT_PAUSE": 0.1,
    "DEFAULT_DURATION": 0.1,
    "DEFAULT_INTERVAL": 0.05,
}


# ─── LOCALIZATION MAPPING ─────────────────────────────────────────────────────
MONTHS_ID = {
    "January": "Januari",
    "February": "Februari",
    "March": "Maret",
    "April": "April",
    "May": "Mei",
    "June": "Juni",
    "July": "Juli",
    "August": "Agustus",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Desember",
}


# ─── AREA / BRANCH REFERENCE DATA ────────────────────────────────────────────
AREA_BRANCH_MAPPING: dict[str, list[str]] = {
    "IBT": [
        "DENPASAR",
        "MATARAM",
        "KUPANG",
    ],
    "JABODETABEKSER": [
        "KEDOYA",
        "SUNTER",
        "BEKASI",
        "TANGERANG",
        "BOGOR",
        "SERANG",
        "DEWI SARTIKA",
        "DEPOK",
    ],
    "JAWA BARAT": [
        "BANDUNG",
        "KARAWANG",
        "CIREBON",
    ],
    "JAWA TENGAH": [
        "YOGYAKARTA",
        "SEMARANG",
        "KUDUS",
        "PURWOKERTO",
        "TEGAL",
        "SOLO",
    ],
    "JAWA TIMUR": [
        "SURABAYA",
        "MALANG",
        "GRESIK",
        "KEDIRI",
    ],
    "KALIMANTAN": [
        "SAMARINDA",
        "BANJARMASIN",
        "BALIKPAPAN",
        "PALANGKARAYA",
        "BARABAI",
        "SAMPIT",
        "PONTIANAK",
    ],
    "SULAWESI": [
        "MAKASSAR",
        "MANADO",
        "GORONTALO",
        "PALU",
        "KENDARI",
        "TERNATE",
    ],
    "SUMBAGSEL": [
        "PALEMBANG",
        "LAMPUNG",
        "PANGKAL PINANG",
        "JAMBI",
    ],
    "SUMBAGUTENG": [
        "PEKANBARU",
        "MEDAN",
        "BATAM",
        "PADANG",
    ],
}

BRANCH_ORDER: list[str] = [
    "BALIKPAPAN",
    "BANDAR LAMPUNG",
    "BANDUNG",
    "BANJARMASIN",
    "BATAM",
    "BEKASI",
    "BOGOR",
    "CIREBON",
    "DENPASAR",
    "DEPOK",
    "DEWI SARTIKA",
    "GORONTALO",
    "GRESIK",
    "JAMBI",
    "KARAWANG",
    "KEDIRI",
    "KEDOYA",
    "KENDARI",
    "KUDUS",
    "KUPANG",
    "MAKASSAR",
    "MALANG",
    "MANADO",
    "MATARAM",
    "MEDAN",
    "PALANGKARAYA",
    "PALEMBANG",
    "PALU",
    "PANGKAL PINANG",
    "PEKANBARU",
    "PONTIANAK",
    "PURWOKERTO",
    "SAMARINDA",
    "SAMPIT",
    "SEMARANG",
    "SERANG",
    "SOLO",
    "SUNTER",
    "SURABAYA",
    "TANGERANG",
    "TEGAL",
    "TERNATE",
    "YOGYAKARTA",
]


# ─── CERTIFICATION FILTER CONFIGURATION ──────────────────────────────────────
CERTIFICATION_FILTER_PRESETS: dict[str, Any] = {
    "NEXT_MONTH": {"MODE": "NEXT_MONTH"},
    "TWO_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 2},
    "THREE_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 3},
    "FOUR_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 4},
    "FIVE_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 5},
    "SIX_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 6},
    "SEVEN_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 7},
    "EIGHT_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 8},
    "NINE_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 9},
    "TEN_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 10},
    "ELEVEN_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 11},
    "ONE_YEAR": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 12},
    "THIRTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 30},
    "SIXTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 60},
    "NINETY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 90},
    "ONE_HUNDRED_TWENTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 120},
    "ONE_HUNDRED_EIGHTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 180},
    "CUSTOM_DATE_RANGE": {
        "MODE": "SPECIFIC_DATE_RANGE",
        "START_DATE": None,
        "END_DATE": None,
    },
}

CERTIFICATION_FILTER_CONFIG: dict[str, Any] = {
    "ACTIVE_PRESET": "NEXT_MONTH",
    "CUSTOM_CONFIG": None,
}


# ─── WHATSAPP UI SETTINGS ─────────────────────────────────────────────────────
WHATSAPP_SETTINGS = {
    "INPUT_X": 800,
    "INPUT_Y": 820,
}


# ─── DEFAULT CONFIGURATION REGISTRY ──────────────────────────────────────────
DEFAULT_CONFIG = {
    **APPLICATION_PATHS,
    **FOLDER_PATHS,
    **CONTACT_INFO,
    "WAIT_TIME": WAIT_TIMES,
    "PYAUTOGUI": PYAUTOGUI_SETTINGS,
    "WHATSAPP": WHATSAPP_SETTINGS,
    "MONTHS_ID": MONTHS_ID,
    "AREA_BRANCH_MAPPING": AREA_BRANCH_MAPPING,
    "BRANCH_ORDER": BRANCH_ORDER,
    "CERTIFICATION_FILTER_PRESETS": CERTIFICATION_FILTER_PRESETS,
    "CERTIFICATION_FILTER_CONFIG": CERTIFICATION_FILTER_CONFIG,
}


# ─── PYAUTOGUI INITIALISATION ─────────────────────────────────────────────────
def setup_pyautogui_config() -> None:
    global _pyautogui_configured
    if _pyautogui_configured:
        return

    try:
        pyautogui.FAILSAFE = PYAUTOGUI_SETTINGS["FAILSAFE"]
        pyautogui.PAUSE = PYAUTOGUI_SETTINGS["PAUSE"]
        _pyautogui_configured = True
    except Exception as e:
        logger.error(f"[SYSTEM] FAILED TO CONFIGURE PYAUTOGUI: {e}")
        raise


# ─── CONFIGURATION LOADER ─────────────────────────────────────────────────────
def load_config() -> dict[str, Any]:
    setup_pyautogui_config()
    return DEFAULT_CONFIG


# ─── TIMER UTILITIES ──────────────────────────────────────────────────────────
def wait_timer(base_time: float) -> None:
    if base_time < 0:
        logger.warning(f"[TIMER] INVALID NEGATIVE VALUE: {base_time}")
        return
    time.sleep(base_time)


# ─── CONFIGURATION ACCESSORS ──────────────────────────────────────────────────
def get_config_value(key: str, default: Any = None) -> Any:
    config = DEFAULT_CONFIG
    keys = key.split(".")

    try:
        for k in keys:
            config = config[k]
        return config
    except (KeyError, TypeError):
        logger.warning(f"[CONFIG] KEY NOT FOUND: {key}")
        return default


def get_wait_time(time_key: str, default: float = 1.0) -> float:
    return WAIT_TIMES.get(time_key, default)


def get_pyautogui_setting(setting_name: str, default: Any = None) -> Any:
    return PYAUTOGUI_SETTINGS.get(setting_name, default)


def get_month_id(english_month: str, case: str = "as-is") -> str:
    indonesian_month = MONTHS_ID.get(english_month, english_month)

    if case == "upper":
        return indonesian_month.upper()
    elif case == "lower":
        return indonesian_month.lower()
    elif case == "title":
        return indonesian_month.title()
    return indonesian_month


# ─── AREA / BRANCH ACCESSORS ─────────────────────────────────────────────────
def area_branch_mapping() -> dict[str, list[str]]:
    return AREA_BRANCH_MAPPING.copy()


def get_branch_order() -> list[str]:
    return BRANCH_ORDER.copy()


# ─── CERTIFICATION FILTER ACCESSORS ──────────────────────────────────────────
_VALID_FILTER_MODES = {
    "NEXT_MONTH",
    "NEXT_N_MONTHS",
    "DAYS_RANGE",
    "SPECIFIC_DATE_RANGE",
}


def get_certification_filter_config(preset: Optional[str] = None) -> dict[str, Any]:
    if CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"] is not None:
        logger.info("[CONFIG] USING CUSTOM FILTER CONFIGURATION")
        return CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"]

    active_preset = preset or CERTIFICATION_FILTER_CONFIG["ACTIVE_PRESET"]

    if active_preset in CERTIFICATION_FILTER_PRESETS:
        logger.info(f"[CONFIG] USING FILTER PRESET: {active_preset}")
        return CERTIFICATION_FILTER_PRESETS[active_preset].copy()

    logger.warning(
        f"[CONFIG] UNKNOWN PRESET '{active_preset}' — FALLING BACK TO NEXT_MONTH"
    )
    return CERTIFICATION_FILTER_PRESETS["NEXT_MONTH"].copy()


def set_certification_filter_preset(preset: str) -> bool:
    if preset not in CERTIFICATION_FILTER_PRESETS:
        logger.error(f"[CONFIG] INVALID PRESET NAME: {preset}")
        return False

    CERTIFICATION_FILTER_CONFIG["ACTIVE_PRESET"] = preset
    CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"] = None
    logger.info(f"[CONFIG] FILTER PRESET SET TO: {preset}")
    return True


def set_custom_certification_filter(custom_config: dict[str, Any]) -> bool:
    mode = custom_config.get("MODE")

    if mode not in _VALID_FILTER_MODES:
        logger.error(f"[CONFIG] INVALID MODE IN CUSTOM FILTER: {mode}")
        return False

    CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"] = custom_config
    logger.info("[CONFIG] CUSTOM FILTER CONFIGURATION APPLIED")
    return True
