from connect import SessionLocal
from models import Note, Record, Tag


if __name__ == "__main__":
    with SessionLocal() as session:
        tag1 = Tag(name="groceries")
        tag2 = Tag(name="food")

        note = Note(name="Go to the store")
        note.tags = [tag1, tag2]
        note.records = [
            Record(description="Buy bread"),
            Record(description="Buy sausage 0.5 kg"),
            Record(description="Buy tomatoes 1 kg"),
        ]

        session.add(note)
        session.commit()

        print("Seed completed")
