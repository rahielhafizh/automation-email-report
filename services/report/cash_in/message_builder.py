from services.message_formatter import ReportTimestamp


def build_cash_in_message(ts: ReportTimestamp) -> str:
    return f"Update Cash In - {ts.date_title} Pukul : {ts.time_str}"
