from grammar_corrector.model_loader import load_model_and_tokenizer
from grammar_corrector.corrector import correct_stream

def main():
    model, tokenizer = load_model_and_tokenizer()

    # Simulated ASR output chunks from a real-time transcript
    stream_chunks = [
        "i think we", "should go to", "the park because", 
        "its nice out", "and there is", "plenty of space", 
        "to run around", "and play with", "the kids"
    ]

    print("\nStream Correction (Sliding Window)\n-----------------------------------")
    corrected_windows = correct_stream(
        model, tokenizer, stream_chunks, buffer_size=3, overlap=1
    )

    for i, corrected in enumerate(corrected_windows):
        print(f"\nWindow {i+1}:")
        print(f"Corrected : {corrected}")

if __name__ == "__main__":
    main()
