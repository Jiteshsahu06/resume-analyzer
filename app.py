import streamlit as st

from src.pdf_loader import extract_text_from_pdf
from src.text_processor import clean_text
from src.text_splitter import split_text
from src.embeddings import load_embedding_model, generate_embeddings
from src.vector_store import create_vector_store, add_documents
from src.rag import retrieve_context, analyze_resume
from src.gemini_llm import create_gemini_client
from src.jd_parser import extract_required_skills
from src.skill_matcher import match_skills
from src.match_scorer import calculate_weighted_score
from src.interview_generator import generate_interview_questions
from src.docx_loader import extract_text_from_docx




# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# MAIN TITLE
# =========================================================

st.title("🤖 AI Resume Analyzer & Job Matcher")


# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs([
    "🤖 AI Resume Analyzer",
    "👨‍💻 Developer"
])


# =========================================================
# TAB 1 — AI RESUME ANALYZER
# =========================================================

with tab1:

    st.write(
        "Upload your resume and paste a job description "
        "to analyze your resume against the job."
    )

    st.subheader("📄 Upload Resume")

    resume_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf", "docx"]
    )

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the Job Description here",
        height=250,
        placeholder="Paste the complete job description here..."
    )

    if st.button("🚀 Analyze Resume", type="primary"):

        if resume_file is None:

            st.error(
                "Please upload your resume PDF."
            )

        elif not job_description.strip():

            st.error(
                "Please enter the job description."
            )

        else:

            with st.spinner("Analyzing your resume..."):

                # =================================================
                # 1. EXTRACT RESUME TEXT
                # =================================================
                

                if resume_file.name.lower().endswith(".pdf"):
                
                    raw_resume_text = extract_text_from_pdf(
                        resume_file
                    )

                elif resume_file.name.lower().endswith(".docx"):
                
                    raw_resume_text = extract_text_from_docx(
                        resume_file
                    )

                # =================================================
                # 2. CLEAN TEXT
                # =================================================

                resume_text = clean_text(
                    raw_resume_text
                )

                if not resume_text:

                    st.error(
                        "Could not extract text from this PDF. "
                        "It may be a scanned PDF."
                    )

                    st.stop()

                # =================================================
                # 3. SPLIT INTO CHUNKS
                # =================================================

                resume_chunks = split_text(
                    resume_text
                )

                # =================================================
                # 4. LOAD EMBEDDING MODEL
                # =================================================

                model = load_embedding_model()

                # =================================================
                # 5. GENERATE EMBEDDINGS
                # =================================================

                embeddings = generate_embeddings(
                    resume_chunks,
                    model
                )

                # =================================================
                # 6. CREATE VECTOR STORE
                # =================================================

                collection = create_vector_store()

                # =================================================
                # 7. STORE RESUME CHUNKS
                # =================================================

                add_documents(
                    collection,
                    resume_chunks,
                    embeddings
                )

                # =================================================
                # 8. EXTRACT REQUIRED SKILLS FROM JD
                # =================================================

                required_skills_text = extract_required_skills(
                    job_description
                )

                # =================================================
                # 9. MATCH JD SKILLS WITH RESUME
                # =================================================

                matching_skills, missing_skills = match_skills(
                    required_skills_text,
                    resume_text
                )

                # =================================================
                # 10. CALCULATE WEIGHTED MATCH SCORE
                # =================================================

                match_score = calculate_weighted_score(
                    resume_text,
                    matching_skills
                )

                # =================================================
                # 11. RETRIEVE RELEVANT CONTEXT
                # =================================================

                query = f"""
                Analyze this resume against the following job description:

                {job_description}
                """

                context = retrieve_context(
                    query,
                    model,
                    collection,
                    n_results=8
                )

                # =================================================
                # 12. CONNECT GEMINI
                # =================================================

                client = create_gemini_client()

                # =================================================
                # 13. GENERATE AI RESUME ANALYSIS
                # =================================================

                analysis = analyze_resume(
                    client,
                    f"""
                    FULL RESUME:
                    {resume_text}

                    RELEVANT RESUME CONTEXT:
                    {context}
                    """,
                    job_description
                )

            # =====================================================
            # ANALYSIS RESULTS
            # =====================================================

            st.success(
                "Resume analysis completed! 🎉"
            )

            # =====================================================
            # MATCH SCORE
            # =====================================================

            st.metric(
                "🎯 Match Score",
                f"{match_score}%"
            )

            # =====================================================
            # SKILL MATCH
            # =====================================================

            st.subheader("🎯 Skill Match")

            col1, col2 = st.columns(2)

            # -----------------------------------------------------
            # MATCHING SKILLS
            # -----------------------------------------------------

            with col1:

                st.write(
                    "### ✅ Matching Skills"
                )

                if matching_skills:

                    for skill in matching_skills:

                        st.success(skill)

                else:

                    st.info(
                        "No matching skills found."
                    )

            # -----------------------------------------------------
            # MISSING SKILLS
            # -----------------------------------------------------

            with col2:

                st.write(
                    "### ❌ Missing Skills"
                )

                if missing_skills:

                    for skill in missing_skills:

                        st.error(skill)

            # =====================================================
            # AI RESUME ANALYSIS
            # =====================================================

            st.subheader(
                "📊 AI Resume Analysis"
            )

            st.markdown(
                analysis
            )

            # =====================================================
            # INTERVIEW QUESTIONS
            # =====================================================

            st.subheader(
                "🎤 Interview Questions"
            )

            interview_questions = generate_interview_questions(
                client,
                resume_text,
                job_description
            )

            st.markdown(
                interview_questions
            )


