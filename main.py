"""
The main file to control Bearification.
"""

import asyncio
import os

from loguru import logger

from bearification.database import engine
from bearification.discord_bot import close
from bearification.discord_bot import start_discord_bot
from dotenv import load_dotenv

if __name__ == "__main__":
    if not os.environ.get("DISCORD_TOKEN"):
        load_dotenv()

    event_loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        event_loop.run_until_complete(engine.create_tables())
        event_loop.run_until_complete(start_discord_bot())
    except KeyboardInterrupt:
        logger.info("Exiting.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception(e)
    finally:
        event_loop.close()
        close()
