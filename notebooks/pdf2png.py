import os
from pdf2image import convert_from_path
from tqdm import tqdm  # Progress bar

# Paths
poppler_path = r"C:\Program Files\poppler-23.11.0\Library\bin"
pdf_folder = r"D:\Y4 Research\nih_pdfs_643_1643"
saving_folder = r"D:\Y4 Research\PNG 2"

# Make sure output folder exists
os.makedirs(saving_folder, exist_ok=True)

# Get list of all PDF files
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

# Loop through each PDF with progress bar
for pdf_file in tqdm(pdf_files, desc="Converting PDFs", unit="pdf"):
    pdf_path = os.path.join(pdf_folder, pdf_file)
    
    try:
        # Convert only the first page to an image
        pages = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path, first_page=1, last_page=1)
        
        # Save the first page as PNG using PDF filename (without extension)
        img_name = os.path.splitext(pdf_file)[0] + ".png"
        save_path = os.path.join(saving_folder, img_name)
        pages[0].save(save_path, "PNG")
        
    except Exception as e:
        print(f"✖ Failed {pdf_file}: {e}")
