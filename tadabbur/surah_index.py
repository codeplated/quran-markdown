"""
One page per surah folder: the surah itself.

Without it the site invents a folder page: "286 items under this folder",
every entry titled the same, sorted as text — 2_1, 2_10, 2_100, 2_2 — with
each note's tags stacked beside it. Nothing there says what the surah is.

Until 2026-10-16 the page answered that with a heading, a 640px picture, a
table of themes and a run of ayah numbers: the first number was 2.3 phone
screens down, and the surah's own words were not on its page at all. Now a
short head says what the surah is called, where it sits and what runs through
it, and under it is the whole text, ayah by ayah, each a link to its own page.
"""

import config
import quranConnections as connections
from tadabbur import data, notes

# Says what kind of page this is, so the site leaves out its own title,
# properties box and reading time: the note's head says them.
SURAH_CLASS = "surah"

# How many themes the head names. The rest are one click away, folded under
# it: Al-Baqarah alone carries over fifty, and listed in full they pushed the
# first ayah two phone screens down.
THEME_LIMIT = 8

# The thumbnails are 1280×720. In the head they sit beside the surah's name,
# not above it, so the text starts on the first screen.
THUMBNAIL_WIDTH = 320


def note_path(number: int) -> str:
    """
    Vault path of a surah's index note, used for links between them.

    Wikilinks resolve from the vault root, and 114 notes are called 'index',
    so a bare [[index]] is ambiguous — the path is what makes it land.
    """
    return data.SURAHS[number].index_path


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


def _theme_link(number: int, key: str) -> str:
    """A theme, linked to this surah's ayaat on the theme's page."""
    title = connections.THEMES[key][1]
    return f"[[{config.THEMES_DIR}/{key}#surah-{number}|{title}]]"


def _head_themes(number: int, themes: list) -> str:
    """The surah's most frequent themes, each with how many of its ayaat carry it."""
    if not themes:
        return "_No themes tagged in this surah yet._"
    shown = " · ".join(
        f'{_theme_link(number, key)} <span class="count">{count}</span>'
        for key, count in themes[:THEME_LIMIT]
    )
    return f"**Themes:** {shown}"


def _all_themes(number: int, themes: list) -> str:
    """Every theme in the surah, folded, when the head could not name them all."""
    if len(themes) <= THEME_LIMIT:
        return ""
    lines = "".join(
        f"- {_theme_link(number, key)} "
        f'<span lang="ur">{connections.THEMES[key][2]}</span> '
        f'{notes.index_count(count, "ayah", "ayaat")}\n'
        for key, count in themes
    )
    return f"""
<details class="surah-themes">
<summary>All {len(themes)} themes in this surah</summary>

{lines}
</details>
"""


def _ayah(surah: data.Surah, ayah: int, texts: dict) -> str:
    """
    One ayah in the surah's text: its number, which leads to the ayah's own
    page (tafsir, recitation), then the Arabic, English and Urdu, then its
    themes. One item of a list, a line each, so Obsidian shows it as written
    and the site can lay the parts out and hide a language.

    The Arabic carries the ayah's number as its id, so a link to #255 lands
    on it; the ayah's own page links back that way.
    """
    tags = connections.get_ayah_themes(surah.number, ayah)
    themes = notes.theme_links(tags, connections.THEMES, config.THEMES_DIR)
    lines = [
        f"- [[{surah.note_name(ayah)}|{ayah}]] "
        f'<span lang="ar" id="{ayah}">{texts["arabic"]}</span>',
        f'  <span lang="en">{texts["english"]}</span>',
        f'  <span lang="ur">{texts["urdu"]}</span>',
    ]
    if themes:
        lines.append(f"  {themes}")
    return "\n".join(lines) + "\n"


def _text(surah: data.Surah) -> str:
    """The whole surah, ayah by ayah, with the Bismillah over it where it has one."""
    key = str(surah.number)
    opening = (
        f'<p class="bismillah" lang="ar">{config.BISMILLAH}</p>\n\n'
        if surah.number not in (1, 9) else ""
    )
    ayaat = "".join(
        _ayah(surah, ayah, {
            "arabic": data.quran[key][ayah - 1]["text"],
            "english": data.english[key][ayah - 1]["text"],
            "urdu": data.urdu[key][ayah - 1]["text"],
        })
        for ayah in range(1, surah.total_ayaat + 1)
    )
    return opening + ayaat


def _neighbours(number: int) -> str:
    """Links to the surah before and after, so the whole Quran is walkable."""
    links = []
    if number > 1:
        previous = data.SURAHS[number - 1]
        links.append(f"[[{note_path(number - 1)}|← {previous.transliteration}]]")
    if number < data.SURAH_COUNT:
        following = data.SURAHS[number + 1]
        links.append(f"[[{note_path(number + 1)}|{following.transliteration} →]]")

    return " · ".join(links)


def build(surah: data.Surah) -> str:
    """
    Frontmatter plus the script-owned block for one surah's page.

    The page is the surah itself. A short head says what it is, where it sits
    and what runs through it; then every ayah in order, readable through,
    each a step from its own page.
    """
    revelation = surah.type.capitalize()
    themes = theme_counts(surah.number)

    head = notes.frontmatter({
        "title": notes.quote(f"{surah.folder_name} {surah.arabic}"),
        "surah": f"{surah.number} / {data.SURAH_COUNT}",
        "surah_name": notes.quote(f"{surah.english} / {surah.arabic} / {surah.urdu}"),
        "transliteration": notes.quote(surah.transliteration),
        "type": surah.type,
        "ayaat": surah.total_ayaat,
        "image": notes.quote(f"/{config.ATTACHMENTS_DIR}/surah_{surah.number:03}.png"),
        "cssclasses": f"[{SURAH_CLASS}]",
    })

    body = f"""![[surah_{surah.number:03}.png|{THUMBNAIL_WIDTH}]]

# {surah.transliteration} {surah.arabic}

{surah.english} · <span lang="ur">{surah.urdu}</span>

> Surah {surah.number} of {data.SURAH_COUNT} · {revelation} · {surah.total_ayaat} ayaat · {_neighbours(surah.number)}
>
> {_head_themes(surah.number, themes)}
{_all_themes(surah.number, themes)}
## Ayaat

{_text(surah)}"""

    return head + notes.wrap(body)


def generate() -> tuple:
    """Writes one index note per surah folder. Returns (created, updated)."""
    created = updated = 0

    for number in range(1, data.SURAH_COUNT + 1):
        surah = data.SURAHS[number]
        is_new = notes.write_note(
            config.VAULT_PATH / surah.folder,
            "index.md",
            build(surah),
            notes.SURAH_PERSONAL,
        )
        if is_new:
            created += 1
        else:
            updated += 1

    return created, updated
