"""roadmap_generator.py
Produce a simple learning roadmap based on missing skills.
Reads `resources.json` co-located with this file.
"""
import json
import os

DEFAULT_DURATION = 4

def load_resources(path="resources.json"):
    """Load resources.json located next to this module."""
    base = os.path.dirname(__file__)
    full = os.path.join(base, path)
    with open(full, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_roadmap(skills_missing):
    """Return a list of roadmap entries for each missing skill."""
    resources = load_resources()
    roadmap = []

    for skill in skills_missing:
        if skill in resources:
            roadmap.append({
                "skill": skill,
                "duration_weeks": resources[skill]["duration_weeks"],
                "resources": resources[skill]["resources"]
            })
        else:
            roadmap.append({
                "skill": skill,
                "duration_weeks": DEFAULT_DURATION,
                "resources": [{"type": "search", "title": f"Search online for {skill} tutorials"}]
            })
    return roadmap


if __name__ == "__main__":
    missing = ["Django", "Machine Learning"]
    roadmap = generate_roadmap(missing)
    print(json.dumps(roadmap, indent=2, ensure_ascii=False))
