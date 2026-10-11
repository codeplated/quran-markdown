"""
Moves a vault written by an earlier version into the current layout.

The vault has one top-level folder per section: The Quran/ (a folder per
surah), Personalities/, Asma Ul Husna/ and tags/ (the themes). Earlier
versions put the surah folders at the top level and Personalities and Asma Ul
Husna under '0 - Explore'. Whole folders move, so every note keeps what the
reader wrote below GENERATED:END. The themes folder holds only generated
notes, so there is nothing to move into it.

Runs before anything is written, whatever part of the build was asked for:
a step that wrote into the new layout first would make the move impossible.
"""

import shutil
from pathlib import Path

import config
from tadabbur import data, explore, personalities


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


def _path_pages(vault: Path) -> None:
    """
    Removes the Straight, Mixed and Deviated Path pages, which the tabs on the
    Personalities page replace. They were rebuilt wholesale on every run, so
    nothing of the reader's is in them.
    """
    folder = vault / config.PERSONALITIES_DIR / personalities.RETIRED_PATH_FOLDER
    if not folder.is_dir():
        return
    for name in personalities.RETIRED_PATH_PAGES:
        (folder / name).unlink(missing_ok=True)
    if not any(folder.iterdir()):
        folder.rmdir()


def migrate(vault: Path | None = None) -> int:
    """Moves old folders into the current layout. Returns how many moved."""
    vault = Path(vault or config.VAULT_PATH)
    if not vault.is_dir():
        return 0
    moved = _surah_folders(vault) + _explore_folder(vault)
    _path_pages(vault)
    # The themes are a folder of notes now; this was their one page.
    (vault / explore.RETIRED_THEMES_NOTE).unlink(missing_ok=True)
    return moved
