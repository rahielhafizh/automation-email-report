from services.message_formatter import ReportTimestamp


def build_area_message(ts: ReportTimestamp) -> str:
    return f"MOBCOLL REPORT LOR | {ts.date_upper} | REPORT AREA"


def build_as_of_message(ts: ReportTimestamp) -> str:
    return f"AS OF REPORT LOR | 1 s/d {ts.date_upper} | AREA DAN CABANG"


def build_today_message(ts: ReportTimestamp) -> str:
    return f"TODAY REPORT LOR | {ts.date_upper} | AREA DAN CABANG"
