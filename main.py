from datetime import datetime

from loguru import logger

import get_emails as gmail
from config import FROM_ADDRESS
from database import Database
from ia import summarize_html_files
from temp_dir import create_temp_dir, delete_html_files


def main():
    logger.info("Starting ia-summary!")
    db: Database = Database()
    db.connect()

    create_temp_dir("generated_files")

    mail_read: list[dict[str, str | datetime]] = []

    for mail_from in FROM_ADDRESS:
        result: list[dict[str, str | datetime]] | None = gmail.search_and_read_emails(mail_from, db, test_only=False)
        if result:
            mail_read.extend(result)

    db.disconnect()

    logger.info(f"emails read: {len(mail_read)}")

    if len(mail_read) > 0:
        for mail in mail_read:
            logger.info(f"{mail['title']} - {mail['id']} - {mail['date']}")
        summarize_html_files()  # summary by Gemini

    delete_html_files()


if __name__ == "__main__":
    logger.warning("Please use maincli.py instead of running this file directly.")
    main()
