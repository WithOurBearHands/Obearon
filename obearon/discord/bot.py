"""
Obearon's Discord related module.
"""

import os

import discord
from loguru import logger

from obearon.discord.tasks.assign_hibernation import assign_hibernation
from obearon.discord.tasks.check_verified_users import check_for_verified_users
from obearon.discord.views.verify import VerifyView
from obearon.mail import Mail

client = discord.Bot()
mail = Mail()


@client.event
async def on_ready() -> None:
    """
    Triggered when pycord reports the bot as fully loaded.
    """
    client.add_view(VerifyView())
    check_for_verified_users.start(client=client, mail=mail)
    assign_hibernation.start(client=client)
    logger.info(f"{client.user} is ready.")


async def start_discord_bot() -> None:
    """
    Start the Discord bot.
    """
    for directory_entry in os.listdir("obearon/discord/commands"):
        if not directory_entry.endswith(".py") or directory_entry == "__init__.py":
            continue
        client.load_extension(f"obearon.discord.commands.{directory_entry.replace(".py", "")}")
        logger.info(f"Loaded the cog in {directory_entry}.")

    mail.login()
    await client.start(os.environ["DISCORD_TOKEN"])
