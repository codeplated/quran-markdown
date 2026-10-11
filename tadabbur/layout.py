"""
Moves a vault written by an earlier version into the current layout.

The vault has one top-level folder per section: The Quran/ (a folder per
surah), Personalities/ and Asma Ul Husna/. Earlier versions put the surah
folders at the top level and the other two under '0 - Explore'. Whole folders
move, so every note keeps what the reader wrote below GENERATED:END.

Runs before anything is written, whatever part of the build was asked for:
a step that wrote into the new layout first would make the move impossible.
"""

import shutil
from pathlib import Path

import config
from tadabbur import data, explore


def _move(old: Path, new: Path) -> bool:
    """Moves a folder unless there is nothing to move or the target exists."""
    if not old.is_dir() or new.exists():
        return False
    new.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(old), str(new))
    return True


def _surah_folders(vault: Path) -> int:
    moved = 0
    for surah in data.SURAHS.values():
        # At the top level, named '2 - The Cow البقرة', then '2 The Cow',
        # then '2 - The Cow'.
        for old_name in (f"{surah.number} - {surah.english} {surah.arabic}",
                         f"{surah.number} {surah.english}",
                         surah.folder_name):
            moved += _move(vault / old_name, vault / surah.folder)
    return moved


def _explore_folder(vault: Path) -> int:
    legacy = vault / config.LEGACY_EXPLORE_DIR
    if not legacy.is_dir():
        return 0

    moved = (_move(legacy / "Personalities", vault / config.PERSONALITIES_DIR)
             + _move(legacy / "Asma Ul Husna", vault / config.ASMA_DIR))

    # Listings the generator rebuilt wholesale, with nothing of the reader's
    # in them. The home page's cards replace the Explore page, and the Themes
    # note is written at its new place.
    for name in explore.RETIRED_EXPLORE_NOTES:
        (legacy / name).unlink(missing_ok=True)

    # Quran.base may carry changes made in Obsidian; only a copy the
    # generator wrote and nobody edited is removed. The Quran's own page
    # holds the same view now.
    base = legacy / "Quran.base"
    if base.exists() and base.read_text(encoding="utf-8") in explore.GENERATED_QURAN_BASES:
        base.unlink()

    if not any(legacy.iterdir()):
        legacy.rmdir()
    else:
        print(f"  note: kept {legacy}: it holds files the generator didn't write")

    return moved


def migrate(vault: Path | None = None) -> int:
    """Moves old folders into the current layout. Returns how many moved."""
    vault = Path(vault or config.VAULT_PATH)
    if not vault.is_dir():
        return 0
    return _surah_folders(vault) + _explore_folder(vault)
