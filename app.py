import streamlit as st
import pdfplumber
from extractor import extract_info
from scorer import get_score
from database import save_job, save_candidate, get_candidates

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #4A90D9;
        padding: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 30px;
    }
    .stButton > button {
        background-color: #4A90D9;
        color: white;
        border-radius: 10px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #357ABD;
        color: white;
    }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .skill-badge {
        display: inline-block;
        background-color: #4A90D9;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 13px;
        font-weight: bold;
    }
    .score-high { color: #27AE60; font-size: 28px; font-weight: bold; }
    .score-mid  { color: #F39C12; font-size: 28px; font-weight: bold; }
    .score-low  { color: #E74C3C; font-size: 28px; font-weight: bold; }
    .summary-box {
        background-color: #4A90D9;
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 18px;
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

        # progress bar
        st.markdown("### ⏳ Analysing Resumes...")
        progress = st.progress(0)
        status = st.empty()

        jd_text = read_pdf(jd_file)

        # save job to database
        job_id = save_job(job_title, jd_text)

        results = []
        total = len(resume_files)

        for i, resume in enumerate(resume_files):
            status.write(f"🔍 Scanning: {resume.name}")
            resume_text = read_pdf(resume)
            info = extract_info(resume_text)
            score = get_score(resume_text, jd_text)

            # save each candidate to database
            save_candidate(
                job_id,
                info["name"] or resume.name,
                info["email"] or "N/A",
                info["skills"],
                score
            )

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

        # summary box
        top_candidate = results[0]["Name"]
        st.markdown(f"""
            <div class="summary-box">
                📊 Total Candidates Screened: <b>{total}</b> &nbsp;|&nbsp;
                🏆 Top Candidate: <b>{top_candidate}</b> &nbsp;|&nbsp;
                💾 Saved to Database ✅
            </div>
        """, unsafe_allow_html=True)

        # results
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

        # show saved history
        st.markdown("---")
        st.markdown("### 💾 Saved Results from Database")
        saved = get_candidates(job_id)
        for row in saved:
            st.write(f"✅ {row[0]} | {row[1]} | Skills: {row[2]} | Score: {row[3]}%")