"""
Check verified users task.
"""

import discord
from discord import Forbidden
from discord.ext import tasks
from loguru import logger

from obearon.database import crud
from obearon.mail import Mail


@tasks.loop(seconds=60)
async def check_for_verified_users(client: discord.Bot, mail: Mail) -> None:
    """
    Check for new verified users and assign nicknames/roles.

    Args:
        client: The client of the bot.
        mail: The mail of the bot.
    """
    await mail.check_messages()

    for user in await crud.get_successful_verifications():
        guild = client.get_guild(user.discord_guild_id)
        verified_role = await crud.get_verify_role(user.discord_guild_id)
        try:
            member = await guild.fetch_member(user.discord_user_id)
        except discord.errors.NotFound:
            logger.info(f"{user.discord_user_id} has left the server. Removing verification.")
            await crud.remove_verification(user.discord_user_id)
            return
        try:
            await member.edit(nick=user.warframe_name)
            logger.info(f"Updated username of {user.discord_user_id} to {user.warframe_name}")
            if verified_role:
                await member.add_roles(guild.get_role(verified_role.verified_role_id))
                logger.info(f"Updated roles of {user.discord_user_id} with {verified_role.verified_role_id}")
            await crud.remove_verification(discord_user_id=user.discord_user_id)
        except Forbidden:
            logger.info(f"Could not change username or roles of {user.discord_user_id} in {user.discord_guild_id}")
