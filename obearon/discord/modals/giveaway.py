"""
Modal for creating a giveaway.
"""

import datetime

import dateparser
import discord

from obearon.database import crud
from obearon.discord.views.giveaway import GiveawayView


class GiveawayModal(discord.ui.Modal):
    """
    Modal for creating a giveaway.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                custom_id="duration",
                label="Duration",
                placeholder="Ex: 10 minutes",
                required=True,
            )
        )
        self.add_item(
            discord.ui.InputText(
                custom_id="number_of_winners", label="Number Of Winners", value="1", required=True, max_length=2
            )
        )
        self.add_item(discord.ui.InputText(custom_id="prize", label="Prize", required=True))
        self.add_item(
            discord.ui.InputText(
                custom_id="mastery_rank_restriction",
                label="Mastery rank restriction",
                placeholder="Ex: < 11",
                required=False,
                max_length=5,
            )
        )
        self.add_item(
            discord.ui.InputText(
                custom_id="description",
                label="Description",
                style=discord.InputTextStyle.long,
                required=False,
                max_length=1000,
            )
        )

    def parse_mastery_rank_restriction(self, value: str) -> tuple[int, int]:
        """
        Parse the mastery rank restriction.

        Args:
            value: The value of the mastery rank restriction.

        Returns:
            A tuple of the minimum and maximum mastery ranks.
        """
        if "<" in value:
            return 0, int(value.replace("<", ""))
        elif ">" in value:
            return int(value.replace(">", "")), 36
        else:
            return 0, 36

    async def callback(self, interaction: discord.Interaction):
        end_date: datetime.datetime
        try:
            end_date = dateparser.parse(self.children[0].value, settings={"PREFER_DATES_FROM": "future"})
            if end_date <= datetime.datetime.now():
                raise ValueError()
        except ValueError:
            await interaction.response.send_message(
                "You provided an invalid duration, or a time in the past.",
                ephemeral=True,
            )
            return

        winners = 1
        try:
            winners = int(self.children[1].value)
        except ValueError:
            pass

        title = self.children[2].value
        description = next((child.value for child in self.children if child.custom_id == "description"), "")

        mastery_rank_restriction = next(
            (child.value for child in self.children if child.custom_id == "mastery_rank_restriction"), ""
        )
        minimum_mastery_rank, maximum_mastery_rank = self.parse_mastery_rank_restriction(mastery_rank_restriction)

        description += f"\n\n**Hosted by:** {interaction.user.mention}"

        if minimum_mastery_rank > 0:
            description += f"\n**__Minimum__ mastery rank:** {minimum_mastery_rank}"

        if maximum_mastery_rank < 36:
            description += f"\n**__Maximum__ mastery rank:** {maximum_mastery_rank}"

        description += f"\n**Ends at:** <t:{int(end_date.timestamp())}:R>"
        description += f"\n**Number of winners:** {winners}"

        embed = discord.Embed(
            title=title,
            description=description,
        )

        interaction_response = await interaction.response.send_message(embed=embed, view=GiveawayView())
        await crud.create_giveaway(
            message_id=interaction_response.message.id, end_date=end_date, hoster_discord_id=interaction.user.id
        )
