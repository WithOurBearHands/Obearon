"""
Verify role command.
"""

import discord
from discord.commands import default_permissions
from discord.commands import option
from discord.ext import commands

from obearon.database import crud
from obearon.discord.views.verify import VerifyView


class VerifyRole(commands.Cog):
    """
    Cog for verify role commands.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the VerifyRole cog.

        Args:
            bot: The bot to add the cog to.
        """
        self.bot = bot

    @commands.slash_command()
    @option("role", type=discord.SlashCommandOptionType.role)
    @default_permissions(manage_roles=True)
    async def set_verify_role(self, ctx: discord.ApplicationContext, role: discord.Role) -> None:
        """
        Sets the verify role to be given upon successful verification.

        Args:
            ctx: The context of the user who executed this command.
            role: The role to store.
        """
        await crud.set_verify_role(guild_id=ctx.guild_id, verified_role_id=role.id)
        await ctx.respond(
            content=f"**{role.name}** has been set as the verified role.",
            ephemeral=True,
        )

    @commands.slash_command()
    @default_permissions(manage_roles=True)
    async def get_verify_role(self, ctx: discord.ApplicationContext) -> None:
        """
        Gets the verify role to be given upon successful verification.

        Args:
            ctx: The context of the user who executed this command.
        """
        role = await crud.get_verify_role(guild_id=ctx.guild_id)
        await ctx.respond(
            content=(f"<@&{role.verified_role_id}>" if role else "No role") + " has been set as the verified role.",
            ephemeral=True,
        )

    @commands.message_command(
        name="Create verify message",
    )
    @default_permissions(manage_messages=True)
    async def create_verify_message(self, ctx: discord.ApplicationContext, message: discord.Message) -> None:
        """
        Creates a "Create verify message" option when the message is right-clicked and Apps is hovered.

        Args:
            ctx: The context of the user who clicked this option.
            message: The message that was right-clicked.
        """
        embed = discord.Embed(
            title="🐝 Bee welcomed to our beary 🐻 gnarly Discord! ✨ <:goopolla:1288497392806527117>",
            description=message.content,
            color=0xDD05ED,
            thumbnail=ctx.guild.icon.url,
        )
        await ctx.channel.send(embed=embed, view=VerifyView())
        await message.delete()
        await ctx.respond("Created the verify message.", ephemeral=True)


def setup(bot: commands.Bot) -> None:
    """
    Setup the VerifyRole cog. Called by pycord.

    Args:
        bot: The bot to add the cog to.
    """
    bot.add_cog(VerifyRole(bot))
