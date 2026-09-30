import re


SKILL_ALIASES = {
    "vector databases": ["vector databases", "vector database", "chromadb"],
    "llm powered applications": [
        "llm-powered applications",
        "llm applications",
        "llm application"
    ],
    "llm apis": [
        "llm apis",
        "llm api",
        "gemini api"
    ],
    "ai agents": [
        "ai agents",
        "agentic ai"
    ]
}


def normalize_text(text):
    text = text.lower()
    text = text.replace("-", " ")
    return text


def check_skill(skill, resume_text):
    resume_text = normalize_text(resume_text)
    skill = normalize_text(skill)

    # Git should NOT match GitHub
    if skill == "git":
        return re.search(r"(?<!hub)\bgit\b", resume_text) is not None

    terms = SKILL_ALIASES.get(skill, [skill])
    terms = [normalize_text(term) for term in terms]

    for term in terms:
        term = normalize_text(term)

        pattern = r"\b" + re.escape(term) + r"\b"

        if re.search(pattern, resume_text):
            return True

    return False


def match_skills(required_skills, resume_text):
    matching_skills = []
    missing_skills = []

    for skill in required_skills:
        if check_skill(skill, resume_text):
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    return matching_skills, missing_skills