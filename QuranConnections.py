"""
quran_connections.py
=====================
The thematic knowledge graph for the Quran vault.

This file defines:
  1. THEMES          — the full taxonomy of topics (deep, not shallow)
  2. AYAH_TAGS       — which ayaat belong to which themes (hand-curated seed set
                       covering ~400 of the most-studied ayaat; grows over time)
  3. RELATED_TOPICS  — explicit cross-theme relationships
  4. build_index()   — returns a dict: theme_key → list of (surah, ayah) tuples
  5. get_ayah_themes()— returns themes for a single ayah

This module is imported by quranImportScript.py and by generate_indexes.py.
"""

# ══════════════════════════════════════════════════════════════════════════════
#  THEME TAXONOMY
#  Each theme has:  key, emoji, title, urdu_title, description
# ══════════════════════════════════════════════════════════════════════════════

THEMES = {
    # ── Aqeedah (Belief) ──────────────────────────────────────────────────────
    "tawheed":         ("🕌", "Tawheed",              "توحید",         "Oneness of Allah"),
    "asma_ul_husna":   ("✨", "Asma ul Husna",         "اسماء الحسنی",  "Names & Attributes of Allah"),
    "akhirah":         ("⚖️", "Akhirah",               "آخرت",          "The Hereafter & Day of Judgment"),
    "jannah":          ("🌿", "Jannah",                "جنت",           "Paradise & its descriptions"),
    "jahannam":        ("🔥", "Jahannam",              "جہنم",          "Hell & divine warnings"),
    "qadr":            ("📜", "Qadr",                  "قدر",           "Divine Decree & Destiny"),
    "prophethood":     ("🌙", "Prophethood",           "نبوت",          "Prophethood & Messengership"),
    "revelation":      ("📖", "Revelation",            "وحی",           "The Quran & Divine Revelation"),
    "angels":          ("👼", "Angels & Unseen",       "ملائکہ",        "Angels, Jinn & the Unseen"),

    # ── Prophet Stories ───────────────────────────────────────────────────────
    "story_adam":      ("🌱", "Prophet Adam",          "آدم علیہ السلام","Creation, fall & repentance"),
    "story_ibrahim":   ("🔥", "Prophet Ibrahim",       "ابراہیم علیہ السلام","Father of monotheism"),
    "story_musa":      ("⚡", "Prophet Musa",          "موسیٰ علیہ السلام","Exodus, Pharaoh & the Law"),
    "story_isa":       ("🕊️", "Prophet Isa",           "عیسیٰ علیہ السلام","Birth, miracles & mission"),
    "story_yusuf":     ("⭐", "Prophet Yusuf",         "یوسف علیہ السلام","Patience, betrayal & triumph"),
    "story_nuh":       ("🚢", "Prophet Nuh",           "نوح علیہ السلام","Flood, patience & calling people"),
    "story_dawud":     ("🎵", "Prophet Dawud",         "داؤد علیہ السلام","Kingship, Psalms & repentance"),
    "story_sulayman":  ("👑", "Prophet Sulayman",      "سلیمان علیہ السلام","Kingdom, wisdom & gratitude"),
    "story_yunus":     ("🐋", "Prophet Yunus",         "یونس علیہ السلام","Despair, dua & mercy"),
    "story_ayyub":     ("💪", "Prophet Ayyub",         "ایوب علیہ السلام","Suffering, patience & healing"),
    "story_muhammad":  ("🌟", "Prophet Muhammad ﷺ",   "محمد ﷺ",        "Life, mission & character"),

    # ── Worship (Ibadah) ──────────────────────────────────────────────────────
    "salah":           ("🕌", "Salah",                 "نماز",          "Prayer — its importance & rules"),
    "zakat":           ("💰", "Zakat & Sadaqah",       "زکوٰۃ و صدقہ", "Charity, giving & purification of wealth"),
    "sawm":            ("🌙", "Sawm",                  "روزہ",          "Fasting & Ramadan"),
    "hajj":            ("🕋", "Hajj & Umrah",          "حج و عمرہ",     "Pilgrimage & its rituals"),
    "dhikr":           ("💭", "Dhikr & Dua",           "ذکر و دعا",     "Remembrance of Allah & supplication"),
    "tawbah":          ("🤲", "Tawbah",                "توبہ",          "Repentance & seeking forgiveness"),
    "quran_recitation":("📖", "Quran & Tilawah",       "تلاوت قرآن",   "Reciting, pondering & living by Quran"),

    # ── Character (Akhlaq) ────────────────────────────────────────────────────
    "sabr":            ("⏳", "Sabr",                  "صبر",           "Patience in hardship & trial"),
    "shukr":           ("🙏", "Shukr",                 "شکر",           "Gratitude to Allah"),
    "tawakkul":        ("🕊️", "Tawakkul",              "توکل",          "Reliance & trust in Allah"),
    "ikhlas":          ("💎", "Ikhlas",                "اخلاص",         "Sincerity of intention"),
    "taqwa":           ("🛡️", "Taqwa",                 "تقویٰ",         "God-consciousness & piety"),
    "ihsan":           ("✨", "Ihsan",                 "احسان",         "Excellence, goodness & beauty in action"),
    "sidq":            ("✅", "Sidq & Amanah",         "صدق و امانت",   "Truthfulness & trustworthiness"),
    "adl":             ("⚖️", "Adl",                   "عدل",           "Justice & fairness"),
    "hilm":            ("🌊", "Hilm & Afw",            "حلم و عفو",     "Forbearance, mercy & forgiveness"),
    "kibr":            ("⚠️", "Kibr & Pride",          "تکبر",          "Arrogance as a spiritual disease"),
    "hasad":           ("💔", "Hasad & Envy",          "حسد",           "Envy & spiritual poison"),

    # ── Daily Life ────────────────────────────────────────────────────────────
    "rizq":            ("🌾", "Rizq",                  "رزق",           "Sustenance, provision & livelihood"),
    "wealth":          ("💵", "Wealth & Spending",     "مال و خرچ",     "Earning, spending & wealth management"),
    "trade":           ("🤝", "Trade & Business",      "تجارت",         "Business ethics & commerce"),
    "debt":            ("📋", "Debt & Loans",          "قرض",           "Borrowing, lending & financial obligations"),
    "time":            ("⏰", "Time & Its Value",      "وقت",           "Time management & its importance"),
    "knowledge":       ("🔬", "Knowledge & Wisdom",   "علم و حکمت",    "Seeking knowledge & wisdom"),
    "health":          ("💚", "Health & Body",         "صحت",           "Body, food & physical wellbeing"),
    "food_halal":      ("🍽️", "Halal & Haram Food",   "حلال و حرام",   "Permissible and forbidden food"),
    "work_ethics":     ("🔨", "Work & Effort",         "محنت",          "Effort, striving & work ethics"),

    # ── Family & Relationships ────────────────────────────────────────────────
    "marriage":        ("💍", "Marriage & Nikah",      "نکاح",          "Marriage, its rights & purposes"),
    "family":          ("👨‍👩‍👧‍👦", "Family & Kinship",    "خاندان",        "Family bonds, duties & rights"),
    "parenting":       ("👶", "Parenting & Children",  "اولاد",         "Rights of children & parenting"),
    "parents":         ("❤️", "Parents & Elders",      "والدین",        "Honouring parents & the elderly"),
    "divorce":         ("📜", "Divorce & Separation",  "طلاق",          "Rules & ethics of divorce"),
    "inheritance":     ("🏠", "Inheritance",           "وراثت",         "Laws of inheritance"),
    "orphans":         ("🤲", "Orphans & Vulnerable",  "یتیم",          "Care for orphans & the vulnerable"),

    # ── Society & Governance ─────────────────────────────────────────────────
    "community":       ("🌍", "Ummah & Community",     "امت",           "Muslim community & brotherhood"),
    "leadership":      ("👑", "Leadership & Authority","قیادت",         "Leadership, authority & responsibility"),
    "shura":           ("🗣️", "Consultation & Shura",  "شوریٰ",         "Consultation & collective decision-making"),
    "oppression":      ("✊", "Oppression & Dhulm",    "ظلم",           "Standing against oppression"),
    "conflict":        ("🕊️", "Peace & Conflict",      "صلح و جنگ",     "War, peace & conflict resolution"),
    "social_justice":  ("⚖️", "Social Justice",        "سماجی انصاف",   "Economic & social justice"),
    "environment":     ("🌿", "Environment & Earth",   "زمین",          "Stewardship of the earth"),

    # ── Spiritual States & Struggles ─────────────────────────────────────────
    "anxiety_fear":    ("😟", "Anxiety & Fear",        "خوف و غم",      "Dealing with worry, grief & fear"),
    "hope_raja":       ("🌅", "Hope & Raja",           "امید",          "Hope in Allah's mercy"),
    "grief_loss":      ("🌧️", "Grief & Loss",          "غم",            "Coping with loss & hardship"),
    "trial_test":      ("🌊", "Trials & Tests",        "آزمائش",        "Purpose of tests & afflictions"),
    "gratitude_life":  ("☀️", "Purpose of Life",       "مقصدِ حیات",    "Why we exist & what we are here for"),
    "tawbah_return":   ("🔄", "Return to Allah",       "رجوع الی اللہ", "Coming back to Allah after sin"),
    "death_reminder":  ("🌑", "Death & Its Reminder",  "موت",           "Remembering death & preparing for it"),

    # ── Signs of Allah ────────────────────────────────────────────────────────
    "nature_signs":    ("🌌", "Signs in Nature",       "قدرت کی نشانیاں","Creation as evidence of Allah"),
    "history_lessons": ("🏛️", "Lessons from History",  "تاریخ کے سبق", "Nations destroyed & lessons to draw"),

    # ── Quran Meta ────────────────────────────────────────────────────────────
    "commands":        ("📌", "Direct Commands",       "اوامر",         "Explicit commands from Allah"),
    "prohibitions":    ("🚫", "Prohibitions",          "نواہی",         "What Allah has forbidden"),
    "glad_tidings":    ("🎉", "Glad Tidings",          "بشارت",         "Promises of reward & mercy"),
    "warnings":        ("⚠️",  "Warnings",             "تنبیہ",         "Divine warnings & admonitions"),
    "parables":        ("💡", "Parables & Amthal",     "امثال",         "Quranic parables & metaphors"),
    "oaths":           ("☀️", "Divine Oaths",          "قسمیں",         "Allah's oaths & what they emphasize"),
}

