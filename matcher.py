import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------------------------
# LOAD JOB DATABASE
# -------------------------------------------------

def load_jobs():
    return pd.read_csv("jobs.csv")


# -------------------------------------------------
# CLEAN TEXT
# -------------------------------------------------

def clean_text(text):
    text = str(text).lower()

    text = re.sub(
        r"[^a-zA-Z0-9+#.\- ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# -------------------------------------------------
# SKILL DATABASE
# -------------------------------------------------

SKILLS = [
    "Python",
    "Java",
    "SQL",
    "Git",
    "Django",
    "Flask",
    "Excel",
    "Power BI",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Deep Learning",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Linux",
    "AWS",
    "Docker",
    "Kubernetes",
    "Statistics",
    "Data Structures",
    "Algorithms"
]


# -------------------------------------------------
# EXTRACT SKILLS
# -------------------------------------------------

def extract_skills(text):

    text = clean_text(text)

    detected = []

    for skill in SKILLS:

        skill_clean = clean_text(skill)

        pattern = r"\b" + re.escape(skill_clean) + r"\b"

        if re.search(pattern, text):

            detected.append(skill)

    return sorted(
        list(set(detected))
    )


# -------------------------------------------------
# TF-IDF MATCHING
# -------------------------------------------------

def calculate_similarity(student_text, job_text):

    documents = [
        clean_text(student_text),
        clean_text(job_text)
    ]

    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


# -------------------------------------------------
# SKILL MATCHING
# -------------------------------------------------

def calculate_skill_score(
    student_skills,
    required_skills
):

    student = set(
        skill.lower()
        for skill in student_skills
    )

    required = set(
        skill.lower()
        for skill in required_skills
    )

    if not required:
        return 0

    matched = student.intersection(required)

    score = (
        len(matched)
        / len(required)
    ) * 100

    return round(score, 2)


# -------------------------------------------------
# SKILL GAP
# -------------------------------------------------

def get_skill_gap(
    student_skills,
    required_skills
):

    student = set(
        skill.lower()
        for skill in student_skills
    )

    required = set(
        skill.lower()
        for skill in required_skills
    )

    matched = student.intersection(required)

    missing = required - student

    return (
        sorted(matched),
        sorted(missing)
    )


# -------------------------------------------------
# JOB MATCHING ENGINE
# -------------------------------------------------

def match_jobs(student_text):

    jobs = load_jobs()

    student_skills = extract_skills(
        student_text
    )

    results = []

    for _, job in jobs.iterrows():

        required_skills = [
            skill.strip()
            for skill in job[
                "Required Skills"
            ].split(",")
        ]

        skill_score = calculate_skill_score(
            student_skills,
            required_skills
        )

        job_text = (
            job["Job Title"]
            + " "
            + job["Required Skills"]
            + " "
            + job["Description"]
        )

        similarity_score = calculate_similarity(
            student_text,
            job_text
        )

        # Weighted final score
        final_score = (
            skill_score * 0.70
            + similarity_score * 0.30
        )

        matched, missing = get_skill_gap(
            student_skills,
            required_skills
        )

        results.append({

            "Job Title":
                job["Job Title"],

            "Company":
                job["Company"],

            "Match Score":
                round(final_score, 2),

            "Skill Score":
                skill_score,

            "Similarity Score":
                similarity_score,

            "Required Skills":
                required_skills,

            "Matched Skills":
                matched,

            "Missing Skills":
                missing,

            "Description":
                job["Description"]
        })

    results.sort(
        key=lambda x: x["Match Score"],
        reverse=True
    )

    return (
        student_skills,
        results
    )


# -------------------------------------------------
# RECOMMENDATION ENGINE
# -------------------------------------------------

RECOMMENDATIONS = {

    "Python":
        "Learn Python programming, functions, OOP and advanced Python.",

    "SQL":
        "Learn SQL queries, joins, subqueries and database management.",

    "Git":
        "Learn Git, GitHub, branching and version control.",

    "Django":
        "Learn Django fundamentals and REST API development.",

    "Flask":
        "Learn Flask and Python backend development.",

    "Pandas":
        "Learn Pandas for data cleaning and analysis.",

    "NumPy":
        "Learn NumPy arrays and numerical computing.",

    "Machine Learning":
        "Study supervised and unsupervised machine learning.",

    "Deep Learning":
        "Study neural networks and deep learning architectures.",

    "TensorFlow":
        "Learn TensorFlow model building and training.",

    "PyTorch":
        "Learn PyTorch and neural network implementation.",

    "NLP":
        "Study Natural Language Processing and text analysis.",

    "Scikit-learn":
        "Learn Scikit-learn for practical machine learning.",

    "Statistics":
        "Study probability, statistics and statistical analysis.",

    "HTML":
        "Learn HTML5 and semantic web structure.",

    "CSS":
        "Learn CSS layouts, Flexbox and responsive design.",

    "JavaScript":
        "Learn modern JavaScript and browser programming.",

    "React":
        "Learn React components, state and hooks.",

    "Node.js":
        "Learn Node.js backend development.",

    "AWS":
        "Learn AWS fundamentals and cloud deployment.",

    "Docker":
        "Learn Docker containers and deployment.",

    "Kubernetes":
        "Learn Kubernetes and container orchestration.",

    "Linux":
        "Learn Linux commands, processes and server administration.",

    "Java":
        "Learn Java programming and object-oriented development.",

    "Data Structures":
        "Study arrays, linked lists, stacks, queues, trees and graphs.",

    "Algorithms":
        "Study searching, sorting, recursion and algorithm analysis."
}


def get_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        for key in RECOMMENDATIONS:

            if key.lower() == skill.lower():

                recommendations.append(
                    RECOMMENDATIONS[key]
                )

    return recommendations