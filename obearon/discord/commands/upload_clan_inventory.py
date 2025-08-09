"""
Upload clan inventory command.
"""

from http.client import HTTPException
import json
from json import JSONDecodeError
import re

import discord
from discord.commands import default_permissions
from discord.commands import option
from discord.ext import commands
from loguru import logger
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
            client: The client to add the cog to.
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
        await ctx.defer(ephemeral=True, invisible=False)
        player_list = []
        player_name_list = []
        platform_dict = {
            "\ue000": "pc",
            "\ue001": "xbox",
            "\ue002": "playstation",
            "\ue003": "nintendo",
            "\ue004": "ios",
            "\ue005": "unk005",
            "\ue006": "unk006",
            "\ue007": "unk007",
        }
        if not file.filename.lower().endswith(".json"):
            await ctx.respond("Can only accept '.JSON' files.", ephemeral=True)
            return
        try:
            file_content = await file.read()
            bytes_to_string = file_content.decode("utf-8")
            parsed_json = json.loads(bytes_to_string)
            for member in parsed_json["Members"]:
                all_names = [member["DisplayName"]]
                all_names.extend(member.get("PlatformNames", []))
                for name in all_names:
                    match = re.match(r"(.*?)([\ue000-\uefff])$", name)
                    if match:
                        player_name = match.group(1)
                        platform_code = match.group(2)
                        platform = platform_dict.get(platform_code, "unknown")
                    else:
                        player_name = name
                        platform = "unknown"
                    player_dict = {"oid": member["_id"]["$oid"], "name": player_name, "platform": platform}
                    player_name_list.append(player_dict)
            for member in parsed_json["Members"]:
                player_dict = {"oid": member["_id"]["$oid"], "mastery_rank": member.get("PlayerLevel", "0")}
                player_list.append(player_dict)
        except (discord.NotFound, HTTPException, JSONDecodeError) as exception:
            logger.info(f"Failed to parse file.\n {exception}")
            await ctx.respond("Data upload failed!", ephemeral=True)
            return
        try:
            await crud.create_update_warframe_players(player_list, player_name_list)
            logger.info("warframe_players and warframe_player_names table updated.")
            await ctx.respond("Data upload complete!", ephemeral=True)

        except SQLAlchemyError as ex:
            logger.info(f"Database upload failed!\n {ex}")
            await ctx.respond("Data upload failed!", ephemeral=True)
            return


def setup(client: commands.Bot) -> None:
    """
    Setup the upload clan inventory cog. Called by pycord.

    Args:
        client: The client to add the cog to.
    """
    client.add_cog(UploadClanInventory(client))
