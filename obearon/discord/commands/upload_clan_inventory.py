"""
Upload clan inventory command.
"""

from http.client import HTTPException
import json
from json import JSONDecodeError

import discord
from discord.commands import default_permissions
from discord.commands import option
from discord.ext import commands
import loguru as logger
from sqlalchemy.exc import SQLAlchemyError

from obearon.database import crud


class UploadClanInventory(commands.Cog):
    """
    Cog for upload clan inventory command.
    """

    def __init__(self, client: commands.Bot):
        """
        Initialize the upload clan inventory cog.

        Args:
            Client: The client to add the cog to.
        """
        self.client = client

    @commands.slash_command()
    @option("file", type=discord.SlashCommandOptionType.attachment)
    @default_permissions(manage_roles=True)
    async def upload_clan_inventory(self, ctx: discord.ApplicationContext, file: discord.Attachment) -> None:
        """
        Accept an attachment uploaded by user and send it to database.

        Args:
            ctx: The context of the user who executed this command.
            file: .JSON file containing clan inventory.
        """
        player_list = []
        if not file.filename.lower().endswith(".json"):
            await ctx.respond(f"Can only accept '.JSON' files.", ephemeral=True)
            return
        try:
            file_content = await file.read()
            bytes_to_string = file_content.decode("utf-8")
            parsed_json = json.loads(bytes_to_string)
            for member in parsed_json["Members"]:
                all_names = [member["DisplayName"]]
                all_names.extend(member.get("PlatformNames", []))
                player_dict = {"oid": member["_id"]["$oid"], "names": all_names, "mastery_rank": member.get("PlayerLevel", "0")}
                player_list.append(player_dict)
        except (discord.NotFound, HTTPException, JSONDecodeError) as exception:
            logger.info(f"Failed to parse file.\n {exception}")
            return
        try:
            await crud.create_update_warframe_players(player_list)

        except SQLAlchemyError as ex:
            logger.info(f"Database update failed.\n {ex}")


def setup(client: commands.Bot) -> None:
    """
    Setup the upload clan inventory cog. Called by pycord.

    Args:
        client: The client to add the cog to.
    """
    client.add_cog(UploadClanInventory(client))