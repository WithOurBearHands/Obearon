"""
CRUD operations for the role table.
"""

from loguru import logger
from sqlalchemy import select

from obearon.database import engine
from obearon.database import models


async def set_verify_role(guild_id: int, verified_role_id: int) -> None:
    """
    Stores the verification role to be given.

    Args:
        guild_id: The guild ID in which to give the role.
        verified_role_id: The ID of the role to be given.
    """
    async with engine.async_session() as session, session.begin():
        role_query = await session.execute(select(models.GuildRole).where(models.GuildRole.guild_id == guild_id))
        role = role_query.scalars().first()
        if role is not None:
            role.discord_role_id = verified_role_id
            logger.info(f"Updated {guild_id} with new role ID {verified_role_id}.")
            return

        session.add(models.GuildRole(guild_id=guild_id, verified_role_id=verified_role_id))
        logger.info(f"Set Discord role ID {verified_role_id} for guild ID {guild_id}.")


async def get_verify_role(guild_id: int) -> models.GuildRole | None:
    """
    Get the verify role ID or none if none is set.

    Args:
        guild_id: The Discord guild ID to search for.

    Returns:
        A GuildRole instance or None if no information exists.
    """
    async with engine.async_session() as session, session.begin():
        role_query = await session.execute(select(models.GuildRole).where(models.GuildRole.guild_id == guild_id))
        return role_query.scalars().first()


async def set_friend_role(guild_id: int, friend_role_id: int) -> None:
    """
    Stores the friend role to be given.

    Args:
        guild_id: The guild ID in which to give the role.
        friend_role_id: The ID of the role to be given.
    """
    async with engine.async_session() as session, session.begin():
        role_query = await session.execute(select(models.GuildRole).where(models.GuildRole.guild_id == guild_id))
        role = role_query.scalars().first()
        if role is not None:
            role.friend_role_id = friend_role_id
            logger.info(f"Updated {guild_id} with new role ID {friend_role_id}.")
            return

        session.add(models.GuildRole(guild_id=guild_id, friend_role_id=friend_role_id))
        logger.info(f"Set Discord role ID {friend_role_id} for guild ID {guild_id}.")


async def get_friend_role(guild_id: int) -> models.GuildRole | None:
    """
    Get the friend role ID or none if none is set.

    Args:
        guild_id: The Discord guild ID to search for.

    Returns:
        A GuildRole instance or None if no information exists.
    """
    async with engine.async_session() as session, session.begin():
        role_query = await session.execute(select(models.GuildRole).where(models.GuildRole.guild_id == guild_id))
        return role_query.scalars().first()
