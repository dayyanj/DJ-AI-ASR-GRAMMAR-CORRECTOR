import torch
import gc
from transformers import (
    T5Tokenizer, T5ForConditionalGeneration,
    Seq2SeqTrainer, Seq2SeqTrainingArguments,
    DataCollatorForSeq2Seq, EarlyStoppingCallback
)
from datasets import load_from_disk
from .config import DATASET_DIR, CHECKPOINT_DIR, TRAIN_BATCH, EVAL_BATCH, EPOCHS, STRATEGY, LOG_STEPS, SAVE_LIMIT, VARIANTS
import os

DATASET_PATH = DATASET_DIR
dataset = load_from_disk(DATASET_PATH)

# Tokenization functions
def tokenize(batch):
    return tokenizer(batch["input"], padding="max_length", truncation=True, max_length=128)

def tokenize_labels(batch):
    batch["labels"] = tokenizer(batch["target"], padding="max_length", truncation=True, max_length=128)["input_ids"]
    return batch

# Models to train
t5_variants = VARIANTS

for variant in t5_variants:
    print(f"\n Training model: {variant}")

    output_dir = f"{CHECKPOINT_DIR}/grammar_corrector_{variant.split('-')[-1]}"
    checkpoint_path = os.path.join(output_dir, "checkpoint-last")
    
    tokenizer = T5Tokenizer.from_pretrained(variant)
    model = T5ForConditionalGeneration.from_pretrained(variant)

    tokenized = dataset.map(tokenize, batched=True).map(tokenize_labels, batched=True)

    args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=TRAIN_BATCH,
        per_device_eval_batch_size=EVAL_BATCH,
        num_train_epochs=EPOCHS,
        eval_strategy=STRATEGY,
        logging_steps=LOG_STEPS,
        save_strategy=STRATEGY,
        save_total_limit=SAVE_LIMIT,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        fp16=False,
        predict_with_generate=True,
        save_safetensors=True,
        overwrite_output_dir=True,
        resume_from_checkpoint=checkpoint_path if os.path.exists(checkpoint_path) else None,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    trainer.train()
    print(f"Finished training {variant}. Best model saved to {output_dir}")

    # Cleanup to avoid memory leaks
    del model, tokenizer, trainer, args
    gc.collect()
    torch.cuda.empty_cache()
