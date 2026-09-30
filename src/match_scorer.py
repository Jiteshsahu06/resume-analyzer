def calculate_weighted_score(resume_text, matching_skills):
    resume_text = resume_text.lower()

    categories = {
        "core_ai": {
            "weight": 40,
            "groups": [
                ["generative ai", "genai"],
                ["rag", "rag pipelines"],
                ["llm applications", "llm-powered applications"],
                ["embeddings"],
                ["vector database", "vector databases", "chromadb"],
                ["llm api", "llm apis", "gemini api"],
                ["prompt engineering"],
                ["semantic search"],
            ],
        },

        "backend": {
            "weight": 25,
            "groups": [
                ["python"],
                ["fastapi", "flask"],
                ["rest api", "rest apis"],
                ["php"],
                ["codeigniter", "codeigniter 3", "ci3"],
            ],
        },

        "database": {
            "weight": 15,
            "groups": [
                ["sql"],
                ["mysql"],
                ["mongodb"],
            ],
        },

        "tools_and_devops": {
            "weight": 10,
            "groups": [
                ["git"],
                ["docker"],
                ["linux"],
            ],
        },

        "cloud_and_ai_tools": {
            "weight": 10,
            "groups": [
                ["aws"],
                ["hugging face", "huggingface"],
                ["langsmith"],
                ["langfuse"],
            ],
        },
    }

    total_score = 0

    for category in categories.values():

        groups = category["groups"]
        matched = 0

        for group in groups:
            if any(
                term in resume_text
                for term in group
            ):
                matched += 1

        category_score = (
            matched / len(groups)
        ) * category["weight"]

        total_score += category_score

    return round(total_score, 2)