import os
import glob
import re
import unicodedata
from ..config import MY_SOURCE_DIR, CLEAN_DIR, MAX_WORDS, MIN_WORDS

def clean_for_asr(text: str) -> str:
    # 1. Remove leading numbers and punctuation
    text = re.sub(r'^\s*\d+[\.\)\-:]\s*', '', text)

    # 2. Remove quotation marks and smart quotes
    text = text.replace('"', '').replace("'", "")
    text = text.translate(str.maketrans({"“": "", "”": "", "‘": "", "’": ""}))

    # 3. Normalize to ASCII
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()

    # 4. Remove non-ASR punctuation and special characters
    text = re.sub(r'[^\w\s,.?!]', '', text)

    # 5. Remove trailing repeated punctuation like !!! or ...
    text = re.sub(r'([!?])\1+', r'\1', text)         # collapse !!! → !
    text = re.sub(r'(\.\s*){2,}', '.', text)         # . . . → .
    text = re.sub(r'\s+\.', '.', text)               # space before period → period

    # 6. Remove ending fragments (e.g., "Continue Reading", or text ending in partial words)
    text = re.sub(r'(Continue Reading.*|Read More.*|\.?\s*(blog|site|Jun \d{1,2}, \d{4})\.?)$', '', text, flags=re.IGNORECASE)

    # 7. Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # 8. Strip out hyperlinks/hashtags etc
    text = re.sub(r'@\w+|#\w+|https?://\S+|\S+@\S+', '', text)

    return text


def split_into_sentences(text: str):
    # Very simple sentence splitter
    return re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)


# Input/output directories
SOURCE_DIR = MY_SOURCE_DIR
OUTPUT_DIR = CLEAN_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

tsv_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.txt")))

for file_path in tsv_files:
    filename = os.path.basename(file_path)
    index = filename.split("-")[1]
    output_path = os.path.join(OUTPUT_DIR, f"clean_chunk_{index}.txt")

    print(f"Processing {filename} → clean_chunk_{index}.txt")

    with open(file_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            clean = line.strip()
            if not clean:
                continue

            clean = clean_for_asr(clean)
            sentences = split_into_sentences(clean)

            for sent in sentences:
                word_count = len(sent.split())
                if MIN_WORDS <= word_count <= MAX_WORDS:
                    fout.write(sent.strip() + "\n")
