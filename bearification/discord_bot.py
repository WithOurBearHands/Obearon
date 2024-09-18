"""
Bearification's Discord related module.
"""

import os
import random

import discord
from discord import Forbidden
from discord.ext import tasks

from bearification.database import crud

client = discord.Bot()


@client.event
async def on_ready() -> None:
    """
    Triggered when pycord reports the bot as fully loaded.
    """
    client.add_view(VerifyView())
    check_for_verified_users.start()
    print(f"{client.user} is ready.")


@tasks.loop(seconds=10)
async def check_for_verified_users() -> None:
    """
    Periodically check for new verified users and assign nicknames/roles.
    """
    for user in await crud.get_verified_users():
        guild = client.get_guild(user.discord_guild_id)
        member = await guild.fetch_member(user.discord_user_id)
        try:
            await member.edit(nick=user.warframe_name)
            print(f"Updated username of {user.discord_user_id} to {user.warframe_name}")
            await crud.update_user_as_linked(discord_user_id=user.discord_user_id)
        except Forbidden:
            print(f"Could not change username of {user.discord_user_id} in {user.discord_guild_id}")


class VerifyView(discord.ui.View):
    """
    Class for handling the verify view/button.
    """

    def __init__(self):
        """
        Initialize the persistent verify view.
        timeout has to be None in order for the button to not break over restarts.
        """
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_view:verify")
    async def on_verify_click(self, _: discord.ui.Button, interaction: discord.Interaction) -> None:
        """
        Triggered when a user clicks the "Verify" button.

        Args:
          _: Required button argument.
          interaction: The interaction of the user.
        """
        verification_code = random.randint(100_000, 999_999)
        await crud.create_user(
            discord_guild_id=interaction.guild_id,
            discord_user_id=interaction.user.id,
            verification_code=verification_code,
        )

        await interaction.response.send_message(
            content=(
                f"1. Go to <{os.environ["CREATE_MESSAGE_LINK"]}>.\n"
                f"2. Enter `{verification_code}` in the **subject** or **message**.\n"
                "3. Send the message and **wait up to 2 minutes**[.](https://i.imgur.com/caLFbWY.png)"
            ),
            ephemeral=True,
        )


@client.message_command(
    name="Create verify message",
    contexts={discord.InteractionContextType.guild},
    default_member_permissions=discord.Permissions(manage_messages=True),
)
async def create_verify_message(interaction: discord.Interaction, message: discord.Message) -> None:
    """
    Creates a "Create verify message" option when the message is right-clicked and Apps is hovered.

    Args:
        interaction: The interaction of the user who clicked this option.
        message: The message that was right-clicked.
    """
    embed = discord.Embed(
        title="Rules",
        description=message.content,
        color=0xDD05ED,
        thumbnail=interaction.guild.icon.url,
    )
    await interaction.channel.send(embed=embed, view=VerifyView())
    await message.delete()
    await interaction.response.send_message("Created the verify message.", ephemeral=True)


def start_discord_bot():
    """
    Start the Discord bot.
    """
    client.run(os.environ["DISCORD_TOKEN"])
