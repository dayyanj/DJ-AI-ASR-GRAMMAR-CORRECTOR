import os
import random
import re
import multiprocessing
from ..config import CLEAN_DIR, NOISY_PAIRS_DIR, SKIPPED_DIR

from noise_functions import (
    homophone_mistake,
    break_subject_verb_agreement,
    drop_auxiliaries,
    corrupt_verb_tense,
    corrupt_wh_question,
    asr_contraction_noise,
    asr_article_noise,
    asr_preposition_noise,
    asr_pronoun_substitution,
    duplicate_random_word,
)

clean_dir = CLEAN_DIR
output_dir = NOISY_PAIRS_DIR
unchanged_dir = SKIPPED_DIR

os.makedirs(output_dir, exist_ok=True)
os.makedirs(unchanged_dir, exist_ok=True)

noise_functions = [
    homophone_mistake,
    break_subject_verb_agreement,
    drop_auxiliaries,
    corrupt_verb_tense,
    corrupt_wh_question,
    asr_contraction_noise,
    asr_article_noise,
    asr_preposition_noise,
    asr_pronoun_substitution,
    duplicate_random_word,
]

def apply_noise(clean):
    noisy = clean
    if random.random() < 0.2:
        noisy = random.choice(noise_functions)(noisy)
    else:
        for fn in random.sample(noise_functions, k=random.randint(2, 4)):
            noisy = fn(noisy)
    return noisy

def process_file(file_idx_filename):
    file_idx, filename = file_idx_filename
    file_path = os.path.join(clean_dir, filename)

    output_path = os.path.join(output_dir, f"noisy_pairs_chunk_{file_idx:02d}.tsv")
    unchanged_path = os.path.join(unchanged_dir, f"skipped_chunk_{file_idx:02d}.txt")

    with open(file_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout_all, \
         open(unchanged_path, "w", encoding="utf-8") as fout_unchanged:

        for line in fin:
            clean = line.strip()
            if not clean:
                continue

            noisy = apply_noise(clean)

            if noisy != clean:
                noisy_lower = re.sub(r"\s+", " ", noisy.lower().strip())
                fout_all.write(f"{noisy_lower}\t{clean}\n")
            else:
                fout_unchanged.write(clean + "\n")


if __name__ == "__main__":
    all_files = sorted(os.listdir(clean_dir))
    file_args = list(enumerate(all_files))

    num_workers = min(multiprocessing.cpu_count(), len(all_files))
    print(f"⏱ Launching {num_workers} worker processes...")

    with multiprocessing.Pool(num_workers) as pool:
        pool.map(process_file, file_args)

    print("✅ Done generating noisy pairs in chunks.")
