import os
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from ..config import CHECKPOINT_DIR

BASE_CHECKPOINT_DIR = CHECKPOINT_DIR

def get_latest_checkpoint(base_dir: str) -> str:
    checkpoints = [d for d in os.listdir(base_dir) if d.startswith("checkpoint-")]
    checkpoints = sorted(checkpoints, key=lambda x: int(x.split("-")[1]))
    if not checkpoints:
        raise FileNotFoundError("No checkpoints found in directory.")
    return os.path.join(base_dir, checkpoints[-1])

def load_model_and_tokenizer(base_dir: str = BASE_CHECKPOINT_DIR):
    ckpt_path = get_latest_checkpoint(base_dir)
    print(f"Loading checkpoint from: {ckpt_path}")
    model = T5ForConditionalGeneration.from_pretrained(ckpt_path)
    tokenizer = T5Tokenizer.from_pretrained(ckpt_path)
    model.eval().cuda()
    return model, tokenizer
