"""
Files copied into the vault rather than generated: surah thumbnails, and the
hand-made notes and canvases under vault_files/.
"""

import json
import re
import shutil

import config
from tadabbur import data

# An ayah note's vault path in any layout, old or current:
# "2 - The Cow البقرة/2_255: The Cow البقرة.md", "2 The Cow/2_255.md",
# "2 - The Cow/2_255.md". A current path maps to itself.
OLD_AYAH_PATH = re.compile(r"(\d+) [^/]+/(\d+)_(\d+)(?:: [^/]+)?\.md")


def copy_thumbnails() -> int:
    """
    Mirrors surah_*.png into the vault's attachments folder, skipping files
    already up to date. Returns how many were copied.
    """
    source = config.THUMBNAILS_SRC
    destination = config.VAULT_PATH / config.ATTACHMENTS_DIR

    if not source.is_dir():
        print(f"  warning: no thumbnails at {source} — skipping")
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    copied = 0

    for image in sorted(source.glob("surah_*.png")):
        target = destination / image.name

        if target.exists():
            current, existing = image.stat(), target.stat()
            if current.st_size == existing.st_size and current.st_mtime <= existing.st_mtime:
                continue

        try:
            shutil.copy2(image, target)
            copied += 1
        except OSError as error:
            print(f"  warning: could not copy {image.name}: {error}")

    return copied


def copy_vault_files() -> int:
    """
    Copies vault_files/ into the vault at the same relative paths. Existing
    files are left alone, so edits made inside Obsidian survive.
    """
    source = config.VAULT_FILES_SRC
    if not source.is_dir():
        return 0

    copied = 0

    for item in source.rglob("*"):
        if item.is_dir():
            continue

        target = config.VAULT_PATH / item.relative_to(source)
        if target.exists():
            if target.suffix == ".canvas":
                relink_canvas(target)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1

    return copied


def relink_canvas(path) -> bool:
    """
    Points a canvas's cards at the ayah notes' current paths.

    A canvas stores each card's note as a vault path, and the notes were
    renamed from outside Obsidian, so nothing updated those paths and the
    cards went blank. Only paths in the old ayah layout are rewritten, in
    place, so the rest of the file — edited in Obsidian or not — is kept
    byte for byte. Returns True if the file changed.
    """
    def current(value: re.Match) -> str:
        old = OLD_AYAH_PATH.fullmatch(value[0])
        if not old or old[1] != old[2] or int(old[2]) not in data.SURAHS:
            return value[0]
        surah = data.SURAHS[int(old[2])]
        return f"{surah.folder_name}/{surah.note_name(int(old[3]))}.md"

    text = path.read_text(encoding="utf-8")
    updated = re.sub(r'(?<="file":")[^"]+(?=")', current, text)

    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True