# ══════════════════════════════════════════════════════════════════════════════
#  AYAH → THEMES MAP
#  Format: (surah_int, ayah_int): ["theme_key", "theme_key", ...]
#
#  This is a curated seed covering ~450 key ayaat.
#  Add your own as you study — this grows with you.
# ══════════════════════════════════════════════════════════════════════════════

AYAH_TAGS = {
    # ── Al-Fatihah (1) ────────────────────────────────────────────────────────
    (1,1):  ["tawheed", "dhikr", "commands"],
    (1,2):  ["tawheed", "shukr", "asma_ul_husna"],
    (1,3):  ["asma_ul_husna", "hope_raja"],
    (1,4):  ["akhirah", "tawheed"],
    (1,5):  ["tawheed", "dhikr", "ikhlas"],
    (1,6):  ["dhikr", "commands", "knowledge"],
    (1,7):  ["history_lessons", "commands"],

    # ── Al-Baqarah (2) ────────────────────────────────────────────────────────
    (2,1):   ["revelation", "parables"],
    (2,2):   ["revelation", "taqwa", "quran_recitation"],
    (2,3):   ["salah", "zakat", "akhirah"],
    (2,21):  ["tawheed", "commands"],
    (2,22):  ["nature_signs", "tawheed"],
    (2,30):  ["story_adam", "leadership", "tawheed"],
    (2,31):  ["story_adam", "knowledge"],
    (2,36):  ["story_adam", "trial_test"],
    (2,37):  ["story_adam", "tawbah"],
    (2,38):  ["story_adam", "glad_tidings"],
    (2,45):  ["salah", "sabr", "commands"],
    (2,83):  ["parents", "family", "commands", "social_justice"],
    (2,110): ["salah", "zakat", "commands"],
    (2,143): ["community", "commands", "social_justice"],
    (2,152): ["dhikr", "shukr", "commands"],
    (2,153): ["sabr", "salah", "commands", "anxiety_fear"],
    (2,155): ["trial_test", "sabr"],
    (2,156): ["sabr", "akhirah", "tawakkul"],
    (2,157): ["sabr", "glad_tidings"],
    (2,163): ["tawheed", "asma_ul_husna"],
    (2,164): ["nature_signs", "tawheed"],
    (2,177): ["taqwa", "family", "zakat", "sabr", "sidq"],
    (2,183): ["sawm", "taqwa", "commands"],
    (2,185): ["sawm", "revelation", "commands"],
    (2,186): ["dhikr", "hope_raja", "tawbah"],
    (2,195): ["commands", "zakat", "prohibitions"],
    (2,197): ["hajj", "taqwa", "commands"],
    (2,216): ["trial_test", "tawakkul", "akhirah"],
    (2,219): ["wealth", "prohibitions", "zakat"],
    (2,222): ["tawbah", "commands"],
    (2,228): ["marriage", "commands"],
    (2,229): ["marriage", "divorce", "commands"],
    (2,233): ["parenting", "family", "commands"],
    (2,255): ["tawheed", "asma_ul_husna"],          # Ayat al-Kursi
    (2,256): ["tawheed", "commands"],               # La ikraha fid-deen
    (2,261): ["zakat", "parables", "glad_tidings"],
    (2,267): ["zakat", "commands", "work_ethics"],
    (2,268): ["anxiety_fear", "wealth", "hope_raja"],
    (2,269): ["knowledge", "asma_ul_husna"],
    (2,275): ["trade", "prohibitions", "debt"],
    (2,276): ["zakat", "wealth"],
    (2,277): ["salah", "zakat", "glad_tidings"],
    (2,282): ["debt", "trade", "commands", "sidq"],
    (2,286): ["tawakkul", "trial_test", "dhikr"],   # La yukallifullahu nafsan

    # ── Ali Imran (3) ─────────────────────────────────────────────────────────
    (3,7):   ["revelation", "knowledge", "taqwa"],
    (3,14):  ["wealth", "trial_test", "parables"],
    (3,17):  ["sabr", "sidq", "dhikr", "taqwa"],
    (3,26):  ["tawheed", "asma_ul_husna", "rizq"],
    (3,27):  ["tawheed", "rizq", "asma_ul_husna"],
    (3,31):  ["ikhlas", "tawbah", "commands"],
    (3,45):  ["story_isa", "revelation"],
    (3,92):  ["zakat", "taqwa", "commands"],
    (3,102): ["taqwa", "commands"],
    (3,103): ["community", "commands"],
    (3,110): ["community", "commands", "social_justice"],
    (3,130): ["trade", "prohibitions", "debt"],
    (3,133): ["taqwa", "tawbah", "commands"],
    (3,134): ["hilm", "zakat", "ihsan"],
    (3,135): ["tawbah", "taqwa", "glad_tidings"],
    (3,139): ["sabr", "tawakkul", "community"],
    (3,159): ["hilm", "shura", "tawakkul", "leadership"],
    (3,160): ["tawakkul", "tawheed"],
    (3,169): ["akhirah", "glad_tidings"],
    (3,173): ["tawakkul", "tawheed"],
    (3,185): ["akhirah", "death_reminder", "trial_test"],
    (3,190): ["nature_signs", "knowledge", "tawheed"],
    (3,191): ["dhikr", "nature_signs", "tawheed"],
    (3,200): ["sabr", "taqwa", "commands"],

    # ── An-Nisa (4) ───────────────────────────────────────────────────────────
    (4,1):   ["family", "tawheed", "commands"],
    (4,3):   ["marriage", "commands", "adl"],
    (4,11):  ["inheritance", "commands"],
    (4,19):  ["marriage", "commands", "adl"],
    (4,29):  ["trade", "prohibitions", "commands"],
    (4,36):  ["tawheed", "parents", "family", "commands"],
    (4,58):  ["leadership", "adl", "commands"],
    (4,59):  ["leadership", "commands", "shura"],
    (4,103): ["salah", "commands"],
    (4,135): ["adl", "sidq", "commands"],

    # ── Al-Maidah (5) ─────────────────────────────────────────────────────────
    (5,2):   ["commands", "community", "taqwa"],
    (5,3):   ["food_halal", "revelation", "tawheed"],
    (5,8):   ["adl", "commands", "taqwa"],
    (5,32):  ["social_justice", "commands", "adl"],
    (5,35):  ["taqwa", "commands"],
    (5,48):  ["revelation", "commands", "community"],
    (5,90):  ["prohibitions", "commands"],
    (5,120): ["tawheed", "asma_ul_husna"],

    # ── Al-Anam (6) ───────────────────────────────────────────────────────────
    (6,54):  ["tawbah", "hope_raja", "asma_ul_husna"],
    (6,59):  ["tawheed", "qadr", "asma_ul_husna"],
    (6,95):  ["nature_signs", "tawheed"],
    (6,103): ["tawheed", "asma_ul_husna"],
    (6,151): ["commands", "prohibitions", "parents"],
    (6,160): ["akhirah", "glad_tidings"],
    (6,162): ["ikhlas", "tawheed", "commands"],

    # ── Al-Araf (7) ───────────────────────────────────────────────────────────
    (7,19):  ["story_adam", "commands"],
    (7,23):  ["story_adam", "tawbah", "dhikr"],
    (7,31):  ["food_halal", "commands", "health"],
    (7,54):  ["tawheed", "nature_signs"],
    (7,96):  ["taqwa", "rizq", "glad_tidings"],
    (7,156): ["tawbah", "asma_ul_husna", "hope_raja"],
    (7,157): ["story_muhammad", "revelation"],
    (7,180): ["asma_ul_husna", "dhikr", "commands"],
    (7,204): ["quran_recitation", "commands"],

    # ── Al-Anfal (8) ──────────────────────────────────────────────────────────
    (8,2):   ["taqwa", "salah", "tawakkul"],
    (8,24):  ["commands", "tawakkul", "community"],
    (8,45):  ["sabr", "commands"],
    (8,46):  ["sabr", "community", "commands"],

    # ── At-Tawbah (9) ─────────────────────────────────────────────────────────
    (9,18):  ["salah", "zakat", "taqwa", "tawheed"],
    (9,51):  ["qadr", "tawakkul", "tawheed"],
    (9,71):  ["community", "salah", "zakat", "commands"],
    (9,103): ["zakat", "salah", "tawbah"],
    (9,119): ["taqwa", "sidq", "commands"],
    (9,128): ["story_muhammad", "asma_ul_husna"],

    # ── Yunus (10) ────────────────────────────────────────────────────────────
    (10,57): ["revelation", "quran_recitation", "health"],
    (10,62): ["taqwa", "glad_tidings", "tawakkul"],
    (10,107): ["tawakkul", "tawheed", "asma_ul_husna"],

    # ── Hud (11) ──────────────────────────────────────────────────────────────
    (11,6):  ["rizq", "tawheed", "tawakkul"],
    (11,88): ["tawakkul", "tawheed"],
    (11,114): ["salah", "commands", "tawbah"],
    (11,115): ["sabr", "commands"],

    # ── Yusuf (12) ────────────────────────────────────────────────────────────
    (12,4):  ["story_yusuf"],
    (12,18): ["story_yusuf", "sabr"],
    (12,20): ["story_yusuf", "wealth"],
    (12,64): ["story_yusuf", "tawakkul", "tawheed"],
    (12,86): ["story_yusuf", "sabr", "grief_loss"],
    (12,87): ["story_yusuf", "hope_raja", "tawakkul"],
    (12,101): ["story_yusuf", "dhikr", "tawbah"],

    # ── Ar-Rad (13) ───────────────────────────────────────────────────────────
    (13,11): ["qadr", "community", "tawakkul"],
    (13,28): ["dhikr", "anxiety_fear", "glad_tidings"],  # Ala bi dhikrillah
    (13,29): ["taqwa", "glad_tidings"],

    # ── Ibrahim (14) ──────────────────────────────────────────────────────────
    (14,7):  ["shukr", "glad_tidings"],                  # La in shakartum
    (14,24): ["parables", "tawheed", "knowledge"],
    (14,31): ["salah", "zakat", "commands"],
    (14,34): ["asma_ul_husna", "shukr", "nature_signs"],
    (14,40): ["salah", "dhikr", "family"],
    (14,41): ["dhikr", "family", "akhirah"],

    # ── Al-Hijr (15) ──────────────────────────────────────────────────────────
    (15,9):  ["revelation", "tawheed"],
    (15,98): ["salah", "commands", "dhikr"],

    # ── An-Nahl (16) ──────────────────────────────────────────────────────────
    (16,18): ["shukr", "asma_ul_husna", "nature_signs"],
    (16,53): ["shukr", "tawheed"],
    (16,78): ["knowledge", "shukr"],
    (16,90): ["adl", "ihsan", "commands", "prohibitions"],
    (16,97): ["work_ethics", "glad_tidings"],
    (16,114): ["food_halal", "shukr", "commands"],
    (16,125): ["knowledge", "commands"],

    # ── Al-Isra (17) ──────────────────────────────────────────────────────────
    (17,1):  ["story_muhammad", "tawheed"],
    (17,9):  ["revelation", "quran_recitation", "glad_tidings"],
    (17,23): ["parents", "commands"],                    # Qada rabbuka
    (17,24): ["parents", "dhikr"],
    (17,25): ["parents", "asma_ul_husna"],
    (17,26): ["family", "zakat", "prohibitions"],
    (17,27): ["prohibitions", "wealth"],
    (17,29): ["wealth", "commands"],
    (17,31): ["parenting", "rizq", "prohibitions"],
    (17,32): ["prohibitions"],
    (17,33): ["prohibitions", "adl"],
    (17,36): ["knowledge", "commands"],
    (17,37): ["kibr", "prohibitions"],
    (17,44): ["tawheed", "nature_signs"],
    (17,78): ["salah", "commands"],
    (17,80): ["dhikr", "commands"],
    (17,82): ["revelation", "health"],
    (17,110): ["asma_ul_husna", "dhikr"],

    # ── Al-Kahf (18) ──────────────────────────────────────────────────────────
    (18,10): ["tawbah", "tawakkul", "hope_raja"],
    (18,13): ["taqwa", "tawakkul"],
    (18,28): ["dhikr", "commands", "taqwa"],
    (18,29): ["tawheed", "commands"],
    (18,45): ["parables", "wealth", "akhirah"],
    (18,46): ["wealth", "akhirah", "parables"],
    (18,54): ["parables", "revelation"],
    (18,65): ["knowledge", "story_musa"],
    (18,66): ["knowledge", "story_musa"],
    (18,109): ["tawheed", "knowledge", "asma_ul_husna"],
    (18,110): ["ikhlas", "tawheed", "commands"],

    # ── Maryam (19) ───────────────────────────────────────────────────────────
    (19,2):  ["dhikr", "story_isa"],
    (19,30): ["story_isa", "revelation"],
    (19,36): ["story_isa", "tawheed"],
    (19,76): ["sabr", "glad_tidings"],
    (19,96): ["ikhlas", "glad_tidings"],

    # ── Ta-Ha (20) ────────────────────────────────────────────────────────────
    (20,14): ["salah", "dhikr", "tawheed", "commands"],
    (20,25): ["dhikr", "story_musa"],
    (20,114): ["knowledge", "dhikr"],
    (20,124): ["akhirah", "warnings", "dhikr"],
    (20,130): ["salah", "sabr", "commands"],
    (20,132): ["salah", "family", "commands"],

    # ── Al-Anbiya (21) ────────────────────────────────────────────────────────
    (21,35): ["trial_test", "akhirah"],
    (21,69): ["story_ibrahim"],
    (21,83): ["story_ayyub", "dhikr"],
    (21,84): ["story_ayyub", "glad_tidings"],
    (21,87): ["story_yunus", "dhikr", "tawbah"],        # Dua of Yunus
    (21,88): ["story_yunus", "glad_tidings", "tawbah"],
    (21,107): ["story_muhammad", "asma_ul_husna"],

    # ── Al-Hajj (22) ──────────────────────────────────────────────────────────
    (22,27): ["hajj", "commands"],
    (22,37): ["ikhlas", "taqwa", "commands"],
    (22,41): ["leadership", "salah", "zakat", "commands"],
    (22,46): ["knowledge", "akhirah"],
    (22,77): ["salah", "commands", "taqwa"],
    (22,78): ["tawakkul", "commands"],

    # ── Al-Muminun (23) ───────────────────────────────────────────────────────
    (23,1):  ["taqwa", "salah", "glad_tidings"],
    (23,2):  ["salah", "taqwa"],
    (23,3):  ["sidq", "taqwa"],
    (23,4):  ["zakat", "taqwa"],
    (23,8):  ["sidq", "amanah"],
    (23,9):  ["salah", "taqwa"],
    (23,10): ["glad_tidings", "akhirah"],

    # ── An-Nur (24) ───────────────────────────────────────────────────────────
    (24,2):  ["commands", "prohibitions"],
    (24,31): ["commands"],
    (24,35): ["tawheed", "asma_ul_husna", "parables"],  # Ayat an-Nur
    (24,56): ["salah", "zakat", "commands"],
    (24,58): ["family", "commands"],
    (24,61): ["family", "commands"],

    # ── Al-Furqan (25) ────────────────────────────────────────────────────────
    (25,63): ["taqwa", "hilm"],
    (25,64): ["salah", "dhikr"],
    (25,65): ["tawbah", "akhirah"],
    (25,67): ["wealth", "commands"],
    (25,68): ["prohibitions", "tawbah"],
    (25,70): ["tawbah", "glad_tidings"],
    (25,74): ["family", "dhikr"],

    # ── Luqman (31) ───────────────────────────────────────────────────────────
    (31,12): ["shukr", "knowledge"],
    (31,13): ["tawheed", "commands", "parents"],
    (31,14): ["parents", "shukr", "commands"],
    (31,15): ["parents", "commands"],
    (31,16): ["akhirah", "qadr"],
    (31,17): ["salah", "commands", "community"],
    (31,18): ["kibr", "prohibitions"],
    (31,19): ["commands"],

    # ── As-Sajdah (32) ────────────────────────────────────────────────────────
    (32,15): ["taqwa", "salah"],
    (32,16): ["salah", "dhikr"],
    (32,17): ["akhirah", "glad_tidings", "sabr"],

    # ── Al-Ahzab (33) ─────────────────────────────────────────────────────────
    (33,21): ["story_muhammad", "commands"],             # Uswatun hasana
    (33,35): ["taqwa", "commands", "salah"],
    (33,41): ["dhikr", "commands"],
    (33,56): ["story_muhammad", "salah"],
    (33,70): ["sidq", "taqwa", "commands"],

    # ── Ya-Sin (36) ───────────────────────────────────────────────────────────
    (36,12): ["akhirah", "qadr"],
    (36,82): ["tawheed", "asma_ul_husna"],

    # ── Az-Zumar (39) ─────────────────────────────────────────────────────────
    (39,9):  ["knowledge", "taqwa"],
    (39,10): ["sabr", "taqwa", "glad_tidings"],
    (39,22): ["taqwa", "glad_tidings"],
    (39,36): ["tawakkul", "tawheed"],
    (39,38): ["tawakkul", "tawheed"],
    (39,53): ["tawbah", "hope_raja", "asma_ul_husna"],   # La taqnatu
    (39,54): ["tawbah", "commands"],

    # ── Ghafir (40) ───────────────────────────────────────────────────────────
    (40,44): ["tawakkul", "tawheed"],
    (40,60): ["dhikr", "glad_tidings", "commands"],      # Uduni astajib lakum

    # ── Fussilat (41) ─────────────────────────────────────────────────────────
    (41,30): ["taqwa", "tawakkul", "glad_tidings"],
    (41,34): ["hilm", "commands"],
    (41,46): ["akhirah", "adl"],

    # ── Ash-Shura (42) ────────────────────────────────────────────────────────
    (42,10): ["tawheed", "akhirah"],
    (42,23): ["glad_tidings", "shukr"],
    (42,25): ["tawbah", "asma_ul_husna"],
    (42,27): ["rizq", "tawheed"],
    (42,38): ["salah", "shura", "zakat"],
    (42,43): ["sabr", "hilm"],

    # ── Al-Hujurat (49) ───────────────────────────────────────────────────────
    (49,6):  ["sidq", "knowledge", "commands"],
    (49,10): ["community", "commands"],
    (49,11): ["prohibitions", "community"],
    (49,12): ["hasad", "prohibitions"],
    (49,13): ["community", "taqwa", "adl"],

    # ── Adh-Dhariyat (51) ─────────────────────────────────────────────────────
    (51,19): ["zakat", "social_justice"],
    (51,56): ["tawheed", "gratitude_life"],

    # ── Al-Waqi'ah (56) ───────────────────────────────────────────────────────
    (56,10): ["akhirah", "glad_tidings"],
    (56,77): ["revelation", "quran_recitation"],
    (56,79): ["quran_recitation", "taqwa"],

    # ── Al-Hadid (57) ─────────────────────────────────────────────────────────
    (57,7):  ["zakat", "tawakkul", "commands"],
    (57,20): ["parables", "wealth", "akhirah"],
    (57,21): ["glad_tidings", "akhirah"],
    (57,22): ["qadr", "tawakkul"],
    (57,23): ["tawakkul", "shukr"],

    # ── Al-Hashr (59) ─────────────────────────────────────────────────────────
    (59,7):  ["social_justice", "zakat", "commands"],
    (59,9):  ["community", "social_justice", "ihsan"],
    (59,18): ["akhirah", "taqwa", "commands"],
    (59,19): ["taqwa", "warnings"],
    (59,22): ["tawheed", "asma_ul_husna"],
    (59,23): ["tawheed", "asma_ul_husna"],
    (59,24): ["tawheed", "asma_ul_husna"],

    # ── Al-Jumu'ah (62) ───────────────────────────────────────────────────────
    (62,9):  ["salah", "trade", "commands"],
    (62,10): ["work_ethics", "commands"],

    # ── At-Talaq (65) ─────────────────────────────────────────────────────────
    (65,2):  ["taqwa", "rizq", "glad_tidings"],
    (65,3):  ["tawakkul", "rizq", "tawheed"],

    # ── Al-Mulk (67) ──────────────────────────────────────────────────────────
    (67,2):  ["trial_test", "death_reminder", "akhirah"],
    (67,14): ["tawheed", "knowledge"],
    (67,15): ["rizq", "nature_signs", "tawakkul"],

    # ── Al-Qalam (68) ─────────────────────────────────────────────────────────
    (68,4):  ["story_muhammad", "ihsan"],

    # ── Al-Insan (76) ─────────────────────────────────────────────────────────
    (76,8):  ["social_justice", "ihsan", "orphans"],
    (76,9):  ["ikhlas", "social_justice"],

    # ── An-Naba (78) ──────────────────────────────────────────────────────────
    (78,8):  ["marriage", "nature_signs"],
    (78,40): ["akhirah", "death_reminder", "warnings"],

    # ── An-Nazi'at (79) ───────────────────────────────────────────────────────
    (79,40): ["taqwa", "akhirah"],
    (79,41): ["akhirah", "glad_tidings"],

    # ── 'Abasa (80) ───────────────────────────────────────────────────────────
    (80,1):  ["story_muhammad", "adl"],
    (80,24): ["shukr", "nature_signs"],

    # ── Al-A'la (87) ──────────────────────────────────────────────────────────
    (87,9):  ["quran_recitation", "commands"],
    (87,14): ["taqwa", "glad_tidings"],

    # ── Al-Ghashiyah (88) ────────────────────────────────────────────────────
    (88,17): ["nature_signs", "tawheed"],
    (88,21): ["commands", "revelation"],

    # ── Al-Fajr (89) ──────────────────────────────────────────────────────────
    (89,27): ["taqwa", "glad_tidings"],
    (89,28): ["glad_tidings", "akhirah"],

    # ── Ad-Duhaa (93) ─────────────────────────────────────────────────────────
    (93,3):  ["hope_raja", "tawheed"],
    (93,4):  ["glad_tidings", "akhirah"],
    (93,5):  ["hope_raja", "tawheed"],
    (93,9):  ["orphans", "commands"],
    (93,11): ["shukr", "commands"],

    # ── Ash-Sharh (94) ────────────────────────────────────────────────────────
    (94,1):  ["anxiety_fear", "hope_raja", "asma_ul_husna"],
    (94,5):  ["glad_tidings", "sabr", "hope_raja"],     # Fa inna ma al-usri yusra
    (94,6):  ["glad_tidings", "sabr"],
    (94,7):  ["work_ethics", "commands"],
    (94,8):  ["dhikr", "commands"],

    # ── At-Tin (95) ───────────────────────────────────────────────────────────
    (95,4):  ["nature_signs", "tawheed", "gratitude_life"],
    (95,5):  ["akhirah", "warnings"],
    (95,6):  ["taqwa", "glad_tidings"],

    # ── Al-'Alaq (96) ─────────────────────────────────────────────────────────
    (96,1):  ["knowledge", "commands", "revelation"],
    (96,2):  ["knowledge", "nature_signs"],
    (96,3):  ["knowledge", "commands"],
    (96,4):  ["knowledge", "commands"],
    (96,5):  ["knowledge"],

    # ── Al-Qadr (97) ──────────────────────────────────────────────────────────
    (97,1):  ["revelation", "time"],
    (97,3):  ["akhirah", "glad_tidings"],

    # ── Az-Zalzalah (99) ──────────────────────────────────────────────────────
    (99,7):  ["akhirah", "adl"],
    (99,8):  ["akhirah", "adl"],

    # ── Al-'Asr (103) ─────────────────────────────────────────────────────────
    (103,1): ["time", "oaths"],
    (103,2): ["akhirah", "warnings"],
    (103,3): ["taqwa", "sabr", "community"],

    # ── Al-Kawthar (108) ──────────────────────────────────────────────────────
    (108,1): ["story_muhammad", "glad_tidings", "shukr"],
    (108,2): ["salah", "commands"],

    # ── Al-Kafirun (109) ──────────────────────────────────────────────────────
    (109,1): ["tawheed", "ikhlas"],
    (109,6): ["tawheed", "ikhlas"],

    # ── An-Nasr (110) ─────────────────────────────────────────────────────────
    (110,1): ["story_muhammad", "tawheed"],
    (110,3): ["tawbah", "commands"],

    # ── Al-Ikhlas (112) ───────────────────────────────────────────────────────
    (112,1): ["tawheed", "ikhlas"],
    (112,2): ["tawheed", "asma_ul_husna"],
    (112,3): ["tawheed", "asma_ul_husna"],
    (112,4): ["tawheed", "asma_ul_husna"],

    # ── Al-Falaq (113) ────────────────────────────────────────────────────────
    (113,1): ["dhikr", "commands"],
    (113,2): ["dhikr", "tawheed"],

    # ── An-Nas (114) ──────────────────────────────────────────────────────────
    (114,1): ["dhikr", "commands"],
    (114,2): ["tawheed", "asma_ul_husna"],
    (114,3): ["tawheed", "asma_ul_husna"],
}

