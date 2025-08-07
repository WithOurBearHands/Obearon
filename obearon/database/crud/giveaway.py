"""
Giveaway CRUD operations.
"""

import datetime

from sqlalchemy import select

from obearon.database import engine
from obearon.database import models


async def create_giveaway(message_id: int, end_date: datetime.datetime, hoster_discord_id: int) -> None:
    """
    Create a giveaway.
    """
    async with engine.async_session() as session, session.begin():
        session.add(models.Giveaway(id=message_id, end_date=end_date, hoster_discord_id=hoster_discord_id))


async def add_giveaway_participant(giveaway_id: int, discord_user_id: int) -> None:
    """
    Add a participant to a giveaway.
    """
    async with engine.async_session() as session, session.begin():
        session.add(models.GiveawayParticipant(giveaway_id=giveaway_id, discord_user_id=discord_user_id))


async def remove_giveaway_participant(giveaway_id: int, discord_user_id: int) -> None:
    """
    Remove a participant from a giveaway.
    """
    async with engine.async_session() as session, session.begin():
        session.delete(models.GiveawayParticipant(giveaway_id=giveaway_id, discord_user_id=discord_user_id))


async def get_giveaway_participants(giveaway_id: int) -> list[int]:
    """
    Get all participants of a giveaway.
    """
    async with engine.async_session() as session, session.begin():
        giveaway_participant_query = await session.execute(
            select(models.GiveawayParticipant).where(models.GiveawayParticipant.giveaway_id == giveaway_id)
        )
        return {participant.discord_user_id for participant in giveaway_participant_query.scalars().all()}
