import spacy
import re

nlp = spacy.load("en_core_web_sm")

# define a skills list to match against
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
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
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

# TEST
if __name__ == "__main__":
    from phaser import parse_resume
    text = parse_resume(r"C:\Users\DELL\Desktop\Resume screener\resume1.pdf")
    info = extract_info(text)
    print(info)