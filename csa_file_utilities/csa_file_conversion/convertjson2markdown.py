#!/usr/bin/env python3

import argparse
import json
import os

class JSONToMarkdownConverter:
    def __init__(self, json_file):
        self.json_file = json_file
        
    def process_element(self, element, indent=0):
        """
        Process an element in the JSON data and convert it to Markdown.
        
        Args:
            element: The element to process (dict, list, or primitive).
            indent (int): The indentation level (default: 0).
            
        Returns:
            str: The Markdown representation of the element.
        """
        md = ""
        indent_str = " " * indent  # Two spaces per indentation level
        
        if isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, (dict, list)):
                    md += f"{indent_str}- **{key}**: \n" + self.process_element(value, indent + 2)
                else:
                    md += f"{indent_str}- **{key}**: {value}\n"
        elif isinstance(element, list):
            for item in element:
                md += f"{indent_str}- " + self.process_element(item, indent + 2).lstrip('- ')
        else:
            md += f"{indent_str}{element}\n"
            
        return md
    
    def convert_json_to_markdown(self):
        """
        Convert the JSON file to Markdown format.
        
        Returns:
            str: The Markdown content converted from the JSON file.
        """
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                
            markdown_content = self.process_element(data)
            return markdown_content
        
        except Exception as e:
            return f"An error occurred: {e}"
    
    def save_markdown(self, markdown_content):
        """
        Save the Markdown content to a file.
        
        Args:
            markdown_content (str): Markdown content to be saved.
        """
        # Derive Markdown filename from the original JSON path
        md_filename = os.path.splitext(self.json_file)[0] + '.md'
        
        # Save the markdown content to the new file name
        with open(md_filename, 'w') as md_file:
            md_file.write(markdown_content)
            
        print(f"Conversion complete. Markdown file saved as '{md_filename}'.")

def main():
    parser = argparse.ArgumentParser(description='Convert a JSON file to Markdown format.')
    parser.add_argument('json_file', metavar='JSON_FILE', type=str, help='Path to the input JSON file')
    args = parser.parse_args()
    
    json_file = args.json_file
    
    # Check if the input file exists
    if not os.path.isfile(json_file):
        print(f"Error: File '{json_file}' does not exist.")
        return
    
    # Check if the input file has a .json extension
    if not json_file.lower().endswith('.json'):
        print(f"Error: File '{json_file}' is not a JSON file.")
        return
    
    converter = JSONToMarkdownConverter(json_file)
    markdown_content = converter.convert_json_to_markdown()
    converter.save_markdown(markdown_content)

if __name__ == "__main__":
    main()
    
