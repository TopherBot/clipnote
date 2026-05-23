# ClipNote

**ClipNote** – *One‑liner clipboard saver*.

```
$ pip install clipnote
$ clipnote          # saves current clipboard to today's note
$ clipnote -l       # list notes for the last 7 days
$ clipnote -c "Hello"  # add custom text without touching the clipboard
```

## What it does
- Reads the system clipboard (Windows, macOS, Linux).
- Stores the text in a markdown file under `~/.clipnote/YYYY-MM-DD.md`.
- Adds a timestamped bullet for each entry.
- Minimal dependencies (`pyperclip` and `tomli` for optional config).
- Fully tested and CI‑protected on every push.

## Why this project?
- Demonstrates a **tiny, useful Python package** that follows 2024 best‑practice conventions.
- Shows a clean layout (`src/`, `tests/`).
- Provides a ready‑to‑use GitHub Actions workflow, linting, type‑checking and security scanning.
- Includes a graceful fallback naming strategy – if `clipnote` is taken on PyPI, the installer will automatically rename the distribution to `clipnote‑lite` (see `pyproject.toml`).

## Contributing
Feel free to open issues or PRs. Every contribution runs the full CI suite before merging.

---
_© 2026 TopherBot – released under the MIT License._