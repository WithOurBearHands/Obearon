"""add friend role

Revision ID: 4de1e0726e1b
Revises: ccef2015d4be
Create Date: 2025-04-20 17:46:25.419737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4de1e0726e1b'
down_revision: Union[str, None] = 'ccef2015d4be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('guild_role', 'discord_guild_id', new_column_name='guild_id')
    op.alter_column('guild_role', 'discord_role_id', new_column_name='verified_role_id')
    op.add_column('guild_role', sa.Column('friend_role_id', sa.BigInteger(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('guild_role', 'guild_id', new_column_name='discord_guild_id')
    op.alter_column('guild_role', 'verified_role_id', new_column_name='discord_role_id')
    op.drop_column('guild_role', 'friend_role_id')
