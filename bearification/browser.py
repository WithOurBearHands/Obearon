import os
import random
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver


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


def wait_for_messages(browser: WebDriver) -> None:
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
            sleep(time_until_refresh)
            continue

        subject = message.text
        message.click()
        sleep(2)

        username = browser.find_element(By.CSS_SELECTOR, "strong.ipsType_normal").text.replace("\n", "")
        newest_comment = browser.find_elements(By.CSS_SELECTOR, 'div[data-role="commentContent"]')[0]
        message = newest_comment.find_element(By.TAG_NAME, "p").text

        print(f"Message from {username} with subject {subject} and message {message}")

        conversation_options = browser.find_element(By.ID, "elConvoActions")
        conversation_options.click()
        sleep(0.25)

        conversation_actions = browser.find_element(By.ID, "elConvoActions_menu")
        delete_action = conversation_actions.find_elements(By.TAG_NAME, "a")[1]
        delete_action.click()
        sleep(1)

        delete_confirm = browser.find_element(By.CSS_SELECTOR, 'button[data-action="ok"]')
        delete_confirm.click()
        sleep(5)


def start_browser() -> None:
    """
    Start a browser, log in and wait for messages. This is blocking.
    """
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
    firefox_options = Options()
    firefox_options.add_argument(f"--user-agent={user_agent}")
    firefox_options.add_argument("--window-size=1920,1080")
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument("--disable-extensions")
    # firefox_options.add_argument("--headless=new")
    firefox = webdriver.Firefox(options=firefox_options)
    try:
        log_in(firefox)
        wait_for_messages(firefox)
    except Exception as e:
        print(e)
    firefox.close()
