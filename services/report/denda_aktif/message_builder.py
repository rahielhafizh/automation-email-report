from services.message_formatter import ReportTimestamp


def build_denda_aktif_message(ts: ReportTimestamp) -> str:
    return f"REPORT DENDA AKTIF | {ts.date_upper} | {ts.time_str}"
