#!/usr/bin/env python3

import argparse
from ai_client import chatgpt
#from ai_client import claude, chatgpt, gemini

def get_model_mapping(model_name):
    model_mapping = {
        'chatgpt': 'gpt-4-0125-preview',
        'claude-sonnet': 'claude-sonnet-xxx',
        'claude-haiku': 'claude-haiku-xxx',
        # Add more model mappings as needed
    }
    return model_mapping.get(model_name, model_name)

def main():
    parser = argparse.ArgumentParser(description='AI Client')
    parser.add_argument('--system', type=str, required=True, help='Path to the file containing the system prompt')
    parser.add_argument('--user-prompt', type=str, required=True, help='Path to the file containing the user content')
    parser.add_argument('--user-data', type=str, required=True, help='Path to additional user data to append to the user prompt')
    parser.add_argument('--output', type=str, required=True, help='Output file path to write the response and metadata')
    parser.add_argument('--model', type=str, required=True, help='Model name')
    parser.add_argument('--temperature', type=float, default=1, help='Temperature setting for model (default: 1)')
    parser.add_argument('--max_tokens', type=int, default=4096, help='Maximum number of tokens (default: 4096)')

    args = parser.parse_args()

    model_name = get_model_mapping(args.model)

    if args.model.startswith('claude'):
        response = claude.generate_response(model_name, args)
    elif args.model.startswith('chatgpt'):
        response = chatgpt.generate_response(model_name, args)
    elif args.model.startswith('gemini'):
        response = gemini.generate_response(model_name, args)
    else:
        raise ValueError(f"Unsupported model: {args.model}")

    with open(args.output, 'w') as f:
        f.write(response)

if __name__ == '__main__':
    main()
    
