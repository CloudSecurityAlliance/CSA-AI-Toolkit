#!/usr/bin/env python3

import argparse
import os
import sys
import datetime
import json
import google.generativeai as genai
from google.generativeai import types

class GoogleGeminiChatbot:
    def __init__(self, model, temperature, max_tokens):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.temperature = temperature
        self.max_tokens = max_tokens

    def read_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def create_completion(self, system_prompt_path, user_prompt_path, user_data_path=None):
        system_prompt = self.read_file(system_prompt_path)
        user_prompt = self.read_file(user_prompt_path)

        if user_data_path:
            user_data = self.read_file(user_data_path)
            user_prompt += "\n" + user_data

        prompt_sequence = [
            system_prompt,
            "Understood.",
            user_prompt
        ]

        responses = []
        config = types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=self.max_tokens,
            temperature=self.temperature
        )

        for text in prompt_sequence:
            response = self.model.generate_content(text, generation_config=config)
            responses.append(response.text)

        return responses

    def write_output(self, output_path, args, responses):
        completion = {
            "id": None,  # Gemini API may not return an ID by default
            "model": self.model.model_name,
            "created": datetime.datetime.now().isoformat(),
            "responses": responses
        }

        ai_output = {
            "VENDOR": "Google Gemini",
            "RUNTIME": datetime.datetime.now().isoformat(),
            "SCRIPTNAME": os.path.basename(sys.argv[0]),
            "AIMODEL": self.model.model_name,
            "TEMPERATURE": self.temperature,
            "MAXTOKENS": self.max_tokens,
            "COMPLETION": completion
        }

        ai_output.update(vars(args))  # Merging argparse arguments

        ai_output = {key: value for key, value in ai_output.items() if value is not None}

        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(ai_output, file, sort_keys=True, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Run Google Gemini chatbot with custom prompts and settings.")
    parser.add_argument('--system', type=str, required=True, help='Path to the file containing the system prompt')
    parser.add_argument('--user-prompt', type=str, required=True, help='Path to the file containing the user content')
    parser.add_argument('--user-data', type=str, help='Optional path to additional user data to append to the user prompt')
    parser.add_argument('--output', type=str, required=True, help='Output file path to write the response and metadata')
    parser.add_argument('--model', type=str, default='gemini-pro', help='Model name (default: gemini-pro)')
    parser.add_argument('--temperature', type=float, default=1.0, help='Temperature setting for model (default: 1.0)')
    parser.add_argument('--max_tokens', type=int, default=4096, help='Maximum number of tokens (default: 4096)')

    args = parser.parse_args()

    chatbot = GoogleGeminiChatbot(model=args.model, temperature=args.temperature, max_tokens=args.max_tokens)
    responses = chatbot.create_completion(system_prompt_path=args.system, user_prompt_path=args.user_prompt, user_data_path=args.user_data)
    chatbot.write_output(args.output, args, responses)

if __name__ == "__main__":
    main()
