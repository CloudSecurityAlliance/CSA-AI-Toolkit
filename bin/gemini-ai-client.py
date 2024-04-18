#!/usr/bin/env python3

import google.generativeai as genai
import os
import argparse

# Configure the client with your API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create an instance of the GenerativeModel using the specified model name
model = genai.GenerativeModel('gemini-1.0-pro-latest')

def read_prompt_from_file(file_path):
    """ Reads and returns the content of a text file as a string. """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def send_interaction_sequence(system_prompt, question):
    """ Send a sequence of prompts to the model and collect responses. """
    conversation_history = []

    # Sequence of interactions
    prompt_parts = [
        read_prompt_from_file(system_prompt),  # Read system prompt from file
        "Understood.",  # System acknowledgment
        read_prompt_from_file(question)  # Read user question from file
    ]

    # Send each part of the prompt sequence to the model
    for text in prompt_parts:
        response = model.generate_content(text)
        conversation_history.append(response.text)

    return conversation_history

def write_responses_to_file(responses, file_path):
    """ Writes responses to a specified output file. """
    with open(file_path, 'w', encoding='utf-8') as file:
        for response in responses:
            file.write(response + "\n")

def main():
    parser = argparse.ArgumentParser(description="Generate content using Google Gemini API")
    parser.add_argument("system_prompt_path", type=str, help="File path to the system prompt text")
    parser.add_argument("question_path", type=str, help="File path to the user question text")
    parser.add_argument("-o", "--output", type=str, help="File path to write the output responses")

    args = parser.parse_args()

    # Process the interaction sequence using the provided file paths
    responses = send_interaction_sequence(args.system_prompt_path, args.question_path)

    # Output handling
    if args.output:
        write_responses_to_file(responses, args.output)
    else:
        for response in responses:
            print(response)

if __name__ == "__main__":
    main()
