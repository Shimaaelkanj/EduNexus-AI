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
import re
def split_by_sentences(text: str) -> list:
    """Splits text into sentences using regex for better accuracy."""
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text.strip())
    return [s.strip() for s in sentences if s.strip()]
def chunk_text_by_words(text: str, max_words: int = 450) -> list:
    """Splits text into chunks based on a maximum word count."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)
    return chunks
def chunk_text_by_sentences(text: str, max_sentences: int = 5) -> list:
    """Splits text into chunks based on a maximum number of sentences."""
    sentences = split_by_sentences(text)
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences])
        chunks.append(chunk)
    return chunks