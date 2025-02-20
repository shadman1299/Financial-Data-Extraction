import os
import json
import re
import fitz  # PyMuPDF

# Define file paths for the PDFs on your local machine
pdf_files = {
    "Amaar_Raja.pdf": r"C:\Users\hassa\Desktop\Financial Data Extraction\Amaar_Raja.pdf",
    "Financial_Report.pdf": r"C:\Users\hassa\Desktop\Financial Data Extraction\Financial_Report.pdf"
}

# Output JSON file location
output_path = r"C:\Users\hassa\Desktop\Financial Data Extraction\extracted_financial_data_2.json"

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text() + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

# Function to extract financial entities
def extract_financial_entities(text):
    entities = {
        "Company Name": None,
        "Report Date": None,
        "Profit Before Tax": None,
    }

    # Extract company name (match known company names)
    company_match = re.search(r"(Amara Raja Energy & Mobility Limited|Eveready Industries India Limited)", text, re.IGNORECASE)
    if company_match:
        entities["Company Name"] = company_match.group(1)

    # Extract report date (formats like "Date: 5th February 2025")
    date_match = re.search(r"Date[:\-\s]+(\d{1,2}[\s\-][A-Za-z]+[\s\-]\d{4})", text)
    if date_match:
        entities["Report Date"] = date_match.group(1)

    # Extract profit before tax (look for numeric values after "Profit before tax")
    profit_match = re.search(r"Profit before tax.*?([\d,]+\.?\d*)", text, re.IGNORECASE)
    if profit_match:
        entities["Profit Before Tax"] = profit_match.group(1)

    return entities

# Extract data from PDFs
extracted_data = []
for pdf_name, pdf_path in pdf_files.items():
    pdf_text = extract_text_from_pdf(pdf_path)
    if pdf_text:
        entities = extract_financial_entities(pdf_text)
        entities["File Name"] = pdf_name
        extracted_data.append(entities)

# Save extracted data as JSON
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)

print(f"Extraction complete! JSON file saved at: {output_path}")
