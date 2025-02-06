"""
Bearification's code receiving related module.
"""

from math import ceil
import os

from aiohttp import ClientSession
from aiohttp import TCPConnector
from bs4 import BeautifulSoup
from loguru import logger
from protonmail import ProtonMail
from protonmail.models import Message

from bearification.database import crud


class Mail:
    """
    Class to cache and interact with the proton mail instance.
    """

    def __init__(self):
        self.proton = ProtonMail()

    def login(self) -> None:
        """
        Log in to Proton mail.
        """
        self.proton.login(
            username=os.environ["PROTON_USERNAME"],
            password=os.environ["PROTON_PASSWORD"],
        )

    async def check_messages(self) -> None:
        """
        Wait for messages. Upon receiving a message, the contents are logged and the message is deleted.
        """
        messages_to_delete = []
        for message in await self.get_messages():
            if message.sender.address != "noreply@invisioncloudcommunity.com" or not message.unread:
                continue

            message_content = self.proton.read_message(message)

            soup = BeautifulSoup(message_content.body, "html.parser")
            subject_tags = soup.find_all("h2")
            if len(subject_tags) == 0:
                continue

            warframe_name = message.subject.replace(" has sent you a message", "")
            subject = subject_tags[0].text.strip()

            logger.info(f"Message from '{warframe_name}' with subject '{subject}'")
            try:
                verification_code = int(subject)
                await crud.update_warframe_name(verification_code=verification_code, warframe_name=warframe_name)
            except ValueError:
                logger.info(f"'{subject}' is not an integer.")

            messages_to_delete.append(message)

        self.proton.delete_messages(messages_to_delete)

    async def get_messages(self, page_size: int | None = 150, label_id: str = "5") -> list[Message]:
        """
        Get all messages from proton.
        Rewrite of the library's method to work in current async context.
        """
        pages = ceil(self.proton.get_messages_count()[5]["Total"] / page_size)
        args = [(page_num, page_size, label_id) for page_num in range(pages)]

        connector = TCPConnector(limit=100)
        headers = dict(self.proton.session.headers)
        cookies = self.proton.session.cookies.get_dict()

        messages = []
        async with ClientSession(headers=headers, cookies=cookies, connector=connector) as client:
            for arg in args:
                messages.append(await self.proton._async_get_messages(client, *arg))
        messages_dict = self.proton._flattening_lists(messages)
        messages = [self.proton._convert_dict_to_message(message) for message in messages_dict]

        return messages
