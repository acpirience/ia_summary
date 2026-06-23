import typer
from loguru import logger

STEPS: dict[int, str] = {
    1: "Initialisation / cleanup",
    2: "Searching and reading emails",
    3: "Summarizing HTML files",
    4: "Deleting HTML files",
}

app: typer.Typer = typer.Typer()


def start():
    restart(1)


@app.command()
def restart(step: int):
    if step <= 0 or step > len(STEPS):
        logger.error(f"Invalid step number: {step}. Valid steps are 1 to {len(STEPS)}.")
        return
    logger.info(f"(Re)Starting at step {step}...")

    while step <= len(STEPS):
        logger.info(f"{step} {STEPS[step]}")
        match step:
            case 1:
                pass  # Initialisation / cleanup is handled in maincli.py
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
