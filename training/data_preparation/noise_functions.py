import random, re

# Dictionary of common homophone mistakes (wrong → correct)
HOMOPHONE_MAP = {
    "their": "there",
    "there": "their",
    "they're": "their",
    "your": "you're",
    "you're": "your",
    "its": "it's",
    "it's": "its",
    "to": "too",
    "too": "to",
    "then": "than",
    "than": "then",
    "affect": "effect",
    "effect": "affect",
    "accept": "except",
    "except": "accept",
    "bear": "bare",
    "bare": "bear",
    "weather": "whether",
    "whether": "weather",
    "lose": "loose",
    "loose": "lose",
    "brake": "break",
    "break": "brake",
    "peace": "piece",
    "piece": "peace",
    "two": ["to", "too"],
    "to": ["two", "too"],
    "too": ["to", "two"],
    "four": ["for"],
    "for": ["four"],
    "one": ["won"],
    "won": ["one"],
    "eight": ["ate"],
    "ate": ["eight"],
}

# Contraction mapping: contraction ↔ expansion
CONTRACTION_MAP = {
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "I'd": "I would",
    "I'll": "I will",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it's": "it is",
    "let's": "let us",
    "mightn't": "might not",
    "mustn't": "must not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "we'd": "we would",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what's": "what is",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
}

PREPOSITIONS = [
    "in", "on", "at", "to", "from", "with", "by", "about", "over", "under", 
    "of", "for", "into", "onto", "off", "out", "through", "around", "against", 
    "before", "after", "between", "without"
]

PREPOSITION_CONFUSIONS = {
    "in": ["on", "at"],
    "on": ["in", "at"],
    "at": ["in", "on"],
    "to": ["for", "toward"],
    "from": ["of", "out"],
    "with": ["by", "along"],
    "by": ["with", "via"],
    "about": ["around", "concerning"],
    "over": ["above", "on"],
    "under": ["beneath", "below"],
    "of": ["from", "to"],
    "for": ["to", "in"],
    "into": ["in", "onto"],
    "onto": ["into", "on"],
    "off": ["out", "from"],
    "out": ["off", "away"],
    "through": ["via", "along"],
    "around": ["about", "surrounding"],
    "against": ["versus", "beside"],
    "before": ["prior", "ahead"],
    "after": ["following", "later"],
    "between": ["among"],
    "without": ["no", "lacking"]
}

PRONOUN_CONFUSIONS = {
    "i": ["you", "we", "they"],
    "you": ["we", "i", "they"],
    "he": ["she", "they", "i"],
    "she": ["he", "they", "you"],
    "they": ["we", "you", "he"],
    "we": ["you", "they", "i"],
    "me": ["you", "him", "her"],
    "him": ["her", "me", "them"],
    "her": ["him", "me", "them"],
    "us": ["them", "you", "me"],
    "them": ["us", "him", "her"],
    "my": ["your", "their"],
    "your": ["my", "our"],
    "his": ["her", "their"],
    "her": ["his", "their"],
    "our": ["your", "my"],
    "their": ["his", "her"]
}

# Reverse map for contractions
EXPANSION_MAP = {v: k for k, v in CONTRACTION_MAP.items()}

ARTICLES = ["a", "an", "the"]


def homophone_mistake(sentence: str) -> str:
    tokens = re.findall(r"\w+|[^\w\s]", sentence)
    changed = False
    new_tokens = []

    for token in tokens:
        lower_token = token.lower()
        if lower_token in HOMOPHONE_MAP:
            replacement = HOMOPHONE_MAP[lower_token]
            if isinstance(replacement, list):
                replacement = random.choice(replacement)
            replacement = replacement if token.islower() else replacement.capitalize()
            new_tokens.append(replacement)
            changed = True
        else:
            new_tokens.append(token)

    if not changed:
        return sentence  # No change

    # Reconstruct with proper spacing (space before word unless it's punctuation)
    output = ""
    for i, tok in enumerate(new_tokens):
        if i > 0 and not re.match(r"[^\w\s]", tok):  # not punctuation
            output += " "
        output += tok

    return output

def break_subject_verb_agreement(sent):
    sent = re.sub(r"\b(is)\b", "are", sent)
    sent = re.sub(r"\b(are)\b", "is", sent)
    sent = re.sub(r"\b(doesn't)\b", "don't", sent)
    sent = re.sub(r"\b(don't)\b", "doesn't", sent)
    sent = re.sub(r"\b(has)\b", "have", sent)
    sent = re.sub(r"\b(have)\b", "has", sent)
    return sent

