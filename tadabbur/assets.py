"""
Files copied into the vault rather than generated: surah thumbnails, and the
hand-made notes and canvases under vault_files/.
"""

import shutil

import config


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
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1

    return copied
