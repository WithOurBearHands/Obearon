"""
Create, Read, Update and Delete operations in the database.
"""
from sqlalchemy import select, update

from bearification.database import engine, models


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
            user.warframe_name = None
            user.verified = False
            user.linked = False
            user.verification_code = verification_code
            print(f"Updated {user.warframe_name} with new verification code.")
            return

        session.add(
            models.User(
                discord_guild_id=discord_guild_id, discord_user_id=discord_user_id, verification_code=verification_code
            )
        )
        print(f"Added Discord ID {discord_user_id} with verification code {verification_code}.")


async def update_warframe_name(verification_code: int, warframe_name: str) -> None:
    """
    Update the warframe name for a verification code.

    Args:
        verification_code: The verification code we received.
        warframe_name: The warframe name we parsed.
    """
    async with engine.async_session() as session, session.begin():
        user_query = await session.execute(
            select(models.User)
            .where(
                models.User.verification_code == verification_code,
                models.User.verified.is_(False)
            )
        )
        user = user_query.scalars().first()
        if user is None:
            print(f"{warframe_name} entered an invalid verification code ({verification_code}).")
            return

        user.warframe_name = warframe_name
        user.verified = True
        print(f"{warframe_name} ({user.discord_user_id}) has been marked as verified.")


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
