from models import User, Base, Note, async_engine, async_session
import asyncio
import random

# async def main():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     async with async_session() as session:
#         async with session.begin():
#             for i in range(10):
#                 user = User(username=f"test{i}", age=random.randint(16, 19), notes=[Note(title="test")])
#                 print(user)
#                 session.add(user)

#             # await session.commit()


# if __name__ == "__main__":
#     asyncio.run(main())