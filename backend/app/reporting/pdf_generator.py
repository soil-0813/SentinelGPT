from fpdf import FPDF
import os

class ReportPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "SentinelGPT Threat & Incident Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(report_data: dict, output_path: str):
    pdf = ReportPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, report_data.get("title", "Incident Report"), ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)

    # Meta
    pdf.cell(0, 8, f"ID: {report_data.get('id', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Severity: {report_data.get('severity', 'Unknown')}", ln=True)
    pdf.cell(0, 8, f"Analyst: {report_data.get('analyst', 'System')}", ln=True)
    pdf.ln(5)

    # Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, report_data.get("summary", "No summary provided."))
    pdf.ln(5)

    # Sections
    sections = report_data.get("sections", {})
    for key, value in sections.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, key.replace("_", " ").title(), ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, value)
        pdf.ln(5)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf.output(output_path)
    return output_path
