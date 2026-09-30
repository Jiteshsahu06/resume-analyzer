# import json


# from src.gemini_llm import create_gemini_client


# def extract_required_skills(job_description):
#     client = create_gemini_client()

#     prompt = f"""
# You are a Job Description Skill Extractor.

# Extract the important technical skills and technologies
# explicitly required or mentioned in the following job description.

# JOB DESCRIPTION:
# {job_description}

# Return only a simple Python-style list of skill names.

# Example:
# ["Python", "SQL", "FastAPI", "Docker", "RAG"]

# Rules:
# - Extract technical skills and technologies only.
# - Include programming languages, frameworks, libraries,
#   databases, AI/ML technologies, developer tools and cloud technologies.
# - Do not include soft skills.
# - Do not include education eligibility.
# - Do not invent skills that are not mentioned in the job description.
# """

#     response = client.models.generate_content(
#         model="gemini-3.5-flash-lite",
#         contents=prompt
#     )

#     return json.loads(response.text)




import json

from src.gemini_llm import create_gemini_client


def extract_required_skills(job_description):
    client = create_gemini_client()

    prompt = f"""
You are a Job Description Skill Extractor.

Extract the important technical skills and technologies
explicitly required or mentioned in the following job description.

JOB DESCRIPTION:
{job_description}

Return ONLY a valid JSON array.

Example:
["Python", "SQL", "FastAPI", "Docker", "RAG"]

Rules:
- Extract technical skills and technologies only.
- Include programming languages, frameworks, libraries,
  databases, AI/ML technologies, developer tools and cloud technologies.
- Do not include soft skills.
- Do not include education eligibility.
- Do not invent skills that are not mentioned in the job description.
- Return only JSON.
- Do not use markdown code blocks.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    skills = json.loads(response.text)

    return skills