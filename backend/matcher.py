import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python", "java", "c++", "machine learning",
    "deep learning", "artificial intelligence",
    "data analysis", "data science", "sql", "mysql",
    "mongodb", "html", "css", "javascript", "flask",
    "django", "react", "node.js", "communication",
    "problem solving", "teamwork", "leadership",
    "content creation", "content writing",
    "social media marketing", "digital marketing",
    "marketing", "seo", "canva", "video editing",
    "photography", "creativity", "research", "excel",
    "power bi", "tableau", "pandas", "numpy",
    "tensorflow", "pytorch", "scikit-learn",
    "statistics", "data visualization", "project management"
]


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found_skills.append(skill.title())

    return sorted(set(found_skills))


def calculate_match_score(resume_text, job_description):
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
        score = cosine_similarity(
            vectors[0:1], vectors[1:2]
        )[0][0]

        return round(float(score * 100), 2)

    except ValueError:
        return 0.0


def analyze_skills(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matching_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }


def generate_suggestions(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    suggestions = []

    if missing_skills:
        suggestions.append(
            "Consider improving these job-related skills: "
            + ", ".join(missing_skills)
            + "."
        )

    if len(resume_text.split()) < 100:
        suggestions.append(
            "If applicable, add relevant projects, "
            "internship experience, and achievements "
            "to strengthen your resume."
        )

    if not suggestions:
        suggestions.append(
            "Your resume covers the listed job skills. "
            "Tailor your project descriptions and achievements "
            "to the job requirements."
        )

    return suggestions