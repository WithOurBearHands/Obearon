import os
import random

import discord
from discord.ext import tasks

client = discord.Bot()


@client.event
async def on_ready():
    client.add_view(VerifyView())
    check_for_verified_users.start()
    print(f'{client.user} is ready.')


@tasks.loop(seconds=10)
async def check_for_verified_users():
    print("loop step")


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Verify', style=discord.ButtonStyle.green, custom_id='verify_view:verify')
    async def on_verify_click(self, _: discord.ui.Button, interaction: discord.Interaction) -> None:
        user_code = random.randint(100_000, 999_999)
        await interaction.response.send_message(
            content=(
                f"1. Go to <{os.environ["CREATE_MESSAGE_LINK"]}>.\n"
                f"2. Enter `{user_code}` in the **subject** or **message**.\n"
                "3. Send the message and **wait up to 2 minutes**[.](https://i.imgur.com/caLFbWY.png)"
            ),
            ephemeral=True
        )


@client.message_command(
    name="Create verify message",
    contexts={discord.InteractionContextType.guild},
    default_member_permissions=discord.Permissions(manage_messages=True)
)
async def create_verify_message(interaction: discord.Interaction, message: discord.Message):
    embed = discord.Embed(
        title="Rules",
        description=message.content,
        color=0xdd05ed,
        thumbnail=interaction.guild.icon.url,
    )
    await interaction.channel.send(embed=embed, view=VerifyView())
    await message.delete()
    await interaction.response.send_message("Created the verify message.", ephemeral=True)


def start_discord_bot():
    client.run(os.environ["DISCORD_TOKEN"])
