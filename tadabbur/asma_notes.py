"""
The 99 Names of Allah.

These notes used to be written straight to disk with no GENERATED:START
sentinel and no read-back, so anything written under them was lost on the
next run. They now go through notes.write_note like every other note.
"""

import json

import config
from tadabbur import data, notes


def build(name: dict) -> str:
    """Frontmatter plus the script-owned block for one Name."""
    ayah_links = "\n".join(
        data.wikilink(surah, ayah) for surah, ayah in name["key_ayaat"]
    ) or "_No ayaat recorded._"

    head = notes.frontmatter({
        "number": name["number"],
        "name": (
            f"{name['english']} / {name['arabic']} / "
            f"{name['urdu']} / {name['transliteration']} / {name['root']}"
        ),
        "root_meaning": name["root_meaning"],
        "category": name["category"],
        "quran_occurrences": name["quran_occurrences"],
        "key_ayaat": name["key_ayaat"],
        "tags": json.dumps(name.get("tags", [])),
    })

    body = f"""## English Explanation

{name['explanation']}

## Urdu Explanation

{name['urdu_explanation']}

## Daily Life

{name['daily_life']}

## Key Ayaat

{ayah_links}
"""

    return head + notes.wrap(body)


def generate() -> tuple:
    """Writes one note per Name. Returns (created, updated)."""
    folder = config.VAULT_PATH / config.ASMA_DIR
    created = updated = 0

    for name in data.asma_ul_husna:
        is_new = notes.write_note(
            folder,
            f"{name['number']} - {name['arabic']}.md",
            build(name),
            notes.ASMA_PERSONAL,
        )
        if is_new:
            created += 1
        else:
            updated += 1

    return created, updated
