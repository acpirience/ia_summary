import email
import imaplib
from datetime import datetime, timedelta

from loguru import logger

from config import DAYS_AGO, EMAIL_PASSWORD, EMAIL_USER, IMAP_SERVER
from database import Database


def get_file_name(title: str, id: str, count: int) -> str:
    return f"{title.replace(' ', '')}_{id}_{count:02}"


def search_and_read_emails(
    mail_from: dict[str, str], db: Database, test_only: bool = False
) -> list[dict[str, str | datetime]] | None:
    mail_found: list[dict[str, str | datetime]] = []
    # 1. Connect to the server and login
    logger.info("Connecting to server...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASSWORD)  # ty: ignore

    # Select the folder you want to search (INBOX is standard)
    mail.select("inbox")

    # 2. Calculate the date condition for IMAP (Format: DD-Mon-YYYY)
    since_date = (datetime.now() - timedelta(days=DAYS_AGO)).strftime("%d-%b-%Y")

    # 3. Construct the IMAP search query
    # IMAP queries use the format: (FROM "email" SINCE "date")
    search_criterion = f'(FROM "{mail_from["email"]}" SINCE "{since_date}")'
    print(f"Searching with criteria: {search_criterion}")

    status, messages = mail.search(None, search_criterion)

    if status != "OK":
        print("No messages found or error occurred.")
        return

    # mail.search returns a list of space-separated IDs
    email_ids = messages[0].split()
    logger.info(f"Found {len(email_ids)} emails matching criteria.\n")
    if len(email_ids) == 0:
        return

    # 4. Fetch and parse the emails
    mail_count: int = 0
    for e_id in email_ids:
        id: str = e_id.decode("utf-8")
        if db.exists_mail(mail_from["title"], id):
            logger.info(f"Email already processed: {mail_from['title']} - {id}")
            continue
        mail_count += 1
        # Fetch the email data (RFC822 is the standard email format)
        status, data = mail.fetch(e_id, "(RFC822)")
        if status != "OK":
            continue

        # Parse the raw bytes into an email object
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        logger.info(f"From: {msg['From']}")
        logger.info(f"Date: {msg['Date']}")

        mail_read: dict[str, str | datetime] = {"title": mail_from["title"], "id": id, "date": msg["Date"]}
        mail_found.append(mail_read)

        # Extract the body of the email
        body = ""
        if msg.is_multipart():
            # If multipart, iterate through the parts to find text/plain
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/html" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            # If not multipart, just grab the payload
            body = msg.get_payload(decode=True).decode()

        filename: str = get_file_name(mail_from["title"], id, mail_count) + ".html"
        logger.info(f"writing file: {filename}")

        if test_only:
            logger.info("File not written")
        else:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(body)

        logger.info("-" * 50)

    # 5. Logout safely
    mail.close()
    mail.logout()
    return mail_found


if __name__ == "__main__":
    logger.critical("launch via main.py")
