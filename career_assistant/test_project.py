import pytest
from career_assistant.extract_cv import extract_text_from_pdf
from career_assistant.skill_extractor import analyze_skills_from_cv
from career_assistant.roadmap_generator import generate_roadmap

# Test pdf Reader
def test_extract_text():
    text = extract_text_from_pdf("MyResume.pdf")
    assert isinstance(text, str)
    assert len(text) > 10  # Check If the text not empty


# Test skills Analysis
def test_analyze_skills():
    result = analyze_skills_from_cv("MyResume.pdf")
    assert "skills_found" in result
    assert "skills_missing" in result


# Test roadmap generatore
def test_generate_roadmap():
    missing = ["Django", "Machine Learning"]
    roadmap = generate_roadmap(missing)
    assert isinstance(roadmap, list)
    assert roadmap[0]["skill"] in missing
