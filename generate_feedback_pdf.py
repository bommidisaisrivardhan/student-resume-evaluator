from fpdf import FPDF

def generate_feedback_pdf(matched, missing, weak_phrases, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume Evaluation Report", ln=1, align="C")

    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Skills Found:\n{', '.join(matched)}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Suggested Keywords:\n{', '.join(missing)}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Weak Phrases:\n" + "\n".join(weak_phrases))
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Match Score: {round(score * 100, 2)}%", ln=1)

    output_path = "feedback_report.pdf"
    pdf.output(output_path)
    return output_path

