"""
Update to hibernation for users out of clan task.
"""

import os
import discord
from discord import Forbidden
from discord.ext import tasks
from loguru import logger

from obearon.database import crud


@tasks.loop(seconds=20)
async def assign_hibernation(client: discord.Bot) -> None:
    """
    Assign hibernation role to users not in clan that have verified role.

    Args:
        client: The client of the bot.
    """

    user_in_clan = False  # Placeholder

    guild_id = int(os.environ["DISCORD_GUILD_ID"])
    guild = client.get_guild(guild_id)
    verify_role = await crud.get_verify_role(guild_id)
    hibernation_role = await crud.get_hibernation_role(guild_id)
    warframe_players = await crud.get_warframe_players()

    for member in guild.members:  ## Uses cache, switch to using API with intent for consistency?
        if member.get_role(verify_role.verified_role_id) is guild.get_role(
            verify_role.verified_role_id
        ):  # Confused about this warning
            if
                try:
                    if not user_in_clan:
                        await member.remove_roles(guild.get_role(verify_role.verified_role_id))
                        await member.add_roles(guild.get_role(hibernation_role.hibernation_role_id))
                        logger.info(
                            f"User {member.id} role update, removed {verify_role.verified_role_id} "
                            f"added {hibernation_role.hibernation_role_id}"
                        )
                except Forbidden:
                    logger.info(f"Failed to updates roles of {member.id} in {guild.id} during 'assign hibernation'.")
