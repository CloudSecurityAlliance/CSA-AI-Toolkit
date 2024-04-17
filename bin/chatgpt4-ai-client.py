#!/usr/bin/env python3

import argparse
import os
import sys
import datetime
from openai import OpenAI

class OpenAIChatbot:
    def __init__(self, model, temperature, max_tokens):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def read_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def create_completion(self, system_prompt_path, user_prompt_path):
        system_prompt = self.read_file(system_prompt_path)
        user_prompt = self.read_file(user_prompt_path)

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return completion

    def write_output(self, output_path, system_file, user_file, completion):
        response_message = completion.choices[0].message.content
        tokens_input = completion.usage.prompt_tokens
        tokens_output = completion.usage.completion_tokens

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(f"RUNTIME: {datetime.datetime.now().isoformat()}\n")
            file.write(f"SCRIPTNAME: {os.path.basename(sys.argv[0])}\n")
            file.write(f"SYSTEMFILE: {system_file}\n")
            file.write(f"USERFILE: {user_file}\n")
            file.write(f"AIMODEL: {self.model}\n")
            file.write(f"TEMPERATURE: {self.temperature}\n")
            file.write(f"MAXTOKENS: {self.max_tokens}\n")
            file.write(f"TOKENS_INPUT: {tokens_input}\n")
            file.write(f"TOKENS_OUTPUT: {tokens_output}\n")
            file.write(f"RESPONSE_OUTPUT: {response_message}\n")

def main():
    parser = argparse.ArgumentParser(description="Run OpenAI chatbot with custom prompts and settings.")
    parser.add_argument('--system', type=str, required=True, help='Path to the file containing the system prompt')
    parser.add_argument('--user', type=str, required=True, help='Path to the file containing the user content')
    parser.add_argument('--output', type=str, required=True, help='Output file path to write the response and metadata')
    parser.add_argument('--model', type=str, default='gpt-4-0125-preview', help='Model name (default: gpt-4-0125-preview)')
    parser.add_argument('--temperature', type=float, default=1, help='Temperature setting for model (default: 2)')
    parser.add_argument('--max_tokens', type=int, default=4096, help='Maximum number of tokens (default: 4096)')

    args = parser.parse_args()

    chatbot = OpenAIChatbot(model=args.model, temperature=args.temperature, max_tokens=args.max_tokens)
    completion = chatbot.create_completion(system_prompt_path=args.system, user_prompt_path=args.user)
    chatbot.write_output(args.output, args.system, args.user, completion)

if __name__ == "__main__":
    main()
