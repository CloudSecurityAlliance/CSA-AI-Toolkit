#!/usr/bin/env python3

import os
import openai
import json
import datetime

def generate_response(model_name, args):
    #
    # FIX THIS!!!!!!! model_name -> model mapping, if chatgpt.... etc?
    #
    model = "gpt-4-0125-preview"
    #
    #
    #
    TIME_START = datetime.datetime.now().isoformat()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = api_key

    with open(args.system, 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()

    with open(args.user_prompt, 'r', encoding='utf-8') as file:
        user_prompt = file.read().strip()

    if args.user_data:
        with open(args.user_data, 'r', encoding='utf-8') as file:
            user_data = file.read().strip()
            user_prompt += "\n" + user_data

    completion = openai.chat.completions.create(
        model=model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    TIME_COMPLETE = datetime.datetime.now().isoformat()

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
        }
    }
    
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

    ai_output = {
        "VENDOR": "OpenAI",
        "AIMODEL": model,
        "TEMPERATURE": args.temperature,
        "MAXTOKENS": args.max_tokens,
        "TOKENS_INPUT": tokens_input,
        "TOKENS_OUTPUT": tokens_output,
        "TOKENS_TOTAL": total_tokens,
        "TIME_START": TIME_START,
        "TIME_COMPLETE": TIME_COMPLETE,
        "COMPLETION": serialized_completion,
        "RESPONSE_TEXT": response_message
    }

    ai_output.update(vars(args))  # Merging argparse arguments

    ai_output = {key: value for key, value in ai_output.items() if value is not None}

    return ai_output
