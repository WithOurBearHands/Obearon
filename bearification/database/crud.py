"""
Create, Read, Update and Delete operations in the database.
"""

from loguru import logger
from sqlalchemy import select
from sqlalchemy import update

from bearification.database import engine
from bearification.database import models


async def create_user(discord_guild_id: int, discord_user_id: int, verification_code: int) -> None:
    """
    Creates a user in the database. If it exists, the existing verification code is updated instead.

    Args:
        discord_guild_id: The guild in which this user is linked.
        discord_user_id: The discord user ID to link.
        verification_code: The verification code the user needs to send us.
    """
    async with engine.async_session() as session, session.begin():
        user_query = await session.execute(select(models.User).where(models.User.discord_user_id == discord_user_id))
        user = user_query.scalars().first()
        if user is not None:
            logger.info(f"Updating {user.warframe_name}/{discord_user_id} with new verification code.")
            user.warframe_name = None
            user.verified = False
            user.linked = False
            user.verification_code = verification_code
            return

        session.add(
            models.User(
                discord_guild_id=discord_guild_id, discord_user_id=discord_user_id, verification_code=verification_code
            )
        )
        logger.info(f"Added Discord ID {discord_user_id} with verification code {verification_code}.")


async def update_warframe_name(verification_code: int, warframe_name: str) -> None:
    """
    Update the warframe name for a verification code.

    Args:
        verification_code: The verification code we received.
        warframe_name: The warframe name we parsed.
    """
    async with engine.async_session() as session, session.begin():
        user_query = await session.execute(
            select(models.User).where(
                models.User.verification_code == verification_code, models.User.verified.is_(False)
            )
        )
        user = user_query.scalars().first()
        if user is None:
            logger.info(f"{warframe_name} entered an invalid verification code ({verification_code}).")
            return

        user.warframe_name = warframe_name
        user.verified = True
        logger.info(f"{warframe_name} ({user.discord_user_id}) has been marked as verified.")


async def get_verified_users() -> list[models.User]:
    """
    Get all verified users.

    Returns:
         A list of verified users.
    """
    async with engine.async_session() as session, session.begin():
        user_query = await session.execute(
            select(models.User).where(models.User.verified.is_(True), models.User.linked.is_(False))
        )
        return user_query.scalars().all()


async def update_user_as_linked(discord_user_id: int) -> None:
    """
    Mark a user as successfully linked.

    Args:
         discord_user_id: The Discord ID of the user to mark as linked.
    """
    async with engine.async_session() as session, session.begin():
        await session.execute(
            update(models.User).where(models.User.discord_user_id == discord_user_id).values({"linked": True})
        )


async def set_verify_role(discord_guild_id: int, discord_role_id: int) -> None:
    """
    Stores the verification role to be given.

    Args:
        discord_guild_id: The guild ID in which to give the role.
        discord_role_id: The ID of the role to be given.
    """
    async with engine.async_session() as session, session.begin():
        role_query = await session.execute(
            select(models.GuildRole).where(models.GuildRole.discord_guild_id == discord_guild_id)
        )
        role = role_query.scalars().first()
        if role is not None:
            role.discord_role_id = discord_role_id
            logger.info(f"Updated {discord_guild_id} with new role ID {discord_role_id}.")
            return

        session.add(models.GuildRole(discord_guild_id=discord_guild_id, discord_role_id=discord_role_id))
        logger.info(f"Set Discord role ID {discord_role_id} for guild ID {discord_guild_id}.")


async def get_verify_role(discord_guild_id: int) -> models.GuildRole | None:
    """
    Get the verify role ID or none if none is set.

    Args:
        discord_guild_id: The Discord guild ID to search for.

    Returns:
        A GuildRole instance or None if no information exists.
    """
    async with engine.async_session() as session, session.begin():
        role_query = await session.execute(
            select(models.GuildRole).where(models.GuildRole.discord_guild_id == discord_guild_id)
        )
        return role_query.scalars().first()
