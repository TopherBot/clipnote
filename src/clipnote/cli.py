#!/usr/bin/env python3
"""CLI entry point for ClipNote.

Provides three sub‑commands:
* ``clipnote`` (default) – read clipboard and append.
* ``clipnote -c "text"`` – add custom text.
* ``clipnote -l`` – list recent note files.
"""

import argparse
import datetime
import os
import sys
from pathlib import Path
from typing import List

import pyperclip

APP_DIR = Path.home() / ".clipnote"
APP_DIR.mkdir(parents=True, exist_ok=True)


def _note_path(date: datetime.date = None) -> Path:
    """Return the markdown file for *date* (defaults to today)."""
    if date is None:
        date = datetime.date.today()
    return APP_DIR / f"{date.isoformat()}.md"


def _write_entry(text: str, timestamp: bool = True) -> None:
    """Append *text* as a bullet point to today's note file.

    If *timestamp* is True, a ``HH:MM`` prefix is added.
    """
    if not text.strip():
        print("[clipnote] Nothing to write – empty string supplied.", file=sys.stderr)
        sys.exit(1)
    line = "- "
    if timestamp:
        now = datetime.datetime.now().strftime("%H:%M")
        line += f"[{now}] "
    line += text.rstrip() + "\n"
    note_file = _note_path()
    with note_file.open("a", encoding="utf-8") as f:
        f.write(line)
    print(f"[clipnote] Saved to {note_file}")


def _list_notes(days: int = 7) -> List[Path]:
    """Return a list of note files from the last *days* days, newest first."""
    today = datetime.date.today()
    files = []
    for i in range(days):
        dt = today - datetime.timedelta(days=i)
        p = _note_path(dt)
        if p.is_file():
            files.append(p)
    return files


def _handle_list(args: argparse.Namespace) -> None:
    files = _list_notes(args.days)
    if not files:
        print("[clipnote] No notes found in the last {} days.".format(args.days))
        return
    for p in files:
        print(f"--- {p.name} ---")
        print(p.read_text(encoding="utf-8"))


def _handle_add(args: argparse.Namespace) -> None:
    text = args.text
    if text is None:
        # read from clipboard
        try:
            text = pyperclip.paste()
        except pyperclip.PyperclipException as exc:
            print(f"[clipnote] Clipboard error: {exc}", file=sys.stderr)
            sys.exit(1)
    _write_entry(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clipnote", description="Save clipboard text to a daily markdown note.")
    sub = parser.add_subparsers(dest="command")
    # default command (no subcommand) -> add from clipboard
    parser.set_defaults(func=_handle_add)

    # explicit add from clipboard / custom text
    add_parser = sub.add_parser("add", help="Add text (default: clipboard)")
    add_parser.add_argument("-c", "--text", type=str, help="Custom text to add (skip clipboard)")
    add_parser.set_defaults(func=_handle_add)

    # list notes
    list_parser = sub.add_parser("list", help="List recent notes")
    list_parser.add_argument("-d", "--days", type=int, default=7, help="How many days back to show")
    list_parser.set_defaults(func=_handle_list)

    return parser


def main(argv: List[str] = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    # If no subcommand was given, argparse still sets func to _handle_add via set_defaults.
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
