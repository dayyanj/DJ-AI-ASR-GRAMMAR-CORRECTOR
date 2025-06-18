from grammar_corrector.model_loader import load_model_and_tokenizer
from grammar_corrector.corrector import correct_grammar

def main():
    model, tokenizer = load_model_and_tokenizer()
    print("Grammar Correction Test Interface")
    while True:
        try:
            text = input("\nNoisy Input > ").strip()
            if not text:
                break
            corrected = correct_grammar(model, tokenizer, text)
            print("Corrected   >", corrected)
        except KeyboardInterrupt:
            print("\n Exiting.")
            break

if __name__ == "__main__":
    main()
