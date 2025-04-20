"""
Create, Read, Update and Delete operations in the database.
"""

from loguru import logger
from sqlalchemy import delete, select

from obearon.database import engine
from obearon.database import models


async def create_verification(discord_guild_id: int, discord_user_id: int, verification_code: int) -> str | None:
    """
    Creates a pending verification.

    Args:
        discord_guild_id: The guild in which the discord user wants to be verified.
        discord_user_id: The discord user ID to verify.
        verification_code: The verification code the user needs to send us.

    Returns:
        The verification code if there is a pending verification, None if the verification was created.
    """
    async with engine.async_session() as session, session.begin():
        verification_query = await session.execute(
            select(models.Verification).where(
                models.Verification.discord_guild_id == discord_guild_id,
                models.Verification.discord_user_id == discord_user_id,
            )
        )
        verification = verification_query.scalars().first()
        if verification is not None:
            logger.info(f"{discord_user_id} already has a pending verification in {discord_guild_id}.")
            return verification.verification_code

        session.add(
            models.Verification(
                discord_guild_id=discord_guild_id,
                discord_user_id=discord_user_id,
                verification_code=verification_code,
            )
        )
        return None


async def update_warframe_name(verification_code: int, warframe_name: str) -> None:
    """
    Update the warframe name for a verification code.

    Args:
        verification_code: The verification code we received.
        warframe_name: The warframe name we parsed.
    """
    async with engine.async_session() as session, session.begin():
        verification_query = await session.execute(
            select(models.Verification).where(
                models.Verification.verification_code == verification_code, models.Verification.verified.is_(False)
            )
        )
        verification = verification_query.scalars().first()
        if verification is None:
            logger.info(f"{warframe_name} entered an invalid verification code ({verification_code}).")
            return

        verification.warframe_name = warframe_name
        verification.verified = True
        logger.info(f"{warframe_name} ({verification.discord_user_id}) has been marked as verified.")


async def get_successful_verifications() -> list[models.Verification]:
    """
    Get all successful verifications.

    Returns:
        A list of successful verifications.
    """
    async with engine.async_session() as session, session.begin():
        verification_query = await session.execute(
            select(models.Verification).where(models.Verification.verified.is_(True))
        )
        return verification_query.scalars().all()


async def remove_verification(discord_user_id: int) -> None:
    """
    Remove a verification because the role has been given.

    Args:
        discord_user_id: The Discord ID of the user to remove the verification for.
    """
    async with engine.async_session() as session, session.begin():
        await session.execute(
            delete(models.Verification).where(models.Verification.discord_user_id == discord_user_id)
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
