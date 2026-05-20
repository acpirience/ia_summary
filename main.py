import os

from loguru import logger

import get_emails as gmail


def main():
    logger.info("Starting ia-summary!")
    if not os.path.exists("generated_files"):
        os.makedirs("generated_files")
    os.chdir("generated_files")
    logger.info(f"Current Directory is = {os.getcwd()}")

    for mail_from in gmail.FROM_ADDRESS:
        logger.info(mail_from)
        gmail.search_and_read_emails(mail_from)


if __name__ == "__main__":
    main()
