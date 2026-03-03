import pyautogui
from typing import List, Optional, Union

from general_task import (
    maximize_app_window,
    creating_new_task,
    blank_mail_space,
    make_important_mail,
    finish_outlook,
    minimize_outlook,
    confirm,
)
from services.config import load_config, wait_timer, logger
from services.capslock_checker import capslock_checking
from services.chrome_checker import open_outlook
from services.certification_utils import get_email_subject


CONFIG = load_config()


def normalizing_recipients(recipients: Union[str, List[str], None]) -> List[str]:
    if recipients is None:
        return []

    if isinstance(recipients, str):
        value = recipients.strip().lower()
        return [value] if value else []

    cleaned: List[str] = []
    for r in recipients:
        if not r:
            continue
        value = str(r).strip().lower()
        if value:
            cleaned.append(value)
    return cleaned


def write_recipients(recipient_list: List[str]) -> None:
    for idx, recipient in enumerate(recipient_list):
        pyautogui.write(recipient)
        confirm()
        if idx < len(recipient_list) - 1:
            wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def send_certification_email(
    branch_name: str,
    branch_manager: str,
    bm_mail: str,
    email_body: str,
    minimize_after_send: bool = True,
    cc_recipients: Optional[Union[str, List[str]]] = None,
) -> bool:
    subject_email = get_email_subject(branch_name)

    primary_recipients = normalizing_recipients(bm_mail)
    primary_log_email = primary_recipients[0] if primary_recipients else ""

    logger.info(f"[SYSTEM] START BRANCH ='{branch_name}' TO '{primary_log_email}')")

    try:
        if not primary_recipients:
            logger.error("[ERROR] PRIMARY RECIPIENT EMAIL (BM_MAIL) IS EMPTY")
            return False

        cc_list = normalizing_recipients(cc_recipients)

        if not open_outlook():
            logger.error("[ERROR] FAILED TO ACTIVATE OR LAUNCH OUTLOOK")
            return False

        wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
        maximize_app_window()
        capslock_checking()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        make_important_mail()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        creating_new_task()

        write_recipients(primary_recipients)

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        if cc_list:
            write_recipients(cc_list)

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        pyautogui.write(subject_email)

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.hotkey("ctrl", "v")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        blank_mail_space()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        if minimize_after_send:
            minimize_outlook()
        else:
            finish_outlook()

        logger.info(f"[SYSTEM] BRANCH '{branch_name}' SUCCESS")
        return True

    except Exception as e:
        logger.error(f"[ERROR] CERTIFICATION EMAIL SENDING FAILED : {e}")
        return False
