from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from sqlite3 import Connection

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "pep249_practice.db"


@contextmanager
def create_connection(db_file: Path):
    conn = sqlite3.connect(db_file)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_tables(conn: Connection) -> None:
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS projects (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      begin_date TEXT,
      end_date TEXT
    );
    """,
    )
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      priority INTEGER,
      project_id INTEGER NOT NULL,
      status BOOLEAN DEFAULT FALSE,
      begin_date TEXT NOT NULL,
      end_date TEXT NOT NULL,
      FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """,
    )


def seed_data(conn: Connection) -> None:
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks;")
    cur.execute("DELETE FROM projects;")
    cur.execute(
        "INSERT INTO projects(name, begin_date, end_date) VALUES(?, ?, ?);",
        ("Cool App with SQLite & Python", "2022-01-01", "2022-01-30"),
    )
    project_id = cur.lastrowid
    cur.executemany(
        """
    INSERT INTO tasks(name, priority, status, project_id, begin_date, end_date)
    VALUES(?, ?, ?, ?, ?, ?);
    """,
        [
            ("Analyze requirements", 1, True, project_id, "2022-01-01", "2022-01-02"),
            (
                "Confirm top requirements",
                1,
                False,
                project_id,
                "2022-01-03",
                "2022-01-05",
            ),
        ],
    )
    cur.close()


def select_examples(conn: Connection) -> None:
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects;")
    projects = cur.fetchall()
    print("\n[PEP249] Projects:", projects)

    cur.execute("SELECT * FROM tasks;")
    tasks = cur.fetchall()
    print("[PEP249] All tasks:", tasks)

    cur.execute("SELECT * FROM tasks WHERE status=?;", (True,))
    done_tasks = cur.fetchall()
    print("[PEP249] Completed tasks:", done_tasks)
    cur.close()


def update_and_delete_examples(conn: Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET priority=?, begin_date=?, end_date=? WHERE id=?;",
        (2, "2022-01-04", "2022-01-06", 1),
    )
    cur.execute("UPDATE tasks SET status=? WHERE id=?;", (True, 2))
    cur.execute("DELETE FROM tasks WHERE id=?;", (1,))
    cur.close()


def run_pep249_demo() -> None:
    with create_connection(DB_PATH) as conn:
        create_tables(conn)
        seed_data(conn)
        select_examples(conn)
        update_and_delete_examples(conn)
        select_examples(conn)


if __name__ == "__main__":
    run_pep249_demo()
