# ASR Grammar Corrector

A post-ASR correction model designed to fix typical speech recognition errors in (near) real-time. It helps clean up transcriptions from ASR systems like Whisper, Nemo etc, improving readability and grammatical correctness with minimal latency.

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

## Pretrained Models
Models have been trained on DJ-AI Custom Dataset which includes over 90 million real and synthetic ASR errors and corrected texts pairs. The models are based on T5 pretrained models.

SMALL | https://huggingface.co/dayyanj/dj-ai-asr-grammar-corrector-t5-small
BASE  | COMIMG SOON

MIT License.
