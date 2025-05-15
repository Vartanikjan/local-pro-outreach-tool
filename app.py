import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# Mock function to simulate scraping
def mock_scrape(zip_code, profession):
    data = [
        {"Name": "Sarah Kim", "Company": "PNW Realty", "Profession": profession, "Phone": "425-555-7890", "Email": "sarah@pnwrealty.com", "Address": f"123 Main St, {zip_code}", "Website": "pnwrealty.com", "Source": "Mock"},
        {"Name": "John Lee", "Company": "Lakeside Mortgage", "Profession": profession, "Phone": "206-555-1234", "Email": "john@lakesidemortgage.com", "Address": f"456 Elm St, {zip_code}", "Website": "lakesidemortgage.com", "Source": "Mock"},
    ]
    return pd.DataFrame(data)

# Streamlit App UI
st.title("Local Pro Outreach Scraper")
st.write("Enter a ZIP code and profession to generate contact lists.")

zip_code = st.text_input("ZIP Code", "98052")
profession = st.selectbox("Profession", ["Realtor", "Loan Officer", "Property Manager"])

if st.button("Generate Contact List"):
    df = mock_scrape(zip_code, profession)
    st.dataframe(df)

    # Excel export
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, engine='openpyxl')
    excel_file.seek(0)
    st.download_button("Download Excel", data=excel_file, file_name="contacts.xlsx")

    # CSV export
    csv_file = BytesIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)
    st.download_button("Download CSV", data=csv_file, file_name="contacts.csv")

    # PDF export
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i, row in df.iterrows():
        line = ', '.join([f"{col}: {str(row[col])}" for col in df.columns])
        pdf.multi_cell(0, 10, line)
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    st.download_button("Download PDF", data=pdf_output, file_name="contacts.pdf")
