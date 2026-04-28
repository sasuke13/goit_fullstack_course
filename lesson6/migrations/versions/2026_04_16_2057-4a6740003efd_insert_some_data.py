"""insert_some_data

Revision ID: 4a6740003efd
Revises: 87dc3057023c
Create Date: 2026-04-16 20:57:05.280370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


USERNAMES_LIST = ["test1", "test2", "test3", "test4", "test5"]
AGES_LIST = [18, 19, 20, 21, 22]

# revision identifiers, used by Alembic.
revision: str = '4a6740003efd'
down_revision: Union[str, Sequence[str], None] = '87dc3057023c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    users = sa.table(
        "users",
        sa.column("id", sa.Integer),
        sa.column("username", sa.String),
        sa.column("age", sa.Integer),
        sa.column("created_at", sa.DateTime),
    )
    op.bulk_insert(
        users,
        [{"username": username, "age": age} for username, age in zip(USERNAMES_LIST, AGES_LIST)]
    )


def downgrade() -> None:
    """Downgrade schema."""
    users = sa.table(
        "users",
        sa.column("username", sa.String)
    )
    op.execute(
        users.delete().where(users.c.username.in_(USERNAMES_LIST))
    )
