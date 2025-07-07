import streamlit as st
import fitz  # PyMuPDF
from generate_feedback_pdf import generate_feedback_pdf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample keywords for suggestion
industry_keywords = [
    "Python", "Teamwork", "Problem-solving", "Machine Learning", "Leadership",
    "Communication", "Project Management", "Time Management", "SQL", "Java",
    "Git", "API", "Data Analysis", "Internship", "Research"
]

# Sample weak phrases to flag (can expand later)
weak_phrases_list = [
    "responsible for", "worked on", "some experience", "involved in", "helped with",
    "knowledge of", "participated", "familiar with"
]

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

# Extract matching skills from text
def extract_keywords(text, keyword_list):
    return [kw for kw in keyword_list if kw.lower() in text.lower()]

# Identify missing but useful keywords
def suggest_keywords(text, keyword_list):
    return [kw for kw in keyword_list if kw.lower() not in text.lower()]

# Detect weak phrases
def find_weak_phrases(text, weak_list):
    return [phrase for phrase in weak_list if phrase.lower() in text.lower()]

# Calculate similarity between resume and a job description (optional)
def get_similarity(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_text, jd_text])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Student Resume Evaluator", layout="centered")
st.title("🎓 AI Resume Evaluator for Students")
st.write("Upload your resume to get personalized feedback, keyword suggestions, and job match insights.")

uploaded_resume = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])
jd_input = st.text_area("📋 Optional: Paste Job Description (to compare with resume)", height=150)

if uploaded_resume:
    resume_text = extract_text_from_pdf(uploaded_resume)

    matched_keywords = extract_keywords(resume_text, industry_keywords)
    missing_keywords = suggest_keywords(resume_text, industry_keywords)
    weak_phrases = find_weak_phrases(resume_text, weak_phrases_list)

    st.subheader("✅ Skills Found:")
    st.write(", ".join(matched_keywords) if matched_keywords else "No keywords found.")

    st.subheader("💡 Suggested Keywords:")
    st.write(", ".join(missing_keywords) if missing_keywords else "Great job! Most keywords are covered.")

    st.subheader("⚠️ Weak Phrases Detected:")
    if weak_phrases:
        st.write(", ".join(weak_phrases))
    else:
        st.success("No weak or vague phrases found!")

    score = 0.0
    if jd_input.strip():
        score = get_similarity(resume_text, jd_input)
        st.subheader("📊 Resume vs Job Description Match:")
        st.info(f"Match Score: {round(score * 100, 2)}%")
        st.progress(score)

    st.subheader("📌 Recommendations:")
    if len(matched_keywords) < 5:
        st.warning("Consider adding more industry-relevant skills.")
    if len(missing_keywords) > 5:
        st.info("Try to naturally include the suggested keywords.")
    if score < 0.5 and jd_input.strip():
        st.warning("Resume alignment with job description is low. Customize it for this role.")

    # Generate PDF feedback
    if st.button("📄 Download PDF Report"):
        path = generate_feedback_pdf(matched_keywords, missing_keywords, weak_phrases, score)
        with open(path, "rb") as f:
            st.download_button("Download PDF", f, file_name="Resume_Feedback_Report.pdf")

