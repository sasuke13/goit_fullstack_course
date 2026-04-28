from __future__ import annotations

from sqlalchemy import delete, func, insert, select, update

from db import get_engine
from models import Address, Base, User


def reset_tables() -> None:
    engine = get_engine(echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def seed_with_execute() -> None:
    engine = get_engine(echo=True)
    with engine.connect() as connection:
        stmt = insert(User).values(
            [
                {"username": "pylyp", "email": "pylyp@example.com", "age": 25},
                {"username": "mykola", "email": "mykola@example.com", "age": 30},
                {"username": "iryna", "email": "iryna@example.com", "age": 20},
            ],
        )
        connection.execute(stmt)
        connection.execute(
            insert(Address).values(
                [
                    {"street": "Saksahanskoho 57", "city": "Kyiv", "user_id": 1},
                    {"street": "Sobornosti 45", "city": "Poltava", "user_id": 2},
                    {"street": "Sumska 61", "city": "Kharkiv", "user_id": 2},
                ],
            ),
        )
        connection.commit()


def run_select_examples() -> None:
    engine = get_engine(echo=True)
    with engine.connect() as connection:
        print("\n[execute()] All users:")
        for row in connection.execute(select(User)):
            print(row)

        print("\n[execute()] Filter users age > 21:")
        for row in connection.execute(select(User).where(User.age > 21)):
            print(row)

        print("\n[execute()] Sorted + limited users:")
        for row in connection.execute(select(User).order_by(User.username).limit(2)):
            print(row)

        print("\n[execute()] JOIN users + addresses:")
        for row in connection.execute(
            select(User.username, Address.city).join(Address)
        ):
            print(row)

        print("\n[execute()] LEFT JOIN users + addresses:")
        for row in connection.execute(
            select(User.username, Address.city).join(Address, isouter=True)
        ):
            print(row)

        print("\n[execute()] Aggregation count(users):")
        users_count = connection.execute(select(func.count(User.id))).scalar_one()
        print(users_count)


def run_update_delete_examples() -> None:
    engine = get_engine(echo=True)
    with engine.connect() as connection:
        connection.execute(update(User).where(User.username == "pylyp").values(age=26))
        connection.execute(delete(User).where(User.username == "iryna"))
        connection.commit()

        print("\n[execute()] Users after UPDATE + DELETE:")
        for row in connection.execute(
            select(User.username, User.age).order_by(User.id)
        ):
            print(row)


def run_execute_demo() -> None:
    reset_tables()
    seed_with_execute()
    run_select_examples()
    run_update_delete_examples()


if __name__ == "__main__":
    run_execute_demo()
