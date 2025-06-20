"""create initial tables

Revision ID: ccef2015d4be
Revises:
Create Date: 2025-04-20 16:19:58.182605

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ccef2015d4be"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "guild_role",
        sa.Column("guild_id", sa.BigInteger(), nullable=False),
        sa.Column("verified_role_id", sa.BigInteger(), nullable=True),
        sa.Column("friend_role_id", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("guild_id"),
    )
    op.create_table(
        "verification",
        sa.Column("discord_guild_id", sa.BigInteger(), nullable=False),
        sa.Column("discord_user_id", sa.BigInteger(), nullable=False),
        sa.Column("warframe_name", sa.String(length=24), nullable=True),
        sa.Column("verification_code", sa.Integer(), nullable=True),
        sa.Column("verified", sa.Boolean(), server_default="false", nullable=False),
        sa.PrimaryKeyConstraint("discord_guild_id", "discord_user_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("verification")
    op.drop_table("guild_role")
