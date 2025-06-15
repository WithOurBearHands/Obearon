"""
Giveaway command.
"""

import discord
from discord.ext import commands


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
        # TODO: Implement GiveawayModal
        # await ctx.respond(modal=GiveawayModal())


def setup(bot: commands.Bot) -> None:
    """
    Setup the Giveaway cog. Called by pycord.

    Args:
        bot: The bot to add the cog to.
    """
    bot.add_cog(Giveaway(bot))
