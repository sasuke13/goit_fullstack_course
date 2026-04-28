from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from db import get_engine, get_session_factory
from models import Address, Base, Course, Profile, Student, User


def reset_db() -> None:
    engine = get_engine(echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def seed_data() -> None:
    SessionLocal = get_session_factory(echo=True)
    with SessionLocal() as session:
        ann = User(
            username="ann",
            email="ann@example.com",
            age=22,
            profile=Profile(bio="Backend enthusiast"),
            addresses=[
                Address(city="Kyiv", street="Khreshchatyk 1"),
                Address(city="Dnipro", street="Central 22"),
            ],
        )
        ivan = User(
            username="ivan",
            email="ivan@example.com",
            age=27,
            profile=Profile(bio="Data engineer"),
            addresses=[Address(city="Lviv", street="Bandery 7")],
        )

        py = Course(title="Python Web")
        db = Course(title="Databases")
        student_1 = Student(full_name="Olena Shevchenko", courses=[py, db])
        student_2 = Student(full_name="Taras Bondar", courses=[db])

        session.add_all([ann, ivan, student_1, student_2])
        session.commit()


def run_queries() -> None:
    SessionLocal = get_session_factory(echo=True)
    with SessionLocal() as session:
        # print("\n[ORM] Basic select + filter:")
        # users = session.scalars(select(User).where(User.age >= 23)).all()
        # for user in users:
        #     print("-", user)

        # print("\n[ORM] JOIN users -> addresses:")
        # rows = session.execute(
        #     select(User.username, Address.city).join(
        #         Address, User.id == Address.user_id
        #     ),
        # ).all()
        # for row in rows:
        #     print(f"- {row.username}: {row.city}")

        # print("\n[ORM] Aggregation:")
        # users_count = session.scalar(select(func.count(User.id)))
        # avg_age = session.scalar(select(func.avg(User.age)))
        # print(f"- users count: {users_count}")
        # print(f"- average age: {avg_age:.2f}")

        print("\n[ORM] Eager loading (selectinload addresses):")
        users_with_addresses = session.scalars(
            select(User).options(selectinload(User.addresses)).order_by(User.id),
        ).all()
        for user in users_with_addresses:
            cities = ", ".join(address.city for address in user.addresses)
            print(f"- {user.username}: {cities}")

        print("\n[ORM] Eager loading one-to-one (joinedload profile):")
        users_with_profiles = session.scalars(
            select(User).options(joinedload(User.profile)).order_by(User.id),
        ).all()
        for user in users_with_profiles:
            bio = user.profile.bio if user.profile else "No profile"
            print(f"- {user.username}: {bio}")

        # print("\n[ORM] Update entity:")
        # ann = session.scalar(select(User).where(User.username == "ann"))
        # if ann:
        #     ann.age = 23
        #     session.commit()
        #     print("- ann age updated to 23")

        # print("\n[ORM] Delete entity with cascading addresses/profile:")
        # ivan = session.scalar(select(User).where(User.username == "ivan"))
        # if ivan:
        #     session.delete(ivan)
        #     session.commit()
        #     print("- ivan deleted")

        # print("\n[ORM] Rollback example:")
        # try:
        #     session.add(User(username="ann", email="duplicate@example.com"))
        #     session.commit()
        # except Exception as exc:
        #     session.rollback()
        #     print(f"- rollback executed after error: {exc.__class__.__name__}")


def run_sync_orm_demo() -> None:
    reset_db()
    seed_data()
    run_queries()


if __name__ == "__main__":
    run_sync_orm_demo()
