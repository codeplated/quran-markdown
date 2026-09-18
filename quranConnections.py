"""
quranConnections.py
===================
The thematic knowledge graph for the Quran vault.

This file defines:
  1. THEMES          — the tag vocabulary. Every tag on an ayah, personality
                       or Name of Allah must be a key here.
  2. RETIRED_TAGS    — old / duplicate tag names and the theme that replaced them
  3. AYAH_TAGS       — (surah, ayah) → [theme keys], loaded from ayah_tags/sNNN.py
  4. RELATED_TOPICS  — cross-theme relationships
  5. get_ayah_themes(), build_index(), get_related_themes()

Tagging rules and progress: TAGGING_PROGRESS.md
Validate everything with:   python tag_audit.py
"""

from ayah_tags import load_all as _load_ayah_tags

# ══════════════════════════════════════════════════════════════════════════════
#  THEME TAXONOMY
#  key: (category, title, urdu_title, description)
#  Categories appear on the index page in the order they first occur here.
# ══════════════════════════════════════════════════════════════════════════════

THEMES = {
    # ── Belief (Aqeedah) ──────────────────────────────────────────────────────
    "tawheed":             ("Belief",     "Tawheed",                  "توحید",                  "Oneness of Allah — His lordship, sole right to worship & uniqueness"),
    "asma_ul_husna":       ("Belief",     "Asma ul Husna",            "اسماء الحسنیٰ",          "Names & attributes of Allah"),
    "rahmah":              ("Belief",     "Mercy & Forgiveness",      "رحمت و مغفرت",           "Allah's vast mercy, forgiveness & kindness to His servants"),
    "iman":                ("Belief",     "Iman",                     "ایمان",                  "Faith, its pillars & the qualities of true believers"),
    "shirk":               ("Belief",     "Shirk",                    "شرک",                    "Associating partners with Allah — idols, false gods & their refutation"),
    "kufr":                ("Belief",     "Kufr",                     "کفر",                    "Disbelief, denial of the truth & the attitudes of the disbelievers"),
    "nifaq":               ("Belief",     "Nifaq",                    "نفاق",                   "Hypocrisy — the hypocrites' traits, schemes & exposure"),
    "hidayah":             ("Belief",     "Guidance",                 "ہدایت و ضلالت",          "Guidance & misguidance — how and why hearts are guided or led astray"),
    "qadr":                ("Belief",     "Qadr",                     "تقدیر",                  "Divine decree, Allah's will & destiny"),
    "prophethood":         ("Belief",     "Prophethood",              "نبوت و رسالت",           "The messengers — their mission, humanity & belief in all of them"),
    "revelation":          ("Belief",     "Revelation",               "وحی و کتب",              "Wahy — the Quran's divine origin, earlier scriptures & the challenge to imitate it"),
    "angels":              ("Belief",     "Angels",                   "ملائکہ",                 "Angels — their nature, duties & the unseen world"),
    "jinn":                ("Belief",     "Jinn",                     "جنات",                   "The jinn — their creation, believers & disbelievers among them"),
    "shaytan":             ("Belief",     "Shaytan",                  "شیطان",                  "Iblis & the devils — enmity, whispers, deception & magic"),

    # ── Hereafter (Akhirah) ───────────────────────────────────────────────────
    "death_reminder":      ("Hereafter",  "Death & the Grave",        "موت و برزخ",             "Death, the barzakh & preparing to meet Allah"),
    "resurrection":        ("Hereafter",  "Resurrection",             "بعث بعد الموت",          "Life after death — its proofs & answers to those who deny it"),
    "akhirah":             ("Hereafter",  "Akhirah & Judgment Day",   "آخرت و یوم الحساب",      "The Hour, the Day of Judgment, reckoning, scales & intercession"),
    "jannah":              ("Hereafter",  "Jannah",                   "جنت",                    "Paradise — its gardens, delights & people"),
    "jahannam":            ("Hereafter",  "Jahannam",                 "جہنم",                   "Hell — its punishment & its people"),

    # ── Prophets (Anbiya) ─────────────────────────────────────────────────────
    "story_adam":          ("Prophets",   "Prophet Adam",             "آدم علیہ السلام",        "Creation of Adam, the angels' prostration, Iblis & repentance"),
    "story_idris":         ("Prophets",   "Prophet Idris",            "ادریس علیہ السلام",      "A truthful prophet raised to a high station"),
    "story_nuh":           ("Prophets",   "Prophet Nuh",              "نوح علیہ السلام",        "Centuries of da'wah, the ark & the flood"),
    "story_hud":           ("Prophets",   "Prophet Hud",              "ہود علیہ السلام",        "The people of 'Ad, their might & the destroying wind"),
    "story_salih":         ("Prophets",   "Prophet Salih",            "صالح علیہ السلام",       "Thamud, the she-camel & the mighty blast"),
    "story_ibrahim":       ("Prophets",   "Prophet Ibrahim",          "ابراہیم علیہ السلام",    "Khalilullah — breaking the idols, the fire, the sacrifice & the Kaaba"),
    "story_lut":           ("Prophets",   "Prophet Lut",              "لوط علیہ السلام",        "The people of Lut, their indecency & the overturned cities"),
    "story_ismail":        ("Prophets",   "Prophet Ismail",           "اسماعیل علیہ السلام",    "The sacrifice, raising the Kaaba & true to his promise"),
    "story_ishaq":         ("Prophets",   "Prophet Ishaq",            "اسحاق علیہ السلام",      "Glad tidings of a son to Ibrahim & Sarah in old age"),
    "story_yaqub":         ("Prophets",   "Prophet Yaqub",            "یعقوب علیہ السلام",      "Beautiful patience in grief & his final counsel to his sons"),
    "story_yusuf":         ("Prophets",   "Prophet Yusuf",            "یوسف علیہ السلام",       "The dream, the well, the prison, the palace & forgiveness"),
    "story_ayyub":         ("Prophets",   "Prophet Ayyub",            "ایوب علیہ السلام",       "Illness, loss & patience rewarded"),
    "story_shuayb":        ("Prophets",   "Prophet Shuayb",           "شعیب علیہ السلام",       "Madyan & Aykah — full measure & honest trade"),
    "story_musa":          ("Prophets",   "Prophet Musa",             "موسیٰ علیہ السلام",      "Pharaoh, the exodus, the Torah & the journey with Khidr"),
    "story_harun":         ("Prophets",   "Prophet Harun",            "ہارون علیہ السلام",      "Musa's brother, minister & fellow messenger"),
    "story_dhulkifl":      ("Prophets",   "Prophet Dhul-Kifl",        "ذوالکفل علیہ السلام",    "Among the patient & the best"),
    "story_dawud":         ("Prophets",   "Prophet Dawud",            "داؤد علیہ السلام",       "Victory over Jalut, kingship, the Zabur & repentance"),
    "story_sulayman":      ("Prophets",   "Prophet Sulayman",         "سلیمان علیہ السلام",     "A kingdom over jinn & wind, the ant, the hoopoe & the Queen of Saba"),
    "story_ilyas":         ("Prophets",   "Prophet Ilyas",            "الیاس علیہ السلام",      "Calling his people away from the idol Ba'l"),
    "story_alyasa":        ("Prophets",   "Prophet Al-Yasa",          "الیسع علیہ السلام",      "Among the chosen & the best"),
    "story_yunus":         ("Prophets",   "Prophet Yunus",            "یونس علیہ السلام",       "Leaving his people, the whale, the dua in the darkness & mercy"),
    "story_zakariya":      ("Prophets",   "Prophet Zakariya",         "زکریا علیہ السلام",      "Guardian of Maryam — a quiet dua answered with Yahya"),
    "story_yahya":         ("Prophets",   "Prophet Yahya",            "یحییٰ علیہ السلام",      "Given wisdom as a child — chaste, dutiful & at peace"),
    "story_isa":           ("Prophets",   "Prophet Isa",              "عیسیٰ علیہ السلام",      "Miraculous birth, miracles, the disciples & being raised"),
    "story_muhammad":      ("Prophets",   "Prophet Muhammad ﷺ",       "محمد ﷺ",                 "His life, mission, character & rights over the believers"),

    # ── Narratives (Qasas) ────────────────────────────────────────────────────
    "story_maryam":        ("Narratives", "Maryam",                   "مریم علیہا السلام",      "Her birth, devotion & the miraculous birth of Isa"),
    "story_luqman":        ("Narratives", "Luqman",                   "لقمان",                  "Luqman's wise counsel to his son"),
    "story_dhulqarnayn":   ("Narratives", "Dhul-Qarnayn",             "ذوالقرنین",              "A just ruler's journeys, the barrier & Ya'juj and Ma'juj"),
    "story_ashab_al_kahf": ("Narratives", "People of the Cave",       "اصحاب کہف",              "Youths who fled with their faith & slept for centuries"),
    "story_bani_israil":   ("Narratives", "Bani Israil",              "بنی اسرائیل",            "Children of Israel — favours, covenants, the calf, the cow & the Sabbath"),

    # ── Seerah ────────────────────────────────────────────────────────────────
    "sahabah":             ("Seerah",     "Sahabah",                  "صحابہ کرام",             "The Companions — Muhajirun, Ansar & their virtues"),
    "prophets_household":  ("Seerah",     "Prophet's Household",      "اہل بیت و ازواج مطہرات", "The Prophet's ﷺ wives & family — the Mothers of the Believers"),
    "hijrah":              ("Seerah",     "Hijrah",                   "ہجرت",                   "Migrating for Allah's sake — Makkah to Madinah & its reward"),
    "isra_miraj":          ("Seerah",     "Isra & Mi'raj",            "اسراء و معراج",          "The Night Journey & the Ascension"),
    "battle_badr":         ("Seerah",     "Battle of Badr",           "غزوۂ بدر",               "The Day of Criterion — 2 AH"),
    "battle_uhud":         ("Seerah",     "Battle of Uhud",           "غزوۂ احد",               "Victory, disobedience & lessons in setback — 3 AH"),
    "battle_ahzab":        ("Seerah",     "Battle of the Trench",     "غزوۂ احزاب",             "The Confederates' siege of Madinah — 5 AH"),
    "treaty_hudaybiyah":   ("Seerah",     "Treaty of Hudaybiyah",     "صلح حدیبیہ",             "The pledge under the tree & the clear victory — 6 AH"),
    "battle_hunayn":       ("Seerah",     "Battle of Hunayn",         "غزوۂ حنین",              "When great numbers impressed them — 8 AH"),
    "expedition_tabuk":    ("Seerah",     "Expedition of Tabuk",      "غزوۂ تبوک",              "Hardship, excuses & the three who stayed behind — 9 AH"),
    "incident_ifk":        ("Seerah",     "The Slander (Ifk)",        "واقعۂ افک",              "The slander against Aisha & its lessons"),

    # ── Worship (Ibadah) ──────────────────────────────────────────────────────
    "salah":               ("Worship",    "Salah",                    "نماز",                   "Prayer — its importance, times & manner"),
    "taharah":             ("Worship",    "Taharah",                  "طہارت",                  "Purification — wudu, ghusl & tayammum"),
    "zakat":               ("Worship",    "Zakat & Sadaqah",          "زکوٰۃ و صدقہ",           "Obligatory charity, voluntary giving & spending in Allah's way"),
    "sawm":                ("Worship",    "Sawm",                     "روزہ",                   "Fasting & Ramadan"),
    "hajj":                ("Worship",    "Hajj & Umrah",             "حج و عمرہ",              "Pilgrimage, its rites & sacrifice"),
    "kaaba":               ("Worship",    "Kaaba & Qiblah",           "کعبہ و قبلہ",            "The Kaaba, the qiblah & the sacred mosques"),
    "dhikr":               ("Worship",    "Dhikr & Tasbih",           "ذکر و تسبیح",            "Remembrance & glorification of Allah"),
    "dua":                 ("Worship",    "Dua",                      "دعا",                    "Supplications of the prophets & the believers"),
    "tawbah":              ("Worship",    "Tawbah",                   "توبہ و استغفار",         "Repentance, seeking forgiveness & returning to Allah"),
    "quran_recitation":    ("Worship",    "Tilawah & Tadabbur",       "تلاوت و تدبر",           "Reciting, reflecting on & living by the Quran"),

    # ── Character (Akhlaq) ────────────────────────────────────────────────────
    "sabr":                ("Character",  "Sabr",                     "صبر",                    "Patience & steadfastness — in hardship, in obedience & against sin"),
    "shukr":               ("Character",  "Shukr",                    "شکر",                    "Gratitude for Allah's blessings — and the ingratitude of man"),
    "tawakkul":            ("Character",  "Tawakkul",                 "توکل",                   "Reliance & trust in Allah"),
    "ikhlas":              ("Character",  "Ikhlas",                   "اخلاص",                  "Sincerity of intention & avoiding showing off"),
    "taqwa":               ("Character",  "Taqwa",                    "تقویٰ",                  "God-consciousness, piety & awe of Allah"),
    "ihsan":               ("Character",  "Ihsan",                    "احسان",                  "Excellence, goodness & kindness in action"),
    "sidq":                ("Character",  "Sidq",                     "صدق",                    "Truthfulness in word & deed — and the evil of lying"),
    "amanah":              ("Character",  "Amanah & Promises",        "امانت و عہد",            "Trusts, promises, oaths & covenants"),
    "adl":                 ("Character",  "Adl",                      "عدل",                    "Justice & fairness — in judgment, testimony & dealings"),
    "hilm":                ("Character",  "Hilm & Afw",               "حلم و عفو",              "Forbearance, restraining anger & forgiving others"),
    "kibr":                ("Character",  "Arrogance & Humility",     "تکبر و عاجزی",           "Pride as a disease of the heart & the humility Allah loves"),
    "hasad":               ("Character",  "Hasad",                    "حسد",                    "Envy & jealousy"),
    "haya":                ("Character",  "Haya",                     "حیا و عفت",              "Modesty, chastity & hijab"),
    "speech_ethics":       ("Character",  "Ethics of Speech",         "زبان کے آداب",           "Good words — and backbiting, mockery, slander & idle talk"),
    "adab":                ("Character",  "Adab",                     "آداب",                   "Manners — greetings, seeking permission, gatherings & conduct"),

    # ── Heart & Spirit ────────────────────────────────────────────────────────
    "tazkiyah":            ("Spirit",     "Tazkiyah",                 "تزکیۂ نفس",              "Purifying the soul — the nafs, desires & hearts sealed or softened"),
    "dunya":               ("Spirit",     "Dunya",                    "دنیا",                   "The worldly life — its reality, allure & heedlessness"),
    "purpose_of_life":     ("Spirit",     "Purpose of Life",          "مقصدِ حیات",             "Why we exist — worship, vicegerency & the test"),
    "love_of_allah":       ("Spirit",     "Love of Allah",            "محبتِ الٰہی",            "Whom Allah loves, whom He does not & loving Him"),
    "hope_raja":           ("Spirit",     "Hope & Raja",              "امید",                   "Hope in Allah & never despairing of His mercy"),
    "anxiety_fear":        ("Spirit",     "Anxiety, Fear & Sakinah",  "خوف و سکینت",            "Worry, fear & finding tranquility of heart"),
    "grief_loss":          ("Spirit",     "Grief & Loss",             "غم",                     "Sorrow, loss & consolation"),
    "trial_test":          ("Spirit",     "Trials & Tests",           "آزمائش",                 "Why hardship & ease come — the tests of this life"),

    # ── Daily Life ────────────────────────────────────────────────────────────
    "rizq":                ("Life",       "Rizq",                     "رزق",                    "Sustenance & provision — Allah as the Provider"),
    "wealth":              ("Life",       "Wealth & Spending",        "مال و خرچ",              "Earning & spending — hoarding, stinginess & extravagance"),
    "trade":               ("Life",       "Trade & Business",         "تجارت",                  "Business ethics, contracts & fair measure"),
    "debt":                ("Life",       "Debt & Loans",             "قرض",                    "Lending, recording debts & easing the debtor"),
    "riba":                ("Life",       "Riba",                     "سود",                    "Usury & interest — its prohibition & consequences"),
    "time":                ("Life",       "Time",                     "وقت",                    "Time, its value & the shortness of life"),
    "knowledge":           ("Life",       "Knowledge & Wisdom",       "علم و حکمت",             "Seeking knowledge, wisdom, scholars & using reason"),
    "health":              ("Life",       "Health & Healing",         "صحت و شفا",              "The body, illness & healing"),
    "food_halal":          ("Life",       "Halal & Haram Food",       "حلال و حرام",            "Permissible & forbidden food, drink & intoxicants"),
    "work_ethics":         ("Life",       "Work & Effort",            "محنت",                   "Effort, striving & earning a living"),

    # ── Family & Relationships ────────────────────────────────────────────────
    "marriage":            ("Relations",  "Marriage & Nikah",         "نکاح",                   "Marriage, its rights & purposes"),
    "family":              ("Relations",  "Family & Kinship",         "خاندان",                 "Family bonds, kinship duties & rights"),
    "parents":             ("Relations",  "Parents & Elders",         "والدین",                 "Honouring parents & the elderly"),
    "parenting":           ("Relations",  "Parenting & Children",     "اولاد",                  "Children, their rights & raising them"),
    "women":               ("Relations",  "Women",                    "خواتین",                 "The dignity & rights of women; exemplary women of the Quran"),
    "divorce":             ("Relations",  "Divorce & Iddah",          "طلاق و عدت",             "Divorce, waiting periods & parting with kindness"),
    "inheritance":         ("Relations",  "Inheritance & Wills",      "وراثت و وصیت",           "Shares of inheritance & bequests"),
    "orphans":             ("Relations",  "Orphans & the Vulnerable", "یتیم",                   "Care for orphans & protecting their wealth"),

    # ── Society & Law ─────────────────────────────────────────────────────────
    "community":           ("Society",    "Ummah & Brotherhood",      "امت و اخوت",             "Unity, brotherhood & avoiding division"),
    "wala_bara":           ("Society",    "Alliances & Loyalty",      "ولاء و براء",            "Whom believers take as allies & protectors"),
    "ahl_al_kitab":        ("Society",    "People of the Book",       "اہلِ کتاب",              "Jews & Christians — dialogue, their claims & critique"),
    "dawah":               ("Society",    "Da'wah",                   "دعوت و تبلیغ",           "Calling to Allah — enjoining good & forbidding evil"),
    "leadership":          ("Society",    "Leadership & Authority",   "قیادت",                  "Rulers, authority, obedience & responsibility"),
    "shura":               ("Society",    "Shura",                    "شوریٰ",                  "Consultation & collective decision-making"),
    "criminal_law":        ("Society",    "Crime & Punishment",       "حدود و قصاص",            "Qisas, hudud & blood money"),
    "oppression":          ("Society",    "Oppression",               "ظلم",                    "Dhulm — oppressors, the oppressed & standing against injustice"),
    "conflict":            ("Society",    "Jihad, War & Peace",       "جہاد، جنگ و صلح",        "Fighting in Allah's way, its ethics, treaties & peacemaking"),
    "social_justice":      ("Society",    "Social Justice",           "سماجی انصاف",            "Rights of the poor & needy, fair distribution & freeing slaves"),
    "environment":         ("Society",    "Earth & Corruption",       "زمین و فساد",            "Stewardship of the earth & spreading corruption (fasad) in it"),

    # ── Signs of Allah ────────────────────────────────────────────────────────
    "nature_signs":        ("Signs",      "Signs in Creation",        "قدرت کی نشانیاں",        "The heavens & earth, rain, plants, seas, night & day as signs of Allah"),
    "human_creation":      ("Signs",      "Creation of Mankind",      "تخلیقِ انسان",           "From clay & a drop — stages of creation & human nature"),
    "animals":             ("Signs",      "Animals",                  "جانور",                  "Cattle, bees, birds & other creatures & their lessons"),
    "miracles":            ("Signs",      "Miracles",                 "معجزات",                 "Signs & miracles granted to the prophets"),
    "history_lessons":     ("Signs",      "Lessons from History",     "تاریخ کے سبق",           "Past nations — their rise, destruction & what to learn"),

    # ── Quran Meta ────────────────────────────────────────────────────────────
    "muqattaat":           ("Meta",       "Muqatta'at",               "حروفِ مقطعات",           "The disjointed letters that open 29 surahs"),
    "sajdah_tilawah":      ("Meta",       "Sajdah Ayaat",             "آیاتِ سجدہ",             "Ayaat of prostration during recitation"),
    "o_believers":         ("Meta",       "O You Who Believe",        "یا ایہا الذین آمنوا",    "Direct addresses to the believers"),
    "o_mankind":           ("Meta",       "O Mankind",                "یا ایہا الناس",          "Addresses to all of humanity"),
    "they_ask_you":        ("Meta",       "They Ask You",             "یسئلونک",                "Questions put to the Prophet ﷺ & their answers"),
    "commands":            ("Meta",       "Direct Commands",          "اوامر",                  "Explicit commands from Allah"),
    "prohibitions":        ("Meta",       "Prohibitions",             "نواہی",                  "What Allah has forbidden"),
    "glad_tidings":        ("Meta",       "Glad Tidings",             "بشارت",                  "Promises of reward & mercy"),
    "warnings":            ("Meta",       "Warnings",                 "تنبیہ",                  "Divine warnings & admonitions"),
    "parables":            ("Meta",       "Parables & Amthal",        "امثال",                  "Quranic parables, similitudes & examples"),
    "oaths":               ("Meta",       "Divine Oaths",             "قسمیں",                  "Allah's oaths & what they emphasize"),
}

