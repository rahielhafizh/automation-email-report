import math
import time
import pyautogui
from pynput.keyboard import Controller, Key
from services.config import load_config, logger, wait_timer

CONFIG = load_config()
FIGURE_EIGHT_CONFIG = {"RADIUS_X": 250, "RADIUS_Y": 200, "TOTAL_DURATION": 5.0}

pynputKeyboard = Controller()


def adjust_picture_size() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] ADJUST IMAGE WIDTH VIA ALT MENU")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("w")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.write("70")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def blank_mail_space() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] INSERT BLANK SPACE IN EMAIL BODY")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def break_excel_link() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CONVERT LINKED EXCEL FILE TO STATIC VALUES")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("k")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("tab", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("left")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def capture_table_as_bitmap() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CAPTURE TABLE TO BITMAP FORMAT")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("down")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def capture_table_as_picture() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CAPTURE TABLE TO PICTURE FORMAT")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def capture_table_as_table() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CAPTURE TABLE AS TABLE FORMAT")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def choose_file_attach() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] LAUNCH FILE ATTACHMENT DIALOG")
    pyautogui.hotkey("alt", "n")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("f")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def close_unsave() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CLOSE WORKBOOK WITHOUT SAVING")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])


def closing_tab() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CLOSE ACTIVE WINDOW")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def confirm() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CONFIRMATION ACTION")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def confirm_file_attach() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CONFIRM FILE ATTACHMENT")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("tab", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def convert_to_range() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CONVERT TO STANDARD CELL RANGE")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j", "t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("g")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def creating_new_task() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CREATE NEW TASK")
    pyautogui.hotkey("ctrl", "n")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def define_center() -> tuple[int, int]:
    screen_width, screen_height = pyautogui.size()
    return screen_width // 2, screen_height // 2


def entering_operation() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] PRESSING ENTER KEY TO HANDLE OPERATION DIALOG")
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def escaping() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def finish_outlook() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SEND EMAIL AND CLOSE OUTLOOK")
    pyautogui.hotkey("alt", "s")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def handle_breaklink_process() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.PAUSE = 0
    center_x, center_y = define_center()
    moving_process(
        center_x,
        center_y,
        FIGURE_EIGHT_CONFIG["RADIUS_X"],
        FIGURE_EIGHT_CONFIG["RADIUS_Y"],
        FIGURE_EIGHT_CONFIG["TOTAL_DURATION"],
    )

    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])

    moving_process(
        center_x,
        center_y,
        FIGURE_EIGHT_CONFIG["RADIUS_X"],
        FIGURE_EIGHT_CONFIG["RADIUS_Y"],
        FIGURE_EIGHT_CONFIG["TOTAL_DURATION"],
    )

    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def handle_move_copy_process() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.PAUSE = 0
    center_x, center_y = define_center()
    moving_process(
        center_x,
        center_y,
        FIGURE_EIGHT_CONFIG["RADIUS_X"],
        FIGURE_EIGHT_CONFIG["RADIUS_Y"],
        FIGURE_EIGHT_CONFIG["TOTAL_DURATION"],
    )

    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.press("left")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.press("right")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])

    moving_process(
        center_x,
        center_y,
        FIGURE_EIGHT_CONFIG["RADIUS_X"],
        FIGURE_EIGHT_CONFIG["RADIUS_Y"],
        FIGURE_EIGHT_CONFIG["TOTAL_DURATION"],
    )

    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def handle_office() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] HANDLING OFFICE STARTUP DIALOGS")
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def handle_refresh_process() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    logger.info("[SYSTEM] HANDLING EXCEL RECALCULATION PROCESS")
    move_cursor_figure_eight()
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    switch_to_first_cells()
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    move_cell_vertical()
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def input_clipboard_picture() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] INSERT CLIPBOARD IMAGE")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def input_dynamic_picture() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] PASTE IMAGE THEN FORMAT")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def input_hyperlink() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] OPEN HYPERLINK DIALOG")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("n")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("i")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def make_important_mail() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] MARK EMAIL AS HIGH IMPORTANCE")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("h")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def make_new_pivot_sheet() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CREATE NEW PIVOT TABLE SHEET")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("n")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def maximize_app_window() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] MAXIMIZE WINDOW TO FULLSCREEN")
    pyautogui.hotkey("win", "up")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def minimize_outlook() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SEND EMAIL AND MINIMIZE OUTLOOK")
    pyautogui.hotkey("alt", "s")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("win", "m")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def minimize_text() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] REDUCE FONT SIZE")
    for _ in range(2):
        pyautogui.hotkey("alt")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        pyautogui.hotkey("h")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        pyautogui.hotkey("f")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        pyautogui.hotkey("k")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def move_cell_horizontal() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] MOVE CELL TO KEEP SCREEN ACTIVE")
    pyautogui.hotkey("ctrl", "right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def move_cell_vertical() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    logger.info("[DATA] NAVIGATING CELLS VERTICALLY TO STAY ACTIVE")
    for _ in range(3):
        pyautogui.hotkey("ctrl", "down")
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    for _ in range(5):
        pyautogui.hotkey("ctrl", "up")
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def move_cursor_figure_eight() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.PAUSE = 0
    center_x, center_y = define_center()

    moving_process(
        center_x,
        center_y,
        FIGURE_EIGHT_CONFIG["RADIUS_X"],
        FIGURE_EIGHT_CONFIG["RADIUS_Y"],
        FIGURE_EIGHT_CONFIG["TOTAL_DURATION"],
    )

    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.click()
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])

    moving_process(
        center_x,
        center_y,
        FIGURE_EIGHT_CONFIG["RADIUS_X"],
        FIGURE_EIGHT_CONFIG["RADIUS_Y"],
        FIGURE_EIGHT_CONFIG["TOTAL_DURATION"],
    )

    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def move_or_copy_as_newbook() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] COPY SHEET TO NEW WORKBOOK")
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("tab", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("up", presses=5)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("tab", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def move_or_copy_menu() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] OPEN MOVE OR COPY DIALOG")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("e")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("m")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def moving_process(
    center_x: int,
    center_y: int,
    radius_x: int | float,
    radius_y: int | float,
    total_duration: float,
) -> None:
    start_time = time.perf_counter()
    while True:
        elapsed = time.perf_counter() - start_time
        if elapsed >= total_duration:
            return

        progress = (elapsed / total_duration) * (2 * math.pi)
        x = center_x + radius_x * math.sin(progress)
        y = center_y + radius_y * math.sin(2 * progress) / 2
        pyautogui.moveTo(x, y, duration=0)


