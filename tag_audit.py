"""
tag_audit.py — validates tags everywhere and tracks tagging progress.

    python tag_audit.py                   validate ayaat, personalities, Asma ul Husna & related topics
    python tag_audit.py --write           …and refresh the status table in TAGGING_PROGRESS.md
    python tag_audit.py --themes          …and print how often each theme is used
    python tag_audit.py --surah 18        print surah 18 ayah by ayah with its current tags
    python tag_audit.py --surah 2 --from 142 --to 152

Exits with status 1 if any error is found.
"""

import argparse
import json
import re
import sys
from collections import Counter

import quranConnections as qc

PROGRESS_FILE = "TAGGING_PROGRESS.md"
TABLE_START   = "<!-- AUDIT:START -->"
TABLE_END     = "<!-- AUDIT:END -->"
STATUS_ICON   = {"todo": "⬜ todo", "seed": "🌱 seed", "deep": "✅ deep"}


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


chapters      = load_json("data/chapters/en.json")
personalities = load_json("data/quran_personalities.json")
asma          = load_json("data/asma_ul_husna.json")


def describe_unknown(tag: str) -> str:
    if tag in qc.TAG_ALIASES:
        return f"'{tag}' is retired — use '{qc.TAG_ALIASES[tag]}'"
    return f"'{tag}' is not a theme in THEMES"


def check_tag_list(where: str, tags: list, errors: list) -> None:
    for tag in tags:
        if tag not in qc.THEMES:
            errors.append(f"{where}: {describe_unknown(tag)}")
    for tag, n in Counter(tags).items():
        if n > 1:
            errors.append(f"{where}: '{tag}' listed {n} times")


# ══════════════════════════════════════════════════════════════════════════════
#  CHECKS
# ══════════════════════════════════════════════════════════════════════════════

def audit_ayaat(errors: list, warnings: list) -> None:
    for ch in chapters:
        s, total = ch["id"], ch["total_verses"]
        status = qc.SURAH_STATUS[s]
        if status not in STATUS_ICON:
            errors.append(f"ayah_tags/s{s:03d}.py: unknown STATUS '{status}'")
        tagged = [a for (ss, a) in qc.AYAH_TAGS if ss == s]
        for a in tagged:
            if not 1 <= a <= total:
                errors.append(f"{s}:{a}: surah {s} has only {total} ayaat")
            tags = qc.AYAH_TAGS[(s, a)]
            if not tags:
                errors.append(f"{s}:{a}: empty tag list")
            check_tag_list(f"{s}:{a}", tags, errors)
        if status == "deep":
            missing = sorted(set(range(1, total + 1)) - set(tagged))
            if missing:
                errors.append(f"surah {s} is 'deep' but untagged ayaat remain: {missing[:10]}"
                              + (" …" if len(missing) > 10 else ""))
        if status == "todo" and tagged:
            warnings.append(f"surah {s} is 'todo' but has {len(tagged)} tagged ayaat")


def audit_personalities(errors: list) -> None:
    ids = {p["id"] for p in personalities}
    for p in personalities:
        where = f"personality '{p['id']}'"
        if not p.get("tags"):
            errors.append(f"{where}: no tags")
        check_tag_list(where, p.get("tags", []), errors)
        for cid in p.get("connections", []):
            if cid not in ids:
                errors.append(f"{where}: connection '{cid}' is not a personality id")


def audit_asma(errors: list) -> None:
    for name in asma:
        where = f"Asma #{name['number']} {name['transliteration']}"
        if not name.get("tags"):
            errors.append(f"{where}: no tags")
        check_tag_list(where, name.get("tags", []), errors)


def audit_themes(errors: list, warnings: list) -> None:
    for key, value in qc.THEMES.items():
        if len(value) != 4:
            errors.append(f"THEMES['{key}'] must be (category, title, urdu, description)")
    for field, label in ((1, "title"), (2, "urdu title")):
        seen = Counter(v[field] for v in qc.THEMES.values())
        for value, n in seen.items():
            if n > 1:
                keys = [k for k, v in qc.THEMES.items() if v[field] == value]
                warnings.append(f"THEMES share the {label} '{value}': {keys}")
    for old, new in qc.TAG_ALIASES.items():
        if old in qc.THEMES:
            errors.append(f"RETIRED_TAGS: '{old}' is retired but still a theme")
        if new not in qc.THEMES:
            errors.append(f"RETIRED_TAGS: replacement '{new}' is not a theme")
    for key, related in qc.RELATED_TOPICS.items():
        if key not in qc.THEMES:
            errors.append(f"RELATED_TOPICS: '{key}' is not a theme")
        for r in related:
            if r not in qc.THEMES:
                errors.append(f"RELATED_TOPICS['{key}']: {describe_unknown(r)}")
            if r == key:
                errors.append(f"RELATED_TOPICS['{key}'] lists itself")
    for key in qc.THEMES:
        if key not in qc.RELATED_TOPICS:
            warnings.append(f"RELATED_TOPICS has no entry for '{key}'")


