"""
Upload clan inventory command.
"""
import json
from http.client import HTTPException
from json import JSONDecodeError

import discord
from discord.commands import default_permissions
from discord.commands import option
from discord.ext import commands
import loguru as logger
from obearon.database import models

from obearon.database import crud


class UploadClanInventory(commands.cog):
    """
    Cog for upload clan inventory command.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the upload clan inventory cog.

        Args:
            bot: The bot to add the cog to.
        """
        self.bot = bot

        @commands.slash_command()
        @option("file", type=discord.SlashCommandOptionType.attachment)
        @default_permissions(manage_roles=True)
        async def upload_clan_inventory(ctx: discord.ApplicationContext, file: discord.Attachment) -> None:
            """
            Accept an attachment uploaded by user and send it to database.

            Args:
                ctx: The context of the user who executed this command.
                file: .JSON file containing clan inventory.
            """
            if not file.filename.lower().endswith(".json"):
                await ctx.respond(f"Can only accept '.JSON' files.", ephemeral=True)
                return
            try:
                file_content = await file.read()
                bytes_to_string = file_content.decode("utf-8")
                parsed_json = json.loads(bytes_to_string)
                for member in parsed_json['Member']:
                    all_names = [member['DisplayName']]
                    all_names.extend(member.get('PlatformNames', []))
                    warframe_player_object = models.WarframePlayer(
                        oid=member['oid'],
                        names=all_names,
                        mastery_rank=member['PlayerLevel']
                    )



            except (discord.NotFound, HTTPException, JSONDecodeError) as exception:
                logger.info(f"Failed to parse file into model objects.\n {exception}")






