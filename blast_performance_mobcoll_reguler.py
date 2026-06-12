import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass
from mail.outlook_performance_mobcoll_reguler import *
from general_task import *
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from services.duration_counter import start_counter, stop_counter, start_counter_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

# ───────── RUNTIME INITIALISATION
CONFIG = load_config()


# ───────── VALIDATION MODELS
class ExcelConfig:
    TARGET_SHEET_NAME = "TABLE"
    DATETIME_CELLS = {"K2": "K-2"}


@dataclass
class DateTimeValidationResult:
    cell_address: str
    expected_date: datetime
    actual_value: str
    is_valid: bool
    error_message: str = ""


# ───────── VALIDATOR
class PicDateTimeValidatorMail:
    def __init__(self, config: Dict):
        self.config = config

    def get_expected_date(self) -> datetime:
        return datetime.combine(datetime.now().date(), datetime.min.time())

    def load_pic_sheet(self, file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"EXCEL FILE NOT FOUND: {file_path}")

        try:
            return pd.read_excel(
                file_path,
                sheet_name=ExcelConfig.TARGET_SHEET_NAME,
                header=None,
            )
        except ValueError as exc:
            if "Worksheet named" in str(exc):
                raise ValueError(
                    f"SHEET '{ExcelConfig.TARGET_SHEET_NAME}' NOT FOUND IN FILE"
                )
            raise
        except Exception as exc:
            raise RuntimeError(f"FAILED TO READ EXCEL FILE: {exc}")

    def excel_col_to_index(self, col_name: str) -> int:
        result = 0
        for char in col_name:
            result = result * 26 + (ord(char.upper()) - ord("A") + 1)
        return result - 1

    def parse_cell_value_as_datetime(self, value) -> Optional[datetime]:
        if pd.isna(value):
            return None

        if isinstance(value, datetime):
            return value

        if hasattr(value, "to_pydatetime"):
            return value.to_pydatetime()

        if isinstance(value, str):
            datetime_formats = [
                "%d/%m/%Y %H:%M:%S",
                "%d/%m/%Y  %H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%d-%m-%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M",
                "%Y-%m-%d %H:%M",
                "%d-%m-%Y %H:%M",
                "%m/%d/%Y %H:%M",
                "%d/%m/%Y",
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%m/%d/%Y",
            ]
            for fmt in datetime_formats:
                try:
                    return datetime.strptime(value.strip(), fmt)
                except ValueError:
                    continue

        if isinstance(value, (int, float)):
            try:
                excel_epoch = datetime(1900, 1, 1)
                adjusted = float(value) - (2 if value > 59 else 1)
                return excel_epoch + timedelta(days=adjusted)
            except (ValueError, OverflowError):
                pass

        return None

    def validate_cell_datetime(
        self,
        df: pd.DataFrame,
        cell_address: str,
        expected_date: datetime,
    ) -> DateTimeValidationResult:
        try:
            col_part = "".join(filter(str.isalpha, cell_address))
            row_part = "".join(filter(str.isdigit, cell_address))
            col_idx = self.excel_col_to_index(col_part)
            row_idx = int(row_part) - 1

            if row_idx >= len(df) or col_idx >= len(df.columns):
                return DateTimeValidationResult(
                    cell_address,
                    expected_date,
                    "NOT_FOUND",
                    False,
                    f"CELL {cell_address} OUT OF RANGE",
                )

            cell_value = df.iloc[row_idx, col_idx]
            actual_datetime = self.parse_cell_value_as_datetime(cell_value)
            actual_value_str = (
                actual_datetime.strftime("%d/%m/%Y %H:%M:%S")
                if actual_datetime
                else (str(cell_value) if not pd.isna(cell_value) else "EMPTY")
            )

            if not actual_datetime:
                return DateTimeValidationResult(
                    cell_address,
                    expected_date,
                    actual_value_str,
                    False,
                    f"INVALID DATETIME IN {cell_address}",
                )

            is_valid = actual_datetime.date() == expected_date.date()
            return DateTimeValidationResult(
                cell_address,
                expected_date,
                actual_value_str,
                is_valid,
                (
                    ""
                    if is_valid
                    else f"DATE MISMATCH IN {cell_address} — NOT TODAY'S DATE"
                ),
            )

        except Exception as exc:
            return DateTimeValidationResult(
                cell_address,
                expected_date,
                "ERROR",
                False,
                f"ERROR VALIDATING {cell_address}: {exc}",
            )

    def validate_pic_datetime(self, file_path: str) -> List[DateTimeValidationResult]:
        df = self.load_pic_sheet(file_path)
        expected_date = self.get_expected_date()
        cell_address = "K2"
        result = self.validate_cell_datetime(df, cell_address, expected_date)

        if result.is_valid:
            logger.info(f"[DATA] CELL {cell_address} VALIDATED SUCCESSFULLY")
        else:
            logger.error(f"[ERROR] {result.error_message}")

        return [result]

    def is_data_valid(self, validation_results: List[DateTimeValidationResult]) -> bool:
        return all(result.is_valid for result in validation_results)


