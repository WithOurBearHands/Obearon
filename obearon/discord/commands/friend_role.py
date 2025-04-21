"""
Friend role commands.
"""

import discord
from discord.commands import default_permissions
from discord.commands import option
from discord.ext import commands

from obearon.database import crud


class FriendRole(commands.Cog):
    """
    Cog for friend role commands.
    """

    def __init__(self, client: commands.Bot):
        """
        Initialize the FriendRole cog.

        Args:
            client: The client to add the cog to.
        """
        self.client = client

    @commands.slash_command()
    @option("role", type=discord.SlashCommandOptionType.role)
    @default_permissions(manage_roles=True)
    async def set_friend_role(self, ctx: discord.ApplicationContext, role: discord.Role) -> None:
        """
        Sets the friend role to be given for server friends that join.

        Args:
            ctx: The context of the user who executed this command.
            role: The role to store.
        """
        await crud.set_friend_role(guild_id=ctx.guild_id, friend_role_id=role.id)
        await ctx.respond(content=f"**{role.name}** has been set as the friend role.", ephemeral=True)

    @commands.slash_command()
    @default_permissions(manage_roles=True)
    async def get_friend_role(self, ctx: discord.ApplicationContext) -> None:
        """
        Gets the friend role to be given for server friends that join.

        Args:
            ctx: The context of the user who executed this command.
        """
        role = await crud.get_friend_role(guild_id=ctx.guild_id)
        await ctx.respond(
            content=(f"<@&{role.friend_role_id}>" if role else "No role") + " has been set as the friend role.",
            ephemeral=True,
        )


def setup(client: commands.Bot) -> None:
    """
    Setup the FriendRole cog. Called by pycord.

    Args:
        client: The client to add the cog to.
    """
    client.add_cog(FriendRole(client))
