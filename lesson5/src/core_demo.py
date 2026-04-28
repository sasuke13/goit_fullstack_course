from __future__ import annotations

from pathlib import Path

from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, Table,
                        create_engine, insert, select)


def run_core_demo() -> None:
    db_path = Path(__file__).resolve().parent.parent / "data" / "core_practice.db"
    engine = create_engine(f"sqlite+pysqlite:///{db_path}", echo=True, future=True)
    metadata = MetaData()

    users = Table(
        "core_users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50), nullable=False, unique=True),
    )
    addresses = Table(
        "core_addresses",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("city", String(100), nullable=False),
        Column("user_id", Integer, ForeignKey("core_users.id")),
    )

    metadata.drop_all(engine)
    metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(insert(users), [{"name": "Alice"}, {"name": "Bob"}])
        conn.execute(
            insert(addresses),
            [
                {"city": "Kyiv", "user_id": 1},
                {"city": "Lviv", "user_id": 1},
                {"city": "Odesa", "user_id": 2},
            ],
        )

    with engine.connect() as conn:
        rows = conn.execute(
            select(users.c.name, addresses.c.city).join(
                addresses, users.c.id == addresses.c.user_id
            ),
        ).all()
        print("\n[Core] Users with addresses:")
        for row in rows:
            print(f"- {row.name}: {row.city}")


if __name__ == "__main__":
    run_core_demo()