def paste_value_as_value() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] PASTE AS VALUES ONLY")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def refresh_excel_data() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] REFRESH ALL DATA CONNECTIONS")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("r")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_as_in() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] OPEN SAVE AS DIALOG")
    pyautogui.hotkey("f12")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_as_name() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATE TO FILENAME FIELD")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_file() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] SAVE CURRENT DOCUMENT")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_new_book() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] SAVE NEW WORKBOOK")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("tab", presses=2)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_new_copy() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] SAVE FILE WITH NEW NAME")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def scroller_page(scroll_amount: int = 500) -> None:
    if not isinstance(scroll_amount, int):
        raise TypeError("scroll_amount must be integer")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.PAUSE = 0
    pyautogui.scroll(scroll_amount)

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.scroll(-scroll_amount)

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_header_content() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    logger.info("[SYSTEM] SELECT HEADER CONTENT")
    for _ in range(5):
        pynputKeyboard.press(Key.shift)
        pynputKeyboard.press(Key.up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.shift)
        pynputKeyboard.release(Key.up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_hyperlink() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SELECT HYPERLINK TEXT")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pynputKeyboard.press(Key.shift)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pynputKeyboard.press(Key.up)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pynputKeyboard.release(Key.shift)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pynputKeyboard.release(Key.up)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_sheet_down() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION DOWNWARD")
    for _ in range(15):
        pynputKeyboard.press(Key.ctrl)
        pynputKeyboard.press(Key.shift)
        pynputKeyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.page_down)
        pynputKeyboard.release(Key.shift)
        pynputKeyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_sheet_half_down() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION DOWNWARD PARTIAL")
    for _ in range(5):
        pynputKeyboard.press(Key.ctrl)
        pynputKeyboard.press(Key.shift)
        pynputKeyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.page_down)
        pynputKeyboard.release(Key.shift)
        pynputKeyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_sheet_half_up() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION UPWARD PARTIAL")
    for _ in range(5):
        pynputKeyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.press(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_sheet_order_in() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SELECT WORKSHEETS FOR REPORT")
    for _ in range(2):
        pynputKeyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_sheet_up() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION UPWARD")
    for _ in range(10):
        pynputKeyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.press(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pynputKeyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def set_new_book_name() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CLEAR FILENAME FOR INPUT")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def set_new_pivot_sheet() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CONFIGURE PIVOT TABLE LAYOUT")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("l")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("l")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("up", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def set_text_right() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] APPLY RIGHT TEXT ALIGNMENT")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("r")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def switch_to_first_cells() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATE TO FIRST CELLS")
    for _ in range(5):
        pyautogui.hotkey("ctrl", "up")
    for _ in range(5):
        pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def switch_to_first_sheet() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SWITCH TO FIRST SHEET")
    for _ in range(15):
        pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def switch_to_last_sheet() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SWITCH TO LAST SHEET")
    for _ in range(15):
        pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def switch_to_left_sheet() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SWITCH TO PREVIOUS SHEET")
    pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def switch_to_right_sheet() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SWITCH TO NEXT SHEET")
    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def switch_to_table_cells() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATE TO TABLE CELLS")
    pyautogui.press("down", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("right", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])