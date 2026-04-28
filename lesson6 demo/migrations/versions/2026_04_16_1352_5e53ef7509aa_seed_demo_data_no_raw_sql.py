"""seed demo data no raw sql

Revision ID: 5e53ef7509aa
Revises: ebec0c0b3aba
Create Date: 2026-04-16 13:50:13.121873

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e53ef7509aa'
down_revision: Union[str, Sequence[str], None] = 'ebec0c0b3aba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert additional demo data without raw SQL."""
    notes = sa.table(
        "notes",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("created", sa.DateTime),
    )
    tags = sa.table(
        "tags",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )
    records = sa.table(
        "records",
        sa.column("id", sa.Integer),
        sa.column("description", sa.String),
        sa.column("done", sa.Boolean),
        sa.column("note_id", sa.Integer),
    )
    note_m2m_tag = sa.table(
        "note_m2m_tag",
        sa.column("note_id", sa.Integer),
        sa.column("tag_id", sa.Integer),
    )

    op.bulk_insert(
        notes,
        [
            {
                "id": 2,
                "name": "Prepare SQLAlchemy lesson",
                "created": datetime.utcnow(),
            }
        ],
    )
    op.bulk_insert(tags, [{"id": 3, "name": "study"}])
    op.bulk_insert(
        records,
        [
            {"id": 4, "description": "Prepare slides", "done": False, "note_id": 2},
            {"id": 5, "description": "Run live demo", "done": False, "note_id": 2},
        ],
    )
    op.bulk_insert(note_m2m_tag, [{"note_id": 2, "tag_id": 3}])


def downgrade() -> None:
    """Remove only data inserted by this migration."""
    note_m2m_tag = sa.table(
        "note_m2m_tag",
        sa.column("note_id", sa.Integer),
        sa.column("tag_id", sa.Integer),
    )
    records = sa.table(
        "records",
        sa.column("id", sa.Integer),
    )
    tags = sa.table("tags", sa.column("id", sa.Integer))
    notes = sa.table("notes", sa.column("id", sa.Integer))

    op.execute(
        sa.delete(note_m2m_tag).where(
            note_m2m_tag.c.note_id == 2, note_m2m_tag.c.tag_id == 3
        )
    )
    op.execute(sa.delete(records).where(records.c.id.in_([4, 5])))
    op.execute(sa.delete(tags).where(tags.c.id == 3))
    op.execute(sa.delete(notes).where(notes.c.id == 2))
