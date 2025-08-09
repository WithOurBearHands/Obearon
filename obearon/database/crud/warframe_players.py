"""
CRUD operations for the warframe_player table.
"""

from loguru import logger
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert

from obearon.database import engine
from obearon.database import models


async def create_update_warframe_players(players: list[dict]): ## TODO: fix
    """
    Bulk operation to process a list of WarframePlayer model objects.

    Args:
        players: list of dicts, should contain oid, names[list], mastery_rank
    """
    player_oids = [player["oid"] for player in players]
    async with engine.async_session() as session, session.begin():
        for player in players:
            upsert = (
                insert(models.WarframePlayers)
                .values(**player)
                .on_conflict_do_update(
                    index_elements=["oid"], set_={"names": player["names"], "mastery_rank": player["mastery_rank"]}
                )
            )
            await session.execute(upsert)
        out_of_clan = (
            update(models.WarframePlayers).where(models.WarframePlayers.oid.not_in(player_oids)).values(in_clan=False)
        )
        await session.execute(out_of_clan)
    logger.info("Updated warframe_players table.")


async def get_warframe_players() -> list[models.WarframePlayers]:
    """
    Get all warframe players.

    Returns:
        A list of WarframePlayers objects.
    """

    async with engine.async_session() as session, session.begin():
        warframe_players_query = await session.execute(select(models.WarframePlayers))
        return warframe_players_query.scalars().all()


async def get_warframe_players_name() -> list[str]: ## TODO: fix
    """
    Get all player names.

    Returns:
        A list of names.
    """

    async with engine.async_session() as session, session.begin():
        names = await session.execute(select(models.WarframePlayers.name))
        return [row[0] for row in names.all()]


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
            models.WarframePlayers(
                oid=oid,
                names=names,
                mastery_rank=mastery_rank,
            )
        )
