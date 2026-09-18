"""
Writing notes without destroying what the reader wrote.

Every generated note has the same shape:

    ---  frontmatter  ---
    <!-- GENERATED:START -->
    ...regenerated from data on every run...
    <!-- GENERATED:END -->
    ...the reader's own notes, never touched...

`write_note` is the only way a note reaches disk, and it always carries the
text after GENERATED:END across from the previous version. That is deliberate:
when Names-of-Allah notes were written through a separate path that skipped
this step, every run silently erased whatever had been written under them.
"""

import os
from pathlib import Path

import config

# Default scaffolding for a note that does not exist yet. Once a note exists,
# whatever the reader has put there wins — these are never re-applied.
AYAH_PERSONAL = """
## Tafsir Notes

"""

PERSONALITY_PERSONAL = """
## Study Notes

"""

ASMA_PERSONAL = """
## Study Notes

"""

SURAH_PERSONAL = """
## Surah Notes

"""

# Every heading the scaffolding has used, including the emoji it used to carry.
# A personal section made of nothing but these has never been written in, so it
# can be replaced with the current scaffolding — that is the only way the old
# emoji headings ever leave the 6,400 notes already in the vault.
_SCAFFOLD_HEADINGS = frozenset({
    "## Tafsir Notes", "## 📝 Tafsir Notes",
    "## Study Notes", "## 📝 Study Notes",
    "## Surah Notes", "## 📝 Surah Notes",
    "## Personal Reflection", "## 💡 Personal Reflection",
    "## Thematic Links", "## 🔗 Thematic Links",
    "## Related Ayaat & Personalities", "## 🔗 Related Ayaat & Personalities",
})


def is_untouched_scaffolding(section: str) -> bool:
    """True when a personal section is bare headings the generator put there."""
    lines = [line.strip() for line in section.splitlines() if line.strip()]
    return bool(lines) and all(line in _SCAFFOLD_HEADINGS for line in lines)

# Headings used before sentinels existed, migrated once on first rewrite.
_LEGACY_HEADINGS = ("## Tafsir Notes", "## 📝 Tafsir Notes", "## Personal Reflection",
                    "## 💡 Personal Reflection", "## Thematic Links", "## 🔗 Thematic Links")


def personal_section(filepath: Path | str, default: str) -> str:
    """
    The reader-owned text that must survive this run.

      note does not exist  → the default scaffolding
      sentinel present     → everything after GENERATED:END, verbatim
      pre-sentinel note    → its old sections, rescued once
    """
    path = Path(filepath)
    if not path.exists():
        return default

    content = path.read_text(encoding="utf-8")

    if config.SENTINEL_END in content:
        after = content.split(config.SENTINEL_END, 1)[1]
        if not after.strip() or is_untouched_scaffolding(after):
            return default
        return after

    return _migrate_legacy(content, default)


def _migrate_legacy(content: str, default: str) -> str:
    """Pulls the old hand-written sections out of a note written before sentinels."""
    import re

    found = []
    for heading in _LEGACY_HEADINGS:
        match = re.search(rf"({re.escape(heading)}.*?)(?=\n## |\Z)", content, re.DOTALL)
        if match:
            found.append(match.group(1).strip())

    return "\n\n" + "\n\n".join(found) + "\n" if found else default


def write_note(folder: Path | str, filename: str, generated: str, default: str) -> bool:
    """
    Writes one note, keeping its personal section. Returns True if it is new.

    `generated` must already end with the GENERATED:END sentinel.
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / filename

    is_new = not filepath.exists()
    kept = personal_section(filepath, default)
    filepath.write_text(generated + kept, encoding="utf-8")

    return is_new


def rename_note(folder: Path | str, old_filename: str, new_filename: str) -> bool:
    """
    Moves a note that an earlier version of the generator named differently.

    The personal section lives in the file, so a rename has to move the file
    rather than write a new one beside it — otherwise the reader's notes stay
    behind in a file nothing regenerates, and the next run creates a fresh
    empty note under the new name. Returns True if a note was moved.
    """
    folder = Path(folder)
    old, new = folder / old_filename, folder / new_filename

    if old_filename == new_filename or not old.exists() or new.exists():
        return False

    old.rename(new)
    return True


def write_plain(folder: Path | str, filename: str, content: str) -> None:
    """
    Writes a fully generated file with no personal section — index notes and
    other listings that are rebuilt wholesale on every run.
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / filename).write_text(content, encoding="utf-8")


def frontmatter(fields: dict) -> str:
    """Renders a YAML frontmatter block. Values are written as given."""
    lines = "\n".join(f"{key}: {value}" for key, value in fields.items())
    return f"---\n{lines}\n---\n"


def quote(value) -> str:
    """
    A YAML-safe scalar for a frontmatter value.

    Frontmatter is written as given, so a value that starts with a YAML
    indicator changes what the line means: surah 80's transliteration is
    'Abasa, and unquoted that opening apostrophe starts a quoted scalar that
    never closes — which fails the whole site build, not just that note.
    """
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def wrap(generated_body: str) -> str:
    """Puts the sentinels around script-owned content."""
    return f"{config.SENTINEL_START}\n{generated_body}\n{config.SENTINEL_END}"
