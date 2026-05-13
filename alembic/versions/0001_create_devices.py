"""create devices table

Revision ID: 0001_create_devices
Revises:
Create Date: 2026-05-13
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_devices"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.String(length=255), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="off"),
        sa.Column("energy_usage", sa.Float(), nullable=False, server_default="0"),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("brightness", sa.Float(), nullable=True),
        sa.Column("temperature", sa.Float(), nullable=True),
        sa.Column("resolution", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("devices")
