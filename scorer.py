from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber

def get_score(resume_text, jd_text):
    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return round(score * 100, 2)

if __name__ == "__main__":
    from extractor import extract_info

    
    text = ""
    with pdfplumber.open(r"C:\Users\DELL\Desktop\Resume screener\py_resume.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    print("TEXT LENGTH:", len(text))  

    jd_text = """
    We are looking for a Senior Python Developer with strong experience in
    machine learning, deep learning, NLP, SQL, PostgreSQL, data analysis,
    scikit-learn, TensorFlow, PyTorch, SpaCy, NLTK, Hugging Face, BERT,
    Pandas, NumPy, data pipelines, ETL, Docker, AWS, MongoDB, Git,
    backend development, predictive modeling, and data science.
    Candidate should have 3+ years of experience in Python development
    and strong knowledge of database architecture and optimization.
    """

    info = extract_info(text)
    score = get_score(text, jd_text)

    print("Candidate:", info["name"])
    print("Skills:", info["skills"])
    print("Match Score:", score, "%")