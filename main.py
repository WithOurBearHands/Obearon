import threading

from dotenv import load_dotenv

from bearification.browser import start_browser

load_dotenv()


if __name__ == "__main__":
    browser_thread = threading.Thread(start_browser())
    browser_thread.start()
    browser_thread.join()
