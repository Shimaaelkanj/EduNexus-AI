from transformers import pipeline
import os


HF_SIMPLIFIER_MODEL = os.getenv('HF_SIMPLIFIER_MODEL', 't5-small')


try:
    rephraser = pipeline('text2text-generation', model=HF_SIMPLIFIER_MODEL)
except Exception:
    rephraser = None




def simplify_text(text: str, max_length: int = 80) -> str:
    if not text or not rephraser:
        return ''
    prompt = f"simplify: {text}"
    output = rephraser(prompt, max_length=max_length)
    return output[0]['generated_text']