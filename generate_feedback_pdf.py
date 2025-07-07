from fpdf import FPDF
from datetime import datetime

def generate_feedback_pdf(matched, missing, weak_phrases, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt="AI Resume Evaluation Report", ln=1, align="C")

    # Report Date
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)

    pdf.ln(10)

    # Summary
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Summary:", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, f"Your resume matches {len(matched)} out of {len(matched) + len(missing)} key industry keywords.")
    pdf.multi_cell(0, 8, f"Match Score: {round(score * 100, 2)}%")
    
    # Stars based on score
    stars = int(score * 5)
    pdf.cell(200, 10, txt=f"Rating: {'⭐' * stars}{'☆' * (5 - stars)}", ln=1)
    
    pdf.ln(5)

    # Skills found
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="✅ Skills Found:", ln=1)
    pdf.set_font("Arial", size=11)
    for skill in matched:
        pdf.multi_cell(0, 8, f"• {skill}")
    
    pdf.ln(3)

    # Suggestions
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="💡 Suggested Keywords to Improve:", ln=1)
    pdf.set_font("Arial", size=11)
    if missing:
        for skill in missing:
            pdf.multi_cell(0, 8, f"• {skill}")
    else:
        pdf.multi_cell(0, 8, "None! Great job covering all important keywords.")

    pdf.ln(3)

    # Weak phrases
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="⚠️ Weak Phrases Found:", ln=1)
    pdf.set_font("Arial", size=11)
    if weak_phrases:
        for phrase in weak_phrases:
            pdf.multi_cell(0, 8, f"• {phrase}")
    else:
        pdf.multi_cell(0, 8, "No weak or vague phrases detected.")

    pdf.ln(5)

    # Personalized suggestions
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="📌 Recommendations:", ln=1)
    pdf.set_font("Arial", size=11)
    if len(matched) < 5:
        pdf.multi_cell(0, 8, "Consider adding more technical skills, project details, and measurable achievements.")
    if len(missing) > 5:
        pdf.multi_cell(0, 8, "Try to naturally incorporate missing keywords, especially those relevant to your field.")
    if score < 0.5:
        pdf.multi_cell(0, 8, "The match score with job description is low. Tailor your resume for the specific role.")

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, txt="— End of Report —", ln=1, align="C")

    output_path = "feedback_report.pdf"
    pdf.output(output_path)
    return output_path

