import re


def skill_exists(resume_text, skill):
    resume_text = resume_text.lower()
    skill = skill.lower()

    # Git should not match GitHub
    if skill == "git":
        return re.search(r"(?<!hub)\bgit\b", resume_text) is not None

    # Handle related terms
    aliases = {
        "vector database": ["vector database", "vector databases", "chromadb"],
        "llm api": ["llm api", "llm apis", "gemini api"],
        "generative ai": ["generative ai", "genai"],
    }

    terms = aliases.get(skill, [skill])

    return any(
        re.search(r"\b" + re.escape(term) + r"\b", resume_text)
        for term in terms
    )


def calculate_match_score(resume_text):

    categories = {
        "core_ai": {
            "weight": 40,
            "skills": [
                "generative ai",
                "rag",
                "llm applications",
                "llm api",
                "vector database",
                "embeddings",
                "prompt engineering",
                "semantic search",
            ],
        },

        "backend": {
            "weight": 25,
            "skills": [
                "python",
                "fastapi",
                "flask",
                "php",
                "rest api",
            ],
        },

        "database": {
            "weight": 15,
            "skills": [
                "sql",
                "mysql",
                "mongodb",
                "chromadb",
            ],
        },

        "tools": {
            "weight": 10,
            "skills": [
                "git",
                "docker",
                "linux",
            ],
        },

        "cloud": {
            "weight": 10,
            "skills": [
                "aws",
                "hugging face",
            ],
        },
    }

    total_score = 0

    for category in categories.values():

        skills = category["skills"]

        matched = sum(
            skill_exists(resume_text, skill)
            for skill in skills
        )

        category_score = (
            matched / len(skills)
        ) * category["weight"]

        total_score += category_score

    return round(total_score, 2)