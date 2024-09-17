from multiprocessing import Process

from dotenv import load_dotenv

from bearification.browser import start_browser
from bearification.discord_bot import start_discord_bot

load_dotenv()


if __name__ == "__main__":
    browser_thread = Process(target=start_browser)
    discord_thread = Process(target=start_discord_bot)

    browser_thread.start()
    discord_thread.start()

    try:
        browser_thread.join()
        discord_thread.join()
    except KeyboardInterrupt:
        print("Exiting.")
    except Exception as e:
        print(e)
