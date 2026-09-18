"""
One index note per surah folder.

Without it the site invents a folder page: "286 items under this folder",
every entry titled the same, sorted as text — 2_1, 2_10, 2_100, 2_2 — with
each note's tags stacked beside it. Nothing there says what the surah is.

This note answers that: what the surah is called in three languages, where
and how long it is, which themes run through it, and every ayah in order.
"""

import config
import quranConnections as connections
from tadabbur import data, notes

# Enough themes to characterise a surah without turning the page into a tag
# dump. Al-Baqarah alone carries over fifty.
THEME_LIMIT = 12

# The thumbnails are 1280×720; full width they would push the surah's own
# text off the first screen.
THUMBNAIL_WIDTH = 640


def note_path(number: int) -> str:
    """
    Vault path of a surah's index note, used for links between them.

    Wikilinks resolve from the vault root, and 114 notes are called 'index',
    so a bare [[index]] is ambiguous — the path is what makes it land.
    """
    return f"{data.SURAHS[number].folder_name}/index"


def theme_counts(number: int) -> list:
    """(theme key, how many ayaat carry it) for one surah, most used first."""
    counts = {}
    for (surah, _ayah), tags in connections.AYAH_TAGS.items():
        if surah != number:
            continue
        for tag in tags:
            if tag in connections.THEMES:
                counts[tag] = counts.get(tag, 0) + 1

    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def _themes_table(number: int) -> str:
    themes = theme_counts(number)
    if not themes:
        return "_No themes tagged in this surah yet._\n"

    lines = ["| Theme | Ayaat |\n", "|-------|-------|\n"]
    for key, count in themes[:THEME_LIMIT]:
        _category, title, urdu, _description = connections.THEMES[key]
        lines.append(f"| **{title}** {urdu} [#{key}](tags/{key}) | {count} |\n")

    remaining = len(themes) - THEME_LIMIT
    if remaining > 0:
        lines.append(f"\n_And {remaining} more themes across the surah._\n")

    return "".join(lines)


def _ayah_links(surah: data.Surah) -> str:
    """Every ayah as a numbered link, in order — the folder listing can't sort them."""
    return " · ".join(
        f"[[{surah.note_name(ayah)}|{ayah}]]"
        for ayah in range(1, surah.total_ayaat + 1)
    )


def _neighbours(number: int) -> str:
    """Links to the surah before and after, so the whole Quran is walkable."""
    links = []
    if number > 1:
        previous = data.SURAHS[number - 1]
        links.append(f"[[{note_path(number - 1)}|← {number - 1} · {previous.english}]]")
    if number < data.SURAH_COUNT:
        following = data.SURAHS[number + 1]
        links.append(f"[[{note_path(number + 1)}|{number + 1} · {following.english} →]]")

    return " · ".join(links)


def build(surah: data.Surah) -> str:
    """Frontmatter plus the script-owned block for one surah's index."""
    revelation = surah.type.capitalize()
    transliteration = data.chapters_en[surah.number - 1]["transliteration"]

    head = notes.frontmatter({
        "surah": f"{surah.number} / {data.SURAH_COUNT}",
        "surah_name": notes.quote(f"{surah.english} / {surah.arabic} / {surah.urdu}"),
        "transliteration": notes.quote(transliteration),
        "type": surah.type,
        "ayaat": surah.total_ayaat,
        "image": notes.quote(f"/{config.ATTACHMENTS_DIR}/surah_{surah.number:03}.png"),
    })

    body = f"""# {surah.number} — {transliteration} · {surah.english} · {surah.arabic}
### {surah.urdu}

![[surah_{surah.number:03}.png|{THUMBNAIL_WIDTH}]]

> **Revealed:** {revelation} · **Ayaat:** {surah.total_ayaat} · **Surah {surah.number} of {data.SURAH_COUNT}**

---

## Themes in this surah

{_themes_table(surah.number)}
---

## Ayaat

{_ayah_links(surah)}
"""

    neighbours = _neighbours(surah.number)
    if neighbours:
        body += f"""
---

{neighbours}
"""

    return head + notes.wrap(body)


def generate() -> tuple:
    """Writes one index note per surah folder. Returns (created, updated)."""
    created = updated = 0

    for number in range(1, data.SURAH_COUNT + 1):
        surah = data.SURAHS[number]
        is_new = notes.write_note(
            config.VAULT_PATH / surah.folder_name,
            "index.md",
            build(surah),
            notes.SURAH_PERSONAL,
        )
        if is_new:
            created += 1
        else:
            updated += 1

    return created, updated
