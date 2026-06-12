import pyodbc
from datetime import date, datetime, timedelta
from services.config import load_config, logger
from services.database import get_database_connection
from typing import Optional, Tuple

CONFIG = load_config()

Dashboard_Control = "[dbo].[Dashboard_Control]"

fetching_query = f"""
    SELECT TOP 1
        [RunningReportDate],
        [Periode Update]
    FROM {Dashboard_Control}
    WHERE [RunningReportDate] IS NOT NULL
    ORDER BY [RunningReportDate] DESC
"""


def parse_running_report_date(raw_value) -> Optional[date]:
    if raw_value is None:
        return None

    if isinstance(raw_value, (datetime, date)):
        return raw_value.date() if isinstance(raw_value, datetime) else raw_value

    raw_str = str(raw_value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw_str, fmt).date()
        except ValueError:
            continue

    logger.warning(f"[INFO] UNRECOGNISED REPORT DATE FORMAT: {raw_str!r}")
    return None


def parsing_update_time(raw_value) -> Optional[datetime]:
    if raw_value is None:
        return None

    if isinstance(raw_value, datetime):
        return raw_value

    raw_str = str(raw_value).strip()
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(raw_str, fmt)
        except ValueError:
            continue

    logger.warning(f"[INFO] UNRECOGNISED UPDATE TIME FORMAT : {raw_str!r}")
    return None


def fetching_report_date(
    conn: Optional[pyodbc.Connection] = None,
) -> Tuple[Optional[date], Optional[datetime]]:
    logger.info("[INFO] FETCHING DASHBOARD CONTROL DATA")

    _shared_conn = conn is not None
    target = conn

    try:
        if not _shared_conn:
            target = get_database_connection()
            if target is None:
                logger.error("[INFO] DATABASE CONNECTION UNAVAILABLE")
                return None, None

        cursor = target.cursor()
        cursor.execute(fetching_query)
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            logger.warning("[INFO] NO ROWS RETURNED")
            return None, None

        running_report_date = parse_running_report_date(row[0])
        periode_update = parsing_update_time(row[1])

        logger.info(
            f"[INFO] REPORT DATE  : {running_report_date} | "
            f"UPDATE TIME : {periode_update}"
        )
        return running_report_date, periode_update

    except Exception as e:
        logger.error(f"[INFO] FETCH FAILED: {e}")
        return None, None

    finally:
        if not _shared_conn and target is not None:
            try:
                target.close()
            except Exception:
                pass


def validating_report_date(running_report_date: Optional[date]) -> bool:
    if running_report_date is None:
        return False

    yesterday = date.today() - timedelta(days=1)
    result = running_report_date == yesterday

    logger.info(f"[INFO] VALIDATION — REPORT DATE : {running_report_date} | ")
    return result


def check_flowrate_status(
    conn: Optional[pyodbc.Connection] = None,
) -> Tuple[bool, Optional[date], Optional[datetime]]:
    running_report_date, periode_update = fetching_report_date(conn=conn)
    result = validating_report_date(running_report_date)

    if result:
        logger.info("[INFO] STATUS: VALID REPORT DATE")
    else:
        logger.warning("[INFO] STATUS: INVALID REPORT DATE")

    return result, running_report_date, periode_update


if __name__ == "__main__":
    result, rrd, periode = check_flowrate_status()
    print(f"Valid     : {result}")
    print(f"RunningReportDate : {rrd}")
    print(f"Periode Update    : {periode}")