def drop_auxiliaries(sent):
    return re.sub(r"\b(has|have|had|was|were|is|are|am|will)\b", "", sent).replace("  ", " ").strip()

def corrupt_verb_tense(sent):
    replacements = {
        r"\b(went)\b": "go",
        r"\b(has|have|had) [a-z]+ed\b": lambda m: m.group(0).split()[0] + " " + m.group(0).split()[1][:-2],  # crude
        r"\b(was|were|is|are|will)\b": "be"
    }
    for pattern, repl in replacements.items():
        sent = re.sub(pattern, repl, sent)
    return sent

def corrupt_wh_question(sent):
    # Basic flip: "What is she doing?" → "What she is doing?"
    sent = re.sub(r"\b(what|who|why|where|how|when)\s+(is|are|was|were|do|does|did|will|has|have|had)\s+(\w+)\b", r"\1 \3 \2", sent, flags=re.I)
    return sent

def asr_contraction_noise(sentence: str) -> str:
    """
    Randomly replaces some contractions with expanded forms or vice versa.
    Simulates ASR handling of contractions.
    """
    original = sentence

    # Randomly decide whether to expand or contract
    if random.random() < 0.5:
        # Expand contractions
        for contraction, expansion in CONTRACTION_MAP.items():
            pattern = re.compile(rf"\b{re.escape(contraction)}\b", flags=re.IGNORECASE)
            sentence = pattern.sub(lambda m: expansion, sentence)
    else:
        # Contract expanded forms
        for expansion, contraction in EXPANSION_MAP.items():
            pattern = re.compile(rf"\b{re.escape(expansion)}\b", flags=re.IGNORECASE)
            sentence = pattern.sub(lambda m: contraction, sentence)

    return sentence if sentence != original else original

def asr_article_noise(sentence: str) -> str:
    """
    Randomly drops or adds common English articles (a, an, the).
    Simulates ASR errors involving article misinterpretation.
    """
    original = sentence

    words = sentence.split()
    modified = False

    # 50% chance to drop existing articles
    if random.random() < 0.5:
        new_words = []
        for word in words:
            if word.lower() in ARTICLES and random.random() < 0.5:
                modified = True
                continue  # Drop the article
            new_words.append(word)
        sentence = " ".join(new_words)
    else:
        # 50% chance to insert extra articles
        insert_positions = random.sample(range(len(words)), k=min(2, len(words)))  # max 2 insertions
        for idx in sorted(insert_positions, reverse=True):
            if words[idx].lower() not in ARTICLES:
                article = random.choice(ARTICLES)
                words.insert(idx, article)
                modified = True
        sentence = " ".join(words)

    return sentence if modified else original

def asr_preposition_noise(sentence: str) -> str:
    """
    Introduces ASR-like preposition errors by randomly dropping or replacing prepositions.
    """
    words = sentence.split()
    modified = False

    for i, word in enumerate(words):
        word_lower = word.lower()
        if word_lower in PREPOSITIONS:
            rand_val = random.random()
            if rand_val < 0.4:
                # Drop the preposition
                words[i] = ""
                modified = True
            elif rand_val < 0.8 and word_lower in PREPOSITION_CONFUSIONS:
                # Replace with a confused one
                replacement = random.choice(PREPOSITION_CONFUSIONS[word_lower])
                words[i] = replacement
                modified = True

    sentence = " ".join(w for w in words if w)  # clean up dropped words
    return sentence if modified else sentence

def asr_pronoun_substitution(sentence: str) -> str:
    """
    Simulates ASR errors by replacing pronouns with common misrecognized counterparts.
    """
    words = sentence.split()
    modified = False

    for i, word in enumerate(words):
        lower = word.lower()
        if lower in PRONOUN_CONFUSIONS and random.random() < 0.6:
            replacement = random.choice(PRONOUN_CONFUSIONS[lower])
            # preserve case
            words[i] = replacement.capitalize() if word[0].isupper() else replacement
            modified = True

    return " ".join(words) if modified else sentence

def duplicate_random_word(sentence: str) -> str:
    words = sentence.split()
    if len(words) < 2: return sentence
    idx = random.randint(0, len(words)-1)
    words.insert(idx, words[idx])
    return " ".join(words)