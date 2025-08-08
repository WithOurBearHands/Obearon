"""
CRUD operations for the warframe_player table.
"""

from loguru import logger
from sqlalchemy import delete
from sqlalchemy import select

from obearon.database import engine
from obearon.database import models


async def create_warframe_player(oid: str, names: list[str], mastery_rank: int) -> None:
    """
    Creates a warframe player.

    Args:
        oid: Unique Warframe player ID.
        names: Primary name of player.
        mastery_rank: Players ingame rank.
    """
    async with engine.async_session() as session, session.begin():
        session.add(
            models.WarframePlayer(
                oid=oid,
                names=names,
                mastery_rank=mastery_rank,
            )
        )


async def get_warframe_players() -> list[models.WarframePlayer]:
    """
    Get all warframe players.

    Returns:
        A list of WarframePlayers objects.
    """

    async with engine.async_session() as session, session.begin():
        warframe_players_query = await session.execute(select(models.WarframePlayer))
        return warframe_players_query.scalars().all()


async def get_warframe_players_name() -> list[str]:
    """
    Get all player names.

    Returns:
        A list of names.
    """

    async with engine.async_session() as session, session.begin():
        names = await session.execute(select(models.WarframePlayer.names))
        return [row[0] for row in names.all()]
