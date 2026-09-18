"""
ayah_tags — the ayah → theme map, one module per surah (s001.py … s114.py).

Each module defines:
    STATUS = "todo" | "seed" | "deep"
        todo  — no tags yet
        seed  — partial, hand-picked tags from the original seed set
        deep  — every ayah reviewed and tagged (see TAGGING_PROGRESS.md)
    TAGS   = {ayah_number: ["theme_key", ...], ...}

Theme keys must exist in quranConnections.THEMES — run `python tag_audit.py`.
"""

import importlib

SURAH_COUNT = 114
STATUSES = ("todo", "seed", "deep")


def load_surah(surah: int):
    """Imports and returns the module for one surah."""
    return importlib.import_module(f"{__name__}.s{surah:03d}")


def load_all() -> tuple:
    """Returns ({(surah, ayah): [tags]}, {surah: status})."""
    tags, status = {}, {}
    for surah in range(1, SURAH_COUNT + 1):
        module = load_surah(surah)
        status[surah] = module.STATUS
        for ayah, theme_keys in module.TAGS.items():
            tags[(surah, ayah)] = list(theme_keys)
    return tags, status
