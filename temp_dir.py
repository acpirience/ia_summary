import os
from pathlib import Path

from loguru import logger


def create_temp_dir(path_name: str | Path) -> None:
    target_path = Path(path_name)

    # Creates the directory and any missing parent directories safely.
    # exist_ok=True prevents an error if the folder already exists.
    target_path.mkdir(parents=True, exist_ok=True)

    # pathlib handles path manipulation, so os.chdir is still used to change
    # the process directory, but it natively accepts Path objects now.
    os.chdir(target_path)

    logger.info(f"Current Directory is = {Path.cwd()}")


def delete_html_files() -> None:
    # Convert string paths to a Path object for robust handling
    target_dir: Path = Path(Path.cwd())

    # Safety check: Ensure the path actually exists and is a directory
    if not target_dir.exists():
        raise FileNotFoundError(f"The directory '{target_dir}' does not exist.")
    if not target_dir.is_dir():
        raise NotADirectoryError(f"The path '{target_dir}' is not a valid directory.")

    # Iterate through all files ending with .html in the target directory
    for html_file in target_dir.glob("*.html"):
        try:
            html_file.unlink()
            logger.info(f"Deleted: {html_file.name}")
        except PermissionError:
            logger.error(f"Permission denied: Could not delete {html_file.name}")
        except OSError as e:
            logger.error(f"Error deleting {html_file.name}: {e}")
