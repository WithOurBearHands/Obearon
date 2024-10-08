"""
The main file to control Bearification.
"""

import asyncio

from bearification.database import engine
from bearification.discord_bot import close
from bearification.discord_bot import start_discord_bot

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        event_loop.run_until_complete(engine.create_tables())
        event_loop.run_until_complete(start_discord_bot())
    except KeyboardInterrupt:
        print("Exiting.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(e)
    finally:
        event_loop.close()
        close()
