import typer
from loguru import logger

from chrono import Chrono
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


def elapsed_time_log(durationq: dict[int, float], step: int):
    logger.info(
        f"Step {step} duration: {durationq[step]:.4f} seconds (total duration: {sum(durationq.values()):.4f} seconds)\n"
    )


def start():
    restart(1)


def initialization() -> None:
    delete_html_files()  # Cleanup any existing HTML files


@app.command()
def restart(step: int):
    # pre-init: database creation/connection - temp folder creation / chg dir
    durations: dict[int, float] = {}
    pre_init_duration: Chrono = Chrono()
    pre_init_duration.start()
    db: Database = Database()
    db.connect()
    create_temp_dir("generated_files")
    pre_init_duration.stop()
    durations[0] = pre_init_duration.elapsed_time()
    elapsed_time_log(durations, 0)

    if step <= 0 or step > max(STEPS):
        logger.error(f"Invalid step number: {step}. Valid steps are 1 to {len(STEPS)}.")
        return
    logger.info(f"(Re)Starting at step {step}...")

    while step <= max(STEPS):
        title_log(f"{step}) {STEPS[step]}")
        match step:
            case 1:
                init_duration: Chrono = Chrono()
                init_duration.start()
                initialization()
                init_duration.stop()
                durations[step] = init_duration.elapsed_time()
                elapsed_time_log(durations, step)

            case 2:
                pass  # Searching and reading emails is handled in maincli.py
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
