from src.embeddings import generate_embeddings
from src.vector_store import search_documents


def retrieve_context(query, model, collection, n_results=5):
    query_embedding = generate_embeddings(
        [query],
        model
    )[0]

    results = search_documents(
        collection,
        query_embedding,
        n_results=n_results
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context


def generate_rag_response(client, query, context):
    prompt = f"""
You are an AI Resume Analyzer.

Use only the resume context provided below to answer the user's question.

Resume Context:
{context}

User Question:
{query}

Instructions:
- Answer based only on the provided resume context.
- Do not invent information.
- If the information is not available in the context, clearly say that it is not available.
- Keep the answer simple and concise.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


def analyze_resume(client, resume_context, job_description):
    prompt = f"""
You are an AI Resume Analyzer.

Analyze the candidate's resume against the provided job description.

RESUME CONTEXT:
{resume_context}

JOB DESCRIPTION:
{job_description}

Provide the analysis in exactly this structure:

MATCH SCORE:
Give a percentage from 0 to 100 based on how well the resume matches
the job description. This is an application-defined matching score,
not a scientifically validated probability.

MATCHING SKILLS:
List the important skills that are explicitly demonstrated in the resume
and are also relevant to the job description.

MISSING SKILLS:
List important job requirements that are missing or not clearly demonstrated
in the resume.

STRENGTHS:
List the candidate's relevant strengths for this specific job.

WEAKNESSES:
List the important areas where the resume is weaker for this specific job.

SUGGESTIONS:
Give practical suggestions to improve the candidate's resume or skills
for this job.

IMPORTANT RULES:
- Use only information supported by the resume context and job description.
- Do not invent candidate experience.
- Do not treat job eligibility conditions as candidate strengths.
- Distinguish between a skill explicitly demonstrated in the resume
  and a skill mentioned only in a certification.
- GitHub should not automatically be treated as Git experience.
- SQL should not automatically be treated as MySQL experience.
- If a requirement is not clearly demonstrated in the resume,
  describe it as "Not demonstrated in resume".
- Do not infer skills from unrelated technologies.
- Do not assume that knowledge of one framework means knowledge of another framework.
- Do not assume that a candidate has a technology just because it is
  commonly used with another technology listed in the resume.
- Keep the language simple, professional, and factual.
- Always consider the FULL RESUME provided in the context before deciding
  whether a requirement is missing.
- If a skill or technology appears anywhere in the full resume,
  do not classify it as missing.
- Give priority to explicit evidence in the resume over assumptions.
- Keep the language simple, professional, and factual.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


