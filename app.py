import streamlit as st
import pyodbc
import pandas as pd
from io import BytesIO

# MSSQL database connection parameters
server = 'your_server'
database = 'your_database'
username = 'your_username'
password = 'your_password'
driver = '{ODBC Driver 17 for SQL Server}'

def save_pdf_to_db(pdf_bytes, pdf_name):
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()
    # Create a table if not exists (optional)
    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pdf_files' AND xtype='U')
    CREATE TABLE pdf_files (
        id INT IDENTITY PRIMARY KEY,
        pdf_name NVARCHAR(255),
        pdf_data VARBINARY(MAX)
    )
    ''')
    conn.commit()
    
    # Insert PDF data into table
    cursor.execute("INSERT INTO pdf_files (pdf_name, pdf_data) VALUES (?, ?)", (pdf_name, pdf_bytes))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_pdfs_from_db():
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, pdf_name FROM pdf_files")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_pdf_data_from_db(pdf_id):
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT pdf_data FROM pdf_files WHERE id=?", (pdf_id,))
    pdf_data = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return pdf_data

# Streamlit app
st.title("PDF Management App")

# Radio button to select between uploading and displaying PDFs
option = st.radio("Choose an action", ("Upload PDF", "Display PDFs"))

if option == "Upload PDF":
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Display PDF name
        st.write(f"File name: {uploaded_file.name}")

        # Save PDF to database
        pdf_bytes = uploaded_file.read()
        save_pdf_to_db(pdf_bytes, uploaded_file.name)
        st.success("PDF saved to database successfully!")

        # Optional: Display the uploaded PDF (first page as image)
        st.write("PDF uploaded:")
        with st.expander("See PDF content"):
            st.download_button("Download PDF", pdf_bytes, file_name=uploaded_file.name)

elif option == "Display PDFs":
    # Fetch PDFs from the database
    pdfs = fetch_pdfs_from_db()

    if pdfs:
        # Display list of PDFs with download links
        st.write("Stored PDFs:")
        for pdf_id, pdf_name in pdfs:
            st.write(f"{pdf_name}")
            if st.button(f"Download {pdf_name}", key=pdf_id):
                pdf_data = fetch_pdf_data_from_db(pdf_id)
                st.download_button(f"Download {pdf_name}", pdf_data, file_name=pdf_name)
    else:
        st.write("No PDFs found in the database.")
