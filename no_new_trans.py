# convert multiple pages upto 5000 char
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from fpdf import FPDF

def split_text(text, max_length=5000):
    """Split text into smaller chunks of a specified max length."""
    chunks = []
    while len(text) > max_length:
        # Split at the nearest sentence-ending punctuation mark (if possible)
        split_index = text[:max_length].rfind('.')
        if split_index == -1:  # If no sentence-ending punctuation is found
            split_index = max_length
        chunks.append(text[:split_index + 1].strip())
        text = text[split_index + 1:].strip()
    if text:
        chunks.append(text)
    return chunks

# Input PDF file path
input_pdf=input("enter the name of pdf file")
reader = PdfReader('C:\\Users\\DeepakChigal\\Desktop\\python\\data\\' + input_pdf)

# Initialize variable to store all translated text
all_translated_text = ""

# Process all pages in the PDF
for i, page in enumerate(reader.pages):
    print(f"Processing page {i + 1}...")
    text = page.extract_text()
    if text:  # Ensure the page has text
        chunks = split_text(text, max_length=5000)
        for chunk in chunks:
            translated_text = GoogleTranslator(source='auto', target='en').translate(chunk)
            all_translated_text += translated_text + "\n\n"

# Save the translated text to a text file
translated_text_file = "translated_file.txt"
with open(translated_text_file, 'w', encoding='utf-8') as f:
    f.write(all_translated_text)

# Convert the text file into a PDF with Unicode font support
output_pdf_name = "Translated_File.pdf"
pdf = FPDF()
pdf.add_page()

# Add a Unicode-compatible font
pdf.add_font('DejaVu', '', 'C:\\Windows\\Fonts\\DejaVuSans.ttf', uni=True)  # Update path to your TTF file
pdf.set_font("DejaVu", size=10)

with open(translated_text_file, "r", encoding="utf-8") as f:
    for line in f:
        pdf.multi_cell(0, 10, txt=line)  # Use multi_cell to handle text wrapping

pdf.output(output_pdf_name)
print(f"Translation complete! The translated PDF is saved as '{output_pdf_name}'.")
