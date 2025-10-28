def chunk_text(text: str, max_words: int = 450):
    """Splits text into chunks on sentence boundaries to improve coherence."""
    words = text.split()
    chunks, current = [], []

    for word in words:
        current.append(word)
        if len(current) >= max_words:
            joined = " ".join(current)
            if "." in joined:
                cutoff = joined.rfind(".") + 1
                chunks.append(joined[:cutoff].strip())
                leftover = joined[cutoff:].strip()
                current = leftover.split() if leftover else []
            else:
                chunks.append(joined.strip())
                current = []
    if current:
        chunks.append(" ".join(current).strip())
    return chunks
