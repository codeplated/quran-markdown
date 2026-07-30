"""
quran_personalities.py
======================
Every person, angel, jinn, and named group mentioned in the Quran.

Each entry contains:
  - id            : unique slug for wikilinks
  - name_arabic   : Arabic name as appears in Quran
  - name_english  : English name / transliteration
  - name_urdu     : Urdu name
  - also_known_as : other names / titles (e.g. Isa = Jesus = Messiah)
  - type          : "prophet" | "angel" | "jinn" | "companion" | "person" | "group"
  - path          : "straight" | "deviated" | "mixed" | "unknown"
  - path_reason   : one-line summary of why
  - era           : approximate period / context
  - mentioned_in  : list of [surah, ayah] for primary mentions
  - story_summary : English summary of their Quranic narrative
  - urdu_summary  : Urdu summary
  - lessons       : key lessons from their story
  - connections   : list of other personality ids they connect to
  - tags          : thematic tags
"""

PERSONALITIES = [

    # ══════════════════════════════════════════════════════════════════════
    #  PROPHETS & MESSENGERS — Anbiya wa Rusul
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": "adam",
        "name_arabic": "آدَم",
        "name_english": "Adam",
        "name_urdu": "آدم علیہ السلام",
        "also_known_as": ["The First Human", "Abu al-Bashar", "Khalifah"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Erred but repented sincerely; chosen, guided, and forgiven by Allah (20:122)",
        "era": "Beginning of humanity",
        "mentioned_in": [[2,30],[2,31],[2,33],[2,35],[2,36],[2,37],[3,33],[3,59],[5,27],[7,11],[7,19],[7,23],[7,26],[17,61],[18,50],[19,58],[20,115],[20,116],[20,120],[20,121],[20,122]],
        "story_summary": "Created from clay as Allah's vicegerent on earth. Taught the names of all things. Commanded to prostrate — Iblis refused. Placed in Jannah with Hawwa, forbidden one tree. Deceived by Iblis, ate from the tree, fell to earth. Repented with the words taught by Allah, was forgiven and chosen as a prophet. His story establishes: the nature of free will, the danger of Iblis, the power of repentance, and the purpose of human existence.",
        "urdu_summary": "مٹی سے بنائے گئے، اللہ کے خلیفہ۔ تمام چیزوں کے نام سکھائے گئے۔ ابلیس نے سجدہ نہ کیا۔ جنت میں رکھے گئے، ممنوعہ درخت کھایا، زمین پر اتارے گئے۔ اللہ کی سکھائی دعا سے توبہ کی، معاف ہوئے اور نبی چنے گئے۔",
        "lessons": [
            "Repentance wipes out any sin if sincere",
            "Iblis's arrogance (refusing to bow to Adam) is the root of all evil",
            "Knowledge (of names/reality) is humanity's distinguishing gift",
            "The earth is a test, not a punishment",
            "Human dignity was established before the first sin"
        ],
        "connections": ["hawwa", "iblis", "habil", "qabil"],
        "tags": ["creation", "repentance", "iblis", "free-will", "khalifah"]
    },

    {
        "id": "hawwa",
        "name_arabic": "حَوَّاء",
        "name_english": "Hawwa (Eve)",
        "name_urdu": "حوا علیہا السلام",
        "also_known_as": ["Eve", "Mother of Humanity"],
        "type": "person",
        "path": "straight",
        "path_reason": "Repented alongside Adam; mentioned with dignity in the Quran",
        "era": "Beginning of humanity",
        "mentioned_in": [[2,35],[2,36],[7,19],[7,20],[7,22],[7,23],[20,117],[20,120],[20,121]],
        "story_summary": "Created as a companion for Adam. Together they lived in Jannah. Iblis deceived them both into eating from the forbidden tree. Together they repented. The Quran always mentions them as a pair — no blame is placed solely on Hawwa, unlike in some other traditions. She is a symbol of human partnership and joint accountability.",
        "urdu_summary": "آدم کی ساتھی کے طور پر پیدا کی گئیں۔ دونوں نے مل کر ممنوعہ درخت کھایا اور مل کر توبہ کی۔ قرآن انہیں ہمیشہ جوڑے کے طور پر ذکر کرتا ہے — صرف ان پر الزام نہیں۔",
        "lessons": [
            "Accountability in Islam is individual — Quran does not blame Hawwa alone",
            "Partnership in both trial and repentance",
            "The Quran corrects the narrative that woman caused the fall"
        ],
        "connections": ["adam", "iblis"],
        "tags": ["creation", "repentance", "family", "partnership"]
    },

    {
        "id": "iblis",
        "name_arabic": "إِبْلِيس",
        "name_english": "Iblis (Satan)",
        "name_urdu": "ابلیس",
        "also_known_as": ["Shaytan", "Satan", "Al-Aduw (The Enemy)", "Al-Waswas"],
        "type": "jinn",
        "path": "deviated",
        "path_reason": "Refused to prostrate to Adam out of arrogance; declared enemy of humanity until Day of Judgment (7:11-18)",
        "era": "Pre-human creation; ongoing until Day of Judgment",
        "mentioned_in": [[2,34],[2,36],[3,36],[4,117],[4,119],[4,120],[7,11],[7,12],[7,13],[7,14],[7,15],[7,16],[7,17],[7,18],[14,22],[15,31],[15,32],[15,33],[15,34],[15,35],[15,36],[15,37],[15,38],[15,39],[15,40],[17,61],[17,62],[17,63],[17,64],[17,65],[18,50],[20,116],[26,95],[34,20],[35,6],[36,60],[38,71],[38,72],[38,73],[38,74],[38,75],[38,76],[38,77],[38,78],[38,79],[38,80],[38,81],[38,82],[38,83],[38,84],[38,85]],
        "story_summary": "A jinn (not an angel) who had risen to the rank of angels through worship. When Allah commanded the angels to prostrate to Adam, Iblis refused — saying he was made of fire and Adam of clay, fire being superior. Allah expelled him. He asked for respite until the Day of Judgment and was granted it. He then declared he would mislead humanity from every direction. His fundamental sin was arrogance (kibr) — the first sin in creation. He admitted Allah's existence and power but allowed pride to override obedience.",
        "urdu_summary": "ایک جن جو عبادت سے فرشتوں کی صف میں پہنچ گیا تھا۔ آدم کو سجدہ کرنے سے انکار کیا — کہا آگ سے ہوں، مٹی سے بہتر ہوں۔ نکالا گیا۔ قیامت تک مہلت مانگی اور ملی۔ انسانیت کو گمراہ کرنے کا اعلان کیا۔ اس کا گناہ تکبر تھا۔",
        "lessons": [
            "Arrogance (kibr) is the root sin — it was the first act of disobedience in creation",
            "Worship without humility is worthless",
            "Knowledge of Allah does not guarantee obedience — Iblis knew Allah perfectly",
            "Iblis is a jinn, not a fallen angel — important theological distinction",
            "His strategy: come from front, back, left, right — comprehensive attack on human resolve"
        ],
        "connections": ["adam", "hawwa", "habil", "qabil"],
        "tags": ["deviated", "arrogance", "jinn", "enemy", "deception", "kibr"]
    },

    {
        "id": "nuh",
        "name_arabic": "نُوح",
        "name_english": "Nuh (Noah)",
        "name_urdu": "نوح علیہ السلام",
        "also_known_as": ["Noah", "Shaykhul Anbiya (Elder of Prophets)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Among the five greatest Messengers (Ulul Azm); praised for steadfast patience over 950 years of calling",
        "era": "Early human history, pre-Ibrahim",
        "mentioned_in": [[3,33],[4,163],[6,84],[7,59],[7,60],[7,61],[7,62],[7,63],[7,64],[9,70],[10,71],[10,72],[10,73],[11,25],[11,26],[11,27],[11,28],[11,29],[11,30],[11,31],[11,32],[11,33],[11,34],[11,35],[11,36],[11,37],[11,38],[11,39],[11,40],[11,41],[11,42],[11,43],[11,44],[11,45],[11,46],[11,47],[11,48],[14,9],[17,3],[17,17],[19,58],[21,76],[21,77],[22,42],[23,23],[23,24],[23,25],[23,26],[23,27],[23,28],[23,29],[26,105],[26,106],[26,107],[26,108],[26,109],[26,110],[26,111],[26,112],[26,113],[26,114],[26,115],[26,116],[26,117],[26,118],[26,119],[26,120],[26,121],[26,122],[29,14],[29,15],[33,7],[37,75],[37,76],[37,77],[37,78],[37,79],[37,80],[37,81],[37,82],[38,12],[40,5],[40,31],[42,13],[51,46],[53,52],[54,9],[54,10],[54,11],[54,12],[54,13],[54,14],[54,15],[57,26],[66,10],[71,1]],
        "story_summary": "Called his people for 950 years (29:14). They rejected him, mocked him, and covered their ears. His own son and wife disbelieved. Allah commanded him to build the ark — he was mocked for it. The flood came and destroyed the disbelievers. His son refused to board, saying he would climb a mountain — Nuh interceded for him, but Allah told him his son was not of his family (by faith). A profound lesson: lineage does not guarantee salvation. Nuh is one of the five Ulul Azm prophets.",
        "urdu_summary": "950 سال تک اپنی قوم کو دعوت دی۔ انہوں نے کانوں میں انگلیاں ڈال لیں۔ کشتی بنانے کا حکم ملا، مذاق اڑایا گیا۔ طوفان آیا۔ بیٹے نے سوار ہونے سے انکار کیا، پہاڑ پر چڑھنے کی کوشش کی۔ نوح نے بیٹے کے لیے سفارش کی لیکن اللہ نے کہا وہ آپ کے گھر والوں میں سے نہیں — نسب نجات نہیں دیتا، ایمان دیتا ہے۔",
        "lessons": [
            "Patience in dawah — 950 years of calling with almost no results",
            "Family bonds do not override faith — Nuh's son and wife were not saved",
            "No one is too far to call — but no one is guaranteed guidance",
            "Mocking the truth is a sign of a doomed civilization",
            "Salvation is by faith, not by birth or relationship to a prophet"
        ],
        "connections": ["wife_of_nuh", "son_of_nuh", "iblis"],
        "tags": ["prophet", "patience", "flood", "dawah", "family", "straight"]
    },

    {
        "id": "wife_of_nuh",
        "name_arabic": "امرأة نوح",
        "name_english": "Wife of Nuh",
        "name_urdu": "نوح کی بیوی",
        "also_known_as": ["Waila (according to some traditions)"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Disbelieved and betrayed her prophet husband; cited as a warning example in 66:10",
        "era": "Time of Nuh",
        "mentioned_in": [[11,27],[66,10]],
        "story_summary": "The Quran presents her as one of two women cited as warnings (66:10) — alongside the wife of Lut. She was married to a prophet yet chose disbelief. She betrayed him — scholars say through mockery and revealing his private matters to his enemies. Her closeness to a prophet did not save her. She is a sobering reminder that marriage to a righteous person does not guarantee guidance.",
        "urdu_summary": "نوح جیسے نبی کی بیوی ہونے کے باوجود کافر رہی۔ قرآن نے اسے عبرت کی مثال کے طور پر (66:10) پیش کیا۔ نسب یا رشتہ نجات کی ضمانت نہیں۔",
        "lessons": [
            "Proximity to a prophet does not guarantee guidance",
            "Faith is an individual choice — no spouse can carry another's burden",
            "Betrayal of trust is a major sin"
        ],
        "connections": ["nuh", "wife_of_lut"],
        "tags": ["deviated", "warning", "family", "disbelief"]
    },

    {
        "id": "son_of_nuh",
        "name_arabic": "ابن نوح",
        "name_english": "Son of Nuh (Kan'an)",
        "name_urdu": "نوح کا بیٹا",
        "also_known_as": ["Kan'an (according to some traditions)"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Refused to board the ark; trusted in his own plan (mountain) over Allah's salvation; drowned (11:42-43)",
        "era": "Time of Nuh, the flood",
        "mentioned_in": [[11,42],[11,43],[11,45],[11,46],[11,47]],
        "story_summary": "When the flood came and Nuh called his son to board the ark, the son refused — saying he would climb a mountain to save himself. He trusted his own strategy over divine guidance. He drowned. Nuh then interceded with Allah for his son, but Allah revealed that the son was not 'of his family' because he was not of faith. This was a painful lesson for Nuh himself about the limits of parental love and the meaning of 'family' in Islam.",
        "urdu_summary": "طوفان کے وقت نوح نے کشتی پر آنے کو کہا۔ بیٹے نے پہاڑ پر چڑھنے کا ارادہ کیا — اپنی تدبیر پر بھروسہ کیا۔ ڈوب گیا۔ نوح نے سفارش کی تو اللہ نے کہا وہ آپ کے گھر والوں میں سے نہیں تھا — ایمان نہ تھا اس کے پاس۔",
        "lessons": [
            "Self-reliance against divine guidance leads to destruction",
            "Family in Islam is defined by faith, not blood",
            "A prophet's love for his child cannot override divine decree",
            "Arrogance in crisis — the mountain vs the ark — is fatal"
        ],
        "connections": ["nuh", "wife_of_nuh"],
        "tags": ["deviated", "family", "arrogance", "flood"]
    },

    {
        "id": "hud",
        "name_arabic": "هُود",
        "name_english": "Hud",
        "name_urdu": "ہود علیہ السلام",
        "also_known_as": [],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Remained steadfast in calling his people; saved when they were destroyed",
        "era": "Ancient Arabia — sent to the people of Aad",
        "mentioned_in": [[7,65],[7,66],[7,67],[7,68],[7,69],[7,70],[7,71],[7,72],[11,50],[11,51],[11,52],[11,53],[11,54],[11,55],[11,56],[11,57],[11,58],[11,59],[11,60],[26,123],[26,124],[26,125],[26,126],[26,127],[26,128],[26,129],[26,130],[26,131],[26,132],[26,133],[26,134],[26,135],[26,136],[26,137],[26,138],[26,139],[26,140],[46,21],[46,22],[46,23],[46,24],[46,25],[46,26]],
        "story_summary": "Sent to the people of Aad — a powerful civilization in ancient Arabia known for their towering pillars and physical strength. They were arrogant about their power ('Who is mightier than us?'). Hud called them to worship Allah alone, abandon arrogance, and stop oppressing others. They rejected and mocked him. Allah sent a violent wind that destroyed them for seven nights and eight days (69:6-7). Hud and the believers were saved.",
        "urdu_summary": "عاد قوم کی طرف بھیجے گئے — طاقتور اور متکبر لوگ۔ توحید کی دعوت دی، انہوں نے انکار کیا۔ سات راتیں آٹھ دن کی آندھی نے انہیں تباہ کر دیا۔ ہود اور مومنین بچ گئے۔",
        "lessons": [
            "Physical strength and civilization are no protection against divine punishment",
            "Arrogance about power ('who is mightier than us?') is particularly dangerous",
            "The caller's duty is only to convey — results are with Allah"
        ],
        "connections": ["people_of_aad"],
        "tags": ["prophet", "straight", "aad", "wind", "dawah"]
    },

    {
        "id": "salih",
        "name_arabic": "صَالِح",
        "name_english": "Salih",
        "name_urdu": "صالح علیہ السلام",
        "also_known_as": [],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Steadfast messenger to Thamud; saved when they were destroyed",
        "era": "Ancient Arabia — sent to the people of Thamud",
        "mentioned_in": [[7,73],[7,74],[7,75],[7,76],[7,77],[7,78],[7,79],[11,61],[11,62],[11,63],[11,64],[11,65],[11,66],[11,67],[11,68],[26,141],[26,142],[26,143],[26,144],[26,145],[26,146],[26,147],[26,148],[26,149],[26,150],[26,151],[26,152],[26,153],[26,154],[26,155],[26,156],[26,157],[26,158],[27,45],[27,46],[27,47],[27,48],[27,49],[27,50],[27,51],[27,52],[27,53],[54,23],[54,24],[54,25],[54,26],[54,27],[54,28],[54,29],[54,30],[54,31],[91,11],[91,12],[91,13],[91,14],[91,15]],
        "story_summary": "Sent to Thamud, a people who carved homes in mountains. Given the miracle of the she-camel of Allah — a sign, told to let her graze freely and drink from the water. If they harmed her, punishment would come. They hamstrung the she-camel. Salih warned them of three days. On the third day, a mighty blast (sayhah) destroyed them. The story is a stark lesson about respecting divine signs and the consequences of crossing clear boundaries.",
        "urdu_summary": "ثمود قوم کی طرف بھیجے گئے جو پہاڑوں میں گھر تراشتے تھے۔ اونٹنی کا معجزہ دیا گیا — اسے آزاد چھوڑیں، پانی پینے دیں۔ انہوں نے اونٹنی کی کونچیں کاٹ دیں۔ تین دن کی مہلت دی گئی۔ تیسرے دن چنگھاڑ نے سب کو ہلاک کر دیا۔",
        "lessons": [
            "Crossing a clear divine boundary (the she-camel) brings irreversible consequences",
            "Signs from Allah are not to be challenged or dismissed",
            "Peer pressure in sin — only one person hamstrung the camel but all bore responsibility (91:12)",
            "Three days warning — Allah gives time even after transgression"
        ],
        "connections": ["people_of_thamud"],
        "tags": ["prophet", "straight", "thamud", "she-camel", "miracle"]
    },

    {
        "id": "ibrahim",
        "name_arabic": "إِبْرَاهِيم",
        "name_english": "Ibrahim (Abraham)",
        "name_urdu": "ابراہیم علیہ السلام",
        "also_known_as": ["Abraham", "Khalilullah (Friend of Allah)", "Abu al-Anbiya (Father of Prophets)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Khalilullah — the Friend of Allah; completed every test; Imam of all who turn to Allah (2:124)",
        "era": "Approximately 2000 BCE, Mesopotamia and Arabia",
        "mentioned_in": [[2,124],[2,125],[2,126],[2,127],[2,128],[2,129],[2,130],[2,131],[2,132],[2,133],[2,135],[2,136],[2,140],[2,258],[2,260],[3,33],[3,65],[3,67],[3,68],[3,84],[3,95],[4,54],[4,125],[4,163],[6,74],[6,75],[6,76],[6,77],[6,78],[6,79],[6,80],[6,81],[6,83],[6,161],[9,114],[11,69],[11,70],[11,71],[11,72],[11,73],[11,74],[11,75],[11,76],[12,6],[12,38],[14,35],[14,36],[14,37],[14,38],[14,39],[14,40],[14,41],[15,51],[15,52],[15,53],[15,54],[15,55],[15,56],[15,57],[15,58],[16,120],[16,121],[16,122],[16,123],[19,41],[19,42],[19,43],[19,44],[19,45],[19,46],[19,47],[19,48],[19,49],[21,51],[21,52],[21,53],[21,54],[21,55],[21,56],[21,57],[21,58],[21,59],[21,60],[21,61],[21,62],[21,63],[21,64],[21,65],[21,66],[21,67],[21,68],[21,69],[21,70],[21,71],[22,26],[22,78],[26,69],[26,70],[26,71],[26,72],[26,73],[26,74],[26,75],[26,76],[26,77],[26,78],[26,79],[26,80],[26,81],[26,82],[26,83],[26,84],[26,85],[26,86],[26,87],[26,88],[26,89],[29,16],[29,17],[29,18],[29,25],[29,26],[29,27],[33,7],[37,83],[37,84],[37,85],[37,86],[37,87],[37,88],[37,89],[37,90],[37,91],[37,92],[37,93],[37,94],[37,95],[37,96],[37,97],[37,98],[37,99],[37,100],[37,101],[37,102],[37,103],[37,104],[37,105],[37,106],[37,107],[37,108],[37,109],[37,110],[37,111],[38,45],[42,13],[43,26],[43,27],[43,28],[51,24],[51,25],[51,26],[51,27],[51,28],[51,29],[51,30],[53,37],[57,26],[60,4],[87,19]],
        "story_summary": "Born in Ur (Iraq), raised in a polytheist family where his father Azar carved idols. As a youth he questioned the idols, stars, moon, and sun — rejecting each when they set or proved powerless. He smashed the idols of his people, was thrown into a fire by Nimrod — the fire was made cool and safe for him. He left his homeland, traveled to multiple lands. He took his wife Hajar and infant son Ismail to the barren valley of Makkah and left them by Allah's command. The well of Zamzam appeared. Later commanded to sacrifice his son Ismail — both submitted, and Allah ransomed Ismail with a great sacrifice. He built the Kaaba with Ismail and made the famous dua for his descendants. His whole life was a series of tests, all of which he passed. Allah called him 'Khalilullah' — His close friend.",
        "urdu_summary": "بت تراش باپ کے گھر پیدا ہوئے، ستاروں، چاند، سورج کو رب نہ مانا۔ بت توڑے، نمرود نے آگ میں پھینکا — آگ ٹھنڈی ہو گئی۔ ہاجرہ اور اسماعیل کو مکہ میں چھوڑا۔ زمزم ظاہر ہوا۔ اسماعیل کو ذبح کا حکم — دونوں نے سر تسلیم خم کیا، اللہ نے دنبہ بھیجا۔ کعبہ تعمیر کی۔ خلیل اللہ کا لقب ملا۔",
        "lessons": [
            "Use your own reason to reach truth — Ibrahim's journey from stars to Allah",
            "Standing alone against everyone for truth",
            "Tawakkul — leaving family in a barren valley by Allah's command",
            "The supreme test: being commanded to sacrifice your beloved son",
            "Dua for your children and descendants is one of the most powerful acts",
            "Khalilullah — you can achieve friendship with Allah through complete devotion"
        ],
        "connections": ["azar", "ismail", "ishaq", "hajar", "sarah", "lut", "nimrod"],
        "tags": ["prophet", "straight", "khalilullah", "tawheed", "test", "kaaba", "sacrifice"]
    },

    {
        "id": "azar",
        "name_arabic": "آزَر",
        "name_english": "Azar (Father of Ibrahim)",
        "name_urdu": "آزر",
        "also_known_as": ["Terah (in some traditions)"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Idol-maker who rejected his own son's sincere call to tawheed; died on shirk (9:114)",
        "era": "Time of Ibrahim",
        "mentioned_in": [[6,74],[9,114],[19,42],[19,43],[19,44],[19,45],[19,46],[19,47],[26,70],[26,71],[26,72],[26,73],[26,74],[37,85],[43,26],[43,27],[60,4]],
        "story_summary": "The father (or uncle by some interpretations) of Ibrahim who carved and worshipped idols. Ibrahim called him with extraordinary gentleness — 'O dear father' (ya abati) — multiple times. He refused repeatedly and finally threatened to stone Ibrahim and told him to leave. Ibrahim left, promising to seek forgiveness for him. Later, when Ibrahim discovered his father had died on shirk, he disassociated from him as Allah commanded (9:114). A profound lesson in da'wah to family — never harsh, always gentle — but also in accepting that guidance is from Allah alone.",
        "urdu_summary": "ابراہیم کے والد جو بت بناتے اور پوجتے تھے۔ ابراہیم نے نہایت نرمی سے 'یا ابتِ' کہہ کر بار بار بلایا۔ انہوں نے انکار کیا اور پتھر مارنے کی دھمکی دی۔ شرک پر مرے تو ابراہیم نے ان سے برائت کا اعلان کیا (9:114)۔",
        "lessons": [
            "Call family with extreme gentleness — Ibrahim's model of 'ya abati'",
            "You cannot guide whom you love — guidance is from Allah alone",
            "After death on disbelief, loyalty to Allah supersedes family loyalty",
            "Gentleness in da'wah is a prophetic method, even when rejected"
        ],
        "connections": ["ibrahim", "nimrod"],
        "tags": ["deviated", "shirk", "family", "dawah", "idol-worship"]
    },

    {
        "id": "nimrod",
        "name_arabic": "النَّمْرُود",
        "name_english": "Nimrod (Namrud)",
        "name_urdu": "نمرود",
        "also_known_as": ["Namrud"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Claimed divinity, threw Ibrahim into fire, argued with Ibrahim about the Lord of life and death (2:258)",
        "era": "Time of Ibrahim, ancient Mesopotamia",
        "mentioned_in": [[2,258],[21,68],[21,69]],
        "story_summary": "The king of the time of Ibrahim who claimed to be a god. The Quran records his debate with Ibrahim (2:258): Ibrahim said his Lord gives life and causes death; Nimrod said 'I give life and death' (by releasing and executing prisoners). Ibrahim then said 'Allah brings the sun from the East — bring it from the West.' Nimrod was confounded. He ordered Ibrahim burned — the fire became cool. According to tradition, he eventually died killed by a mosquito that entered his nostril — the mightiest king, destroyed by the most insignificant creature.",
        "urdu_summary": "ابراہیم کے زمانے کا بادشاہ جو خدائی کا دعویٰ کرتا تھا۔ ابراہیم سے بحث کی (2:258)۔ آگ میں جلانے کا حکم دیا لیکن آگ ٹھنڈی ہو گئی۔ روایت کے مطابق مچھر سے مرا۔",
        "lessons": [
            "Power and wealth breed delusion of divinity",
            "Ibrahim's logical argument silenced the most powerful king",
            "Allah uses the smallest means to destroy the greatest tyrants",
            "Claiming divinity is the ultimate arrogance — and always falls"
        ],
        "connections": ["ibrahim", "azar"],
        "tags": ["deviated", "tyrant", "shirk", "arrogance", "power"]
    },

    {
        "id": "ismail",
        "name_arabic": "إِسْمَاعِيل",
        "name_english": "Ismail (Ishmael)",
        "name_urdu": "اسماعیل علیہ السلام",
        "also_known_as": ["Ishmael", "Dhbihullah (the one to be sacrificed)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Submitted to the command of sacrifice without hesitation; praised as truthful and a prophet (19:54)",
        "era": "Time of Ibrahim, ancient Makkah",
        "mentioned_in": [[2,125],[2,127],[2,133],[2,136],[2,140],[3,84],[4,163],[6,86],[14,39],[19,54],[19,55],[21,85],[37,101],[37,102],[37,103],[37,107],[37,108],[38,48]],
        "story_summary": "Son of Ibrahim and Hajar, left as an infant in the barren valley of Makkah. The Zamzam well appeared for him. When old enough, Ibrahim told him of the dream command to sacrifice him. Ismail's response was immediate and complete submission: 'Do what you are commanded; you will find me, if Allah wills, of the patient' (37:102). He laid himself down. Allah ransomed him with a great sacrifice. Later he helped his father build the Kaaba. He is the ancestor of the Prophet Muhammad ﷺ.",
        "urdu_summary": "ابراہیم اور ہاجرہ کے بیٹے، مکہ کی بے آب و گیاہ وادی میں چھوڑے گئے۔ ذبح کے خواب کا سنا تو فوراً راضی ہو گئے: 'جو حکم ہے کریں، مجھے صبر والوں میں پائیں گے' (37:102)۔ اللہ نے دنبہ بھیجا۔ کعبہ کی تعمیر میں باپ کے ساتھ ہاتھ بٹایا۔",
        "lessons": [
            "Complete submission to Allah even in the ultimate test",
            "Sabr (patience) declared before the test even begins",
            "Father and son both submitted — tawakkul is generational",
            "The meaning of Islam — submission — embodied perfectly"
        ],
        "connections": ["ibrahim", "hajar", "ishaq"],
        "tags": ["prophet", "straight", "sacrifice", "submission", "kaaba", "sabr"]
    },

    {
        "id": "hajar",
        "name_arabic": "هَاجَر",
        "name_english": "Hajar (Hagar)",
        "name_urdu": "ہاجرہ علیہا السلام",
        "also_known_as": ["Hagar"],
        "type": "person",
        "path": "straight",
        "path_reason": "Exemplary tawakkul — asked once 'did Allah command this?' then fully submitted; her sa'y between Safa and Marwa became an eternal rite",
        "era": "Time of Ibrahim, ancient Makkah",
        "mentioned_in": [[2,158],[14,37]],
        "story_summary": "Wife of Ibrahim and mother of Ismail. Left with her infant in the barren, uninhabited valley of Makkah by Ibrahim on Allah's command. When Ibrahim turned to leave, she asked: 'Did Allah command you to do this?' He said yes. She said: 'Then He will not let us be lost.' She ran between Safa and Marwa seven times in desperate search of water for her dying child. The Zamzam well burst forth. Her run (sa'y) became one of the five pillars of Hajj — preserved for all time. She is the mother of Ismail and grandmother of the Arab prophets.",
        "urdu_summary": "ابراہیم کی بیوی، اسماعیل کی ماں۔ ننھے بچے کے ساتھ بے آب و گیاہ مکہ میں چھوڑی گئیں۔ پوچھا: 'اللہ کا حکم ہے؟' ہاں سنا تو کہا: 'اللہ ہمیں ضائع نہیں کرے گا'۔ صفا مروہ کے درمیان دوڑیں — یہ سعی قیامت تک حج کا رکن ہے۔ زمزم ظاہر ہوا۔",
        "lessons": [
            "The greatest tawakkul in Quran — 'then He will not let us be lost'",
            "Action + trust: she ran (took action) while trusting Allah",
            "One woman's act of desperation and faith became eternal worship for billions",
            "Asking one clear question — 'is this Allah's command?' — and then fully submitting"
        ],
        "connections": ["ibrahim", "ismail"],
        "tags": ["straight", "tawakkul", "hajj", "zamzam", "safa-marwa", "mother"]
    },

    {
        "id": "sarah",
        "name_arabic": "سَارَة",
        "name_english": "Sarah",
        "name_urdu": "سارہ علیہا السلام",
        "also_known_as": [],
        "type": "person",
        "path": "straight",
        "path_reason": "Wife of Ibrahim, mother of Ishaq; laughed in disbelief at glad tidings then corrected herself",
        "era": "Time of Ibrahim",
        "mentioned_in": [[11,71],[11,72],[51,29],[51,30]],
        "story_summary": "Wife of Ibrahim and mother of Ishaq. When the angels visited with glad tidings that she would bear a son despite being old and barren, she laughed and said 'Woe to me! Shall I bear a child when I am an old woman and this, my husband, is an old man?' The angels confirmed it was the decree of Allah. A brief moment of doubt quickly corrected — she became the mother of Ishaq, grandfather of the Tribes of Israel.",
        "urdu_summary": "ابراہیم کی بیوی اور اسحاق کی ماں۔ فرشتوں نے بیٹے کی خوشخبری دی تو بوڑھی ہونے پر تعجب سے ہنس پڑیں۔ فرشتوں نے کہا یہ اللہ کا حکم ہے — مان گئیں۔ اسحاق کی ماں بنیں۔",
        "lessons": [
            "Human reaction to the miraculous — initial disbelief quickly corrected by faith",
            "Allah's power is not limited by natural laws",
            "Both Hajar and Sarah were honored wives of Ibrahim with different, equally valid roles"
        ],
        "connections": ["ibrahim", "ishaq", "hajar"],
        "tags": ["straight", "miracle", "family"]
    },

    {
        "id": "lut",
        "name_arabic": "لُوط",
        "name_english": "Lut (Lot)",
        "name_urdu": "لوط علیہ السلام",
        "also_known_as": ["Lot"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Steadfast prophet; warned his people for years; saved with his family (except his wife) when the cities were destroyed",
        "era": "Time of Ibrahim; the cities of Sodom and Gomorrah",
        "mentioned_in": [[6,86],[7,80],[7,81],[7,82],[7,83],[7,84],[11,69],[11,70],[11,71],[11,72],[11,73],[11,74],[11,77],[11,78],[11,79],[11,80],[11,81],[11,82],[11,83],[15,57],[15,58],[15,59],[15,60],[15,61],[15,62],[15,63],[15,64],[15,65],[15,66],[15,67],[15,68],[15,69],[15,70],[15,71],[15,72],[21,71],[21,74],[21,75],[22,43],[26,160],[26,161],[26,162],[26,163],[26,164],[26,165],[26,166],[26,167],[26,168],[26,169],[26,170],[26,171],[26,172],[26,173],[27,54],[27,55],[27,56],[27,57],[27,58],[29,26],[29,28],[29,29],[29,30],[29,31],[29,32],[29,33],[29,34],[29,35],[37,133],[37,134],[37,135],[37,136],[37,137],[54,33],[54,34],[54,35],[54,36],[54,37],[66,10]],
        "story_summary": "Nephew of Ibrahim, sent as prophet to the cities known for their sexual transgression (homosexual practice as a public norm, robbery, and rejection of guests). His people openly rejected his call, threatened to expel him, and even came to his house seeking his angel guests. He was distressed, having only his daughters to shield against them. The angels revealed they were sent to destroy the city. Lut and his believing daughters were told to leave at night without looking back. His wife looked back and was destroyed with the people. The cities were turned upside down and stones of clay rained upon them.",
        "urdu_summary": "ابراہیم کے بھتیجے، گناہ کی قوم کی طرف بھیجے گئے۔ قوم نے مہمانوں (فرشتوں) سے بدکاری کا ارادہ کیا۔ لوط پریشان ہوئے۔ فرشتوں نے بتایا کہ ہم قوم کو تباہ کرنے آئے ہیں۔ رات کو نکل جاؤ، پیچھے نہ دیکھو۔ بیوی نے دیکھا، ہلاک ہوئی۔ شہر الٹے گئے، پتھروں کی بارش ہوئی۔",
        "lessons": [
            "Public normalization of transgression brings collective punishment",
            "A prophet's loneliness — 'I wish I had strength against you or refuge in a strong support' (11:80)",
            "Leaving a sinful environment when escape is possible",
            "A spouse's disbelief can end in destruction even while the prophet is saved"
        ],
        "connections": ["ibrahim", "wife_of_lut", "people_of_lut"],
        "tags": ["prophet", "straight", "transgression", "destruction", "family"]
    },

    {
        "id": "wife_of_lut",
        "name_arabic": "امرأة لوط",
        "name_english": "Wife of Lut",
        "name_urdu": "لوط کی بیوی",
        "also_known_as": ["Waligha (according to some traditions)"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Sided with the people of transgression; looked back in disobedience and was destroyed; cited as a warning in 66:10",
        "era": "Time of Lut",
        "mentioned_in": [[7,83],[11,81],[15,60],[26,171],[27,57],[29,32],[29,33],[37,135],[66,10]],
        "story_summary": "Wife of the prophet Lut who secretly sympathized with her people rather than her husband. When the family fled, she was commanded not to look back but she did — and was destroyed with the people. She is paired with the wife of Nuh in Surah At-Tahrim (66:10) as a dual warning: marriage to a prophet does not save you. She betrayed her husband by informing the people of the presence of guests.",
        "urdu_summary": "لوط کی بیوی جو اپنے شوہر سے نہیں بلکہ قوم کی ہم نوا تھی۔ پیچھے مڑ کر دیکھا، ہلاک ہوئی۔ زوجۃ نوح کے ساتھ عبرت کی مثال (66:10)۔",
        "lessons": [
            "Internal loyalty is what matters — not external proximity to a prophet",
            "One act of disobedience (looking back) brought destruction",
            "Betrayal of trust within the household is a serious sin"
        ],
        "connections": ["lut", "wife_of_nuh"],
        "tags": ["deviated", "warning", "family", "disobedience"]
    },

    {
        "id": "ishaq",
        "name_arabic": "إِسْحَاق",
        "name_english": "Ishaq (Isaac)",
        "name_urdu": "اسحاق علیہ السلام",
        "also_known_as": ["Isaac"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Prophet and righteous son of Ibrahim; ancestor of many prophets",
        "era": "Time of Ibrahim and beyond",
        "mentioned_in": [[2,133],[2,136],[2,140],[3,84],[4,163],[6,84],[11,71],[12,6],[12,38],[14,39],[19,49],[21,72],[29,27],[37,112],[37,113],[38,45]],
        "story_summary": "Son of Ibrahim and Sarah, born miraculously to an elderly barren woman. Promised by angels as a bearer of knowledge (37:113). Father of Yaqub (Jacob), grandfather of Yusuf. Ancestor of all the Israelite prophets. His miraculous birth from an old mother confirmed the unlimited power of Allah.",
        "urdu_summary": "ابراہیم اور سارہ کے بیٹے، معجزاتی ولادت۔ یعقوب کے باپ، یوسف کے دادا۔ بنی اسرائیل کے انبیاء کے جد امجد۔",
        "lessons": [
            "Miracles of birth — Allah's power over natural limits",
            "Prophecy can run in families — but it is Allah's gift, not inheritance"
        ],
        "connections": ["ibrahim", "sarah", "yaqub", "ismail"],
        "tags": ["prophet", "straight", "family", "miracle"]
    },

    {
        "id": "yaqub",
        "name_arabic": "يَعْقُوب",
        "name_english": "Yaqub (Jacob)",
        "name_urdu": "یعقوب علیہ السلام",
        "also_known_as": ["Jacob", "Israel", "Abu Yusuf"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Maintained faith through decades of grief over Yusuf; his grief was worship not complaint (12:86)",
        "era": "Patriarch era, Canaan",
        "mentioned_in": [[2,132],[2,133],[2,136],[2,140],[3,84],[4,163],[6,84],[11,71],[12,4],[12,5],[12,6],[12,7],[12,8],[12,11],[12,12],[12,13],[12,14],[12,16],[12,17],[12,18],[12,63],[12,64],[12,65],[12,66],[12,67],[12,68],[12,83],[12,84],[12,85],[12,86],[12,87],[12,93],[12,94],[12,96],[12,97],[12,98],[12,99],[12,100],[19,6],[19,49],[21,72],[29,27],[38,45]],
        "story_summary": "Son of Ishaq, father of twelve sons including Yusuf. Warned Yusuf not to tell his brothers his dream. When Yusuf disappeared, his brothers brought back a false blood-stained shirt. Yaqub said 'Sabrun jamil — beautiful patience' and declared they had fabricated something. He wept so much for Yusuf that he lost his sight. When accused of losing himself in grief, he said 'I complain of my suffering only to Allah' (12:86). He never lost hope in Yusuf being alive. Years later his sight was restored when Yusuf's shirt was placed on his face.",
        "urdu_summary": "اسحاق کے بیٹے، یوسف کے باپ۔ یوسف کے غائب ہونے پر خون آلود قمیص لائی گئی۔ 'صبر جمیل' کہا۔ اتنا رویا کہ آنکھیں چلی گئیں۔ کہا: 'میں اپنا غم صرف اللہ سے کہتا ہوں' (12:86)۔ یوسف کی امید کبھی نہ چھوڑی۔",
        "lessons": [
            "Sabrun jamil — beautiful patience that does not include complaint to people",
            "Grief expressed to Allah alone is not weakness — it is worship",
            "Never lose hope in Allah's mercy — 'do not despair of relief from Allah' (12:87)",
            "A father's love and a prophet's faith can coexist",
            "Certainty about inner sense — he knew Yusuf was alive despite all evidence otherwise"
        ],
        "connections": ["ishaq", "yusuf", "ibrahim", "sons_of_yaqub"],
        "tags": ["prophet", "straight", "patience", "grief", "family", "hope"]
    },

    {
        "id": "yusuf",
        "name_arabic": "يُوسُف",
        "name_english": "Yusuf (Joseph)",
        "name_urdu": "یوسف علیہ السلام",
        "also_known_as": ["Joseph", "Ahsanul Qasas (Best of Stories)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Maintained faith, chastity, and forgiveness through betrayal, slavery, imprisonment, and power",
        "era": "Patriarch era, Canaan and Egypt",
        "mentioned_in": [[6,84],[12,4],[12,5],[12,6],[12,7],[12,8],[12,9],[12,10],[12,11],[12,12],[12,13],[12,14],[12,15],[12,16],[12,17],[12,18],[12,19],[12,20],[12,21],[12,22],[12,23],[12,24],[12,25],[12,26],[12,27],[12,28],[12,29],[12,30],[12,31],[12,32],[12,33],[12,34],[12,35],[12,36],[12,37],[12,38],[12,39],[12,40],[12,41],[12,42],[12,43],[12,44],[12,45],[12,46],[12,47],[12,48],[12,49],[12,50],[12,51],[12,52],[12,53],[12,54],[12,55],[12,56],[12,57],[12,58],[12,59],[12,60],[12,61],[12,62],[12,63],[12,64],[12,65],[12,66],[12,67],[12,68],[12,69],[12,70],[12,71],[12,72],[12,73],[12,74],[12,75],[12,76],[12,77],[12,78],[12,79],[12,80],[12,81],[12,82],[12,83],[12,84],[12,85],[12,86],[12,87],[12,88],[12,89],[12,90],[12,91],[12,92],[12,93],[12,94],[12,95],[12,96],[12,97],[12,98],[12,99],[12,100],[12,101],[40,34]],
        "story_summary": "The most complete human story in the Quran — the entire Surah Yusuf is his story, called 'the best of stories' (12:3). Thrown into a well by jealous brothers. Sold as a slave in Egypt. Bought by a noble household. Seduced by his master's wife (Zulaikha) — he chose prison over sin. In prison, interpreted dreams. Eventually brought before the king to interpret the royal dream. Appointed minister of Egypt's treasury. Reunited with his brothers — who came begging for food — and finally with his father Yaqub. His response to his brothers' betrayal: 'No blame on you today' (12:92). At the pinnacle of power, his prayer was to die as a Muslim and be with the righteous (12:101).",
        "urdu_summary": "کنویں میں پھینکے گئے بھائیوں نے۔ غلام بنا کر مصر بھیجے گئے۔ زلیخا نے بہکانا چاہا — جیل قبول کی گناہ نہ کیا۔ خواب کی تعبیر سے وزیر بنے۔ بھائی فاقہ سے آئے — 'آج تم پر کوئی ملامت نہیں' (12:92)۔ اقتدار کی بلندی پر دعا کی: مسلمان مروں اور صالحین میں شامل کرو (12:101)۔",
        "lessons": [
            "Every stage of Yusuf's suffering was a step toward a higher station",
            "Choosing prison over sin — the greatest choice",
            "Forgiveness at the height of power is the mark of true nobility",
            "Never use power for revenge — use it for mercy",
            "Dreams are real — divine communication through visions",
            "Sabr without despair leads to the most beautiful outcomes"
        ],
        "connections": ["yaqub", "zulaikha", "sons_of_yaqub", "ishaq", "ibrahim"],
        "tags": ["prophet", "straight", "patience", "chastity", "forgiveness", "power", "dream"]
    },

    {
        "id": "zulaikha",
        "name_arabic": "زُلَيْخَا",
        "name_english": "Zulaikha (Wife of Al-Aziz)",
        "name_urdu": "زلیخا",
        "also_known_as": ["Wife of Al-Aziz", "Imra'at al-Aziz"],
        "type": "person",
        "path": "mixed",
        "path_reason": "Attempted to seduce Yusuf, falsely imprisoned him, but ultimately confessed the truth (12:51)",
        "era": "Time of Yusuf, Egypt",
        "mentioned_in": [[12,23],[12,24],[12,25],[12,26],[12,27],[12,28],[12,29],[12,30],[12,31],[12,32],[12,51]],
        "story_summary": "Wife of the Egyptian nobleman (Al-Aziz) who bought Yusuf. She fell deeply in love with Yusuf and tried to seduce him. He refused and ran — she tore his shirt from behind. When her husband came, Yusuf said she seduced him; she said he tried to seduce her. The evidence of the torn shirt proved Yusuf's innocence. She then summoned the women of the city who were gossiping; they were so struck by Yusuf's beauty they cut their hands. She admitted privately that she had tried to seduce him. Eventually, before the king, she publicly confessed: 'Now the truth has come to light — it was I who tried to seduce him, and he is indeed of the truthful' (12:51).",
        "urdu_summary": "عزیز مصر کی بیوی جس نے یوسف کو ورغلانا چاہا۔ یوسف نے انکار کیا، بھاگے، قمیص پیچھے سے پھٹی — ثبوت یوسف کے حق میں۔ شہر کی عورتیں باتیں کرنے لگیں تو بلایا — سب نے ہاتھ کاٹ لیے۔ آخرکار بادشاہ کے سامنے اعتراف: 'میں نے ہی ورغلانا چاہا تھا، یوسف سچے ہیں' (12:51)۔",
        "lessons": [
            "Obsessive love that crosses boundaries leads to great sin and suffering",
            "Truth emerges even from the most carefully constructed lie",
            "Public confession of wrongdoing — the courage of Zulaikha's ultimate admission",
            "A person can be both perpetrator and eventual truth-teller"
        ],
        "connections": ["yusuf", "aziz_of_egypt"],
        "tags": ["mixed", "temptation", "confession", "love", "truth"]
    },

    {
        "id": "sons_of_yaqub",
        "name_arabic": "أبناء يعقوب",
        "name_english": "Brothers of Yusuf",
        "name_urdu": "یوسف کے بھائی",
        "also_known_as": ["Sons of Jacob", "The Twelve Tribes (ancestors of)"],
        "type": "group",
        "path": "mixed",
        "path_reason": "Committed grave sin (betrayal of a brother) but ultimately repented and were forgiven by both Yusuf and Allah",
        "era": "Time of Yusuf, Canaan and Egypt",
        "mentioned_in": [[12,7],[12,8],[12,9],[12,10],[12,11],[12,12],[12,13],[12,14],[12,15],[12,16],[12,17],[12,18],[12,58],[12,59],[12,60],[12,61],[12,62],[12,63],[12,64],[12,65],[12,66],[12,67],[12,68],[12,69],[12,70],[12,71],[12,72],[12,73],[12,74],[12,75],[12,76],[12,77],[12,78],[12,79],[12,80],[12,81],[12,82],[12,87],[12,91],[12,92],[12,97],[12,98]],
        "story_summary": "Eleven brothers who were jealous of Yusuf's special place in their father's heart. They threw him into a well and told their father a wolf ate him. Years later they came to Egypt in famine, not recognizing Yusuf as the minister. He recognized them. He tested them, revealed himself, and forgave them completely. They returned to Yaqub with his shirt — his sight was restored. The brothers' story is one of jealousy, sin, years of carrying guilt, and ultimate repentance and forgiveness.",
        "urdu_summary": "یوسف سے جلتے تھے، کنویں میں پھینکا، باپ کو بھیڑیے سے مرنے کی جھوٹی خبر دی۔ برسوں بعد قحط میں مصر آئے، یوسف کو نہ پہچانا۔ یوسف نے پہچانا، آزمایا، پھر معاف کیا۔ یعقوب کے پاس قمیص لے گئے — آنکھیں ٹھیک ہوئیں۔",
        "lessons": [
            "Jealousy leads to grave sin — the brothers' story is a warning",
            "Sin has consequences that last for years but can be forgiven",
            "The one you wronged may be the one who saves you",
            "Forgiveness is possible for the gravest betrayals"
        ],
        "connections": ["yusuf", "yaqub"],
        "tags": ["mixed", "jealousy", "betrayal", "repentance", "forgiveness"]
    },

    {
        "id": "shuayb",
        "name_arabic": "شُعَيْب",
        "name_english": "Shuayb (Jethro)",
        "name_urdu": "شعیب علیہ السلام",
        "also_known_as": ["Jethro", "Father-in-law of Musa"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Called his people to business ethics and justice; steadfast despite being threatened with stoning",
        "era": "Midian and Aykah, time overlapping with Musa",
        "mentioned_in": [[7,85],[7,86],[7,87],[7,88],[7,89],[7,90],[7,91],[7,92],[11,84],[11,85],[11,86],[11,87],[11,88],[11,89],[11,90],[11,91],[11,92],[11,93],[11,94],[11,95],[15,78],[22,44],[26,176],[26,177],[26,178],[26,179],[26,180],[26,181],[26,182],[26,183],[26,184],[26,185],[26,186],[26,187],[26,188],[26,189],[26,190],[29,36],[29,37]],
        "story_summary": "Sent to the people of Midian who cheated in weights and measures and robbed on the highways. He called them specifically to business ethics — give full measure, do not defraud. His people mocked him: 'Your prayer commands you that we should leave what our fathers worshipped or that we stop doing with our wealth what we want?' They threatened to stone him. He was rescued when the punishment of the earthquake took them. His daughter later became the wife of Musa.",
        "urdu_summary": "مدین کے لوگوں کی طرف بھیجے گئے جو ناپ تول میں کمی کرتے اور راستوں میں ڈکیتی کرتے تھے۔ کاروباری اخلاق کی دعوت دی۔ سنگسار کرنے کی دھمکی دی۔ زلزلے نے انہیں ہلاک کیا۔ ان کی بیٹی بعد میں موسیٰ کی بیوی بنیں۔",
        "lessons": [
            "Business ethics are a core part of Islam — not separate from religion",
            "Economic injustice is a spiritual problem",
            "Standing for justice in the marketplace is prophetic"
        ],
        "connections": ["musa", "people_of_midian"],
        "tags": ["prophet", "straight", "business-ethics", "justice", "midian"]
    },

    {
        "id": "musa",
        "name_arabic": "مُوسَى",
        "name_english": "Musa (Moses)",
        "name_urdu": "موسیٰ علیہ السلام",
        "also_known_as": ["Moses", "Kalimullah (The one Allah spoke to directly)", "Ulul Azm"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Kalimullah — Allah spoke to him directly; most mentioned prophet in Quran; led Bani Israel from slavery",
        "era": "Egypt, Sinai, approximately 1300 BCE",
        "mentioned_in": [[2,51],[2,53],[2,54],[2,55],[2,56],[2,60],[2,61],[2,67],[2,87],[2,92],[2,108],[3,84],[4,153],[4,164],[5,20],[5,21],[5,22],[5,23],[5,24],[5,25],[5,26],[6,84],[6,91],[6,154],[7,103],[7,104],[7,105],[7,106],[7,107],[7,108],[7,109],[7,110],[7,111],[7,112],[7,113],[7,114],[7,115],[7,116],[7,117],[7,118],[7,119],[7,120],[7,121],[7,122],[7,123],[7,127],[7,128],[7,129],[7,130],[7,131],[7,132],[7,133],[7,134],[7,135],[7,136],[7,137],[7,138],[7,139],[7,140],[7,141],[7,142],[7,143],[7,144],[7,145],[7,148],[7,150],[7,151],[7,152],[7,154],[7,155],[7,159],[7,160],[10,75],[10,76],[10,77],[10,78],[10,79],[10,80],[10,81],[10,82],[10,83],[10,84],[10,85],[10,86],[10,87],[10,88],[10,89],[10,90],[11,17],[11,96],[11,97],[11,110],[14,5],[14,6],[14,8],[17,2],[17,101],[17,102],[18,60],[18,65],[18,66],[18,67],[18,68],[18,69],[18,70],[18,71],[18,72],[18,73],[18,74],[18,75],[18,76],[18,77],[18,78],[18,79],[18,80],[18,81],[18,82],[19,51],[19,52],[19,53],[20,9],[20,10],[20,11],[20,12],[20,13],[20,14],[20,15],[20,16],[20,17],[20,18],[20,19],[20,20],[20,21],[20,22],[20,23],[20,24],[20,25],[20,26],[20,27],[20,28],[20,29],[20,30],[20,31],[20,32],[20,33],[20,34],[20,35],[20,36],[20,37],[20,38],[20,39],[20,40],[20,41],[20,42],[20,43],[20,44],[20,45],[20,46],[20,47],[20,48],[20,49],[20,50],[20,51],[20,52],[20,53],[20,54],[20,55],[20,56],[20,57],[20,58],[20,59],[20,60],[20,61],[20,62],[20,63],[20,64],[20,65],[20,66],[20,67],[20,68],[20,69],[20,70],[20,71],[20,72],[20,73],[20,77],[20,78],[20,80],[20,83],[20,84],[20,85],[20,86],[20,87],[20,88],[20,89],[20,90],[20,91],[20,92],[20,93],[20,94],[20,95],[20,96],[20,97],[21,48],[23,45],[23,49],[25,35],[26,10],[26,11],[26,12],[26,13],[26,14],[26,15],[26,16],[26,17],[26,18],[26,19],[26,20],[26,21],[26,22],[26,23],[26,24],[26,25],[26,26],[26,27],[26,28],[26,29],[26,30],[26,31],[26,32],[26,33],[26,34],[26,35],[26,36],[26,37],[26,38],[26,39],[26,40],[26,41],[26,42],[26,43],[26,44],[26,45],[26,46],[26,47],[26,48],[26,49],[26,50],[26,51],[26,52],[26,53],[26,54],[26,55],[26,56],[26,57],[26,58],[26,59],[26,60],[26,61],[26,62],[26,63],[26,64],[26,65],[26,66],[26,67],[26,68],[27,7],[27,8],[27,9],[27,10],[27,11],[27,12],[28,3],[28,4],[28,5],[28,6],[28,7],[28,8],[28,9],[28,10],[28,11],[28,12],[28,13],[28,14],[28,15],[28,16],[28,17],[28,18],[28,19],[28,20],[28,21],[28,22],[28,23],[28,24],[28,25],[28,26],[28,27],[28,28],[28,29],[28,30],[28,31],[28,32],[28,33],[28,34],[28,35],[28,36],[28,37],[28,38],[28,43],[28,44],[28,48],[28,76],[29,39],[32,23],[33,7],[33,69],[37,114],[37,115],[37,116],[37,117],[37,118],[37,119],[37,120],[37,121],[40,23],[40,24],[40,25],[40,26],[40,27],[40,28],[41,45],[42,13],[43,46],[43,47],[43,48],[43,49],[43,50],[43,51],[43,52],[43,53],[43,54],[43,55],[44,17],[44,18],[44,19],[44,20],[44,21],[44,22],[44,23],[44,24],[44,25],[44,26],[44,27],[44,28],[44,29],[44,30],[44,31],[46,12],[51,38],[53,36],[61,5],[79,15],[79,16],[79,17],[79,18],[79,19],[79,20]],
        "story_summary": "The most mentioned prophet in the Quran. Born in Egypt during Pharaoh's decree to kill all male Israelite babies. His mother placed him in a basket in the Nile — found by Pharaoh's household, raised in the palace. Grew up among Egyptians, killed a man accidentally while defending an Israelite, fled to Midian. Married Shuayb's daughter. Received prophethood at the burning bush — 'Take off your sandals; you are in the sacred valley.' Commanded to go to Pharaoh. Performed miracles (staff-serpent, white hand). The showdown with Pharaoh's magicians — the magicians believed. Nine plagues on Egypt. The Red Sea crossing — Pharaoh drowned. Received the Torah. His people worshipped the golden calf in his absence. Took his people on a forty-year wandering. Met Al-Khidr and learned about divine wisdom that transcends apparent justice. His story is the most comprehensive in the Quran — themes of justice, liberation, patience, faith, law, and the nature of divine wisdom.",
        "urdu_summary": "قرآن میں سب سے زیادہ ذکر والے نبی۔ فرعون کے حکم سے قتل سے بچائے گئے، دریا میں ٹوکری میں رکھے گئے، فرعون کے گھر میں پلے۔ ایک مصری کو مارا، بھاگے۔ جلتی جھاڑی پر نبوت ملی۔ فرعون کی طرف بھیجے گئے، معجزات دکھائے، جادوگر ایمان لائے۔ بحر قلزم پار کیا، فرعون ڈوبا۔ توراۃ ملی۔ بچھڑے کی پوجا، چالیس سال سرگردانی۔ خضر سے ملاقات۔",
        "lessons": [
            "A mother's ultimate tawakkul — placing her baby in the Nile by divine command",
            "Your enemy's household can become your protection — Allah's planning is beyond imagination",
            "A single moment of anger (killing the man) changed Musa's whole life trajectory",
            "Feeling inadequate for a task ('I am not eloquent') is not a barrier — Allah provides Harun",
            "Facing the greatest tyrant with only a staff — tawakkul in the face of impossible odds",
            "Even a prophet's people can fall into shirk the moment he turns his back",
            "The Khidr story: sometimes what appears as injustice contains mercy we cannot see"
        ],
        "connections": ["haroon", "firawn", "khidr", "bani_israel", "shuayb", "samiri"],
        "tags": ["prophet", "straight", "liberation", "law", "miracle", "patience", "most-mentioned"]
    },

    {
        "id": "haroon",
        "name_arabic": "هَارُون",
        "name_english": "Harun (Aaron)",
        "name_urdu": "ہارون علیہ السلام",
        "also_known_as": ["Aaron"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Prophet and brother/assistant of Musa; tried to stop the golden calf worship but was overwhelmed",
        "era": "Same as Musa, Egypt and Sinai",
        "mentioned_in": [[2,248],[4,163],[6,84],[7,122],[7,142],[7,150],[7,151],[10,75],[19,28],[19,53],[20,29],[20,30],[20,31],[20,32],[20,36],[20,42],[20,70],[20,90],[20,91],[20,92],[20,93],[20,94],[21,48],[23,45],[25,35],[26,13],[26,48],[28,34],[28,35],[37,114],[37,115],[37,116],[37,117],[37,118],[37,119],[37,120]],
        "story_summary": "Brother of Musa, given as a helper/prophet to assist in the mission to Pharaoh. When Musa went to receive the Torah, he left Harun in charge. During the forty days, the Samiri led the Israelites into golden calf worship. Harun tried to stop them but was nearly killed — he prioritized not causing division over maintaining order. When Musa returned furiously, he grabbed Harun by the head and beard. Harun explained he had tried but feared causing disunity. Musa prayed for both himself and Harun. Harun died before reaching the promised land.",
        "urdu_summary": "موسیٰ کے بھائی اور مددگار نبی۔ موسیٰ کی غیاب میں بچھڑے کی پوجا روکنے کی کوشش کی لیکن قتل کے خوف سے نہ ڈٹ سکے۔ موسیٰ نے ڈانٹا، انہوں نے صفائی دی۔ وعدہ کی سرزمین سے پہلے وفات پائی۔",
        "lessons": [
            "Even a prophet can be overwhelmed by a deviated crowd",
            "The tension between preventing evil and maintaining community unity",
            "Supporting a greater mission is itself a form of nobility",
            "Family prophetic pairs — Musa and Harun, a model of partnership"
        ],
        "connections": ["musa", "samiri", "bani_israel", "firawn"],
        "tags": ["prophet", "straight", "brotherhood", "support", "golden-calf"]
    },

    {
        "id": "firawn",
        "name_arabic": "فِرْعَوْن",
        "name_english": "Fir'awn (Pharaoh)",
        "name_urdu": "فرعون",
        "also_known_as": ["Pharaoh", "Ramesses II (by some historians)"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Claimed divinity ('I am your highest lord' 79:24), enslaved Bani Israel, killed male babies, rejected every sign, drowned — his deathbed declaration rejected (10:90-91)",
        "era": "Egypt, time of Musa",
        "mentioned_in": [[2,49],[2,50],[3,11],[7,103],[7,104],[7,105],[7,109],[7,110],[7,113],[7,123],[7,127],[7,128],[7,129],[7,130],[7,132],[7,133],[7,134],[7,135],[7,136],[7,137],[8,52],[8,54],[10,75],[10,76],[10,79],[10,83],[10,88],[10,90],[10,91],[10,92],[11,97],[11,98],[11,99],[14,6],[17,101],[17,102],[17,103],[20,24],[20,43],[20,44],[20,49],[20,56],[20,57],[20,58],[20,60],[20,71],[20,78],[20,79],[23,46],[23,47],[26,11],[26,16],[26,17],[26,18],[26,23],[26,29],[26,34],[26,41],[26,44],[26,45],[26,49],[26,53],[26,54],[26,55],[26,56],[26,57],[26,58],[26,59],[26,60],[26,61],[26,62],[26,63],[26,64],[26,65],[26,66],[27,12],[28,3],[28,4],[28,5],[28,6],[28,7],[28,8],[28,9],[28,32],[28,36],[28,37],[28,38],[28,39],[28,40],[28,41],[28,42],[29,39],[38,12],[40,24],[40,25],[40,26],[40,27],[40,28],[40,29],[40,36],[40,37],[40,45],[40,46],[43,46],[43,51],[43,53],[44,17],[44,31],[50,13],[51,38],[51,39],[51,40],[54,41],[54,42],[66,11],[69,9],[73,15],[73,16],[79,17],[79,18],[79,19],[79,20],[79,21],[79,22],[79,23],[79,24],[79,25],[85,18],[89,10]],
        "story_summary": "The ultimate symbol of tyranny in the Quran. Claimed to be the highest lord ('Ana rabbukumul ala' 79:24). Enslaved and oppressed Bani Israel. Ordered the killing of all male Israelite babies. Rejected every sign brought by Musa. Called the magicians to defeat Musa — when the magicians believed, he had them crucified. Pursued Musa and Bani Israel to the Red Sea. As he was drowning, he declared: 'I believe that there is no god but the One the Children of Israel believe in.' Allah rejected his deathbed declaration — 'Now? When before you disobeyed.' His body was preserved as a sign for those who come after (10:92). The Quran describes him as 'a sign for those who come after him' — preserved as a lesson.",
        "urdu_summary": "قرآن میں ظلم کی سب سے بڑی علامت۔ 'انا ربکم الاعلیٰ' (79:24)۔ بنی اسرائیل کو غلام بنایا، لڑکوں کو قتل کرواتا رہا۔ موسیٰ کا ہر معجزہ جھٹلایا۔ جادوگروں کو مومن ہونے پر سولی دی۔ ڈوبتے وقت ایمان لایا — اللہ نے کہا: 'اب؟ پہلے کیوں نہ ایمان لائے؟' لاش محفوظ کی گئی نشانی کے طور پر (10:92)۔",
        "lessons": [
            "The most powerful human who ever rejected Allah — and his complete end",
            "Deathbed repentance is not accepted when it is forced by seeing punishment",
            "Allah preserves some bodies as signs — Fir'awn's mummified body is a lesson",
            "Power and wealth are not signs of Allah's approval",
            "The system of Fir'awn (claiming divine authority over people) is a recurring danger"
        ],
        "connections": ["musa", "haroon", "haman", "qarun", "wife_of_firawn", "bani_israel"],
        "tags": ["deviated", "tyrant", "arrogance", "shirk", "power", "egypt"]
    },

    {
        "id": "wife_of_firawn",
        "name_arabic": "امرأة فرعون",
        "name_english": "Wife of Fir'awn (Asiya)",
        "name_urdu": "آسیہ — فرعون کی بیوی",
        "also_known_as": ["Asiya bint Muzahim", "One of the four greatest women in Islam"],
        "type": "person",
        "path": "straight",
        "path_reason": "Believed in Allah while married to the greatest tyrant; her prayer in Quran (66:11) is one of the greatest recorded prayers; counted among the best women of all time",
        "era": "Time of Musa, Egypt",
        "mentioned_in": [[28,9],[66,11]],
        "story_summary": "Wife of Fir'awn who is the counterpart to the wives of Nuh and Lut — while those two were married to prophets yet deviated, Asiya was married to the worst tyrant yet maintained faith. She was the one who found baby Musa in the basket and pleaded with Fir'awn to spare him. When Fir'awn discovered her faith, he tortured her. Her prayer recorded in the Quran (66:11): 'My Lord, build for me near You a house in Paradise and save me from Fir'awn and his deeds, and save me from the wrongdoing people.' She died under torture, smiling — because at the moment of her death, Jannah was shown to her. The Prophet ﷺ named her as one of the four greatest women who ever lived.",
        "urdu_summary": "فرعون کی بیوی جو مسلمان تھیں — نوح اور لوط کی بیویوں کے برعکس جو نبیوں کی بیویاں ہوتے ہوئے کافر رہیں۔ موسیٰ کو ٹوکری میں دیکھا، بچانے کی درخواست کی۔ ایمان ظاہر ہوا تو فرعون نے عذاب دیا۔ دعا (66:11): 'اے میرے رب! اپنے پاس جنت میں گھر بنا' — جنت دیکھتے ہوئے مسکرا کر وفات پائیں۔",
        "lessons": [
            "The most extreme example that environment does not determine faith",
            "Married to the worst tyrant — yet among the best humans who ever lived",
            "Her prayer (66:11) is a model for anyone trapped in an oppressive environment",
            "Jannah shown at the moment of death as the ultimate comfort",
            "The prophet cited her as one of four greatest women — dignity in oppression"
        ],
        "connections": ["firawn", "musa"],
        "tags": ["straight", "faith", "oppression", "sabr", "woman", "greatest-women", "jannah"]
    },

    {
        "id": "haman",
        "name_arabic": "هَامَان",
        "name_english": "Haman",
        "name_urdu": "ہامان",
        "also_known_as": [],
        "type": "person",
        "path": "deviated",
        "path_reason": "Chief minister and architect of Fir'awn's tyranny; built the tower to 'reach Allah' in mockery; destroyed with Fir'awn (28:8)",
        "era": "Time of Musa, Egypt",
        "mentioned_in": [[28,6],[28,8],[28,38],[29,39],[40,24],[40,36],[40,37]],
        "story_summary": "Fir'awn's chief minister and close ally in oppression. Fir'awn commanded him to build a tower so high they could 'reach Moses's God' — a mockery of divine transcendence. He was the architect of a system of oppression. He and Fir'awn and Qarun are cited together as a trio of those who were destroyed (29:39). His role represents those who enable and implement tyrants — not the tyrant themselves, but their architects of oppression.",
        "urdu_summary": "فرعون کا وزیر جس نے ظلم کا نظام بنایا۔ فرعون کے حکم پر اونچا مینار بنانے لگا تاکہ 'موسیٰ کے رب تک پہنچیں'۔ فرعون اور قارون کے ساتھ ہلاک ہوا (29:39)۔",
        "lessons": [
            "Enablers of tyranny share the tyrant's sin and fate",
            "Those who build systems of oppression are as guilty as those who command it",
            "Mockery of Allah's transcendence — building towers to 'reach God'"
        ],
        "connections": ["firawn", "qarun", "musa"],
        "tags": ["deviated", "tyrant", "oppression", "enabler"]
    },

    {
        "id": "qarun",
        "name_arabic": "قَارُون",
        "name_english": "Qarun (Korah)",
        "name_urdu": "قارون",
        "also_known_as": ["Korah"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Given immense wealth but attributed it to his own knowledge/merit; rejected advice; swallowed with his treasures into the earth (28:81)",
        "era": "Time of Musa, among Bani Israel",
        "mentioned_in": [[28,76],[28,77],[28,78],[28,79],[28,80],[28,81],[28,82],[29,39],[40,24]],
        "story_summary": "A man from Bani Israel who was given such enormous wealth that the keys to his treasures required a group of strong men to carry. He paraded before his people in his finery, causing some to wish they had what he had. The righteous advised him to seek the next world and not forget his share in this one, and to do good as Allah had done good to him. He replied: 'I have been given this because of knowledge I have.' He was swallowed into the earth along with his treasures. Those who had envied him said, 'It is Allah who extends provision to whom He wills... had Allah not favored us, He would have caused it to swallow us too.'",
        "urdu_summary": "بنی اسرائیل میں سے ایک شخص جسے اتنی دولت دی گئی کہ خزانوں کی چابیاں اٹھانے کے لیے قوی آدمیوں کی جماعت چاہیے تھی۔ کہا: 'یہ میرے اپنے علم کی وجہ سے ملا ہے'۔ زمین میں دھنس گیا اپنے خزانوں سمیت (28:81)۔",
        "lessons": [
            "Attributing blessings to your own merit/intelligence rather than Allah",
            "Wealth is a test — the wealthier the test, the greater the responsibility",
            "The envy of onlookers converted to gratitude the moment Qarun was destroyed",
            "The earth can swallow everything — no wealth is truly secure",
            "Advice given by the righteous: 'seek the next world but do not forget your share in this'"
        ],
        "connections": ["musa", "firawn", "haman", "bani_israel"],
        "tags": ["deviated", "wealth", "arrogance", "gratitude", "destroyed"]
    },

    {
        "id": "samiri",
        "name_arabic": "السَّامِرِيّ",
        "name_english": "Al-Samiri",
        "name_urdu": "سامری",
        "also_known_as": [],
        "type": "person",
        "path": "deviated",
        "path_reason": "Seduced Bani Israel into worshipping the golden calf; crafted a lie about taking dust from the messenger's footstep; condemned to isolation (20:96-97)",
        "era": "Time of Musa, Sinai",
        "mentioned_in": [[20,85],[20,87],[20,88],[20,95],[20,96],[20,97]],
        "story_summary": "A man among Bani Israel who, during Musa's absence to receive the Torah, collected the people's gold jewelry and melted it into a calf that made a lowing sound. He claimed he had taken a handful of dust from the footprint of the messenger (Jibreel) and cast it into the calf, giving it a special power. Musa returned furiously, challenged Samiri directly. Samiri's explanation: 'I saw what they did not see.' He was condemned by Musa to spend his life alone, saying 'touch me not' — and he would wander declaring 'no touch' for the rest of his life. His calf would be burned and scattered into the sea.",
        "urdu_summary": "بنی اسرائیل میں سے شخص جس نے غیاب موسیٰ میں سونے کا بچھڑا بنایا۔ کہا: 'فرشتے کے قدموں سے مٹی لی تھی'۔ موسیٰ نے سزا دی: باقی زندگی اکیلا رہے گا، کہے گا 'مجھے مت چھونا'۔ بچھڑا جلا کر سمندر میں بہا دیا گیا۔",
        "lessons": [
            "A single bad actor with a persuasive lie can lead an entire community astray",
            "The golden calf — material attraction dressed as spirituality",
            "A specific, crafted lie ('I took dust from the messenger's footstep') — deception always needs a story",
            "Social isolation as punishment — the opposite of community"
        ],
        "connections": ["musa", "haroon", "bani_israel"],
        "tags": ["deviated", "golden-calf", "deception", "fitna", "isolation"]
    },

    {
        "id": "khidr",
        "name_arabic": "الْخَضِر",
        "name_english": "Al-Khidr",
        "name_urdu": "خضر علیہ السلام",
        "also_known_as": ["Al-Khadir", "The Green One"],
        "type": "person",
        "path": "straight",
        "path_reason": "A servant of Allah given special knowledge and mercy; acted on divine wisdom that transcended apparent justice",
        "era": "Time of Musa (and possibly beyond — debates exist)",
        "mentioned_in": [[18,65],[18,66],[18,67],[18,68],[18,69],[18,70],[18,71],[18,72],[18,73],[18,74],[18,75],[18,76],[18,77],[18,78],[18,79],[18,80],[18,81],[18,82]],
        "story_summary": "Described as a servant of Allah 'upon whom We had bestowed mercy from Ourselves and had taught him knowledge from Ourselves' (18:65). Musa sought him out to learn. He agreed to accompany Musa on condition that Musa not question his actions. Three events followed: he scuttled a boat (to save it from a king who seized ships), killed a boy (whose parents were believers and who would have led them to disbelief), and rebuilt a wall in a town that refused them hospitality (to protect hidden treasure for two orphan boys). Each action appeared wrong on the surface; each had a divine mercy beneath. His story is the Quran's deepest teaching on the nature of divine wisdom and the limits of human judgment.",
        "urdu_summary": "اللہ کا خاص بندہ جسے خاص علم اور رحمت دی گئی (18:65)۔ موسیٰ نے سیکھنے کے لیے تلاش کیا۔ کشتی میں سوراخ کیا (ظالم بادشاہ سے بچانے)، لڑکے کو قتل کیا (مومن ماں باپ کو گمراہی سے بچانے)، دیوار بنائی (یتیموں کا خزانہ بچانے)۔ ہر عمل بظاہر غلط، باطناً رحمت۔",
        "lessons": [
            "Some divine wisdom operates at a level beyond human perception",
            "What appears as harm may be mercy — what appears as loss may be protection",
            "The most learned person (Musa) needed to learn from someone else",
            "Patience in learning requires suspending judgment",
            "Allah's mercy reaches people through means they cannot see or control"
        ],
        "connections": ["musa"],
        "tags": ["straight", "wisdom", "divine-knowledge", "apparent-vs-real", "mercy"]
    },

    {
        "id": "dawud",
        "name_arabic": "دَاوُود",
        "name_english": "Dawud (David)",
        "name_urdu": "داؤد علیہ السلام",
        "also_known_as": ["David", "Khalifah of the earth (38:26)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Prophet and king; erred once but repented immediately and deeply; Allah forgave and praised him (38:25)",
        "era": "Ancient Palestine, approximately 1000 BCE",
        "mentioned_in": [[2,251],[4,163],[5,78],[6,84],[17,55],[21,78],[21,79],[21,80],[27,15],[27,16],[34,10],[34,11],[34,13],[38,17],[38,18],[38,19],[38,20],[38,21],[38,22],[38,23],[38,24],[38,25],[38,26]],
        "story_summary": "Prophet and king of Israel. Killed the giant Jalut (Goliath) as a young man. Taught the language of birds and was given wisdom and sound judgment. Allah softened iron for him so he could make armor. The mountains and birds joined him in glorifying Allah. He was given the Zabur (Psalms). He erred in a matter of judgment regarding a woman (married her after her husband was sent to battle) — when two angels came in the form of litigants and he gave an unjust verdict, he realized the parable was about himself, fell prostrate, and wept. Allah forgave him and made him a khalifah on earth, warning him not to follow desire.",
        "urdu_summary": "نبی اور بادشاہ۔ جالوت کو قتل کیا۔ پرندوں اور پہاڑوں کی تسبیح ساتھ ہوتی۔ زبور دی گئی۔ ایک معاملے میں غلطی کی، فوراً سجدے میں گر کر روئے، اللہ نے معاف کر کے زمین پر خلیفہ بنایا اور خواہش کی پیروی سے بچنے کا حکم دیا (38:26)۔",
        "lessons": [
            "A prophet-king can err — but the mark of greatness is immediate, genuine repentance",
            "Power and desire are the greatest tests of the powerful",
            "Khalifah on earth — with the warning about following hawa (desire)",
            "The Psalms — worship through beautiful voice is a divine gift",
            "Creation joins in tasbih — everything has its own glorification"
        ],
        "connections": ["sulayman", "jalut"],
        "tags": ["prophet", "straight", "king", "repentance", "psalms", "wisdom"]
    },

    {
        "id": "sulayman",
        "name_arabic": "سُلَيْمَان",
        "name_english": "Sulayman (Solomon)",
        "name_urdu": "سلیمان علیہ السلام",
        "also_known_as": ["Solomon"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Prophet-king given unrivalled dominion; maintained gratitude and sought forgiveness even at the height of power",
        "era": "Ancient Palestine, approximately 950 BCE",
        "mentioned_in": [[2,102],[4,163],[6,84],[21,78],[21,79],[21,81],[21,82],[27,15],[27,16],[27,17],[27,18],[27,19],[27,20],[27,21],[27,22],[27,23],[27,24],[27,25],[27,26],[27,27],[27,28],[27,29],[27,30],[27,31],[27,32],[27,33],[27,34],[27,35],[27,36],[27,37],[27,38],[27,39],[27,40],[27,41],[27,42],[27,43],[27,44],[27,44],[34,12],[34,13],[34,14],[34,15],[34,16],[38,30],[38,31],[38,32],[38,33],[38,34],[38,35],[38,36],[38,37],[38,38],[38,39],[38,40]],
        "story_summary": "Son of Dawud, given an unrivalled kingdom (38:35) — command over wind, jinn, birds, and human armies. Could understand the language of all creatures. The ant's speech (27:18-19) — he heard the ant warning others and smiled in gratitude, making dua to do righteous deeds pleasing to Allah. Communicated with the Hudhud (hoopoe bird) about Bilqis, Queen of Sheba. Her throne was transported from Yemen to Palestine by a jinn before she arrived. The Quran corrects the biblical account — Sulayman did not practice magic; those who claimed he did were liars (2:102). He tested himself when his kingdom was shaken and prayed for forgiveness and an unrivalled kingdom — it was granted.",
        "urdu_summary": "داؤد کے بیٹے، بے مثال سلطنت دی گئی (38:35)۔ ہوا، جنات، پرندوں اور انسانوں کی فوج پر اختیار۔ چیونٹی کی بات سن کر مسکرائے اور شکر کی دعا مانگی۔ ملکہ بلقیس کا تخت لمحوں میں منگوایا۔ قرآن نے تصیح کی: سلیمان جادوگر نہیں تھے (2:102)۔",
        "lessons": [
            "The greatest power still needs humility — Sulayman smiled at the ant",
            "True gratitude at the height of blessing",
            "Asking Allah for an unrivalled gift and being granted it — the boldness of dua",
            "Jinn can work — and those who misattributed magic to Sulayman were the disbelievers",
            "The power to understand all creatures — listening to the smallest"
        ],
        "connections": ["dawud", "bilqis", "jinn_of_sulayman"],
        "tags": ["prophet", "straight", "king", "wisdom", "gratitude", "jinn", "power"]
    },

    {
        "id": "bilqis",
        "name_arabic": "بِلْقِيس",
        "name_english": "Bilqis (Queen of Sheba)",
        "name_urdu": "بلقیس — ملکہ سبا",
        "also_known_as": ["Queen of Sheba", "Malakat Saba"],
        "type": "person",
        "path": "straight",
        "path_reason": "Moved from sun-worship to Islam upon seeing the truth; her submission was sincere and public (27:44)",
        "era": "Time of Sulayman, ancient Yemen",
        "mentioned_in": [[27,22],[27,23],[27,24],[27,25],[27,26],[27,27],[27,29],[27,31],[27,32],[27,33],[27,34],[27,35],[27,36],[27,37],[27,38],[27,39],[27,40],[27,41],[27,42],[27,43],[27,44]],
        "story_summary": "Queen of Yemen (Sheba) and her people worshipped the sun. The Hudhud reported her kingdom to Sulayman. He sent a letter: 'It is from Sulayman, and it is in the name of Allah, the Most Gracious, the Most Merciful — do not be arrogant with me and come to me in submission.' She consulted her council, tested Sulayman with gifts (he refused), then came herself. Her throne was transported to Sulayman before she arrived. When she saw it, she recognized divine power. She was then brought into a palace of glass — thinking it was water, she lifted her dress; Sulayman revealed it was smooth glass. She said: 'My Lord, indeed I have wronged myself, and I submit with Sulayman to Allah, Lord of the worlds' (27:44). A queen chose Islam.",
        "urdu_summary": "یمن کی ملکہ جو سورج کی پوجا کرتی تھیں۔ سلیمان کا خط آیا۔ سفارت کاری سے کام لیا۔ خود آئیں۔ محل کے شیشے کے فرش کو پانی سمجھ کر دامن اٹھایا۔ سلیمان نے بتایا — حقیقت کا ادراک ہوا۔ فوراً کہا: 'اے رب! میں نے اپنے آپ پر ظلم کیا، اللہ کے آگے سر تسلیم خم کرتی ہوں' (27:44)۔",
        "lessons": [
            "A leader who listens to advice and consults — Bilqis modeled shura",
            "Testing with material gifts vs responding to divine truth",
            "The moment of clarity — the glass palace was the mirror of reality",
            "A queen's humble admission: 'I have wronged myself'",
            "Submission to truth regardless of what you would lose in status"
        ],
        "connections": ["sulayman"],
        "tags": ["straight", "islam", "queen", "wisdom", "submission", "humility"]
    },

    {
        "id": "ayyub",
        "name_arabic": "أَيُّوب",
        "name_english": "Ayyub (Job)",
        "name_urdu": "ایوب علیہ السلام",
        "also_known_as": ["Job", "Symbol of Sabr"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Lost everything — health, wealth, family — yet maintained trust in Allah; his dua (21:83) is considered the master dua of distress",
        "era": "Ancient Levant region",
        "mentioned_in": [[4,163],[6,84],[21,83],[21,84],[38,41],[38,42],[38,43],[38,44]],
        "story_summary": "A prophet who was afflicted with severe illness and loss for years. He called upon his Lord: 'Harm has touched me, and You are the Most Merciful of the merciful' (21:83). He did not complain to people, did not curse his fate, did not lose faith. Allah responded: 'So We responded to him and removed what afflicted him of adversity. And We restored his family and the like thereof with them as mercy from Us.' He is the Quranic archetype of patience in affliction — not passive silence, but active, trusting petition to Allah. Surah Sad mentions he struck the ground with his foot and a cool water spring appeared for him to bathe and drink.",
        "urdu_summary": "نبی جن پر شدید بیماری اور تکلیف برسوں رہی۔ دعا کی: 'مجھے تکلیف پہنچی ہے اور تو سب سے بڑا رحم کرنے والا ہے' (21:83)۔ شکوہ نہ کیا، ایمان نہ چھوڑا۔ اللہ نے سب کچھ دو گنا واپس کیا۔ زمین پر پاؤں مارا — ٹھنڈا پانی نکلا۔",
        "lessons": [
            "The dua of Ayyub (21:83) is the model dua for any hardship",
            "Patience is not silence — it is active trust expressed in dua",
            "Loss can precede the greatest restoration",
            "The duration of suffering does not indicate divine abandonment",
            "After the deepest valley comes the highest peak — Allah restored everything doubled"
        ],
        "connections": [],
        "tags": ["prophet", "straight", "sabr", "illness", "dua", "restoration", "patience"]
    },

    {
        "id": "yunus",
        "name_arabic": "يُونُس",
        "name_english": "Yunus (Jonah)",
        "name_urdu": "یونس علیہ السلام",
        "also_known_as": ["Jonah", "Dhul-Nun (Companion of the Whale)", "Sahib al-Hut"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Left his people without permission; was swallowed by a whale; his dua in the darkness is the most powerful recorded; his people were saved — the only people who returned to faith after seeing punishment",
        "era": "Ancient Nineveh (modern Iraq area)",
        "mentioned_in": [[4,163],[6,86],[10,98],[21,87],[21,88],[37,139],[37,140],[37,141],[37,142],[37,143],[37,144],[37,145],[37,146],[37,147],[37,148],[68,48],[68,49],[68,50]],
        "story_summary": "Sent to the people of Nineveh. Left them in frustration before receiving permission to go. Boarded a ship; a storm came; lots were cast and he was thrown overboard; swallowed by a whale. In the depths of the sea, in the darkness of the whale's belly, he called: 'There is no god but You, exalted are You; indeed I have been of the wrongdoers' (21:87) — the Tasbih of Yunus. Allah responded; the whale cast him out onto the bank. He was in a state of illness. A plant grew over him. Then he was sent back to his 100,000+ people — and this time they believed. They are the only community in history to have believed after seeing the signs of punishment coming, and their faith was accepted.",
        "urdu_summary": "اہل نینوا کی طرف بھیجے گئے۔ اجازت کے بغیر چلے گئے۔ کشتی میں سوار ہوئے، طوفان آیا، سمندر میں پھینکے گئے، مچھلی نے نگل لیا۔ اندھیرے میں دعا: 'لا الٰہ الا انت سبحانک انی کنت من الظالمین' (21:87)۔ اللہ نے قبول کیا، مچھلی نے ساحل پر اگل دیا۔ دوبارہ قوم کی طرف گئے — ایک لاکھ سے زیادہ ایمان لائے۔",
        "lessons": [
            "The Tasbih of Yunus (21:87) — the dua for any darkness",
            "Leaving without permission has consequences, even for prophets",
            "No darkness is so deep that Allah cannot hear you",
            "The only community saved by belief after seeing punishment — timing of repentance matters",
            "Allah's mercy: illness, shade, food — gentle restoration after trauma"
        ],
        "connections": ["people_of_yunus"],
        "tags": ["prophet", "straight", "whale", "dua", "darkness", "repentance", "sabr"]
    },

    {
        "id": "ilyas",
        "name_arabic": "إِلْيَاس",
        "name_english": "Ilyas (Elijah)",
        "name_urdu": "الیاس علیہ السلام",
        "also_known_as": ["Elijah"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Steadfast prophet who called his people away from idol worship (Ba'l); praised as 'of the excellent' (37:130)",
        "era": "Ancient Levant",
        "mentioned_in": [[6,85],[37,123],[37,124],[37,125],[37,126],[37,127],[37,128],[37,129],[37,130]],
        "story_summary": "Sent to a people who worshipped the idol Ba'l. He called them to abandon it and worship Allah. His people rejected him. He was praised by Allah: 'Peace be upon Ilyas' (37:130) and counted among the excellent servants. His story is brief in the Quran but establishes the continuity of prophetic mission against idol worship.",
        "urdu_summary": "بال بت کی پوجا کرنے والی قوم کی طرف بھیجے گئے۔ دعوت دی، قوم نے نہ مانا۔ اللہ نے فرمایا: 'سلام ہو الیاس پر' (37:130)۔",
        "lessons": ["Continuity of prophetic mission against idol worship"],
        "connections": [],
        "tags": ["prophet", "straight", "idol-worship", "dawah"]
    },

    {
        "id": "alyasa",
        "name_arabic": "الْيَسَع",
        "name_english": "Al-Yasa' (Elisha)",
        "name_urdu": "یسع علیہ السلام",
        "also_known_as": ["Elisha"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Named among the best servants; praised alongside Ismail, Dhul-Kifl (38:48)",
        "era": "Ancient Levant, successor of Ilyas",
        "mentioned_in": [[6,86],[38,48]],
        "story_summary": "Mentioned twice in the Quran, placed among the excellent prophets. He is understood to be the successor of Ilyas (Elijah). Brief mention but honored placement.",
        "urdu_summary": "قرآن میں دو بار ذکر، بہترین انبیاء میں شمار۔",
        "lessons": ["Every prophet, however briefly mentioned, carries divine honor"],
        "connections": ["ilyas"],
        "tags": ["prophet", "straight"]
    },

    {
        "id": "dhul_kifl",
        "name_arabic": "ذُو الْكِفْل",
        "name_english": "Dhul-Kifl",
        "name_urdu": "ذوالکفل علیہ السلام",
        "also_known_as": ["Possibly Ezekiel or Elijah (scholarly debate)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Praised as patient and among the righteous (21:85-86)",
        "era": "Ancient Levant",
        "mentioned_in": [[21,85],[21,86],[38,48]],
        "story_summary": "Mentioned alongside Ismail and Idris as patient and righteous. His identity is debated — some say he is Ezekiel, others suggest another prophet. His name means 'one who has a pledge/double reward.' Very brief mention in the Quran but honored.",
        "urdu_summary": "اسماعیل اور ادریس کے ساتھ ذکر، صابر اور نیک۔",
        "lessons": ["Patience and righteousness are the defining characteristics even of the lesser-known"],
        "connections": [],
        "tags": ["prophet", "straight", "patience"]
    },

    {
        "id": "idris",
        "name_arabic": "إِدْرِيس",
        "name_english": "Idris (Enoch)",
        "name_urdu": "ادریس علیہ السلام",
        "also_known_as": ["Enoch", "Raised to a high station"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Prophet of patience and truthfulness; raised by Allah to a high station (19:57)",
        "era": "Very early human history, before Nuh by some accounts",
        "mentioned_in": [[19,56],[19,57],[21,85],[21,86]],
        "story_summary": "Mentioned as a prophet, a truthful one, and one raised to a high station (rafa'nahu makanan aliyyan). He is believed to have been raised (physically) to a high place by Allah. He is among the earliest prophets and is praised for patience.",
        "urdu_summary": "نبی، صدیق، اونچے مقام پر اٹھائے گئے (19:57)۔",
        "lessons": ["Truthfulness (sidq) and patience are the foundation of prophetic character"],
        "connections": ["nuh"],
        "tags": ["prophet", "straight", "raised", "patience", "truthfulness"]
    },

    {
        "id": "isa",
        "name_arabic": "عِيسَى",
        "name_english": "Isa (Jesus)",
        "name_urdu": "عیسیٰ علیہ السلام",
        "also_known_as": ["Jesus", "Al-Masih (The Messiah)", "Kalimullah (Word of Allah)", "Ruhullah (Spirit of Allah)", "Ibn Maryam (Son of Mary)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Mighty messenger; born of miracle; performed miracles by Allah's permission; was raised to Allah; will return before the Day of Judgment",
        "era": "Roman-era Palestine, approximately 1-33 CE",
        "mentioned_in": [[2,87],[2,136],[2,253],[3,45],[3,46],[3,47],[3,48],[3,49],[3,50],[3,51],[3,52],[3,53],[3,54],[3,55],[3,59],[3,84],[4,157],[4,158],[4,163],[4,171],[4,172],[5,17],[5,46],[5,72],[5,73],[5,75],[5,78],[5,110],[5,111],[5,112],[5,113],[5,114],[5,115],[5,116],[5,117],[5,118],[6,85],[9,30],[9,31],[19,19],[19,20],[19,21],[19,22],[19,27],[19,29],[19,30],[19,31],[19,32],[19,33],[19,34],[19,36],[21,91],[23,50],[33,7],[42,13],[43,57],[43,58],[43,59],[43,61],[43,63],[43,64],[57,27],[61,6],[61,14]],
        "story_summary": "Born without a father to Maryam bint Imran — a miracle. Spoke in the cradle (19:29-33). Given miracles: made birds from clay that flew, healed the blind and leper, raised the dead — all by Allah's permission. Given the Injeel. Called Bani Israel to return to true monotheism. The disciples (Hawariyyun) believed in him. The Quran corrects critical misconceptions: Isa was not crucified — 'They did not kill him nor did they crucify him, but so it was made to appear to them' (4:157). He was raised to Allah (4:158). He is not divine — 'He is only a messenger' (5:75). He himself disavowed worship of him (5:116). He is expected to return before the Day of Judgment. Predicted the coming of Ahmad (Muhammad ﷺ) (61:6).",
        "urdu_summary": "بغیر باپ کے مریم سے پیدا ہوئے — معجزہ۔ گود میں بولے (19:29-33)۔ اللہ کی اجازت سے اندھوں کو بینائی، کوڑھیوں کو شفا، مردوں کو زندگی دی۔ انجیل دی گئی۔ صلیب نہیں دی گئی — اللہ نے اٹھا لیا (4:157-158)۔ الٰہ نہیں — نبی ہیں (5:75)۔ احمد ﷺ کی بشارت دی (61:6)۔ قیامت سے پہلے واپس آئیں گے۔",
        "lessons": [
            "Miraculous birth as a sign — creation without a father shows Allah creates how He wills",
            "The Quran corrects the crucifixion narrative",
            "Isa himself disavowed being worshipped — his testimony against shirk",
            "Predicting Muhammad ﷺ — the continuity of prophetic mission",
            "The return of Isa — a major sign before the Day of Judgment",
            "Being called 'Kalimullah' and 'Ruhullah' — special status without divinity"
        ],
        "connections": ["maryam", "yahya", "hawariyyun", "ibrahim", "musa"],
        "tags": ["prophet", "straight", "miracle", "messiah", "born-without-father", "raised", "return"]
    },

    {
        "id": "maryam",
        "name_arabic": "مَرْيَم",
        "name_english": "Maryam (Mary)",
        "name_urdu": "مریم علیہا السلام",
        "also_known_as": ["Mary", "The only woman with a Surah named after her", "Siddiqah (the truthful)"],
        "type": "person",
        "path": "straight",
        "path_reason": "Chosen above all women of all worlds (3:42); guarded her chastity; believed in the words of Allah; counted among the Qanitin (devoutly obedient) (66:12)",
        "era": "Roman-era Palestine",
        "mentioned_in": [[2,87],[3,36],[3,37],[3,42],[3,43],[3,44],[3,45],[3,47],[4,156],[4,157],[4,171],[5,17],[5,75],[5,110],[5,116],[19,16],[19,17],[19,18],[19,19],[19,20],[19,21],[19,22],[19,23],[19,24],[19,25],[19,26],[19,27],[19,28],[19,29],[21,91],[23,50],[66,12]],
        "story_summary": "Born to Imran and Hannah, dedicated to the temple before birth. Cared for by Zakariyya. Received provision miraculously in her chamber. Chosen by Allah above all women. The angel Jibreel appeared to her in human form — she sought refuge in Allah from him. He told her of Isa. She said 'How can I have a child when no man has touched me?' He said: 'Such is Allah — He creates what He wills.' She retreated to give birth alone. Shook a palm tree for fresh dates during labor. Held the baby who spoke in the cradle when she returned. The Quran honors her with an entire surah (Maryam) — the only woman with a surah named after her. She is described as a 'siddiqah' (completely truthful) in 5:75.",
        "urdu_summary": "عمران اور حنہ کی بیٹی، پیدائش سے پہلے ہی نذر کی گئیں۔ زکریا کی نگرانی میں رہیں۔ غیبی رزق ملتا رہا۔ تمام دنیا کی عورتوں پر چن لی گئیں (3:42)۔ فرشتہ آیا، عیسیٰ کی خبر دی۔ تنہا بچہ جنا۔ لوگوں نے الزام لگایا — بچے نے گود میں بول کر سب کیا۔ قرآن کی واحد خاتون جن کے نام پر سورت ہے۔",
        "lessons": [
            "Chosen above all women — the honor of submission and chastity",
            "Her dua when labor began: 'I wish I had died before this' — even the righteous can be overwhelmed",
            "The dates during labor — Allah provides in the most unexpected ways",
            "Her silence strategy: 'I have vowed a fast of silence' — not defending against slander",
            "The baby speaking in the cradle answered all accusations",
            "One of four greatest women ever — Asiya, Khadijah, Fatimah, Maryam"
        ],
        "connections": ["isa", "zakariyya", "imran", "hannah"],
        "tags": ["straight", "chastity", "miracle", "chosen", "mother", "greatest-women", "siddiqah"]
    },

    {
        "id": "zakariyya",
        "name_arabic": "زَكَرِيَّا",
        "name_english": "Zakariyya (Zechariah)",
        "name_urdu": "زکریا علیہ السلام",
        "also_known_as": ["Zechariah"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Prophet who prayed for an heir in old age with full certainty of Allah's power; dua answered with Yahya",
        "era": "Roman-era Palestine, guardian of Maryam",
        "mentioned_in": [[3,37],[3,38],[3,39],[3,40],[3,41],[6,85],[19,2],[19,3],[19,4],[19,5],[19,6],[19,7],[19,8],[19,9],[19,10],[19,11],[21,89],[21,90]],
        "story_summary": "Prophet and guardian of Maryam in the temple. When he saw miraculous provision appearing for her, he was inspired to ask Allah for an heir despite his old age and barren wife. His private dua (19:3-6): 'My Lord, indeed my bones have weakened, and my head has filled with white hair, and never have I been in my supplication to You, my Lord, unhappy... so grant me from Yourself an heir.' The angel gave him the news of Yahya. He asked for a sign — he was made mute for three days/nights as the sign. He kept worshipping in gratitude.",
        "urdu_summary": "مریم کے کفیل نبی۔ مریم کا غیبی رزق دیکھا تو ولی کی دعا مانگی۔ بڑھاپے اور بانجھ بیوی کے باوجود امید نہ چھوڑی۔ رات کو چپکے سے دعا کی (19:3-6)۔ یحییٰ کی خبر ملی۔ نشانی مانگی — تین دن/رات گونگے ہو گئے۔",
        "lessons": [
            "Asking the impossible from the One to Whom nothing is impossible",
            "Praying in private, by night — the sincerest dua",
            "Never losing hope despite old age, barren wife, and apparent impossibility",
            "Signs of faith: asking for a sign not from doubt but from wanting to increase in certainty",
            "Witnessing a miracle (Maryam's food) often unlocks the courage to ask for your own miracle"
        ],
        "connections": ["yahya", "maryam", "isa"],
        "tags": ["prophet", "straight", "dua", "miracle", "heir", "hope", "old-age"]
    },

    {
        "id": "yahya",
        "name_arabic": "يَحْيَى",
        "name_english": "Yahya (John the Baptist)",
        "name_urdu": "یحییٰ علیہ السلام",
        "also_known_as": ["John the Baptist"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Given wisdom from childhood; unique in being named by Allah before birth; described as chaste, kind to parents, not arrogant (19:12-15)",
        "era": "Roman-era Palestine, contemporary with Isa",
        "mentioned_in": [[3,39],[6,85],[19,7],[19,12],[19,13],[19,14],[19,15],[21,90]],
        "story_summary": "Son of Zakariyya, named by Allah before his birth — a unique honor. Given wisdom while still a child. Described as having tenderness, purity, and righteousness from his very nature. Kind to his parents, not arrogant or disobedient. Peace upon him the day he was born, the day he dies, and the day he is raised alive — the same blessing given to Isa (19:33). He was the first to confirm Isa as a prophet.",
        "urdu_summary": "زکریا کے بیٹے، پیدائش سے پہلے اللہ نے نام رکھا۔ بچپن سے حکمت دی گئی۔ والدین کا مطیع، گناہ سے پاک، غرور سے دور۔ پیدائش، موت اور اٹھائے جانے کے دن سلام (19:15)۔",
        "lessons": [
            "Named by Allah before birth — some souls are designated for greatness from the start",
            "Wisdom given to the young — age is not a prerequisite for knowledge",
            "Chastity, kindness to parents, lack of arrogance — the three pillars of his character",
            "Peace at birth, death, and resurrection — the completeness of divine blessing"
        ],
        "connections": ["zakariyya", "isa", "maryam"],
        "tags": ["prophet", "straight", "wisdom", "chastity", "parents", "young"]
    },

    {
        "id": "muhammad",
        "name_arabic": "مُحَمَّد",
        "name_english": "Muhammad ﷺ",
        "name_urdu": "محمد ﷺ",
        "also_known_as": ["Ahmad", "Mustafa", "Al-Amin", "Khatam al-Nabiyyin (Seal of Prophets)", "Rahmatan lil-Alamin (Mercy to all worlds)"],
        "type": "prophet",
        "path": "straight",
        "path_reason": "Seal of all Prophets; Mercy to all worlds (21:107); described as of magnificent character (68:4); the Quran is his lasting miracle",
        "era": "570-632 CE, Makkah and Madinah",
        "mentioned_in": [[3,144],[33,40],[47,2],[48,29],[61,6]],
        "story_summary": "The final prophet and messenger of Allah. Born in Makkah, the city of Ibrahim. Named Muhammad (the praised one) and Ahmad (the most praising). Received the Quran over 23 years via Jibreel. Known as Al-Amin (the trustworthy) even before prophethood. Called to prophethood at 40. Faced severe opposition in Makkah for 13 years. Migrated to Madinah (Hijra). Built the first Muslim community. Returned to Makkah in the conquest with a general amnesty. Delivered the final sermon. Passed away at 63. The Quran is his eternal miracle — 'We will preserve the Reminder, and We are its Guardian' (15:9). Described in the Quran: 'And you are surely on a magnificent character' (68:4). Predicted by Isa as 'Ahmad' (61:6).",
        "urdu_summary": "آخری نبی اور رسول۔ مکہ میں پیدا ہوئے، المامین کہلائے۔ 40 سال میں نبوت ملی۔ 23 سال وحی آئی۔ 13 سال مکہ میں ظلم برداشت کیا۔ ہجرت مدینہ۔ امت بنائی۔ فتح مکہ پر عام معافی۔ خطبہ حجۃ الوداع۔ 63 سال میں وفات۔ قرآن ان کا دائمی معجزہ ہے۔",
        "lessons": [
            "Al-Amin — trustworthiness before prophethood; character precedes calling",
            "13 years of persecution in Makkah — patience before power",
            "Conquest of Makkah with general amnesty — power used for forgiveness",
            "His character (68:4) — the Quran is the description; his life is the commentary",
            "Rahmatan lil-alamin — mercy is the defining mission, not power",
            "Last sermon as a complete ethical charter for humanity"
        ],
        "connections": ["abu_bakr", "umar", "uthman", "ali", "khadijah", "aisha", "jibreel"],
        "tags": ["prophet", "straight", "seal-of-prophets", "mercy", "quran", "character", "final"]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  ANGELS — Malaika
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": "jibreel",
        "name_arabic": "جِبْرِيل",
        "name_english": "Jibreel (Gabriel)",
        "name_urdu": "جبریل علیہ السلام",
        "also_known_as": ["Gabriel", "Ruh al-Qudus (Holy Spirit)", "Ruh al-Amin (Trustworthy Spirit)", "Al-Namus (according to Waraqa)"],
        "type": "angel",
        "path": "straight",
        "path_reason": "The angel of revelation; brought the Quran to the Prophet ﷺ; described as powerful, trustworthy, obeyed (81:19-21)",
        "era": "From the beginning of creation to the end",
        "mentioned_in": [[2,97],[2,98],[2,253],[5,110],[16,102],[26,193],[66,4],[81,19],[81,20],[81,21]],
        "story_summary": "The greatest of the angels, the bearer of divine revelation. Brought the Quran to Muhammad ﷺ over 23 years. Described as 'of great power, secure in position with the Lord of the Throne, obeyed there and trustworthy' (81:19-21). Appeared to the Prophet ﷺ in his true form twice — once near Sidrat al-Muntaha (53:13-14). Appeared to Maryam in the form of a man. Appeared as a man to the companions to teach about Islam, Iman, and Ihsan (Hadith of Jibreel). He is supported by Allah's permission to bring revelation (2:97). Whoever is an enemy to Jibreel has made Allah their enemy (2:97-98).",
        "urdu_summary": "سب سے عظیم فرشتہ، وحی کا امین۔ 23 سال قرآن لاتے رہے۔ 'قوت والے، عرش والے کے ہاں با عزت' (81:19-21)۔ مریم کے پاس انسانی شکل میں آئے۔ صحابہ کو اسلام، ایمان اور احسان سکھایا۔",
        "lessons": [
            "The trustworthiness of the conveyor ensures the trustworthiness of the message",
            "Enmity to Jibreel is enmity to Allah — the carrier of divine words is sacred",
            "His appearance in human form — the bridge between the divine and human"
        ],
        "connections": ["muhammad", "maryam", "ibrahim", "musa", "isa"],
        "tags": ["angel", "straight", "revelation", "wahi", "trustworthy", "powerful"]
    },

    {
        "id": "mikael",
        "name_arabic": "مِيكَائِيل",
        "name_english": "Mikael (Michael)",
        "name_urdu": "میکائیل علیہ السلام",
        "also_known_as": ["Michael", "Angel of Provision"],
        "type": "angel",
        "path": "straight",
        "path_reason": "Named alongside Jibreel in the Quran; enmity to him means enmity to Allah (2:98)",
        "era": "From creation to its end",
        "mentioned_in": [[2,98]],
        "story_summary": "Named alongside Jibreel in Surah Al-Baqarah (2:98): 'Whoever is an enemy to Allah, and His angels, and His messengers, and Jibreel and Mikael — then indeed, Allah is an enemy to the disbelievers.' According to Islamic tradition, Mikael is responsible for rizq (provision) and rain — managing the physical sustenance of creation. He is among the highest angels.",
        "urdu_summary": "جبریل کے ساتھ ذکر (2:98)۔ روایت کے مطابق رزق اور بارش کے فرشتے۔",
        "lessons": ["Even the names of the angels are sacred — enmity to them is disbelief"],
        "connections": ["jibreel"],
        "tags": ["angel", "straight", "provision", "rain"]
    },

    {
        "id": "israfil",
        "name_arabic": "إِسْرَافِيل",
        "name_english": "Israfil",
        "name_urdu": "اسرافیل علیہ السلام",
        "also_known_as": ["Angel of the Trumpet"],
        "type": "angel",
        "path": "straight",
        "path_reason": "The angel who will blow the trumpet (Sur) to end creation and begin resurrection",
        "era": "From creation, will act at the end of time",
        "mentioned_in": [[6,73],[18,99],[20,102],[23,101],[27,87],[36,51],[39,68],[50,20],[50,41],[52,45],[54,6],[69,13],[74,8],[78,18],[79,6],[80,33]],
        "story_summary": "Not named in the Quran but extensively referenced as the blower of the Sur (trumpet/horn). The Quran frequently mentions the 'Sur' being blown as the signal of the Day of Judgment and resurrection. He has been holding the trumpet at his lips since creation, waiting for the command. At the first blow — all in the heavens and earth die (except whom Allah wills). At the second blow — all are resurrected.",
        "urdu_summary": "صور پھونکنے والا فرشتہ۔ قیامت کا آغاز اسی کے صور سے ہوگا۔ پہلے صور پر سب ہلاک، دوسرے پر سب اٹھیں گے۔",
        "lessons": ["The Day of Judgment is one command away — ever-readiness for accountability"],
        "connections": [],
        "tags": ["angel", "straight", "trumpet", "resurrection", "judgment-day"]
    },

    {
        "id": "izraeel",
        "name_arabic": "عِزْرَائِيل",
        "name_english": "Izraeel (Angel of Death)",
        "name_urdu": "عزرائیل علیہ السلام",
        "also_known_as": ["Malak al-Mawt (Angel of Death)", "Izrael"],
        "type": "angel",
        "path": "straight",
        "path_reason": "Carries out Allah's command over death; not named in Quran but referenced as 'Angel of Death' (32:11)",
        "era": "From creation to end",
        "mentioned_in": [[6,61],[32,11]],
        "story_summary": "Referenced in the Quran as 'the Angel of Death who has been entrusted with you' (32:11). He takes the souls of the dying by Allah's command. Described in 6:61 as angels who take souls. The Quran describes different levels of experience: souls taken in peace (gently drawn out) for the righteous, souls taken harshly for the wrongdoers.",
        "urdu_summary": "ملک الموت — 'کہو: تمہارے لیے مقرر موت کا فرشتہ تمہاری روح قبض کرے گا' (32:11)۔",
        "lessons": ["Death is not random — it is managed, appointed, and purposeful"],
        "connections": [],
        "tags": ["angel", "straight", "death", "soul", "appointed-time"]
    },

    {
        "id": "munkar_nakeer",
        "name_arabic": "مُنكَر وَنَكِير",
        "name_english": "Munkar and Nakeer",
        "name_urdu": "منکر و نکیر",
        "also_known_as": ["The Two Questioners of the Grave"],
        "type": "angel",
        "path": "straight",
        "path_reason": "Carry out Allah's will in questioning the dead; referenced in hadith extensively though not named in Quran",
        "era": "The realm of the grave (Barzakh)",
        "mentioned_in": [],
        "story_summary": "Referenced in hadith rather than named in the Quran, but connected to Quranic ayaat about the life of Barzakh (the grave). Allah affirms the believers in the grave (14:27): 'Allah keeps firm those who believe, with the firm word, in worldly life and in the Hereafter.' These two angels question the soul about its Lord, its religion, and its prophet.",
        "urdu_summary": "قبر کے دو سوال کرنے والے فرشتے — رب کون، دین کیا، نبی کون؟ قرآن میں بالواسطہ اشارہ (14:27)۔",
        "lessons": ["The answers you give in the grave reflect the life you lived above it"],
        "connections": [],
        "tags": ["angel", "straight", "grave", "barzakh", "questioning"]
    },

    {
        "id": "malik",
        "name_arabic": "مَالِك",
        "name_english": "Malik (Keeper of Hell)",
        "name_urdu": "مالک — جہنم کا داروغہ",
        "also_known_as": ["Keeper of Jahannam"],
        "type": "angel",
        "path": "straight",
        "path_reason": "Carries out Allah's just decree as the guardian of Hell",
        "era": "The Hereafter",
        "mentioned_in": [[43,77]],
        "story_summary": "Named in the Quran in 43:77 where the people of Hell will call out to him: 'O Malik, let your Lord put an end to us!' He will reply: 'Indeed, you will remain.' He is the stern, powerful guardian of Jahannam who carries out divine justice.",
        "urdu_summary": "جہنم کا داروغہ۔ اہل جہنم پکاریں گے: 'اے مالک! تیرا رب ہمیں فنا کر دے' — وہ کہے گا: 'تم رہو گے' (43:77)۔",
        "lessons": ["No exit from Hell — the permanence of divine justice for the unrepentant"],
        "connections": [],
        "tags": ["angel", "straight", "hell", "justice", "hereafter"]
    },

    {
        "id": "ridwan",
        "name_arabic": "رِضْوَان",
        "name_english": "Ridwan (Keeper of Paradise)",
        "name_urdu": "رضوان — جنت کا داروغہ",
        "also_known_as": ["Keeper of Jannah"],
        "type": "angel",
        "path": "straight",
        "path_reason": "Guardian of Paradise who welcomes the believers",
        "era": "The Hereafter",
        "mentioned_in": [[39,73]],
        "story_summary": "Referenced in 39:73: 'And those who feared their Lord will be led to Paradise in groups until, when they reach it while its gates have been opened and its keepers say, Peace be upon you; you have done well, so enter to abide eternally.' The keeper's greeting — salaam — is the welcome of the righteous.",
        "urdu_summary": "جنت کے دروازے کھلیں گے، داروغے کہیں گے: 'سلام ہو تم پر، تم نے اچھا کیا، داخل ہو جاؤ' (39:73)۔",
        "lessons": ["The greeting of paradise is Salam — peace that is the fulfillment of all peace sought in this world"],
        "connections": [],
        "tags": ["angel", "straight", "paradise", "welcome", "hereafter"]
    },

    {
        "id": "harut_marut",
        "name_arabic": "هَارُوت وَمَارُوت",
        "name_english": "Harut and Marut",
        "name_urdu": "ہاروت و ماروت",
        "also_known_as": [],
        "type": "angel",
        "path": "straight",
        "path_reason": "Angels who were sent as a test — they taught magic but warned people first that it is a trial and a disbelief",
        "era": "Ancient Babylon, time of Sulayman",
        "mentioned_in": [[2,102]],
        "story_summary": "Mentioned in 2:102 in the context of correcting the falsehood that Sulayman practiced magic. The two angels were in Babylon and taught people magic — but not without first warning them: 'We are only a trial, so do not disbelieve.' What they taught separated husband from wife. They could harm no one except by Allah's permission. Those who chose to learn from them chose harm over benefit. This ayah establishes: magic is real, it is disbelief, and it was not connected to Sulayman.",
        "urdu_summary": "بابل میں دو فرشتے جو جادو سکھاتے تھے لیکن پہلے بتاتے: 'ہم آزمائش ہیں، کفر نہ کرو'۔ جادو میاں بیوی میں جدائی ڈالتا — اللہ کی اجازت کے بغیر نقصان نہیں۔ سلیمان بری ہیں (2:102)۔",
        "lessons": [
            "Magic is real and it is kufr — not a harmless entertainment",
            "Every harm in this world requires Allah's permission",
            "Even a test comes with a warning — those who fail chose to fail",
            "Sulayman was completely innocent of magic — the Quran corrects slander"
        ],
        "connections": ["sulayman"],
        "tags": ["angel", "straight", "magic", "trial", "babylon"]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  COMPANIONS & KEY FIGURES — Sahabah wa Shakhsiyat
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": "abu_bakr",
        "name_arabic": "أَبُو بَكْر",
        "name_english": "Abu Bakr As-Siddiq",
        "name_urdu": "ابو بکر صدیق رضی اللہ عنہ",
        "also_known_as": ["As-Siddiq (The Truthful)", "Second of Two (in the cave)", "Atiq (freed by Allah from Fire)"],
        "type": "companion",
        "path": "straight",
        "path_reason": "Referenced in the Quran as 'the second of two in the cave' (9:40); the Prophet ﷺ comforted him with 'Do not grieve; Allah is with us'",
        "era": "570-634 CE, Makkah and Madinah",
        "mentioned_in": [[9,40],[92,17],[92,18],[92,19],[92,20],[92,21]],
        "story_summary": "The closest companion of the Prophet ﷺ and his father-in-law. The Quran references him in 9:40 during the Hijra: hiding in the cave of Thawr with the Prophet, he was afraid — 'Do not grieve; indeed Allah is with us.' He is believed by scholars to be referenced in 92:17-21 as 'the one who gives his wealth for purification, not expecting any favor in return, only seeking the pleasure of his Lord the Most High.' The first adult male to embrace Islam. The Prophet's closest companion. First Caliph after the Prophet's death.",
        "urdu_summary": "غار ثور میں ہجرت کے دوران نبی ﷺ کے ساتھ — 'غم نہ کرو، اللہ ہمارے ساتھ ہے' (9:40)۔ سب سے پہلے ایمان لانے والے بالغ مرد۔ خلیفہ اول۔",
        "lessons": [
            "Companionship in the cause of Allah is itself a blessing referenced in the Quran",
            "Grief in a righteous cause is met with divine reassurance",
            "Giving wealth purely for Allah's pleasure — 92:17-21 is his portrait"
        ],
        "connections": ["muhammad", "aisha"],
        "tags": ["companion", "straight", "siddiq", "cave", "hijra", "wealth", "trust"]
    },

    {
        "id": "ali",
        "name_arabic": "عَلِيّ",
        "name_english": "Ali ibn Abi Talib",
        "name_urdu": "علی ابن ابی طالب رضی اللہ عنہ",
        "also_known_as": ["Abu al-Hasan", "Al-Murtada", "Asadullah (Lion of Allah)"],
        "type": "companion",
        "path": "straight",
        "path_reason": "Among the foremost believers; his sleeping in the Prophet's bed during Hijra referenced by scholars as a supreme act of sacrifice",
        "era": "600-661 CE, Makkah, Madinah, Kufa",
        "mentioned_in": [[2,207],[3,61],[5,55],[76,8],[76,9]],
        "story_summary": "Cousin and son-in-law of the Prophet ﷺ. The first child to embrace Islam. Slept in the Prophet's bed during Hijra so the assassins would think the Prophet was still there. 2:207 is understood by scholars to reference his sacrifice that night: 'And of the people is he who sells himself, seeking means to the approval of Allah.' Surah Al-Insan (76:8-9) is understood to reference him and his family feeding the poor three nights in a row despite their own hunger. Fourth Caliph.",
        "urdu_summary": "نبی ﷺ کے چچازاد اور داماد۔ ہجرت کی رات نبی کے بستر پر سوئے۔ (2:207) اسی قربانی کی طرف اشارہ۔ (76:8-9) کھانا کھلانا تین راتیں باوجود خود فاقے کے۔ چوتھے خلیفہ۔",
        "lessons": [
            "Sacrifice of self for a greater cause — sleeping in the Prophet's bed",
            "Feeding the poor despite personal need — the epitome of ithar (preferring others)"
        ],
        "connections": ["muhammad", "fatimah", "hasan", "husayn"],
        "tags": ["companion", "straight", "sacrifice", "courage", "ithar"]
    },

    {
        "id": "aisha",
        "name_arabic": "عَائِشَة",
        "name_english": "Aisha bint Abi Bakr",
        "name_urdu": "عائشہ رضی اللہ عنہا",
        "also_known_as": ["Umm al-Mu'minin (Mother of the Believers)", "Al-Humayra", "Scholar of Islam"],
        "type": "companion",
        "path": "straight",
        "path_reason": "Mother of the Believers; Allah directly revealed her innocence in the Quran (24:11-20) — the greatest divine vindication",
        "era": "613-678 CE, Makkah and Madinah",
        "mentioned_in": [[24,11],[24,12],[24,16],[24,17],[24,23],[33,6],[33,32],[33,53],[66,3],[66,4]],
        "story_summary": "Youngest wife of the Prophet ﷺ and daughter of Abu Bakr. The incident of Al-Ifk (the slander): hypocrites spread false accusations about her. Allah revealed ten ayaat (24:11-20) establishing her complete innocence and condemning those who spread the slander. One of the greatest scholars of Islam — narrated thousands of hadith. The Prophet ﷺ said 'Learn half your religion from Humaira.' She is an Umm al-Mu'minin — a mother of all believers.",
        "urdu_summary": "نبی ﷺ کی زوجہ، ابو بکر کی بیٹی۔ افک کا واقعہ: منافقین نے الزام لگایا، اللہ نے دس آیات سے براءت ظاہر کی (24:11-20)۔ ہزاروں حدیث کی راوی، اسلام کی عظیم عالمہ۔",
        "lessons": [
            "Divine vindication — Allah Himself cleared her name",
            "Slander (qadhf) is a major sin — the Quran warned severely against it",
            "Women as primary transmitters of knowledge — Aisha taught the entire ummah",
            "Patience in facing false accusation — trusting Allah's eventual clarity"
        ],
        "connections": ["muhammad", "abu_bakr"],
        "tags": ["companion", "straight", "mother-of-believers", "scholar", "vindication", "slander"]
    },

    {
        "id": "abu_lahab",
        "name_arabic": "أَبُو لَهَب",
        "name_english": "Abu Lahab",
        "name_urdu": "ابو لہب",
        "also_known_as": ["Abd al-Uzza ibn Abd al-Muttalib", "Father of Flame"],
        "type": "person",
        "path": "deviated",
        "path_reason": "The only person condemned by name in the Quran (111:1-5); active enemy of the Prophet ﷺ despite being his uncle",
        "era": "Before Islam, Makkah, died 624 CE",
        "mentioned_in": [[111,1],[111,2],[111,3],[111,4],[111,5]],
        "story_summary": "Uncle of the Prophet ﷺ (son of Abd al-Muttalib, making him a blood relative). Yet he was the most virulent enemy of the Prophet in Makkah. When the Prophet ﷺ called his clan to Islam, Abu Lahab responded: 'May you perish! Is this why you called us?' An entire surah (Al-Masad) is revealed condemning him and his wife by name — the only such specific condemnation in the Quran. He would follow the Prophet in the markets undoing his message. He and his wife are condemned to the Fire. His wife Umm Jamil would carry thorny branches to scatter in the Prophet's path.",
        "urdu_summary": "نبی ﷺ کے چچا لیکن سب سے بڑے دشمن۔ 'تیرے ہاتھ ٹوٹیں، تو ہلاک ہو' کہا۔ قرآن نے نام لے کر مذمت کی — واحد شخص (111:1-5)۔ بیوی کانٹے ڈالتی تھی راستے میں۔",
        "lessons": [
            "Blood relation to a prophet does not guarantee faith or protection",
            "Active opposition to truth brings specific divine condemnation",
            "The Quran's prophecy — Abu Lahab would not believe — was fulfilled, proving the Quran's divine origin",
            "Wealth and children are no protection from divine judgment (111:2)"
        ],
        "connections": ["muhammad", "umm_jamil"],
        "tags": ["deviated", "enemy", "family", "condemned", "makkah"]
    },

    {
        "id": "umm_jamil",
        "name_arabic": "أُمّ جَمِيل",
        "name_english": "Umm Jamil (Wife of Abu Lahab)",
        "name_urdu": "ام جمیل",
        "also_known_as": ["Arwa bint Harb", "Carrier of thorns"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Condemned alongside her husband in Surah Al-Masad (111:4-5) as the carrier of thorns who will carry a rope of twisted fiber in Hell",
        "era": "Makkah, time of early Islam",
        "mentioned_in": [[111,4],[111,5]],
        "story_summary": "Wife of Abu Lahab and sister of Abu Sufyan. She would carry bundles of thorns and scatter them in the path where the Prophet ﷺ would walk, to hurt his feet. When Surah Al-Masad was revealed condemning her, she came to the Prophet ﷺ carrying a stone and said she had heard Muhammad was mocking her. Abu Bakr was with the Prophet — the Prophet sat silent, and she could not see him even though he was there. She is described in the Quran as carrying the fuel (firewood/thorns) in this world and will carry a rope of twisted fiber around her neck in Hell.",
        "urdu_summary": "ابو لہب کی بیوی جو نبی ﷺ کے راستے میں کانٹے بچھاتی تھی۔ قرآن نے 'حمالۃ الحطب' — کانٹے اٹھانے والی کہا (111:4)۔ جہنم میں رسی گردن میں ہوگی۔",
        "lessons": [
            "Active persecution of the Prophet is specifically recorded and punished",
            "Female agency in persecution and female accountability in the Quran",
            "Small acts of harassment against truth accumulate into major condemnation"
        ],
        "connections": ["abu_lahab", "muhammad"],
        "tags": ["deviated", "persecution", "enemy", "condemned"]
    },

    {
        "id": "abu_jahl",
        "name_arabic": "أَبُو جَهْل",
        "name_english": "Abu Jahl",
        "name_urdu": "ابو جہل",
        "also_known_as": ["Amr ibn Hisham", "Father of Ignorance (nickname given by Muslims)"],
        "type": "person",
        "path": "deviated",
        "path_reason": "One of the most violent persecutors of early Muslims; killed at Badr; referenced in 96:9-18",
        "era": "Makkah, died 624 CE at Battle of Badr",
        "mentioned_in": [[96,9],[96,10],[96,11],[96,12],[96,13],[96,14],[96,15],[96,16],[96,17],[96,18]],
        "story_summary": "One of the chieftains of Quraysh and the most vicious persecutor of the Prophet ﷺ and early Muslims. His real name was Amr ibn Hisham; Muslims called him Abu Jahl (Father of Ignorance). Surah Al-Alaq (96:9-18) was revealed about him specifically — describing 'the one who forbids a servant from praying,' threatening to grab him by the forelock if he saw the Prophet praying. He persecuted, tortured, killed early Muslims (including Sumayyah — the first martyr). He died at the Battle of Badr — young companions recognized and killed him. His treatment was exactly as the Quran had warned: dragged by the forelock.",
        "urdu_summary": "قریش کا سردار، سب سے ظالم ستانے والا۔ اصل نام عمرو بن ہشام۔ سورۃ العلق (96:9-18) اسی کے بارے میں نازل ہوئی — نماز پڑھنے سے روکنے والا۔ سمیہ رضی اللہ عنہا کا قاتل۔ بدر میں مارا گیا — پیشانی سے گھسیٹا گیا جیسا قرآن نے کہا تھا۔",
        "lessons": [
            "Preventing people from worship is specifically condemned",
            "The Quran's prophecy about his forelock was literally fulfilled at Badr",
            "Despite great social power and intellect, he chose destruction"
        ],
        "connections": ["muhammad", "sumayyah"],
        "tags": ["deviated", "persecutor", "enemy", "badr", "makkah"]
    },

    {
        "id": "sumayyah",
        "name_arabic": "سُمَيَّة",
        "name_english": "Sumayyah bint Khayyat",
        "name_urdu": "سمیہ رضی اللہ عنہا",
        "also_known_as": ["First Martyr of Islam", "Umm Ammar"],
        "type": "companion",
        "path": "straight",
        "path_reason": "First martyr of Islam; died under torture refusing to renounce faith",
        "era": "Early Islam, Makkah",
        "mentioned_in": [],
        "story_summary": "Though not named in the Quran directly, she is the first martyr of Islam — an elderly freed slave woman who was tortured by Abu Jahl for her faith. She refused to renounce Islam and was killed by Abu Jahl with a spear. Her husband Yasir and son Ammar were also tortured. The Prophet ﷺ would pass by them saying 'Be patient, family of Yasir — your promised place is Paradise.' The Quran's general ayaat about those who are oppressed for their faith (16:106, 22:58-59) encompass her story.",
        "urdu_summary": "اسلام کی پہلی شہیدہ — بوڑھی خاتون۔ ابو جہل نے نیزہ مار کر شہید کیا۔ نبی ﷺ نے کہا: 'صبر کرو، جنت وعدہ ہے'۔",
        "lessons": [
            "The first blood shed for Islam was that of an elderly woman — weakness in worldly terms, greatest strength in faith",
            "Patience under torture rather than renouncing truth",
            "Divine promise of paradise for those killed in faith"
        ],
        "connections": ["abu_jahl", "ammar"],
        "tags": ["companion", "straight", "martyr", "first", "women", "sabr"]
    },

    {
        "id": "ammar",
        "name_arabic": "عَمَّار",
        "name_english": "Ammar ibn Yasir",
        "name_urdu": "عمار ابن یاسر رضی اللہ عنہ",
        "also_known_as": [],
        "type": "companion",
        "path": "straight",
        "path_reason": "Allowed to say words of disbelief under torture while his heart remained firm; Quran directly vindicated him (16:106)",
        "era": "Early Islam, Makkah and Madinah",
        "mentioned_in": [[16,106]],
        "story_summary": "Son of Yasir and Sumayyah. Tortured in Makkah. Under extreme duress he verbally said words pleasing to his torturers but his heart remained firm in faith. He came to the Prophet ﷺ weeping — the Prophet asked if his heart was firm; he said yes. The Prophet ﷺ told him he could repeat it if they forced him again. Allah revealed 16:106: 'Whoever disbelieves in Allah after his belief — except for one who is forced while his heart is secure in faith.' This became the foundation of the principle of ikrah (coercion) in Islamic law.",
        "urdu_summary": "یاسر اور سمیہ کے بیٹے۔ تشدد میں زبان سے کفر کہہ دیا، دل مومن رہا۔ نبی ﷺ نے تسلی دی۔ اللہ نے آیت نازل کی (16:106): 'مگر جسے مجبور کیا جائے جبکہ دل ایمان پر مطمئن ہو'۔",
        "lessons": [
            "Coercion (ikrah) creates a different standard — forced words do not break faith",
            "The heart's condition is what Allah judges, not only the tongue",
            "Weeping at the perceived failure — the sincerity of Ammar's faith"
        ],
        "connections": ["sumayyah", "abu_jahl", "muhammad"],
        "tags": ["companion", "straight", "coercion", "martyrdom-family", "faith"]
    },

    {
        "id": "zayd",
        "name_arabic": "زَيْد",
        "name_english": "Zayd ibn Harithah",
        "name_urdu": "زید ابن حارثہ رضی اللہ عنہ",
        "also_known_as": ["Zayd ibn Muhammad (before ruling)", "The only companion named in the Quran"],
        "type": "companion",
        "path": "straight",
        "path_reason": "The only companion named by name in the Quran (33:37); his adoption was dissolved by divine command to establish a legal ruling",
        "era": "610-629 CE, Arabia",
        "mentioned_in": [[33,37]],
        "story_summary": "The freed slave and adopted son of the Prophet ﷺ. The only companion mentioned by name in the Quran. When he divorced his wife Zaynab bint Jahsh, Allah commanded the Prophet ﷺ to marry her — to establish that adoption does not create biological son status, and that a man may marry his adopted son's ex-wife. The Prophet had hidden the command out of fear of people's reaction — Allah addressed this in 33:37. A profound lesson about following divine command despite social pressure.",
        "urdu_summary": "نبی ﷺ کے آزاد کردہ غلام اور متبنیٰ بیٹے — قرآن میں نام سے ذکر ہونے والے واحد صحابی (33:37)۔ اپنی بیوی کو طلاق دی تو اللہ نے نبی کو اس سے نکاح کا حکم دیا — متبنیٰ کا رشتہ ختم کرنے کی شرعی وضاحت کے لیے۔",
        "lessons": [
            "Divine law sometimes runs against social custom — and must be followed anyway",
            "Adoption is honored but does not create biological legal status",
            "The Prophet himself feared people's reaction — vulnerability even in prophets",
            "Honor of being named in the Quran — the only companion with this distinction"
        ],
        "connections": ["muhammad", "zaynab_bint_jahsh"],
        "tags": ["companion", "straight", "adoption", "marriage", "divine-law"]
    },

    {
        "id": "luqman",
        "name_arabic": "لُقْمَان",
        "name_english": "Luqman",
        "name_urdu": "لقمان",
        "also_known_as": ["The Wise", "Luqman al-Hakim"],
        "type": "person",
        "path": "straight",
        "path_reason": "Given wisdom by Allah; his advice to his son in the Quran (31:12-19) is the complete parenting manual",
        "era": "Ancient times — scholars debate his identity and era",
        "mentioned_in": [[31,12],[31,13],[31,14],[31,15],[31,16],[31,17],[31,18],[31,19]],
        "story_summary": "A wise man mentioned in the Quran who was given wisdom by Allah (31:12). Not confirmed as a prophet. The Quran records his advice to his son across seven ayaat — a complete guide to raising a God-conscious child: do not associate partners with Allah, honor your parents (but not into disobedience to Allah), even if a deed is the weight of a mustard seed Allah will bring it forth, establish prayer, command good, forbid evil, be patient on what befalls you, do not turn your face from people in pride, walk with modesty, lower your voice.",
        "urdu_summary": "اللہ کا عطا کردہ حکیم (نبی ہونا ثابت نہیں)۔ بیٹے کو سات آیات میں نصیحت: شرک نہ کرو، والدین کا خیال رکھو، ذرے کے برابر بھی اللہ جانتا ہے، نماز قائم کرو، امر بالمعروف ونہی عن المنکر کرو، صبر کرو، غرور نہ کرو، آواز دھیمی رکھو۔",
        "lessons": [
            "Wisdom begins with gratitude to Allah (31:12)",
            "The seven pieces of advice cover the complete ethical foundation",
            "No deed is too small for Allah's knowledge — the mustard seed (31:16)",
            "Parenting is primarily about planting God-consciousness, not worldly achievement",
            "The modesty of voice and walk — outward behavior reflects inward character"
        ],
        "connections": [],
        "tags": ["straight", "wisdom", "parenting", "advice", "gratitude"]
    },

    {
        "id": "dhul_qarnayn",
        "name_arabic": "ذُو الْقَرْنَيْن",
        "name_english": "Dhul-Qarnayn",
        "name_urdu": "ذوالقرنین",
        "also_known_as": ["The Two-Horned One", "Alexander (debated)", "Cyrus the Great (debated)"],
        "type": "person",
        "path": "straight",
        "path_reason": "Given power in the earth by Allah; used it with justice; built the barrier against Yajuj and Majuj; attributed all power to Allah",
        "era": "Ancient history — identity debated",
        "mentioned_in": [[18,83],[18,84],[18,85],[18,86],[18,87],[18,88],[18,89],[18,90],[18,91],[18,92],[18,93],[18,94],[18,95],[18,96],[18,97],[18,98],[18,99]],
        "story_summary": "A powerful ruler given dominion across the earth by Allah. He traveled to the west (where the sun sets in murky water), then to the east (where the sun rises on people with no shelter), then between two mountains where a people complained about the corruptors Yajuj and Majuj. He built an iron and copper barrier to contain them. His response when offered payment for building the barrier: 'What my Lord has established me in is better — but assist me with strength and I will make a barrier between you and them.' At every stage he attributed his power to Allah. He declared the barrier is from the mercy of his Lord, and when Allah's promise comes the barrier will be leveled.",
        "urdu_summary": "اللہ کا عطا کردہ عالمی حکمران۔ مغرب، مشرق اور دو پہاڑوں کے درمیان تک سفر کیا۔ یاجوج ماجوج کے خلاف لوہے اور تانبے کی دیوار بنائی۔ معاوضہ ٹھکرایا: 'اللہ نے جو دیا وہ بہتر ہے'۔ طاقت کو اللہ سے منسوب کیا۔",
        "lessons": [
            "Power given by Allah used justly — not for personal gain",
            "Refusing payment: 'What my Lord has given me is better'",
            "The barrier of Yajuj and Majuj — a sign for the Last Days",
            "Attributing all capability to Allah at every stage of power"
        ],
        "connections": [],
        "tags": ["straight", "power", "justice", "yajuj-majuj", "barrier", "travel"]
    },

    {
        "id": "imran",
        "name_arabic": "عِمْرَان",
        "name_english": "Imran",
        "name_urdu": "عمران",
        "also_known_as": ["Father of Maryam", "Surah Ali Imran is named for his family"],
        "type": "person",
        "path": "straight",
        "path_reason": "A righteous man chosen by Allah; his family is among the chosen (3:33)",
        "era": "Roman-era Palestine",
        "mentioned_in": [[3,33],[3,35],[66,12]],
        "story_summary": "Father of Maryam, chosen by Allah among the families (3:33). His wife Hannah made a vow to dedicate her unborn child to Allah's service — the child turned out to be a girl (Maryam), not the boy she expected. Hannah said: 'The male is not like the female' — acknowledging her surprise. Allah accepted the dedication and made Maryam among the greatest of people. Imran is the grandfather of Isa through Maryam.",
        "urdu_summary": "مریم کے باپ، اللہ کے منتخب گھرانے کے سربراہ (3:33)۔ بیوی نے پیدائش سے پہلے ہی بچہ اللہ کی نذر کیا۔ بیٹی نکلی — 'لڑکا لڑکی جیسا نہیں' — اللہ نے قبول فرمایا۔",
        "lessons": [
            "Dedication of children to Allah's service — Maryam's life of devotion",
            "Allah's plan is better than ours — Hannah wanted a boy; Allah gave the mother of the Messiah",
            "Family lines chosen for divine purpose"
        ],
        "connections": ["maryam", "isa", "zakariyya"],
        "tags": ["straight", "family", "dedication", "chosen"]
    },

    {
        "id": "habil",
        "name_arabic": "هَابِيل",
        "name_english": "Habil (Abel)",
        "name_urdu": "ہابیل",
        "also_known_as": ["Abel"],
        "type": "person",
        "path": "straight",
        "path_reason": "His sacrifice was accepted; refused to kill in self-defense; the first righteous martyr (5:27-32)",
        "era": "First generation of humanity",
        "mentioned_in": [[5,27],[5,28],[5,29],[5,30],[5,31]],
        "story_summary": "Son of Adam whose sacrifice was accepted by Allah while his brother Qabil's was not. When Qabil threatened to kill him, Habil said: 'If you raise your hand against me to kill me — I shall not raise my hand against you to kill you. Indeed I fear Allah, Lord of the worlds. Indeed I want you to take upon yourself my sin and your sin so you will be among the companions of the Fire.' He was killed — the first death in human history. A raven showed Qabil how to bury him. His story establishes the sacredness of human life and the principle that killing one innocent soul is like killing all of humanity.",
        "urdu_summary": "آدم کا بیٹا جس کی قربانی قبول ہوئی۔ قابیل نے قتل کی دھمکی دی تو کہا: 'تو ہاتھ بڑھائے، میں نہ بڑھاؤں گا'۔ قتل ہوئے — انسانی تاریخ کا پہلا قتل۔ کوے نے دفن سکھایا۔",
        "lessons": [
            "Refusing to retaliate for a greater principle",
            "The first murder in human history — and its eternal condemnation (5:32)",
            "Acceptance or rejection of deeds is from Allah — not human approval",
            "Killing one innocent is like killing all of humanity (5:32)"
        ],
        "connections": ["adam", "qabil"],
        "tags": ["straight", "martyr", "first-murder", "sacrifice", "non-retaliation"]
    },

    {
        "id": "qabil",
        "name_arabic": "قَابِيل",
        "name_english": "Qabil (Cain)",
        "name_urdu": "قابیل",
        "also_known_as": ["Cain"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Killed his brother out of envy; committed the first murder; burdened with the sin of all who follow his method (5:30-32)",
        "era": "First generation of humanity",
        "mentioned_in": [[5,27],[5,28],[5,29],[5,30],[5,31],[5,32]],
        "story_summary": "Son of Adam whose sacrifice was not accepted while his brother's was. Instead of correcting himself, he gave in to envy and killed Habil — the first murder in human history. He did not know what to do with the body until a raven showed him by scratching the ground. He said: 'Woe to me! Have I failed to be like this raven and bury my brother's body?' He became remorseful. The Quran establishes: whoever kills an innocent person, it is as if he killed all of humanity. Whoever revives one person, it is as if he revived all of humanity. Qabil bears the sin of every murder committed from his day until the Day of Judgment.",
        "urdu_summary": "آدم کا بیٹا جس کی قربانی مقبول نہ ہوئی۔ حسد میں بھائی کو قتل کیا — پہلا قتل۔ کوے سے دفن سیکھا۔ پچھتایا۔ قیامت تک ہر قتل کا بوجھ اس پر ہے (5:32)۔",
        "lessons": [
            "Envy left unchecked leads to the worst acts",
            "Refusing to correct the inner cause (deficiency in sacrifice) and blaming others instead",
            "The weight of innovation in sin: the first murderer carries every subsequent murder's burden",
            "Regret after an irreversible act — remorse too late"
        ],
        "connections": ["adam", "habil", "iblis"],
        "tags": ["deviated", "murder", "envy", "first-sin", "hasad"]
    },

    {
        "id": "jalut",
        "name_arabic": "جَالُوت",
        "name_english": "Jalut (Goliath)",
        "name_urdu": "جالوت",
        "also_known_as": ["Goliath"],
        "type": "person",
        "path": "deviated",
        "path_reason": "Giant warrior and oppressor defeated by young Dawud; symbol of oppressive power overcome by faith",
        "era": "Ancient Palestine, time of Dawud",
        "mentioned_in": [[2,249],[2,250],[2,251]],
        "story_summary": "The giant warrior of the enemy forces against Bani Israel. The small believing army (those who passed the river test) faced him. Dawud, a young man, picked up five stones from a river. He killed Jalut with one. Allah gave Dawud kingship and wisdom. The story establishes: small in number but firm in faith overcomes large in number but absent in faith. 'How many a small company has overcome a large company by permission of Allah' (2:249).",
        "urdu_summary": "دشمن فوج کا دیوقامت سردار۔ نوجوان داؤد نے پتھر سے قتل کیا۔ داؤد کو ملک اور حکمت ملی۔ 'کتنی ہی چھوٹی جماعت بڑی جماعت پر غالب آئی اللہ کی اجازت سے' (2:249)۔",
        "lessons": [
            "Physical might means nothing before faith",
            "Small numbers + tawakkul > large numbers without it",
            "The stone that killed Jalut launched Dawud's prophethood"
        ],
        "connections": ["dawud", "bani_israel", "talut"],
        "tags": ["deviated", "warrior", "oppressor", "defeated", "faith-vs-power"]
    },

    {
        "id": "talut",
        "name_arabic": "طَالُوت",
        "name_english": "Talut (Saul)",
        "name_urdu": "طالوت",
        "also_known_as": ["Saul", "King of Bani Israel"],
        "type": "person",
        "path": "straight",
        "path_reason": "Chosen by Allah as king; his test (the river) separated the committed from the uncommitted; led the victory over Jalut",
        "era": "Ancient Palestine, before Dawud",
        "mentioned_in": [[2,247],[2,248],[2,249],[2,250],[2,251]],
        "story_summary": "Chosen by Allah as king of Bani Israel when they asked for a king to lead them against their enemies. They objected — he was not wealthy or of noble birth. The prophet told them: 'Allah has chosen him above you and has increased him abundantly in knowledge and stature. And Allah gives His sovereignty to whom He wills.' The test of the river — whoever drinks from it is not with him; only those who take a handful are of his company. Most drank; only a small group remained faithful. They went on to overcome Jalut's army.",
        "urdu_summary": "بنی اسرائیل نے بادشاہ مانگا — اللہ نے طالوت کو چنا۔ انہوں نے اعتراض کیا: نہ مالدار نہ خاندانی۔ نبی نے کہا: اللہ نے علم اور جسم میں فوقیت دی۔ دریا کا امتحان: جس نے پیا وہ ہمارے ساتھ نہیں — اکثر نے پیا، چند ثابت قدم رہے۔",
        "lessons": [
            "Leadership is from Allah — not from wealth or birth",
            "The river test: commitment is proven in small moments of restraint",
            "Most people fail tests of self-restraint — but a faithful few are enough",
            "Do not judge leadership by worldly standards"
        ],
        "connections": ["dawud", "jalut", "bani_israel"],
        "tags": ["straight", "king", "test", "leadership", "faith", "bani-israel"]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  GROUPS — Majmuat
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": "bani_israel",
        "name_arabic": "بَنُو إِسْرَائِيل",
        "name_english": "Bani Israel (Children of Israel)",
        "name_urdu": "بنی اسرائیل",
        "also_known_as": ["Children of Israel", "The Israelites"],
        "type": "group",
        "path": "mixed",
        "path_reason": "A nation given immense blessings and prophets; repeatedly deviated, repented, and deviated again; the Quran's most addressed nation after the Arabs",
        "era": "From Yaqub through to the time of Muhammad ﷺ",
        "mentioned_in": [[2,40],[2,47],[2,83],[2,122],[3,49],[5,20],[7,137],[7,138],[17,2],[17,4],[20,80],[26,59],[32,23],[45,16]],
        "story_summary": "The descendants of Yaqub (Israel), given immense blessings: prophets, scripture, miracles, liberation from Pharaoh, the split sea, provision of manna and quail, forgiveness of the golden calf. Yet they repeatedly broke their covenant, asked to see Allah directly, worshipped the golden calf, killed their prophets, altered their scriptures, and violated the Sabbath. The Quran addresses them extensively — both to remind them of their blessings and to warn them of their transgressions. The pattern: blessing → ingratitude → punishment → repentance → blessing — repeated.",
        "urdu_summary": "یعقوب کی اولاد — عظیم نعمتیں ملیں: انبیاء، کتابیں، معجزات، فرعون سے نجات۔ بار بار عہد توڑا، بچھڑا پوجا، انبیاء کو قتل کیا، کتابیں بدلیں، سبت توڑا۔ برکت→ناشکری→عذاب→توبہ — یہ چکر بار بار۔",
        "lessons": [
            "Blessings without gratitude lead to repeated failure",
            "The Quran's warnings to Bani Israel are also warnings to this ummah — same patterns recur",
            "Killing prophets is the ultimate betrayal of divine trust",
            "Covenant-breaking has generational consequences",
            "Ingratitude after miracles is particularly condemned"
        ],
        "connections": ["musa", "haroon", "dawud", "isa", "yaqub", "firawn"],
        "tags": ["group", "mixed", "covenant", "prophets", "blessings", "ingratitude"]
    },

    {
        "id": "people_of_aad",
        "name_arabic": "قَوْم عَاد",
        "name_english": "People of Aad",
        "name_urdu": "قوم عاد",
        "also_known_as": ["Aad"],
        "type": "group",
        "path": "deviated",
        "path_reason": "Rejected prophet Hud; boasted of their power; destroyed by a violent wind lasting seven nights and eight days",
        "era": "Ancient Arabia, pre-Ibrahim",
        "mentioned_in": [[7,65],[7,69],[7,72],[9,70],[11,50],[11,58],[11,60],[14,9],[22,42],[25,38],[26,123],[29,38],[38,12],[40,31],[41,13],[41,15],[41,16],[46,21],[46,25],[50,13],[51,41],[53,50],[54,18],[54,19],[54,20],[54,21],[69,4],[69,6],[69,7],[69,8],[89,6],[89,7],[89,8]],
        "story_summary": "A powerful, arrogant civilization in ancient Arabia known for their towering pillars (89:7). They asked: 'Who is mightier than us?' They rejected their prophet Hud and were destroyed by a violent wind (reeh sarsar) that lasted seven nights and eight days continuously — it left them like hollow trunks of palm trees (69:7). Their ruins are referenced in the Quran. They are the archetypal example of arrogance destroyed.",
        "urdu_summary": "قدیم عرب کی طاقتور قوم — 'ہم سے قوی کون ہے؟' ہود کو جھٹلایا۔ سات رات آٹھ دن کی تیز آندھی — کھجور کے ٹھونٹھوں کی طرح گرے (69:7)۔",
        "lessons": [
            "Physical strength and civilization are temporary",
            "Arrogance about power is the most cited reason for divine punishment",
            "The wind: Allah destroys with the weakest of natural forces what armies cannot"
        ],
        "connections": ["hud"],
        "tags": ["group", "deviated", "arrogance", "destroyed", "wind"]
    },

    {
        "id": "people_of_thamud",
        "name_arabic": "قَوْم ثَمُود",
        "name_english": "People of Thamud",
        "name_urdu": "قوم ثمود",
        "also_known_as": ["Thamud"],
        "type": "group",
        "path": "deviated",
        "path_reason": "Hamstrung the she-camel of Allah despite warning; destroyed by a blast three days after the warning",
        "era": "Ancient Arabia, post-Hud era",
        "mentioned_in": [[7,73],[7,74],[7,77],[7,78],[9,70],[11,61],[11,68],[14,9],[17,59],[22,42],[25,38],[26,141],[27,45],[29,38],[38,13],[40,31],[41,13],[41,17],[41,18],[50,12],[51,43],[53,51],[54,23],[54,27],[54,28],[54,29],[54,30],[54,31],[69,4],[69,5],[85,18],[89,9],[89,11],[91,11],[91,14]],
        "story_summary": "A people who carved homes in the mountains. Given the she-camel as a miracle and test. One man (the most wretched among them — 91:12) hamstrung her, though the Quran assigns collective responsibility to them all. They were warned of three days. On the third day the blast came. The Quran references them frequently as a clear sign for those who pass their area (27:52). Surah Ash-Shams (91) devotes its climax to their story.",
        "urdu_summary": "پہاڑ تراشنے والی قوم۔ اونٹنی کا معجزہ دیا — سب سے بدبخت نے کونچیں کاٹیں۔ تین دن بعد چنگھاڑ۔ 'اپنے رب کی نافرمانی کی تو انہیں ہلاک کر دیا' (91:14)۔",
        "lessons": [
            "Collective responsibility for the act of one — the most wretched represents the community's choice",
            "A specific divine sign deliberately destroyed — the ultimate ingratitude",
            "Three days' warning — divine justice gives notice before punishment"
        ],
        "connections": ["salih"],
        "tags": ["group", "deviated", "she-camel", "destroyed", "collective-responsibility"]
    },

    {
        "id": "people_of_lut",
        "name_arabic": "قَوْم لُوط",
        "name_english": "People of Lut",
        "name_urdu": "قوم لوط",
        "also_known_as": ["Sodom and Gomorrah", "Mu'tafikaat"],
        "type": "group",
        "path": "deviated",
        "path_reason": "Normalized sexual transgression, rejected their prophet, and tried to assault the angelic guests; their cities were overturned",
        "era": "Time of Ibrahim and Lut",
        "mentioned_in": [[7,80],[7,81],[7,82],[7,83],[7,84],[9,70],[11,77],[11,78],[11,82],[11,83],[15,67],[15,68],[15,69],[22,43],[26,160],[26,165],[27,54],[27,55],[27,56],[29,28],[29,29],[29,35],[51,32],[51,33],[53,53],[54,33],[54,34]],
        "story_summary": "The people of Sodom and Gomorrah who had normalized homosexual acts as a public practice (going beyond this to robbery and other transgressions). They rejected Lut's call. When the angels came as guests, the people rushed to Lut's house demanding access to them. The cities were destroyed — turned upside down with stones of hardened clay raining down on them (11:82-83). Their destruction is referenced extensively throughout the Quran as a warning.",
        "urdu_summary": "سدوم اور عمورہ کے لوگ جنہوں نے بدکاری کو عام کر لیا تھا۔ لوط کے مہمانوں سے بدکاری کا ارادہ کیا۔ شہر الٹے گئے، پکی مٹی کے پتھروں کی بارش ہوئی (11:82)۔",
        "lessons": [
            "Normalization of transgression accelerates collective punishment",
            "Transgression against guests is a specific violation of sacred hospitality",
            "Their ruins remain as a visible sign (29:35)"
        ],
        "connections": ["lut", "ibrahim"],
        "tags": ["group", "deviated", "transgression", "destroyed", "normalization"]
    },

    {
        "id": "people_of_midian",
        "name_arabic": "أَهْل مَدْيَن",
        "name_english": "People of Midian",
        "name_urdu": "اہل مدین",
        "also_known_as": ["Midianites"],
        "type": "group",
        "path": "deviated",
        "path_reason": "Cheated in weights and measures, robbed travelers, rejected Shuayb; destroyed by the earthquake",
        "era": "Ancient Midian (northwest Arabia)",
        "mentioned_in": [[7,85],[7,91],[9,70],[11,84],[11,95],[22,44],[28,22],[28,23],[29,36],[29,37]],
        "story_summary": "The people of Midian who cheated in weights and measures and engaged in highway robbery. Their prophet Shuayb called them to business ethics and justice. They rejected him. The earthquake destroyed them — 'and the people of Midian — the people of Shuayb were destroyed, and Musa's destination was also Midian' (29:36-37 context).",
        "urdu_summary": "مدین کے لوگ جو ناپ تول میں کمی اور ڈاکہ زنی کرتے تھے۔ شعیب کو جھٹلایا۔ زلزلے نے ہلاک کیا۔",
        "lessons": [
            "Business ethics are a religious obligation — their violation destroys communities",
            "Economic injustice left uncorrected accumulates into divine punishment"
        ],
        "connections": ["shuayb", "musa"],
        "tags": ["group", "deviated", "business-ethics", "destroyed", "earthquake"]
    },

    {
        "id": "ashabus_sabt",
        "name_arabic": "أَصْحَاب السَّبْت",
        "name_english": "People of the Sabbath",
        "name_urdu": "اصحاب السبت",
        "also_known_as": ["Companions of the Sabbath"],
        "type": "group",
        "path": "deviated",
        "path_reason": "Used deception to violate the Sabbath prohibition; transformed into apes as divine punishment (7:163-166)",
        "era": "Ancient Israelite history",
        "mentioned_in": [[2,65],[4,47],[4,154],[7,163],[7,164],[7,165],[7,166]],
        "story_summary": "A community by the sea who were forbidden from fishing on the Sabbath (Saturday). The fish would come abundantly on Saturday and be scarce other days — a specific test. They devised a trick: they set nets on Friday, collected fish on Sunday. They thought they were technically not violating the Sabbath. When they refused the warning of the righteous among them, Allah transformed them into apes as punishment. The Quran references this as a 'deterrent punishment' for those before them and a lesson for the righteous.",
        "urdu_summary": "سمندر کنارے قوم جن پر سبت کا پابندی تھی۔ ہفتے کو مچھلیاں کثرت سے آتیں — آزمائش۔ انہوں نے چال چلی: جمعہ کو جال ڈالیں، اتوار کو اٹھائیں۔ بندر بنا دیے گئے — 'ذلیل بندر ہو جاؤ' (7:166)۔",
        "lessons": [
            "Circumventing the spirit of a law while following its letter is deception",
            "Tests come in the form of abundant temptation at exactly the forbidden time",
            "Deterrent punishment: visible transformation as a sign for others",
            "Community responsibility — the righteous who warned were saved"
        ],
        "connections": ["bani_israel"],
        "tags": ["group", "deviated", "sabbath", "deception", "transformed", "test"]
    },

    {
        "id": "ashabul_kahf",
        "name_arabic": "أَصْحَاب الْكَهْف",
        "name_english": "People of the Cave",
        "name_urdu": "اصحاب الکہف",
        "also_known_as": ["The Seven Sleepers"],
        "type": "group",
        "path": "straight",
        "path_reason": "Young men who fled their society to preserve their faith; slept in the cave by divine protection; their story is told as an example of faith in resurrection",
        "era": "Roman era (Decius persecution, approximately 250 CE — scholarly debate)",
        "mentioned_in": [[18,9],[18,10],[18,11],[18,12],[18,13],[18,14],[18,15],[18,16],[18,17],[18,18],[18,19],[18,20],[18,21],[18,22],[18,23],[18,24],[18,25],[18,26]],
        "story_summary": "A group of young men (with their dog) who rejected the polytheism of their society and took refuge in a cave. 'They were youths who believed in their Lord, and We increased them in guidance.' They prayed: 'Our Lord, grant us from Yourself mercy and prepare for us from our affair right guidance.' Allah caused them to sleep for 309 years. When they awoke they thought they had slept a day or part of a day. They sent one with money to buy food, warning him to be quiet about them. The city had changed to a believing community. Their story confirmed the resurrection — a direct divine proof that sleep is a kind of death and waking is a kind of resurrection.",
        "urdu_summary": "نوجوانوں کی جماعت جو شرک سے بھاگ کر غار میں پناہ لی۔ 'وہ نوجوان تھے جو اپنے رب پر ایمان لائے' (18:13)۔ 309 سال سوئے — اٹھے تو سوچا تھوڑی دیر سوئے۔ قیامت کی دلیل بنے۔",
        "lessons": [
            "Fleeing a corrupt environment to preserve faith is a valid and honored choice",
            "Youth and faith together are among the most beloved things to Allah",
            "Sleep is a form of death — waking is a form of resurrection",
            "The dog — even a loyal animal is remembered alongside the faithful",
            "Divine protection: the sun adjusted its angle so it would not harm them (18:17)"
        ],
        "connections": [],
        "tags": ["group", "straight", "youth", "faith", "cave", "sleep", "resurrection-proof"]
    },

    {
        "id": "ashabul_ukhdud",
        "name_arabic": "أَصْحَاب الْأُخْدُود",
        "name_english": "People of the Ditch",
        "name_urdu": "اصحاب الاخدود",
        "also_known_as": ["Companions of the Trench"],
        "type": "group",
        "path": "mixed",
        "path_reason": "The tyrants who dug the trench (deviated — destroyed); the believers thrown in (straight — martyred and in Jannah)",
        "era": "Pre-Islamic Arabia or Yemen, scholars debate",
        "mentioned_in": [[85,4],[85,5],[85,6],[85,7],[85,8],[85,9],[85,10]],
        "story_summary": "Rulers who dug a trench, filled it with fire, and burned alive believers who refused to renounce their faith. The Quran condemns the persecutors and says they are in the punishment of the burning fire (85:10). The believers who were thrown in and died are implied to be in Jannah — 'the companions of Paradise' (85:11). The story is referenced as one of the gravest crimes against believers. Their only crime was that they believed in Allah the Mighty, the Praiseworthy (85:8).",
        "urdu_summary": "آگ کی خندق کھودنے والوں نے ایمان والوں کو زندہ جلایا۔ ایمان والوں کا قصور صرف یہ تھا کہ وہ اللہ پر ایمان لائے تھے (85:8)۔ ظالم آگ کے عذاب میں، شہید جنت میں۔",
        "lessons": [
            "The only 'crime' of the believers was their faith — the purest form of persecution",
            "Martyrdom for faith: sitting at the edge of the trench and choosing death over denial",
            "Persecutors of believers will face the fire they thought they were victorious with",
            "Faith that does not waver even before the fire"
        ],
        "connections": [],
        "tags": ["mixed", "martyrdom", "persecutors", "faith", "fire", "persecution"]
    },

    {
        "id": "munafiqqun",
        "name_arabic": "الْمُنَافِقُون",
        "name_english": "The Hypocrites",
        "name_urdu": "منافقین",
        "also_known_as": ["The Hypocrites", "Those with two faces"],
        "type": "group",
        "path": "deviated",
        "path_reason": "Outward profession of Islam with inner disbelief; described as in the lowest depths of Hell (4:145); a surah named for them (Al-Munafiqun)",
        "era": "Madinah period of early Islam",
        "mentioned_in": [[2,8],[2,9],[2,10],[2,11],[2,12],[2,13],[2,14],[2,15],[2,16],[2,17],[2,18],[2,19],[2,20],[3,167],[4,61],[4,88],[4,138],[4,140],[4,142],[4,143],[4,145],[8,49],[9,64],[9,67],[9,73],[9,77],[9,78],[9,79],[9,80],[9,84],[9,85],[9,86],[9,87],[29,11],[33,1],[33,48],[33,60],[47,20],[48,6],[57,13],[57,14],[58,14],[59,11],[63,1],[63,2],[63,3],[63,4],[63,5],[63,6],[63,7],[63,8]],
        "story_summary": "The hypocrites of Madinah who outwardly professed Islam while concealing disbelief. Led by Abdullah ibn Ubayy ibn Salul (though he is not named in the Quran). They would say 'We believe' then privately say 'We are only mocking.' They undermined the Muslim community, spread discord, refused to fight, returned from battles, and threatened to expel the Prophet from Madinah. A whole surah (Al-Munafiqun) addresses them. They are described as 'in the lowest depths of the Fire' (4:145) — below even the open disbelievers.",
        "urdu_summary": "مدینہ کے منافقین جو ظاہر میں مسلمان، باطن میں کافر۔ اللہ ان کا مذاق اڑا رہا ہے (2:15)۔ مسجد اور جماعت میں شرکت — لیکن نماز میں سستی (4:142)۔ جہنم کے سب سے نچلے طبقے میں (4:145)۔",
        "lessons": [
            "Hypocrisy is worse than open disbelief in divine ranking",
            "Allah sees what no human can — inner faith vs outer profession",
            "The signs of nifaq: lying, breaking promises, betrayal of trust (Hadith)",
            "The lowest level of Hell reserved for them — a serious warning",
            "Community threat from within is more dangerous than open enemies"
        ],
        "connections": ["muhammad", "abu_bakr"],
        "tags": ["group", "deviated", "hypocrisy", "deceit", "lowest-hell", "madinah"]
    },

    {
        "id": "hawariyyun",
        "name_arabic": "الْحَوَارِيُّون",
        "name_english": "The Disciples of Isa",
        "name_urdu": "حواریون",
        "also_known_as": ["The Apostles of Jesus", "The Disciples"],
        "type": "group",
        "path": "straight",
        "path_reason": "Responded to Isa's call: 'We are helpers of Allah' (61:14); asked for the table from heaven; bore witness to Isa's message",
        "era": "Roman-era Palestine, time of Isa",
        "mentioned_in": [[3,52],[3,53],[5,111],[5,112],[5,113],[5,114],[5,115],[61,14]],
        "story_summary": "The chosen companions of Isa who believed in him and supported his mission. When Isa asked 'Who will be my helpers toward Allah?' they responded: 'We are the helpers of Allah.' They asked for the Table Spread (Ma'idah) from heaven — a feast from Allah as a sign and festival day. Allah granted it with a warning: whoever disbelieves after this, he will punish with a punishment unlike any in the worlds. They are cited in 61:14 as the example of supporters who helped Isa, and the call is made to believers to be like them.",
        "urdu_summary": "عیسیٰ کے منتخب ساتھی۔ 'کون ہے اللہ کی طرف میرا مددگار؟' — 'ہم انصار اللہ ہیں'۔ آسمانی دسترخوان مانگا — ملا، تنبیہ کے ساتھ (5:115)۔ 61:14 میں نمونہ کے طور پر پیش۔",
        "lessons": [
            "Responding to the call with 'We are the helpers of Allah' — the model response",
            "Asking for a sign to strengthen certainty is acceptable",
            "After a clear sign, rejection is the gravest disbelief"
        ],
        "connections": ["isa", "maryam"],
        "tags": ["group", "straight", "disciples", "support", "isa", "table"]
    },

    {
        "id": "people_of_yunus",
        "name_arabic": "قَوْم يُونُس",
        "name_english": "People of Yunus",
        "name_urdu": "قوم یونس",
        "also_known_as": ["People of Nineveh"],
        "type": "group",
        "path": "straight",
        "path_reason": "The only community who believed and were accepted after seeing the signs of punishment approaching — their faith was accepted (10:98)",
        "era": "Ancient Nineveh (modern Iraq)",
        "mentioned_in": [[10,98],[37,147],[37,148]],
        "story_summary": "The people of Yunus (Nineveh). When Yunus left them, punishment signs appeared. Unlike the people of Nuh, Aad, and Thamud who saw punishment arrive and could not repent — these people repented before it actually struck, when they saw its approach. Their faith was accepted. 100,000+ people believed (37:147). The Quran specifically notes this as unique: the only community whose belief was accepted in such circumstances (10:98).",
        "urdu_summary": "یونس کی قوم — جب یونس نے چھوڑا تو عذاب کی نشانیاں ظاہر ہوئیں۔ پہنچنے سے پہلے ایمان لائے — قبول ہوا۔ ایک لاکھ سے زیادہ ایمان لائے (37:147)۔ واحد قوم جس کی یہ توبہ قبول ہوئی۔",
        "lessons": [
            "Repentance before punishment fully arrives can still be accepted",
            "The timing of sincerity matters",
            "Collective repentance of an entire city — the greatest example of mass return to faith"
        ],
        "connections": ["yunus"],
        "tags": ["group", "straight", "repentance", "unique", "mass-faith", "nineveh"]
    },

]

# ══════════════════════════════════════════════════════════════════════════════
#  LOOKUP HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_by_id(personality_id: str) -> dict:
    for p in PERSONALITIES:
        if p["id"] == personality_id:
            return p
    return {}

def get_by_path(path: str) -> list:
    """Returns all personalities with a given path: 'straight', 'deviated', 'mixed', 'unknown'."""
    return [p for p in PERSONALITIES if p["path"] == path]

def get_by_type(ptype: str) -> list:
    """Returns all of a given type: 'prophet', 'angel', 'jinn', 'companion', 'person', 'group'."""
    return [p for p in PERSONALITIES if p["type"] == ptype]

def get_connected(personality_id: str) -> list:
    """Returns all personalities connected to the given id."""
    p = get_by_id(personality_id)
    if not p:
        return []
    return [get_by_id(cid) for cid in p.get("connections", []) if get_by_id(cid)]


if __name__ == "__main__":
    print(f"Total personalities: {len(PERSONALITIES)}")
    straight = get_by_path("straight")
    deviated = get_by_path("deviated")
    mixed    = get_by_path("mixed")
    prophets = get_by_type("prophet")
    angels   = get_by_type("angel")
    print(f"  Straight path : {len(straight)}")
    print(f"  Deviated path : {len(deviated)}")
    print(f"  Mixed path    : {len(mixed)}")
    print(f"  Prophets      : {len(prophets)}")
    print(f"  Angels        : {len(angels)}")
