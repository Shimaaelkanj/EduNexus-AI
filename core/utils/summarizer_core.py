import asyncio
from transformers import pipeline

# Load model globally once for all APIs (fast, memory-safe)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

async def async_summarize(prompt: str, max_length: int = 150, min_length: int = 50) -> str:
    """Async summarization wrapper for concurrency."""
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            None,
            lambda: summarizer(
                prompt,
                max_length=max_length,
                min_length=min_length,
                truncation=True,
                do_sample=False,
            ),
        )
        return result[0].get("summary_text", "").strip()
    except Exception as e:
        print(f"[Summarizer Error] {e}")
        return ""