# =========================================================
# TAB 2 — DEVELOPER PORTFOLIO
# =========================================================

with tab2:

    st.title("👨‍💻 Jitesh Sahu")
    st.subheader("AI Software Engineer")

    # ---------------------------------------------------------
    # PROFILE + ABOUT
    # ---------------------------------------------------------

    profile_col, about_col = st.columns([1, 2])

    with profile_col:

        st.image(
            "assets/profile.png",
            width=280
        )

    with about_col:

        st.header("👋 About Me")

        st.write(
            """
            I am an MCA student specializing in Machine Learning & AI.
            I am interested in building AI-powered software applications
            using Generative AI, RAG, LLMs, and modern AI technologies.

            I enjoy working with Python and building practical AI
            applications that solve real-world problems.
            """
        )

        st.write(
            "📍 Jaipur, Rajasthan  |  🎓 MCA (2025–2027)  |  🤖 AI/ML"
        )

        # Resume Download
        with open("assets/resume.pdf", "rb") as file:

            st.download_button(
                label="📄 Download My Resume",
                data=file,
                file_name="Jitesh_Sahu_Resume.pdf",
                mime="application/pdf"
            )

    # ---------------------------------------------------------
    # TECHNICAL SKILLS
    # ---------------------------------------------------------

    st.header("🛠️ Technical Skills")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("💻 Programming")

        st.markdown(
            """
            `Python` `Java` `SQL`
            """
        )

    with col2:

        st.subheader("🤖 AI / ML")

        st.markdown(
            """
            `Generative AI` `RAG` `LLM Applications`

            `Gemini API` `Prompt Engineering` `Embeddings`

            `Semantic Search` `Machine Learning`
            """
        )

    with col3:

        st.subheader("🧰 Tools & Technologies")

        st.markdown(
            """
            `Streamlit` `REST APIs` `Pandas` `NumPy`

            `Power BI` `MongoDB` `ChromaDB`

            `GitHub` `Jupyter` `VS Code`
            """
        )

    # ---------------------------------------------------------
    # PROJECTS
    # ---------------------------------------------------------

    st.header("🚀 Projects")

    project1, project2 = st.columns(2)

    with project1:

        st.subheader("🤖 AI Resume Analyzer & Job Matcher")

        st.write(
            """
            AI-powered application that analyzes resumes against
            job descriptions using RAG, embeddings, ChromaDB,
            Gemini, and semantic skill matching.
            """
        )

    with project2:

        st.subheader("📊 Diwali Sales Analysis")

        st.write(
            """
            Data analysis project using Python, Pandas and NumPy
            to analyze customer behavior and sales patterns.
            """
        )

    # ---------------------------------------------------------
    # SOCIAL LINKS
    # ---------------------------------------------------------

    st.header("🔗 Connect With Me")

    github_col, linkedin_col = st.columns(2)

    with github_col:

        st.link_button(
            "🐙 GitHub",
            "https://github.com/Jiteshsahu06"
        )

    with linkedin_col:

        st.link_button(
            "💼 LinkedIn",
            "https://www.linkedin.com/in/jitesh-sahu/"
        )