"""
Update to hibernation for users out of clan task.
"""

import discord
from discord import Forbidden
from discord.ext import tasks
from loguru import logger

from obearon.database import crud


@tasks.loop(seconds=20)
async def assign_hibernation(client: discord.Bot) -> None:
    raise NotImplementedError("Function not implemented yet")
    """
    Assign hibernation role to users not in clan that have verified role.
    
    Args:
        client: The client of the bot.
    """
    for member in await crud.

    guild = client.get_guild(guild_id)
    verified_role = await crud.get_verify_role(guild_id)
    hibernation_role = await crud.get_hibernation_role(guild_id)
    member = await guild.fetch_member(discord_id)
    await member.remove_roles(guild.get_role(verified_role.verified_role_id)) #Confused about this warning
    await member.add_roles(guild.get_role(hibernation_role.hibernation_role_id)) #Confused about this warning
    logger.info(f"User {discord_id} role update, removed {verified_role.verified_role_id} "
                f"added {hibernation_role.hibernation_role_id}")