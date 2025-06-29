"""
The main file to control Obearon.
"""

import asyncio
import os

from dotenv import load_dotenv
from loguru import logger

from obearon.discord.bot import start_discord_bot

if __name__ == "__main__":
    if not os.environ.get("DISCORD_TOKEN"):
        load_dotenv()

    event_loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        event_loop.run_until_complete(start_discord_bot())
    except KeyboardInterrupt:
        logger.info("Exiting.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception(e)
    finally:
        event_loop.close()
