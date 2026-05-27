import os
from datetime import datetime

from loguru import logger

import get_emails as gmail
from config import FROM_ADDRESS
from database import Database


def main():
    logger.info("Starting ia-summary!")
    db: Database = Database()
    db.connect()

    if not os.path.exists("generated_files"):
        os.makedirs("generated_files")
    os.chdir("generated_files")
    logger.info(f"Current Directory is = {os.getcwd()}")
    mail_read: list[dict[str, str | datetime]] = []

    for mail_from in FROM_ADDRESS:
        logger.info(mail_from)
        result: list[dict[str, str | datetime]] | None = gmail.search_and_read_emails(mail_from, False)
        if result:
            mail_read.extend(result)

    logger.info(f"emails read: {len(mail_read)}")
    for mail in mail_read:
        logger.info(f"{mail['title']} - {mail['id']} - {mail['date']}")

    db.disconnect()


if __name__ == "__main__":
    main()
