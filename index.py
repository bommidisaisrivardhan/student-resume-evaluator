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

# Calculate similarity between resume and a job description (optional)
def get_similarity(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_text, jd_text])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

# Streamlit UI
st.title("AI Resume Evaluation for Students")

st.write("Upload your resume to get feedback and improvement suggestions.")

uploaded_resume = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])
jd_input = st.text_area("Optional: Paste Job Description for Comparison (or leave blank)")

if uploaded_resume:
    resume_text = extract_text_from_pdf(uploaded_resume)

    # Extract skills and suggestions
    matched_keywords = extract_keywords(resume_text, industry_keywords)
    missing_keywords = suggest_keywords(resume_text, industry_keywords)

    st.subheader("✅ Skills Found in Your Resume:")
    st.write(", ".join(matched_keywords) if matched_keywords else "No key skills found.")

    st.subheader("💡 Suggested Keywords to Add:")
    st.write(", ".join(missing_keywords) if missing_keywords else "Looks good!")

    # Optional: Match score with job description
    score=0.0
    if jd_input.strip():
        score = get_similarity(resume_text, jd_input)
        st.subheader("📊 Resume vs Job Description Match:")
        st.success(f"Match Score: {round(score * 100, 2)}%")
        st.progress(score)

    st.subheader("🧠 Overall Suggestions:")
    if len(matched_keywords) < 5:
        st.warning("Try to include more relevant skills and achievements.")
    else:
        st.info("Your resume contains several important keywords. Nice work!")

    if len(resume_text.split()) < 150:
        st.warning("Your resume seems very short. Consider adding more details like projects, skills, or achievements.")


if st.button("📄 Download Feedback as PDF"):
    path = generate_feedback_pdf(matched_keywords, missing_keywords, [], score)
    with open(path, "rb") as file:
        st.download_button("Download PDF", file, file_name="Resume_Feedback.pdf")
