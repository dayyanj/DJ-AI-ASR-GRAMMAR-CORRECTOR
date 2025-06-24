# ASR Grammar Corrector

A post-ASR correction model trained on 90 million noisy / clean pairs, designed to fix typical speech recognition errors in (near) real-time. It helps clean up transcriptions from ASR systems like Whisper, Nemo etc, improving readability and grammatical correctness with minimal latency.

Designed to:
Improve readability and professionalism in transcripts
Make ASR outputs usable for customer service, legal, and healthcare
Helping non-native speakers interpret ASR more easily
Supports real-time captioning and assistive technologies

---

## Features

- Fixes common ASR issues:
  - Homophones (e.g., “their” vs “there”)
  - Subject-verb agreement
  - Verb tense errors
  - Missing auxiliaries and articles
  - Contractions and prepositions
  - Pronoun misuse
  - Repeated or corrupted words

- Fast inference (<50ms on GPU)
- Easy to plug into real-time ASR pipelines
- HuggingFace-compatible model loading

---

license: mit
language:
- en
base_model:
- google-t5/t5-small
pipeline_tag: text2text-generation
tags:
- ASR,

---

# DJ-AI ASR Grammar Corrector

A lightweight grammar correction model fine-tuned from `t5-small` and `t5-base`, specifically designed to correct common errors in **automatic speech recognition (ASR)** outputs — including homophones, verb tense issues, contractions, duplicated words, and more. Optimized for **fast inference** in (near) real-time ASR pipelines.

---

## Model Details

- **Small model**: [`t5-small`](https://huggingface.co/t5-small)
- **Base model**: [`t5-base`](https://huggingface.co/t5-base)
- **Fine-tuned on**: 90 million synthetic (noisy → clean) sentence pairs
- **Training objective**: Correct ASR-style transcription errors into clean, grammatical English
- **Framework**: Hugging Face Transformers + PyTorch

---

## Benchmark Results (10,000 real world noisy inputs used in benchmarking)
| Model                                | Type | Precision | Latency (s/sample) | VRAM (MB) | BLEU  | ROUGE-L | Accuracy (%)¹ | Token Accuracy (%)² | Size (MB) |
|--------------------------------------|------|-----------|--------------------|-----------|-------|---------|----------------|----------------------|-----------|
| [dj-ai-asr-grammar-corrector-t5-base](https://huggingface.co/dayyanj/dj-ai-asr-grammar-corrector-base) | HF   | fp32      | 0.1151             | 24.98     | 78.92 | 90.31   | 44.62          | 90.39                | 5956.76   |
| [dj-ai-asr-grammar-corrector-t5-small](https://huggingface.co/dayyanj/dj-ai-asr-grammar-corrector-small) | HF   | fp32      | 0.0648             | 6.27      | 76.47 | 89.54   | 39.59          | 88.76                | 1620.15   |
| [dj-ai-asr-grammar-corrector-t5-small-streaming](https://huggingface.co/dayyanj/dj-ai-asr-grammar-corrector-small-streaming) | HF   | fp32      | 0.0634             | 14.77      | 76.25 | 89.61   | 39.90          | 88.54                | 1620.65   |


1. Accuracy is a measure of how well the model performs across the full sentence. That is, a prediction is only counted as "correct" if the entire corrected sentence exactly matches the reference sentence. So if the model corrects 1 out of 2 errors, but the final output does not exactly match the expected sentence, it's counted as a fail.
2. Token Accuracy is a measure of how well the model performs at the token level.
$$\text{Token Accuracy (\%)} = \left( \frac{\text{Number of Matched Tokens}}{\text{Total Reference Tokens}} \right) \times 100$$



## Intended Use

| Use Case | ✅ Supported | 🚫 Not Recommended |
|----------|--------------|--------------------|
| Post-ASR correction | ✅ Yes |  |
| Real-time ASR pipelines | ✅ Yes |  |
| Batch transcript cleanup | ✅ Yes |  |
| Grammar education tools | ✅ Yes |  |
| Formal document editing | 🚫 | Model may be too informal |
| Multilingual input | 🚫 | English-only fine-tuning |

---

## Corrects Common ASR Errors:

- Homophone mistakes (`their` → `they're`)
- Subject-verb disagreement (`he go` → `he goes`)
- Verb tense corruption (`i seen` → `i saw`)
- Missing auxiliaries (`you going` → `are you going`)
- Contraction normalization (`she is not` → `she isn't`)
- Repeated words (`i i want` → `i want`)
- Misused articles/prepositions/pronouns

---

## Example

**Input (noisy ASR)**:

## Pretrained Models
Models have been trained on DJ-AI Custom Dataset which includes over 90 million real and synthetic ASR errors and corrected texts pairs. The models are based on T5 pretrained models.

https://huggingface.co/dayyanj/dj-ai-asr-grammar-corrector-small

https://huggingface.co/dayyanj/dj-ai-asr-grammar-corrector-small-streaming

https://huggingface.co/dayyanj/dj-ai-asr-grammar-corrector-base



## Demo
DEMO: https://huggingface.co/spaces/dayyanj/dj-ai-asr-grammar-corrector-demo


MIT License.
