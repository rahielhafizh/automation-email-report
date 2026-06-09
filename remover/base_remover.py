import os
import glob
from typing import List, Dict
from services.config import logger


def get_matching_files(folder_path: str, pattern: str = "*") -> List[str]:
    search_pattern = os.path.join(folder_path, pattern)
    return [item for item in glob.glob(search_pattern) if os.path.isfile(item)]


def delete_files(files: List[str], dry_run: bool = False) -> Dict[str, int]:
    deleted_count, failed_count = 0, 0
    for file_path in files:
        file_name = os.path.basename(file_path)
        if dry_run:
            logger.info(f"[SYSTEM] DRY RUN - SKIPPING: {file_name}")
            continue
        try:
            os.remove(file_path)
            logger.info(f"[SYSTEM] DELETED: {file_name}")
            deleted_count += 1
        except Exception:
            logger.error(f"[SYSTEM] FAILED: {file_name}", exc_info=True)
            failed_count += 1
    return {"deleted": deleted_count, "failed": failed_count}


def log_deletion_summary(summary: Dict[str, int], dry_run: bool) -> None:
    mode = "DRY RUN" if dry_run else "ACTUAL RUN"
    logger.info(
        f"[SYSTEM] {mode} SUMMARY - DELETED: {summary['deleted']} | FAILED: {summary['failed']}"
    )


def clear_submission_folder(
    target_folder: str, filename_pattern: str = "*", dry_run: bool = False
) -> Dict[str, int]:
    if not os.path.exists(target_folder):
        logger.error(f"[SYSTEM] FOLDER NOT FOUND: {target_folder}")
        return {"deleted": 0, "failed": 0}

    matching_files = get_matching_files(target_folder, filename_pattern)
    if not matching_files:
        logger.warning(f"[SYSTEM] NO FILES MATCHED IN: {target_folder}")
        return {"deleted": 0, "failed": 0}

    logger.info(f"[SYSTEM] DELETING {len(matching_files)} FILE(S) IN: {target_folder}")
    summary = delete_files(matching_files, dry_run=dry_run)
    log_deletion_summary(summary, dry_run=dry_run)
    return summary
