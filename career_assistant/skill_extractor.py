# career_assistant/skill_extractor.py
import os
import json
import re
from rapidfuzz import fuzz, process
from career_assistant.extract_cv import extract_text_from_pdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_PATH = os.path.join(BASE_DIR, "career_assistant", "resources.json")
#Load skills from cv
def load_skills():
    try:
        with open(RESOURCES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "skills" in data:
            return data["skills"]
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return list(data.keys())
    except Exception as e:
        print("⚠️ load_skills error:", e)
    return []
#Clean the text
def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s+#\.\-]", " ", text)  # keep letters, numbers, +, #, ., -
    text = re.sub(r"\s+", " ", text).strip()
    return text
#Upload the skills with more than one word
def generate_ngrams(tokens, max_n=5):
    ngrams = []
    n_tokens = len(tokens)
    for n in range(1, max_n+1):
        for i in range(0, n_tokens - n + 1):
            ngram = " ".join(tokens[i:i+n])
            ngrams.append(ngram)
    return ngrams
#Detect skills
def detect_skills(text, skills_list, fuzzy_threshold=60):
    if not text:
        return []

    norm_text = normalize_text(text)
    tokens = norm_text.split()
    if not tokens:
        return []

    skills_norm = [(skill, skill.lower()) for skill in skills_list if isinstance(skill, str) and skill.strip()]
    found = set()

    # exact match
    for skill, s_norm in skills_norm:
        pattern = r"\b" + re.escape(s_norm) + r"\b"
        if re.search(pattern, norm_text):
            found.add(skill)

    # fuzzy match on ngrams
    max_skill_len = max((len(s.split()) for _, s in skills_norm), default=1)
    max_n = min(max_skill_len + 2, 6)
    ngrams = generate_ngrams(tokens, max_n=max_n)
    ngrams_unique = list(dict.fromkeys(ngrams))

    norm_to_orig = {}
    for orig, s_norm in skills_norm:
        norm_to_orig.setdefault(s_norm, []).append(orig)

    skill_norm_keys = list(norm_to_orig.keys())

    for ngram in ngrams_unique:
        matches = process.extract(ngram, skill_norm_keys, scorer=fuzz.token_sort_ratio, limit=5)
        for match_key, score, _ in matches:
            if score >= fuzzy_threshold:
                for orig_skill in norm_to_orig.get(match_key, []):
                    found.add(orig_skill)

    return sorted(found)

def analyze_skills_from_cv(file_path, fuzzy_threshold=60):
    text = ""
    try:
        text = extract_text_from_pdf(file_path) or ""
    except Exception as e:
        print("⚠️ extract_text_from_pdf error:", e)
        text = ""

    skills_master = load_skills()
    if not skills_master:
        return {"filename": os.path.basename(file_path), "skills_found": [], "skills_missing": [], "roadmap": [], "error": "no skills list"}

    skills_found = detect_skills(text, skills_master, fuzzy_threshold=fuzzy_threshold)
    skills_missing = [s for s in skills_master if s not in skills_found]

    roadmap = [{"skill": s, "duration_weeks": 4, "resources": []} for s in skills_missing]

    return {
        "filename": os.path.basename(file_path),
        "skills_found": skills_found,
        "skills_missing": skills_missing,
        "roadmap": roadmap
    }

if __name__ == "__main__":
    cv_path = "MyResume.pdf"
    print(analyze_skills_from_cv(cv_path))
