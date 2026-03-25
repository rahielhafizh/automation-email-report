import pyodbc
from typing import Optional
from services.db_connection import get_database_connection
from services.config import (
    load_config,
    wait_timer,
    logger,
    get_branch_order,
    get_certification_filter_config,
    set_certification_filter_preset,
)
from services.database_queries import (
    fetch_certification_data_internal,
    fetch_certification_data_external,
)
from services.certification_utils import (
    filter_expiring_certifications,
    group_by_branch,
    extract_branch_manager_info,
)
from services.email_formatter import format_combined_email_body
from services.email_sender import send_certification_email

CONFIG = load_config()


def process_certification_reminders(
    filter_preset: Optional[str] = None, minimize_after_send: bool = True
) -> bool:
    if filter_preset:
        if not set_certification_filter_preset(filter_preset):
            logger.error(f"[ERROR] FAILED TO SET FILTER : {filter_preset}")

    conn = get_database_connection()
    if conn is None:
        logger.error("[ERROR] DATABASE CONNECTION UNAVAILABLE")
        return False

    try:
        logger.info("[SYSTEM] FETCHING INTERNAL & EXTERNAL CERTIFICATION DATA")
        columns_internal, rows_internal = fetch_certification_data_internal(conn)
        columns_external, rows_external = fetch_certification_data_external(conn)

        if columns_internal is None or columns_external is None:
            logger.error("[ERROR] FAILED TO FETCH DATA FROM DATABASE")
            return False

        active_filter = get_certification_filter_config()
        filtered_internal = filter_expiring_certifications(
            columns_internal, rows_internal, "EXPIRED_DATE"
        )
        filtered_external = filter_expiring_certifications(
            columns_external, rows_external, "EXPIRED_DATE"
        )

        logger.info(
            f"[SYSTEM] FILTER={active_filter.get('MODE')} | "
            f"INTERNAL={len(filtered_internal)} ROWS, EXTERNAL={len(filtered_external)} ROWS"
        )

        branch_groups_internal = group_by_branch(
            columns_internal, filtered_internal, "BRANCH_NAME"
        )
        branch_groups_external = group_by_branch(
            columns_external, filtered_external, "BRANCH"
        )

        all_branches = set(branch_groups_internal.keys()) | set(
            branch_groups_external.keys()
        )

        if len(all_branches) == 0:
            logger.info("[SYSTEM] NO EXPIRING CERTIFICATIONS FOUND")
            return True

        logger.info(f"[SYSTEM] GROUPED INTO {len(all_branches)} BRANCHES")
        for branch in sorted(all_branches):
            internal_count = len(branch_groups_internal.get(branch, []))
            external_count = len(branch_groups_external.get(branch, []))
            logger.info(
                f"[BRANCH] {branch:<20} INTERNAL = {internal_count}, EXTERNAL = {external_count}"
            )

        column_indices_internal = {col: idx for idx, col in enumerate(columns_internal)}
        column_indices_external = {col: idx for idx, col in enumerate(columns_external)}
        branch_order = get_branch_order()
        processed_count = 0
        failed_count = 0

        for branch_name in branch_order:
            internal_pic_list = branch_groups_internal.get(branch_name, [])
            external_pic_list = branch_groups_external.get(branch_name, [])

            if not internal_pic_list and not external_pic_list:
                continue

            branch_manager = None
            bm_mail = None

            if internal_pic_list:
                branch_manager, bm_mail = extract_branch_manager_info(
                    internal_pic_list,
                    column_indices_internal,
                    "BRANCH_MANAGER",
                    "BM_MAIL",
                )
            elif external_pic_list:
                branch_manager, bm_mail = extract_branch_manager_info(
                    external_pic_list,
                    column_indices_external,
                    "BRANCH_MANAGER",
                    "BM_MAIL",
                )

            if not branch_manager or not bm_mail:
                logger.warning(f"[WARNING] MISSING BRANCH MANAGER INFO : {branch_name}, SKIPPING")
                failed_count += 1
                continue

            email_body = format_combined_email_body(
                branch_name,
                branch_manager,
                internal_pic_list,
                external_pic_list,
                columns_internal,
                columns_external,
            )

            success = send_certification_email(
                branch_name, branch_manager, bm_mail, email_body, minimize_after_send
            )

            if success:
                processed_count += 1
            else:
                failed_count += 1

            wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

        logger.info(
            f"[SYSTEM] COMPLETED : {processed_count} SENT, {failed_count} FAILED"
        )
        return True

    except Exception as e:
        logger.error(f"[ERROR] COMBINED CERTIFICATION REMINDER FAILED : {e}")
        return False
    finally:
        conn.close()
        logger.info("[SYSTEM] DATABASE CONNECTION CLOSED")


if __name__ == "__main__":
    process_certification_reminders()  # DEFAULT VALUE (NEXT_MONTH)

    # process_certification_reminders(filter_preset="TWO_MONTHS")
    # process_certification_reminders(filter_preset="THREE_MONTHS")
    # process_certification_reminders(filter_preset="SIX_MONTHS")
    # process_certification_reminders(filter_preset="SIXTY_DAYS")