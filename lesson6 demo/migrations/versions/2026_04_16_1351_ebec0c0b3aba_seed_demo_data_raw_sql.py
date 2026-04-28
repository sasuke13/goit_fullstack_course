"""seed demo data raw sql

Revision ID: ebec0c0b3aba
Revises: 4676c07737d9
Create Date: 2026-04-16 13:50:12.324409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebec0c0b3aba'
down_revision: Union[str, Sequence[str], None] = '4676c07737d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert demo data using raw SQL."""
    conn = op.get_bind()

    conn.execute(
        sa.text(
            """
            INSERT OR IGNORE INTO notes (id, name, created)
            VALUES (1, 'Go to the store', CURRENT_TIMESTAMP)
            """
        )
    )

    conn.execute(
        sa.text(
            """
            INSERT OR IGNORE INTO tags (id, name)
            VALUES
              (1, 'groceries'),
              (2, 'food')
            """
        )
    )

    conn.execute(
        sa.text(
            """
            INSERT OR IGNORE INTO records (id, description, done, note_id)
            VALUES
              (1, 'Buy bread', 0, 1),
              (2, 'Buy sausage 0.5 kg', 0, 1),
              (3, 'Buy tomatoes 1 kg', 0, 1)
            """
        )
    )

    conn.execute(
        sa.text(
            """
            INSERT OR IGNORE INTO note_m2m_tag (note_id, tag_id)
            VALUES
              (1, 1),
              (1, 2)
            """
        )
    )


def downgrade() -> None:
    """Remove only data inserted by this migration."""
    conn = op.get_bind()

    conn.execute(
        sa.text("DELETE FROM note_m2m_tag WHERE note_id = 1 AND tag_id IN (1, 2)")
    )
    conn.execute(sa.text("DELETE FROM records WHERE id IN (1, 2, 3)"))
    conn.execute(sa.text("DELETE FROM tags WHERE id IN (1, 2)"))
    conn.execute(sa.text("DELETE FROM notes WHERE id = 1"))