# ══════════════════════════════════════════════════════════════════════════════
#  REPORTS
# ══════════════════════════════════════════════════════════════════════════════

def theme_usage() -> dict:
    """{theme: (ayaat, personalities, names)}"""
    ayah_count = Counter(t for tags in qc.AYAH_TAGS.values() for t in tags)
    pers_count = Counter(t for p in personalities for t in p.get("tags", []))
    asma_count = Counter(t for n in asma for t in n.get("tags", []))
    return {k: (ayah_count[k], pers_count[k], asma_count[k]) for k in qc.THEMES}


def summary_lines() -> list:
    total   = sum(ch["total_verses"] for ch in chapters)
    tagged  = len(qc.AYAH_TAGS)
    by_status = Counter(qc.SURAH_STATUS.values())
    deep_ayaat = sum(ch["total_verses"] for ch in chapters if qc.SURAH_STATUS[ch["id"]] == "deep")
    usage = theme_usage()
    unused = [k for k, (a, p, n) in usage.items() if a == 0]
    return [
        f"- **Ayaat tagged:** {tagged} / {total} ({tagged / total:.1%})",
        f"- **Surahs deep-tagged:** {by_status['deep']} / 114 "
        f"({deep_ayaat} ayaat, {deep_ayaat / total:.1%} of the Quran)",
        f"- **Surahs with seed tags only:** {by_status['seed']} · **untouched:** {by_status['todo']}",
        f"- **Themes:** {len(qc.THEMES)} · on ayaat: {len(qc.THEMES) - len(unused)} · "
        f"not yet on any ayah: {len(unused)}",
        f"- **Personalities tagged:** {sum(1 for p in personalities if p.get('tags'))} / {len(personalities)}"
        f" · **Names of Allah tagged:** {sum(1 for n in asma if n.get('tags'))} / {len(asma)}",
    ]


def status_table() -> str:
    lines = summary_lines() + [
        "",
        "| # | Surah | Ayaat | Tagged | Tags/ayah | Status |",
        "|---|-------|-------|--------|-----------|--------|",
    ]
    for ch in chapters:
        s = ch["id"]
        rows = [tags for (ss, _), tags in qc.AYAH_TAGS.items() if ss == s]
        density = f"{sum(map(len, rows)) / len(rows):.1f}" if rows else "—"
        lines.append(
            f"| {s} | {ch['transliteration']} | {ch['total_verses']} | {len(rows)} "
            f"| {density} | {STATUS_ICON.get(qc.SURAH_STATUS[s], qc.SURAH_STATUS[s])} |"
        )
    unused = [k for k, (a, _, _) in theme_usage().items() if a == 0]
    if unused:
        lines += ["", "**Themes not yet on any ayah:** " + ", ".join(f"`{k}`" for k in unused)]
    return "\n".join(lines)


def write_progress() -> None:
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        text = f.read()
    if TABLE_START not in text or TABLE_END not in text:
        sys.exit(f"{PROGRESS_FILE} is missing the {TABLE_START} / {TABLE_END} markers")
    block = f"{TABLE_START}\n{status_table()}\n{TABLE_END}"
    text = re.sub(re.escape(TABLE_START) + r".*?" + re.escape(TABLE_END),
                  lambda _: block, text, flags=re.DOTALL)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {PROGRESS_FILE}")


def print_surah(surah: int, start: int, end: int) -> None:
    ch = chapters[surah - 1]
    english = load_json("data/en.json")[str(surah)]
    print(f"# {surah} {ch['transliteration']} — {ch['translation']} "
          f"({ch['total_verses']} ayaat, {ch['type']}) · status: {qc.SURAH_STATUS[surah]}")
    for ayah in english:
        n = ayah["verse"]
        if start <= n <= end:
            tags = qc.AYAH_TAGS.get((surah, n))
            print(f"{n}| {ayah['text']}" + (f"  ⟨{', '.join(tags)}⟩" if tags else ""))


def print_themes() -> None:
    print(f"\n{'theme':<22}{'ayaat':>7}{'people':>8}{'names':>7}")
    for key, (a, p, n) in sorted(theme_usage().items(), key=lambda kv: -kv[1][0]):
        print(f"{key:<22}{a:>7}{p:>8}{n:>7}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="refresh the table in TAGGING_PROGRESS.md")
    parser.add_argument("--themes", action="store_true", help="print usage count per theme")
    parser.add_argument("--surah", type=int, help="print one surah with its current tags")
    parser.add_argument("--from", dest="start", type=int, default=1)
    parser.add_argument("--to", dest="end", type=int, default=10_000)
    args = parser.parse_args()

    if args.surah:
        print_surah(args.surah, args.start, args.end)
        return

    errors, warnings = [], []
    audit_themes(errors, warnings)
    audit_ayaat(errors, warnings)
    audit_personalities(errors)
    audit_asma(errors)

    print("\n".join(summary_lines()))
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  ERROR: {e}")
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")

    if args.themes:
        print_themes()
    if args.write:
        write_progress()
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
