#!/usr/bin/env python3

import argparse
import os
import sys
import datetime
import json
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

    def create_completion(self, system_prompt_path, user_prompt_path, user_data_path=None):
        system_prompt = self.read_file(system_prompt_path)
        user_prompt = self.read_file(user_prompt_path)

        if user_data_path:
            user_data = self.read_file(user_data_path)
            user_prompt += "\n" + user_data

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

    def write_output(self, output_path, args, completion):
        try:
            response_message = completion.choices[0].message.content
        except AttributeError:
            response_message = None

        try:
            tokens_input = completion.usage.prompt_tokens
            tokens_output = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens
        except AttributeError:
            tokens_input = tokens_output = total_tokens = None

        serialized_completion = {
            "id": getattr(completion, 'id', None),
            "model": getattr(completion, 'model', None),
            "created": getattr(completion, 'created', None),
            "system_fingerprint": getattr(completion, 'system_fingerprint', None),
            "choices": [
                {
                    "finish_reason": choice.finish_reason,
                    "index": choice.index,
                    "message": {
                        "content": getattr(choice.message, 'content', None),
                        "role": getattr(choice.message, 'role', None)
                    }
                } for choice in getattr(completion, 'choices', [])
            ] if hasattr(completion, 'choices') else [],
            "usage": {
                "prompt_tokens": tokens_input,
                "completion_tokens": tokens_output,
                "total_tokens": total_tokens
            } if tokens_input is not None and tokens_output is not None else None
        }

        ai_output = {
            "RUNTIME": datetime.datetime.now().isoformat(),
            "SCRIPTNAME": os.path.basename(sys.argv[0]),
            "AIMODEL": self.model,
            "TEMPERATURE": self.temperature,
            "MAXTOKENS": self.max_tokens,
            "TOKENS_INPUT": tokens_input,
            "TOKENS_OUTPUT": tokens_output,
            "COMPLETION": serialized_completion,
            "RESPONSE_TEXT": response_message
        }

        ai_output.update(vars(args))  # Merging argparse arguments

        ai_output = {key: value for key, value in ai_output.items() if value is not None}

        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(ai_output, file, sort_keys=True, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Run OpenAI chatbot with custom prompts and settings.")
    parser.add_argument('--system', type=str, required=True, help='Path to the file containing the system prompt')
    parser.add_argument('--user-prompt', type=str, required=True, help='Path to the file containing the user content')
    parser.add_argument('--user-data', type=str, help='Optional path to additional user data to append to the user prompt')
    parser.add_argument('--output', type=str, required=True, help='Output file path to write the response and metadata')
    parser.add_argument('--model', type=str, default='gpt-4-0125-preview', help='Model name (default: gpt-4-0125-preview)')
    parser.add_argument('--temperature', type=float, default=1, help='Temperature setting for model (default: 1)')
    parser.add_argument('--max_tokens', type=int, default=4096, help='Maximum number of tokens (default: 4096)')

    args = parser.parse_args()

    chatbot = OpenAIChatbot(model=args.model, temperature=args.temperature, max_tokens=args.max_tokens)
    completion = chatbot.create_completion(system_prompt_path=args.system, user_prompt_path=args.user_prompt, user_data_path=args.user_data)
    chatbot.write_output(args.output, args, completion)

if __name__ == "__main__":
    main()
