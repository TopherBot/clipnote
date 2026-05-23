# -*- coding: utf-8 -*-
"""ClipNote package – expose version information.
"""

__all__ = ["__version__"]

# The version is read from the package metadata; fallback to static string for dev.
try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version("clipnote")
except Exception:  # pragma: no cover
    __version__ = "0.1.0"
