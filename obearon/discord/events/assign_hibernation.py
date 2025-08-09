"""
Assign hibernation to users out of clan task.
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone
import os

import discord
from discord import Forbidden
from loguru import logger

from obearon.database import crud

client = discord.Bot()


@client.event
async def on_application_command_completion(ctx) -> None:
    """
    Assign hibernation role to users not in clan that have verified role.

    Args:
        ctx: Context of completed commands.
    """
    if ctx.command.name == "upload_clan_inventory":
        guild_id = int(os.environ["DISCORD_GUILD_ID"])
        guild = client.get_guild(guild_id)
        verified_role = await crud.get_verify_role(guild_id)
        hibernation_role = await crud.get_hibernation_role(guild_id)
        warframe_players = await crud.get_warframe_player_names()

        for member in guild.members:  ## Uses cache, which doesn't update consistently
            if not member.get_role(verified_role.verified_role_id):
                continue
            joined_recently = datetime.now(timezone.utc) - member.joined_at < timedelta(hours=24)
            if joined_recently:
                continue
            if any(name == member.nick for name in warframe_players):
                continue
            try:
                await member.remove_roles(guild.get_role(verified_role.verified_role_id))
                await member.add_roles(guild.get_role(hibernation_role.hibernation_role_id))
                logger.info(
                    f"User {member.id} role update, removed {verified_role.verified_role_id} "
                    f"added {hibernation_role.hibernation_role_id}"
                )
            except Forbidden:
                logger.info(f"Failed to updates roles of {member.id} in " f"{guild.id} during 'assign hibernation'.")
