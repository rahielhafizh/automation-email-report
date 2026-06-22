from mail.base_mail import send_base_outlook


def send_outlook_email(
    outlook_recipients, secondary_recipients, subject_email, core_email, footer_template
):
    send_base_outlook(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
        attachment_key="SUB_PERFORMANCE_RECOVERY_WO",
        report_label="REPORT PERFORMANCE RECOVERY WO",
    )
