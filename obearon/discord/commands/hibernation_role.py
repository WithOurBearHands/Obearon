"""
Hibernation role command.
"""

import discord
from discord.commands import default_permissions
from discord.commands import option
from discord.ext import commands

from obearon.database import crud


class HibernationRole(commands.Cog):
    """
    Cog for Hibernation role commands.
    """
    def __init__(self, bot: commands.Bot):
        """
        Initialize the HibernationRole cog.

        Args:
            bot: The bot to add the cog to.
        """
        self.bot = bot

    @commands.slash_command()
    @option("role", type=discord.SlashCommandOptionType.role)
    @default_permissions(manage_roles=True)
    async def set_hibernation_role(self, ctx: discord.ApplicationContext, role: discord.Role) -> None:
        """
        Sets the hibernation role to be given when discord member is no longer in clan.

        Args:
            ctx: The context of the user who executed this command.
            role: The role to store.
        """
        await crud.set_hibernation_role(guild_id=ctx.guild_id, hibernation_role_id=role.id)
        await ctx.respond(content=f"**{role.name}** has been set as the hibernation role.", ephemeral=True)

    @commands.slash_command()
    @default_permissions(manage_roles=True)
    async def get_hibernation_role(self, ctx: discord.ApplicationContext) -> None:
        """
        Gets the hibernation role to be given when discord member is no longer in clan.

        Args:
            ctx: The context of the user who executed this command.
        """
        role = await crud.get_hibernation_role(guild_id=ctx.guild_id)
        await ctx.respond(
            content=(f"<@&{role.hibernation_role_id}>" if role else "No role") + " has been set as the hibernation role.",
            ephemeral=True,
        )

def setup(bot: commands.Bot) -> None:
    """
    Setup the hibernation cog. Called by pycord.

    Args:
        bot: The bot to add the cog to.
    """
    bot.add_cog(HibernationRole(bot))