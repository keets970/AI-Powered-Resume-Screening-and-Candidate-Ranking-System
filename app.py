import streamlit as st
import pdfplumber
from extractor import extract_info
from scorer import get_score


st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; }
    
    * { color: #ffffff !important; }
    
    header[data-testid="stHeader"] {
        background-color: #0d0d0d !important;
        visibility: visible !important;
    }
    #MainMenu { visibility: visible !important; }
    footer { visibility: hidden; }
    
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #00e5ff !important;
        padding: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #aaaaaa !important;
        margin-bottom: 30px;
    }
    .stButton > button {
        background-color: #00e5ff;
        color: #0d0d0d !important;
        border-radius: 10px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #00b8d4;
        color: #0d0d0d !important;
    }
    .result-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00e5ff;
        margin-bottom: 15px;
    }
    .skill-badge {
        display: inline-block;
        background-color: #00e5ff;
        color: #0d0d0d !important;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 13px;
        font-weight: bold;
    }
    .score-high { color: #00e676 !important; font-size: 28px; font-weight: bold; }
    .score-mid  { color: #ffab00 !important; font-size: 28px; font-weight: bold; }
    .score-low  { color: #ff1744 !important; font-size: 28px; font-weight: bold; }
    .summary-box {
        background-color: #1a1a1a;
        border: 1px solid #00e5ff;
        color: #00e5ff !important;
        padding: 15px 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 18px;
    }
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a !important;
        border: 2px dashed #00e5ff !important;
        border-radius: 10px !important;
    }
    [data-testid="stFileUploader"] * {
        color: #ffffff !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #1a1a1a !important;
        border: none !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    section[data-testid="stFileUploader"] > div {
        background-color: #1a1a1a !important;
    }
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #00e5ff !important;
        border-radius: 8px !important;
    }
    button[data-testid="baseButton-secondary"] {
        background-color: #00e5ff !important;
        color: #0d0d0d !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def get_score_color(score):
    if score >= 50:
        return "score-high"
    elif score >= 30:
        return "score-mid"
    else:
        return "score-low"

# header
st.markdown('<div class="title">📄 AI-Powered Resume Screener</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a Job Description and Resumes to instantly rank candidates</div>', unsafe_allow_html=True)
st.markdown("---")

# upload section
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 Job Description")
    jd_file = st.file_uploader("Upload JD (PDF)", type=["pdf"], label_visibility="collapsed")
    if jd_file:
        st.success("✅ Job Description uploaded!")

with col2:
    st.markdown("### 📄 Candidate Resumes")
    resume_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"],
                                     accept_multiple_files=True,
                                     label_visibility="collapsed")
    if resume_files:
        st.success(f"✅ {len(resume_files)} resume(s) uploaded!")

st.markdown("---")

# job title input
st.markdown("### 💼 Job Title")
job_title = st.text_input("Enter job title (e.g. Python Developer)")

st.markdown("---")

# screen button
col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b2:
    screen_btn = st.button("🔍 Screen Candidates")

if screen_btn:
    if not jd_file:
        st.warning("⚠️ Please upload a Job Description!")
    elif not resume_files:
        st.warning("⚠️ Please upload at least one resume!")
    elif not job_title:
        st.warning("⚠️ Please enter a job title!")
    else:
        st.markdown("---")
        st.markdown("### ⏳ Analysing Resumes...")
        progress = st.progress(0)
        status = st.empty()

        jd_text = read_pdf(jd_file)
        

        results = []
        total = len(resume_files)

        for i, resume in enumerate(resume_files):
            status.write(f"🔍 Scanning: {resume.name}")
            resume_text = read_pdf(resume)
            info = extract_info(resume_text)
            score = get_score(resume_text, jd_text)

            

            results.append({
                "Name": info["name"] or resume.name,
                "Email": info["email"] or "N/A",
                "Skills": info["skills"],
                "Score": score
            })
            progress.progress((i + 1) / total)

        status.write("✅ Analysis complete! Results saved to database.")
        results = sorted(results, key=lambda x: x["Score"], reverse=True)

        st.markdown("---")

        top_candidate = results[0]["Name"]
        st.markdown(f"""
            <div class="summary-box">
                📊 Total Screened: <b>{total}</b> &nbsp;|&nbsp;
                🏆 Top Candidate: <b>{top_candidate}</b> &nbsp;|&nbsp;
                💾 Saved to Database ✅
            </div>
        """, unsafe_allow_html=True)

        st.markdown("## 🏆 Ranked Candidates")

        for i, r in enumerate(results):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
            sc = get_score_color(r["Score"])

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([3, 4, 1])

            with c1:
                st.markdown(f"### {medal} {r['Name']}")
                st.write(f"📧 {r['Email']}")

            with c2:
                st.markdown("**🛠 Skills Matched:**")
                if r["Skills"]:
                    badges = " ".join([f'<span class="skill-badge">{s}</span>' for s in r["Skills"]])
                    st.markdown(badges, unsafe_allow_html=True)
                else:
                    st.write("No skills matched")

            with c3:
                st.markdown(f'<div class="{sc}">{r["Score"]}%</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("")

        st.markdown("---")
       