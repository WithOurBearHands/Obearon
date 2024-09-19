"""
Bearification's browser related module.
"""

import asyncio
import os
import random

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from bearification.database import crud


def log_in(browser: WebDriver) -> None:
    """
    Log in to Warframe.
    Since log-in requires a captcha if the user is suspected to be a bot, we use cookie sessions instead.

    Args:
        browser: An instance of the browser to log in on.
    """
    browser.get("https://forums.warframe.com/")
    browser.add_cookie(
        {
            "name": "gid",
            "value": os.environ["COOKIE_GID"],
            "domain": ".warframe.com",
        }
    )
    browser.add_cookie(
        {
            "name": "logsig",
            "value": os.environ["COOKIE_LOGSIG"],
            "domain": ".warframe.com",
        }
    )
    browser.add_cookie(
        {
            "name": "ips4_device_key",
            "value": os.environ["COOKIE_IPS4_DEVICE_KEY"],
            "domain": "forums.warframe.com",
        }
    )
    browser.get("https://forums.warframe.com/")


async def wait_for_messages(browser: WebDriver) -> None:
    """
    Wait for messages. Upon receiving a message, the contents are logged and the message is deleted.

    Args:
        browser: An instance of the browser to check messages in.
    """
    while True:
        browser.get("https://forums.warframe.com/messenger")
        try:
            message = browser.find_element(By.CLASS_NAME, "cMessageTitle")
        except NoSuchElementException:
            time_until_refresh = random.randint(90, 150)
            print(f"No messages. Trying again in {time_until_refresh}s.")
            await asyncio.sleep(time_until_refresh)
            continue

        subject = message.text.strip()
        message.click()
        await asyncio.sleep(2)

        username = browser.find_element(By.CSS_SELECTOR, "strong.ipsType_normal").text.replace("\n", "")
        newest_comment = browser.find_elements(By.CSS_SELECTOR, 'div[data-role="commentContent"]')[0]
        message = newest_comment.find_element(By.TAG_NAME, "p").text

        print(f"Message from '{username}' with subject '{subject}' and message '{message}'")
        try:
            verification_code = int(subject)
            await crud.update_warframe_name(verification_code=verification_code, warframe_name=username)
        except ValueError:
            print(f"'{subject}' is not an integer.")

        conversation_options = browser.find_element(By.ID, "elConvoActions")
        conversation_options.click()
        await asyncio.sleep(0.5)

        conversation_actions = browser.find_element(By.ID, "elConvoActions_menu")
        delete_action = conversation_actions.find_elements(By.TAG_NAME, "a")[1]
        delete_action.click()
        await asyncio.sleep(2)

        delete_confirm = browser.find_element(By.CSS_SELECTOR, 'button[data-action="ok"]')
        delete_confirm.click()
        await asyncio.sleep(1)


def start_browser() -> None:
    """
    Start a browser, log in and wait for messages. This is blocking.
    """
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
    firefox_options.add_argument("--headless")
    chrome = webdriver.Firefox(options=firefox_options)
    try:
        log_in(chrome)
        asyncio.run(wait_for_messages(chrome))
    except KeyboardInterrupt:
        pass
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(e)
    chrome.close()
