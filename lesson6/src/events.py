from sqlalchemy import event
from sqlalchemy.orm import Session
from datetime import datetime
from models import User, Base, Note, async_engine, async_session
import asyncio

@event.listens_for(User, "before_update")
def before_update_user(mapper, connection, target):
    if target.age < 18:
        raise ValueError("Age must be greater than 18")
    target.updated_at = datetime.now()
    # connection.execute(update(User).where(User.id == target.id).values(updated_at=datetime.now()))

@event.listens_for(User, "before_insert")
def before_insert_user(mapper, connection, target):
    if target.age < 18:
        raise ValueError("Age must be greater than 18")
    target.updated_at = datetime.now()

@event.listens_for(User, "before_delete")
def before_delete_user(mapper, connection, target):
    print("before_delete")

@event.listens_for(User, "after_insert")
def after_insert_user(mapper, connection, target):
    print("after_insert")

@event.listens_for(Session, "before_flush")
def before_flush_user(session, connection, targets):
    print("before_flush")

@event.listens_for(Session, "after_commit")
def after_commit_user(session):
    print("after_commit")

# async def main():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
    
#     async with async_session() as session:
#         user = User(username="test1245556768", age=19, notes=[Note(title="test")])
#         session.add(user)
#         await session.commit()
    
#         user = await session.get(User, user.id)
#         user.age = 20
#         # user.updated_at = datetime.now()
#         await session.commit()


# if __name__ == "__main__":
#     asyncio.run(main())
