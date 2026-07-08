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
        log_lines: list[str] = logs.splitlines()
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
        subprocess.run(["git", "add", file_path], check=True)
        logger.info(f"File added to git: '{file_path}'")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to add file to git: {file_path}")
        logger.error(e.stderr)


def git_commit_and_push():
    try:
        subprocess.run(["git", "commit", "-m", f"{datetime.now().strftime('%Y-%m-%d')} run"], check=True)
        logger.info("Changes committed to git.")
        subprocess.run(["git", "push"], check=True)
        logger.info("Changes pushed to remote repository.")
    except subprocess.CalledProcessError as e:
        logger.error("Failed to commit or push changes to git.")
        logger.error(e.stderr)
