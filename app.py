!pip install gradio PyPDF2 matplotlib
import gradio as gr
import PyPDF2
import matplotlib.pyplot as plt
import os

skills_db = [
    "python", "java", "sql", "excel", "html",
    "css", "machine learning", "data analysis"
]

course_map = {
    "python": "Python for Beginners (YouTube/Coursera)",
    "java": "Java Programming Masterclass",
    "sql": "SQL Bootcamp",
    "excel": "Excel for Data Analysis",
    "html": "HTML & CSS Crash Course",
    "css": "Modern CSS Guide",
    "machine learning": "ML A-Z (Udemy)",
    "data analysis": "Data Analysis with Python"
}

job_roles = {
    "python": "Python Developer",
    "java": "Java Developer",
    "sql": "Data Analyst",
    "excel": "Business Analyst",
    "machine learning": "ML Engineer",
    "data analysis": "Data Analyst",
    "html": "Frontend Developer",
    "css": "Frontend Developer"
}

def extract_text(file):
    reader = PyPDF2.PdfReader(file.name)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

def generate_chart(found, missing):
    labels = ["Known Skills", "Missing Skills"]
    values = [len(found), len(missing)]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Skill Analysis")

    path = "skill_chart.png"
    plt.savefig(path)
    plt.close()
    return path

def jobfit(file):
    if file is None:
        return "Upload a resume PDF"

    text = extract_text(file)

    found = [s for s in skills_db if s in text]
    missing = [s for s in skills_db if s not in found]

    score = int((len(found) / len(skills_db)) * 100)

    # Course suggestions
    courses = [course_map[m] for m in missing if m in course_map]

    # Job role prediction (simple logic)
    role_scores = {}
    for skill in found:
        if skill in job_roles:
            role = job_roles[skill]
            role_scores[role] = role_scores.get(role, 0) + 1

    predicted_role = max(role_scores, key=role_scores.get) if role_scores else "Entry Level Role"

    chart_path = generate_chart(found, missing)

    report = f"""
========================
🚀 JOBFIT AI REPORT
========================

📊 Score: {score}%

🎯 Predicted Role: {predicted_role}

✅ Skills Found:
{found}

❌ Missing Skills:
{missing}

🎓 Recommended Courses:
{courses if courses else "No suggestions - you are strong!"}

========================
"""

    return report, chart_path

demo = gr.Interface(
    fn=jobfit,
    inputs=gr.File(file_types=[".pdf"]),
    outputs=[
        gr.Textbox(label="JobFit Report"),
        gr.Image(label="Skill Chart")
    ],
    title="JobFit AI Pro"
)

demo.launch(share=True)
