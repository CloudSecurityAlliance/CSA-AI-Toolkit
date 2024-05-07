#!/usr/bin/env python3

import argparse
import os
import json
from ai_client import claude, chatgpt, gemini

class FoundationModelAPIClient:
    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = self.get_model_api_key()
        self.model_mapping = self.get_model_mapping()

    def get_model_mapping(self):
        model_mapping = {
            'chatgpt': 'gpt-4-turbo-preview',
            'claude': 'claude-3-opus-20240229',
            'claude-haiku': 'claude-3-haiku-20240307',
            'claude-sonnet': 'claude-3-sonnet-20240229',
            'claude-opus': 'claude-3-opus-20240229',
            'gemini': 'gemini-1.5-pro-latest'
        }
        return model_mapping.get(self.model_name, self.model_name)

    def get_model_api_key(self):
        model_api_key = {
            'chatgpt': 'OPENAI_CHATGPT_API_KEY',
            'claude-haiku': 'ANTHROPIC_CLAUDE_API_KEY',
            'claude-sonnet': 'ANTHROPIC_CLAUDE_API_KEY',
            'claude-opus': 'ANTHROPIC_CLAUDE_API_KEY',
            'gemini': 'GOOGLE_GEMINI_API_KEY'
        }
        api_key_env = model_api_key.get(self.model_name, model_api_key)
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ValueError("API KEY environment variable not set.")
        return api_key

    def generate_response(self, system_prompt, user_prompt, user_data, args):
        user_prompt_full = self.prepare_prompt(user_prompt, user_data)
        if self.model_name.startswith('claude'):
            return claude.generate_response(self.model_mapping, self.api_key, system_prompt, user_prompt_full, args)
        elif self.model_name.startswith('chatgpt'):
            return chatgpt.generate_response(self.model_mapping, self.api_key, system_prompt, user_prompt_full, args)
        elif self.model_name.startswith('gemini'):
            return gemini.generate_response(self.model_mapping, self.api_key, system_prompt, user_prompt_full, args)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def prepare_prompt(self, user_prompt, user_data):
        if user_data:
            return f"{user_prompt}\n{user_data}"
        return user_prompt

def main():
    parser = argparse.ArgumentParser(description='AI Model Client')
    parser.add_argument('--system-prompt', type=str, required=True, help='Path to the file containing the system prompt')
    parser.add_argument('--user-prompt', type=str, required=True, help='Path to the file containing the user content')
    parser.add_argument('--user-data', type=str, required=True, help='Path to additional user data to append to the user prompt')
    parser.add_argument('--output-file', type=str, required=True, help='Output file path to write the response and metadata')
    parser.add_argument('--model', type=str, required=True, help='Model name')
    parser.add_argument('--temperature', type=float, default=1, help='Temperature setting for model (default: 1)')
    parser.add_argument('--max-tokens', type=int, default=4096, help='Maximum number of tokens (default: 4096)')

    args = parser.parse_args()
    client = AIModelClient(args.model)

    with open(args.system_prompt, 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()
    with open(args.user_prompt, 'r', encoding='utf-8') as file:
        user_prompt = file.read().strip()
    with open(args.user_data, 'r', encoding='utf-8') as file:
        user_data = file.read().strip()

    response = client.generate_response(system_prompt, user_prompt, user_data, args)
    
    with open(args.output_file, 'w', encoding='utf-8') as file:
        json.dump(response, file, sort_keys=True, indent=2)

if __name__ == '__main__':
    main()