# ══════════════════════════════════════════════════════════════════════════════
#  RELATED TOPICS MAP
#  Defines conceptual bridges between themes for cross-navigation.
#  "If you are reading about X, also see Y because..."
# ══════════════════════════════════════════════════════════════════════════════

RELATED_TOPICS = {
    "tawheed":         ["asma_ul_husna", "ikhlas", "tawakkul", "revelation"],
    "asma_ul_husna":   ["tawheed", "dhikr", "hope_raja"],
    "akhirah":         ["death_reminder", "jannah", "jahannam", "trial_test", "akhirah"],
    "jannah":          ["taqwa", "sabr", "glad_tidings", "akhirah"],
    "jahannam":        ["taqwa", "warnings", "akhirah"],
    "qadr":            ["tawakkul", "sabr", "anxiety_fear"],
    "sabr":            ["tawakkul", "trial_test", "hope_raja", "grief_loss"],
    "shukr":           ["rizq", "taqwa", "asma_ul_husna"],
    "tawakkul":        ["rizq", "qadr", "tawheed", "sabr"],
    "ikhlas":          ["tawheed", "taqwa", "salah"],
    "taqwa":           ["akhirah", "salah", "commands"],
    "anxiety_fear":    ["sabr", "tawakkul", "dhikr", "hope_raja"],
    "grief_loss":      ["sabr", "tawbah", "hope_raja", "qadr"],
    "trial_test":      ["sabr", "tawakkul", "qadr", "shukr"],
    "rizq":            ["tawakkul", "zakat", "trade", "shukr"],
    "wealth":          ["zakat", "trade", "rizq", "prohibitions"],
    "trade":           ["debt", "adl", "commands"],
    "family":          ["parents", "marriage", "parenting", "orphans"],
    "marriage":        ["family", "parenting", "commands"],
    "parents":         ["family", "commands", "shukr"],
    "parenting":       ["family", "parents", "commands"],
    "knowledge":       ["revelation", "taqwa", "work_ethics"],
    "salah":           ["dhikr", "taqwa", "commands"],
    "zakat":           ["social_justice", "wealth", "commands"],
    "tawbah":          ["hope_raja", "ikhlas", "asma_ul_husna"],
    "community":       ["leadership", "shura", "social_justice"],
    "leadership":      ["adl", "shura", "community"],
    "social_justice":  ["adl", "zakat", "orphans", "oppression"],
    "death_reminder":  ["akhirah", "taqwa", "dhikr"],
    "nature_signs":    ["tawheed", "knowledge", "shukr"],
    "history_lessons": ["warnings", "taqwa", "prophethood"],
    "story_yusuf":     ["sabr", "tawakkul", "trial_test", "grief_loss"],
    "story_musa":      ["leadership", "trial_test", "history_lessons"],
    "story_ibrahim":   ["tawheed", "trial_test", "tawakkul"],
    "story_ayyub":     ["sabr", "grief_loss", "dhikr"],
    "story_yunus":     ["tawbah", "grief_loss", "hope_raja"],
    "story_muhammad":  ["prophethood", "community", "revelation"],
    "parables":        ["knowledge", "akhirah", "nature_signs"],
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
