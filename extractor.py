import re

SKILLS_LIST = [
    "python", "sql", "machine learning", "deep learning",
    "data analysis", "excel", "power bi", "tableau",
    "java", "c++", "javascript", "html", "css",
    "nlp", "tensorflow", "keras", "scikit-learn",
    "communication", "leadership", "teamwork"
]

def extract_email(text):
    match = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match[0] if match else ""

def extract_phone(text):
    match = re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", text)
    return match[0] if match else ""

def extract_name(text):
    # get first line of resume as name
    lines = text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line and len(line.split()) <= 4:
            return line
    return ""

def extract_skills(text):
    text_lower = text.lower()
    found = [skill for skill in SKILLS_LIST if skill in text_lower]
    return found

def extract_info(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }