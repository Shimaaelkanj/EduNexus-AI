from ..utils.chunking import split_by_sentences

def generate_outline_simple(text: str, max_points: int = 6) -> list:
    """
    Simple rule-based outline generator:
    - Split text into sentences
    - Score sentences by length and presence of keywords
    - Return top N sentences as bullets (trimmed)
    """
    if not text:
        return []
    sentences = split_by_sentences(text)
    # naive scoring by length and position
    scored = []
    for i, s in enumerate(sentences):
        score = len(s.split()) + max(0, 10 - i) # prefer earlier sentences
        scored.append((score, s))
    scored.sort(reverse=True, key=lambda x: x[0])
    bullets = [s.strip() for _, s in scored[:max_points]]
    return bullets