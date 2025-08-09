"""
CRUD operations for the warframe_player table.
"""

from loguru import logger
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert

from obearon.database import engine
from obearon.database import models


async def create_update_warframe_players(players: list[dict], player_names: list[dict]):
    """
    Bulk operation to process Warframe Players and Warframe Player Names.

    Args:
        players: list of dicts, contains oid, mastery_rank
        player_names: list of dicts, contains oid, name, platform
    """
    player_oids = [player["oid"] for player in players]
    async with engine.async_session() as session, session.begin():
        for player in players:
            upsert = (
                insert(models.WarframePlayers)
                .values(**player)
                .on_conflict_do_update(
                    index_elements=["oid"], set_={"mastery_rank": player["mastery_rank"], "in_clan": True}
                )
            )
            await session.execute(upsert)
        out_of_clan = (
            update(models.WarframePlayers).where(models.WarframePlayers.oid.not_in(player_oids)).values(in_clan=False)
        )
        await session.execute(out_of_clan)
        for name in player_names:
            name_insert = (
                insert(models.WarframePlayerNames)
                .values(**name)
                .on_conflict_do_nothing(index_elements=["oid", "name", "platform"])
            )
            await session.execute(name_insert)

        await session.commit()
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


async def get_warframe_player_names() -> list[str]:
    """
    Get all player names.

    Returns:
        A list of names.
    """

    async with engine.async_session() as session, session.begin():
        names = await session.execute(select(models.WarframePlayerNames.name))
        return [row[0] for row in names.all()]


async def get_warframe_player_names_not_in_clan() -> list[str]:
    """
    Get all player names of players not in clan.

    Returns:
        A list of names.
    """
    fetch_names = (
        select(models.WarframePlayerNames.name)
        .join(models.WarframePlayers, models.WarframePlayerNames.oid == models.WarframePlayers.oid)
        .where(models.WarframePlayers.in_clan.is_(False))
    )
    async with engine.async_session() as session, session.begin():
        names = await session.execute(fetch_names)
        return [row[0] for row in names.all()]