# ══════════════════════════════════════════════════════════════════════════════
#  RETIRED TAGS
#  replacement theme: [old names that meant the same thing]
#  Kept as a record of every merge, and so tag_audit.py can point stray old
#  names at their replacement. Old names must never be used as tags again.
# ══════════════════════════════════════════════════════════════════════════════

RETIRED_TAGS = {
    # ── duplicate ayah themes ─────────────────────────────────────────────────
    "tawbah":            ["tawbah_return", "repentance"],   # "Return to Allah" = Tawbah
    "purpose_of_life":   ["gratitude_life", "khalifah"],    # key said gratitude; theme was Purpose of Life

    # ── free-form personality tags, now on the shared vocabulary ─────────────
    "sabr":              ["patience"],
    "kibr":              ["arrogance", "humility"],
    "hasad":             ["envy", "jealousy"],
    "iman":              ["faith", "islam", "mass-faith"],
    "kufr":              ["disbelief"],
    "nifaq":             ["hypocrisy", "deceit"],
    "shirk":             ["idol-worship"],
    "shaytan":           ["iblis", "magic"],
    "prophethood":       ["prophet", "prophets"],
    "angels":            ["angel"],
    "sahabah":           ["companion"],
    "miracles":          ["miracle"],
    "trial_test":        ["test", "trial", "fitna"],
    "grief_loss":        ["grief"],
    "hope_raja":         ["hope"],
    "haya":              ["chastity"],
    "sidq":              ["truth", "truthfulness", "siddiq", "siddiqah", "confession"],
    "amanah":            ["trustworthy", "covenant", "betrayal"],
    "adl":               ["justice"],
    "oppression":        ["tyrant", "oppressor", "persecution", "persecutor", "persecutors",
                          "enabler", "liberation", "coercion"],
    "knowledge":         ["wisdom", "scholar", "divine-knowledge", "advice"],
    "shukr":             ["gratitude", "ingratitude", "blessings"],
    "rahmah":            ["mercy", "restoration"],
    "leadership":        ["king", "queen"],
    "health":            ["illness"],
    "rizq":              ["provision"],
    "nature_signs":      ["rain"],
    "human_creation":    ["creation"],
    "qadr":              ["free-will", "apparent-vs-real"],
    "resurrection":      ["trumpet", "resurrection-proof"],
    "akhirah":           ["judgment-day", "hereafter"],
    "death_reminder":    ["death", "soul", "appointed-time", "grave", "barzakh", "questioning"],
    "jahannam":          ["hell", "lowest-hell", "condemned"],
    "jannah":            ["paradise", "welcome"],
    "revelation":        ["wahi", "quran", "law", "psalms"],
    "women":             ["woman", "greatest-women", "mother"],
    "family":            ["brotherhood", "adoption", "heir"],
    "marriage":          ["partnership"],
    "trade":             ["business-ethics"],
    "criminal_law":      ["murder", "first-murder"],
    "history_lessons":   ["destroyed", "destruction", "earthquake", "collective-responsibility",
                          "normalization"],
    "warnings":          ["warning"],
    "ihsan":             ["ithar", "character"],
    "hilm":              ["non-retaliation"],
    "tazkiyah":          ["temptation", "love"],
    "conflict":          ["warrior", "defeated", "faith-vs-power"],
    "hajj":              ["zamzam", "safa-marwa"],
    "hijrah":            ["hijra"],
    "battle_badr":       ["badr"],
    "incident_ifk":      ["slander", "vindication"],
    "prophets_household":["mother-of-believers"],
    "story_nuh":         ["flood"],
    "story_hud":         ["aad"],
    "story_salih":       ["thamud", "she-camel"],
    "story_ibrahim":     ["khalilullah"],
    "story_shuayb":      ["midian"],
    "story_yusuf":       ["dream"],
    "story_yunus":       ["whale", "nineveh"],
    "story_isa":         ["messiah", "born-without-father", "disciples", "table"],
    "story_muhammad":    ["seal-of-prophets", "final"],
    "story_dhulqarnayn": ["yajuj-majuj", "barrier"],
    "story_bani_israil": ["bani-israel", "sabbath", "golden-calf", "transformed"],
}

