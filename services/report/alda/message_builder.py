from services.message_formatter import ReportTimestamp


def build_alda_message(ts: ReportTimestamp) -> str:
    return f"REPORT ALDA | {ts.date_upper} | {ts.time_str}"
