"""
The main file to control Bearification.
"""
import asyncio
from multiprocessing import Process

from dotenv import load_dotenv
load_dotenv()

from bearification import database
from bearification.browser import start_browser
from bearification.discord_bot import start_discord_bot


if __name__ == "__main__":
    asyncio.run(database.create_database())

    browser_thread = Process(target=start_browser)
    discord_thread = Process(target=start_discord_bot)

    browser_thread.start()
    discord_thread.start()

    try:
        browser_thread.join()
        discord_thread.join()
    except KeyboardInterrupt:
        print("Exiting.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(e)
