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


## Installation

```bash
git clone https://github.com/<your_username>/asr_grammar_corrector.git
cd asr_grammar_corrector
pip install -r requirements.txt

## Contributions

If you want to fine-tune this model on your own data or improve the logic, feel free to open issues or PRs.

## License

MIT License.