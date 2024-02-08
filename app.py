import os
import pyheif
import img2pdf
from PIL import Image
from io import BytesIO
import PyPDF2
import streamlit as st

def merge_pdfs(pdf_files, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    merger.write(output_file)
    merger.close()

def convert_to_pdf(input_file, output_file):
    heif_file = pyheif.read(input_file)
    img = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    img_buffer = BytesIO()
    img.save(img_buffer, format='JPEG')
    img_bytes = img_buffer.getvalue()

    pdf_bytes = img2pdf.convert(img_bytes)
    with open(output_file, 'wb') as f:
        f.write(pdf_bytes)

def main():
    st.title("HEIC to PDF Converter")

    input_folder = st.text_input("Input Folder Path:")
    output_folder = st.text_input("Output Folder Path:")

    if st.button("Convert HEIC to PDF"):
        heic_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".heic")]
        pdf_files = []

        for heic_path in heic_files:
            output_pdf_path = os.path.join(output_folder, os.path.splitext(os.path.basename(heic_path))[0] + ".pdf")
            convert_to_pdf(heic_path, output_pdf_path)
            pdf_files.append(output_pdf_path)

        combined_pdf_path = os.path.join(output_folder, "combined.pdf")
        merge_pdfs(pdf_files, combined_pdf_path)

        st.success("Conversion complete. Combined PDF saved at: {}".format(combined_pdf_path))

if __name__ == "__main__":
    main()
