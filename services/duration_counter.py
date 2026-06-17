import time
import datetime
from services.config import logger

_start_time: float | None = None
_end_time: float | None = None
_on_going: bool = False


def start_counter() -> float:
    global _start_time, _on_going
    _start_time = time.time()
    _on_going = True
    logger.warning(
        f"[SYSTEM] TIMER START AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return _start_time


def stop_counter() -> float | None:
    global _end_time, _on_going
    if not _on_going:
        logger.error("[ERROR] TIMER NOT STARTED")
        return None
    _end_time = time.time()
    _on_going = False
    logger.warning(
        f"[SYSTEM] TIMER STOP AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return _end_time


def get_execution_duration(format_output: bool = True) -> str | float | None:
    global _start_time, _end_time
    if _start_time is None:
        logger.error("[ERROR] TIMER NOT STARTED, DURATION UNAVAILABLE")
        return None
    execution_seconds = (time.time() if _end_time is None else _end_time) - _start_time
    if format_output:
        hours, remainder = divmod(execution_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return execution_seconds


def log_counter_execution(process_name: str | None = None) -> str:
    execution_time = get_execution_duration()
    process_str = f" FOR {process_name.upper()}" if process_name else ""
    log_message = f"[SYSTEM] TOTAL EXECUTION TIME{process_str} : {execution_time}"
    logger.info(log_message)
    return log_message


def reset_timer() -> None:
    global _start_time, _end_time, _on_going
    _start_time = None
    _end_time = None
    _on_going = False
    logger.debug("[SYSTEM] TIMER RESET")


def check_running_timer() -> bool:
    return _on_going


class ExecutionTimer:
    def __init__(self, process_name: str | None = None) -> None:
        self.process_name = process_name

    def __enter__(self) -> "ExecutionTimer":
        start_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        stop_counter()
        log_counter_execution(self.process_name)
        return False
