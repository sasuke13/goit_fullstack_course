from sqlalchemy import event
from sqlalchemy.orm import Session as ORMSession

from connect import SessionLocal, engine
from models import Base, User


@event.listens_for(User, "before_insert")
def before_insert_user(mapper, connection, target):
    if len(target.username.strip()) < 3:
        raise ValueError("before_insert: username too short")
    if target.age < 18:
        raise ValueError("before_insert: age must be >= 18")
    print(f"[EVENT] before_insert for: {target.username}")


@event.listens_for(User, "before_update")
def before_update_user(mapper, connection, target):
    print(f"[EVENT] before_update for: {target.username}")


@event.listens_for(User, "after_insert")
def after_insert_user(mapper, connection, target):
    print(f"[EVENT] after_insert for: {target.username}")


@event.listens_for(User, "before_delete")
def before_delete_user(mapper, connection, target):
    print(f"[EVENT] before_delete for: {target.username}")


@event.listens_for(ORMSession, "before_flush")
def before_flush_session(session, flush_context, instances):
    print(
        f"[EVENT] before_flush: new={len(session.new)}, "
        f"dirty={len(session.dirty)}, deleted={len(session.deleted)}"
    )


@event.listens_for(ORMSession, "after_commit")
def after_commit_session(session):
    print("[EVENT] after_commit")


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        # INSERT -> before_flush, before_insert, after_insert, after_commit
        user = User(username="Alice", age=25)
        session.add(user)
        session.commit()

        # UPDATE -> before_flush, before_update, after_commit
        user.username = "Alice Cooper"
        session.commit()

        # DELETE -> before_flush, before_delete, after_commit
        session.delete(user)
        session.commit()
