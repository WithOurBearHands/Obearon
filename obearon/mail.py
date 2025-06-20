"""
Obearon's code receiving related module.
"""

import email
from email.header import decode_header
import imaplib
import os

from bs4 import BeautifulSoup
from loguru import logger
import re

from obearon.database import crud


class Mail:
    """
    Class to cache and interact with the mail instance.
    """

    def __init__(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.code_regex = re.compile(r"\d{6}")

    def login(self) -> None:
        """
        Log in to the mail provider.
        """
        self.mail.login(
            user=os.environ["EMAIL_USERNAME"],
            password=os.environ["EMAIL_PASSWORD"],
        )
        self.mail.select("inbox")

    async def check_messages(self) -> None:
        """
        Wait for messages. Upon receiving a message, the contents are logged and the message is deleted.
        """
        status, messages = self.mail.search(None, 'FROM "noreply@invisioncloudcommunity.com"')
        if status != "OK":
            logger.error(f"Mail search returned '{status}'.")
            return

        # Messages is an array of one element with all message ids spaced,
        # for example [b"1 2 3 4 5"].
        for message_id in messages[0].split():
            status, raw_message = self.mail.fetch(message_id, "(RFC822)")
            if status != "OK":
                logger.warning(f"Mail fetch for mail '{message_id}' returned '{status}'.")
                continue

            # Similarly to search, fetch returns a two element array, where the first
            # array element is a tuple containing all information.
            # The first element in that tuple is the standard the second element is in,
            # which we know is RFC822.
            message = email.message_from_bytes(raw_message[0][1])

            # Get the subject of the message and, if necessary, decode it.
            subject, encoding = decode_header(message["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            if not message.is_multipart():
                logger.warning(f"Message with subject '{subject}' has an unexpected body. Ignoring it.")
                continue

            message_parts = list(message.walk())
            if len(message_parts) < 3:
                logger.warning(f"Message with subject '{subject}' has an unexpected body. Ignoring it.")
                continue

            body = message_parts[2].get_payload()

            soup = BeautifulSoup(body, "html.parser")
            warframe_message_subject_tags = soup.find_all("h2")
            warframe_message_content_tags = soup.find_all("div")
            if len(warframe_message_subject_tags) == 0 or len(warframe_message_subject_tags) == 0:
                logger.warning(
                    f"The Warframe message body changed. "
                    f"Soup tag finding needs to be adjusted for the following:\n{body}"
                )
                continue

            self.mail.store(message_id, "+FLAGS", "\\Deleted")

            warframe_name = subject.replace(" has sent you a message", "")
            warframe_subject = warframe_message_subject_tags[0].text.strip()
            warframe_message = warframe_message_content_tags[0].text.strip()

            logger.info(
                f"Message from '{warframe_name}' with subject '{warframe_subject}' and message '{warframe_message}'"
            )

            verification_code = self.code_regex.search(warframe_subject)
            if not verification_code:
                verification_code = self.code_regex.search(warframe_message)
            if not verification_code:
                logger.warning("Neither subject nor message contain a code.")
                continue

            try:
                verification_code = int(verification_code.group())
                await crud.update_warframe_name(verification_code=verification_code, warframe_name=warframe_name)
            except ValueError:
                logger.info(f"'{subject}' is not an integer.")

        self.mail.expunge()
