from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
DB_PATH = Path(".video_folder_gpt.sqlite3")


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL
        )
        """
    )
    return conn


def index_folder(folder: Path, db_path: Path = DB_PATH) -> int:
    conn = connect(db_path)
    count = 0
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in VIDEO_EXTS:
            conn.execute(
                "INSERT OR REPLACE INTO videos(path, title) VALUES (?, ?)",
                (str(path.resolve()), path.stem.replace("_", " ").replace("-", " ")),
            )
            count += 1
    conn.commit()
    conn.close()
    return count


def search(query: str, db_path: Path = DB_PATH) -> list[tuple[str, str]]:
    conn = connect(db_path)
    rows = conn.execute(
        "SELECT title, path FROM videos WHERE lower(title) LIKE ? ORDER BY title LIMIT 10",
        (f"%{query.lower()}%",),
    ).fetchall()
    conn.close()
    return [(title, path) for title, path in rows]


def answer(query: str, db_path: Path = DB_PATH) -> str:
    rows = search(query, db_path)
    if not rows:
        return "No matching video moments found. Try indexing a folder first."
    lines = [f"Answer for: {query}", ""]
    for i, (title, path) in enumerate(rows, start=1):
        lines.append(f"{i}. {title} — 00:00 — {path}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local video folder search starter")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="Index video files in a folder")
    p_index.add_argument("folder", type=Path)

    p_ask = sub.add_parser("ask", help="Search indexed videos")
    p_ask.add_argument("question")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "index":
        count = index_folder(args.folder)
        print(f"Indexed {count} video(s).")
        return 0
    if args.command == "ask":
        print(answer(args.question))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
