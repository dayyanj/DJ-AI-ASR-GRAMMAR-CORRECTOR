from grammar_corrector.model_loader import load_model_and_tokenizer
from grammar_corrector.corrector import correct_batch

def main():
    model, tokenizer = load_model_and_tokenizer()

    noisy_sentences = [
        "she go to school every day",
        "i seen him yesterday",
        "they was happy with their decision",
        "me and him is working together"
    ]

    print("\n🧪 Batch Correction\n----------------------")
    corrected = correct_batch(model, tokenizer, noisy_sentences)
    for orig, clean in zip(noisy_sentences, corrected):
        print(f"\nInput     : {orig}\nCorrected : {clean}")

if __name__ == "__main__":
    main()
