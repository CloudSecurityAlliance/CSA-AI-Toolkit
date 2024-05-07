#!/usr/bin/env python3

import argparse
import html2text
import os

class HTMLToMarkdownConverter:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def convert_html_to_markdown(self):
        """
        Convert an HTML file to Markdown format.
        
        Returns:
            str: Markdown text converted from the HTML file.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                
            markdown = html2text.html2text(html_content)
            return markdown
        
        except Exception as e:
            return f"An error occurred: {e}"
    
    def save_markdown(self, markdown_content):
        """
        Save the Markdown content to a file.
        
        Args:
            markdown_content (str): Markdown content to be saved.
        """
        # Derive Markdown filename from the original HTML path
        md_filename = os.path.splitext(self.file_path)[0] + '.md'
        
        # Save the markdown content to the new file name
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)
            
        print(f"Conversion complete. Markdown file saved as '{md_filename}'.")

def main():
    parser = argparse.ArgumentParser(description='Convert an HTML file to Markdown format.')
    parser.add_argument('file_path', metavar='FILE_PATH', type=str, help='Path to the input HTML file')
    args = parser.parse_args()
    
    file_path = args.file_path
    
    # Check if the input file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return
    
    # Check if the input file has a .html or .htm extension
    if not (file_path.lower().endswith('.html') or file_path.lower().endswith('.htm')):
        print(f"Error: File '{file_path}' is not an HTML file.")
        return
    
    converter = HTMLToMarkdownConverter(file_path)
    markdown_content = converter.convert_html_to_markdown()
    converter.save_markdown(markdown_content)

if __name__ == "__main__":
    main()
    
