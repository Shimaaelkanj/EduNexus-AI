from transformers import pipeline
import textwrap
import re
import nltk

# Make sure nltk sentence tokenizer is available
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Load summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Load text
with open("long_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Loaded text from long_text.txt\n")

# Step 1: Chunking for long texts (>500 chars)
CHUNK_SIZE = 500
chunks = textwrap.wrap(text, CHUNK_SIZE) if len(text) > CHUNK_SIZE else [text]

# Step 2: Summarize each chunk
chunk_summaries = []
for i, chunk in enumerate(chunks, 1):
    summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
    clean_summary = re.sub(r'\s+', ' ', summary[0]['summary_text']).strip()
    chunk_summaries.append(clean_summary)
    print(f"Chunk {i} Summary:", clean_summary, "\n")

# Step 3: Combine chunk summaries
combined_text = " ".join(chunk_summaries)

# Step 4: Split combined text into sentences
sentences = sent_tokenize(combined_text)

# Step 5: Re-join into a text with shorter sentences for polishing
short_text = " ".join(sentences)

# Step 6: Final summarization (polishing)
final_summary = summarizer(
    combined_text,
    max_length=400,  # increase to capture all points
    min_length=150,
    do_sample=False
)

# Step 7: Final cleanup
polished_summary = re.sub(r'\s+', ' ', final_summary[0]['summary_text']).strip()

print("\n--- Polished Final Summary ---")
print(polished_summary)
