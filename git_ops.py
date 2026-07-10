import subprocess
from datetime import datetime

from loguru import logger


def git_status() -> str | None:
    try:
        # Run the command and capture the output
        result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
        file_to_add: str = ""

        # Access the captured logs
        logs: str = result.stdout
        logger.info("--- Git Status Output ---")
        log_lines: list[str] = [str(line) for line in logs.splitlines()]
        for line in log_lines:
            logger.info(line)
            if line.rstrip().endswith(".md"):
                file_to_add = line.strip().lstrip()

        logger.info(f"File to add to git: '{file_to_add}'")
        return file_to_add

    except subprocess.CalledProcessError as e:
        logger.error(  # If the command returns a non-zero exit code
            f"Command failed with exit code {e.returncode}"
        )
        logger.error("--- Error Logs ---")
        logger.error(e.stderr)

    except FileNotFoundError:
        logger.error("Error: 'git' command not found. Is it installed and in your PATH?")
        logger.info(logs)

    except subprocess.CalledProcessError as e:
        logger.error(  # If the command returns a non-zero exit code
            f"Command failed with exit code {e.returncode}"
        )
        logger.error("--- Error Logs ---")
        logger.error(e.stderr)

    except FileNotFoundError:
        logger.error("Error: 'git' command not found. Is it installed and in your PATH?")


def git_add(file_path: str):
    try:
        result = subprocess.run(["git", "add", file_path], capture_output=True, text=True, check=True)
        logs: str = result.stdout or ""
        logger.info(f"--- Git add {file_path} ---")
        log_lines: list[str] = [str(line) for line in logs.splitlines()]
        for line in log_lines:
            logger.info(line)

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to add file to git: {file_path}")
        logger.error(e.stderr)


def git_commit_and_push():
    try:
        result = subprocess.run(
            ["git", "commit", "-m", f"{datetime.now().strftime('%Y-%m-%d')} run"],
            capture_output=True,
            text=True,
            check=True,
        )
        logs: str = result.stdout or ""
        logger.info(f"--- Git commit -m '{datetime.now().strftime('%Y-%m-%d')} run' ---")
        log_lines: list[str] = [str(line) for line in logs.splitlines()]
        for line in log_lines:
            logger.info(line)
        subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True,
            check=True,
        )
        logs: str = result.stdout or ""
        logger.info("--- Git push ---")
        log_lines: list[str] = [str(line) for line in logs.splitlines()]
        for line in log_lines:
            logger.info(line)
    except subprocess.CalledProcessError as e:
        logger.error("Failed to commit or push changes to git.")
        logger.error(e.stderr)
