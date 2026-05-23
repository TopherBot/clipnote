import datetime
import os
from pathlib import Path

import pytest

from clipnote.cli import _note_path, _write_entry, _list_notes, _handle_add, _handle_list
from clipnote.cli import main as cli_main

@pytest.fixture(autouse=True)
def isolated_tmp_path(tmp_path, monkeypatch):
    """Redirect the APP_DIR to a temporary folder for each test."""
    from clipnote import cli as c
    monkeypatch.setattr(c, "APP_DIR", tmp_path)
    yield
    # cleanup is automatic via tmp_path fixture

def test_write_and_read_entry():
    _write_entry("Hello world", timestamp=False)
    note_file = _note_path()
    assert note_file.is_file()
    content = note_file.read_text()
    assert "Hello world" in content
    assert content.startswith("- ")

def test_write_entry_fails_on_empty():
    with pytest.raises(SystemExit):
        _write_entry("   ")

def test_list_notes_order():
    # create notes for today and yesterday
    today = Path(_note_path())
    yesterday = Path(_note_path(datetime.date.today() - datetime.timedelta(days=1)))
    today.write_text("- today\n")
    yesterday.write_text("- yesterday\n")
    notes = _list_notes(days=2)
    assert notes[0] == today
    assert notes[1] == yesterday

def test_cli_add_from_clipboard(monkeypatch, capsys):
    # patch pyperclip.paste to return a known string
    monkeypatch.setattr("pyperclip.paste", lambda: "Clipboard text")
    _handle_add(type('Args', (), {"text": None}))
    captured = capsys.readouterr()
    assert "Saved to" in captured.out
    note_file = _note_path()
    assert "Clipboard text" in note_file.read_text()

def test_cli_add_custom_text(monkeypatch, capsys):
    _handle_add(type('Args', (), {"text": "Custom note"}))
    note_file = _note_path()
    assert "Custom note" in note_file.read_text()

def test_cli_list_output(monkeypatch, capsys):
    # create a single note file
    _write_entry("First entry", timestamp=False)
    args = type('Args', (), {"days": 1})
    _handle_list(args)
    out = capsys.readouterr().out
    assert "First entry" in out
    assert "---" in out

def test_main_no_args(monkeypatch, capsys):
    monkeypatch.setattr("pyperclip.paste", lambda: "Auto clip")
    cli_main([])
    out = capsys.readouterr().out
    assert "Saved to" in out