TAG_ALIASES = {old: new for new, olds in RETIRED_TAGS.items() for old in olds}

# ══════════════════════════════════════════════════════════════════════════════
#  AYAH → THEMES MAP
#  Lives in ayah_tags/s001.py … s114.py — one file per surah.
# ══════════════════════════════════════════════════════════════════════════════

AYAH_TAGS, SURAH_STATUS = _load_ayah_tags()

# ══════════════════════════════════════════════════════════════════════════════
#  RELATED TOPICS MAP
#  Conceptual bridges between themes for cross-navigation.
#  "If you are reading about X, also see Y."
# ══════════════════════════════════════════════════════════════════════════════

RELATED_TOPICS = {
    # Belief
    "tawheed":            ["asma_ul_husna", "shirk", "ikhlas", "purpose_of_life"],
    "asma_ul_husna":      ["tawheed", "rahmah", "dhikr", "dua"],
    "rahmah":             ["tawbah", "hope_raja", "asma_ul_husna", "love_of_allah"],
    "iman":               ["taqwa", "hidayah", "kufr", "trial_test"],
    "shirk":              ["tawheed", "kufr", "story_ibrahim", "history_lessons"],
    "kufr":               ["iman", "shirk", "nifaq", "jahannam"],
    "nifaq":              ["kufr", "ikhlas", "wala_bara", "battle_uhud"],
    "hidayah":            ["iman", "qadr", "revelation", "dua"],
    "qadr":               ["tawakkul", "trial_test", "hidayah", "sabr"],
    "prophethood":        ["revelation", "story_muhammad", "dawah", "miracles"],
    "revelation":         ["quran_recitation", "prophethood", "angels", "knowledge"],
    "angels":             ["revelation", "jinn", "akhirah", "shaytan"],
    "jinn":               ["shaytan", "angels", "story_sulayman", "purpose_of_life"],
    "shaytan":            ["story_adam", "jinn", "tazkiyah", "kibr"],
    # Hereafter
    "death_reminder":     ["akhirah", "time", "dunya", "taqwa"],
    "resurrection":       ["akhirah", "human_creation", "nature_signs", "kufr"],
    "akhirah":            ["resurrection", "jannah", "jahannam", "adl"],
    "jannah":             ["glad_tidings", "iman", "sabr", "akhirah"],
    "jahannam":           ["warnings", "kufr", "akhirah", "taqwa"],
    # Prophets
    "story_adam":         ["shaytan", "human_creation", "tawbah", "angels"],
    "story_idris":        ["prophethood", "sidq", "sabr"],
    "story_nuh":          ["dawah", "sabr", "history_lessons", "story_hud"],
    "story_hud":          ["history_lessons", "kibr", "story_nuh", "story_salih"],
    "story_salih":        ["history_lessons", "miracles", "story_hud", "story_shuayb"],
    "story_ibrahim":      ["tawheed", "story_ismail", "kaaba", "trial_test"],
    "story_lut":          ["haya", "history_lessons", "story_ibrahim", "warnings"],
    "story_ismail":       ["story_ibrahim", "kaaba", "hajj", "amanah"],
    "story_ishaq":        ["story_ibrahim", "story_yaqub", "glad_tidings"],
    "story_yaqub":        ["story_yusuf", "sabr", "grief_loss", "family"],
    "story_yusuf":        ["sabr", "story_yaqub", "haya", "hilm"],
    "story_ayyub":        ["sabr", "health", "dua", "trial_test"],
    "story_shuayb":       ["trade", "history_lessons", "story_musa", "adl"],
    "story_musa":         ["story_harun", "story_bani_israil", "oppression", "miracles"],
    "story_harun":        ["story_musa", "story_bani_israil", "leadership", "family"],
    "story_dhulkifl":     ["sabr", "prophethood", "story_ayyub"],
    "story_dawud":        ["story_sulayman", "tawbah", "adl", "story_bani_israil"],
    "story_sulayman":     ["story_dawud", "shukr", "jinn", "leadership"],
    "story_ilyas":        ["shirk", "dawah", "prophethood"],
    "story_alyasa":       ["prophethood", "story_ilyas"],
    "story_yunus":        ["dua", "tawbah", "sabr", "anxiety_fear"],
    "story_zakariya":     ["dua", "story_yahya", "story_maryam", "hope_raja"],
    "story_yahya":        ["story_zakariya", "parents", "haya", "story_isa"],
    "story_isa":          ["story_maryam", "miracles", "ahl_al_kitab", "tawheed"],
    "story_muhammad":     ["prophethood", "sahabah", "prophets_household", "revelation"],
    # Narratives
    "story_maryam":       ["story_isa", "women", "story_zakariya", "haya"],
    "story_luqman":       ["parenting", "knowledge", "shirk", "adab"],
    "story_dhulqarnayn":  ["leadership", "adl", "akhirah", "story_ashab_al_kahf"],
    "story_ashab_al_kahf":["iman", "resurrection", "tawakkul", "story_dhulqarnayn"],
    "story_bani_israil":  ["story_musa", "ahl_al_kitab", "amanah", "shukr"],
    # Seerah
    "sahabah":            ["story_muhammad", "hijrah", "community", "battle_badr"],
    "prophets_household": ["story_muhammad", "marriage", "women", "incident_ifk"],
    "hijrah":             ["sahabah", "story_muhammad", "community", "tawakkul"],
    "isra_miraj":         ["story_muhammad", "kaaba", "miracles", "salah"],
    "battle_badr":        ["conflict", "tawakkul", "sahabah", "angels"],
    "battle_uhud":        ["conflict", "sabr", "nifaq", "battle_badr"],
    "battle_ahzab":       ["conflict", "nifaq", "trial_test", "battle_uhud"],
    "treaty_hudaybiyah":  ["conflict", "sahabah", "amanah", "kaaba"],
    "battle_hunayn":      ["conflict", "tawakkul", "kibr"],
    "expedition_tabuk":   ["conflict", "nifaq", "tawbah", "sabr"],
    "incident_ifk":       ["speech_ethics", "prophets_household", "haya", "sabr"],
    # Worship
    "salah":              ["taharah", "dhikr", "kaaba", "sajdah_tilawah"],
    "taharah":            ["salah", "haya", "health"],
    "zakat":              ["wealth", "social_justice", "ikhlas", "orphans"],
    "sawm":               ["taqwa", "revelation", "dua"],
    "hajj":               ["kaaba", "story_ibrahim", "taqwa", "dhikr"],
    "kaaba":              ["hajj", "story_ibrahim", "salah", "isra_miraj"],
    "dhikr":              ["dua", "salah", "anxiety_fear", "quran_recitation"],
    "dua":                ["dhikr", "hope_raja", "tawbah", "asma_ul_husna"],
    "tawbah":             ["rahmah", "hope_raja", "tazkiyah", "dua"],
    "quran_recitation":   ["revelation", "knowledge", "hidayah", "dhikr"],
    # Character
    "sabr":               ["trial_test", "tawakkul", "grief_loss", "jannah"],
    "shukr":              ["rizq", "sabr", "dunya", "trial_test"],
    "tawakkul":           ["qadr", "rizq", "sabr", "anxiety_fear"],
    "ikhlas":             ["tawheed", "taqwa", "nifaq", "zakat"],
    "taqwa":              ["iman", "akhirah", "tazkiyah", "ihsan"],
    "ihsan":              ["taqwa", "love_of_allah", "hilm", "zakat"],
    "sidq":               ["amanah", "speech_ethics", "iman", "nifaq"],
    "amanah":             ["sidq", "trade", "debt", "leadership"],
    "adl":                ["oppression", "criminal_law", "leadership", "social_justice"],
    "hilm":               ["ihsan", "speech_ethics", "community", "rahmah"],
    "kibr":               ["shaytan", "story_hud", "dunya", "adab"],
    "hasad":              ["story_yusuf", "story_adam", "tazkiyah", "community"],
    "haya":               ["marriage", "women", "adab", "tazkiyah"],
    "speech_ethics":      ["adab", "sidq", "incident_ifk", "community"],
    "adab":               ["speech_ethics", "haya", "family", "community"],
    # Spirit
    "tazkiyah":           ["taqwa", "shaytan", "dunya", "tawbah"],
    "dunya":              ["akhirah", "wealth", "trial_test", "death_reminder"],
    "purpose_of_life":    ["tawheed", "trial_test", "akhirah", "dunya"],
    "love_of_allah":      ["ihsan", "taqwa", "rahmah", "story_muhammad"],
    "hope_raja":          ["rahmah", "tawbah", "grief_loss", "anxiety_fear"],
    "anxiety_fear":       ["tawakkul", "dhikr", "hope_raja", "sabr"],
    "grief_loss":         ["sabr", "hope_raja", "death_reminder", "story_yaqub"],
    "trial_test":         ["sabr", "qadr", "dunya", "shukr"],
    # Life
    "rizq":               ["tawakkul", "shukr", "work_ethics", "wealth"],
    "wealth":             ["zakat", "dunya", "riba", "trade"],
    "trade":              ["amanah", "debt", "riba", "story_shuayb"],
    "debt":               ["trade", "riba", "amanah"],
    "riba":               ["trade", "debt", "wealth", "social_justice"],
    "time":               ["death_reminder", "dunya", "akhirah"],
    "knowledge":          ["revelation", "quran_recitation", "nature_signs", "story_luqman"],
    "health":             ["taharah", "food_halal", "story_ayyub"],
    "food_halal":         ["health", "commands", "prohibitions"],
    "work_ethics":        ["rizq", "trade", "time"],
    # Relations
    "marriage":           ["family", "divorce", "women", "haya"],
    "family":             ["parents", "parenting", "marriage", "inheritance"],
    "parents":            ["family", "parenting", "story_luqman", "ihsan"],
    "parenting":          ["parents", "family", "story_luqman", "orphans"],
    "women":              ["marriage", "story_maryam", "prophets_household", "haya"],
    "divorce":            ["marriage", "women", "family"],
    "inheritance":        ["family", "orphans", "adl"],
    "orphans":            ["social_justice", "zakat", "inheritance"],
    # Society
    "community":          ["sahabah", "wala_bara", "adl", "speech_ethics"],
    "wala_bara":          ["community", "nifaq", "ahl_al_kitab", "iman"],
    "ahl_al_kitab":       ["story_bani_israil", "story_isa", "revelation", "wala_bara"],
    "dawah":              ["prophethood", "knowledge", "hilm", "community"],
    "leadership":         ["shura", "adl", "amanah", "story_sulayman"],
    "shura":              ["leadership", "community"],
    "criminal_law":       ["adl", "commands", "prohibitions"],
    "oppression":         ["adl", "story_musa", "sabr", "history_lessons"],
    "conflict":           ["oppression", "battle_badr", "sabr", "hijrah"],
    "social_justice":     ["zakat", "orphans", "adl", "riba"],
    "environment":        ["nature_signs", "animals", "oppression"],
    # Signs
    "nature_signs":       ["tawheed", "knowledge", "shukr", "human_creation"],
    "human_creation":     ["nature_signs", "resurrection", "story_adam", "purpose_of_life"],
    "animals":            ["nature_signs", "food_halal", "story_sulayman"],
    "miracles":           ["prophethood", "story_musa", "story_isa", "nature_signs"],
    "history_lessons":    ["warnings", "story_nuh", "story_hud", "kibr"],
    # Meta
    "muqattaat":          ["revelation", "quran_recitation"],
    "sajdah_tilawah":     ["salah", "quran_recitation", "dhikr"],
    "o_believers":        ["commands", "iman", "prohibitions"],
    "o_mankind":          ["tawheed", "purpose_of_life", "dawah"],
    "they_ask_you":       ["story_muhammad", "knowledge", "commands"],
    "commands":           ["prohibitions", "o_believers", "taqwa"],
    "prohibitions":       ["commands", "food_halal", "criminal_law"],
    "glad_tidings":       ["jannah", "hope_raja", "iman"],
    "warnings":           ["jahannam", "history_lessons", "kufr"],
    "parables":           ["knowledge", "dunya", "nature_signs"],
    "oaths":              ["nature_signs", "akhirah", "time"],
}

# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

def get_ayah_themes(surah: int, ayah: int) -> list:
    """Return list of theme keys for a given ayah."""
    return AYAH_TAGS.get((surah, ayah), [])


def build_index() -> dict:
    """
    Returns { theme_key: [(surah, ayah), ...] } sorted by surah then ayah.
    """
    index = {k: [] for k in THEMES}
    for (s, a), tags in AYAH_TAGS.items():
        for tag in tags:
            if tag in index:
                index[tag].append((s, a))
    for key in index:
        index[key].sort()
    return index


def get_related_themes(theme_key: str) -> list:
    """Return list of related theme keys."""
    return RELATED_TOPICS.get(theme_key, [])
