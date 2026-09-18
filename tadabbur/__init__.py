"""
Tadabbur generator internals.

Read `main.py` first — it is the whole pipeline in one screen. Each module
here owns one kind of note and can be read on its own:

    data.py          loads every source JSON exactly once
    audio.py         turns (surah, ayah) into a playable audio embed
    notes.py         writing notes and preserving hand-written sections
    ayah_notes.py    the 6,236 ayah notes
    asma_notes.py    the 99 Names of Allah
    personalities.py the 79 Quranic figures and their indexes
    explore.py       the thematic index and the Obsidian base view
    assets.py        thumbnails and hand-made vault files
"""
