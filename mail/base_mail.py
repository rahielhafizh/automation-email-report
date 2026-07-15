import pyautogui
from general_task import *
from services.config import load_config, wait_timer, logger
from services.capslock_checker import capslock_checking
from services.chrome_checker import open_outlook

CONFIG = load_config()


def send_base_outlook(
    outlook_recipients,
    secondary_recipients,
    subject_email,
    core_email,
    footer_template,
    attachment_key,
    report_label,
):
    logger.info(f"[SYSTEM] START {report_label} REPORT MAIL")
    try:
        if not open_outlook():
            raise RuntimeError("FAILED TO ACTIVATE OR LAUNCH OUTLOOK")

        wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
        maximize_app_window()
        capslock_checking()
        creating_new_task()

        # Input Recipients (To)
        recipients = (
            [outlook_recipients]
            if isinstance(outlook_recipients, str)
            else outlook_recipients
        )

        for idx, recipient in enumerate(recipients):
            pyautogui.write(recipient)
            confirm()
            if idx < len(recipients) - 1:
                wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        # Input CC (Secondary)
        if secondary_recipients:
            cc_list = (
                [secondary_recipients]
                if isinstance(secondary_recipients, str)
                else secondary_recipients
            )

            for cc in cc_list:
                pyautogui.write(cc)
                confirm()
                wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        # Subject & Attachment
        pyautogui.write(subject_email)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])

        choose_file_attach()
        pyautogui.write(CONFIG.get(attachment_key, ""))
        confirm_file_attach()

        pyautogui.write(core_email)
        blank_mail_space()
        input_clipboard_picture()
        pyautogui.write(footer_template)

        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        finish_outlook()
        logger.info(f"[SYSTEM] {report_label} REPORT MAIL COMPLETED")

    except Exception as e:
        logger.error(f"[ERROR] {report_label} REPORT MAIL FAILED: {e}")
        raise
