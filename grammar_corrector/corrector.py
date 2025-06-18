import torch
from typing import List, Union

def correct_grammar(
    model,
    tokenizer,
    text: str,
    max_new_tokens: int = 50,
    return_tokens: bool = False
) -> Union[str, List[str]]:
    """
    Corrects a single sentence.
    """
    inputs = tokenizer(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    if return_tokens:
        return tokenizer.convert_ids_to_tokens(outputs[0])
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def correct_batch(
    model,
    tokenizer,
    texts: List[str],
    max_new_tokens: int = 50
) -> List[str]:
    """
    Corrects a batch of sentences. Useful for post-processing ASR output.
    """
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to("cuda")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]

def correct_stream(
    model,
    tokenizer,
    stream: List[str],
    buffer_size: int = 3,
    overlap: int = 1,
    max_new_tokens: int = 50
) -> List[str]:
    """
    Simulates streaming ASR correction using a sliding window over stream chunks.

    Parameters:
    - stream: A list of ASR chunk strings.
    - buffer_size: Number of chunks per window.
    - overlap: How many chunks to reuse between windows.
    """
    corrected = []
    i = 0
    while i < len(stream):
        window = stream[i:i+buffer_size]
        joined_text = " ".join(window)
        cleaned = correct_grammar(model, tokenizer, joined_text, max_new_tokens)
        corrected.append(cleaned)
        i += buffer_size - overlap  # slide window
    return corrected
