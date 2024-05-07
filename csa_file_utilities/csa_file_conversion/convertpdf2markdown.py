#!/usr/bin/env python3

import argparse
import os
from PyPDF2 import PdfReader
from markdownify import markdownify as md

class PDFToMarkdownConverter:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        
    def convert_pdf_to_markdown(self):
        """
        Convert a PDF file to Markdown format.
        
        Returns:
            str: Markdown text extracted from the PDF file.
        """
        # Open the PDF file
        with open(self.pdf_path, 'rb') as file:
            reader = PdfReader(file)
            
            # Initialize a variable to store all text
            full_text = ""
            
            # Iterate over each page and extract text
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text
                    
        # Convert extracted text to Markdown
        markdown_text = md(full_text)
        return markdown_text
    
    def save_markdown(self, markdown_text):
        """
        Save the Markdown text to a file.
        
        Args:
            markdown_text (str): Markdown text to be saved.
        """
        # Derive Markdown filename from the original PDF path
        md_filename = os.path.splitext(self.pdf_path)[0] + '.md'
        
        # Save the markdown text to the new file name
        with open(md_filename, 'w') as md_file:
            md_file.write(markdown_text)
            
        print(f"Conversion complete. Markdown file saved as '{md_filename}'.")

def main():
    parser = argparse.ArgumentParser(description='Convert a PDF file to Markdown format.')
    parser.add_argument('pdf_path', metavar='PDF_PATH', type=str, help='Path to the input PDF file')
    args = parser.parse_args()
    
    pdf_path = args.pdf_path
    
    # Check if the input file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist.")
        return
    
    # Check if the input file has a .pdf extension
    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: File '{pdf_path}' is not a PDF file.")
        return
    
    converter = PDFToMarkdownConverter(pdf_path)
    markdown_text = converter.convert_pdf_to_markdown()
    converter.save_markdown(markdown_text)

if __name__ == "__main__":
    main()
