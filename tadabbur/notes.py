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
## 📝 Tafsir Notes


## 💡 Personal Reflection


## 🔗 Thematic Links

"""

PERSONALITY_PERSONAL = """
## 📝 Study Notes


## 💡 Personal Reflection


## 🔗 Related Ayaat & Personalities

"""

ASMA_PERSONAL = """
## 📝 Study Notes


## 💡 Personal Reflection

"""

# Headings used before sentinels existed, migrated once on first rewrite.
_LEGACY_HEADINGS = ("## Tafsir Notes", "## Personal Reflection", "## 🔗 Thematic Links")


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
        return after if after.strip() else default

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


def wrap(generated_body: str) -> str:
    """Puts the sentinels around script-owned content."""
    return f"{config.SENTINEL_START}\n{generated_body}\n{config.SENTINEL_END}"
