# utils.py

import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from all pages.
    """
    text = []
    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        # Iterate through each page in the PDF
        for page in pdf.pages:
            # Extract text from the current page
            page_text = page.extract_text()
            # Only append if text was found on the page
            if page_text:
                text.append(page_text)

    # Join all page texts into a single string separated by newlines
    full_text = "\n".join(text)
    # Clean the combined text before returning
    return clean_text(full_text)


def clean_text(text: str) -> str:
    """
    Basic text cleaning: strip whitespace, normalize spaces, remove empties.
    """
    # Remove leading/trailing spaces and normalize internal whitespace
    cleaned = " ".join(text.split())
    return cleaned
