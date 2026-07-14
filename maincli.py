import traceback
from datetime import datetime

import typer
from loguru import logger

import get_emails as gmail
from chrono import Chrono
from config import FROM_ADDRESS
from database import Database
from git_ops import git_add, git_commit_and_push, git_status
from ia import summarize_html_files
from log_ops import setup_logging
from temp_dir import create_temp_dir, delete_html_files

STEPS: dict[int, str] = {
    0: "Pre-initialization",
    1: "cleanup HTML files",
    2: "Searching and reading emails",
    3: "Summarizing HTML files",
    4: "Deleting HTML files",
    5: "Git operations",
    6: "Stats",
}

app: typer.Typer = typer.Typer()


def title_log(message: str):
    logger.info(message)
    logger.info("=" * len(message))


def elapsed_time_log(duration: dict[int, float], step: int):
    logger.info(
        f"Step {step} duration: {duration[step]:.4f} seconds (total duration: {sum(duration.values()):.4f} seconds)\n"
    )


def show_stats(durations: dict[int, float]):
    durations = {
        0: 0.01397889998042956,
        1: 0.1464830000186339,
        2: 31.57685939996736,
        3: 460.80753130000085,
        4: 0.03012260003015399,
        5: 4.468728699954227,
    }
    logger.warning(durations)
    sum_dur: float = sum(durations.values()) if durations else 0
    logger.info("=" * 20)
    for step, description in STEPS.items():
        if step in durations:
            logger.info(
                f"{step}: {description:<30} - Duration: {durations[step]:.4f} seconds ({durations[step] / sum_dur * 100:.2f}%)"
            )
        else:
            if step != 6:
                logger.info(f"{step}: {description:<30} - Duration: Not executed")
    logger.info("=" * 20)
    logger.info(f"Total Execution Time: {sum(durations.values()):.4f} seconds")


def start():
    restart(1)


def initialization(db: Database) -> None:
    delete_html_files()  # Cleanup any existing HTML files
    db.delete_generated_mails()


def read_all_mails_from_mailing_lists(db: Database) -> list[dict[str, str | datetime]]:
    mail_read: list[dict[str, str | datetime]] = []
    for mail_from in FROM_ADDRESS:
        result: list[dict[str, str | datetime]] | None = gmail.search_and_read_emails(mail_from, db, test_only=False)
        if result:
            mail_read.extend(result)
    return mail_read


@app.command()
def restart(step: int = 0):
    # pre-init: database creation/connection - temp folder creation / chg dir
    try:
        durations: dict[int, float] = {}
        pre_init_duration: Chrono = Chrono()
        pre_init_duration.start()
        db: Database = Database()
        db.connect()
        create_temp_dir("generated_files")
        pre_init_duration.stop()
        durations[0] = pre_init_duration.elapsed_time()
        elapsed_time_log(durations, 0)
    except Exception as e:
        logger.error(f"Error occurred during step 0 : {STEPS[0]}")
        logger.error(f"Exception: {e}")
        logger.error(traceback.format_exc())
        logger.warning("This should not happen. please correct and restart via python maincli.py or uv run maincli.py")
        return

    if step <= 0 or step > max(STEPS):
        logger.error(f"Invalid step number: {step}. Valid steps are 1 to {len(STEPS)}.")
        return
    logger.info(f"(Re)Starting at step {step}...")

    while step <= max(STEPS):
        title_log(f"{step}) {STEPS[step]}")
        match step:
            case 1:
                try:
                    init_duration: Chrono = Chrono()
                    init_duration.start()
                    initialization(db)
                    init_duration.stop()
                    durations[step] = init_duration.elapsed_time()
                    elapsed_time_log(durations, step)
                except Exception as e:
                    logger.error(f"Error occurred during step {step} : {STEPS[step]}")
                    logger.error(f"Exception: {e}")
                    logger.error(traceback.format_exc())
                    logger.warning(
                        "This should not happen. please correct and restart via python maincli.py or uv run maincli.py"
                    )
                    return

            case 2:
                try:
                    search_duration: Chrono = Chrono()
                    search_duration.start()
                    mail_read: list[dict[str, str | datetime]] = read_all_mails_from_mailing_lists(db)

                    logger.info(f"Html files generated: {len(mail_read)}")

                    if len(mail_read) > 0:
                        for mail in mail_read:
                            logger.info(f"- {mail['title']} - {mail['id']} - {mail['date']}")

                    search_duration.stop()
                    durations[step] = search_duration.elapsed_time()
                    elapsed_time_log(durations, step)
                except Exception as e:
                    logger.error(f"Error occurred during step {step} : {STEPS[step]}")
                    logger.error(f"Exception: {e}")
                    logger.error(traceback.format_exc())
                    logger.warning(
                        "This should not happen. please correct and restart via python maincli.py or uv run maincli.py"
                    )
                    return
            case 3:
                try:
                    html_duration: Chrono = Chrono()
                    html_duration.start()
                    summarize_html_files()  # summary by Gemini
                    html_duration.stop()
                    durations[step] = html_duration.elapsed_time()
                    elapsed_time_log(durations, step)
                except Exception as e:
                    logger.error(f"Error occurred during step {step} : {STEPS[step]}")
                    logger.error(f"Exception: {e}")
                    logger.error(traceback.format_exc())
                    logger.warning(
                        "You should relaunch directly step 3: Please correct and restart via python maincli.py restart --step 3 or uv run maincli.py restart --step3"
                    )
                    return
            case 4:
                try:
                    delete_duration: Chrono = Chrono()
                    delete_duration.start()
                    delete_html_files()
                    delete_duration.stop()
                    durations[step] = delete_duration.elapsed_time()
                    elapsed_time_log(durations, step)
                except Exception as e:
                    logger.error(f"Error occurred during step {step} : {STEPS[step]}")
                    logger.error(f"Exception: {e}")
                    logger.error(traceback.format_exc())
                    logger.warning(
                        "You should relaunch directly step 4: Please correct and restart via python maincli.py restart --step 4 or uv run maincli.py restart --step 4"
                    )
                    return
            case 5:
                try:
                    git_duration: Chrono = Chrono()
                    git_duration.start()
                    file_to_add: str | None = git_status()
                    if not file_to_add:
                        logger.warning("No .md file found to add to git. Is this normal ?")
                    else:
                        git_add(file_to_add)
                        git_commit_and_push()
                    git_duration.stop()
                    durations[step] = git_duration.elapsed_time()
                    elapsed_time_log(durations, step)
                except Exception as e:
                    logger.error(f"Error occurred during step {step} : {STEPS[step]}")
                    logger.error(f"Exception: {e}")
                    logger.error(traceback.format_exc())
                    logger.warning(
                        "You should relaunch directly step 5: Please correct and restart via python maincli.py restart --step 5 or uv run maincli.py -restart --step 5"
                    )
                    return
            case 6:
                try:
                    show_stats(durations)
                except Exception as e:
                    logger.error(f"Error occurred during step {step} : {STEPS[step]}")
                    logger.error(f"Exception: {e}")
                    logger.error(traceback.format_exc())
                    logger.warning(
                        "This should not happen. please correct and restart via python maincli.py or uv run maincli.py"
                    )
                    return

        step += 1


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Callback that triggers on the base command."""
    # ctx.invoked_subcommand is None if the user didn't type 'restart'
    if ctx.invoked_subcommand is None:
        start()


if __name__ == "__main__":
    setup_logging()
    app()
