from services.config import load_config
from remover.base_remover import clear_submission_folder


def run_remover(dry_run: bool = False):
    config = load_config()
    target = str(config.get("SUB_PENERIMAAN_DENDA_AKTIF", ""))
    return clear_submission_folder(
        target_folder=target, filename_pattern="*", dry_run=dry_run
    )


if __name__ == "__main__":
    run_remover()
