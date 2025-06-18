import os
import glob
import pandas as pd
from datasets import Dataset, concatenate_datasets, DatasetDict
from tqdm import tqdm
import multiprocessing as mp
from ..config import NOISY_PAIRS_DIR, DATASET_DIR, CHUNK_SIZE

CHUNKS_DIR = NOISY_PAIRS_DIR

def process_file(file_path):
    """
    Load a TSV file in chunks and return a list of HuggingFace Datasets.
    """
    datasets = []
    with open(file_path, "r", encoding="utf-8") as f:
        batch = []
        for i, line in enumerate(f):
            parts = line.strip().split("\t")
            if len(parts) != 2:
                continue
            noisy, clean = parts
            batch.append({"input": noisy, "target": clean})
            if len(batch) >= CHUNK_SIZE:
                datasets.append(Dataset.from_pandas(pd.DataFrame(batch)))
                batch = []
        if batch:
            datasets.append(Dataset.from_pandas(pd.DataFrame(batch)))
    return datasets

def build_dataset_parallel(tsv_files):
    """
    Build full dataset from multiple .tsv files using multiprocessing.
    """
    all_datasets = []
    with mp.Pool(processes=os.cpu_count()) as pool:
        for file_datasets in tqdm(pool.imap_unordered(process_file, tsv_files), total=len(tsv_files)):
            all_datasets.extend(file_datasets)
    return concatenate_datasets(all_datasets)

def main():
    print("Scanning .tsv files...")
    tsv_files = sorted(glob.glob(os.path.join(CHUNKS_DIR, "*.tsv")))
    print(f"Found {len(tsv_files)} files")

    print("Building dataset...")
    full_dataset = build_dataset_parallel(tsv_files)

    print("Splitting into train/test...")
    dataset = full_dataset.train_test_split(test_size=0.05, seed=42)

    print("Saving to disk...")
    dataset.save_to_disk(DATASET_DIR)

    print(f"Done. Dataset saved to {DATASET_DIR}\nYour data is now ready for training")

if __name__ == "__main__":
    main()