# ───────── VALIDATION HELPERS
def _validate_pic_data(file_path: Optional[str] = None) -> bool:
    try:
        target_file = file_path or CONFIG["WORKSOURCE_MOBCOLL_REGULER"]
        logger.info(f"[SYSTEM] VALIDATING MOBCOLL REGULER : {target_file}")

        if not os.path.exists(target_file):
            logger.error(f"[ERROR] {target_file} NOT FOUND")
            return False

        validator = PicDateTimeValidatorMail(CONFIG)
        results = validator.validate_pic_datetime(target_file)
        is_valid = validator.is_data_valid(results)

        if is_valid:
            logger.info("[DATA] MOBCOLL REGULER VALID")
            return True

        for result in results:
            if not result.is_valid:
                logger.warning(f"[VALIDATION] {result.error_message}")

        return False

    except Exception as exc:
        logger.error(f"[ERROR] MOBCOLL REGULER VALIDATION FAILED: {exc}")
        return False


def _get_pic_validation_details(file_path: Optional[str] = None) -> Dict:
    target_file = file_path or CONFIG["WORKSOURCE_MOBCOLL_REGULER"]
    try:
        validator = PicDateTimeValidatorMail(CONFIG)
        results = validator.validate_pic_datetime(target_file)

        return {
            "file_path": target_file,
            "validation_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "expected_date": datetime.now().date().strftime("%d/%m/%Y"),
            "is_valid": validator.is_data_valid(results),
            "results": [
                {
                    "cell": r.cell_address,
                    "expected": r.expected_date.strftime("%d/%m/%Y"),
                    "actual": r.actual_value,
                    "valid": r.is_valid,
                    "error": r.error_message,
                }
                for r in results
            ],
        }

    except Exception as exc:
        return {
            "file_path": target_file,
            "validation_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "error": str(exc),
            "is_valid": False,
        }


# ───────── CORE WORKFLOW
def excel_config():
    logger.info("[SYSTEM] MOBCOLL REGULER EXCEL WORKFLOW")

    os.startfile(CONFIG["WORKSOURCE_MOBCOLL_REGULER"])
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    entering_operation()
    switch_to_first_cells()

    switch_to_right_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()

    switch_to_first_cells()
    switch_to_first_sheet()
    switch_to_first_cells()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def send_email():
    outlook_recipients = ["herberth.simbolon@sfi.co.id"]
    secondary_recipients = ["collho.3@sfi.co.id", "asset.mgmt@sfi.co.id"]
    today = datetime.now()
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = (
        f"Summary Penugasan & Kunjungan Mobcoll Reguler | "
        f"{today.strftime('%d')} {month_idn_title} ({today.strftime('%H:%M')})"
    )

    core_email = (
        f"Yth. Bapak Chief of Operating Officer,\n\n"
        f"Dengan hormat,\n\n"
        f"Berikut terlampir laporan aktivitas PIC yang telah dilaksanakan pada "
        f"{today.strftime('%d')} {month_idn_title} pukul {today.strftime('%H:%M')} WIB.\n\n"
        f"Catatan\n"
        f"- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.\n"
        f"Seluruh data diperoleh secara real-time namun harap diperhatikan dan dievaluasi kembali.\n"
    )

    footer_template = (
        "\n\nHormat kami,\n"
        "Asset Management Division.\n"
        "Collection HO - PT Suzuki Finance Indonesia.\n"
    )

    try:
        send_outlook_email(
            outlook_recipients,
            secondary_recipients,
            subject_email,
            core_email,
            footer_template,
        )
    except Exception as exc:
        logger.error(f"[ERROR] FAILED TO SEND EMAIL: {exc}")
        raise

    logger.info("[DATA] MOBCOLL REGULER REPORT SENT")


def validate_and_send_email() -> bool:
    is_valid = _validate_pic_data()

    if is_valid:
        logger.info("[VALIDATION] MOBCOLL REGULER DATA SUCCESS")
        send_email()
        return True

    logger.warning("[VALIDATION] MOBCOLL REGULER DATA FAILED")
    details = _get_pic_validation_details()

    if "results" in details:
        for result in details["results"]:
            if not result["valid"]:
                logger.warning(f"[WARNING] CELL {result['cell']} — {result['error']}")

    return False


# ───────── ENTRY POINT
if __name__ == "__main__":
    logger.info("[SYSTEM] START MOBCOLL REGULER REPORT")

    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    email_sent = validate_and_send_email()

    if email_sent:
        logger.info("[SYSTEM] MOBCOLL REGULER REPORT SENT")
    else:
        logger.warning("[SYSTEM] MOBCOLL REGULER REPORT FAILED")

    stop_counter()
    execution_time = start_counter_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
