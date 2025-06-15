"""
Giveaway view.
"""

import discord
from loguru import logger

from obearon.database import crud


# TODO: Add handler to re-add view on bot restarts.
class GiveawayView(discord.ui.View):
    """
    Class for handling the giveaway view.
    """

    def __init__(self):
        """
        Initialize the persistent giveaway view.
        timeout has to be None in order for the button to not break over restarts.
        """
        super().__init__(timeout=None)

    @discord.ui.button(
        emoji="🎉",
        label="Join giveaway",
        style=discord.ButtonStyle.blurple,
    )
    async def on_join_giveaway(self, _: discord.ui.Button, interaction: discord.Interaction) -> None:
        """
        Triggered when a user clicks the "Join giveaway" button.

        Args:
          _: Required button argument.
          interaction: The interaction of the user.
        """
        giveaway_participants = await crud.get_giveaway_participants(giveaway_id=interaction.message.id)
        if interaction.user.id in giveaway_participants:
            logger.info(
                f"Removing {interaction.user.display_name} ({interaction.user.id}) "
                f"from the giveaway {interaction.message.id}."
            )
            await crud.remove_giveaway_participant(
                giveaway_id=interaction.message.id, discord_user_id=interaction.user.id
            )
            await interaction.response.send_message(
                content="You have left the giveaway.",
                ephemeral=True,
            )
            return

        logger.info(
            f"Adding {interaction.user.display_name} ({interaction.user.id}) to the giveaway {interaction.message.id}."
        )
        await crud.add_giveaway_participant(giveaway_id=interaction.message.id, discord_user_id=interaction.user.id)
        await interaction.response.send_message(
            content="You have joined the giveaway.",
            ephemeral=True,
        )
