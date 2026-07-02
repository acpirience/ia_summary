import traceback
from datetime import datetime

import typer
from loguru import logger

import get_emails as gmail
from chrono import Chrono
from config import FROM_ADDRESS
from database import Database
from temp_dir import create_temp_dir, delete_html_files

STEPS: dict[int, str] = {
    0: "Pre-initialization",
    1: "cleanup HTML files",
    2: "Searching and reading emails",
    3: "Summarizing HTML files",
    4: "Deleting HTML files",
}

app: typer.Typer = typer.Typer()


def title_log(message: str):
    logger.info(message)
    logger.info("=" * len(message))


def elapsed_time_log(duration: dict[int, float], step: int):
    logger.info(
        f"Step {step} duration: {duration[step]:.4f} seconds (total duration: {sum(duration.values()):.4f} seconds)\n"
    )


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

                    logger.info(f"emails read: {len(mail_read)}")

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
                pass  # Summarizing HTML files is handled in maincli.py
            case 4:
                pass  # Deleting HTML files is handled in maincli.py

        step += 1


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Callback that triggers on the base command."""
    # ctx.invoked_subcommand is None if the user didn't type 'restart'
    if ctx.invoked_subcommand is None:
        start()


if __name__ == "__main__":
    app()
