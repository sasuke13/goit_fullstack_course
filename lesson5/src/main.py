from __future__ import annotations

import argparse
import asyncio

from core_demo import run_core_demo
from execute_demo import run_execute_demo
from orm_async_demo import run_async_orm_demo
from orm_sync_demo import run_sync_orm_demo
from pep249_demo import run_pep249_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SQLAlchemy practice project runner")
    parser.add_argument(
        "--mode",
        choices=["all", "pep249", "core", "sync", "execute", "async"],
        default="all",
        help="Choose which demo to run",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.mode in {"all", "pep249"}:
        run_pep249_demo()
    if args.mode in {"all", "core"}:
        run_core_demo()
    if args.mode in {"all", "sync"}:
        run_sync_orm_demo()
    if args.mode in {"all", "execute"}:
        run_execute_demo()
    if args.mode in {"all", "async"}:
        asyncio.run(run_async_orm_demo())


if __name__ == "__main__":
    main()
