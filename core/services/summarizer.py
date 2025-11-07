from transformers import pipeline
import os

# Best practice: load models once at module import.
# If you prefer lighter models, switch to 't5-small' or use the HF Inference API.

HF_SUMMARIZER_MODEL = os.getenv('HF_SUMMARIZER_MODEL', 'facebook/bart-large-cnn')


try:
    summarizer = pipeline('summarization', model=HF_SUMMARIZER_MODEL)
except Exception as e:
# Fallback to None. In production you'd want to log and perhaps use remote inference.
    summarizer = None

def generate_summary(text: str) -> str:
    """Safely summarize text with fallback and chunk handling."""
    if not text or not text.strip():
        return ""

    try:
        # 🔹 HuggingFace models have token limits (usually 1024)
        # So we ensure we don’t pass huge chunks
        if len(text.split()) > 400:
            text = " ".join(text.split()[:400])

        result = summarizer(
            text,
            max_length=150,
            min_length=40,
            do_sample=False,
        )

        # Handle output list safely
        if result and isinstance(result, list) and len(result) > 0:
            return result[0].get("summary_text", "").strip()

    except Exception as e:
        print(f"[WARN] Summarization failed: {e}")
        return text[:400] + "..."  # fallback partial text

    return ""
