"""
Member 3 - Week 1 Deliverable
Task: Extract 3 keywords from input text (supports long articles from .txt file)
Approaches: 
  1. HuggingFace (KeyBERT-based, ML)
  2. Rule-based (NLTK, frequency analysis)
"""

from keybert import KeyBERT
import nltk
from collections import Counter
import string
import os

# -------------------------------
# Setup for NLTK (only first run)
# -------------------------------
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

# -------------------------------
# 1. HuggingFace / KeyBERT method
# -------------------------------
kw_model = KeyBERT()

def extract_keywords_keybert(text, num_keywords=10):
    keywords = kw_model.extract_keywords(text, top_n=num_keywords)
    return [kw[0] for kw in keywords]

# -------------------------------
# 2. Rule-based method (NLTK)
# -------------------------------
def extract_keywords_rule_based(text, num_keywords=10):
    words = nltk.word_tokenize(text.lower())
    words = [w for w in words if w.isalpha()]  # keep words only
    stop_words = set(stopwords.words("english"))
    filtered = [w for w in words if w not in stop_words]
    most_common = Counter(filtered).most_common(num_keywords)
    return [word for word, _ in most_common]

# -------------------------------
# Main script
# -------------------------------
if __name__ == "__main__":
    # Load article from file
    file_path = "long_text.txt"  # change if needed
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            sample_text = f.read()
    else:
        sample_text = input("Enter text: ")

    print("\n--- Keyword Extraction Results ---")
    print("Text loaded from file (first 300 chars):")
    print(sample_text[:300] + ("..." if len(sample_text) > 300 else ""))

    # Method 1: KeyBERT (HuggingFace-based)
    try:
        keybert_keywords = extract_keywords_keybert(sample_text)
        print("\nKeyBERT Keywords:", keybert_keywords)
    except Exception as e:
        print("\nKeyBERT failed (check transformers & sentence-transformers). Error:", e)

    # Method 2: Rule-based
    rule_based_keywords = extract_keywords_rule_based(sample_text)
    print("Rule-based Keywords:", rule_based_keywords)
