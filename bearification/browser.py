"""
Bearification's browser related module.
"""

import asyncio
import os

from loguru import logger
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from bearification.database import crud


class Browser:
    """
    Class to cache and interact with the firefox instance.
    """

    def __init__(self):
        user_agent = (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/128.0.0.0 "
            "Safari/537.36"
        )
        firefox_options = Options()
        firefox_options.set_preference("general.useragent.override", user_agent)
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        # firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")

        if os.path.exists("/usr/local/bin/geckodriver"):
            service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
            self.browser = webdriver.Firefox(options=firefox_options, service=service)
            return

        self.browser = webdriver.Firefox(options=firefox_options)

    def close(self):
        """
        Close the browser window.
        """
        self.browser.quit()

    def login(self) -> None:
        """
        Log in to Warframe.
        Since log-in requires a captcha if the user is suspected to be a bot, we use cookie sessions instead.
        """
        self.browser.get("https://forums.warframe.com/")
        self.browser.add_cookie(
            {
                "name": "gid",
                "value": os.environ["COOKIE_GID"],
                "domain": ".warframe.com",
            }
        )
        self.browser.add_cookie(
            {
                "name": "logsig",
                "value": os.environ["COOKIE_LOGSIG"],
                "domain": ".warframe.com",
            }
        )
        self.browser.add_cookie(
            {
                "name": "ips4_device_key",
                "value": os.environ["COOKIE_IPS4_DEVICE_KEY"],
                "domain": "forums.warframe.com",
            }
        )
        self.browser.get("https://forums.warframe.com/")

    async def check_messages(self) -> None:
        """
        Wait for messages. Upon receiving a message, the contents are logged and the message is deleted.
        """
        self.browser.get("https://forums.warframe.com/messenger")
        try:
            message = self.browser.find_element(By.CLASS_NAME, "cMessageTitle")
        except NoSuchElementException:
            logger.info("No messages.")
            return

        subject = message.text.strip()
        message.click()
        await asyncio.sleep(2)

        username = self.browser.find_element(By.CSS_SELECTOR, "strong.ipsType_normal").text.replace("\n", "")
        newest_comment = self.browser.find_elements(By.CSS_SELECTOR, 'div[data-role="commentContent"]')[0]
        message = newest_comment.find_element(By.TAG_NAME, "p").text

        logger.info(f"Message from '{username}' with subject '{subject}' and message '{message}'")
        try:
            verification_code = int(subject)
            return
            await crud.update_warframe_name(verification_code=verification_code, warframe_name=username)
        except ValueError:
            logger.info(f"'{subject}' is not an integer.")

        conversation_options = self.browser.find_element(By.ID, "elConvoActions")
        conversation_options.click()
        await asyncio.sleep(0.5)

        conversation_actions = self.browser.find_element(By.ID, "elConvoActions_menu")
        delete_action = conversation_actions.find_elements(By.TAG_NAME, "a")[1]
        delete_action.click()
        await asyncio.sleep(2)

        delete_confirm = self.browser.find_element(By.CSS_SELECTOR, 'button[data-action="ok"]')
        delete_confirm.click()
        await asyncio.sleep(1)
