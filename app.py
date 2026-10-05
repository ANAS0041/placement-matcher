import streamlit as st
import pandas as pd

from matcher import (
    match_jobs,
    get_recommendations
)


# =================================================
# PAGE CONFIG
# =================================================

st.set_page_config(

    page_title="Placement Matcher",

    page_icon="🎯",

    layout="wide"
)


# =================================================
# CUSTOM CSS
# =================================================

st.markdown(
    """
    <style>

    .main-title {

        font-size: 42px;

        font-weight: 700;

        text-align: center;

        margin-bottom: 5px;

    }

    .subtitle {

        text-align: center;

        color: #777;

        font-size: 18px;

        margin-bottom: 30px;

    }

    .job-card {

        padding: 20px;

        border-radius: 12px;

        border: 1px solid #ddd;

        margin-bottom: 15px;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =================================================
# HEADER
# =================================================

st.markdown(
    '<div class="main-title">🎯 Placement Matcher</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Based Placement Matching & Skill-Gap Analysis</div>',
    unsafe_allow_html=True
)


# =================================================
# SIDEBAR
# =================================================

st.sidebar.title("👤 Student Profile")

name = st.sidebar.text_input(
    "Full Name",
    placeholder="Muhammad Anas"
)

email = st.sidebar.text_input(
    "Email",
    placeholder="your@email.com"
)

age = st.sidebar.number_input(
    "Age",
    min_value=16,
    max_value=60,
    value=20
)

location = st.sidebar.text_input(
    "Location",
    placeholder="Bengaluru"
)

skills = st.sidebar.text_area(
    "Skills",
    placeholder=(
        "Example:\n"
        "Python\n"
        "SQL\n"
        "Machine Learning\n"
        "Pandas\n"
        "Git"
    ),
    height=150
)


# =================================================
# RESUME UPLOAD
# =================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📄 Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload TXT Resume",
    type=["txt"]
)


# =================================================
# ANALYZE BUTTON
# =================================================

analyze = st.sidebar.button(
    "🚀 Analyze Profile",
    use_container_width=True
)


# =================================================
# ANALYSIS
# =================================================

if analyze:

    if not name:

        st.error(
            "Please enter your name."
        )

        st.stop()


    # ---------------------------------------------
    # BUILD PROFILE TEXT
    # ---------------------------------------------

    profile_text = skills


    # ---------------------------------------------
    # ADD RESUME CONTENT
    # ---------------------------------------------

    if uploaded_file:

        resume_text = uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

        profile_text += " " + resume_text


    if not profile_text.strip():

        st.error(
            "Please enter your skills or upload a resume."
        )

        st.stop()


    # ---------------------------------------------
    # RUN BACKEND
    # ---------------------------------------------

    student_skills, results = match_jobs(
        profile_text
    )


    # =================================================
    # PROFILE
    # =================================================

    st.success(
        f"Profile analyzed successfully for {name}."
    )

    st.header("👤 Candidate Profile")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Name",
            name
        )

    with col2:

        st.metric(
            "Age",
            age
        )

    with col3:

        st.metric(
            "Location",
            location
            if location
            else "Not specified"
        )

    with col4:

        st.metric(
            "Skills Detected",
            len(student_skills)
        )


    # =================================================
    # DETECTED SKILLS
    # =================================================

    st.subheader(
        "🧠 Detected Skills"
    )

    if student_skills:

        skill_columns = st.columns(
            min(
                5,
                len(student_skills)
            )
        )

        for i, skill in enumerate(
            student_skills
        ):

            with skill_columns[
                i % len(skill_columns)
            ]:

                st.success(
                    f"✓ {skill}"
                )

    else:

        st.warning(
            "No recognized technical skills detected."
        )


    st.divider()


    # =================================================
    # TOP JOB MATCHES
    # =================================================

    st.header(
        "🎯 Top Placement Matches"
    )

    for job in results[:5]:

        score = job["Match Score"]

        st.markdown(
            f"""
            ### {job['Job Title']}

            **🏢 Company:** {job['Company']}

            **🎯 Match Score:** {score}%
            """
        )

        st.progress(
            int(score)
        )

        st.caption(
            job["Description"]
        )

        st.divider()


    # =================================================
    # JOB SELECTION
    # =================================================

    st.header(
        "🔍 Skill-Gap Analysis"
    )

    job_names = [

        job["Job Title"]
        for job in results

    ]

    selected_job = st.selectbox(
        "Select a job:",
        job_names
    )


    selected = next(

        job
        for job in results

        if job["Job Title"]
        == selected_job

    )


    # =================================================
    # SCORE CARDS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Overall Match",
            f"{selected['Match Score']}%"
        )

    with col2:

        st.metric(
            "Skills Matched",
            len(selected["Matched Skills"])
        )

    with col3:

        st.metric(
            "Skills Missing",
            len(selected["Missing Skills"])
        )


    st.divider()


    # =================================================
    # MATCHED SKILLS
    # =================================================

    st.subheader(
        "✅ Skills You Have"
    )

    if selected["Matched Skills"]:

        for skill in selected[
            "Matched Skills"
        ]:

            st.success(
                f"✓ {skill}"
            )

    else:

        st.info(
            "No matching skills."
        )


    # =================================================
    # MISSING SKILLS
    # =================================================

    st.subheader(
        "❌ Skill Gap"
    )

    if selected["Missing Skills"]:

        for skill in selected[
            "Missing Skills"
        ]:

            st.error(
                f"✗ {skill}"
            )

    else:

        st.success(
            "🔥 No skill gap detected!"
        )


    # =================================================
    # LEARNING RECOMMENDATIONS
    # =================================================

    st.subheader(
        "📚 Recommended Learning"
    )

    recommendations = get_recommendations(
        selected["Missing Skills"]
    )

    if recommendations:

        for recommendation in recommendations:

            st.info(
                f"📖 {recommendation}"
            )

    else:

        st.info(
            "No additional recommendations."
        )


    # =================================================
    # TECHNICAL DETAILS
    # =================================================

    with st.expander(
        "🤖 View AI Matching Details"
    ):

        st.write(
            "The system combines:"
        )

        st.write(
            "• Skill-based matching — 70%"
        )

        st.write(
            "• TF-IDF text similarity — 30%"
        )

        st.write(
            "The final score ranks jobs according "
            "to how closely the candidate profile "
            "matches the job requirements."
        )


# =================================================
# INITIAL SCREEN
# =================================================

else:

    st.info(
        "👈 Enter your profile details and skills "
        "in the sidebar, then click **Analyze Profile**."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            "## 🎯"
        )

        st.subheader(
            "Placement Matching"
        )

        st.write(
            "Ranks available jobs according "
            "to candidate-job compatibility."
        )


    with col2:

        st.markdown(
            "## 🔍"
        )

        st.subheader(
            "Skill Gap"
        )

        st.write(
            "Identifies technical skills required "
            "for the selected job but missing "
            "from the candidate profile."
        )


    with col3:

        st.markdown(
            "## 📚"
        )

        st.subheader(
            "Learning Recommendations"
        )

        st.write(
            "Suggests learning areas based on "
            "the identified skill gaps."
        )
        