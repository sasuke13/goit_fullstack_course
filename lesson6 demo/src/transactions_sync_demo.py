from connect import SessionLocal, engine
from models import Base, User


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        try:
            with session.begin():
                session.add(User(username="Bob", age=30))
                session.add(User(username="Kate", age=28))
            print("Transaction committed successfully")
        except Exception as err:
            session.rollback()
            print(f"Transaction rolled back: {err}")
