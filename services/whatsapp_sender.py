import pyautogui
import pyperclip
import pywhatkit as kit
import webbrowser
from typing import Optional
from services.config import load_config, wait_timer, logger
from services.chrome_checker import open_chrome

CONFIG = load_config()


def number_formatter(phone_no: str) -> Optional[str]:
    if not phone_no or phone_no == "0":
        return None

    phone_no = phone_no.strip()
    if len(phone_no) < 5:
        return None

    if phone_no.startswith("0"):
        return "+62" + phone_no[1:]

    if not phone_no.startswith("+"):
        return "+" + phone_no

    return phone_no


def validate_group_link(group_link: str) -> Optional[str]:
    if not group_link:
        return None

    group_link = group_link.strip()
    valid_prefixes = [
        "https://chat.whatsapp.com/",
        "https://web.whatsapp.com/accept?code=",
        "https://wa.me/",
    ]

    if not any(group_link.startswith(prefix) for prefix in valid_prefixes):
        logger.error(f"[ERROR] INVALID WHATSAPP LINK FORMAT: {group_link}")
        return None

    return group_link


def click_whatsapp() -> None:
    input_x = CONFIG["WHATSAPP"]["INPUT_X"]
    input_y = CONFIG["WHATSAPP"]["INPUT_Y"]
    logger.info(f"[SYSTEM] CLICKING WHATSAPP INPUT AT X: {input_x}, Y: {input_y}")
    pyautogui.click(input_x, input_y)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def cleanup_report_preparation() -> None:
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def closing_whatsapp_tab() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "w")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])


def send_to_group(group_link: str, message: str = "") -> bool:
    try:
        open_chrome()
        validated_link = validate_group_link(group_link)
        if not validated_link:
            raise ValueError("INVALID LINK FORMAT")

        webbrowser.open(validated_link)
        wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])

        click_whatsapp()
        cleanup_report_preparation()

        if message:
            pyautogui.typewrite(message)
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.hotkey("ctrl", "v")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        closing_whatsapp_tab()
        logger.info("[SYSTEM] MESSAGE SUCCESSFULLY SENT TO GROUP")
        return True

    except Exception as e:
        logger.error(f"[ERROR] GROUP MESSAGE SEND FAILURE: {str(e)}")
        raise


def send_whatsapp_report(phone_no: str, message: str) -> bool:
    try:
        open_chrome()
        formatted_no = number_formatter(phone_no)
        if not formatted_no:
            raise ValueError(f"INVALID PHONE NUMBER: {phone_no}")

        logger.info(f"[SYSTEM] INITIATING MESSAGE TO {formatted_no}")

        kit.sendwhatmsg_instantly(
            phone_no=formatted_no,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        click_whatsapp()
        cleanup_report_preparation()

        if message:
            pyautogui.typewrite(message)
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.hotkey("ctrl", "v")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        closing_whatsapp_tab()
        logger.info(f"[SYSTEM] MESSAGE SUCCESSFULLY SENT TO {formatted_no}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] MESSAGE SEND FAILURE TO {phone_no}: {str(e)}")
        raise


def send_summary_report(phone_no: str, message: str) -> bool:
    try:
        open_chrome()
        formatted_no = number_formatter(phone_no)
        if not formatted_no:
            raise ValueError(f"INVALID PHONE NUMBER: {phone_no}")

        logger.info(f"[SYSTEM] INITIATING SUMMARY MESSAGE TO {formatted_no}")

        kit.sendwhatmsg_instantly(
            phone_no=formatted_no,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        click_whatsapp()
        cleanup_report_preparation()

        if message:
            pyautogui.typewrite(message)
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        closing_whatsapp_tab()
        logger.info(f"[SYSTEM] SUMMARY MESSAGE SUCCESSFULLY SENT TO {formatted_no}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] SUMMARY MESSAGE SEND FAILURE TO {phone_no}: {str(e)}")
        raise


def send_paste_report(phone_no: str, message: str) -> bool:
    try:
        open_chrome()
        formatted_no = number_formatter(phone_no)
        if not formatted_no:
            raise ValueError(f"INVALID PHONE NUMBER: {phone_no}")

        logger.info(f"[SYSTEM] INITIATING PASTE MESSAGE TO {formatted_no}")

        kit.sendwhatmsg_instantly(
            phone_no=formatted_no,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        click_whatsapp()
        cleanup_report_preparation()
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])

        if not message:
            raise ValueError("EMPTY MESSAGE CANNOT BE PASTED")

        pyperclip.copy(message)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])

        pyautogui.hotkey("ctrl", "v")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        closing_whatsapp_tab()
        logger.info(f"[SYSTEM] PASTE MESSAGE SUCCESSFULLY SENT TO {formatted_no}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] PASTE MESSAGE SEND FAILURE TO {phone_no}: {str(e)}")
        raise
