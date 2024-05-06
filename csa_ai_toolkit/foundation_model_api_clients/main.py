#!/usr/bin/env python3

import argparse
import json
#from ai_client import chatgpt, claude
from ai_client import claude, chatgpt, gemini

def get_model_mapping(model_name):
    # ChatGPT model list https://platform.openai.com/docs/models
    # Claude Model list: https://docs.anthropic.com/claude/docs/models-overview
    # Gemini model lisT: https://ai.google.dev/gemini-api/docs/models/gemini

    model_mapping = {
        'chatgpt': 'gpt-4-turbo-preview',
        'claude-haiku': 'claude-3-haiku-20240307',
        'claude-sonnet': 'claude-3-sonnet-20240229',
        'claude-opus': 'claude-3-opus-20240229',
        'gemini': 'gemini-1.5-pro-latest'
        # Add more model mappings as needed
    }
    return model_mapping.get(model_name, model_name)

def main():
    parser = argparse.ArgumentParser(description='AI Client')
    parser.add_argument('--system-prompt', type=str, required=True, help='Path to the file containing the system prompt')
    parser.add_argument('--user-prompt', type=str, required=True, help='Path to the file containing the user content')
    parser.add_argument('--user-data', type=str, required=True, help='Path to additional user data to append to the user prompt')
    parser.add_argument('--output-file', type=str, required=True, help='Output file path to write the response and metadata')
    parser.add_argument('--model', type=str, required=True, help='Model name')
    parser.add_argument('--temperature', type=float, default=1, help='Temperature setting for model (default: 1)')
    parser.add_argument('--max-tokens', type=int, default=4096, help='Maximum number of tokens (default: 4096)')

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

    with open(args.output_file, 'w', encoding='utf-8') as file:
        json.dump(response, file, sort_keys=True, indent=2)

# TODO: add max-tokens check and data to the get_model_mapping() function, error if the number is to high? 
# TOOD: have a --max-tokens of "max"?

# TODO: how to support local testing using pickled AI output? Each client will have to accept the local-testing flag and if set create a pickle file, or use one specified? --create-ai-ouput-test-file and --use-ai-output-test-file?

if __name__ == '__main__':
    main()
    
