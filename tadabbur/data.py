"""
Loads the source dataset once, at import time.

Everything downstream reads from here rather than opening files itself, so
there is a single place to look when you want to know what data exists.
"""

import json
from pathlib import Path

import config


def load_json(path: Path):
    """Reads a UTF-8 JSON file, with a message that names the file when it fails."""
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise FileNotFoundError(f"missing data file: {path}") from None
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error}") from None


quran = load_json(config.QURAN_JSON)
english = load_json(config.ENGLISH_JSON)
urdu = load_json(config.URDU_JSON)
chapters_en = load_json(config.CHAPTERS_EN_JSON)
chapters_ur = load_json(config.CHAPTERS_UR_JSON)
asma_ul_husna = load_json(config.ASMA_JSON)
personalities = load_json(config.PERSONALITIES_JSON)

SURAH_COUNT = len(chapters_en)


class Surah:
    """The names and metadata of one surah, gathered from both chapter files."""

    __slots__ = ("number", "english", "arabic", "urdu", "type", "total_ayaat")

    def __init__(self, number: int):
        index = number - 1
        self.number = number
        self.english = chapters_en[index]["translation"]
        self.arabic = chapters_ur[index]["name"]
        self.urdu = chapters_ur[index]["translation"]
        self.type = chapters_ur[index]["type"]
        self.total_ayaat = chapters_ur[index]["total_verses"]

    @property
    def folder_name(self) -> str:
        """Vault folder for this surah, e.g. '2 - The Cow البقرة'."""
        return f"{self.number} - {self.english} {self.arabic}"

    def note_name(self, ayah: int) -> str:
        """
        Note name for one ayah, e.g. '2_255: The Cow البقرة'.

        This doubles as the wikilink target, so the format is load-bearing:
        the published site's links break if it changes.
        """
        return f"{self.number}_{ayah}: {self.english} {self.arabic}"


# Built once so any module can turn a surah number into its names.
SURAHS = {number: Surah(number) for number in range(1, SURAH_COUNT + 1)}


def wikilink(surah: int, ayah: int) -> str:
    """An Obsidian link to an ayah note: [[2_255: The Cow البقرة]]."""
    if surah in SURAHS:
        return f"[[{SURAHS[surah].note_name(ayah)}]]"
    return f"[[{surah}_{ayah}]]"


def load_tafsir(surah: int, ayah: int) -> str:
    """
    Urdu tafsir for one ayah. Missing or unreadable files degrade to a notice
    rather than aborting a 6,236-note run partway through.
    """
    path = config.TAFSIR_DIR / str(surah) / f"{ayah}.json"
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle).get("text", "")
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return "_Tafsir not available for this ayah._"
