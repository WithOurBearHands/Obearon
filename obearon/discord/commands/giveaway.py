"""
Giveaway command.
"""

import discord
from discord.ext import commands

from obearon.discord.modals.giveaway import GiveawayModal


class Giveaway(commands.Cog):
    """
    Cog for giveaway commands.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the Giveaway cog.

        Args:
            bot: The bot to add the cog to.
        """
        self.bot = bot

    @commands.slash_command()
    async def create_giveaway(self, ctx: discord.ApplicationContext) -> None:
        """
        Create a giveaway.

        Args:
            ctx: The context of the user who executed this command.
        """
        await ctx.send_modal(GiveawayModal(title="Create Giveaway"))


def setup(bot: commands.Bot) -> None:
    """
    Setup the Giveaway cog. Called by pycord.

    Args:
        bot: The bot to add the cog to.
    """
    bot.add_cog(Giveaway(bot))
