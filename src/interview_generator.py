def generate_interview_questions(
    client,
    resume_text,
    job_description
):
    prompt = f"""
You are an AI Interview Preparation Assistant.

Generate interview questions based ONLY on the candidate's resume
and the provided job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Generate questions in these categories:

1. RESUME QUESTIONS
- 3 questions directly related to the candidate's resume.

2. PROJECT QUESTIONS
- 3 questions about the candidate's projects.

3. TECHNICAL QUESTIONS
- 5 questions based on technologies and requirements mentioned
  in the job description.

4. MISSING SKILL QUESTIONS
- 3 questions about important skills required by the job
  that are not clearly demonstrated in the resume.

5. HR QUESTIONS
- 3 general interview questions relevant to this role.

Rules:
- Do not invent experience.
- Do not claim the candidate knows a technology unless supported
  by the resume.
- Keep questions practical and interview-oriented.
- Keep the language simple and professional.
- Clearly separate each category.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text